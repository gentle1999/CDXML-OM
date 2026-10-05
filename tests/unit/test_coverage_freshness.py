"""End-to-end coverage provenance and SDK-result accounting regressions."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import cast

import pytest
from tools.schema_compiler import coverage as coverage_module
from tools.schema_compiler.coverage import (
    CoverageError,
    build_coverage_report,
    run_feature_tests,
)
from tools.schema_compiler.ir import Schema
from tools.schema_compiler.loader import load_schema

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIRECTORIES = (
    "src",
    "tools/schema_compiler",
    "tools/schema_importer",
    "tests",
    "schema/canonical",
    "schema/sources",
    "schema/coverage",
    "schema/overrides",
)
PROJECT_FILES = ("pyproject.toml", "uv.lock", "schema/schema.lock.json")
FRESHNESS_MUTATIONS = (
    ("fixture only", "tests/fixtures/full_schema/sdk_extensions.cdxml"),
    ("parser/runtime only", "src/cdxml_om/core/codecs.py"),
    ("SDK-only catalog", "tests/coverage/sdk_extension_cases.json"),
    ("overrides only", "schema/overrides/full_schema.yaml"),
)
SDK_TEST_PAIR = ("n", "bgcolor")


def _ignore_transient(_directory: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".pyright"}
    return set(names) & ignored


def _copy_feature_project(destination: Path) -> Path:
    destination.mkdir()
    for relative in PROJECT_DIRECTORIES:
        source = PROJECT_ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=_ignore_transient)
    for relative in PROJECT_FILES:
        source = PROJECT_ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return destination


def _sdk_feature_nodes(
    root: Path,
    pair: tuple[str, str] = SDK_TEST_PAIR,
) -> tuple[str, str]:
    catalog = json.loads((root / "tests/coverage/sdk_extension_cases.json").read_text())
    cases = cast(list[dict[str, object]], catalog["cases"])
    case = next(row for row in cases if (row["owner_tag"], row["xml_attribute"]) == pair)
    recipe = cast(dict[str, object], case["typed_recipe"])
    return cast(str, case["pytest_nodeid"]), cast(str, recipe["pytest_nodeid"])


def _run_with_local_imports(
    root: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    pytest_arguments: list[str],
    name: str,
) -> tuple[int, Path]:
    schema = load_schema(root)
    run_path = root.parent / f"{name}-run.json"
    junit_path = root.parent / f"{name}-junit.xml"
    paths = [str(root), str(root / "src")]
    paths.extend(item for item in os.environ.get("PYTHONPATH", "").split(os.pathsep) if item)
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(paths))
    result = run_feature_tests(
        root,
        schema,
        run_output=run_path,
        junit_output=junit_path,
        pytest_arguments=pytest_arguments,
    )
    return result, run_path


def _sdk_report_row(
    report: dict[str, object],
    pair: tuple[str, str] = SDK_TEST_PAIR,
) -> dict[str, object]:
    rows = cast(list[dict[str, object]], report["sdk_extension_pairs"])
    return next(row for row in rows if (row["owner_xml_name"], row["xml_name"]) == pair)


def test_actual_saved_feature_run_is_rejected_after_any_fingerprinted_scope_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _copy_feature_project(tmp_path / "project")
    raw_node, typed_node = _sdk_feature_nodes(root)
    return_code, run_path = _run_with_local_imports(
        root,
        monkeypatch,
        pytest_arguments=[typed_node],
        name="freshness",
    )
    assert return_code == 0

    schema = load_schema(root)
    catalog = _normalized_feature_catalog(root)
    report = build_coverage_report(root, schema, test_run_path=run_path)
    sdk_row = _sdk_report_row(report)
    assert sdk_row["tested"] is True
    assert sdk_row["round_trip_verified"] is True
    assert sdk_row["raw_preservation_tested"] is False
    assert raw_node != typed_node

    saved_run = json.loads(run_path.read_text(encoding="utf-8"))
    saved_fingerprints = cast(dict[str, object], saved_run["fingerprints"])
    saved_files = cast(dict[str, str], saved_fingerprints["files"])
    junit_path = run_path.parent / "freshness-junit.xml"
    assert saved_run["junit_sha256"] == hashlib.sha256(junit_path.read_bytes()).hexdigest()

    for label, relative in FRESHNESS_MUTATIONS:
        source = root / relative
        original = source.read_bytes()
        if relative.endswith(".cdxml"):
            changed = original.replace(b'bgcolor="2"', b'bgcolor="4"', 1)
        elif relative.endswith(".json"):
            changed = original + b"\n "
        else:
            changed = original + b"\n# coverage freshness test mutation\n"
        assert changed != original, relative
        source.write_bytes(changed)
        try:
            assert hashlib.sha256(changed).hexdigest() != saved_files[relative], label
            with pytest.raises(CoverageError, match="test-run is stale"):
                _feature_run_outcomes(root, schema, catalog, run_path)
        finally:
            source.write_bytes(original)
        assert hashlib.sha256(original).hexdigest() == saved_files[relative]


def _normalized_feature_catalog(
    root: Path,
) -> dict[str, object]:
    _, elements = coverage_module._pinned_inventory(root)  # pyright: ignore[reportPrivateUsage]
    tags = {item.xml_name for item in elements}
    pairs = {(item.xml_name, attribute.name) for item in elements for attribute in item.attributes}
    return coverage_module._catalog(root, tags, pairs)  # pyright: ignore[reportPrivateUsage]


def _feature_run_outcomes(
    root: Path,
    schema: Schema,
    catalog: dict[str, object],
    run_path: Path,
) -> tuple[dict[str, str], dict[str, object]]:
    return coverage_module._run_outcomes(  # pyright: ignore[reportPrivateUsage]
        root,
        schema,
        catalog,
        run_path,
    )


def _sdk_case_credit(
    catalog: dict[str, object],
    outcomes: dict[str, str],
    pair: tuple[str, str],
) -> dict[str, object]:
    sdk_cases = cast(dict[tuple[str, str], dict[str, object]], catalog["_sdk_extensions_by_key"])
    case = sdk_cases[pair]
    operations = coverage_module._sdk_extension_operations(  # pyright: ignore[reportPrivateUsage]
        case
    )
    passed = {node for node, status in outcomes.items() if status == "passed"}
    failed = {node for node, status in outcomes.items() if status == "failed"}
    skipped = {node for node, status in outcomes.items() if status == "skipped"}
    tested, tests = coverage_module._test_state(  # pyright: ignore[reportPrivateUsage]
        operations,
        passed,
        failed,
        skipped,
        required=("read", "write", "mutation"),
    )
    round_trip_verified, _ = coverage_module._test_state(  # pyright: ignore[reportPrivateUsage]
        operations,
        passed,
        failed,
        skipped,
        required=("round_trip",),
    )
    raw_node = cast(str, case["raw_pytest_nodeid"])
    return {
        "tested": tested,
        "round_trip_verified": round_trip_verified,
        "tests": tests,
        "raw_preservation_tested": raw_node in passed,
        "raw_status": outcomes[raw_node],
    }


def test_failed_skipped_and_uncollected_sdk_nodes_never_receive_coverage_credit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = _copy_feature_project(tmp_path / "project")
    failure_pair = ("n", "bgcolor")
    skipped_pair = ("b", "bgcolor")
    uncollected_pair = ("graphic", "bgcolor")
    failure_nodes = _sdk_feature_nodes(root, failure_pair)
    skipped_nodes = _sdk_feature_nodes(root, skipped_pair)
    uncollected_nodes = _sdk_feature_nodes(root, uncollected_pair)
    node_statuses = {
        failure_nodes[0]: "failed",
        failure_nodes[1]: "failed",
        skipped_nodes[0]: "skipped",
        skipped_nodes[1]: "skipped",
    }
    monkeypatch.setenv("CDXML_OM_FEATURE_STATUSES", json.dumps(node_statuses))
    pytest_arguments = [
        "-p",
        "tests.unit.coverage_status_plugin",
        *failure_nodes,
        *skipped_nodes,
    ]

    return_code, run_path = _run_with_local_imports(
        root,
        monkeypatch,
        pytest_arguments=pytest_arguments,
        name="sdk-nonpassing-statuses",
    )
    assert return_code == 1

    schema = load_schema(root)
    catalog = _normalized_feature_catalog(root)
    outcomes, run_metadata = _feature_run_outcomes(root, schema, catalog, run_path)
    assert run_metadata["identity_matches"] is True
    saved_run = json.loads(run_path.read_text(encoding="utf-8"))
    junit_path = run_path.parent / "sdk-nonpassing-statuses-junit.xml"
    assert saved_run["junit_sha256"] == hashlib.sha256(junit_path.read_bytes()).hexdigest()
    for pair, (raw_node, typed_node), status in (
        (failure_pair, failure_nodes, "failed"),
        (skipped_pair, skipped_nodes, "skipped"),
        (uncollected_pair, uncollected_nodes, "not_run"),
    ):
        row = _sdk_case_credit(catalog, outcomes, pair)
        assert row["tested"] is False
        assert row["round_trip_verified"] is False
        assert row["raw_preservation_tested"] is False

        typed_states = cast(dict[str, object], row["tests"])
        for operation in ("read", "write", "mutation", "round_trip"):
            state = cast(dict[str, object], typed_states[operation])
            assert state["passed"] is False
            assert state[status] == [typed_node]

        assert row["raw_status"] == status
        assert raw_node != typed_node
