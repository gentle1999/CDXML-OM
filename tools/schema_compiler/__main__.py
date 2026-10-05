"""CLI entry point for the canonical schema compiler."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tools.schema_compiler.errors import SchemaError
from tools.schema_compiler.generate import compare_outputs, compile_outputs, write_outputs
from tools.schema_compiler.ir import Schema
from tools.schema_compiler.loader import load_schema
from tools.schema_compiler.validate import validate_schema

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_validated() -> Schema | None:
    schema = load_schema(PROJECT_ROOT)
    issues = validate_schema(schema)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return None
    return schema


def _coverage(schema: Schema, *, output_format: str, test_run: str | None) -> int:
    from tools.schema_compiler.coverage import (
        CoverageError,
        build_coverage_report,
        report_json,
        report_text,
    )

    run_path = _rooted_path(test_run) if test_run else None
    try:
        report = build_coverage_report(PROJECT_ROOT, schema, test_run_path=run_path)
        print(report_json(report) if output_format == "json" else report_text(report), end="")
        return 0
    except CoverageError as exc:
        print(exc, file=sys.stderr)
        return 1


def _rooted_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else PROJECT_ROOT / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.schema_compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="validate schema and check generated files/lock")
    subparsers.add_parser("build", help="validate schema and regenerate static artifacts")
    coverage = subparsers.add_parser("coverage", help="report pinned DTD and feature coverage")
    coverage.add_argument("--format", choices=("text", "json"), default="text")
    coverage.add_argument(
        "--test-run",
        help="pytest-time feature run evidence produced by test-features",
    )
    feature_tests = subparsers.add_parser(
        "test-features", help="run feature cases and capture source-bound JUnit evidence"
    )
    feature_tests.add_argument("--run-evidence", required=True, help="output path for run JSON")
    feature_tests.add_argument("--junitxml", help="retain JUnit XML at this path")
    feature_tests.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="arguments passed to pytest after `--`",
    )
    args = parser.parse_args(argv)
    try:
        schema = _load_validated()
        if schema is None:
            return 1
        if args.command == "coverage":
            return _coverage(schema, output_format=args.format, test_run=args.test_run)
        if args.command == "test-features":
            from tools.schema_compiler.coverage import CoverageError, run_feature_tests

            pytest_args = args.pytest_args
            if pytest_args and pytest_args[0] == "--":
                pytest_args = pytest_args[1:]
            try:
                return run_feature_tests(
                    PROJECT_ROOT,
                    schema,
                    run_output=_rooted_path(args.run_evidence),
                    junit_output=_rooted_path(args.junitxml) if args.junitxml else None,
                    pytest_arguments=pytest_args,
                )
            except CoverageError as exc:
                print(exc, file=sys.stderr)
                return 1
        outputs = compile_outputs(schema, PROJECT_ROOT)
        if args.command == "build":
            write_outputs(outputs, PROJECT_ROOT)
            generated_count = sum(path.startswith("src/cdxml_om/_generated/") for path in outputs)
            print(f"Generated {generated_count} Python files and updated schema lock.")
            return 0
        differences = compare_outputs(outputs, PROJECT_ROOT)
        if differences:
            for difference in differences:
                print(difference, file=sys.stderr)
            print("Run `python -m tools.schema_compiler build` to regenerate.", file=sys.stderr)
            return 1
        print("Schema valid; generated files and schema lock are current.")
        return 0
    except SchemaError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
