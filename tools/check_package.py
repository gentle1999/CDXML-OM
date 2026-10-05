"""Build and verify the distributable package without development dependencies."""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from email.parser import Parser
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from packaging.utils import canonicalize_name

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
_PURE_EXTRA_MARKER = re.compile(
    r"^extra\s*==\s*(['\"])([A-Za-z0-9][A-Za-z0-9._-]*)\1$", re.IGNORECASE
)
_CACHE_DIRECTORIES = {"__pycache__", ".hypothesis", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
IMPORT_CHECK = """
from importlib.metadata import distribution, distributions
from importlib.util import find_spec
from pathlib import Path
import sys

import cdxml_om
from cdxml_om import (
    Bond,
    BondDisplay,
    BondOrder,
    CDXMLDocument,
    ElementList,
    Fragment,
    GenericList,
    Node,
    Page,
    Point2D,
    Point3D,
    TagType,
)
from cdxml_om._generated.schema_metadata import OBJECT_METADATA

assert Bond.__spec_id__ == "bond"
assert Fragment.__spec_id__ == "fragment"
assert Node.__spec_id__ == "node"
assert Page.__spec_id__ == "page"
assert BondOrder.SINGLE | BondOrder.DOUBLE == 3
assert BondDisplay.SOLID.value == 0
assert len(OBJECT_METADATA) == 53
for spec_id, metadata in OBJECT_METADATA.items():
    assert metadata.python_name in cdxml_om.__all__, metadata.python_name
    public_model = getattr(cdxml_om, metadata.python_name)
    assert public_model.__spec_id__ == spec_id

blocked = {
    "hypothesis",
    "ipykernel",
    "mypy",
    "nbclient",
    "nbformat",
    "packaging",
    "pyright",
    "pytest",
    "pytest-cov",
    "pyyaml",
    "rdkit",
    "ruff",
    "types-pyyaml",
}
installed = {
    item.metadata["Name"].lower().replace("_", "-").replace(".", "-")
    for item in distributions()
    if item.metadata.get("Name")
}
assert not blocked.intersection(installed), blocked.intersection(installed)
package_path = Path(cdxml_om.__file__).resolve()
assert Path(sys.prefix).resolve() in package_path.parents
assert package_path.parent == Path(distribution("cdxml-om").locate_file("cdxml_om")).resolve()
assert cdxml_om.__version__ == distribution("cdxml-om").version
assert find_spec("tools") is None
for module in (
    "hypothesis",
    "ipykernel",
    "mypy",
    "nbclient",
    "nbformat",
    "packaging",
    "pyright",
    "pytest",
    "ruff",
    "yaml",
    "rdkit",
):
    assert find_spec(module) is None, module

source = (
    '<CDXML><fonttable><font id="100" name="Test Font" '
    'charset="iso-8859-1"/></fonttable><page id="1"><fragment id="2">'
    '<n id="3" Element="6" ElementList="NOT 9 17" GenericList="NOT R X"/>'
    '<n id="4" Element="8"/><b id="5" B="3" E="4" Order="1"/>'
    '</fragment><curve id="6" CurvePoints="1 2 3 4" '
    'CurvePoints3D="1 2 3 4 5 6"/>'
    '<objecttag id="7" Name="measurement" TagType="Double" Value="1.25"/>'
    '<spectrum id="8">left<objecttag Name="metadata" TagType="String" '
    'Value="nested">nested label</objecttag>right</spectrum>'
    '</page></CDXML>'
)
document = CDXMLDocument.from_string(source)
fragment = document.pages[0].fragments[0]
node = document.get(Node, 3)
bond = document.get(Bond, 5)
assert node is not None and bond is not None
assert fragment.nodes[0] is node
assert bond.begin is node
assert isinstance(document.root, cdxml_om.CDXMLRoot)
assert document.root.pages[0] is document.pages[0]
font = document.font_table.fonts[0]
assert font.charset == "iso-8859-1"
assert node.element_list == ElementList((9, 17), negated=True)
assert node.generic_list == GenericList(("R", "X"), negated=True)
curve = document.wrap(document.tree.xpath("//curve")[0])
assert isinstance(curve, cdxml_om.Curve)
assert curve.curve_points == (Point2D(1.0, 2.0), Point2D(3.0, 4.0))
assert curve.curve_points3_d == (Point3D(1.0, 2.0, 3.0), Point3D(4.0, 5.0, 6.0))
object_tag = document.wrap(document.tree.xpath("//objecttag[@Name='measurement']")[0])
assert isinstance(object_tag, cdxml_om.ObjectTag)
assert object_tag.tag_type == TagType.DOUBLE
assert object_tag.value == 1.25
spectrum = document.wrap(document.tree.xpath("//spectrum")[0])
assert isinstance(spectrum, cdxml_om.Spectrum)
assert spectrum.data == "leftright"
spectrum_child = spectrum.raw_element[0]
node.charge = 1
node.element_list = ElementList((8, 26))
node.generic_list = GenericList(("R", "Y"))
curve.curve_points = (Point2D(7.0, 8.0), Point2D(9.0, 10.0))
curve.curve_points3_d = (Point3D(7.0, 8.0, 9.0),)
object_tag.value = 2.5
spectrum.data = "replacement"
assert spectrum.raw_element[0] is spectrum_child
created_node = fragment.nodes.create(element=8, position=(2.0, 3.0))
created_bond = fragment.bonds.create(begin=node, end=created_node, order=2)
assert bond.begin is node

reparsed = CDXMLDocument.from_string(document.to_string())
reparsed_node = reparsed.get(Node, 3)
reparsed_created_node = reparsed.get(Node, created_node.id)
reparsed_created_bond = reparsed.get(Bond, created_bond.id)
assert reparsed_node is not None and reparsed_created_node is not None
assert reparsed_created_bond is not None
assert reparsed_node.charge == 1
assert reparsed_node.element_list == ElementList((8, 26))
assert reparsed_node.generic_list == GenericList(("R", "Y"))
reparsed_curve = reparsed.wrap(reparsed.tree.xpath("//curve")[0])
assert reparsed_curve.curve_points == (Point2D(7.0, 8.0), Point2D(9.0, 10.0))
assert reparsed_curve.curve_points3_d == (Point3D(7.0, 8.0, 9.0),)
reparsed_font = reparsed.font_table.fonts[0]
assert reparsed_font.charset == "iso-8859-1"
reparsed_object_tag = reparsed.wrap(
    reparsed.tree.xpath("//objecttag[@Name='measurement']")[0]
)
assert reparsed_object_tag.value == 2.5
reparsed_spectrum = reparsed.wrap(reparsed.tree.xpath("//spectrum")[0])
assert reparsed_spectrum.data == "replacement"
assert reparsed_spectrum.raw_element[0].text == "nested label"
assert reparsed_created_bond.begin is reparsed_node
assert reparsed_created_bond.end is reparsed_created_node
"""


class PackageCheckError(RuntimeError):
    """Raised when a built distribution does not meet package guarantees."""


def _version_from_text(text: str, *, source: str) -> str:
    try:
        module = ast.parse(text, filename=source)
    except SyntaxError as exc:
        raise PackageCheckError(f"could not parse version source {source}: {exc}") from exc

    matches: list[str] = []
    for statement in module.body:
        target: ast.expr | None = None
        value: ast.expr | None = None
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target = statement.targets[0]
            value = statement.value
        elif isinstance(statement, ast.AnnAssign):
            target = statement.target
            value = statement.value
        if isinstance(target, ast.Name) and target.id == "__version__":
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                raise PackageCheckError(f"{source} must assign __version__ a literal string")
            matches.append(value.value)
    if len(matches) != 1:
        raise PackageCheckError(
            f"expected one literal __version__ assignment in {source}, found {len(matches)}"
        )
    return matches[0]


def read_source_version(path: Path = PROJECT_ROOT / "src/cdxml_om/_version.py") -> str:
    """Read the canonical version without importing the package runtime."""
    return _version_from_text(path.read_text(encoding="utf-8"), source=str(path))


def required_sdist_files(root: Path = PROJECT_ROOT) -> frozenset[str]:
    """Return files needed to install the package and rebuild generated schema."""
    required = {
        "LICENSE",
        "README.md",
        "pyproject.toml",
        "schema/schema.lock.json",
        "tools/__init__.py",
    }
    for relative_directory in (
        "src/cdxml_om",
        "tools/schema_compiler",
        "tools/schema_importer",
        "schema/canonical",
        "schema/overrides",
        "schema/sources",
    ):
        directory = root / relative_directory
        required.update(
            path.relative_to(root).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
            and not _CACHE_DIRECTORIES.intersection(path.relative_to(root).parts)
            and path.suffix not in {".pyc", ".pyo"}
        )
    return frozenset(required)


def verify_mandatory_requirements(
    requirements: list[str], *, optional_extras: frozenset[str] = frozenset({"dev"})
) -> None:
    """Require lxml to be the only mandatory wheel dependency.

    Requirements guarded only by a declared optional extra are optional. Other
    environment markers are treated as mandatory conservatively.
    """
    mandatory_names: list[str] = []
    for requirement in requirements:
        base, separator, marker = requirement.partition(";")
        optional_marker = _PURE_EXTRA_MARKER.fullmatch(marker.strip()) if separator else None
        if optional_marker is not None and optional_marker.group(2) in optional_extras:
            continue
        name_match = _REQUIREMENT_NAME.match(base)
        if name_match is None:
            raise PackageCheckError(f"could not parse dependency requirement {requirement!r}")
        normalized_name = re.sub(r"[-_.]+", "-", name_match.group(1)).lower()
        mandatory_names.append(normalized_name)

    if mandatory_names != ["lxml"]:
        raise PackageCheckError(
            f"expected only lxml as a mandatory requirement, found {mandatory_names!r}"
        )


def verify_wheel(wheel_path: Path, *, expected_version: str | None = None) -> str:
    """Check wheel version, typing marker, and runtime dependency metadata."""
    with ZipFile(wheel_path) as wheel:
        members = set(wheel.namelist())
        if "cdxml_om/py.typed" not in members:
            raise PackageCheckError("wheel is missing cdxml_om/py.typed")

        metadata_paths = [name for name in members if name.endswith(".dist-info/METADATA")]
        if len(metadata_paths) != 1:
            raise PackageCheckError(f"expected one wheel METADATA file, found {metadata_paths!r}")
        metadata_text = wheel.read(metadata_paths[0]).decode("utf-8")

    metadata = Parser().parsestr(metadata_text)
    package_name = metadata.get("Name")
    if package_name is None or canonicalize_name(package_name) != "cdxml-om":
        raise PackageCheckError(
            f"wheel distribution name must be 'cdxml-om', found {package_name!r}"
        )
    verify_mandatory_requirements(
        metadata.get_all("Requires-Dist", []),
        optional_extras=frozenset(metadata.get_all("Provides-Extra", [])),
    )
    version = metadata.get("Version")
    if not version:
        raise PackageCheckError("wheel METADATA is missing Version")
    if expected_version is not None and version != expected_version:
        raise PackageCheckError(
            f"wheel version {version!r} does not match source version {expected_version!r}"
        )
    return version


def verify_sdist(sdist_path: Path, *, expected_version: str | None = None) -> str:
    """Check sdist contents and ensure metadata/source carry one version."""
    with tarfile.open(sdist_path, mode="r:gz") as sdist:
        members = {member.name: member for member in sdist.getmembers() if member.isfile()}
        files = [PurePosixPath(name) for name in members]
    roots = {path.parts[0] for path in files if path.parts}
    if len(roots) != 1:
        raise PackageCheckError(f"expected one sdist root directory, found {sorted(roots)!r}")
    root = next(iter(roots))
    included = {
        PurePosixPath(*path.parts[1:]).as_posix()
        for path in files
        if path.parts and path.parts[0] == root
    }
    missing = sorted(required_sdist_files() - included)
    if missing:
        raise PackageCheckError(f"sdist is missing essential project files: {missing!r}")

    metadata_path = f"{root}/PKG-INFO"
    version_source_path = f"{root}/src/cdxml_om/_version.py"
    if metadata_path not in members:
        raise PackageCheckError("sdist is missing PKG-INFO")
    if version_source_path not in members:
        raise PackageCheckError("sdist is missing the canonical package version source")

    with tarfile.open(sdist_path, mode="r:gz") as sdist:
        metadata_member = sdist.extractfile(metadata_path)
        version_member = sdist.extractfile(version_source_path)
        if metadata_member is None or version_member is None:
            raise PackageCheckError("sdist version files could not be read")
        metadata = Parser().parsestr(metadata_member.read().decode("utf-8"))
        source_version = _version_from_text(
            version_member.read().decode("utf-8"), source=version_source_path
        )

    package_name = metadata.get("Name")
    if package_name is None or canonicalize_name(package_name) != "cdxml-om":
        raise PackageCheckError(
            f"sdist distribution name must be 'cdxml-om', found {package_name!r}"
        )
    metadata_version = metadata.get("Version")
    if not metadata_version:
        raise PackageCheckError("sdist PKG-INFO is missing Version")
    if metadata_version != source_version:
        raise PackageCheckError(
            f"sdist PKG-INFO version {metadata_version!r} does not match its source version "
            f"{source_version!r}"
        )
    if expected_version is not None and metadata_version != expected_version:
        raise PackageCheckError(
            f"sdist version {metadata_version!r} does not match source version {expected_version!r}"
        )
    return metadata_version


def _run(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def _venv_python(venv_path: Path) -> Path:
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def verify_package(dist_dir: Path | None = None) -> None:
    uv = shutil.which("uv")
    if uv is None:
        raise PackageCheckError("uv must be installed and available on PATH")

    with tempfile.TemporaryDirectory(prefix="cdxml-om-package-check-") as temporary:
        temporary_path = Path(temporary)
        if dist_dir is None:
            build_path = temporary_path / "dist"
            build_path.mkdir()
            _run([uv, "build", "--out-dir", str(build_path)], cwd=PROJECT_ROOT)
        else:
            build_path = dist_dir.resolve()
            if not build_path.is_dir():
                raise PackageCheckError(f"distribution directory does not exist: {dist_dir}")

        wheels = sorted(build_path.glob("*.whl"))
        sdists = sorted(build_path.glob("*.tar.gz"))
        if len(wheels) != 1 or len(sdists) != 1:
            raise PackageCheckError(
                f"expected one wheel and one sdist, found {wheels!r} and {sdists!r}"
            )
        wheel_path = wheels[0]
        source_version = read_source_version()
        try:
            wheel_version = verify_wheel(wheel_path, expected_version=source_version)
            sdist_version = verify_sdist(sdists[0], expected_version=source_version)
        except (BadZipFile, EOFError, tarfile.TarError, UnicodeDecodeError) as exc:
            raise PackageCheckError(f"distribution archive could not be read: {exc}") from exc
        if wheel_version != sdist_version:
            raise PackageCheckError(
                f"wheel version {wheel_version!r} does not match sdist version {sdist_version!r}"
            )

        venv_path = temporary_path / "runtime-venv"
        _run(
            [uv, "venv", "--python", sys.executable, str(venv_path)],
            cwd=temporary_path,
        )
        python = _venv_python(venv_path)
        _run(
            [uv, "pip", "install", "--python", str(python), str(wheel_path)],
            cwd=temporary_path,
        )
        _run([str(python), "-I", "-c", IMPORT_CHECK], cwd=temporary_path)

        print(
            f"Verified version {source_version} in wheel and sdist: "
            f"{wheels[0].name}, {sdists[0].name}"
        )
        print(
            "Verified sdist contents, py.typed, lxml-only mandatory metadata, "
            "all 53 public model exports, isolated irregular/contextual runtime "
            "imports, and typed mutation/reparse"
        )
        if dist_dir is not None:
            print(f"Verified prebuilt distributions in {build_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dist-dir",
        type=Path,
        help="verify and smoke-test existing distributions without rebuilding",
    )
    args = parser.parse_args(argv)
    try:
        verify_package(args.dist_dir)
    except PackageCheckError as exc:
        print(f"Package verification failed: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(
            f"Package verification command failed with exit code {exc.returncode}",
            file=sys.stderr,
        )
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
