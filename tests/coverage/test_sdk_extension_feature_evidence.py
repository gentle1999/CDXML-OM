"""SDK-documented XML attributes outside the pinned DTD inventory."""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import cast

import pytest
from tools.schema_importer.dtd_importer import import_dtd

from cdxml_om import ArrowheadSide, ArrowheadType, CDXMLDocument, Node

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parents[1]
CASES_PATH = TEST_DIR / "sdk_extension_cases.json"
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "full_schema" / "sdk_extensions.cdxml"
SDK_EVIDENCE_PATH = PROJECT_ROOT / "schema" / "sources" / "sdk" / "evidence.json"
DTD_PATH = PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"
SOURCE_CONTRACTS_PATH = TEST_DIR / "source_contracts.json"

SDK_ONLY_XML_PAIRS = {
    ("n", "bgcolor"),
    ("b", "bgcolor"),
    ("graphic", "bgcolor"),
    ("curve", "bgcolor"),
    ("embeddedobject", "bgcolor"),
    ("table", "bgcolor"),
    ("altgroup", "bgcolor"),
    ("spectrum", "bgcolor"),
    ("tlcplate", "bgcolor"),
    ("geometry", "BondLength"),
    ("geometry", "LabelFont"),
    ("geometry", "LabelSize"),
    ("geometry", "LabelFace"),
    ("geometry", "LabelColor"),
    ("geometry", "PointIsDirected"),
    ("constraint", "BondLength"),
    ("constraint", "LabelFont"),
    ("constraint", "LabelSize"),
    ("constraint", "LabelFace"),
    ("constraint", "LabelColor"),
}

SDK_CASE_VARIANT_PAIRS = {
    ("curve", "ArrowHeadType"),
    ("curve", "ArrowHeadHead"),
    ("curve", "ArrowHeadTail"),
}

RAW_ASSERTIONS = [
    "raw_lexical_read",
    "unrelated_edit_preserves_raw",
    "serialization_reload_preserves_raw",
]
TYPED_ASSERTIONS = [
    "typed_read_value_and_python_type",
    "typed_mutation",
    "mutation_lexical_value",
    "serialization_reload_typed_readback",
]
SCALAR_PYTHON_TYPES: dict[str, type[object]] = {
    "bool": bool,
    "float": float,
    "int": int,
}
ENUM_PYTHON_TYPES: dict[str, type[object]] = {
    "ArrowheadSide": ArrowheadSide,
    "ArrowheadType": ArrowheadType,
}
FIELD_NAMES: dict[tuple[str, str], str] = {
    ("n", "bgcolor"): "bgcolor",
    ("b", "bgcolor"): "bgcolor",
    ("graphic", "bgcolor"): "bgcolor",
    ("curve", "bgcolor"): "bgcolor",
    ("curve", "ArrowHeadType"): "arrowhead_type",
    ("curve", "ArrowHeadHead"): "arrowhead_head",
    ("curve", "ArrowHeadTail"): "arrowhead_tail",
    ("embeddedobject", "bgcolor"): "bgcolor",
    ("table", "bgcolor"): "bgcolor",
    ("altgroup", "bgcolor"): "bgcolor",
    ("spectrum", "bgcolor"): "bgcolor",
    ("geometry", "BondLength"): "bond_length",
    ("geometry", "LabelFont"): "label_font",
    ("geometry", "LabelSize"): "label_size",
    ("geometry", "LabelFace"): "label_face",
    ("geometry", "LabelColor"): "label_color",
    ("geometry", "PointIsDirected"): "point_is_directed",
    ("constraint", "BondLength"): "bond_length",
    ("constraint", "LabelFont"): "label_font",
    ("constraint", "LabelSize"): "label_size",
    ("constraint", "LabelFace"): "label_face",
    ("constraint", "LabelColor"): "label_color",
    ("tlcplate", "bgcolor"): "bgcolor",
}
XML_TYPE_OVERRIDES: dict[tuple[str, str], str] = {
    # SDK CDX storage is INT16, but the XML attribute is handled as a point size.
    ("geometry", "LabelSize"): "float",
    ("constraint", "LabelSize"): "float",
}


def _json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def _cases() -> tuple[dict[str, object], ...]:
    catalog = _json(CASES_PATH)
    assert catalog["format"] == "cdxml-om-sdk-extension-feature-cases"
    assert catalog["version"] == 1
    rows = cast(list[object], catalog["cases"])
    return tuple(cast(dict[str, object], row) for row in rows)


CASES = _cases()


def _sdk_extra_rows() -> dict[tuple[str, str], dict[str, object]]:
    evidence = _json(SDK_EVIDENCE_PATH)
    rows = cast(list[dict[str, object]], evidence["sdk_only_properties"])
    return {
        (cast(str, row["owner_xml_name"]), cast(str, row["xml_name"])): row
        for row in rows
        if row["classification"]
        in {
            "sdk_documented_xml_attribute_not_in_pinned_dtd",
            "case_variant_of_dtd_xml_attribute",
        }
    }


def _fixture_target(document: CDXMLDocument, case: dict[str, object]):
    owner_tag = cast(str, case["owner_tag"])
    marker = f"sdk-{owner_tag}"
    matches = [
        element
        for element in document.tree.iter()
        if element.tag == owner_tag and element.get("{urn:vendor}case") == marker
    ]
    assert len(matches) == 1, (owner_tag, marker)
    return matches[0]


def _expected_type_name(
    case: dict[str, object], sdk_rows: dict[tuple[str, str], dict[str, object]]
) -> str:
    pair = (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
    if pair in SDK_CASE_VARIANT_PAIRS:
        return "ArrowheadType" if pair[1] == "ArrowHeadType" else "ArrowheadSide"
    if pair in XML_TYPE_OVERRIDES:
        return XML_TYPE_OVERRIDES[pair]
    sdk_fact_rows = cast(list[dict[str, object]], sdk_rows[pair]["sdk_facts"])
    sdk_type = cast(str, sdk_fact_rows[0]["sdk_type"])
    return {
        "CDXBooleanImplied": "bool",
        "CDXCoordinate": "float",
        "INT16": "int",
    }[sdk_type]


def _typed_value(recipe: dict[str, object], *, field: str) -> object:
    type_name = cast(str, recipe["expected_python_type"])
    value = recipe[field]
    if type_name in ENUM_PYTHON_TYPES:
        enum_type = ENUM_PYTHON_TYPES[type_name]
        assert isinstance(value, str)
        return enum_type(value)  # type: ignore[call-arg]
    scalar_type = SCALAR_PYTHON_TYPES[type_name]
    if scalar_type is float:
        assert isinstance(value, int | float) and not isinstance(value, bool)
        return float(value)
    assert type(value) is scalar_type
    return value


def _source_typed_value(case: dict[str, object], expected_type_name: str) -> object:
    source_xml = cast(str, case["source_xml"])
    if expected_type_name in ENUM_PYTHON_TYPES:
        return ENUM_PYTHON_TYPES[expected_type_name](source_xml)  # type: ignore[call-arg]
    scalar_type = SCALAR_PYTHON_TYPES[expected_type_name]
    if scalar_type is bool:
        assert source_xml in {"yes", "no"}
        return source_xml == "yes"
    if scalar_type is int:
        return int(source_xml)
    if scalar_type is float:
        return float(source_xml)
    raise AssertionError(f"unsupported SDK XML type {expected_type_name!r}")


@pytest.mark.parametrize("case", CASES, ids=lambda case: cast(str, case["case_id"]))
def test_sdk_extension_raw_attributes_survive_an_unrelated_edit(
    case: dict[str, object],
) -> None:
    case_id = cast(str, case["case_id"])
    expected_nodeid = (
        "tests/coverage/test_sdk_extension_feature_evidence.py::"
        "test_sdk_extension_raw_attributes_survive_an_unrelated_edit"
        f"[{case_id}]"
    )
    assert case["pytest_nodeid"] == expected_nodeid
    assert case["assertions"] == RAW_ASSERTIONS

    document = CDXMLDocument.from_file(FIXTURE_PATH)
    target_element = _fixture_target(document, case)
    attribute_name = cast(str, case["xml_attribute"])
    source_xml = cast(str, case["source_xml"])
    assert target_element.get(attribute_name) == source_xml
    target = document.wrap(target_element)
    assert target.raw_attributes[attribute_name] == source_xml

    # Exercise unrelated typed mutation while each exact SDK-only source pair
    # remains available in both raw storage and serialized output.
    node = document.find(Node)[0]
    node.charge = -2
    assert node.raw_attributes["Charge"] == "-2"
    serialized = document.to_string()
    restored = CDXMLDocument.from_string(serialized)
    restored_element = _fixture_target(restored, case)
    assert restored_element.get(attribute_name) == source_xml
    assert restored.wrap(restored_element).raw_attributes[attribute_name] == source_xml
    assert restored.find(Node)[0].charge == -2


def test_sdk_extension_inventory_separates_twenty_new_pairs_and_three_case_aliases() -> None:
    rows = _sdk_extra_rows()
    assert set(rows) == SDK_ONLY_XML_PAIRS | SDK_CASE_VARIANT_PAIRS
    assert len(SDK_ONLY_XML_PAIRS) == 20
    assert len(SDK_CASE_VARIANT_PAIRS) == 3
    assert len(CASES) == 23
    assert {(cast(str, row["owner_tag"]), cast(str, row["xml_attribute"])) for row in CASES} == (
        SDK_ONLY_XML_PAIRS | SDK_CASE_VARIANT_PAIRS
    )

    evidence = _json(SDK_EVIDENCE_PATH)
    dtd = import_dtd(str(DTD_PATH))
    dtd_attributes = {
        (element.xml_name, attribute.name): attribute
        for element in dtd.dtd_elements
        for attribute in element.attributes
    }
    dtd_tags = {element.xml_name for element in dtd.dtd_elements}
    source_ids = {
        cast(str, item["id"]) for item in cast(list[dict[str, object]], evidence["sources"])
    }
    for case in CASES:
        pair = (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
        source_row = rows[pair]
        source_fact_rows = cast(list[dict[str, object]], source_row["sdk_facts"])
        assert len(source_fact_rows) == 1
        source_fact = source_fact_rows[0]
        assert case["sdk_type"] == source_fact["sdk_type"]
        source_ref = cast(dict[str, object], source_fact["source"])
        assert source_ref["source_id"] in source_ids
        assert pair[0] in dtd_tags

        if pair in SDK_ONLY_XML_PAIRS:
            assert pair not in dtd_attributes
            assert source_row["classification"] == (
                "sdk_documented_xml_attribute_not_in_pinned_dtd"
            )
        else:
            assert source_row["classification"] == "case_variant_of_dtd_xml_attribute"
            canonical_name = next(
                name
                for owner, name in dtd_attributes
                if owner == pair[0] and name.casefold() == pair[1].casefold()
            )
            declaration = dtd_attributes[(pair[0], canonical_name)]
            recipe = cast(dict[str, object], case["typed_recipe"])
            assert case["source_xml"] in declaration.enum_values
            assert recipe["mutation_xml"] in declaration.enum_values


def test_each_sdk_extension_pair_has_an_independent_typed_recipe() -> None:
    sdk_rows = _sdk_extra_rows()
    for case in CASES:
        pair = (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
        recipe = cast(dict[str, object], case["typed_recipe"])
        assert case["typed_status"] == "typed", pair
        assert "typed_gap_reason" not in case
        assert recipe["field_name"] == FIELD_NAMES[pair]
        expected_nodeid = (
            "tests/coverage/test_sdk_extension_feature_evidence.py::"
            "test_sdk_extension_typed_mutation_roundtrip"
            f"[{case['case_id']}]"
        )
        assert recipe["pytest_nodeid"] == expected_nodeid
        assert recipe["required_assertions"] == TYPED_ASSERTIONS

        type_name = cast(str, recipe["expected_python_type"])
        assert type_name == _expected_type_name(case, sdk_rows), pair
        expected_value = _typed_value(recipe, field="expected_python_value")
        mutation_value = _typed_value(recipe, field="mutation_python_value")
        assert type(expected_value) is (
            ENUM_PYTHON_TYPES[type_name]
            if type_name in ENUM_PYTHON_TYPES
            else SCALAR_PYTHON_TYPES[type_name]
        ), pair
        assert type(mutation_value) is type(expected_value), pair
        assert expected_value == _source_typed_value(case, type_name), pair
        if isinstance(mutation_value, Enum):
            mutation_xml = mutation_value.value
        elif isinstance(mutation_value, bool):
            mutation_xml = "yes" if mutation_value else "no"
        else:
            mutation_xml = str(mutation_value)
        assert recipe["mutation_xml"] == mutation_xml


@pytest.mark.parametrize("case", CASES, ids=lambda case: cast(str, case["case_id"]))
def test_sdk_extension_typed_mutation_roundtrip(case: dict[str, object]) -> None:
    pair = (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
    recipe = cast(dict[str, object], case["typed_recipe"])
    sdk_rows = _sdk_extra_rows()
    type_name = _expected_type_name(case, sdk_rows)
    assert recipe["expected_python_type"] == type_name
    expected_value = _typed_value(recipe, field="expected_python_value")
    mutation_value = _typed_value(recipe, field="mutation_python_value")

    document = CDXMLDocument.from_file(FIXTURE_PATH)
    target_element = _fixture_target(document, case)
    attribute_name = cast(str, case["xml_attribute"])
    source_xml = cast(str, case["source_xml"])
    assert target_element.get(attribute_name) == source_xml
    target = document.wrap(target_element)
    field_name = cast(str, recipe["field_name"])

    typed_before = getattr(target, field_name)
    expected_type = (
        ENUM_PYTHON_TYPES[type_name]
        if type_name in ENUM_PYTHON_TYPES
        else SCALAR_PYTHON_TYPES[type_name]
    )
    assert type(typed_before) is expected_type, pair
    assert typed_before == expected_value, pair

    original_attributes = tuple(target_element.attrib.items())
    original_children = tuple(target_element)
    page = next(element for element in document.tree.iter() if element.tag == "page")
    original_page_children = tuple(page)
    assert any(child.tag == "{urn:vendor}opaque" for child in page)

    setattr(target, field_name, mutation_value)
    mutation_xml = cast(str, recipe["mutation_xml"])
    assert target_element.get(attribute_name) == mutation_xml, pair
    assert getattr(target, field_name) == mutation_value, pair
    assert type(getattr(target, field_name)) is expected_type, pair

    expected_attributes = tuple(
        (name, mutation_xml if name == attribute_name else value)
        for name, value in original_attributes
    )
    assert tuple(target_element.attrib.items()) == expected_attributes, pair
    assert tuple(target_element) == original_children, pair
    assert tuple(page) == original_page_children, pair

    serialized = document.to_string()
    restored = CDXMLDocument.from_string(serialized)
    restored_element = _fixture_target(restored, case)
    restored_target = restored.wrap(restored_element)
    typed_after_reload = getattr(restored_target, field_name)
    assert restored_element.get(attribute_name) == mutation_xml, pair
    assert type(typed_after_reload) is expected_type, pair
    assert typed_after_reload == mutation_value, pair

    restored_page = next(element for element in restored.tree.iter() if element.tag == "page")
    assert [child.tag for child in restored_page] == [child.tag for child in original_page_children]
    opaque = next(child for child in restored_page if child.tag == "{urn:vendor}opaque")
    assert opaque.get("marker") == "keep"
    assert opaque.text == "opaque payload"


def test_sdk_extension_fixture_uses_source_parent_routes_and_required_dtd_attributes() -> None:
    contracts = _json(SOURCE_CONTRACTS_PATH)
    contract_rows = cast(list[dict[str, object]], contracts["elements"])
    by_tag = {cast(str, row["xml_name"]): row for row in contract_rows}
    dtd = import_dtd(str(DTD_PATH))
    declarations = {element.xml_name: element for element in dtd.dtd_elements}
    document = CDXMLDocument.from_file(FIXTURE_PATH)

    for case in CASES:
        owner_tag = cast(str, case["owner_tag"])
        target = _fixture_target(document, case)
        allowed_parents = set(cast(list[str], by_tag[owner_tag]["parents"]))
        parent = target.getparent()
        assert parent is not None
        assert parent.tag in allowed_parents
        route = [cast(str, item.tag) for item in target.iterancestors()][::-1] + [owner_tag]
        for parent_tag, child_tag in zip(route, route[1:], strict=False):
            assert child_tag in declarations[parent_tag].children
        required = {
            attribute.name for attribute in declarations[owner_tag].attributes if attribute.required
        }
        assert required <= set(target.attrib)


def test_sdk_extension_fixture_covers_every_catalog_attribute_exactly_once() -> None:
    document = CDXMLDocument.from_file(FIXTURE_PATH)
    seen = {
        (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
        for case in CASES
        if _fixture_target(document, case).get(cast(str, case["xml_attribute"]))
        == case["source_xml"]
    }
    assert len(seen) == 23
    assert seen == SDK_ONLY_XML_PAIRS | SDK_CASE_VARIANT_PAIRS
