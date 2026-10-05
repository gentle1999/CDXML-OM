"""Subprocess-level contract tests for the offline schema importer CLI."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINNED_DTD = ROOT / "schema" / "sources" / "revvity-CDXML.dtd"


def _run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tools.schema_importer", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )


def _error_payload(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    assert result.returncode == 2
    assert result.stdout == ""
    envelope = json.loads(result.stderr)
    assert envelope["format"] == "cdxml-om-schema-import-error"
    payload = envelope["error"]
    assert isinstance(payload, dict)
    return payload


def test_pinned_dtd_candidate_is_deterministic_and_diffable(tmp_path: Path) -> None:
    candidate_path = tmp_path / "pinned-dtd-candidate.json"
    first = _run_cli("import-dtd", str(PINNED_DTD), "--output", str(candidate_path))
    assert first.returncode == 0, first.stderr
    assert first.stdout == ""
    first_text = candidate_path.read_text(encoding="utf-8")

    second = _run_cli("import-dtd", str(PINNED_DTD), "--output", str(candidate_path), "--force")
    assert second.returncode == 0, second.stderr
    second_text = candidate_path.read_text(encoding="utf-8")
    assert second_text == first_text

    candidate = json.loads(first_text)
    assert candidate["format"] == "cdxml-om-schema-candidate"
    assert candidate["scope"] == "dtd"
    assert candidate["source"]["sha256"] == hashlib.sha256(PINNED_DTD.read_bytes()).hexdigest()
    assert any(item["xml_name"] == "CDXML" for item in candidate["dtd_elements"])

    first_diff = _run_cli("diff", str(candidate_path))
    second_diff = _run_cli("diff", str(candidate_path))
    assert first_diff.returncode == 0, first_diff.stderr
    assert second_diff.returncode == 0, second_diff.stderr
    assert first_diff.stdout == second_diff.stdout
    report = json.loads(first_diff.stdout)
    assert report["format"] == "cdxml-om-schema-diff"
    assert report["candidate_source"]["sha256"] == candidate["source"]["sha256"]
    assert sum(report["summary"].values()) > 0


def test_synthetic_sdk_candidate_is_deterministic_and_keeps_source_digest(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "node-sdk.html"
    source_path.write_text(
        """<!doctype html>
<html><body><table>
<tr><th>Value</th><th>Name</th><th>CDXML Name</th><th>Object</th></tr>
<tr><td>0x8004</td><td>kCDXObj_Node</td><td>n</td><td>Node</td></tr>
</table></body></html>
""",
        encoding="utf-8",
    )
    candidate_path = tmp_path / "node-sdk-candidate.json"

    first = _run_cli("import-sdk", str(source_path))
    second = _run_cli("import-sdk", str(source_path))
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout

    candidate = json.loads(first.stdout)
    assert candidate["scope"] == "inventory"
    assert candidate["source"]["sha256"] == hashlib.sha256(source_path.read_bytes()).hexdigest()
    assert candidate["sdk_entries"][0]["xml_name"] == "n"
    assert candidate["sdk_entries"][0]["cdx_id"] == 0x8004

    saved = _run_cli("import-sdk", str(source_path), "--output", str(candidate_path))
    assert saved.returncode == 0, saved.stderr
    assert candidate_path.read_text(encoding="utf-8") == first.stdout
    diff = _run_cli("diff", str(candidate_path))
    assert diff.returncode == 0, diff.stderr
    report = json.loads(diff.stdout)
    assert report["candidate_source"]["sha256"] == candidate["source"]["sha256"]
    assert report["summary"]["missing"] > 0


def test_unsafe_dtd_input_returns_structured_nonzero_error(tmp_path: Path) -> None:
    source_path = tmp_path / "external.dtd"
    source_path.write_text(
        '<!ENTITY % remote SYSTEM "https://example.invalid/external.dtd">%remote;\n',
        encoding="utf-8",
    )

    result = _run_cli("import-dtd", str(source_path))

    payload = _error_payload(result)
    assert payload["code"] == "DTD_PARAMETER_ENTITY"
    assert isinstance(payload["message"], str)
    assert isinstance(payload["location"], str)


def test_canonical_schema_is_protected_even_with_force(tmp_path: Path) -> None:
    source_path = tmp_path / "node-sdk.html"
    source_path.write_text(
        """<html><body><table>
<tr><th>Value</th><th>Name</th><th>CDXML Name</th><th>Object</th></tr>
<tr><td>0x8004</td><td>kCDXObj_Node</td><td>n</td><td>Node</td></tr>
</table></body></html>""",
        encoding="utf-8",
    )
    protected_path = ROOT / "schema" / "canonical" / "objects.yaml"
    original = protected_path.read_bytes()

    result = _run_cli(
        "import-sdk",
        str(source_path),
        "--output",
        str(protected_path),
        "--force",
    )

    payload = _error_payload(result)
    assert payload["code"] == "PROTECTED_OUTPUT"
    assert protected_path.read_bytes() == original
