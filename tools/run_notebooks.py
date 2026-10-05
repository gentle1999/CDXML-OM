"""Execute the checked-in tutorial notebooks with the current Python interpreter."""

from __future__ import annotations

import argparse
import copy
import importlib
import json
import os
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from jupyter_client.manager import AsyncKernelManager
    from nbformat import NotebookNode


class NotebookRunError(RuntimeError):
    """Raised when notebook input, execution, or output validation fails."""


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTEBOOK_DIR = PROJECT_ROOT / "examples" / "notebooks"
_KERNEL_NAME = "cdxml-om-current-python"
_CELL_TIMEOUT_SECONDS = 120
_KERNEL_STARTUP_TIMEOUT_SECONDS = 60


def _require_notebook_dependencies() -> None:
    try:
        for name in ("ipykernel", "jupyter_client", "nbclient", "nbformat"):
            importlib.import_module(name)
    except ImportError as exc:
        raise NotebookRunError(
            "notebook execution dependencies are missing; install with `uv sync --extra notebooks`"
        ) from exc


def _load_notebook(path: Path) -> NotebookNode:
    import nbformat

    try:
        read_notebook = cast("Callable[..., NotebookNode]", vars(nbformat)["read"])
        notebook = read_notebook(path, as_version=4)
        nbformat.validate(notebook)
    except Exception as exc:
        raise NotebookRunError(f"could not read valid notebook {path.name}: {exc}") from exc

    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    if not code_cells:
        raise NotebookRunError(f"notebook {path.name} has no executable code cells")
    for cell in code_cells:
        if not str(cell.source).strip():
            raise NotebookRunError(f"notebook {path.name} has an empty code cell")
        tags = cell.metadata.get("tags", [])
        if "skip-execution" in tags:
            raise NotebookRunError(
                f"notebook {path.name} has a skip-execution code cell; all examples must run"
            )
    return notebook


def _new_kernel_manager(kernel_spec_root: Path) -> AsyncKernelManager:
    try:
        from jupyter_client.kernelspec import KernelSpecManager
        from jupyter_client.manager import AsyncKernelManager
    except ImportError as exc:
        raise NotebookRunError(
            "notebook execution dependencies are missing; install with `uv sync --extra notebooks`"
        ) from exc

    kernel_directory = kernel_spec_root / "kernels" / _KERNEL_NAME
    kernel_directory.mkdir(parents=True)
    spec = {
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Python (CDXML-OM runner)",
        "language": "python",
    }
    (kernel_directory / "kernel.json").write_text(
        json.dumps(spec, ensure_ascii=True), encoding="utf-8"
    )
    manager = KernelSpecManager(
        kernel_dirs=[str(kernel_spec_root / "kernels")],
        ensure_native_kernel=False,
        allowed_kernelspecs={_KERNEL_NAME},
    )
    try:
        return AsyncKernelManager(
            kernel_name=_KERNEL_NAME,
            kernel_spec_manager=manager,
        )
    except Exception as exc:
        raise NotebookRunError(f"could not configure the temporary Python kernel: {exc}") from exc


def _normalize_execution(notebook: NotebookNode, source_metadata: NotebookNode) -> NotebookNode:
    import nbformat

    notebook.metadata = copy.deepcopy(source_metadata)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.metadata.pop("execution", None)
            cell.metadata.pop("ExecuteTime", None)
    try:
        nbformat.validate(notebook)
    except Exception as exc:
        raise NotebookRunError(f"executed notebook is invalid: {exc}") from exc
    return notebook


def _execute_one(notebook_path: Path) -> NotebookNode:
    try:
        from nbclient import NotebookClient
    except ImportError as exc:
        raise NotebookRunError(
            "notebook execution dependencies are missing; install with `uv sync --extra notebooks`"
        ) from exc

    notebook = _load_notebook(notebook_path)
    source_metadata = copy.deepcopy(notebook.metadata)
    with tempfile.TemporaryDirectory(prefix="cdxml-om-notebook-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        working_directory = temporary_root / "work"
        working_directory.mkdir()
        kernel_manager = _new_kernel_manager(temporary_root)
        client = NotebookClient(
            notebook,
            km=kernel_manager,
            timeout=_CELL_TIMEOUT_SECONDS,
            startup_timeout=_KERNEL_STARTUP_TIMEOUT_SECONDS,
            allow_errors=False,
            record_timing=False,
        )
        try:
            client.execute(cwd=str(working_directory), cleanup_kc=True)
        except Exception as exc:
            raise NotebookRunError(f"execution failed in {notebook_path.name}: {exc}") from exc
        executed_counts = [
            cell.execution_count for cell in notebook.cells if cell.cell_type == "code"
        ]
        expected_counts = list(range(1, len(executed_counts) + 1))
        if executed_counts != expected_counts:
            raise NotebookRunError(
                f"notebook {notebook_path.name} did not execute every code cell in order: "
                f"{executed_counts!r}"
            )
        if any(
            output.output_type == "error"
            for cell in notebook.cells
            if cell.cell_type == "code"
            for output in cell.outputs
        ):
            raise NotebookRunError(f"notebook {notebook_path.name} contains an error output")

    notebook = _normalize_execution(notebook, source_metadata)
    return notebook


def _serialized(notebook: NotebookNode) -> str:
    import nbformat

    write_notebook = cast("Callable[..., str]", vars(nbformat)["writes"])
    return write_notebook(notebook, version=4)


def _preflight_output_dir(output_dir: Path, notebook_paths: list[Path]) -> Path:
    if output_dir.is_symlink():
        raise NotebookRunError("refusing to write notebook copies through a symlink output path")
    resolved_output = output_dir.resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise NotebookRunError(f"output path is not a directory: {output_dir}")
    destinations = [resolved_output / path.name for path in notebook_paths]
    source_paths = {path.resolve() for path in notebook_paths}
    if any(destination in source_paths for destination in destinations):
        raise NotebookRunError(
            "output directory aliases a source notebook; refusing to overwrite it"
        )
    existing = [path.name for path in destinations if path.exists() or path.is_symlink()]
    if existing:
        raise NotebookRunError(
            "refusing to overwrite existing output notebook(s): " + ", ".join(existing)
        )
    return resolved_output


def _write_executed_copies(output_dir: Path, payloads: dict[Path, str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    try:
        for source_path, rendered in payloads.items():
            destination = output_dir / source_path.name
            with destination.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
            written.append(destination)
    except OSError as exc:
        for destination in written:
            destination.unlink(missing_ok=True)
        raise NotebookRunError(f"could not write executed copies to {output_dir}: {exc}") from exc


def _update_sources(payloads: dict[Path, str], original_bytes: dict[Path, bytes]) -> None:
    staged: dict[Path, Path] = {}
    try:
        for source_path, rendered in payloads.items():
            if source_path.is_symlink():
                raise NotebookRunError(
                    f"refusing to update notebook through symlink: {source_path.name}"
                )
            if source_path.read_bytes() != original_bytes[source_path]:
                raise NotebookRunError(
                    f"source notebook changed during execution: {source_path.name}"
                )
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                prefix=f".{source_path.name}.",
                suffix=".tmp",
                dir=source_path.parent,
                delete=False,
            ) as stream:
                stream.write(rendered)
                staged[source_path] = Path(stream.name)
        for source_path, staged_path in staged.items():
            os.replace(staged_path, source_path)
    except (OSError, NotebookRunError) as exc:
        for staged_path in staged.values():
            staged_path.unlink(missing_ok=True)
        if isinstance(exc, NotebookRunError):
            raise
        raise NotebookRunError(f"could not update executed source notebooks: {exc}") from exc


def run_notebooks(
    notebook_dir: Path = DEFAULT_NOTEBOOK_DIR,
    *,
    output_dir: Path | None = None,
    update: bool = False,
    check: bool = False,
) -> list[Path]:
    """Execute every notebook, then copy, explicitly update, or compare outputs."""
    modes = int(output_dir is not None) + int(update) + int(check)
    if modes != 1:
        raise NotebookRunError("choose exactly one of output_dir, update, or check")
    if notebook_dir.is_symlink():
        raise NotebookRunError("notebook directory must not be a symlink")
    try:
        resolved_notebook_dir = notebook_dir.resolve(strict=True)
    except OSError as exc:
        raise NotebookRunError(f"notebook directory does not exist: {notebook_dir}") from exc
    if not resolved_notebook_dir.is_dir():
        raise NotebookRunError(f"notebook path is not a directory: {notebook_dir}")
    notebook_paths = sorted(resolved_notebook_dir.glob("*.ipynb"), key=lambda path: path.name)
    if not notebook_paths:
        raise NotebookRunError(f"no .ipynb files found in {resolved_notebook_dir}")
    if update and any(path.is_symlink() for path in notebook_paths):
        raise NotebookRunError("refusing to update source notebook symlinks")

    resolved_output: Path | None = None
    if output_dir is not None:
        resolved_output = _preflight_output_dir(output_dir, notebook_paths)

    _require_notebook_dependencies()

    payloads: dict[Path, str] = {}
    original_bytes: dict[Path, bytes] = {}
    for notebook_path in notebook_paths:
        original_bytes[notebook_path] = notebook_path.read_bytes()
        notebook = _execute_one(notebook_path)
        payloads[notebook_path] = _serialized(notebook)
        print(f"Executed {notebook_path.name}")

    if resolved_output is not None:
        _write_executed_copies(resolved_output, payloads)
        return [resolved_output / path.name for path in notebook_paths]

    if update:
        _update_sources(payloads, original_bytes)
        print(f"Updated executed notebook outputs in {resolved_notebook_dir}")
        return notebook_paths

    stale: list[str] = []
    for notebook_path, rendered in payloads.items():
        if rendered != _serialized(_load_notebook(notebook_path)):
            stale.append(notebook_path.name)
    if stale:
        raise NotebookRunError(
            "committed notebook outputs are stale; review and refresh with --update: "
            + ", ".join(stale)
        )
    print(f"Notebook outputs are current for {len(notebook_paths)} notebooks")
    return notebook_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notebook-dir",
        type=Path,
        default=DEFAULT_NOTEBOOK_DIR,
        help="directory of notebooks (default: examples/notebooks)",
    )
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--output-dir", type=Path, help="write non-overwriting executed copies here")
    modes.add_argument("--update", action="store_true", help="explicitly refresh source outputs")
    modes.add_argument("--check", action="store_true", help="execute and check committed outputs")
    args = parser.parse_args(argv)
    try:
        run_notebooks(
            args.notebook_dir,
            output_dir=args.output_dir,
            update=args.update,
            check=args.check,
        )
    except (NotebookRunError, OSError) as exc:
        print(f"Notebook run failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
