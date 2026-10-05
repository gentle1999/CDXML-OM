from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
REQUIRED_SDIST_ROOT_FILES = (
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "schema/schema.lock.json",
    "tools/__init__.py",
)
SDIST_SOURCE_DIRS = (
    "src/cdxml_om",
    "tools/schema_compiler",
    "tools/schema_importer",
    "schema/canonical",
    "schema/overrides",
    "schema/sources",
)


def _artifact_names(version: str) -> tuple[str, str]:
    return (
        f"cdxml_om-{version}-py3-none-any.whl",
        f"cdxml_om-{version}.tar.gz",
    )


def _filename_version(name: str, fallback: str) -> str:
    if name.startswith("cdxml_om-") and name.endswith(".tar.gz"):
        return name.removeprefix("cdxml_om-").removesuffix(".tar.gz")
    if name.startswith("cdxml_om-") and name.endswith(".whl"):
        stem = name.removeprefix("cdxml_om-").removesuffix(".whl")
        version, separator, _tags = stem.partition("-")
        return version if separator else fallback
    return fallback


def _create_wheel(
    path: Path,
    version: str,
    payload: bytes,
    *,
    metadata_version: str | None = None,
    metadata_name: str = "cdxml-om",
) -> None:
    actual_metadata_version = version if metadata_version is None else metadata_version
    metadata = (
        "Metadata-Version: 2.1\n"
        f"Name: {metadata_name}\n"
        f"Version: {actual_metadata_version}\n"
        "Requires-Dist: lxml\n\n"
    )
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as wheel:
        wheel.writestr("cdxml_om/py.typed", "")
        wheel.writestr("cdxml_om/release-fixture.bin", payload)
        wheel.writestr(f"cdxml_om-{version}.dist-info/METADATA", metadata)


def _sdist_source_files(project: Path) -> list[Path]:
    files = [project / name for name in REQUIRED_SDIST_ROOT_FILES]
    for directory in SDIST_SOURCE_DIRS:
        files.extend(path for path in (project / directory).rglob("*") if path.is_file())
    return sorted(set(files), key=lambda path: path.relative_to(project).as_posix())


def _create_sdist(
    path: Path,
    version: str,
    project: Path,
    payload: bytes,
    *,
    metadata_version: str | None = None,
    metadata_name: str = "cdxml-om",
) -> None:
    root_name = f"cdxml_om-{version}"
    with tarfile.open(path, "w:gz") as archive:
        pkg_info = (
            "Metadata-Version: 2.1\n"
            f"Name: {metadata_name}\n"
            f"Version: {version if metadata_version is None else metadata_version}\n\n"
        ).encode()
        metadata = tarfile.TarInfo(f"{root_name}/PKG-INFO")
        metadata.size = len(pkg_info)
        archive.addfile(metadata, BytesIO(pkg_info))
        for source_path in _sdist_source_files(project):
            relative = source_path.relative_to(project).as_posix()
            file_metadata = tarfile.TarInfo(f"{root_name}/{relative}")
            file_metadata.size = source_path.stat().st_size
            archive.addfile(file_metadata, BytesIO(source_path.read_bytes()))
        fixture_metadata = tarfile.TarInfo(f"{root_name}/release-fixture.bin")
        fixture_metadata.size = len(payload)
        archive.addfile(fixture_metadata, BytesIO(payload))


def _prepare_sdist_tree(project: Path, source_version: str) -> None:
    (project / "schema").mkdir()
    (project / "src/cdxml_om").mkdir(parents=True)
    (project / "LICENSE").write_text("fixture license\n", encoding="utf-8")
    (project / "README.md").write_text("fixture readme\n", encoding="utf-8")
    (project / "pyproject.toml").write_text("[project]\nname='cdxml-om'\n", encoding="utf-8")
    (project / "schema/schema.lock.json").write_text("{}\n", encoding="utf-8")
    (project / "tools/__init__.py").write_text('"""Test tools package."""\n', encoding="utf-8")
    (project / "src/cdxml_om/_version.py").write_text(
        f"__version__ = {source_version!r}\n", encoding="utf-8"
    )
    (project / "src/cdxml_om/__init__.py").write_text(
        'raise RuntimeError("release helper imported the runtime package")\n', encoding="utf-8"
    )
    (project / "src/cdxml_om/py.typed").write_text("", encoding="utf-8")
    for relative in (
        "tools/schema_compiler/fixture.py",
        "tools/schema_importer/fixture.py",
        "schema/canonical/fixture.json",
        "schema/overrides/fixture.yaml",
        "schema/sources/fixture.json",
    ):
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")


def _write_asset(
    project: Path,
    packages: Path,
    name: str,
    payload: bytes,
    fallback_version: str,
    metadata_version: str | None = None,
    metadata_name: str = "cdxml-om",
) -> None:
    path = packages / name
    path.parent.mkdir(parents=True, exist_ok=True)
    version = _filename_version(name, fallback_version)
    if payload == b"malformed-archive":
        path.write_bytes(payload)
    elif name.startswith("cdxml_om-") and name.endswith(".whl"):
        _create_wheel(
            path,
            version,
            payload,
            metadata_version=metadata_version,
            metadata_name=metadata_name,
        )
    elif name.startswith("cdxml_om-") and name.endswith(".tar.gz"):
        _create_sdist(
            path,
            version,
            project,
            payload,
            metadata_version=metadata_version,
            metadata_name=metadata_name,
        )
    else:
        path.write_bytes(payload)


def _run_release_helper(
    tmp_path: Path,
    *,
    source_version: str,
    tag: str,
    assets: dict[str, bytes],
    existing_output: str = "",
    github_output_inside_bundle: bool = False,
    github_output_hardlink_to: str | None = None,
    metadata_versions: dict[str, str] | None = None,
    metadata_names: dict[str, str] | None = None,
) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path]:
    project = tmp_path / "checkout"
    (project / "tools").mkdir(parents=True)
    shutil.copy2(TOOLS / "release.py", project / "tools" / "release.py")
    shutil.copy2(TOOLS / "check_package.py", project / "tools" / "check_package.py")
    _prepare_sdist_tree(project, source_version)

    bundle = tmp_path / "release-bundle"
    packages = bundle / "packages"
    packages.mkdir(parents=True)
    for name, payload in assets.items():
        _write_asset(
            project,
            packages,
            name,
            payload,
            source_version,
            (metadata_versions or {}).get(name),
            (metadata_names or {}).get(name, "cdxml-om"),
        )
    if github_output_inside_bundle:
        github_output = bundle / "github-output"
        github_output.write_text(existing_output, encoding="utf-8")
    else:
        github_output = tmp_path / "github-output"
        if github_output_hardlink_to is None:
            github_output.write_text(existing_output, encoding="utf-8")
        else:
            aliased_package = packages / github_output_hardlink_to
            (tmp_path / "github-output-original").write_bytes(aliased_package.read_bytes())
            os.link(aliased_package, github_output)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.release",
            "--tag",
            tag,
            "--packages-dir",
            str(packages),
            "--bundle-dir",
            str(bundle),
            "--github-output",
            str(github_output),
        ],
        cwd=project,
        capture_output=True,
        check=False,
        text=True,
    )
    return result, bundle, packages, github_output


def _read_outputs(path: Path) -> dict[str, str]:
    return dict(
        line.split("=", maxsplit=1) for line in path.read_text(encoding="utf-8").splitlines()
    )


def test_release_helper_writes_sorted_checksums_and_outputs_without_runtime_import(
    tmp_path: Path,
) -> None:
    wheel_name, sdist_name = _artifact_names("1.2.3")
    result, bundle, packages, github_output = _run_release_helper(
        tmp_path,
        source_version="1.2.3",
        tag="v1.2.3",
        assets={wheel_name: b"wheel fixture", sdist_name: b"sdist fixture"},
        existing_output="previous=value\n",
    )

    assert result.returncode == 0, result.stderr
    expected_lines = [
        f"{hashlib.sha256((packages / name).read_bytes()).hexdigest()}  packages/{name}"
        for name in sorted((wheel_name, sdist_name))
    ]
    assert (bundle / "SHA256SUMS").read_text(encoding="ascii").splitlines() == expected_lines
    assert not (packages / "SHA256SUMS").exists()
    bundle_files = {
        path.relative_to(bundle).as_posix() for path in bundle.rglob("*") if path.is_file()
    }
    assert bundle_files == {
        "SHA256SUMS",
        *(f"packages/{name}" for name in (wheel_name, sdist_name)),
    }
    assert _read_outputs(github_output) == {
        "previous": "value",
        "tag": "v1.2.3",
        "version": "1.2.3",
        "prerelease": "false",
    }


@pytest.mark.parametrize(
    ("version", "expected_prerelease"),
    [
        ("1.2.3", "false"),
        ("1!1.2.3", "false"),
        ("1.2.3.post1", "false"),
        ("1.2.3.dev1", "true"),
        ("1.2.3a1", "true"),
        ("1.2.3b2", "true"),
        ("1.2.3rc1", "true"),
    ],
)
def test_release_helper_classifies_canonical_pep440_prereleases(
    tmp_path: Path,
    version: str,
    expected_prerelease: str,
) -> None:
    wheel_name, sdist_name = _artifact_names(version)
    result, _, _, github_output = _run_release_helper(
        tmp_path,
        source_version=version,
        tag=f"v{version}",
        assets={wheel_name: b"wheel", sdist_name: b"sdist"},
    )

    assert result.returncode == 0, result.stderr
    output = _read_outputs(github_output)
    assert output["version"] == version
    assert output["prerelease"] == expected_prerelease
    assert output["tag"] == f"v{version}"


@pytest.mark.parametrize(
    ("source_version", "tag"),
    [
        ("1.2.3+local", "v1.2.3+local"),
        ("1.2.3RC1", "v1.2.3RC1"),
        ("1.2.3", "refs/tags/v1.2.3"),
        ("1.2.3", "v1.2.3/../../other"),
        ("1.2.3", "v1.2.3; touch injected"),
        ("1.2.3", "v1.2.4"),
        ("1.2.3; touch injected", "v1.2.3; touch injected"),
    ],
)
def test_release_helper_rejects_noncanonical_versions_and_unsafe_or_mismatched_tags(
    tmp_path: Path,
    source_version: str,
    tag: str,
) -> None:
    wheel_name, sdist_name = _artifact_names("1.2.3")
    result, bundle, _, github_output = _run_release_helper(
        tmp_path,
        source_version=source_version,
        tag=tag,
        assets={wheel_name: b"wheel", sdist_name: b"sdist"},
    )

    assert result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    assert github_output.read_text(encoding="utf-8") == ""
    assert not (tmp_path / "checkout" / "injected").exists()


@pytest.mark.parametrize(
    "assets",
    [
        {},
        {"cdxml_om-1.2.3.tar.gz": b"sdist only"},
        {"cdxml_om-1.2.3-py3-none-any.whl": b"wheel only"},
        {
            "cdxml_om-1.2.3-py3-none-any.whl": b"wheel",
            "cdxml_om-1.2.3-py3-none-any.whl.backup": b"extra",
            "cdxml_om-1.2.3.tar.gz": b"sdist",
        },
        {
            "cdxml_om-1.2.3-py3-none-any.whl": b"wheel",
            "cdxml_om-1.2.3.tar.gz": b"sdist",
            "unexpected.txt": b"extra",
        },
        {
            "cdxml_om-1.2.3-py3-none-any\n.whl": b"control character in wheel tag",
            "cdxml_om-1.2.3.tar.gz": b"sdist",
        },
        {
            "cdxml_om-1.2.3-py3-none-any.whl": b"malformed-archive",
            "cdxml_om-1.2.3.tar.gz": b"sdist",
        },
        {
            "cdxml_om-1.2.3-py3-none-any.whl": b"wheel",
            "cdxml_om-1.2.3.tar.gz": b"malformed-archive",
        },
        {
            "cdxml_om-1.2.4-py3-none-any.whl": b"wrong wheel version",
            "cdxml_om-1.2.3.tar.gz": b"sdist",
        },
        {
            "cdxml_om-1.2.3-py3-none-any.whl": b"wheel",
            "cdxml_om-1.2.4.tar.gz": b"wrong sdist version",
        },
        {"not-a-wheel.whl": b"malformed", "not-an-sdist.tar.gz": b"malformed"},
    ],
)
def test_release_helper_rejects_missing_extra_malformed_or_mismatched_assets(
    tmp_path: Path,
    assets: dict[str, bytes],
) -> None:
    result, bundle, _, github_output = _run_release_helper(
        tmp_path,
        source_version="1.2.3",
        tag="v1.2.3",
        assets=assets,
    )

    assert result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    assert github_output.read_text(encoding="utf-8") == ""
    if b"malformed-archive" in assets.values():
        assert "Traceback" not in result.stderr
        assert "Release validation failed" in result.stderr


@pytest.mark.parametrize(
    ("artifact_kind", "metadata_field", "bad_value"),
    [
        ("wheel", "name", "other-project"),
        ("sdist", "name", "other-project"),
        ("wheel", "version", "1.2.4"),
        ("sdist", "version", "1.2.4"),
    ],
)
def test_release_helper_rejects_artifact_metadata_name_or_version_mismatch_atomically(
    tmp_path: Path,
    artifact_kind: str,
    metadata_field: str,
    bad_value: str,
) -> None:
    wheel_name, sdist_name = _artifact_names("1.2.3")
    target_name = wheel_name if artifact_kind == "wheel" else sdist_name
    result, bundle, _, github_output = _run_release_helper(
        tmp_path,
        source_version="1.2.3",
        tag="v1.2.3",
        assets={wheel_name: b"wheel", sdist_name: b"sdist"},
        metadata_names={target_name: bad_value} if metadata_field == "name" else None,
        metadata_versions={target_name: bad_value} if metadata_field == "version" else None,
    )
    assert result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    assert github_output.read_text(encoding="utf-8") == ""


def test_release_helper_rejects_nested_or_symlinked_package_entries_atomically(
    tmp_path: Path,
) -> None:
    wheel_name, sdist_name = _artifact_names("1.2.3")
    result, bundle, packages, github_output = _run_release_helper(
        tmp_path,
        source_version="1.2.3",
        tag="v1.2.3",
        assets={wheel_name: b"wheel", sdist_name: b"sdist"},
    )
    assert result.returncode == 0, result.stderr

    # A second invocation must not replace a published manifest or append outputs.
    manifest_before = (bundle / "SHA256SUMS").read_bytes()
    output_before = github_output.read_bytes()
    rerun = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.release",
            "--tag",
            "v1.2.3",
            "--packages-dir",
            str(packages),
            "--bundle-dir",
            str(bundle),
            "--github-output",
            str(github_output),
        ],
        cwd=tmp_path / "checkout",
        capture_output=True,
        check=False,
        text=True,
    )
    assert rerun.returncode != 0
    assert (bundle / "SHA256SUMS").read_bytes() == manifest_before
    assert github_output.read_bytes() == output_before

    (bundle / "SHA256SUMS").unlink()
    nested = packages / "nested"
    nested.mkdir()
    nested_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.release",
            "--tag",
            "v1.2.3",
            "--packages-dir",
            str(packages),
            "--bundle-dir",
            str(bundle),
            "--github-output",
            str(github_output),
        ],
        cwd=tmp_path / "checkout",
        capture_output=True,
        check=False,
        text=True,
    )
    assert nested_result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    assert github_output.read_bytes() == output_before

    nested.rmdir()
    link = packages / "extra.whl"
    link.symlink_to(packages / wheel_name)
    linked_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.release",
            "--tag",
            "v1.2.3",
            "--packages-dir",
            str(packages),
            "--bundle-dir",
            str(bundle),
            "--github-output",
            str(github_output),
        ],
        cwd=tmp_path / "checkout",
        capture_output=True,
        check=False,
        text=True,
    )
    assert linked_result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    assert github_output.read_bytes() == output_before


@pytest.mark.parametrize("output_location", ["inside_bundle", "hardlink_to_wheel"])
def test_release_helper_rejects_github_output_aliases_before_writing(
    tmp_path: Path,
    output_location: str,
) -> None:
    wheel_name, sdist_name = _artifact_names("1.2.3")
    result, bundle, packages, github_output = _run_release_helper(
        tmp_path,
        source_version="1.2.3",
        tag="v1.2.3",
        assets={wheel_name: b"wheel", sdist_name: b"sdist"},
        existing_output="unchanged\n",
        github_output_inside_bundle=output_location == "inside_bundle",
        github_output_hardlink_to=wheel_name if output_location == "hardlink_to_wheel" else None,
    )

    assert result.returncode != 0
    assert not (bundle / "SHA256SUMS").exists()
    if output_location == "inside_bundle":
        assert github_output.read_text(encoding="utf-8") == "unchanged\n"
    else:
        assert github_output.samefile(packages / wheel_name)
        original_wheel = (tmp_path / "github-output-original").read_bytes()
        assert (packages / wheel_name).read_bytes() == original_wheel
