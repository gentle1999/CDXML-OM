"""Command line for offline source import and review diffs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import NoReturn

from tools.schema_compiler.errors import SchemaError
from tools.schema_compiler.loader import load_schema
from tools.schema_compiler.validate import validate_schema
from tools.schema_importer.candidate import CandidateDocument
from tools.schema_importer.common import PROJECT_ROOT, write_text_output
from tools.schema_importer.diff import compare_candidate
from tools.schema_importer.dtd_importer import import_dtd
from tools.schema_importer.errors import ImporterError
from tools.schema_importer.sdk_importer import import_sdk_html


class _StructuredArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ImporterError("CLI_USAGE", message, self.prog)


def _parser() -> argparse.ArgumentParser:
    parser = _StructuredArgumentParser(prog="python -m tools.schema_importer")
    commands = parser.add_subparsers(dest="command", required=True)
    for command, help_text in (
        ("import-dtd", "import one local DTD as candidate evidence"),
        ("import-sdk", "import one local archived SDK HTML page"),
    ):
        subparser = commands.add_parser(command, help=help_text)
        subparser.add_argument("path", help="local input path")
        subparser.add_argument(
            "--output",
            default="-",
            help="candidate JSON path, or - for stdout (default: -)",
        )
        subparser.add_argument("--force", action="store_true", help="replace an existing output")
    diff = commands.add_parser("diff", help="compare a candidate JSON file with canonical schema")
    diff.add_argument("candidate", help="candidate JSON path")
    diff.add_argument("--output", default="-", help="diff JSON path, or - for stdout (default: -)")
    diff.add_argument("--force", action="store_true", help="replace an existing output")
    return parser


def _write_json(
    output: str,
    payload: str,
    *,
    source_path: str | None = None,
    force: bool = False,
) -> None:
    if not write_text_output(
        output,
        payload,
        source_path=source_path,
        force=force,
    ):
        sys.stdout.write(payload)


def _candidate_from_path(path_text: str) -> CandidateDocument:
    try:
        candidate_text = Path(path_text).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ImporterError("CANDIDATE_READ", str(exc), path_text) from exc
    return CandidateDocument.from_json(candidate_text)


def _diff_candidate(candidate: CandidateDocument) -> dict[str, object]:
    try:
        schema = load_schema(PROJECT_ROOT)
    except SchemaError as exc:
        raise ImporterError("CANONICAL_SCHEMA", str(exc), "schema/canonical") from exc
    issues = validate_schema(schema)
    if issues:
        raise ImporterError(
            "CANONICAL_SCHEMA",
            "; ".join(str(issue) for issue in issues),
            "schema/canonical",
        )
    return compare_candidate(candidate, schema)


def _error_json(error: ImporterError) -> str:
    return json.dumps(
        {
            "format": "cdxml-om-schema-import-error",
            "format_version": 1,
            "error": error.as_dict(),
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.command == "import-dtd":
            candidate = import_dtd(args.path)
            _write_json(
                args.output,
                candidate.to_json(),
                source_path=args.path,
                force=args.force,
            )
            return 0
        if args.command == "import-sdk":
            candidate = import_sdk_html(args.path)
            _write_json(
                args.output,
                candidate.to_json(),
                source_path=args.path,
                force=args.force,
            )
            return 0
        candidate = _candidate_from_path(args.candidate)
        diff_text = (
            json.dumps(_diff_candidate(candidate), ensure_ascii=False, indent=2, sort_keys=True)
            + "\n"
        )
        _write_json(
            args.output,
            diff_text,
            source_path=args.candidate,
            force=args.force,
        )
        return 0
    except ImporterError as exc:
        print(_error_json(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
