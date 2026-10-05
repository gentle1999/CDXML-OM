"""Keep the bilingual documentation navigable and its examples executable."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import cast
from urllib.parse import unquote, urlsplit

import pytest

from cdxml_om._generated.schema_registry import OBJECT_BY_XML_TAG

ROOT = Path(__file__).resolve().parents[2]
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
INLINE_CODE_SPAN_RE = re.compile(r"(?<!`)(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)", re.DOTALL)
LINK_RE = re.compile(
    r"!?\[(?P<label>(?:`+[^`]*`+|\\.|[^\]])+)\]"
    r"\(\s*(?P<destination><[^>]+>|(?:\\.|[^()\s])+)(?:\s+(?P<quote>['\"]).*?(?P=quote))?\s*\)"
)
TABLE_MARKUP_RE = re.compile(r"`([^`]*)`|\[([^\]]+)\]\([^)]*\)|<[^>]+>")

PAGE_PAIRS = (
    ("README.md", "README.zh-CN.md"),
    ("docs/index.md", "docs/zh-CN/index.md"),
    ("docs/architecture.md", "docs/zh-CN/architecture.md"),
    ("docs/schema.md", "docs/zh-CN/schema.md"),
    ("docs/compatibility.md", "docs/zh-CN/compatibility.md"),
    ("docs/coverage.md", "docs/zh-CN/coverage.md"),
    ("docs/ingestion.md", "docs/zh-CN/ingestion.md"),
    ("docs/specification-baseline.md", "docs/zh-CN/specification-baseline.md"),
    ("docs/feature-support.md", "docs/zh-CN/feature-support.md"),
    ("docs/feature-tests.md", "docs/zh-CN/feature-tests.md"),
    (
        "docs/adr/0001-conservative-reference-and-content-boundaries.md",
        "docs/zh-CN/adr/0001-conservative-reference-and-content-boundaries.md",
    ),
    (
        "docs/adr/0002-semantic-static-metadata.md",
        "docs/zh-CN/adr/0002-semantic-static-metadata.md",
    ),
)


def _markdown_files() -> tuple[Path, ...]:
    files = [ROOT / "README.md", ROOT / "README.zh-CN.md"]
    files.extend((ROOT / "docs").rglob("*.md"))
    return tuple(sorted(set(files)))


def _fenced_blocks(markdown: str) -> list[tuple[str, str]]:
    """Return language/content pairs for fenced blocks, supporting backticks and tildes."""
    lines = markdown.splitlines()
    blocks: list[tuple[str, str]] = []
    index = 0
    while index < len(lines):
        opening = FENCE_RE.match(lines[index])
        if opening is None:
            index += 1
            continue

        fence = opening.group(1)
        language = (
            opening.group(2).strip().split(maxsplit=1)[0].lower()
            if opening.group(2).strip()
            else ""
        )
        content: list[str] = []
        index += 1
        while index < len(lines):
            closing = re.match(r"^\s*(`+|~+)\s*$", lines[index])
            if (
                closing is not None
                and closing.group(1)[0] == fence[0]
                and len(closing.group(1)) >= len(fence)
            ):
                blocks.append((language, "\n".join(content)))
                index += 1
                break
            content.append(lines[index])
            index += 1
        else:
            raise AssertionError("unclosed fenced code block in Markdown")
    return blocks


def _without_fences(markdown: str) -> str:
    lines = markdown.splitlines()
    visible: list[str] = []
    index = 0
    while index < len(lines):
        opening = FENCE_RE.match(lines[index])
        if opening is None:
            visible.append(lines[index])
            index += 1
            continue
        fence = opening.group(1)
        index += 1
        while index < len(lines):
            closing = re.match(r"^\s*(`+|~+)\s*$", lines[index])
            if (
                closing is not None
                and closing.group(1)[0] == fence[0]
                and len(closing.group(1)) >= len(fence)
            ):
                index += 1
                break
            index += 1
        else:
            raise AssertionError("unclosed fenced code block in Markdown")
    return "\n".join(visible)


def _markdown_links(markdown_path: Path, markdown: str) -> list[tuple[str, Path]]:
    visible = _without_fences(markdown)
    code_spans = [match.span() for match in INLINE_CODE_SPAN_RE.finditer(visible)]
    links: list[tuple[str, Path]] = []
    for match in LINK_RE.finditer(visible):
        if any(start <= match.start() < end for start, end in code_spans):
            continue
        destination = match.group("destination")
        if destination.startswith("<") and destination.endswith(">"):
            destination = destination[1:-1]
        destination = destination.replace(r"\(", "(").replace(r"\)", ")")
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc:
            continue
        if not parsed.path:
            continue
        path_text = unquote(parsed.path)
        target = (
            ROOT / path_text.lstrip("/")
            if path_text.startswith("/")
            else markdown_path.parent / path_text
        )
        label = match.group("label").replace("`", "")
        links.append((label, target.resolve()))
    return links


def _link_paths(markdown_path: Path, markdown: str) -> set[Path]:
    return {target for _, target in _markdown_links(markdown_path, markdown)}


def _plain_table_cell(cell: str) -> str:
    def replace_markup(match: re.Match[str]) -> str:
        if match.group(1) is not None:
            return match.group(1)
        if match.group(2) is not None:
            return match.group(2)
        return match.group(0)[1:-1]

    return TABLE_MARKUP_RE.sub(replace_markup, cell).strip()


def _feature_table(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    rows: dict[str, str] = {}
    found_table = False
    for index, line in enumerate(lines[:-1]):
        header = [_plain_table_cell(cell).casefold() for cell in line.strip().strip("|").split("|")]
        if len(header) < 2 or tuple(header[:2]) not in {
            ("xml tag", "public model"),
            ("xml 标签", "公开模型"),
        }:
            continue
        found_table = True
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [_plain_table_cell(cell) for cell in row.strip().strip("|").split("|")]
            if len(cells) < 2 or all(set(cell.replace(":", "")) <= {"-", " "} for cell in cells):
                continue
            tag, model = cells[:2]
            if tag and model:
                assert tag not in rows, f"duplicate XML tag {tag!r} in feature table"
                rows[tag] = model
    assert found_table, "feature-support page must contain an XML tag / Public model table"
    return rows


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(":", "")) <= {"-", " "} for cell in cells)


def _feature_id(label: str, prefix: str) -> str | None:
    match = re.search(rf"{re.escape(prefix)}:[^\]\s]+", label)
    return match.group(0) if match is not None else None


def _test_source_path(nodeid: str) -> Path:
    module = nodeid.split("::", maxsplit=1)[0]
    return (ROOT / module).resolve()


def _nodeid_function(nodeid: str) -> str:
    assert "::" in nodeid, f"invalid pytest node ID {nodeid!r}"
    return nodeid.split("::", maxsplit=1)[1].split("[", maxsplit=1)[0]


def _test_function_names(relative: str) -> set[str]:
    tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _json_catalog(relative: str) -> dict[str, object]:
    data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return cast(dict[str, object], data)


def _catalog_records(relative: str, key: str) -> list[dict[str, object]]:
    rows = _json_catalog(relative).get(key)
    assert isinstance(rows, list), f"{relative} has no {key!r} array"
    result: list[dict[str, object]] = []
    for row in cast(list[object], rows):
        assert isinstance(row, dict)
        result.append(cast(dict[str, object], row))
    return result


def _catalog_string(row: dict[str, object], key: str) -> str:
    value = row.get(key)
    assert isinstance(value, str), f"catalog entry has no string {key!r}"
    return value


def _nested_catalog_string(row: dict[str, object], parent: str, key: str) -> str:
    nested = row.get(parent)
    assert isinstance(nested, dict), f"catalog entry has no {parent!r} object"
    return _catalog_string(cast(dict[str, object], nested), key)


def _element_test_references(relative: str) -> dict[str, tuple[str, str, Path]]:
    markdown_path = ROOT / relative
    markdown = markdown_path.read_text(encoding="utf-8")
    lines = markdown.splitlines()
    result: dict[str, tuple[str, str, Path]] = {}
    for index, line in enumerate(lines[:-1]):
        header = [_plain_table_cell(cell).casefold() for cell in _table_cells(line)]
        if len(header) < 3 or tuple(header[:2]) not in {
            ("xml tag", "public model"),
            ("xml 标签", "公开模型"),
        }:
            continue
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = _table_cells(row)
            if _is_table_separator(cells) or len(cells) < 3:
                continue
            tag, model = (_plain_table_cell(cell) for cell in cells[:2])
            references = [
                (label, target)
                for label, target in _markdown_links(markdown_path, row)
                if _feature_id(label, "feature-element") is not None
            ]
            assert len(references) == 1, (
                f"{relative} element row {tag!r} needs one feature test link"
            )
            label, target = references[0]
            assert tag not in result, f"duplicate element test reference for {tag!r} in {relative}"
            result[tag] = (model, label, target)
    assert result, f"{relative} has no element test references"
    return result


def _sdk_test_references(relative: str) -> dict[str, tuple[str, str, str, Path]]:
    markdown_path = ROOT / relative
    result: dict[str, tuple[str, str, str, Path]] = {}
    for line in markdown_path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        links = [
            (label, target)
            for label, target in _markdown_links(markdown_path, line)
            if _feature_id(label, "feature-sdk") is not None
        ]
        if not links:
            continue
        cells = _table_cells(line)
        assert len(cells) >= 3
        assert len(links) == 1, f"{relative} SDK row must link one typed feature case"
        label, target = links[0]
        case_id = _feature_id(label, "feature-sdk")
        assert case_id is not None
        assert case_id not in result, f"duplicate SDK feature reference {case_id!r} in {relative}"
        result[case_id] = (
            _plain_table_cell(cells[0]),
            _plain_table_cell(cells[1]),
            label,
            target,
        )
    assert result, f"{relative} has no SDK feature references"
    return result


def _character_data_references(relative: str) -> dict[str, tuple[str, Path, Path | None]]:
    markdown_path = ROOT / relative
    result: dict[str, tuple[str, Path, Path | None]] = {}
    for line in markdown_path.read_text(encoding="utf-8").splitlines():
        if "feature-character:" not in line:
            continue
        links = _markdown_links(markdown_path, line)
        function_targets = [
            target
            for label, target in links
            if label == "test_character_data_parse_read_mutate_serialize_reload"
        ]
        for label, target in links:
            case_id = _feature_id(label, "feature-character")
            if case_id is None:
                continue
            assert case_id not in result, (
                f"duplicate character-data reference {case_id!r} in {relative}"
            )
            result[case_id] = (
                label,
                target,
                function_targets[0] if len(function_targets) == 1 else None,
            )
    assert result, f"{relative} has no PCDATA references"
    return result


def _appendix_case_references(relative: str) -> dict[tuple[str, str], tuple[str, Path]]:
    markdown_path = ROOT / relative
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    owner: str | None = None
    result: dict[tuple[str, str], tuple[str, Path]] = {}
    for line in lines:
        if line.startswith("### XML owner:"):
            owner = line.split(":", maxsplit=1)[1].strip().strip(chr(96))
        elif line.startswith("### XML 所属标签："):
            owner = line.split("：", maxsplit=1)[1].strip().strip(chr(96))
        if owner is None or not line.strip().startswith("|"):
            continue
        cells = _table_cells(line)
        if len(cells) < 2 or _is_table_separator(cells):
            continue
        header = [_plain_table_cell(cell).casefold() for cell in cells[:2]]
        if header in (
            ["xml attribute", "feature id / test source"],
            ["xml 属性", "特性 id / 测试源码"],
        ):
            continue
        attribute = _plain_table_cell(cells[0])
        references = [
            (label, target)
            for label, target in _markdown_links(markdown_path, line)
            if _feature_id(label, "feature") is not None
        ]
        if not references:
            continue
        assert len(references) == 1, f"{relative} DTD row needs one feature ID link"
        label, target = references[0]
        case_id = _feature_id(label, "feature")
        assert case_id is not None
        key = (owner, attribute)
        assert key not in result, f"duplicate DTD feature reference {key!r} in {relative}"
        result[key] = (case_id, target)
    assert result, f"{relative} has no DTD attribute feature index"
    return result


def test_all_local_markdown_links_resolve() -> None:
    markdown_files = _markdown_files()
    assert markdown_files
    missing_pages = [
        path.relative_to(ROOT).as_posix() for path in markdown_files if not path.is_file()
    ]
    assert not missing_pages, f"missing documentation pages: {missing_pages}"

    broken: list[str] = []
    for path in markdown_files:
        for target in _link_paths(path, path.read_text(encoding="utf-8")):
            if not target.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    assert not broken, "broken local Markdown links:\n" + "\n".join(broken)


def test_bilingual_selectors_and_navigation_are_bidirectional() -> None:
    page_text = {
        ROOT / relative: (ROOT / relative).read_text(encoding="utf-8")
        for pair in PAGE_PAIRS
        for relative in pair
    }
    for english, chinese in PAGE_PAIRS:
        english_path = ROOT / english
        chinese_path = ROOT / chinese
        assert chinese_path.resolve() in _link_paths(english_path, page_text[english_path]), english
        assert english_path.resolve() in _link_paths(chinese_path, page_text[chinese_path]), chinese

    english_index = _link_paths(ROOT / "docs/index.md", page_text[ROOT / "docs/index.md"])
    chinese_index = _link_paths(
        ROOT / "docs/zh-CN/index.md", page_text[ROOT / "docs/zh-CN/index.md"]
    )
    for english, chinese in PAGE_PAIRS[2:]:
        if english.endswith("/index.md"):
            continue
        assert (ROOT / english).resolve() in english_index, f"English navigation omits {english}"
        assert (ROOT / chinese).resolve() in chinese_index, f"Chinese navigation omits {chinese}"


@pytest.mark.parametrize("relative", ("docs/feature-support.md", "docs/zh-CN/feature-support.md"))
def test_feature_support_table_matches_generated_tag_model_registry(relative: str) -> None:
    markdown = (ROOT / relative).read_text(encoding="utf-8")
    actual = _feature_table(markdown)
    expected = {tag: model.__name__ for tag, model in OBJECT_BY_XML_TAG.items()}
    assert len(expected) == 53
    assert len(actual) == len(expected), (
        f"{relative} lists {len(actual)} rows; expected {len(expected)}"
    )
    assert actual == expected


def test_bilingual_element_rows_link_the_catalog_lifecycle_cases() -> None:
    catalog_rows = _catalog_records("tests/coverage/feature_cases.json", "element_cases")
    assert len(catalog_rows) == len(OBJECT_BY_XML_TAG) == 53
    expected_models = {tag: model.__name__ for tag, model in OBJECT_BY_XML_TAG.items()}
    expected: dict[str, tuple[str, str, str]] = {}
    for row in catalog_rows:
        tag = _catalog_string(row, "xml_name")
        case_id = _catalog_string(row, "case_id")
        nodeid = _catalog_string(row, "pytest_nodeid")
        model = _catalog_string(row, "expected_model")
        assert case_id == f"feature-element:{tag}"
        assert model == expected_models[tag]
        function = _nodeid_function(nodeid)
        expected_function = (
            "test_root_creation_mutation_round_trip"
            if tag == "CDXML"
            else "test_element_create_remove_round_trip"
        )
        assert function == expected_function
        assert nodeid == (
            f"tests/coverage/test_full_schema_feature_evidence.py::{function}[{case_id}]"
        )
        expected[tag] = (case_id, function, nodeid)

    source_functions = _test_function_names("tests/coverage/test_full_schema_feature_evidence.py")
    actual_by_language: list[dict[str, tuple[str, Path]]] = []
    for relative in ("docs/feature-support.md", "docs/zh-CN/feature-support.md"):
        markdown = (ROOT / relative).read_text(encoding="utf-8")
        assert "test_element_create_remove_round_trip[feature-element:<tag>]" in markdown
        assert "test_root_creation_mutation_round_trip[feature-element:CDXML]" in markdown
        refs = _element_test_references(relative)
        assert set(refs) == set(expected)
        actual: dict[str, tuple[str, Path]] = {}
        for tag, (model, label, target) in refs.items():
            case_id = _feature_id(label, "feature-element")
            assert case_id is not None
            expected_case_id, function, nodeid = expected[tag]
            assert model == expected_models[tag]
            assert case_id == expected_case_id
            assert label in {case_id, f"{function}[{case_id}]"}
            assert target == _test_source_path(nodeid)
            assert function in source_functions
            actual[tag] = (case_id, target)
        actual_by_language.append(actual)
    assert actual_by_language[0] == actual_by_language[1]


def test_bilingual_sdk_rows_link_all_typed_extension_cases() -> None:
    catalog_rows = _catalog_records("tests/coverage/sdk_extension_cases.json", "cases")
    expected: dict[str, tuple[str, str, str, str]] = {}
    for row in catalog_rows:
        case_id = _catalog_string(row, "case_id")
        owner = _catalog_string(row, "owner_tag")
        attribute = _catalog_string(row, "xml_attribute")
        nodeid = _nested_catalog_string(row, "typed_recipe", "pytest_nodeid")
        function = _nodeid_function(nodeid)
        assert row.get("typed_status") == "typed"
        assert case_id == f"feature-sdk:{owner}@{attribute}"
        assert function == "test_sdk_extension_typed_mutation_roundtrip"
        assert nodeid == (
            f"tests/coverage/test_sdk_extension_feature_evidence.py::{function}[{case_id}]"
        )
        assert case_id not in expected
        expected[case_id] = (owner, attribute, function, nodeid)
    assert len(expected) == 23

    source_functions = _test_function_names("tests/coverage/test_sdk_extension_feature_evidence.py")
    actual_by_language: list[dict[str, tuple[str, str, Path]]] = []
    for relative in ("docs/feature-support.md", "docs/zh-CN/feature-support.md"):
        markdown = (ROOT / relative).read_text(encoding="utf-8")
        assert "test_sdk_extension_typed_mutation_roundtrip" in markdown
        refs = _sdk_test_references(relative)
        assert set(refs) == set(expected)
        actual: dict[str, tuple[str, str, Path]] = {}
        for case_id, (owner, attribute, label, target) in refs.items():
            expected_owner, expected_attribute, function, nodeid = expected[case_id]
            assert (owner, attribute) == (expected_owner, expected_attribute)
            assert label in {case_id, f"{function}[{case_id}]"}
            assert target == _test_source_path(nodeid)
            assert function in source_functions
            actual[case_id] = (owner, attribute, target)
        actual_by_language.append(actual)
    assert actual_by_language[0] == actual_by_language[1]


def test_bilingual_pcdata_rows_link_both_typed_roundtrip_cases() -> None:
    catalog_rows = _catalog_records("tests/coverage/feature_cases.json", "character_data_cases")
    expected: dict[str, tuple[str, str, str]] = {}
    for row in catalog_rows:
        tag = _catalog_string(row, "xml_name")
        case_id = _catalog_string(row, "case_id")
        nodeid = _catalog_string(row, "pytest_nodeid")
        function = _nodeid_function(nodeid)
        assert case_id == f"feature-character:{tag}"
        assert function == "test_character_data_parse_read_mutate_serialize_reload"
        assert nodeid == (
            f"tests/coverage/test_full_schema_feature_evidence.py::{function}[{case_id}]"
        )
        expected[case_id] = (tag, function, nodeid)
    assert set(expected) == {"feature-character:s", "feature-character:spectrum"}

    source_functions = _test_function_names("tests/coverage/test_full_schema_feature_evidence.py")
    actual_by_language: list[dict[str, tuple[str, Path]]] = []
    for relative in ("docs/feature-support.md", "docs/zh-CN/feature-support.md"):
        refs = _character_data_references(relative)
        assert set(refs) == set(expected)
        actual: dict[str, tuple[str, Path]] = {}
        for case_id, (label, target, function_target) in refs.items():
            _, function, nodeid = expected[case_id]
            assert label == case_id
            assert target == _test_source_path(nodeid)
            assert function_target == _test_source_path(nodeid)
            assert function in source_functions
            actual[case_id] = (label, target)
        actual_by_language.append(actual)
    assert actual_by_language[0] == actual_by_language[1]


def test_bilingual_attribute_test_indexes_match_all_762_catalog_cases() -> None:
    catalog_rows = _catalog_records("tests/coverage/feature_cases.json", "cases")
    assert len(catalog_rows) == 762
    expected: dict[tuple[str, str], tuple[str, str]] = {}
    nodeids_by_case_id: dict[str, str] = {}
    for row in catalog_rows:
        owner = _catalog_string(row, "owner_tag")
        attribute = _catalog_string(row, "xml_attribute")
        case_id = _catalog_string(row, "case_id")
        nodeid = _catalog_string(row, "pytest_nodeid")
        function = _nodeid_function(nodeid)
        key = (owner, attribute)
        assert case_id == f"feature:{owner}@{attribute}"
        assert function == "test_mapped_pair_parse_read_mutate_serialize_reload"
        assert nodeid == (
            f"tests/coverage/test_full_schema_feature_evidence.py::{function}[{case_id}]"
        )
        assert key not in expected
        expected[key] = (case_id, nodeid)
        nodeids_by_case_id[case_id] = nodeid
    assert len(expected) == 762

    source_functions = _test_function_names("tests/coverage/test_full_schema_feature_evidence.py")
    function = "test_mapped_pair_parse_read_mutate_serialize_reload"
    assert function in source_functions
    sample_nodeid = nodeids_by_case_id["feature:n@Element"]
    actual_by_language: list[dict[tuple[str, str], tuple[str, Path]]] = []
    for relative in ("docs/feature-tests.md", "docs/zh-CN/feature-tests.md"):
        path = ROOT / relative
        markdown = path.read_text(encoding="utf-8")
        assert markdown.endswith("\n")
        assert not markdown.endswith("\n\n"), f"{relative} has a blank line at EOF"
        assert f"{function}[<feature-case-id>]" in markdown
        assert sample_nodeid in markdown
        refs = _appendix_case_references(relative)
        assert set(refs) == set(expected), f"{relative} owner/attribute cases differ from catalog"
        actual: dict[tuple[str, str], tuple[str, Path]] = {}
        for key, (case_id, target) in refs.items():
            expected_case_id, nodeid = expected[key]
            assert case_id == expected_case_id
            assert target == _test_source_path(nodeid)
            actual[key] = (case_id, target)
        actual_by_language.append(actual)
    assert actual_by_language[0] == actual_by_language[1]


def test_schema_override_guide_describes_existing_reviewed_overrides() -> None:
    guide = (ROOT / "schema/overrides/README.md").read_text(encoding="utf-8")
    overrides = (ROOT / "schema/overrides/full_schema.yaml").read_text(encoding="utf-8")
    assert "No overrides are currently defined" not in guide
    for section in (
        "object_models:",
        "reference_targets:",
        "property_type_families:",
        "sdk_property_conflicts:",
        "source_anomalies:",
    ):
        assert section in overrides
        assert section.removesuffix(":") in guide
    assert guide.endswith("\n")
    assert not guide.endswith("\n\n")


def test_coverage_docs_state_scope_counts_and_application_boundary() -> None:
    english = (ROOT / "docs/coverage.md").read_text(encoding="utf-8")
    chinese = (ROOT / "docs/zh-CN/coverage.md").read_text(encoding="utf-8")
    for count in (53, 762, 2, 20, 23, 3):
        assert re.search(rf"(?<!\d){count}(?!\d)", english), f"English coverage doc omits {count}"
        assert re.search(rf"(?<!\d){count}(?!\d)", chinese), f"Chinese coverage doc omits {count}"

    assert re.search(
        r"ChemDraw.{0,140}(?:not|no|separate|unverified|\b0\b)", english, re.I | re.S
    ) or re.search(r"(?:not|no|separate|unverified).{0,140}ChemDraw", english, re.I | re.S), (
        "English coverage text must distinguish mapper evidence from ChemDraw verification"
    )
    assert "ChemDraw" in chinese
    assert re.search(
        r"ChemDraw.{0,100}(?:不代表|不等于|未验证|并非|尚未|\b0\b)", chinese, re.S
    ) or re.search(r"(?:不代表|不等于|未验证|并非|尚未).{0,100}ChemDraw", chinese, re.S), (
        "Chinese coverage text must distinguish mapper evidence from ChemDraw verification"
    )


def _graph_example(readme: str) -> str:
    candidates = [
        code
        for language, code in _fenced_blocks(readme)
        if language == "python"
        and all(
            token in code
            for token in (
                "CDXMLDocument.from_string",
                ".nodes.create(",
                ".bonds.create(",
                ".validate()",
                ".to_file(",
                "CDXMLDocument.from_file",
                "reloaded",
            )
        )
    ]
    assert len(candidates) == 1, "README must have one self-contained graph round-trip example"
    return candidates[0]


def test_bilingual_readme_graph_examples_have_equivalent_python_behavior() -> None:
    english = _graph_example((ROOT / "README.md").read_text(encoding="utf-8"))
    chinese = _graph_example((ROOT / "README.zh-CN.md").read_text(encoding="utf-8"))
    assert ast.dump(ast.parse(english), include_attributes=False) == ast.dump(
        ast.parse(chinese), include_attributes=False
    )


@pytest.mark.parametrize("relative", ("README.md", "README.zh-CN.md"))
def test_readme_graph_roundtrip_example_executes_in_temporary_directory(
    relative: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme = (ROOT / relative).read_text(encoding="utf-8")
    code = _graph_example(readme)
    syntax_tree = ast.parse(code)
    write_targets: set[str] = set()
    read_targets: set[str] = set()
    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr not in {"to_file", "from_file"}:
                continue
            assert node.args and isinstance(node.args[0], ast.Constant)
            assert isinstance(node.args[0].value, str)
            file_path = Path(node.args[0].value)
            assert not file_path.is_absolute() and ".." not in file_path.parts
            if node.func.attr == "to_file":
                write_targets.add(node.args[0].value)
            else:
                read_targets.add(node.args[0].value)
    assert write_targets and write_targets == read_targets

    monkeypatch.chdir(tmp_path)
    namespace: dict[str, object] = {}
    exec(compile(syntax_tree, relative + " graph example", "exec"), namespace)

    from cdxml_om import Bond, CDXMLDocument, Node, Point2D

    reloaded = namespace["reloaded"]
    assert isinstance(reloaded, CDXMLDocument)
    assert list(tmp_path.rglob("*.cdxml")), "README example did not write a CDXML file"
    assert reloaded.validate().is_valid
    fragment = reloaded.pages[0].fragments[0]
    assert len(fragment.nodes) == 2
    assert len(fragment.bonds) == 1
    assert fragment.nodes[0].element == 6
    assert fragment.nodes[0].position == Point2D(0.0, 0.0)
    assert fragment.nodes[1].element == 8
    assert fragment.nodes[1].position == Point2D(10.0, 0.0)
    assert fragment.nodes[1].charge == -1
    bond = fragment.bonds[0]
    assert isinstance(bond, Bond)
    assert bond.order.value == 2
    assert isinstance(bond.begin, Node)
    assert isinstance(bond.end, Node)
    assert bond.begin is fragment.nodes[0]
    assert bond.end is fragment.nodes[1]
    assert bond.begin is not bond.end


def test_markdown_link_parser_ignores_fences_and_handles_fragment_and_title() -> None:
    markdown_path = ROOT / "docs" / "probe.md"
    markdown = (
        "`[inline](missing-inline.md)`\n\n"
        "```text\n[example](missing-fenced.md)\n```\n\n"
        '[coverage](coverage.md#scope "optional title") and [top](#heading)'
    )

    assert _link_paths(markdown_path, markdown) == {(ROOT / "docs" / "coverage.md").resolve()}


def test_markdown_link_parser_keeps_code_labeled_links_and_skips_inline_code_links() -> None:
    markdown_path = ROOT / "docs" / "feature-support.md"
    markdown = (
        "`[fake](missing-inline.md)`\n\n"
        "[`test_element_create_remove_round_trip[feature-element:n]`]("
        '../tests/coverage/test_full_schema_feature_evidence.py "test source")'
    )

    assert _markdown_links(markdown_path, markdown) == [
        (
            "test_element_create_remove_round_trip[feature-element:n]",
            (ROOT / "tests/coverage/test_full_schema_feature_evidence.py").resolve(),
        )
    ]


def test_feature_table_parser_aggregates_groups_and_rejects_duplicate_tags() -> None:
    grouped = """\
### First group

| XML tag | Public model |
| --- | --- |
| `CDXML` | `CDXMLRoot` |

### Second group

| XML tag | Public model |
| --- | --- |
| `page` | `Page` |

### 第三组

| XML 标签 | 公开模型 |
| --- | --- |
| `annotation` | `Annotation` |
"""
    assert _feature_table(grouped) == {
        "CDXML": "CDXMLRoot",
        "page": "Page",
        "annotation": "Annotation",
    }

    duplicated = (
        grouped
        + "\n### Fourth group\n\n| XML 标签 | 公开模型 |\n| --- | --- |\n| `page` | `Page` |\n"
    )
    with pytest.raises(AssertionError, match="duplicate XML tag 'page'"):
        _feature_table(duplicated)
