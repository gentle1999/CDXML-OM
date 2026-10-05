"""Focused evidence, namespace, and offline-parser regression tests."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from tools.schema_compiler.loader import load_schema
from tools.schema_importer import dtd_importer
from tools.schema_importer.candidate import CandidateDocument
from tools.schema_importer.common import PROJECT_ROOT
from tools.schema_importer.diff import compare_candidate
from tools.schema_importer.dtd_importer import import_dtd
from tools.schema_importer.errors import ImporterError
from tools.schema_importer.sdk_importer import import_sdk_html

PINNED_DTD = PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_pinned_dtd_keeps_raw_legacy_enum_evidence_and_round_trips_json() -> None:
    candidate = import_dtd(str(PINNED_DTD))
    restored = CandidateDocument.from_json(candidate.to_json())
    assert restored == candidate
    assert candidate.source.sha256 == hashlib.sha256(PINNED_DTD.read_bytes()).hexdigest()
    assert any("Parser-only DTD enum token escape" in note for note in candidate.normalizations)

    node = next(item for item in candidate.dtd_elements if item.xml_name == "n")
    atom_stereo = next(attribute for attribute in node.attributes if attribute.name == "AS")
    assert atom_stereo.enum_values == (
        "U",
        "N",
        "R",
        "S",
        "r",
        "s",
        "u",
        "M",
        "P",
        "a",
        "+",
        "-",
        "?",
    )


@pytest.mark.parametrize(
    ("name", "contents", "expected_code"),
    [
        (
            "nested-parameter.dtd",
            """<!ENTITY % payload "<!ENTITY &#37; ext SYSTEM 'file:///not-read'>">
%payload;
%ext;
<!ELEMENT root EMPTY>""",
            "DTD_PARAMETER_ENTITY",
        ),
        (
            "unicode-entity.dtd",
            "<!ENTITY naïve SYSTEM 'file:///not-read'>\n<!ELEMENT root EMPTY>",
            "EXTERNAL_DTD_REFERENCE",
        ),
    ],
)
def test_dtd_rejects_parameter_and_unicode_named_external_entities_before_parser(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    contents: str,
    expected_code: str,
) -> None:
    source = _write(tmp_path, name, contents)

    def parser_must_not_be_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("unsafe input reached lxml DTD parsing")

    monkeypatch.setattr(dtd_importer.etree, "DTD", parser_must_not_be_called)
    with pytest.raises(ImporterError) as raised:
        import_dtd(str(source))
    assert raised.value.code == expected_code


def test_utf16_dtd_is_rejected_before_parser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "utf16.dtd"
    source.write_bytes("<!ELEMENT root EMPTY>".encode("utf-16"))

    def parser_must_not_be_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("non-UTF-8 input reached lxml DTD parsing")

    monkeypatch.setattr(dtd_importer.etree, "DTD", parser_must_not_be_called)
    with pytest.raises(ImporterError) as raised:
        import_dtd(str(source))
    assert raised.value.code == "DTD_ENCODING"


def test_diff_surfaces_attribute_default_and_enum_drift(tmp_path: Path) -> None:
    source = _write(
        tmp_path,
        "drift.dtd",
        """<!ELEMENT n EMPTY>
<!ATTLIST n Element CDATA "8">
<!ELEMENT b EMPTY>
<!ATTLIST b Display (Solid|Dash|Novel) "Solid">""",
    )
    candidate = import_dtd(str(source))
    report = compare_candidate(candidate, load_schema(PROJECT_ROOT))
    differences = report["differences"]
    element_default = next(
        item for item in differences if item["target"] == "attribute:n.Element.default"
    )
    assert element_default["canonical"] == "6"
    assert element_default["candidate"] == "8"
    assert "lexical comparison only" in element_default["interpretation"]

    display_enum = next(
        item for item in differences if item["target"] == "attribute:b.Display.enum_values"
    )
    assert display_enum["candidate"] == ["Solid", "Dash", "Novel"]
    assert "no enum normalization" in display_enum["interpretation"]


def test_sdk_inventory_preserves_object_property_and_xml_only_namespaces(
    tmp_path: Path,
) -> None:
    source = _write(
        tmp_path,
        "inventory.html",
        """<!doctype html><html><body><table><tr><td>layout
<table>
<tr><th>Object</th><th>Value</th><th>Name</th><th>CDXML Name</th></tr>
<tr><td>Group</td><td>0x8002</td><td>kCDXObj_Group</td><td>group</td></tr>
<tr><td>Color Table</td><td>0x0300</td><td>kCDXProp_ColorTable</td><td>colortable</td></tr>
<tr><td>Style</td><td>n/a</td><td>n/a</td><td>s</td></tr>
</table></td></tr></table></body></html>""",
    )
    candidate = import_sdk_html(str(source))
    assert candidate.scope == "inventory"
    assert candidate.source.sha256 == hashlib.sha256(source.read_bytes()).hexdigest()
    assert len(candidate.sdk_entries) == 3
    by_xml = {entry.xml_name: entry for entry in candidate.sdk_entries}
    assert by_xml["group"].namespace == "object"
    assert by_xml["group"].cdx_id == 0x8002
    assert by_xml["colortable"].namespace == "property"
    assert by_xml["colortable"].cdx_constant == "kCDXProp_ColorTable"
    assert by_xml["s"].namespace == "xml-only"

    report = compare_candidate(candidate, load_schema(PROJECT_ROOT))
    changed = [item for item in report["differences"] if item["target"] == "namespace:colortable"]
    assert changed
    assert changed[0]["candidate"] == "property"
    assert changed[0]["canonical"] == "xml-only"


def test_sdk_subobject_table_accepts_rows_without_empty_trailing_header_cell(
    tmp_path: Path,
) -> None:
    source = _write(
        tmp_path,
        "subobjects.html",
        """<html><body>
<table><tr><td>CDXML Name:</td><td>altgroup</td></tr>
<tr><td>CDX Constant Name:</td><td>kCDXObj_NamedAlternativeGroup</td></tr>
<tr><td>CDX Constant Value:</td><td>0x800A</td></tr></table>
<table><tr><th>Value</th><th>Name</th><th>CDXML Name</th><th></th></tr>
<tr><td>0x8002</td><td>kCDXObj_Group</td><td>group</td></tr>
<tr><td>0x8003</td><td>kCDXObj_Fragment</td><td>fragment</td></tr>
</table></body></html>""",
    )

    candidate = import_sdk_html(str(source))

    subobjects = [item for item in candidate.sdk_entries if item.relation == "subobject"]
    assert [(item.xml_name, item.cdx_id) for item in subobjects] == [
        ("group", 0x8002),
        ("fragment", 0x8003),
    ]


def test_sdk_node_property_type_evidence_is_not_normalized(tmp_path: Path) -> None:
    source = _write(
        tmp_path,
        "node.html",
        """<html><head><title>Node Object</title></head><body>
<table><tr><td>CDXML Name:</td><td>n</td></tr>
<tr><td>CDX Constant Name:</td><td>kCDXObj_Node</td></tr>
<tr><td>CDX Constant Value:</td><td>0x8004</td></tr></table>
<table><tr><th>Value</th><th>Name</th><th>CDXML Name</th><th>Type</th></tr>
<tr><td>n/a</td><td>n/a</td><td>id</td><td>UINT16</td></tr>
<tr><td>0x0421</td><td>kCDXProp_Atom_Charge</td><td>Charge</td><td>INT16</td></tr>
</table></body></html>""",
    )
    candidate = import_sdk_html(str(source))
    id_entry = next(item for item in candidate.sdk_entries if item.xml_name == "id")
    assert id_entry.type_name == "UINT16"
    assert id_entry.value_text == "n/a"

    report = compare_candidate(candidate, load_schema(PROJECT_ROOT))
    mismatch = next(
        item for item in report["differences"] if item["target"] == "property:n.id.type_evidence"
    )
    assert mismatch["canonical"] == "object_id"
    assert mismatch["candidate"] == "UINT16"
    assert mismatch["interpretation"] == "raw SDK type evidence; no normalization applied"


def test_sdk_external_doctype_is_refused(tmp_path: Path) -> None:
    source = _write(
        tmp_path,
        "external.html",
        "<!DOCTYPE html SYSTEM 'file:///not-read'><html><table>"
        "<tr><th>Value</th><th>Name</th><th>CDXML Name</th></tr>"
        "<tr><td>0x8004</td><td>kCDXObj_Node</td><td>n</td></tr></table></html>",
    )
    with pytest.raises(ImporterError) as raised:
        import_sdk_html(str(source))
    assert raised.value.code == "EXTERNAL_HTML_REFERENCE"


def test_sdk_legacy_malformed_html_recovers_and_records_diagnostics(
    tmp_path: Path,
) -> None:
    source = _write(
        tmp_path,
        "legacy-node.html",
        """<html><body>
<table><tr><td>CDXML Name:</td><td>n</td></tr>
<tr><td>CDX Constant Name:</td><td>kCDXObj_Node</td></tr>
<tr><td>CDX Constant Value:</td><td>0x8004</td></tr></table>
<table><tr><th>Value</th><th>Name</th><th>CDXML Name</th><th>Type</th></tr>
<tr><td>n/a</td><td>n/a</td><td>id</td><td>UINT16</td></tr>
<tr><td>0x0421</td><td>kCDXProp_Atom_Charge</td><td>Charge</td><td>INT16</td></tr>
</table></font></body></html>""",
    )

    candidate = import_sdk_html(str(source))

    assert candidate.scope == "object_page"
    assert any(item.startswith("HTML recovery diagnostic:") for item in candidate.normalizations)
    assert any(
        item.xml_name == "Charge" and item.type_name == "INT16" for item in candidate.sdk_entries
    )
    assert CandidateDocument.from_json(candidate.to_json()) == candidate
