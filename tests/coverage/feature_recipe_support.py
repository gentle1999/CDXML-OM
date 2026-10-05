"""Independent DTD/SDK recipe families for full-schema feature tests.

This module builds one explicit read/write recipe per pinned-DTD attribute.
Expected values come from the pinned DTD, SDK evidence, and listed XML-specific
compatibility overrides; they are not decoded through the mapper under test.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import cast

from tools.schema_importer.candidate import DTDAttributeCandidate
from tools.schema_importer.dtd_importer import import_dtd

from cdxml_om import (
    AminoAcidTermini,
    ArrowheadSide,
    ArrowheadType,
    ArrowType,
    BioShapeType,
    BondStereochemistry,
    BracketType,
    BracketUsage,
    CaptionJustification,
    Connectivity,
    ConstraintType,
    DoublePosition,
    DrawingSpace,
    ExternalConnectionType,
    FillType,
    GeometricFeature,
    GraphicType,
    IsotopicAbundance,
    Justification,
    LabelJustification,
    LineType,
    NodeGeometry,
    NodeStereochemistry,
    NodeType,
    NoGo,
    OrbitalType,
    PageDefinition,
    PolymerFlipType,
    PolymerRepeatPattern,
    PositioningType,
    Radical,
    RingBondCount,
    RxnParticipation,
    RxnStereo,
    SequenceType,
    Side,
    SpectrumClass,
    SpectrumXType,
    SpectrumYType,
    SymbolType,
    TagType,
    Topology,
    Translation,
    UnsaturatedBonds,
)
from cdxml_om._generated.schema_metadata import OBJECT_METADATA

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
DTD_PATH = PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"
SDK_EVIDENCE_PATH = PROJECT_ROOT / "schema" / "sources" / "sdk" / "evidence.json"
CASE_PATH = HERE / "feature_cases.json"
DTD_SHA256 = "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2"
ASSERTIONS = [
    "exact_wrapper_type",
    "source_lexical_value",
    "typed_read_value_and_python_type",
    "typed_mutation",
    "mutation_lexical_value",
    "serialization_reload_readback",
    "unknown_content_and_order_preserved",
]

# These type distinctions are stated by the cited SDK XML evidence, not inferred
# from a binary datatype alone. See the corresponding focused-properties rows.
XML_TYPE_OVERRIDES_BY_OWNER_ATTRIBUTE: dict[tuple[str, str], str] = {
    ("font", "charset"): "str",
    ("color", "r"): "float",
    ("color", "g"): "float",
    ("color", "b"): "float",
    ("s", "size"): "float",
    # Text-run alpha is a numeric CDXML formatting scalar, despite the DTD's
    # generic CDATA declaration for this application-level field.
    ("s", "alpha"): "float",
}
XML_TYPE_OVERRIDES_BY_ATTRIBUTE: dict[str, str] = {
    "LabelSize": "float",
    "CaptionSize": "float",
    "RotationAngle": "float",
    "HeadSize": "float",
    "Center3D": "Point3D",
    "MajorAxisEnd3D": "Point3D",
    "MinorAxisEnd3D": "Point3D",
    "Head3D": "Point3D",
    "Tail3D": "Point3D",
}

# DTD string-valued enumerations are assigned to independent public enum names.
# Boolean enumerations are recognized from their pinned lexical token pair.
ENUM_CLASS_BY_ATTRIBUTE: dict[str, type[object]] = {
    "AS": NodeStereochemistry,
    "AminoAcidTermini": AminoAcidTermini,
    "ArrowType": ArrowType,
    "ArrowheadHead": ArrowheadSide,
    "ArrowheadTail": ArrowheadSide,
    "ArrowheadType": ArrowheadType,
    "BS": BondStereochemistry,
    "BioShapeType": BioShapeType,
    "BracketType": BracketType,
    "BracketUsage": BracketUsage,
    "CaptionJustification": CaptionJustification,
    "Class": SpectrumClass,
    "Connectivity": Connectivity,
    "ConstraintType": ConstraintType,
    "DoublePosition": DoublePosition,
    "DrawingSpace": DrawingSpace,
    "ExternalConnectionType": ExternalConnectionType,
    "FillType": FillType,
    "GeometricFeature": GeometricFeature,
    "Geometry": NodeGeometry,
    "GraphicType": GraphicType,
    "IsotopicAbundance": IsotopicAbundance,
    "Justification": Justification,
    "LabelAlignment": LabelJustification,
    "LabelDisplay": LabelJustification,
    "LabelJustification": LabelJustification,
    "LineType": LineType,
    "NoGo": NoGo,
    "NodeType": NodeType,
    "OrbitalType": OrbitalType,
    "PageDefinition": PageDefinition,
    "PolymerFlipType": PolymerFlipType,
    "PolymerRepeatPattern": PolymerRepeatPattern,
    "PositioningType": PositioningType,
    "Radical": Radical,
    "RingBondCount": RingBondCount,
    "RxnParticipation": RxnParticipation,
    "RxnStereo": RxnStereo,
    "SequenceType": SequenceType,
    "Side": Side,
    "SymbolType": SymbolType,
    "TagType": TagType,
    "Topology": Topology,
    "Translation": Translation,
    "UnsaturatedBonds": UnsaturatedBonds,
    "XType": SpectrumXType,
    "YType": SpectrumYType,
}

BOND_DISPLAY_MEMBER_BY_XML_VALUE = {
    "Solid": "SOLID",
    "Dash": "DASH",
    "Hash": "HASH",
    "WedgedHashBegin": "WEDGED_HASH_BEGIN",
    "WedgedHashEnd": "WEDGED_HASH_END",
    "Bold": "BOLD",
    "WedgeBegin": "WEDGE_BEGIN",
    "WedgeEnd": "WEDGE_END",
    "Wavy": "WAVY",
    "HollowWedgeBegin": "HOLLOW_WEDGE_BEGIN",
    "HollowWedgeEnd": "HOLLOW_WEDGE_END",
    "WavyWedgeBegin": "WAVY_WEDGE_BEGIN",
    "WavyWedgeEnd": "WAVY_WEDGE_END",
    "Dot": "DOT",
    "DashDot": "DASH_DOT",
}

REFERENCE_ARRAY_PAIRS = {
    ("page", "SplitterPositions"),
    ("fragment", "ConnectionOrder"),
    ("n", "BondOrdering"),
    ("n", "Attachments"),
    ("b", "CrossingBonds"),
    ("b", "BondCircularOrdering"),
    ("step", "ReactionStepReactants"),
    ("step", "ReactionStepProducts"),
    ("step", "ReactionStepPlusses"),
    ("step", "ReactionStepObjectsBelowArrow"),
    ("step", "ReactionStepObjectsAboveArrow"),
    ("step", "ReactionStepAtomMapManual"),
    ("step", "ReactionStepAtomMapAuto"),
    ("step", "ReactionStepAtomMap"),
    ("step", "ReactionStepArrows"),
    ("geometry", "BasisObjects"),
    ("constraint", "BasisObjects"),
    ("bracketedgroup", "BracketedObjectIDs"),
    ("chemicalproperty", "BasisObjects"),
    ("coloredmoleculararea", "BasisObjects"),
}

REFERENCE_MODEL_BY_PAIR: dict[tuple[str, str], str] = {
    ("b", "B"): "Node",
    ("b", "E"): "Node",
    ("crossingbond", "BondID"): "Bond",
    ("crossingbond", "InnerAtomID"): "Node",
    ("n", "Attachments"): "Node",
    ("represent", "object"): "Node",
    ("bracketattachment", "GraphicID"): "Graphic",
    ("step", "ReactionStepReactants"): "Fragment",
    ("step", "ReactionStepProducts"): "Fragment",
    ("step", "ReactionStepArrows"): "Arrow",
}

SDK_FAMILY_BY_TYPE = {
    "CDXBoolean": "bool",
    "CDXBooleanImplied": "bool",
    "CDXCoordinate": "float",
    "CDXCurvePoints": "Point2DList",
    "CDXCurvePoints3D": "Point3DList",
    "CDXDate": "str",
    "CDXElementList": "ElementList",
    "CDXFormula": "str",
    "CDXGenericList": "GenericList",
    "CDXObjectID": "reference",
    "CDXObjectIDArray": "references",
    "CDXObjectIDArrayWithCounts": "references",
    "CDXPoint2D": "Point2D",
    "CDXPoint3D": "Point3D",
    "CDXRectangle": "BoundingBox",
    "CDXString": "str",
    "FLOAT64": "float",
    "INT16ListWithCounts": "int_list",
    "Unformatted": "str",
    "UINT8": "int",
    "INT8": "int",
    "UINT16": "int",
    "INT16": "int",
    "UINT32": "int",
    "INT32": "int",
}

EXPLICIT_REFERENCE_PAIRS = {
    ("t", "SupersededBy"),
    ("n", "SupersededBy"),
    ("n", "AltGroupID"),
    ("b", "SupersededBy"),
    ("graphic", "SupersededBy"),
    ("arrow", "SupersededBy"),
    ("curve", "SupersededBy"),
    ("altgroup", "SupersededBy"),
    ("geometry", "SupersededBy"),
    ("constraint", "SupersededBy"),
    ("spectrum", "SupersededBy"),
    ("embeddedobject", "SupersededBy"),
    ("represent", "object"),
    ("table", "SupersededBy"),
    ("tlcplate", "SupersededBy"),
    ("gepplate", "SupersededBy"),
    ("stoichiometrygrid", "SupersededBy"),
    ("plasmidmap", "SupersededBy"),
    ("bracketattachment", "GraphicID"),
    ("crossingbond", "BondID"),
    ("crossingbond", "InnerAtomID"),
    ("chemicalproperty", "ChemicalPropertyDisplayID"),
    ("bioshape", "SupersededBy"),
    ("bracketedgroup", "BracketedObjectIDs"),
    ("coloredmoleculararea", "BasisObjects"),
}


def _sdk_types_by_name(evidence: dict[str, object]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in cast(list[dict[str, object]], evidence["owner_attribute_pairs"]):
        for match in cast(list[dict[str, object]], row["sdk_matches"]):
            sdk_type = match.get("sdk_type")
            if isinstance(sdk_type, str) and sdk_type != "varies":
                result[cast(str, row["xml_name"])].add(sdk_type)
    for row in cast(list[dict[str, object]], evidence["sdk_only_properties"]):
        for fact in cast(list[dict[str, object]], row["sdk_facts"]):
            sdk_type = fact.get("sdk_type")
            if isinstance(sdk_type, str) and sdk_type != "varies":
                result[cast(str, row["xml_name"])].add(sdk_type)
    return result


def _source_family(
    owner: str,
    attribute: DTDAttributeCandidate,
    source_row: dict[str, object],
    sdk_types_by_name: dict[str, set[str]],
) -> tuple[str, dict[str, object]]:
    pair = (owner, attribute.name)
    override = XML_TYPE_OVERRIDES_BY_OWNER_ATTRIBUTE.get(pair)
    if override is None:
        override = XML_TYPE_OVERRIDES_BY_ATTRIBUTE.get(attribute.name)
    if override is not None:
        return override, {
            "kind": "reviewed_xml_type_override",
            "rule": f"{owner}@{attribute.name}",
            "family": override,
        }

    if attribute.enum_values:
        if set(attribute.enum_values) == {"yes", "no"}:
            return "bool", {"kind": "pinned_dtd_boolean_enumeration"}
        if attribute.name in {"Display", "Display2"} and owner == "b":
            return "enum", {"kind": "pinned_dtd_enum", "enum_class": "BondDisplay"}
        enum_class = ENUM_CLASS_BY_ATTRIBUTE.get(attribute.name)
        if enum_class is None:
            raise ValueError(f"no independent enum type contract for {owner}@{attribute.name}")
        return "enum", {"kind": "pinned_dtd_enum", "enum_class": enum_class.__name__}

    if (owner, attribute.name) == ("b", "Order"):
        return "bond_order", {"kind": "focused_sdk_xml_value_contract", "family": "BondOrder"}
    if (owner, attribute.name) in {
        ("objecttag", "Value"),
        ("marker", "Value"),
        ("plasmidmarker", "Value"),
    }:
        return "object_tag_value", {
            "kind": "sdk_contextual_value_contract",
            "sdk_type": "varies",
            "tag_type": "Long",
        }
    if pair in EXPLICIT_REFERENCE_PAIRS or pair in REFERENCE_ARRAY_PAIRS:
        return ("references" if pair in REFERENCE_ARRAY_PAIRS else "reference"), {
            "kind": "sdk_object_id_reference_contract",
            "model": REFERENCE_MODEL_BY_PAIR.get(pair, "Node"),
        }

    sdk_matches = cast(list[dict[str, object]], source_row["sdk_matches"])
    sdk_type: str | None = None
    source_fact: dict[str, object] | None = None
    if sdk_matches:
        sdk_type = cast(str | None, sdk_matches[0].get("sdk_type"))
        source_fact = cast(dict[str, object], sdk_matches[0]["source"])
    elif len(sdk_types_by_name.get(attribute.name, set())) == 1:
        sdk_type = next(iter(sdk_types_by_name[attribute.name]))

    family = SDK_FAMILY_BY_TYPE.get(sdk_type or "")
    if family is not None:
        profile: dict[str, object] = {"kind": "sdk_type_family", "sdk_type": sdk_type}
        if source_fact is not None:
            profile["source"] = source_fact
        else:
            profile["source"] = {"locator": f"SDK XML-name family {attribute.name}"}
        return family, profile

    if sdk_type == "varies":
        return "object_tag_value", {
            "kind": "sdk_contextual_value_contract",
            "sdk_type": "varies",
            "tag_type": "Long",
        }

    return "str", {
        "kind": "pinned_dtd_cdata_lexical",
        "dtd_type": attribute.declared_type,
    }


def _enum_spec(attribute_name: str, lexical: str) -> dict[str, object]:
    if attribute_name in {"Display", "Display2"}:
        return {
            "type": "enum",
            "class": "BondDisplay",
            "member": BOND_DISPLAY_MEMBER_BY_XML_VALUE[lexical],
        }
    enum_class = ENUM_CLASS_BY_ATTRIBUTE[attribute_name]
    member = enum_class(lexical)
    return {"type": "enum", "class": enum_class.__name__, "member": member.name}


def _reference_spec(model: str, object_id: int) -> dict[str, object]:
    return {"type": "reference", "model": model, "id": object_id}


def _scalar_spec(family: str, value: object) -> dict[str, object]:
    if family in {"bool", "float", "int", "str"}:
        return {"type": family, "value": value}
    raise ValueError(f"not a scalar family: {family}")


def _recipe_values(
    family: str,
    owner: str,
    attribute: DTDAttributeCandidate,
    pair_number: int,
) -> tuple[str, dict[str, object], str, dict[str, object], dict[str, object]]:
    if family == "bool":
        lexical = attribute.enum_values or ("yes", "no")
        source_token = "yes" if "yes" in lexical else lexical[0]
        mutation_token = "no" if source_token == "yes" else lexical[-1]
        return (
            source_token,
            _scalar_spec("bool", source_token in {"yes", "true", "1"}),
            mutation_token,
            _scalar_spec("bool", mutation_token in {"yes", "true", "1"}),
            {},
        )
    if family == "enum":
        values = attribute.enum_values
        if not values:
            raise ValueError(f"expected enum source values for {owner}@{attribute.name}")
        source_token = values[0]
        mutation_token = values[1] if len(values) > 1 else values[0]
        return (
            source_token,
            _enum_spec(attribute.name, source_token),
            mutation_token,
            _enum_spec(attribute.name, mutation_token),
            {},
        )
    if family == "bond_order":
        return (
            "3",
            {"type": "enum", "class": "BondOrder", "member": "TRIPLE"},
            "2",
            {"type": "enum", "class": "BondOrder", "member": "DOUBLE"},
            {},
        )
    if family == "object_tag_value":
        return (
            "17",
            _scalar_spec("int", 17),
            "23",
            _scalar_spec("int", 23),
            {"TagType": "Long"},
        )
    if family == "int":
        if attribute.name == "id":
            source_value = 10_000 + pair_number * 2
            mutation_value = source_value + 1
        else:
            source_value, mutation_value = 17, 23
        return (
            str(source_value),
            _scalar_spec("int", source_value),
            str(mutation_value),
            _scalar_spec("int", mutation_value),
            {},
        )
    if family == "float":
        if owner == "s" and attribute.name == "alpha":
            return (
                "0.25",
                _scalar_spec("float", 0.25),
                "0.5",
                _scalar_spec("float", 0.5),
                {},
            )
        if owner == "color" and attribute.name in {"r", "g", "b"}:
            return (
                "0.25",
                _scalar_spec("float", 0.25),
                "0.5",
                _scalar_spec("float", 0.5),
                {},
            )
        return (
            "1.25",
            _scalar_spec("float", 1.25),
            "2.5",
            _scalar_spec("float", 2.5),
            {},
        )
    if family == "str":
        if owner == "font" and attribute.name == "charset":
            return (
                "iso-8859-1",
                _scalar_spec("str", "iso-8859-1"),
                "UTF-8",
                _scalar_spec("str", "UTF-8"),
                {},
            )
        source_value = f"source{pair_number}"
        mutation_value = f"changed{pair_number}"
        return (
            source_value,
            _scalar_spec("str", source_value),
            mutation_value,
            _scalar_spec("str", mutation_value),
            {},
        )
    if family == "Point2D":
        return (
            "1.25 -2.5",
            {"type": "Point2D", "coordinates": [1.25, -2.5]},
            "3.5 4.75",
            {"type": "Point2D", "coordinates": [3.5, 4.75]},
            {},
        )
    if family == "Point3D":
        return (
            "1.25 -2.5 3.75",
            {"type": "Point3D", "coordinates": [1.25, -2.5, 3.75]},
            "4.5 5.5 6.5",
            {"type": "Point3D", "coordinates": [4.5, 5.5, 6.5]},
            {},
        )
    if family == "BoundingBox":
        return (
            "0 1 10 11",
            {"type": "BoundingBox", "coordinates": [0.0, 1.0, 10.0, 11.0]},
            "2.0 3.0 12.0 13.0",
            {"type": "BoundingBox", "coordinates": [2.0, 3.0, 12.0, 13.0]},
            {},
        )
    if family == "Point2DList":
        return (
            "1 2 3 4",
            {"type": "Point2DList", "coordinates": [1, 2, 3, 4]},
            "5.0 6.0 7.0 8.0",
            {"type": "Point2DList", "coordinates": [5, 6, 7, 8]},
            {},
        )
    if family == "Point3DList":
        return (
            "1 2 3 4 5 6",
            {"type": "Point3DList", "coordinates": [1, 2, 3, 4, 5, 6]},
            "7.0 8.0 9.0 10.0 11.0 12.0",
            {"type": "Point3DList", "coordinates": [7, 8, 9, 10, 11, 12]},
            {},
        )
    if family == "int_list":
        return (
            "2 3 5",
            {"type": "int_list", "values": [2, 3, 5]},
            "7 11",
            {"type": "int_list", "values": [7, 11]},
            {},
        )
    if family == "ElementList":
        return (
            "6 8",
            {"type": "ElementList", "elements": [6, 8], "negated": False},
            "NOT 7 9",
            {"type": "ElementList", "elements": [7, 9], "negated": True},
            {},
        )
    if family == "GenericList":
        return (
            "C N",
            {"type": "GenericList", "values": ["C", "N"], "negated": False},
            "NOT O S",
            {"type": "GenericList", "values": ["O", "S"], "negated": True},
            {},
        )
    if family in {"reference", "references"}:
        model = REFERENCE_MODEL_BY_PAIR.get((owner, attribute.name), "Node")
        first_id = 60_001 + pair_number * 2
        second_id = first_id + 1
        if family == "reference":
            return (
                str(first_id),
                _reference_spec(model, first_id),
                str(second_id),
                _reference_spec(model, second_id),
                {
                    "reference_targets": [
                        {"model": model, "id": first_id},
                        {"model": model, "id": second_id},
                    ]
                },
            )
        return (
            f"{first_id} {second_id}",
            {
                "type": "references",
                "items": [_reference_spec(model, first_id), _reference_spec(model, second_id)],
            },
            f"{second_id} {first_id}",
            {
                "type": "references",
                "items": [_reference_spec(model, second_id), _reference_spec(model, first_id)],
            },
            {
                "reference_targets": [
                    {"model": model, "id": first_id},
                    {"model": model, "id": second_id},
                ]
            },
        )
    raise ValueError(f"unsupported source family {family!r} for {owner}@{attribute.name}")


def build_case_rows() -> list[dict[str, object]]:
    dtd = import_dtd(str(DTD_PATH))
    if dtd.source.sha256 != DTD_SHA256:
        raise ValueError("pinned DTD hash changed; source contracts require review")
    evidence = json.loads(SDK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    source_rows = cast(list[dict[str, object]], evidence["owner_attribute_pairs"])
    source_by_pair = {
        (cast(str, row["owner_xml_name"]), cast(str, row["xml_name"])): row for row in source_rows
    }
    if len(source_by_pair) != 762:
        raise ValueError("expected the pinned DTD's exact 762 owner/attribute source inventory")

    sdk_types_by_name = _sdk_types_by_name(evidence)
    # Element-case model names are a separate reviewed source contract. Do not
    # generate an expected class name from the registry being tested.
    catalog = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    model_by_tag = {
        cast(str, row["xml_name"]): cast(str, row["expected_model"])
        for row in cast(list[dict[str, object]], catalog["element_cases"])
    }
    result: list[dict[str, object]] = []
    pair_number = 0
    for element in dtd.dtd_elements:
        expected_model = model_by_tag[element.xml_name]
        model = next(
            metadata
            for metadata in OBJECT_METADATA.values()
            if metadata.xml_tag == element.xml_name
        )
        props = {
            prop.xml_name: prop for prop in model.properties.values() if prop.storage == "attribute"
        }
        for attribute in element.attributes:
            pair = (element.xml_name, attribute.name)
            source_row = source_by_pair[pair]
            prop = props[attribute.name]
            family, source_profile = _source_family(
                element.xml_name, attribute, source_row, sdk_types_by_name
            )
            source_xml, expected, mutation_xml, mutation, context = _recipe_values(
                family, element.xml_name, attribute, pair_number
            )
            row: dict[str, object] = {
                "case_id": f"feature:{element.xml_name}@{attribute.name}",
                "pytest_nodeid": (
                    "tests/coverage/test_full_schema_feature_evidence.py::"
                    "test_mapped_pair_parse_read_mutate_serialize_reload"
                    f"[feature:{element.xml_name}@{attribute.name}]"
                ),
                "owner_tag": element.xml_name,
                "expected_model": expected_model,
                "marker": f"feature:{element.xml_name}@{attribute.name}",
                "xml_attribute": attribute.name,
                "field_name": prop.name,
                "source_xml": source_xml,
                "expected": expected,
                "mutation_xml": mutation_xml,
                "mutation": mutation,
                "source_profile": source_profile,
                "assertions": ASSERTIONS,
            }
            if context:
                row["source_context"] = {
                    key: value for key, value in context.items() if key != "reference_targets"
                }
                if "reference_targets" in context:
                    row["reference_targets"] = context["reference_targets"]
            result.append(row)
            pair_number += 1
    if pair_number != 762:
        raise ValueError(f"expected 762 DTD pairs, generated {pair_number}")
    return result


def update_catalog() -> None:
    catalog = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    catalog["cases"] = build_case_rows()
    for row in cast(list[dict[str, object]], catalog["element_cases"]):
        xml_name = cast(str, row["xml_name"])
        case_id = f"feature-element:{xml_name}"
        row["case_id"] = case_id
        if xml_name == "CDXML":
            row["pytest_nodeid"] = (
                "tests/coverage/test_full_schema_feature_evidence.py::"
                f"test_root_creation_mutation_round_trip[{case_id}]"
            )
            row["assertions"] = [
                "exact_wrapper_type",
                "root_creation",
                "root_mutation",
                "element_round_trip",
            ]
            row["gap_reason"] = None
        else:
            row["pytest_nodeid"] = (
                "tests/coverage/test_full_schema_feature_evidence.py::"
                f"test_element_create_remove_round_trip[{case_id}]"
            )
            row["assertions"] = [
                "exact_wrapper_type",
                "element_creation",
                "element_removal",
                "element_round_trip",
            ]
            row["gap_reason"] = None
    catalog["character_data_cases"] = [
        {
            "case_id": "feature-character:s",
            "xml_name": "s",
            "pytest_nodeid": (
                "tests/coverage/test_full_schema_feature_evidence.py::"
                "test_character_data_parse_read_mutate_serialize_reload[feature-character:s]"
            ),
            "source_xml": "seed",
            "expected": "seed",
            "mutation": "new <glyph> & ligature",
            "mutation_xml": "new <glyph> & ligature",
            "assertions": [
                "storage_lexical_value",
                "typed_read_value_and_python_type",
                "typed_mutation",
                "mutation_lexical_value",
                "serialization_reload_readback",
            ],
            "gap_reason": None,
        },
        {
            "case_id": "feature-character:spectrum",
            "xml_name": "spectrum",
            "pytest_nodeid": (
                "tests/coverage/test_full_schema_feature_evidence.py::"
                "test_character_data_parse_read_mutate_serialize_reload"
                "[feature-character:spectrum]"
            ),
            "source_xml": "100 200 ",
            "expected": "100 200 300 400 500 600",
            "mutation": "110 220",
            "mutation_xml": "110 220",
            "mutation_readback": "110 220",
            "assertions": [
                "storage_lexical_value",
                "typed_read_value_and_python_type",
                "typed_mutation",
                "mutation_lexical_value",
                "serialization_reload_readback",
            ],
            "gap_reason": None,
        },
    ]
    CASE_PATH.write_text(f"{json.dumps(catalog, indent=2, ensure_ascii=False)}\n", encoding="utf-8")


if __name__ == "__main__":
    update_catalog()
