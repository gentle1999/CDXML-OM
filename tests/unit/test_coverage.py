"""Regression tests for source-relative DTD coverage and test evidence."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import cast

import pytest
from tools.schema_compiler.coverage import (
    CoverageError,
    _catalog,  # pyright: ignore[reportPrivateUsage]
    _pinned_inventory,  # pyright: ignore[reportPrivateUsage]
    _test_state,  # pyright: ignore[reportPrivateUsage]
    build_coverage_report,
    run_feature_tests,
)
from tools.schema_compiler.loader import load_schema

ROOT = Path(__file__).resolve().parents[2]


def _inventory() -> tuple[set[str], set[tuple[str, str]]]:
    _, elements = _pinned_inventory(ROOT)
    return (
        {item.xml_name for item in elements},
        {(item.xml_name, attribute.name) for item in elements for attribute in item.attributes},
    )


def test_coverage_report_uses_exact_pinned_denominators_and_reports_dtd_anomaly() -> None:
    report = build_coverage_report(ROOT, load_schema(ROOT))

    assert report["baseline"] == {
        "dtd_path": "schema/sources/revvity-CDXML.dtd",
        "dtd_sha256": "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2",
        "element_count": 53,
        "nonroot_element_count": 52,
        "owner_attribute_pair_count": 762,
    }
    summary = cast(dict[str, dict[str, int]], report["summary"])
    assert summary["elements"]["known"] == 53
    assert summary["owner_attribute_pairs"]["known"] == 762
    assert summary["sdk_extension_pairs"]["total"] == 23
    assert summary["sdk_extension_pairs"]["known"] == 23
    assert summary["sdk_extension_pairs"]["tested"] == 0
    sdk_rows = cast(list[dict[str, object]], report["sdk_extension_pairs"])
    assert len(sdk_rows) == 23
    assert all(row["raw_preservation_tested"] is False for row in sdk_rows)
    unresolved = cast(dict[str, object], report["structure"])["unresolved_dtd_child_symbols"]
    assert unresolved == [{"owner_xml_name": "altgroup", "child_xml_name": "bracket"}]
    assert (
        cast(dict[str, object], report["structure"])["strict_grammar_validation_claimed"] is False
    )


def test_coverage_catalog_rejects_reassigned_case_id(tmp_path: Path) -> None:
    tags, pairs = _inventory()
    catalog_dir = tmp_path / "tests" / "coverage"
    catalog_dir.mkdir(parents=True)
    shutil.copy2(ROOT / "tests" / "coverage" / "test_full_schema_feature_evidence.py", catalog_dir)
    shutil.copy2(ROOT / "tests" / "coverage" / "sdk_extension_cases.json", catalog_dir)
    shutil.copy2(
        ROOT / "tests" / "coverage" / "test_sdk_extension_feature_evidence.py", catalog_dir
    )
    (tmp_path / "schema" / "sources" / "sdk").mkdir(parents=True)
    shutil.copy2(
        ROOT / "schema" / "sources" / "sdk" / "evidence.json",
        tmp_path / "schema" / "sources" / "sdk" / "evidence.json",
    )
    catalog = json.loads((ROOT / "tests" / "coverage" / "feature_cases.json").read_text())
    first = cast(dict[str, object], cast(list[object], catalog["cases"])[0])
    first["case_id"] = "feature:forged@attribute"
    (catalog_dir / "feature_cases.json").write_text(json.dumps(catalog), encoding="utf-8")

    with pytest.raises(CoverageError, match="attribute case ID"):
        _catalog(tmp_path, tags, pairs)


def test_failed_and_skipped_feature_cases_do_not_count_as_verified() -> None:
    tests = {
        operation: ("tests/test_feature.py::test_feature[case]",)
        for operation in (
            "read",
            "write",
            "mutation",
            "round_trip",
        )
    }

    verified, states = _test_state(
        tests,
        passed=set(),
        failed={"tests/test_feature.py::test_feature[case]"},
        skipped=set(),
        required=("read", "write", "mutation", "round_trip"),
    )
    assert verified is False
    assert cast(dict[str, object], states["read"])["failed"] == [
        "tests/test_feature.py::test_feature[case]"
    ]

    skipped_verified, skipped_states = _test_state(
        tests,
        passed=set(),
        failed=set(),
        skipped={"tests/test_feature.py::test_feature[case]"},
        required=("read", "write", "mutation", "round_trip"),
    )
    assert skipped_verified is False
    assert cast(dict[str, object], skipped_states["round_trip"])["skipped"] == [
        "tests/test_feature.py::test_feature[case]"
    ]


def test_feature_test_run_rejects_stale_fingerprints(tmp_path: Path) -> None:
    tags, pairs = _inventory()
    catalog = _catalog(ROOT, tags, pairs)
    node_ids = cast(tuple[str, ...], catalog["_node_ids"])
    run_path = tmp_path / "run.json"
    run_path.write_text(
        json.dumps(
            {
                "format": "cdxml-om-feature-test-run",
                "format_version": 2,
                "dtd_sha256": "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2",
                "fingerprints": {"fingerprint_sha256": "0" * 64},
                "junit_sha256": "0" * 64,
                "cases": [{"test_id": node_id, "status": "passed"} for node_id in node_ids],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(CoverageError, match="stale"):
        build_coverage_report(ROOT, load_schema(ROOT), test_run_path=run_path)


def test_feature_test_runner_rejects_preexisting_junit_output(tmp_path: Path) -> None:
    junit_path = tmp_path / "old-junit.xml"
    junit_path.write_text(
        '<testsuite><testcase classname="tests.unit.test_coverage" name="test_old" /></testsuite>',
        encoding="utf-8",
    )
    run_path = tmp_path / "run.json"

    with pytest.raises(CoverageError, match="already exists"):
        run_feature_tests(
            ROOT,
            load_schema(ROOT),
            run_output=run_path,
            junit_output=junit_path,
            pytest_arguments=["--collect-only"],
        )
    assert not run_path.exists()


def test_inventory_contains_all_pinned_dtd_elements() -> None:
    _, elements = _pinned_inventory(ROOT)
    assert len(elements) == 53
