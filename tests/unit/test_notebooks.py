from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote

import nbformat
import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = ROOT / "examples" / "notebooks"
NOTEBOOK_NAMES = (
    "01_core_workflow.ipynb",
    "02_document_features.ipynb",
    "03_validation_and_preservation.ipynb",
)
MARKER_PREFIX = "CDXML-OM notebook: "
FORBIDDEN_NETWORK_IMPORTS = {
    "aiohttp",
    "ftplib",
    "http.client",
    "httpx",
    "requests",
    "socket",
    "subprocess",
    "urllib",
    "urllib.request",
    "webbrowser",
    "websockets",
}
SECRET_PATTERNS = (
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)
EPHEMERAL_PATH_PATTERN = re.compile(r"(?:/tmp/|/home/|/Users/|pytest-of-|[A-Z]:\\Users\\)")
TIMING_OUTPUT_PATTERN = re.compile(r"\b(?:CPU times|Wall time|Execution time|Elapsed)\s*:", re.I)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _notebooks(directory: Path) -> dict[str, nbformat.NotebookNode]:
    files = sorted(directory.glob("*.ipynb"), key=lambda path: path.name)
    assert {path.name for path in files} == set(NOTEBOOK_NAMES)
    notebooks: dict[str, nbformat.NotebookNode] = {}
    for path in files:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        notebooks[path.name] = notebook
    return notebooks


def _code_cells(notebook: nbformat.NotebookNode) -> list[nbformat.NotebookNode]:
    return [cell for cell in notebook.cells if cell.cell_type == "code"]


def _cell_tags(cell: nbformat.NotebookNode) -> set[str]:
    metadata = cell.get("metadata", {})
    tags: object = metadata.get("tags", []) if isinstance(metadata, dict) else []
    assert isinstance(tags, list)
    return {str(tag) for tag in tags}


def _outputs_text(notebook: nbformat.NotebookNode) -> str:
    pieces: list[str] = []
    for cell in _code_cells(notebook):
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                pieces.append(str(output.get("text", "")))
            elif output.output_type in {"display_data", "execute_result"}:
                data = output.get("data", {})
                if isinstance(data, dict):
                    pieces.extend(str(value) for value in data.values())
    return "\n".join(pieces)


def _code_source(notebook: nbformat.NotebookNode) -> str:
    return "\n".join(str(cell.source) for cell in _code_cells(notebook))


def _local_markdown_targets(path: Path) -> set[Path]:
    targets: set[Path] = set()
    for raw_target in MARKDOWN_LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        target = unquote(raw_target.split(maxsplit=1)[0].strip("<>"))
        if target.startswith(("#", "mailto:")) or "://" in target:
            continue
        target_path = target.split("#", maxsplit=1)[0]
        if target_path:
            targets.add((path.parent / target_path).resolve())
    return targets


def _run_runner(
    *,
    cwd: Path,
    notebook_dir: Path,
    mode: str,
    output_dir: Path | None = None,
    timeout: float = 60,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-m",
        "tools.run_notebooks",
        "--notebook-dir",
        str(notebook_dir),
    ]
    if mode == "output-dir":
        assert output_dir is not None
        command.extend(("--output-dir", str(output_dir)))
    elif mode in {"update", "check"}:
        command.append(f"--{mode}")
    else:
        raise AssertionError(f"unknown notebook runner mode: {mode}")

    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT), existing_pythonpath) if part
    )
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
        timeout=timeout,
    )


def _assert_no_runtime_error_or_skip(notebook: nbformat.NotebookNode) -> None:
    code_cells = _code_cells(notebook)
    execution_counts: list[int] = []
    for cell in code_cells:
        assert cell.get("execution_count") is not None
        execution_counts.append(int(cell.execution_count))
        assert "skip-execution" not in _cell_tags(cell)
        assert all(output.output_type != "error" for output in cell.get("outputs", []))
    assert execution_counts == list(range(1, len(code_cells) + 1))


def _assert_output_is_sanitized(text: str, *, notebook_name: str) -> None:
    assert not EPHEMERAL_PATH_PATTERN.search(text), notebook_name
    assert not TIMING_OUTPUT_PATTERN.search(text), notebook_name
    assert str(ROOT) not in text, notebook_name
    for pattern in SECRET_PATTERNS:
        assert pattern.search(text) is None, notebook_name


def _network_imports(source: str) -> set[str]:
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names = {node.module, *(f"{node.module}.{alias.name}" for alias in node.names)}
        else:
            continue
        found.update(name for name in names if name in FORBIDDEN_NETWORK_IMPORTS)
    return found


def _has_absolute_file_target(source: str) -> bool:
    tree = ast.parse(source)
    file_methods = {
        "from_file",
        "open",
        "read_bytes",
        "read_text",
        "save",
        "to_file",
        "write_bytes",
        "write_text",
    }

    def absolute_target(expression: ast.expr) -> bool:
        if isinstance(expression, ast.Constant) and isinstance(expression.value, str):
            return (
                Path(expression.value).is_absolute()
                or PureWindowsPath(expression.value).is_absolute()
            )
        if isinstance(expression, ast.Call) and isinstance(expression.func, ast.Name):
            return (
                expression.func.id in {"Path", "PurePath"}
                and bool(expression.args)
                and (absolute_target(expression.args[0]))
            )
        if isinstance(expression, ast.Call) and isinstance(expression.func, ast.Attribute):
            return expression.func.attr in {"expanduser", "home"}
        return False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if isinstance(function, ast.Name):
            method_name = function.id
        elif isinstance(function, ast.Attribute):
            method_name = function.attr
        else:
            continue
        if method_name not in file_methods:
            continue
        if isinstance(function, ast.Attribute) and absolute_target(function.value):
            return True
        if node.args and absolute_target(node.args[0]):
            return True
    return False


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("open('/absolute/example.cdxml', 'w')", True),
        ("CDXMLDocument.from_file('/absolute/example.cdxml')", True),
        ("Path('/absolute/example.cdxml').write_text('data')", True),
        ("Path('relative/example.cdxml').read_bytes()", False),
        ("document.to_file('example.cdxml')", False),
    ],
)
def test_absolute_file_guard_handles_literal_and_path_targets(
    source: str,
    expected: bool,
) -> None:
    assert _has_absolute_file_target(source) is expected


@pytest.mark.parametrize(
    "source",
    ["import requests", "from urllib import request", "import http.client"],
)
def test_network_import_guard_detects_common_client_import_forms(source: str) -> None:
    assert _network_imports(source)


def test_committed_notebooks_are_bilingual_executed_and_policy_checked() -> None:
    notebooks = _notebooks(NOTEBOOK_DIR)

    for name, notebook in notebooks.items():
        markdown = "\n".join(
            str(cell.source) for cell in notebook.cells if cell.cell_type == "markdown"
        )
        assert re.search(r"\b[A-Za-z]{3,}\b", markdown), name
        assert any("\u4e00" <= character <= "\u9fff" for character in markdown), name
        _assert_no_runtime_error_or_skip(notebook)
        combined_output = _outputs_text(notebook)
        assert f"{MARKER_PREFIX}{Path(name).stem} OK" in combined_output
        _assert_output_is_sanitized(combined_output, notebook_name=name)

        for cell in _code_cells(notebook):
            source = str(cell.source)
            assert not _network_imports(source), name
            assert not _has_absolute_file_target(source), name


def test_core_workflow_example_creates_and_reloads_a_referenced_bond() -> None:
    source = _code_source(_notebooks(NOTEBOOK_DIR)["01_core_workflow.ipynb"])

    for operation in (
        "CDXMLDocument.from_string(source)",
        "fragment.nodes.create(element=7, position=(6.0, 8.0))",
        "fragment.bonds.create(begin=oxygen, end=created_node, order=BondOrder.SINGLE)",
        "fragment.nodes.remove(temporary_node)",
        "bond.order = BondOrder.DOUBLE",
        "oxygen.charge = -1",
        "oxygen.position = Point2D(4.0, 5.0)",
        "document.validate().is_valid",
        "document.to_string()",
        "document.to_file(path)",
        "CDXMLDocument.from_file(path)",
        "reloaded_created_bond.begin is reloaded_fragment.nodes[1]",
        "reloaded_created_bond.end is reloaded_created_node",
        "reloaded_fragment.nodes[1].charge == -1",
        "reloaded_fragment.nodes[1].position == Point2D(4.0, 5.0)",
    ):
        assert operation in source


def test_document_features_example_exercises_typed_document_features() -> None:
    source = _code_source(_notebooks(NOTEBOOK_DIR)["02_document_features.ipynb"])

    for operation in (
        "create_font_table()",
        "create_color_table()",
        "font_table.fonts.create(",
        "color_table.colors.create(",
        "text.runs.create(",
        "second_run = text.runs.create(",
        "run.size = 13.0",
        "group.fragments.create()",
        "group.graphics.create(",
        "group.arrows.create(",
        "fragment.curves.create(",
        "group.objecttags.create(",
        "ElementList(elements=(6, 8), negated=True)",
        'GenericList(values=("alpha", "beta"))',
        "step.reactants = (fragment, group)",
        "step.products = (fragment,)",
        "step.arrows = (arrow, graphic)",
        "group.spectrums.create(",
        'data="400 0.2 500 0.5"',
        "reloaded_step.reactants == (reloaded_fragment, reloaded_group)",
        "reloaded_step.products == (reloaded_fragment,)",
        "reloaded_step.arrows == (reloaded_group.arrows[0], reloaded_group.graphics[0])",
        '[run.content for run in reloaded_text.runs] == ["Updated", " emphasized"]',
        "[run.size for run in reloaded_text.runs] == [13.0, 9.0]",
        "reloaded_text.runs[1].face == 1 and reloaded_text.runs[1].font_id == font.id",
        'reloaded.font_table.fonts[0].name == "Example Sans"',
        'reloaded.font_table.fonts[0].charset == "iso-8859-1"',
        "reloaded.color_table.colors[0].r == 0.15",
        "reloaded_group.graphics[0].bounding_box == BoundingBox(2.0, 3.0, 18.0, 14.0)",
        "reloaded_group.arrows[0].head_3d == Point3D(9.0, 4.0, 0.0)",
        "reloaded_group.arrows[0].tail_3d == Point3D(1.0, 4.0, 0.0)",
        "reloaded_fragment.curves[0].curve_points == curve.curve_points",
        "reloaded_fragment.curves[0].curve_points3_d == curve.curve_points3_d",
        "reloaded_group.spectrums[0].data == spectrum.data",
        'reloaded_group.spectrums[0].annotations[0].content == "Illustrative lexical payload"',
        'reloaded_step.arrows[0].xml_tag == "arrow"',
        "document.validate().is_valid",
        "reloaded.validate().is_valid",
    ):
        assert operation in source


def test_validation_example_checks_preservation_and_untrusted_entities() -> None:
    source = _code_source(_notebooks(NOTEBOOK_DIR)["03_validation_and_preservation.ipynb"])

    for operation in (
        "UnknownElement",
        'xmlns:v="urn:vendor"',
        'VendorNode="keep"',
        'p="001.000 02.500"',
        "retain sibling position",
        "document.to_string() == before_validation",
        'reloaded_node.raw_attributes["p"] == "001.000 02.500"',
        'reloaded_node.raw_attributes["VendorNode"] == "keep"',
        'roundtrip_xml.index("<v:opaque")',
        "roundtrip_xml.index('<n id=\"3\"')",
        "roundtrip_xml.index('<n id=\"4\"')",
        'duplicate == ("duplicate-id", "common.id")',
        'dangling[0] == "dangling-reference"',
        'wrong_target == ("wrong-reference-target", "bond.begin")',
        'bad_value == ("invalid-value", "node.charge")',
        'bad_parent[0] == "invalid-parent"',
        'raw_reference_id("bond.end") == 999',
        'dangling_reloaded.find(Bond)[0].raw_reference_id("bond.end") == 999',
        "<!ENTITY local SYSTEM",
        'assert "&local;" in entity_xml',
        'assert "MUST_NOT_BE_READ_OR_SERIALIZED" not in entity_xml',
        'assert entity.name == "local"',
    ):
        assert operation in source


def test_bilingual_docs_link_to_every_executable_notebook() -> None:
    for readme, guide, index, expected_guide in (
        (ROOT / "README.md", ROOT / "docs/examples.md", ROOT / "docs/index.md", "docs/examples.md"),
        (
            ROOT / "README.zh-CN.md",
            ROOT / "docs/zh-CN/examples.md",
            ROOT / "docs/zh-CN/index.md",
            "docs/zh-CN/examples.md",
        ),
    ):
        guide_link = (ROOT / expected_guide).resolve()
        assert guide_link in _local_markdown_targets(readme)
        assert guide.name == "examples.md"
        index_targets = _local_markdown_targets(index)
        assert guide.resolve() in index_targets
        guide_targets = _local_markdown_targets(guide)
        for name in NOTEBOOK_NAMES:
            assert (NOTEBOOK_DIR / name).resolve() in guide_targets


def test_runner_executes_fresh_copies_in_clean_kernels_independent_of_cwd(
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "source notebooks"
    output_dir = tmp_path / "executed copies"
    source_dir.mkdir()
    source_bytes: dict[str, bytes] = {}
    for name in NOTEBOOK_NAMES:
        source = NOTEBOOK_DIR / name
        source_bytes[name] = source.read_bytes()
        shutil.copy2(source, source_dir / name)

    result = _run_runner(
        cwd=tmp_path,
        notebook_dir=source_dir,
        mode="output-dir",
        output_dir=output_dir,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert {path.name for path in output_dir.iterdir()} == set(NOTEBOOK_NAMES)
    assert {name: (source_dir / name).read_bytes() for name in NOTEBOOK_NAMES} == source_bytes
    assert {path.name for path in tmp_path.iterdir()} == {source_dir.name, output_dir.name}

    executed = _notebooks(output_dir)
    for name, notebook in executed.items():
        _assert_no_runtime_error_or_skip(notebook)
        output = _outputs_text(notebook)
        assert f"{MARKER_PREFIX}{Path(name).stem} OK" in output
        _assert_output_is_sanitized(output, notebook_name=name)


def test_runner_refuses_source_overwrite_and_update_is_all_or_nothing(
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "failing notebook batch"
    source_dir.mkdir()
    expected_executable = repr(sys.executable)
    expected_caller_cwd = repr(str(tmp_path))
    good = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell(
                f"import sys\n"
                "from pathlib import Path\n"
                f"assert sys.executable == {expected_executable}\n"
                f"assert Path.cwd() != Path({expected_caller_cwd})\n"
                "assert 2 + 2 == 4\n"
                "notebook_batch_sentinel = True\n"
                "print('good notebook ran')"
            ),
        ],
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
    )
    failing = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell(
                "assert 'notebook_batch_sentinel' not in globals()\n"
                "raise RuntimeError('intentional notebook failure')"
            )
        ],
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
    )
    good_path = source_dir / "01_good.ipynb"
    failing_path = source_dir / "02_failing.ipynb"
    nbformat.write(good, good_path)
    nbformat.write(failing, failing_path)
    originals = {path.name: path.read_bytes() for path in source_dir.glob("*.ipynb")}

    overwrite = _run_runner(
        cwd=tmp_path,
        notebook_dir=source_dir,
        mode="output-dir",
        output_dir=source_dir,
    )
    assert overwrite.returncode != 0
    assert {path.name: path.read_bytes() for path in source_dir.glob("*.ipynb")} == originals

    existing_output_dir = tmp_path / "preexisting output"
    existing_output_dir.mkdir()
    sentinel = existing_output_dir / good_path.name
    sentinel.write_bytes(b"do not overwrite")
    output_collision = _run_runner(
        cwd=tmp_path,
        notebook_dir=source_dir,
        mode="output-dir",
        output_dir=existing_output_dir,
    )
    assert output_collision.returncode != 0
    assert sentinel.read_bytes() == b"do not overwrite"
    assert {path.name for path in existing_output_dir.iterdir()} == {good_path.name}

    update = _run_runner(cwd=tmp_path, notebook_dir=source_dir, mode="update", timeout=60)
    assert update.returncode != 0
    assert "intentional notebook failure" in update.stdout + update.stderr
    assert {path.name: path.read_bytes() for path in source_dir.glob("*.ipynb")} == originals


def test_runner_rejects_skip_execution_cells_without_silently_skipping(
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "skip notebook"
    source_dir.mkdir()
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell(
                "print('must not be silently skipped')",
                metadata={"tags": ["skip-execution"]},
            ),
        ],
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
    )
    nbformat.write(notebook, source_dir / "skip.ipynb")
    output_dir = tmp_path / "skip output"

    result = _run_runner(
        cwd=tmp_path,
        notebook_dir=source_dir,
        mode="output-dir",
        output_dir=output_dir,
    )
    assert result.returncode != 0
    assert not output_dir.exists() or not any(output_dir.iterdir())


def test_runner_reports_missing_notebook_extra_clearly(tmp_path: Path) -> None:
    notebook_dir = tmp_path / "dependency test notebook"
    notebook_dir.mkdir()
    nbformat.write(
        nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("print('must not execute')")]),
        notebook_dir / "minimal.ipynb",
    )
    output_dir = tmp_path / "missing-dependency-output"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT)
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            "-m",
            "tools.run_notebooks",
            "--notebook-dir",
            str(notebook_dir),
            "--output-dir",
            str(output_dir),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
        timeout=15,
    )
    assert result.returncode != 0
    assert "notebook execution dependencies are missing" in result.stderr.lower()
    assert "extra" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()
    assert not output_dir.exists()


def test_update_detects_source_change_during_execution_before_replacing_anything(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import tools.run_notebooks as notebook_runner

    source_dir = tmp_path / "concurrent update"
    source_dir.mkdir()
    notebook_path = source_dir / "change-during-run.ipynb"
    original_notebook = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_code_cell("print('original source')")]
    )
    nbformat.write(original_notebook, notebook_path)
    external_change = b"concurrent editor update"

    def modify_during_execution(source_path: Path) -> object:
        source_path.write_bytes(external_change)
        return original_notebook

    monkeypatch.setattr(notebook_runner, "_execute_one", modify_during_execution)
    with pytest.raises(notebook_runner.NotebookRunError, match="source notebook changed"):
        notebook_runner.run_notebooks(source_dir, update=True)

    assert notebook_path.read_bytes() == external_change
    assert not list(source_dir.glob(".*.tmp"))
