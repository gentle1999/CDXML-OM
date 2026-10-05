from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _attributes(*paths: str) -> dict[tuple[str, str], str]:
    result = subprocess.run(
        ["git", "check-attr", "text", "eol", "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    values: dict[tuple[str, str], str] = {}
    for line in result.stdout.splitlines():
        path, attribute, value = line.rsplit(": ", maxsplit=2)
        values[(path, attribute)] = value
    return values


def test_text_sources_have_lf_and_hashed_inputs_disable_eol_conversion() -> None:
    paths = (
        "README.md",
        "src/cdxml_om/__init__.py",
        "examples/notebooks/01_core_workflow.ipynb",
        "schema/canonical/properties.yaml",
        "schema/schema.lock.json",
        "schema/sources/revvity-CDXML.dtd",
        "tests/fixtures/corpus/mol1.cdxml",
        "examples/render_samples/probe_curve_points.cdxml",
    )
    values = _attributes(*paths)

    for path in paths[:3]:
        assert values[(path, "text")] == "auto"
        assert values[(path, "eol")] == "lf"
    for path in paths[3:]:
        assert values[(path, "text")] == "unset"


def test_project_inputs_are_not_ignored() -> None:
    paths = (
        "uv.lock",
        "schema/schema.lock.json",
        "schema/canonical/properties.yaml",
        "src/cdxml_om/_generated/models.py",
        "tests/fixtures/corpus/mol1.cdxml",
        "examples/notebooks/01_core_workflow.ipynb",
        "examples/render_samples/probe_curve_points.cdxml",
    )
    for path in paths:
        assert (ROOT / path).is_file()
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", "--", path],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 1, f"project input is ignored: {path}"


def test_hashed_source_paths_preserve_synthetic_crlf_bytes_with_autocrlf() -> None:
    paths = (
        "schema/sources/revvity-CDXML.dtd",
        "tests/fixtures/corpus/mol1.cdxml",
        "examples/render_samples/probe_curve_points.cdxml",
    )
    sample_bytes = b"first line\r\nsecond line\r\n"
    expected = subprocess.run(
        ["git", "hash-object", "--stdin", "--no-filters"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        input=sample_bytes,
    ).stdout

    for path in paths:
        filtered = subprocess.run(
            [
                "git",
                "-c",
                "core.autocrlf=true",
                "hash-object",
                "--stdin",
                f"--path={path}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            input=sample_bytes,
        )
        assert filtered.stdout == expected, f"Git normalized protected bytes for {path}"
