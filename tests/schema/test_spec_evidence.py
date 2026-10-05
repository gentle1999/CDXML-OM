"""Hash-pinned CDXML DTD/SDK evidence catalog checks (offline)."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import cast

from tools.schema_importer.common import PROJECT_ROOT
from tools.schema_importer.dtd_importer import import_dtd

SDK_EVIDENCE = PROJECT_ROOT / "schema" / "sources" / "sdk" / "evidence.json"
FOCUSED_EVIDENCE = PROJECT_ROOT / "schema" / "sources" / "sdk" / "focused-properties.json"
DTD_PATH = PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"


def _object(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def _array(value: object) -> list[object]:
    assert isinstance(value, list)
    return cast(list[object], value)


def _catalog(path: Path) -> dict[str, object]:
    payload: object = json.loads(path.read_text(encoding="utf-8"))
    return _object(payload)


def _source_map(catalog: dict[str, object]) -> dict[str, dict[str, object]]:
    sources = _array(catalog["sources"])
    return {str(_object(item)["id"]): _object(item) for item in sources}


def _assert_source_refs_resolve(value: object, source_ids: set[str]) -> None:
    if isinstance(value, dict):
        mapping = cast(dict[str, object], value)
        if "source_id" in mapping:
            assert mapping["source_id"] in source_ids
            assert isinstance(mapping.get("locator"), str)
        for child in mapping.values():
            _assert_source_refs_resolve(child, source_ids)
    elif isinstance(value, list):
        for child in cast(list[object], value):
            _assert_source_refs_resolve(child, source_ids)


def test_dtd_catalog_reconciles_every_declared_attribute_and_parent_path() -> None:
    catalog = _catalog(SDK_EVIDENCE)
    baseline = _object(catalog["baseline"])
    candidate = import_dtd(str(DTD_PATH))
    assert baseline["dtd_sha256"] == hashlib.sha256(DTD_PATH.read_bytes()).hexdigest()
    assert baseline["dtd_element_count"] == 53
    assert baseline["nonroot_element_count"] == 52
    assert baseline["owner_attribute_pair_count"] == 762
    assert len(candidate.dtd_elements) == 53

    expected_elements = {element.xml_name: element for element in candidate.dtd_elements}
    parent_names: dict[str, list[str]] = {name: [] for name in expected_elements}
    for parent in candidate.dtd_elements:
        for child in parent.children:
            if child in parent_names:
                parent_names[child].append(parent.xml_name)

    elements = [_object(item) for item in _array(catalog["elements"])]
    assert {str(item["xml_name"]) for item in elements} == set(expected_elements)
    for item in elements:
        name = str(item["xml_name"])
        declaration = expected_elements[name]
        assert item["dtd_children"] == list(declaration.children)
        assert item["dtd_parent_xml_names"] == parent_names[name]
        assert item["attributes"] == len(declaration.attributes)

    pair_rows = [_object(item) for item in _array(catalog["owner_attribute_pairs"])]
    actual_pairs = {
        (element.xml_name, attribute.name): attribute
        for element in candidate.dtd_elements
        for attribute in element.attributes
    }
    assert len(pair_rows) == 762
    assert len({(row["owner_xml_name"], row["xml_name"]) for row in pair_rows}) == 762
    for row in pair_rows:
        key = (str(row["owner_xml_name"]), str(row["xml_name"]))
        attribute = actual_pairs[key]
        assert row["dtd_type"] == attribute.declared_type
        assert row["required"] == attribute.required
        assert row["default_kind"] == attribute.default_kind
        assert row["default_value"] == attribute.default_value
        assert row["enum_values"] == list(attribute.enum_values)
        assert _object(row["dtd_source"])["source_id"] == "revvity_dtd"


def test_sdk_inventory_namespaces_extensions_and_conflicts_are_explicit() -> None:
    catalog = _catalog(SDK_EVIDENCE)
    baseline = _object(catalog["baseline"])
    assert baseline["sdk_inventory_count"] == 38
    assert baseline["sdk_inventory_namespace_counts"] == {
        "object": 32,
        "property": 3,
        "xml-only": 3,
    }
    assert baseline["matched_sdk_owner_attribute_pair_count"] == 410
    assert catalog["sdk_only_inventory_elements"] == []
    assert set(_array(catalog["dtd_elements_without_sdk_inventory"])) == {
        "annotation",
        "bioshape",
        "coloredmoleculararea",
        "gepband",
        "geplane",
        "gepplate",
        "marker",
        "plasmidmap",
        "plasmidmarker",
        "plasmidregion",
        "rlogic",
        "rlogicitem",
        "sgcomponent",
        "sgdatum",
        "stoichiometrygrid",
    }
    assert catalog["sdk_only_property_classification_counts"] == {
        "binary_property_not_used_as_xml_attribute": 6,
        "case_variant_of_dtd_xml_attribute": 3,
        "property_encoded_xml_child_element": 2,
        "sdk_documented_xml_attribute_not_in_pinned_dtd": 20,
    }

    extras = [_object(item) for item in _array(catalog["sdk_only_properties"])]
    actual_xml_attrs = [
        item
        for item in extras
        if item["classification"] == "sdk_documented_xml_attribute_not_in_pinned_dtd"
    ]
    assert len(actual_xml_attrs) == 20
    assert {item["xml_name"] for item in actual_xml_attrs} >= {
        "bgcolor",
        "BondLength",
        "LabelFont",
        "LabelSize",
        "LabelFace",
        "LabelColor",
        "PointIsDirected",
    }
    aliases = [
        item for item in extras if item["classification"] == "case_variant_of_dtd_xml_attribute"
    ]
    assert {(item["owner_xml_name"], item["xml_name"]) for item in aliases} == {
        ("curve", "ArrowHeadType"),
        ("curve", "ArrowHeadHead"),
        ("curve", "ArrowHeadTail"),
    }

    pairs = [_object(item) for item in _array(catalog["owner_attribute_pairs"])]
    assert not any(item["owner_xml_name"] == "CDXML" and item["xml_name"] == "id" for item in pairs)
    node_id = next(
        item for item in pairs if item["owner_xml_name"] == "n" and item["xml_name"] == "id"
    )
    assert _object(_array(node_id["sdk_matches"])[0])["sdk_type"] == "UINT16"
    assert _object(catalog["id_semantics"])["generic_object_id"]
    anomalies = [_object(item) for item in _array(catalog["schema_anomalies"])]
    assert {str(item["id"]) for item in anomalies} >= {
        "altgroup_undeclared_bracket_child",
        "curve_closed_spacing_duplicate_cdx_id",
    }
    curve_conflict = next(
        item for item in anomalies if item["id"] == "curve_closed_spacing_duplicate_cdx_id"
    )
    claims = [_object(item) for item in _array(curve_conflict["claims"])]
    assert {
        (item["xml_name"], item["cdx_id"], item["cdx_constant"], item["sdk_type"])
        for item in claims
    } == {
        ("Closed", 2616, "kCDXProp_Closed", "CDXBoolean"),
        ("CurveSpacing", 2616, "kCDXProp_Curve_Spacing", "UINT16"),
    }
    assert curve_conflict["status"] == "unresolved_source_anomaly"
    assert _object(curve_conflict["cross_check"])["independent_source"] is False


def test_sdk_sources_are_hash_pinned_and_all_citations_resolve() -> None:
    for path in (SDK_EVIDENCE, FOCUSED_EVIDENCE):
        catalog = _catalog(path)
        source_map = _source_map(catalog)
        assert source_map
        for _source_id, source in source_map.items():
            digest = source["sha256"]
            assert isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)
            assert isinstance(source["original_url"], str)
            assert isinstance(source["retrieved_at"], str)
            assert "/tmp/" not in str(source)
            assert "cdxml-sdk-" not in str(source)
            if source["snapshot_url"] is not None:
                assert "web.archive.org/web/" in str(source["snapshot_url"])
                assert re.search(r"/web/\d{14}id_/", str(source["snapshot_url"]))
        _assert_source_refs_resolve(catalog, set(source_map))


def test_focused_sdk_contracts_preserve_binary_xml_distinctions() -> None:
    catalog = _catalog(FOCUSED_EVIDENCE)
    facts = [_object(item) for item in _array(catalog["facts"])]
    fact_map = {str(item["id"]): item for item in facts}

    bond = fact_map["bond_order_bit_values"]
    assert bond["binary_type"] == "INT16"
    assert len(_array(bond["source_values"])) == 17
    assert sum(_object(row)["xml_token"] is not None for row in _array(bond["source_values"])) == 16
    bond_rows = {
        str(_object(row)["binary_value"]): _object(row)["xml_token"]
        for row in _array(bond["source_values"])
    }
    assert bond_rows["0xFFFF"] is None
    assert bond_rows["0x0001"] == "1"
    assert bond_rows["0x0040"] == "0.5"
    assert bond_rows["0x1000"] == "dative"
    assert bond_rows["0x8000"] == "threecenter"
    assert _object(bond["pinned_dtd"])["declared_type"] == "cdata"
    assert _object(bond["source_statement"])["absent_property_semantics"] == "single bond"

    font_size = fact_map["font_size_encodings"]
    assert [_object(item)["binary_type"] for item in _array(font_size["properties"])] == [
        "INT16",
        "INT16",
    ]
    assert "does not explicitly state" in str(font_size["scope_note"])
    assert _object(font_size["text_style_run"])["minimum_binary_resolution_points"] == 0.05

    font_charset = fact_map["font_table_charset_encodings"]
    xml_property = _object(font_charset["xml_property"])
    binary_encoding = _object(font_charset["binary_encoding"])
    assert xml_property["owner_xml_name"] == "font"
    assert xml_property["xml_name"] == "charset"
    assert xml_property["dtd_declared_type"] == "cdata"
    assert xml_property["example_value"] == "iso-8859-1"
    assert binary_encoding["component_type"] == "UINT16"
    assert "XML-to-binary code map" in str(font_charset["scope_note"])

    assert _object(fact_map["rotation_angle"])["encoding"] == "degrees multiplied by 65536"
    date = fact_map["cdx_date"]
    assert date["cdxml_lexical_format"] is None
    assert _object(date["binary_encoding"])["timezone"] == "UTC"

    attachments = fact_map["attachments_array_with_counts"]
    assert attachments["binary_type"] == "CDXObjectIDArrayWithCounts"
    assert attachments["reference_target_xml_name"] == "n"
    assert _object(attachments["cdxml_encoding"])["count_prefix"] is False
    line_starts = fact_map["line_starts_counted_list"]
    assert line_starts["binary_type"] == "INT16ListWithCounts"
    assert _object(line_starts["cdxml_encoding"])["count_prefix"] is False

    lists = fact_map["element_generic_and_formula_lists"]
    datatypes = {str(_object(item)["name"]): _object(item) for item in _array(lists["datatypes"])}
    assert datatypes["CDXFormula"]["binary_encoding"] is None
    assert datatypes["CDXFormula"]["chem_draw_reads_or_writes"] is False
    assert datatypes["CDXElementList"]["cdxml_not_prefix"] == "NOT"
    assert datatypes["CDXGenericList"]["cdxml_not_prefix"] == "NOT"

    object_tag = fact_map["object_tag_value_by_tag_type"]
    assert object_tag["binary_type"] == "varies"
    assert object_tag["empty_xml_value_semantics"] is None
    assert [_object(item)["value"] for item in _array(object_tag["tag_type_cases"])] == [0, 1, 2, 3]
    spectrum = fact_map["spectrum_data_is_pcdata"]
    assert spectrum["sdk_property_page_xml_name"] == "temp_SpectrumDataPoint"
    assert spectrum["literal_xml_attribute_or_element_name"] is False
    assert str(spectrum["cdxml_representation"]).endswith("#PCDATA")


def test_geometry_facts_pin_point3d_lexical_example_and_keep_name_conflict_open() -> None:
    catalog = _catalog(FOCUSED_EVIDENCE)
    sources = _source_map(catalog)
    assert sources["sdk_geometry_properties"]["sha256"] == (
        "f9f16b8a0725f0b701bda8d6c21dcc0f4dde9b4500a863b935683fd493fd280c"
    )
    assert sources["sdk_coordinates"]["sha256"] == (
        "49a8550c46232135a6206b8fa7fd1222a20e3288933c96ffffdcb1ab7b84ee44"
    )
    facts = {str(_object(item)["id"]): _object(item) for item in _array(catalog["facts"])}
    point = facts["point3d_lexical_contract"]
    assert point["sdk_datatype"] == "CDXPoint3D"
    assert point["cdxml_component_order"] == ["x", "y", "z"]
    assert point["example"] == "72 144 216"
    assert point["decimal_values_allowed"] is True
    assert "calls the XML form CDXPoint2D" in str(point["source_caveat"])

    reconciliation = facts["axis_point3d_property_name_reconciliation"]
    rows = [_object(item) for item in _array(reconciliation["sdk_property_rows"])]
    assert {
        (item["cdx_constant"], item["cdx_id"], item["sdk_xml_name"], item["sdk_type"])
        for item in rows
    } == {
        ("kCDXProp_3DCenter", 525, "Center3D", "CDXPoint3D"),
        ("kCDXProp_3DMajorAxisEnd", 526, "Center3D", "CDXPoint3D"),
        ("kCDXProp_3DMinorAxisEnd", 527, "Center3D", "CDXPoint3D"),
    }
    dtd_attributes = {
        str(_object(item)["xml_name"]): _object(item)
        for item in _array(reconciliation["dtd_attributes"])
    }
    assert dtd_attributes["Center3D"]["owners"] == ["graphic", "arrow", "plasmidregion"]
    assert dtd_attributes["MajorAxisEnd3D"]["owners"] == [
        "graphic",
        "arrow",
        "plasmidregion",
        "bioshape",
    ]
    assert dtd_attributes["MinorAxisEnd3D"]["owners"] == [
        "graphic",
        "arrow",
        "plasmidregion",
        "bioshape",
    ]
    assert reconciliation["resolution"] is None
    assert "Do not infer owner-to-CDX-ID associations" in str(reconciliation["scope_note"])
