"""Validate tag/version correspondence and prepare an immutable release bundle."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tarfile
from pathlib import Path
from zipfile import BadZipFile

from packaging.utils import (
    InvalidSdistFilename,
    InvalidWheelFilename,
    parse_sdist_filename,
    parse_wheel_filename,
)
from packaging.version import InvalidVersion, Version

from tools.check_package import (
    PackageCheckError,
    read_source_version,
    verify_sdist,
    verify_wheel,
)


class ReleaseError(ValueError):
    """A release tag or distribution bundle failed validation."""


_SAFE_PACKAGE_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._!-]*\Z", re.ASCII)


def validate_tag(tag: str, source_version: str) -> tuple[str, bool]:
    """Require a canonical ``v<PEP 440 version>`` tag matching the source."""
    try:
        parsed = Version(source_version)
    except InvalidVersion as exc:
        raise ReleaseError(f"source version is not valid PEP 440: {source_version!r}") from exc

    if str(parsed) != source_version:
        raise ReleaseError(
            f"source version is not canonical PEP 440: {source_version!r} "
            f"(canonical form is {str(parsed)!r})"
        )
    if parsed.local is not None:
        raise ReleaseError("local-version identifiers are not allowed for public releases")
    expected_tag = f"v{source_version}"
    if tag != expected_tag:
        raise ReleaseError(f"tag {tag!r} must exactly match the source version as {expected_tag!r}")
    return source_version, parsed.is_prerelease


def _distribution_files(packages_dir: Path) -> tuple[Path, Path]:
    package_paths = sorted(packages_dir.iterdir(), key=lambda path: path.name)
    if len(package_paths) != 2 or any(
        path.is_symlink() or not path.is_file() for path in package_paths
    ):
        raise ReleaseError("packages directory must contain only one wheel and one sdist")
    if any(_SAFE_PACKAGE_FILENAME.fullmatch(path.name) is None for path in package_paths):
        raise ReleaseError(
            "distribution filenames must contain only safe ASCII filename characters"
        )

    wheels = [path for path in package_paths if path.name.endswith(".whl")]
    sdists = [path for path in package_paths if path.name.endswith(".tar.gz")]
    if len(wheels) != 1 or len(sdists) != 1:
        raise ReleaseError("packages directory must contain exactly one .whl and one .tar.gz")
    return wheels[0], sdists[0]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _checked_paths(packages_dir: Path, bundle_dir: Path) -> tuple[Path, Path, Path]:
    try:
        resolved_bundle = bundle_dir.resolve(strict=True)
        resolved_packages = packages_dir.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ReleaseError(f"release bundle directories must already exist: {exc}") from exc
    if not resolved_bundle.is_dir() or not resolved_packages.is_dir():
        raise ReleaseError("release bundle and packages paths must be directories")
    if resolved_packages.name != "packages" or resolved_packages.parent != resolved_bundle:
        raise ReleaseError("packages directory must be the direct 'packages' child of bundle-dir")
    manifest_path = resolved_bundle / "SHA256SUMS"
    if manifest_path.exists() or manifest_path.is_symlink():
        raise ReleaseError(f"refusing to overwrite existing checksum manifest: {manifest_path}")
    return resolved_bundle, resolved_packages, manifest_path


def _validate_github_output(path: Path | None, manifest_path: Path) -> Path | None:
    if path is None:
        return None
    if path.is_symlink() or not path.is_file():
        raise ReleaseError(f"GitHub output must be an existing regular file: {path}")
    resolved = path.resolve()
    if resolved.is_relative_to(manifest_path.parent):
        raise ReleaseError("GitHub output path must be outside the release bundle")
    packages_dir = manifest_path.parent / "packages"
    try:
        aliases_package = any(resolved.samefile(candidate) for candidate in packages_dir.iterdir())
    except OSError as exc:
        raise ReleaseError(f"could not inspect packages directory: {exc}") from exc
    if aliases_package:
        raise ReleaseError("GitHub output path cannot be a hardlink to a release package")
    return resolved


def verify_packages(packages_dir: Path, expected_version: str) -> tuple[Path, Path]:
    """Verify the exact package pair using the package checker primitives."""
    wheel_path, sdist_path = _distribution_files(packages_dir)
    try:
        wheel_name, wheel_filename_version, _, _ = parse_wheel_filename(wheel_path.name)
        sdist_name, sdist_filename_version = parse_sdist_filename(sdist_path.name)
    except (InvalidSdistFilename, InvalidWheelFilename) as exc:
        raise ReleaseError(f"distribution filename is invalid: {exc}") from exc
    if wheel_name != "cdxml-om" or sdist_name != "cdxml-om":
        raise ReleaseError("wheel and sdist filenames must identify the cdxml-om project")
    version_object = Version(expected_version)
    if wheel_filename_version != version_object or sdist_filename_version != version_object:
        raise ReleaseError("wheel and sdist filenames must match the source version")
    try:
        wheel_version = verify_wheel(wheel_path, expected_version=expected_version)
        sdist_version = verify_sdist(sdist_path, expected_version=expected_version)
    except (
        PackageCheckError,
        BadZipFile,
        EOFError,
        KeyError,
        tarfile.TarError,
        UnicodeDecodeError,
    ) as exc:
        raise ReleaseError(f"distribution validation failed: {exc}") from exc
    if wheel_version != sdist_version:
        raise ReleaseError(
            f"wheel version {wheel_version!r} does not match sdist version {sdist_version!r}"
        )
    return wheel_path, sdist_path


def create_checksums(
    packages_dir: Path,
    bundle_dir: Path,
    *,
    expected_version: str,
) -> Path:
    """Validate package bytes, then create a non-overwriting GNU sha256 manifest."""
    _, resolved_packages, manifest_path = _checked_paths(packages_dir, bundle_dir)
    wheel_path, sdist_path = verify_packages(resolved_packages, expected_version)
    entries = sorted((wheel_path, sdist_path), key=lambda path: path.name)
    manifest = "".join(f"{_sha256(path)}  packages/{path.name}\n" for path in entries)
    try:
        with manifest_path.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(manifest)
    except OSError as exc:
        raise ReleaseError(f"could not write checksum manifest {manifest_path}: {exc}") from exc
    return manifest_path


def _write_github_output(path: Path | None, *, tag: str, version: str, prerelease: bool) -> None:
    if path is None:
        return
    try:
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"tag={tag}\nversion={version}\nprerelease={str(prerelease).lower()}\n")
    except OSError as exc:
        raise ReleaseError(f"could not write GitHub Actions outputs to {path}: {exc}") from exc


def prepare_release_bundle(
    tag: str,
    packages_dir: Path,
    bundle_dir: Path,
    *,
    github_output: Path | None = None,
) -> tuple[str, bool, Path]:
    """Validate source/tag/packages and only then write manifest and outputs."""
    source_version = read_source_version()
    version, prerelease = validate_tag(tag, source_version)
    _, _, manifest_path = _checked_paths(packages_dir, bundle_dir)
    output_path = _validate_github_output(github_output, manifest_path)
    manifest_path = create_checksums(packages_dir, bundle_dir, expected_version=version)
    _write_github_output(output_path, tag=tag, version=version, prerelease=prerelease)
    return version, prerelease, manifest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="tag name, exactly v plus the source version")
    parser.add_argument("--packages-dir", type=Path, required=True)
    parser.add_argument("--bundle-dir", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)
    try:
        version, prerelease, manifest = prepare_release_bundle(
            args.tag,
            args.packages_dir,
            args.bundle_dir,
            github_output=args.github_output,
        )
    except (OSError, PackageCheckError, ReleaseError) as exc:
        print(f"Release validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Validated release {args.tag}: version={version}, prerelease={str(prerelease).lower()}")
    print(f"Checksum manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
