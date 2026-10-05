"""Import archived SDK HTML tables as raw, locally supplied evidence."""

from __future__ import annotations

import re

from lxml import etree, html
from lxml.html import HtmlElement

from tools.schema_importer.candidate import (
    CandidateDocument,
    SDKEntryCandidate,
    SDKNamespace,
    SDKRelation,
)
from tools.schema_importer.common import read_local_input
from tools.schema_importer.errors import ImporterError

_EXTERNAL_MARKUP = re.compile(
    rb"<!\s*(?:DOCTYPE|ENTITY)\b[^>]*\b(?:SYSTEM|PUBLIC)\b", re.IGNORECASE | re.DOTALL
)
_HEX_VALUE = re.compile(r"^0[xX]([0-9a-fA-F]+)$")
_DECIMAL_VALUE = re.compile(r"^[+-]?[0-9]+$")


def _cell_text(cell: HtmlElement) -> str:
    return " ".join(" ".join(cell.itertext()).split())


def _normalized_header(value: str) -> str:
    return " ".join(value.strip().rstrip(":").casefold().split())


def _optional_cell(value: str) -> str | None:
    normalized = value.strip()
    if not normalized or normalized.casefold() in {"n/a", "na", "—", "–"}:
        return None
    return normalized


def _numeric_value(value: str | None) -> int | None:
    if value is None:
        return None
    match = _HEX_VALUE.fullmatch(value.strip())
    if match is not None:
        return int(match.group(1), 16)
    if _DECIMAL_VALUE.fullmatch(value.strip()) is not None:
        return int(value)
    return None


def _namespace(constant: str | None, *, property_table: bool = False) -> SDKNamespace:
    if property_table:
        return "property"
    if constant is not None and constant.startswith("kCDXObj_"):
        return "object"
    if constant is not None and constant.startswith("kCDXProp_"):
        return "property"
    if constant is None:
        return "xml-only"
    return "unknown"


def _direct_cells(row: HtmlElement) -> list[HtmlElement]:
    return [node for node in row.xpath("./th | ./td") if isinstance(node, HtmlElement)]


def _table_rows(table: HtmlElement) -> list[HtmlElement]:
    """Select only rows owned by this table, not rows from layout sub-tables."""
    rows: list[HtmlElement] = []
    for node in table.xpath(".//tr"):
        if not isinstance(node, HtmlElement):
            continue
        nearest_table = node.xpath("ancestor::table[1]")
        if nearest_table and nearest_table[0] is table:
            rows.append(node)
    return rows


def _table_entries(
    document: HtmlElement,
    owner_xml_name: str | None,
) -> tuple[list[SDKEntryCandidate], bool]:
    entries: list[SDKEntryCandidate] = []
    saw_inventory = False
    tables = [node for node in document.xpath("//table") if isinstance(node, HtmlElement)]
    for table_index, table in enumerate(tables):
        rows = _table_rows(table)
        header_index: int | None = None
        headers: tuple[str, ...] = ()
        for row_index, row in enumerate(rows):
            cells = _direct_cells(row)
            candidate_headers = tuple(_normalized_header(_cell_text(cell)) for cell in cells)
            required = {"value", "name", "cdxml name"}
            if required.issubset(candidate_headers):
                header_index = row_index
                headers = candidate_headers
                break
        if header_index is None:
            continue

        header_positions = {header: index for index, header in enumerate(headers)}
        minimum_cells = max(position for header, position in header_positions.items() if header) + 1
        is_inventory = "object" in header_positions
        has_type = "type" in header_positions
        if is_inventory:
            relation: SDKRelation = "inventory"
            saw_inventory = True
        elif has_type:
            relation = "property"
        else:
            relation = "subobject"

        for row_index, row in enumerate(rows[header_index + 1 :], start=header_index + 1):
            cells = _direct_cells(row)
            if len(cells) < minimum_cells:
                continue
            values = tuple(_cell_text(cell) for cell in cells[: len(headers)]) + tuple(
                "" for _ in range(max(0, len(headers) - len(cells)))
            )
            if tuple(_normalized_header(value) for value in values) == headers:
                continue
            raw_value = values[header_positions["value"]].strip()
            value_text = raw_value or None
            name_text = _optional_cell(values[header_positions["name"]])
            xml_name = _optional_cell(values[header_positions["cdxml name"]])
            display_name = (
                _optional_cell(values[header_positions["object"]]) if is_inventory else None
            )
            type_name = _optional_cell(values[header_positions["type"]]) if has_type else None
            record_namespace = _namespace(name_text, property_table=relation == "property")
            if (
                value_text is None
                and name_text is None
                and xml_name is None
                and display_name is None
            ):
                continue
            entries.append(
                SDKEntryCandidate(
                    namespace=record_namespace,
                    relation=relation,
                    display_name=display_name or name_text,
                    value_text=value_text,
                    cdx_id=_numeric_value(value_text),
                    cdx_constant=name_text,
                    xml_name=xml_name,
                    type_name=type_name,
                    owner_xml_name=owner_xml_name,
                    locator=f"table[{table_index}]/row[{row_index}]",
                )
            )
    return entries, saw_inventory


def _summary(document: HtmlElement) -> dict[str, str]:
    summary: dict[str, str] = {}
    recognized = {
        "cdxml name": "xml_name",
        "cdx constant name": "cdx_constant",
        "cdx constant value": "cdx_value",
    }
    tables = [node for node in document.xpath("//table") if isinstance(node, HtmlElement)]
    for table in tables:
        for row in _table_rows(table):
            cells = _direct_cells(row)
            if len(cells) != 2:
                continue
            label = _normalized_header(_cell_text(cells[0]))
            target = recognized.get(label)
            if target is None:
                continue
            value = _optional_cell(_cell_text(cells[1]))
            if value is not None:
                summary[target] = value
    return summary


def _heading(document: HtmlElement) -> str | None:
    for xpath in ("//h1", "//title"):
        matches = [node for node in document.xpath(xpath) if isinstance(node, HtmlElement)]
        if matches:
            text = " ".join(" ".join(matches[0].itertext()).split())
            if text:
                return text
    return None


def import_sdk_html(path_text: str) -> CandidateDocument:
    """Parse one local archived SDK HTML page without loading external resources."""
    raw, source = read_local_input(path_text, "sdk-html")
    if _EXTERNAL_MARKUP.search(raw) is not None:
        raise ImporterError(
            "EXTERNAL_HTML_REFERENCE",
            "external DOCTYPE/ENTITY declarations are refused in offline HTML input",
            path_text,
        )
    # The archived CambridgeSoft pages contain malformed HTML (for example,
    # unmatched legacy </font> tags). Recovery is safe here because external
    # declarations are rejected above and network access remains disabled.
    parser = html.HTMLParser(no_network=True, recover=True, default_doctype=False)
    try:
        document = html.document_fromstring(raw, parser=parser)
    except (etree.ParserError, etree.XMLSyntaxError, ValueError) as exc:
        raise ImporterError("SDK_HTML_PARSE", str(exc), path_text) from exc

    normalizations = tuple(
        "HTML recovery diagnostic: "
        f"line {entry.line}, column {entry.column}, {entry.type_name}: {entry.message}"
        for entry in parser.error_log
    )
    summary = _summary(document)
    owner_xml_name = summary.get("xml_name")
    entries: list[SDKEntryCandidate] = []
    if owner_xml_name is not None or "cdx_constant" in summary:
        title = _heading(document)
        display_name = title.removesuffix(" Object").strip() if title is not None else None
        constant = summary.get("cdx_constant")
        value_text = summary.get("cdx_value")
        entries.append(
            SDKEntryCandidate(
                namespace=_namespace(constant),
                relation="summary",
                display_name=display_name,
                value_text=value_text,
                cdx_id=_numeric_value(value_text),
                cdx_constant=constant,
                xml_name=owner_xml_name,
                type_name=None,
                owner_xml_name=owner_xml_name,
                locator="summary:CDXML Name / CDX Constant",
            )
        )
    table_entries, saw_inventory = _table_entries(document, owner_xml_name)
    entries.extend(table_entries)
    scope = "inventory" if saw_inventory else "object_page" if entries else "unknown"
    if not entries:
        raise ImporterError(
            "SDK_HTML_TABLES",
            "no recognized SDK summary or Value/Name/CDXML Name table was found",
            path_text,
        )
    return CandidateDocument(
        source=source,
        scope=scope,
        normalizations=normalizations,
        sdk_entries=tuple(entries),
    )
