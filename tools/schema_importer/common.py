"""Shared local-input and protected-output helpers for the importer CLI."""

from __future__ import annotations

import hashlib
from pathlib import Path

from tools.schema_importer.candidate import CandidateSource, SourceKind
from tools.schema_importer.errors import ImporterError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ROOT = PROJECT_ROOT / "schema" / "canonical"


def read_local_input(path_text: str, kind: SourceKind) -> tuple[bytes, CandidateSource]:
    """Read bytes from a local path only and record their digest and path evidence."""
    source_path = Path(path_text)
    try:
        raw = source_path.read_bytes()
    except OSError as exc:
        raise ImporterError("SOURCE_READ", str(exc), path_text) from exc
    if not raw:
        raise ImporterError("SOURCE_EMPTY", "input file is empty", path_text)
    return raw, CandidateSource(kind=kind, path=path_text, sha256=hashlib.sha256(raw).hexdigest())


def safe_output_path(
    output_text: str,
    *,
    source_path: str | None = None,
    force: bool = False,
    repo_root: Path = PROJECT_ROOT,
) -> Path | None:
    """Resolve a CLI output while prohibiting canonical-schema replacement."""
    if output_text == "-":
        return None
    target = Path(output_text).resolve()
    canonical = (repo_root / "schema" / "canonical").resolve()
    if target == canonical or canonical in target.parents:
        raise ImporterError(
            "PROTECTED_OUTPUT",
            "candidate and diff outputs may not be written inside schema/canonical",
            output_text,
        )
    if source_path is not None and target == Path(source_path).resolve():
        raise ImporterError("OUTPUT_IS_INPUT", "output path is the same as the source", output_text)
    if target.exists() and not force:
        raise ImporterError(
            "OUTPUT_EXISTS", "output already exists; pass --force to replace it", output_text
        )
    return target


def write_text_output(
    output_text: str,
    text: str,
    *,
    source_path: str | None = None,
    force: bool = False,
    repo_root: Path = PROJECT_ROOT,
) -> bool:
    """Write explicit output, returning false when the caller should use stdout."""
    target = safe_output_path(
        output_text,
        source_path=source_path,
        force=force,
        repo_root=repo_root,
    )
    if target is None:
        return False
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if force:
            target.write_text(text, encoding="utf-8", newline="\n")
        else:
            with target.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
    except FileExistsError as exc:
        raise ImporterError(
            "OUTPUT_EXISTS", "output already exists; pass --force to replace it", output_text
        ) from exc
    except OSError as exc:
        raise ImporterError("OUTPUT_WRITE", str(exc), output_text) from exc
    return True
