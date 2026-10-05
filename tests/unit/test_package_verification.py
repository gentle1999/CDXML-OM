import shutil
import subprocess
import tarfile
import tomllib
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest
from tools.check_package import (
    IMPORT_CHECK,
    PackageCheckError,
    read_source_version,
    required_sdist_files,
    verify_mandatory_requirements,
    verify_sdist,
    verify_wheel,
)

from cdxml_om import __version__


def test_only_lxml_is_unconditional_wheel_dependency() -> None:
    verify_mandatory_requirements(
        [
            "lxml>=6.0",
            'pytest>=8.0; extra == "dev"',
            'pyyaml>=6.0; extra == "dev"',
            'ipykernel>=6.29; extra == "dev"',
            'nbclient>=0.10; extra == "notebooks"',
            'nbformat>=5.10; extra == "notebooks"',
        ],
        optional_extras=frozenset({"dev", "notebooks"}),
    )


def test_isolated_runtime_smoke_covers_full_generated_feature_surface() -> None:
    compile(IMPORT_CHECK, "<isolated-package-smoke>", "exec")
    for feature in (
        "len(OBJECT_METADATA) == 53",
        "cdxml_om.CDXMLRoot",
        'charset == "iso-8859-1"',
        "ElementList((9, 17), negated=True)",
        'GenericList(("R", "X"), negated=True)',
        "curve.curve_points3_d",
        "TagType.DOUBLE",
        "spectrum.data",
        'cdxml_om.__version__ == distribution("cdxml-om").version',
    ):
        assert feature in IMPORT_CHECK


def test_runtime_version_matches_distribution_metadata_and_source() -> None:
    from importlib.metadata import version

    assert __version__ == version("cdxml-om")
    assert __version__ == read_source_version()


def test_uv_cache_key_tracks_the_single_version_source() -> None:
    project_root = Path(__file__).resolve().parents[2]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    cache_keys = pyproject["tool"]["uv"]["cache-keys"]

    assert {entry["file"] for entry in cache_keys} == {
        "pyproject.toml",
        "src/cdxml_om/_version.py",
    }
    assert pyproject["project"]["dynamic"] == ["version"]
    assert "version" not in pyproject["project"]
    assert pyproject["tool"]["hatch"]["version"]["path"] == "src/cdxml_om/_version.py"


def test_hatch_build_reads_changed_version_without_importing_runtime(tmp_path: Path) -> None:
    uv = shutil.which("uv")
    if uv is None:
        pytest.skip("uv is required for the isolated build-backend check")

    project_root = Path(__file__).resolve().parents[2]
    project = tmp_path / "project"
    project.mkdir()
    for relative in required_sdist_files(project_root):
        source = project_root / relative
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    version_path = project / "src/cdxml_om/_version.py"
    version_path.write_text(
        '"""Single source version for the isolated build test."""\n\n__version__ = "0.1.0.dev7"\n',
        encoding="utf-8",
    )
    (project / "src/cdxml_om/__init__.py").write_text(
        'raise RuntimeError("the build backend imported the runtime package")\n', encoding="utf-8"
    )

    output = project / "dist"
    result = subprocess.run(
        [uv, "build", "--out-dir", str(output), "--no-progress"],
        cwd=project,
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    wheels = list(output.glob("*.whl"))
    sdists = list(output.glob("*.tar.gz"))
    assert len(wheels) == len(sdists) == 1
    assert verify_wheel(wheels[0], expected_version="0.1.0.dev7") == "0.1.0.dev7"
    assert verify_sdist(sdists[0], expected_version="0.1.0.dev7") == "0.1.0.dev7"

    with ZipFile(wheels[0]) as wheel:
        metadata_path = next(
            name for name in wheel.namelist() if name.endswith(".dist-info/METADATA")
        )
        assert "Version: 0.1.0.dev7" in wheel.read(metadata_path).decode("utf-8")


def test_wheel_rejects_metadata_version_mismatch(tmp_path: Path) -> None:
    wheel_path = tmp_path / "cdxml_om-0.1.0.dev0-py3-none-any.whl"
    metadata = (
        "Metadata-Version: 2.1\nName: cdxml-om\nVersion: 0.1.0.dev0\nRequires-Dist: lxml>=5.0\n"
    )
    with ZipFile(wheel_path, "w") as wheel:
        wheel.writestr("cdxml_om/py.typed", "")
        wheel.writestr("cdxml_om-0.1.0.dev0.dist-info/METADATA", metadata)

    with pytest.raises(PackageCheckError, match="does not match source version"):
        verify_wheel(wheel_path, expected_version="0.1.0.dev7")


def test_source_version_reader_accepts_literal_single_quotes(tmp_path: Path) -> None:
    version_path = tmp_path / "_version.py"
    version_path.write_text("__version__ = '2.4.1'\n", encoding="utf-8")

    assert read_source_version(version_path) == "2.4.1"


@pytest.mark.parametrize(
    ("source", "error"),
    [
        ("__version__ = get_version()\n", "literal string"),
        ('__version__ = "1.0"\n__version__ = "2.0"\n', "found 2"),
        ('description = "no version here"\n', "found 0"),
    ],
)
def test_source_version_reader_rejects_dynamic_duplicate_or_missing_values(
    tmp_path: Path, source: str, error: str
) -> None:
    version_path = tmp_path / "_version.py"
    version_path.write_text(source, encoding="utf-8")

    with pytest.raises(PackageCheckError, match=error):
        read_source_version(version_path)


@pytest.mark.parametrize(
    "requirements",
    [
        [],
        ["lxml>=5.0", "rdkit>=2024.03"],
        ["lxml>=5.0", 'rdkit>=2024.03; python_version >= "3.11"'],
        ["lxml>=5.0", "pytest>=8.0"],
        ["lxml>=5.0", 'pytest>=8.0; extra == "dev" and python_version >= "3.11"'],
        ["lxml>=5.0", 'nbclient>=0.10; extra == "notebooks"'],
        ["lxml>=5.0", 'nbclient>=0.10; extra == "notebooks" and python_version >= "3.11"'],
        ["lxml>=5.0", 'nbclient>=0.10; extra == "unknown"'],
    ],
)
def test_rejects_unexpected_mandatory_dependencies(requirements: list[str]) -> None:
    with pytest.raises(PackageCheckError):
        verify_mandatory_requirements(requirements)


def test_sdist_must_include_runtime_typing_schema_and_compiler_files(tmp_path: Path) -> None:
    archive_path = tmp_path / "cdxml-om.tar.gz"
    with tarfile.open(archive_path, mode="w:gz") as archive:
        names = required_sdist_files() | {"PKG-INFO"}
        for name in names:
            member = tarfile.TarInfo(f"cdxml-om-0.1.0/{name}")
            if name == "PKG-INFO":
                contents = b"Metadata-Version: 2.1\nName: cdxml-om\nVersion: 0.1.0.dev0\n"
            elif name == "src/cdxml_om/_version.py":
                contents = b'__version__ = "0.1.0.dev0"\n'
            else:
                contents = b"x"
            member.size = len(contents)
            archive.addfile(member, BytesIO(contents))

    assert verify_sdist(archive_path, expected_version="0.1.0.dev0") == "0.1.0.dev0"


def test_sdist_rejects_missing_essential_files(tmp_path: Path) -> None:
    archive_path = tmp_path / "cdxml-om.tar.gz"
    with tarfile.open(archive_path, mode="w:gz") as archive:
        member = tarfile.TarInfo("cdxml-om-0.1.0/README.md")
        member.size = 1
        archive.addfile(member, BytesIO(b"x"))

    with pytest.raises(PackageCheckError, match="missing essential project files"):
        verify_sdist(archive_path)


def test_required_sdist_files_ignores_bytecode_caches(tmp_path: Path) -> None:
    source = tmp_path / "src/cdxml_om/core.py"
    source.parent.mkdir(parents=True)
    source.touch()
    cache = source.parent / "__pycache__"
    cache.mkdir()
    bytecode = cache / "core.cpython-311.pyc"
    bytecode.touch()
    tool_cache = source.parent / ".ruff_cache"
    tool_cache.mkdir()
    (tool_cache / "cache.json").touch()

    required = required_sdist_files(tmp_path)

    assert "src/cdxml_om/core.py" in required
    assert "src/cdxml_om/__pycache__/core.cpython-311.pyc" not in required
    assert "src/cdxml_om/.ruff_cache/cache.json" not in required


def test_sdist_requires_offline_schema_importer_sources() -> None:
    required = required_sdist_files()

    assert "tools/schema_importer/__main__.py" in required
    assert "tools/schema_importer/diff.py" in required
