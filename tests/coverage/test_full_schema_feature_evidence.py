"""Independent typed read, mutation, and reload evidence for modeled fields."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import pytest
from lxml import etree
from tests.coverage.feature_recipe_support import (
    BOND_DISPLAY_MEMBER_BY_XML_VALUE,
    ENUM_CLASS_BY_ATTRIBUTE,
)
from tools.schema_compiler.coverage import _element_operations
from tools.schema_compiler.sources import SOURCES
from tools.schema_importer.dtd_importer import import_dtd

from cdxml_om import (
    AminoAcidTermini,
    ArrowheadSide,
    ArrowheadType,
    ArrowType,
    BioShapeType,
    BondDisplay,
    BondOrder,
    BondStereochemistry,
    BoundingBox,
    BracketType,
    BracketUsage,
    CaptionJustification,
    CDXMLDocument,
    CDXMLElement,
    CDXMLRoot,
    Connectivity,
    ConstraintType,
    DoublePosition,
    DrawingSpace,
    ElementList,
    ExternalConnectionType,
    FillType,
    GenericList,
    GeometricFeature,
    GraphicType,
    IsotopicAbundance,
    Justification,
    LabelJustification,
    LineType,
    Node,
    NodeGeometry,
    NodeStereochemistry,
    NodeType,
    NoGo,
    OrbitalType,
    PageDefinition,
    Point2D,
    Point3D,
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
    TextRun,
    Topology,
    Translation,
    UnknownElement,
    UnsaturatedBonds,
)
from cdxml_om._generated.schema_metadata import DATATYPE_METADATA, ENUM_METADATA, OBJECT_METADATA
from cdxml_om._generated.schema_registry import OBJECT_BY_XML_TAG

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "full_schema" / "mapped_fields.cdxml"
CASE_PATH = TEST_DIR / "feature_cases.json"
SOURCE_CONTRACTS_PATH = TEST_DIR / "source_contracts.json"
SDK_EVIDENCE_PATH = PROJECT_ROOT / "schema" / "sources" / "sdk" / "evidence.json"
CASE_FORMAT = "cdxml-om-full-schema-feature-cases"
CASE_FORMAT_VERSION = 1
DTD_SHA256 = "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2"
VENDOR_NS = "urn:vendor"
VENDOR_CASE = f"{{{VENDOR_NS}}}case"
VENDOR_FEATURE = f"{{{VENDOR_NS}}}feature-case"
VENDOR_ROOT = f"{{{VENDOR_NS}}}root"


def _read_case_catalog() -> dict[str, object]:
    catalog = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    assert isinstance(catalog, dict)
    assert catalog.get("format") == CASE_FORMAT
    assert catalog.get("version") == CASE_FORMAT_VERSION
    cases = catalog.get("cases")
    assert isinstance(cases, list)
    return catalog


def _cases() -> tuple[dict[str, object], ...]:
    raw_cases = _read_case_catalog()["cases"]
    assert isinstance(raw_cases, list)
    return tuple(cast(dict[str, object], case) for case in raw_cases)


CASES = _cases()


def _element_cases() -> tuple[dict[str, object], ...]:
    raw_cases = _read_case_catalog().get("element_cases")
    assert isinstance(raw_cases, list)
    return tuple(cast(dict[str, object], case) for case in raw_cases)


ELEMENT_CASES = _element_cases()


def _character_data_cases() -> tuple[dict[str, object], ...]:
    raw_cases = _read_case_catalog().get("character_data_cases")
    assert isinstance(raw_cases, list)
    return tuple(cast(dict[str, object], case) for case in raw_cases)


CHARACTER_DATA_CASES = _character_data_cases()


def _source_contracts() -> dict[str, object]:
    contracts = json.loads(SOURCE_CONTRACTS_PATH.read_text(encoding="utf-8"))
    assert isinstance(contracts, dict)
    assert contracts.get("format") == "cdxml-om-dtd-element-source-contracts"
    assert contracts.get("version") == 1
    return contracts


SOURCE_CONTRACTS = _source_contracts()

EXPECTED_CURRENT_SDK_MAPPING_GAPS: dict[tuple[str, str], tuple[int | None, str | None]] = {}
SDK_SOURCE_ID_CONFLICT_PAIRS = {("curve", "Closed"), ("curve", "CurveSpacing")}
EXPECTED_CURRENT_SDK_NUMERIC_TYPE_GAPS: set[tuple[str, str]] = set()
SDK_BINARY_TYPE_XML_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    ("font", "charset"): {
        "sdk_type": "INT16",
        "xml_python_type": "str",
        "source_uri": "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXFontTable.htm",
        "source_locator": 'CDXML example <font id="3" charset="iso-8859-1" name="Arial"/>',
        "provenance_locator": "CDXFontTable datatype page: CDXML charset values are encoding names",
    }
}
SDK_BINARY_XML_FAMILY_OVERRIDES: dict[str, dict[str, object]] = {
    "LabelSize": {
        "owners": {"b", "CDXML", "n", "spectrum", "table", "t", "tlcplate"},
        "sdk_type": "INT16",
        "xml_python_type": "float",
        "source_uri": "https://web.archive.org/web/20190326232657id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/LabelStyleSize.htm",
        "source_locator": (
            "LabelStyleSize property page: default label font size; binary type does not "
            "specify CDXML scale"
        ),
    },
    "CaptionSize": {
        "owners": {"CDXML", "graphic", "t"},
        "sdk_type": "INT16",
        "xml_python_type": "float",
        "source_uri": "https://web.archive.org/web/20190326232725id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/CaptionStyleSize.htm",
        "source_locator": (
            "CaptionStyleSize property page: default caption font size; binary type does not "
            "specify CDXML scale"
        ),
    },
    "RotationAngle": {
        "owners": {"embeddedobject", "t"},
        "sdk_type": "INT32",
        "xml_python_type": "float",
        "source_uri": "https://web.archive.org/web/20190121160337id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/RotationAngle.htm",
        "source_locator": "RotationAngle property description: angle measured in degrees",
    },
    "HeadSize": {
        "owners": {"curve", "graphic"},
        "sdk_type": "INT16",
        "xml_python_type": "float",
        "source_uri": "https://web.archive.org/web/20100503174322id_/http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/Graphic.htm",
        "source_locator": (
            "Graphic property table: HeadSize uses kCDXProp_Arrowhead_Size (0x0A20), binary INT16"
        ),
    },
}
REMOVAL_GUARD_RAW_VALUE_ASSERTIONS = {
    "color": {"r": "0.25", "g": "0.5", "b": "0.75"},
    "font": {"name": "Feature Font"},
}


def _case_id(case: dict[str, object]) -> str:
    return cast(str, case["case_id"])


def _model_class(name: str) -> type[CDXMLElement]:
    matching_models = [model for model in OBJECT_BY_XML_TAG.values() if model.__name__ == name]
    assert len(matching_models) == 1, f"expected one generated model named {name!r}"
    return matching_models[0]


EXPECTED_MODEL_BY_TAG = {
    cast(str, case["xml_name"]): cast(str, case["expected_model"])
    for case in ELEMENT_CASES
    if isinstance(case["expected_model"], str)
}

EXPECTED_ID_SCOPE_BY_TAG = {
    element.xml_name: (
        "local"
        if element.xml_name == "font"
        else "none"
        if element.xml_name in {"fonttable", "colortable"}
        else "document"
        if any(attribute.name == "id" for attribute in element.attributes)
        else "none"
    )
    for element in import_dtd(
        str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd")
    ).dtd_elements
}


# Independent lexical-to-Python expectations for every DTD enumeration on a
# currently mapped attribute. The DTD token inventory is checked against this
# table, so new values or newly mapped enum attributes require an explicit row.
EXPECTED_MAPPED_DTD_ENUM_VALUES: dict[tuple[str, str], dict[str, object]] = {
    ("b", "Display"): {
        "Solid": BondDisplay.SOLID,
        "Dash": BondDisplay.DASH,
        "Hash": BondDisplay.HASH,
        "WedgedHashBegin": BondDisplay.WEDGED_HASH_BEGIN,
        "WedgedHashEnd": BondDisplay.WEDGED_HASH_END,
        "Bold": BondDisplay.BOLD,
        "WedgeBegin": BondDisplay.WEDGE_BEGIN,
        "WedgeEnd": BondDisplay.WEDGE_END,
        "Wavy": BondDisplay.WAVY,
        "HollowWedgeBegin": BondDisplay.HOLLOW_WEDGE_BEGIN,
        "HollowWedgeEnd": BondDisplay.HOLLOW_WEDGE_END,
        "WavyWedgeBegin": BondDisplay.WAVY_WEDGE_BEGIN,
        "WavyWedgeEnd": BondDisplay.WAVY_WEDGE_END,
        "Dot": BondDisplay.DOT,
        "DashDot": BondDisplay.DASH_DOT,
    },
    ("group", "Integral"): {"yes": True, "no": False},
    ("t", "Visible"): {"yes": True, "no": False},
    ("t", "IgnoreWarnings"): {"yes": True, "no": False},
    ("graphic", "GraphicType"): {
        "Undefined": GraphicType.UNDEFINED,
        "Line": GraphicType.LINE,
        "Arc": GraphicType.ARC,
        "Rectangle": GraphicType.RECTANGLE,
        "Oval": GraphicType.OVAL,
        "Orbital": GraphicType.ORBITAL,
        "Bracket": GraphicType.BRACKET,
        "Symbol": GraphicType.SYMBOL,
    },
    ("graphic", "Visible"): {"yes": True, "no": False},
    ("arrow", "Visible"): {"yes": True, "no": False},
    ("arrow", "ArrowheadType"): {
        "Solid": ArrowheadType.SOLID,
        "Hollow": ArrowheadType.HOLLOW,
        "Angle": ArrowheadType.ANGLE,
    },
    ("arrow", "ArrowheadHead"): {
        "Unspecified": ArrowheadSide.UNSPECIFIED,
        "None": ArrowheadSide.VALUE_NONE,
        "Full": ArrowheadSide.FULL,
        "HalfLeft": ArrowheadSide.HALF_LEFT,
        "HalfRight": ArrowheadSide.HALF_RIGHT,
    },
    ("arrow", "ArrowheadTail"): {
        "Unspecified": ArrowheadSide.UNSPECIFIED,
        "None": ArrowheadSide.VALUE_NONE,
        "Full": ArrowheadSide.FULL,
        "HalfLeft": ArrowheadSide.HALF_LEFT,
        "HalfRight": ArrowheadSide.HALF_RIGHT,
    },
    ("arrow", "FillType"): {
        "Unspecified": FillType.UNSPECIFIED,
        "None": FillType.VALUE_NONE,
        "Solid": FillType.SOLID,
        "Shaded": FillType.SHADED,
    },
}

DTD_STRING_ENUM_TYPES: dict[str, type[object]] = {
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

EXPECTED_BOND_ORDER_XML_VALUES: dict[str, BondOrder] = {
    "1": BondOrder.SINGLE,
    "2": BondOrder.DOUBLE,
    "3": BondOrder.TRIPLE,
    "4": BondOrder.QUADRUPLE,
    "5": BondOrder.QUINTUPLE,
    "6": BondOrder.SEXTUPLE,
    "0.5": BondOrder.HALF,
    "1.5": BondOrder.AROMATIC,
    "2.5": BondOrder.TWO_AND_HALF,
    "3.5": BondOrder.THREE_AND_HALF,
    "4.5": BondOrder.FOUR_AND_HALF,
    "5.5": BondOrder.FIVE_AND_HALF,
    "dative": BondOrder.DATIVE,
    "ionic": BondOrder.IONIC,
    "hydrogen": BondOrder.HYDROGEN,
    "threecenter": BondOrder.THREE_CENTER,
}

EXPECTED_BOND_ORDER_CDX_VALUES = {
    "1": 1,
    "2": 2,
    "3": 4,
    "4": 8,
    "5": 16,
    "6": 32,
    "0.5": 64,
    "1.5": 128,
    "2.5": 256,
    "3.5": 512,
    "4.5": 1024,
    "5.5": 2048,
    "dative": 4096,
    "ionic": 8192,
    "hydrogen": 16384,
    "threecenter": 32768,
}

ENUM_TEST_TARGETS: dict[tuple[str, str], tuple[str, str]] = {
    ("b", "Display"): ("bond", "display"),
    ("group", "Integral"): ("group", "integral"),
    ("t", "Visible"): ("text", "visible"),
    ("t", "IgnoreWarnings"): ("text", "ignore_warnings"),
    ("graphic", "GraphicType"): ("graphic", "graphic_type"),
    ("graphic", "Visible"): ("graphic", "visible"),
    ("arrow", "Visible"): ("arrow", "visible"),
    ("arrow", "ArrowheadType"): ("arrow", "arrowhead_type"),
    ("arrow", "ArrowheadHead"): ("arrow", "arrowhead_head"),
    ("arrow", "ArrowheadTail"): ("arrow", "arrowhead_tail"),
    ("arrow", "FillType"): ("arrow", "fill_type"),
}


def _source_expected_enum_values() -> dict[tuple[str, str], dict[str, object]]:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    result: dict[tuple[str, str], dict[str, object]] = {}
    for element in dtd.dtd_elements:
        for attribute in element.attributes:
            if not attribute.enum_values:
                continue
            pair = (element.xml_name, attribute.name)
            expected_by_lexical: dict[str, object] = {}
            for lexical in attribute.enum_values:
                if set(attribute.enum_values) == {"yes", "no"}:
                    expected_by_lexical[lexical] = lexical == "yes"
                elif attribute.name in {"Display", "Display2"}:
                    expected_by_lexical[lexical] = BondDisplay[
                        BOND_DISPLAY_MEMBER_BY_XML_VALUE[lexical]
                    ]
                else:
                    expected_by_lexical[lexical] = ENUM_CLASS_BY_ATTRIBUTE[attribute.name](lexical)
            result[pair] = expected_by_lexical
    return result


def _enum_test_targets_from_recipes() -> dict[tuple[str, str], tuple[str, str]]:
    return {
        (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"])): (
            cast(str, case["marker"]),
            cast(str, case["field_name"]),
        )
        for case in CASES
        if (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))
        in _source_expected_enum_values()
    }


EXPECTED_MAPPED_DTD_ENUM_VALUES = _source_expected_enum_values()
ENUM_TEST_TARGETS = _enum_test_targets_from_recipes()
DTD_STRING_ENUM_TYPES = dict(ENUM_CLASS_BY_ATTRIBUTE)


SOURCED_DEFAULT_DIFFERENCES = {
    ("n", "Charge"): {
        "canonical_xml": "0",
        "dtd_xml": None,
        "source_uri": "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Atom_Charge.htm",
        "source_locator": "Default value is 0",
    },
    ("n", "Isotope"): {
        "canonical_xml": "0",
        "dtd_xml": None,
        "source_uri": "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Atom_Isotope.htm",
        "source_locator": "Default value is 0 for natural abundance",
    },
    ("b", "Order"): {
        "canonical_xml": "1",
        "dtd_xml": None,
        "source_uri": "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Bond_Order.htm",
        "source_locator": "If this property is absent, it is treated as a single bond",
    },
    ("objecttag", "Value"): {
        "canonical_xml": "0",
        "dtd_xml": None,
        "source_uri": "https://web.archive.org/web/20190326232119id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/ObjectTag_Value.htm",
        "source_locator": "ObjectTag.Value is zero when the value property is absent",
    },
    ("marker", "Value"): {
        "canonical_xml": "0",
        "dtd_xml": None,
        "source_uri": "https://web.archive.org/web/20190326232119id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/ObjectTag_Value.htm",
        "source_locator": "ObjectTag.Value is zero when the value property is absent",
    },
    ("plasmidmarker", "Value"): {
        "canonical_xml": "0",
        "dtd_xml": None,
        "source_uri": "https://web.archive.org/web/20190326232119id_/http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx/properties/ObjectTag_Value.htm",
        "source_locator": "ObjectTag.Value is zero when the value property is absent",
    },
}


def _expected_value(spec: dict[str, object], document: CDXMLDocument) -> object:
    kind = cast(str, spec["type"])
    if kind in {"str", "int", "float", "bool"}:
        return spec["value"]
    if kind == "enum":
        enum_classes = {
            enum_type.__name__: enum_type
            for enum_type in (
                *DTD_STRING_ENUM_TYPES.values(),
                BondDisplay,
                BondOrder,
                GraphicType,
            )
        }
        enum_type = enum_classes[cast(str, spec["class"])]
        return enum_type[cast(str, spec["member"])]
    if kind in {"Point2D", "Point3D", "BoundingBox"}:
        coordinates = cast(list[float], spec["coordinates"])
        if kind == "Point2D":
            return Point2D(coordinates[0], coordinates[1])
        if kind == "Point3D":
            return Point3D(coordinates[0], coordinates[1], coordinates[2])
        return BoundingBox(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
    if kind == "Point2DList":
        coordinates = cast(list[float], spec["coordinates"])
        return tuple(
            Point2D(coordinates[i], coordinates[i + 1]) for i in range(0, len(coordinates), 2)
        )
    if kind == "Point3DList":
        coordinates = cast(list[float], spec["coordinates"])
        return tuple(
            Point3D(coordinates[i], coordinates[i + 1], coordinates[i + 2])
            for i in range(0, len(coordinates), 3)
        )
    if kind == "int_list":
        return tuple(cast(list[int], spec["values"]))
    if kind == "ElementList":
        return ElementList(tuple(cast(list[int], spec["elements"])), cast(bool, spec["negated"]))
    if kind == "GenericList":
        return GenericList(tuple(cast(list[str], spec["values"])), cast(bool, spec["negated"]))
    if kind == "reference":
        model = _model_class(cast(str, spec["model"]))
        result = document.get(model, cast(int, spec["id"]))
        assert result is not None
        return result
    if kind == "references":
        items = cast(list[dict[str, object]], spec["items"])
        result: list[CDXMLElement] = []
        for item in items:
            model = _model_class(cast(str, item["model"]))
            value = document.get(model, cast(int, item["id"]))
            assert value is not None
            result.append(value)
        return tuple(result)
    raise AssertionError(f"unsupported independent recipe type {kind!r}")


def _model_tags_from_contract() -> dict[str, str]:
    return {
        cast(str, case["expected_model"]): cast(str, case["xml_name"])
        for case in ELEMENT_CASES
        if isinstance(case["expected_model"], str)
    }


MODEL_TAG_BY_NAME = _model_tags_from_contract()
DTD_ELEMENT_BY_TAG = {
    element.xml_name: element
    for element in import_dtd(
        str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd")
    ).dtd_elements
}


def _required_attribute_values(
    xml_tag: str, *, forced_id: int | None = None, next_id: int = 9000
) -> dict[str, str]:
    element = DTD_ELEMENT_BY_TAG[xml_tag]
    values: dict[str, str] = {}
    for attribute in element.attributes:
        if not attribute.required:
            continue
        if attribute.name == "id":
            values[attribute.name] = str(forced_id if forced_id is not None else next_id)
        elif attribute.name == "B":
            values[attribute.name] = "200"
        elif attribute.name == "E":
            values[attribute.name] = "201"
        elif attribute.name == "BondID":
            values[attribute.name] = "400"
        elif attribute.name == "object":
            values[attribute.name] = "202"
        elif attribute.name == "InnerAtomID":
            values[attribute.name] = "200"
        elif attribute.name == "Name":
            values[attribute.name] = "Feature"
        elif attribute.name in {"r", "g", "b"}:
            values[attribute.name] = {"r": "0.25", "g": "0.5", "b": "0.75"}[attribute.name]
        elif attribute.enum_values:
            values[attribute.name] = attribute.enum_values[0]
        else:
            values[attribute.name] = "Feature"
    return values


def _make_case_xml(case: dict[str, object]) -> str:
    root = etree.Element("CDXML", nsmap={"v": VENDOR_NS})
    root.set(VENDOR_ROOT, "preserve-root")
    root.append(etree.Comment("preserve source comment and following sibling order"))

    color_table = etree.SubElement(root, "colortable")
    etree.SubElement(color_table, "color", r="0.25", g="0.5", b="0.75")
    font_table = etree.SubElement(root, "fonttable")
    etree.SubElement(font_table, "font", id="1", name="Base Font")
    page = etree.SubElement(root, "page", id="1")

    def ensure_node(object_id: int) -> etree._Element:
        fragment = next((item for item in page if item.tag == "fragment"), None)
        if fragment is None:
            fragment = etree.SubElement(page, "fragment")
        existing = next(
            (item for item in fragment.iter("n") if item.get("id") == str(object_id)), None
        )
        if existing is not None:
            return existing
        node = etree.SubElement(
            fragment,
            "n",
            id=str(object_id),
            element="6",
            p="001.250 02.500",
        )
        return node

    ensure_node(200)
    ensure_node(201)
    ensure_node(202)
    fragment = next(item for item in page if item.tag == "fragment")
    etree.SubElement(fragment, "b", id="400", B="200", E="201", Order="1")

    def append_by_source_route(xml_tag: str, *, forced_id: int | None = None) -> etree._Element:
        path = cast(list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["root_path"])
        if path == ["CDXML"]:
            return root
        current = root
        for index, path_tag in enumerate(path[1:], start=1):
            is_final = index == len(path) - 1
            if is_final and path_tag == "page":
                current = page
                continue
            if is_final and path_tag == "colortable":
                current = color_table
                continue
            if is_final and path_tag == "fonttable":
                current = font_table
                continue
            if not is_final:
                found = next((child for child in current if child.tag == path_tag), None)
                if found is not None:
                    current = found
                    continue
            attrs = _required_attribute_values(
                path_tag,
                forced_id=forced_id if is_final else None,
                next_id=9000 + len(list(root.iter())),
            )
            current = etree.SubElement(current, path_tag, **attrs)
        return current

    # Source-referenced objects are real, typed model instances in this parse;
    # their identities are independent of the reference decoder's output.
    for ref in cast(list[dict[str, object]], case.get("reference_targets", [])):
        model_name = cast(str, ref["model"])
        xml_tag = MODEL_TAG_BY_NAME[model_name]
        object_id = cast(int, ref["id"])
        if xml_tag == "n":
            ensure_node(object_id)
        else:
            referenced = append_by_source_route(xml_tag, forced_id=object_id)
            if "id" not in referenced.attrib:
                referenced.set("id", str(object_id))

    owner = cast(str, case["owner_tag"])
    expected = cast(dict[str, object], case["expected"])
    expected_type = cast(str, expected["type"])
    forced_id = (
        cast(int, expected["value"])
        if expected_type == "int" and case["xml_attribute"] == "id"
        else None
    )
    target = append_by_source_route(owner, forced_id=forced_id)
    target.set(VENDOR_CASE, cast(str, case["marker"]))
    target.set(cast(str, case["xml_attribute"]), cast(str, case["source_xml"]))
    for key, value in cast(dict[str, str], case.get("source_context", {})).items():
        target.set(key, value)
    if owner == "s":
        target.text = "seed"
    if owner == "t" and not any(child.tag == "s" for child in target):
        text_run = etree.SubElement(target, "s")
        text_run.text = "seed"

    etree.SubElement(root, f"{{{VENDOR_NS}}}opaque", marker="preserve-element")
    return etree.tostring(root, encoding="unicode")


def _mapped_enum_alternatives() -> tuple[tuple[str, str, str, str, str, object], ...]:
    cases: list[tuple[str, str, str, str, str, object]] = []
    for (owner, xml_attribute), values in EXPECTED_MAPPED_DTD_ENUM_VALUES.items():
        marker, field_name = ENUM_TEST_TARGETS[(owner, xml_attribute)]
        cases.extend(
            (owner, xml_attribute, marker, field_name, lexical, expected)
            for lexical, expected in values.items()
        )
    return tuple(cases)


MAPPED_ENUM_ALTERNATIVES = _mapped_enum_alternatives()
MAPPED_ENUM_ALTERNATIVE_IDS = tuple(
    f"{case[0]}@{case[1]}={case[4]}" for case in MAPPED_ENUM_ALTERNATIVES
)


def _case_for_pair(owner: str, attribute: str) -> dict[str, object]:
    return next(
        case for case in CASES if case["owner_tag"] == owner and case["xml_attribute"] == attribute
    )


def _target(document: CDXMLDocument, case: dict[str, object]) -> CDXMLElement:
    tag = cast(str, case["owner_tag"])
    marker = cast(str, case["marker"])
    marker_name = "{urn:vendor}case"
    matches = [
        document.wrap(element)
        for element in document.tree.iter()
        if isinstance(element.tag, str)
        and element.tag == tag
        and element.get(marker_name) == marker
    ]
    assert len(matches) == 1
    return matches[0]


def _assert_typed_value(actual: object, expected: object) -> None:
    assert type(actual) is type(expected)
    if isinstance(expected, CDXMLElement):
        assert actual is expected
    elif isinstance(expected, tuple) and all(isinstance(item, CDXMLElement) for item in expected):
        assert actual == expected
        assert all(
            left is right
            for left, right in zip(cast(tuple[object, ...], actual), expected, strict=True)
        )
    else:
        assert actual == expected


def _assert_opaque_fixture_content(serialized: str) -> None:
    assert 'xmlns:v="urn:vendor"' in serialized
    assert 'v:root="preserve-root"' in serialized
    assert "preserve source comment and following sibling order" in serialized
    assert '<v:opaque marker="preserve-element"' in serialized
    assert serialized.index("<colortable") < serialized.index("<fonttable")
    assert serialized.index("<fonttable") < serialized.index("<page")
    assert serialized.index("<page") < serialized.index("<v:opaque")


@pytest.mark.parametrize("case", CASES, ids=_case_id)
def test_mapped_pair_parse_read_mutate_serialize_reload(case: dict[str, object]) -> None:
    expected_nodeid = cast(str, case["pytest_nodeid"])
    case_id = cast(str, case["case_id"])
    assert expected_nodeid.endswith(f"[{case_id}]")

    document = CDXMLDocument.from_string(_make_case_xml(case))
    target = _target(document, case)
    xml_attribute = cast(str, case["xml_attribute"])
    field_name = cast(str, case["field_name"])

    assert type(target) is _model_class(EXPECTED_MODEL_BY_TAG[target.xml_tag])
    assert target.raw_attributes[xml_attribute] == case["source_xml"]
    source_expected = _expected_value(cast(dict[str, object], case["expected"]), document)
    _assert_typed_value(getattr(target, field_name), source_expected)

    mutation_expected = _expected_value(cast(dict[str, object], case["mutation"]), document)
    setattr(target, field_name, mutation_expected)
    assert target.raw_attributes[xml_attribute] == case["mutation_xml"]

    serialized = document.to_string()
    _assert_opaque_fixture_content(serialized)
    restored = CDXMLDocument.from_string(serialized)
    restored_target = _target(restored, case)
    assert type(restored_target) is type(target)
    assert restored_target.raw_attributes[xml_attribute] == case["mutation_xml"]
    reloaded_expected = _expected_value(cast(dict[str, object], case["mutation"]), restored)
    _assert_typed_value(getattr(restored_target, field_name), reloaded_expected)

    base_node = next(element for element in document.tree.iter("n") if element.get("id") == "200")
    assert base_node.get("p") == "001.250 02.500"


def _modeled_attribute_pairs() -> set[tuple[str, str]]:
    return {
        (metadata.xml_tag, prop.xml_name)
        for metadata in OBJECT_METADATA.values()
        for prop in metadata.properties.values()
        if prop.storage == "attribute"
    }


def test_recipe_pairs_exactly_cover_current_static_attribute_mappings() -> None:
    recipe_pairs = {
        (cast(str, case["owner_tag"]), cast(str, case["xml_attribute"])) for case in CASES
    }
    assert len(recipe_pairs) == len(CASES)
    dtd_pairs = {
        (element.xml_name, attribute.name)
        for element in import_dtd(
            str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd")
        ).dtd_elements
        for attribute in element.attributes
    }
    assert len(dtd_pairs) == 762
    assert recipe_pairs == dtd_pairs
    assert recipe_pairs <= _modeled_attribute_pairs()


def test_feature_case_ids_match_the_exact_owner_attribute_recipe() -> None:
    for case in CASES:
        owner = cast(str, case["owner_tag"])
        attribute = cast(str, case["xml_attribute"])
        case_id = f"feature:{owner}@{attribute}"
        nodeid = (
            "tests/coverage/test_full_schema_feature_evidence.py::"
            f"test_mapped_pair_parse_read_mutate_serialize_reload[{case_id}]"
        )
        assert case["case_id"] == case_id
        assert case["pytest_nodeid"] == nodeid
        assert case["assertions"] == [
            "exact_wrapper_type",
            "source_lexical_value",
            "typed_read_value_and_python_type",
            "typed_mutation",
            "mutation_lexical_value",
            "serialization_reload_readback",
            "unknown_content_and_order_preserved",
        ]


@pytest.mark.parametrize(
    "case",
    tuple(case for case in CHARACTER_DATA_CASES if case["pytest_nodeid"] is not None),
    ids=lambda case: cast(str, case["case_id"]),
)
def test_character_data_parse_read_mutate_serialize_reload(
    case: dict[str, object],
) -> None:
    case_id = cast(str, case["case_id"])
    assert cast(str, case["pytest_nodeid"]).endswith(f"[{case_id}]")
    if case["xml_name"] == "s":
        document = CDXMLDocument.from_file(FIXTURE_PATH)
        matches = [
            document.wrap(element)
            for element in document.tree.iter("s")
            if element.get("{urn:vendor}case") == "run"
        ]
        assert len(matches) == 1
        target = matches[0]
        assert type(target) is TextRun
        content_field = "content"
    else:
        document = CDXMLDocument.from_string(_spectrum_case_xml(case))
        matches = [
            document.wrap(element)
            for element in document.tree.iter("spectrum")
            if element.get(VENDOR_CASE) == case_id
        ]
        assert len(matches) == 1
        target = matches[0]
        assert type(target).__name__ == "Spectrum"
        content_field = "data"

    assert getattr(target, content_field) == case["expected"]
    assert type(getattr(target, content_field)) is str
    assert target.raw_element.text == case["source_xml"]
    target_children_before = [
        child.tag for child in target.raw_element if isinstance(child.tag, str)
    ]
    if case["xml_name"] == "s":
        assert target_children_before == []
    else:
        assert target_children_before == ["objecttag", "annotation"]
        assert target.objecttags[0].name == "peak-label"
        assert target.annotations[0].xml_tag == "annotation"

        # The `data` value is the whole direct-PCDATA projection: an unrelated
        # attribute edit must retain every original segment and nested label.
        target.visible = False
        assert target.data == case["expected"]
        unrelated_xml = document.to_string()
        document = CDXMLDocument.from_string(unrelated_xml)
        target = next(
            document.wrap(element)
            for element in document.tree.iter("spectrum")
            if element.get(VENDOR_CASE) == case_id
        )
        assert target.visible is False
        assert target.data == case["expected"]
        assert target.raw_element[0].tail == "300 400 "
        assert target.raw_element[-1].tail == "500 600"
        assert target.objecttags[0].name == "peak-label"
        assert "preserve spectrum child-order comment" in unrelated_xml

    setattr(target, content_field, cast(str, case["mutation"]))
    assert target.raw_element.text == case["mutation_xml"]
    expected_after_mutation = cast(str, case.get("mutation_readback", case["mutation"]))
    assert getattr(target, content_field) == expected_after_mutation
    assert type(getattr(target, content_field)) is str

    serialized = document.to_string()
    restored = CDXMLDocument.from_string(serialized)
    tag = cast(str, case["xml_name"])
    if tag == "spectrum":
        restored_matches = [
            restored.wrap(element)
            for element in restored.tree.iter(tag)
            if element.get(VENDOR_CASE) == case_id
        ]
    else:
        restored_matches = [
            restored.wrap(element)
            for element in restored.tree.iter(tag)
            if element.get("{urn:vendor}case") == "run"
        ]
    assert len(restored_matches) == 1
    restored_target = restored_matches[0]
    assert type(restored_target) is type(target)
    assert restored_target.raw_element.text == case["mutation_xml"]
    assert getattr(restored_target, content_field) == expected_after_mutation
    assert type(getattr(restored_target, content_field)) is str
    if tag == "spectrum":
        assert [
            child.tag for child in restored_target.raw_element if isinstance(child.tag, str)
        ] == ["objecttag", "annotation"]
        assert restored_target.objecttags[0].name == "peak-label"
        assert restored_target.annotations[0].xml_tag == "annotation"
        assert "preserve spectrum child-order comment" in serialized
        assert restored_target.raw_element[0].tail in {None, ""}
        assert restored_target.raw_element[-1].tail in {None, ""}


def _spectrum_case_xml(case: dict[str, object]) -> str:
    root = etree.Element("CDXML", nsmap={"v": VENDOR_NS})
    page = etree.SubElement(root, "page", id="1")
    spectrum = etree.SubElement(page, "spectrum")
    spectrum.set(VENDOR_CASE, cast(str, case["case_id"]))
    spectrum.text = cast(str, case["source_xml"])
    objecttag = etree.SubElement(spectrum, "objecttag", Name="peak-label")
    objecttag.text = "nested label must not enter the numeric series"
    objecttag.tail = "300 400 "
    spectrum.append(etree.Comment("preserve spectrum child-order comment"))
    annotation = etree.SubElement(spectrum, "annotation")
    annotation.tail = "500 600"
    return etree.tostring(root, encoding="unicode")


def test_character_data_catalog_covers_both_pinned_pcdata_tags() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    pcdata_tags = {
        element.xml_name for element in dtd.dtd_elements if element.declaration_type == "mixed"
    }
    rows = {cast(str, case["xml_name"]): case for case in CHARACTER_DATA_CASES}
    assert pcdata_tags == {"s", "spectrum"}
    assert set(rows) == pcdata_tags
    text_run = rows["s"]
    assert text_run["case_id"] == "feature-character:s"
    assert isinstance(text_run["pytest_nodeid"], str)
    assert text_run["assertions"] == [
        "storage_lexical_value",
        "typed_read_value_and_python_type",
        "typed_mutation",
        "mutation_lexical_value",
        "serialization_reload_readback",
    ]
    assert text_run["source_xml"] == "seed"
    assert text_run["expected"] == "seed"
    assert text_run["mutation"] == "new <glyph> & ligature"
    assert text_run["gap_reason"] is None

    spectrum = rows["spectrum"]
    assert spectrum["case_id"] == "feature-character:spectrum"
    assert isinstance(spectrum["pytest_nodeid"], str)
    assert spectrum["assertions"] == text_run["assertions"]
    assert spectrum["source_xml"] == "100 200 "
    assert spectrum["expected"] == "100 200 300 400 500 600"
    assert spectrum["mutation"] == "110 220"
    # Assigning .data replaces the whole direct PCDATA value, including text
    # tails around mixed-content children.
    assert spectrum["mutation_readback"] == "110 220"
    assert spectrum["gap_reason"] is None


def test_element_case_inventory_matches_all_pinned_dtd_declarations() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    catalog = _read_case_catalog()
    assert catalog["dtd_sha256"] == dtd.source.sha256
    assert len(dtd.dtd_elements) == 53
    assert len(ELEMENT_CASES) == 53
    assert {cast(str, case["xml_name"]) for case in ELEMENT_CASES} == {
        element.xml_name for element in dtd.dtd_elements
    }
    assert set(EXPECTED_MODEL_BY_TAG) == {element.xml_name for element in dtd.dtd_elements}
    assert len(set(EXPECTED_MODEL_BY_TAG.values())) == len(dtd.dtd_elements)
    for case in ELEMENT_CASES:
        xml_name = cast(str, case["xml_name"])
        assert isinstance(case["expected_model"], str)
        case_id = f"feature-element:{xml_name}"
        assert case["case_id"] == case_id
        nodeid = case["pytest_nodeid"]
        assertions = cast(list[str], case["assertions"])
        if nodeid is None:
            assert assertions == []
            continue
        assert isinstance(nodeid, str)
        assert nodeid.endswith(f"[{case_id}]")

    for metadata in OBJECT_METADATA.values():
        item = next(case for case in ELEMENT_CASES if case["xml_name"] == metadata.xml_tag)
        assert item["expected_model"] == metadata.python_name


def test_typed_attributes_and_recipe_lexicals_are_present_in_the_pinned_dtd() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    attributes = {
        (element.xml_name, attribute.name): attribute
        for element in dtd.dtd_elements
        for attribute in element.attributes
    }
    assert set(attributes) <= _modeled_attribute_pairs()
    for case in CASES:
        declaration = attributes[(cast(str, case["owner_tag"]), cast(str, case["xml_attribute"]))]
        if declaration.enum_values:
            assert case["source_xml"] in declaration.enum_values
            assert case["mutation_xml"] in declaration.enum_values


def test_dtd_parent_paths_and_required_attribute_contracts_cover_all_53_elements() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    assert dtd.source.sha256 == DTD_SHA256
    assert SOURCE_CONTRACTS["dtd_sha256"] == DTD_SHA256
    source_rows = cast(list[dict[str, object]], SOURCE_CONTRACTS["elements"])
    by_tag = {element.xml_name: element for element in dtd.dtd_elements}
    rows_by_tag = {cast(str, row["xml_name"]): row for row in source_rows}
    assert len(source_rows) == 53
    assert len(rows_by_tag) == len(source_rows)
    assert set(rows_by_tag) == set(by_tag)

    actual_parents: dict[str, set[str]] = {tag: set() for tag in by_tag}
    for parent in dtd.dtd_elements:
        for child in parent.children:
            if child in actual_parents:
                actual_parents[child].add(parent.xml_name)

    # The source paths are static contracts; verify their edges and shortest
    # lengths against the pinned DTD so future lifecycle tests can reuse them.
    distances = {"CDXML": 0}
    queue = ["CDXML"]
    while queue:
        parent_tag = queue.pop(0)
        for child_tag in by_tag[parent_tag].children:
            if child_tag in by_tag and child_tag not in distances:
                distances[child_tag] = distances[parent_tag] + 1
                queue.append(child_tag)

    assert set(distances) == set(by_tag)
    for tag, row in rows_by_tag.items():
        assert row["parents"] == sorted(actual_parents[tag])
        assert row["required_attributes"] == sorted(
            attribute.name for attribute in by_tag[tag].attributes if attribute.required
        )
        path = cast(list[str], row["root_path"])
        assert path[0] == "CDXML"
        assert path[-1] == tag
        assert len(path) - 1 == distances[tag]
        assert all(
            child in by_tag[parent].children and parent in actual_parents[child]
            for parent, child in zip(path, path[1:], strict=False)
        )
        minimum_child_counts = cast(dict[str, int], row.get("minimum_child_counts", {}))
        if minimum_child_counts:
            content_model = by_tag[tag].content_model
            assert content_model.kind == "element"
            assert content_model.occurrence == "plus"
            assert minimum_child_counts == {cast(str, content_model.name): 1}


def _canonical_default_xml(value: object) -> str | None:
    if value is None:
        return None
    if type(value) is bool:
        return "yes" if value else "no"
    return str(value)


def _default_is_semantically_equal(canonical_value: object, dtd_value: str | None) -> bool:
    """Compare DTD defaults as values without changing any serialized lexicals."""
    if canonical_value is None or dtd_value is None:
        return canonical_value is None and dtd_value is None
    if type(canonical_value) in {int, float}:
        try:
            return float(canonical_value) == float(dtd_value)
        except ValueError:
            return False
    return _canonical_default_xml(canonical_value) == dtd_value


def test_mapped_dtd_required_default_and_enum_contracts_are_reconciled() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    declarations = {
        (element.xml_name, attribute.name): attribute
        for element in dtd.dtd_elements
        for attribute in element.attributes
    }
    mapped_enum_pairs: set[tuple[str, str]] = set()
    observed_default_differences: dict[tuple[str, str], dict[str, str | None]] = {}

    for spec_id, metadata in OBJECT_METADATA.items():
        for prop in metadata.properties.values():
            if prop.storage != "attribute":
                continue
            pair = (metadata.xml_tag, prop.xml_name)
            if pair not in declarations:
                continue
            declaration = declarations[pair]
            assert prop.required is declaration.required, (spec_id, prop.name, pair)
            canonical_default = _canonical_default_xml(prop.default)
            if not _default_is_semantically_equal(prop.default, declaration.default_value):
                observed_default_differences[pair] = {
                    "canonical_xml": canonical_default,
                    "dtd_xml": declaration.default_value,
                }
            if declaration.enum_values:
                mapped_enum_pairs.add(pair)
                assert declaration.default_value is None or (
                    declaration.default_value in declaration.enum_values
                )

    expected_default_differences = {
        pair: {
            "canonical_xml": cast(str | None, recipe["canonical_xml"]),
            "dtd_xml": cast(str | None, recipe["dtd_xml"]),
        }
        for pair, recipe in SOURCED_DEFAULT_DIFFERENCES.items()
    }
    assert observed_default_differences == expected_default_differences
    assert mapped_enum_pairs == set(EXPECTED_MAPPED_DTD_ENUM_VALUES)

    for pair, expected_values in EXPECTED_MAPPED_DTD_ENUM_VALUES.items():
        declaration = declarations[pair]
        assert tuple(expected_values) == declaration.enum_values
        assert pair in ENUM_TEST_TARGETS

    for pair, recipe in SOURCED_DEFAULT_DIFFERENCES.items():
        metadata = next(item for item in OBJECT_METADATA.values() if item.xml_tag == pair[0])
        property_metadata = next(
            prop for prop in metadata.properties.values() if prop.xml_name == pair[1]
        )
        source_uri = cast(str, recipe["source_uri"])
        source_locator = cast(str, recipe["source_locator"])
        assert any(
            item.uri == source_uri and source_locator in item.locator
            for item in property_metadata.provenance
        ), f"{pair} has no provenance for its canonical-vs-DTD default difference"


def test_mapped_sdk_property_ids_and_provenance_match_exact_source_facts() -> None:
    evidence = json.loads(SDK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    source_rows = cast(list[dict[str, object]], evidence["owner_attribute_pairs"])
    by_pair = {
        (cast(str, row["owner_xml_name"]), cast(str, row["xml_name"])): row for row in source_rows
    }
    source_ids = {
        cast(str, row["id"]) for row in cast(list[dict[str, object]], evidence["sources"])
    }
    sources_by_id = {
        cast(str, row["id"]): row for row in cast(list[dict[str, object]], evidence["sources"])
    }
    assert len(source_rows) == 762
    assert len(by_pair) == 762
    exact_source_rows = [row for row in source_rows if row["sdk_matches"]]
    assert len(exact_source_rows) == 410
    observed_gaps: dict[tuple[str, str], tuple[int | None, str | None]] = {}

    for metadata in OBJECT_METADATA.values():
        for prop in metadata.properties.values():
            if prop.storage != "attribute":
                continue
            pair = (metadata.xml_tag, prop.xml_name)
            if pair not in by_pair:
                continue
            source_row = by_pair[pair]
            sdk_matches = cast(list[dict[str, object]], source_row["sdk_matches"])
            if not sdk_matches:
                continue
            matching_properties = {
                (item.get("cdx_id"), item.get("cdx_constant")) for item in sdk_matches
            }
            assert len(matching_properties) == 1, pair
            expected_id, expected_constant = next(iter(matching_properties))
            source_fact = cast(dict[str, object], sdk_matches[0]["source"])
            source_id = cast(str, source_fact["source_id"])
            assert source_id in source_ids
            source_manifest = sources_by_id[source_id]
            assert len(cast(str, source_manifest["sha256"])) == 64
            source_locator = cast(str, source_fact["locator"])
            expected_source_uris = {cast(str, source_manifest["snapshot_url"])}
            registered_source = SOURCES.get(source_id)
            if registered_source is not None:
                expected_source_uris.add(registered_source.uri)
            assert any(
                provenance.uri in expected_source_uris and provenance.locator == source_locator
                for provenance in prop.provenance
            ), (pair, source_id, source_locator, sorted(expected_source_uris))

            actual = (prop.cdx_id, prop.cdx_constant)
            expected = (cast(int | None, expected_id), cast(str | None, expected_constant))
            if pair in SDK_SOURCE_ID_CONFLICT_PAIRS:
                assert expected[0] == 2616
                assert actual == (None, None)
                continue
            if actual != expected:
                observed_gaps[pair] = expected
                continue

    assert observed_gaps == EXPECTED_CURRENT_SDK_MAPPING_GAPS


def test_sdk_numeric_types_are_not_silently_generated_as_strings() -> None:
    evidence = json.loads(SDK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    source_rows = cast(list[dict[str, object]], evidence["owner_attribute_pairs"])
    by_pair = {
        (cast(str, row["owner_xml_name"]), cast(str, row["xml_name"])): row for row in source_rows
    }
    integer_types = {"INT8", "UINT8", "INT16", "UINT16", "INT32", "UINT32"}
    float_types = {"FLOAT64", "CDXCoordinate"}
    observed_gaps: set[tuple[str, str]] = set()
    observed_xml_overrides: set[tuple[str, str]] = set(SDK_BINARY_TYPE_XML_OVERRIDES)
    expected_xml_overrides = set(SDK_BINARY_TYPE_XML_OVERRIDES)
    for attribute, family in SDK_BINARY_XML_FAMILY_OVERRIDES.items():
        owners = cast(set[str], family["owners"])
        family_pairs = {(owner, attribute) for owner in owners}
        expected_xml_overrides.update(family_pairs)
        assert len(family_pairs) == len(owners)

    for metadata in OBJECT_METADATA.values():
        for prop in metadata.properties.values():
            if prop.storage != "attribute":
                continue
            pair = (metadata.xml_tag, prop.xml_name)
            if pair not in by_pair:
                continue
            source_row = by_pair[pair]
            sdk_matches = cast(list[dict[str, object]], source_row["sdk_matches"])
            if not sdk_matches:
                continue
            assert len(sdk_matches) == 1, pair
            sdk_type = sdk_matches[0]["sdk_type"]
            if sdk_type not in integer_types | float_types:
                continue

            if pair in SDK_BINARY_TYPE_XML_OVERRIDES:
                override = SDK_BINARY_TYPE_XML_OVERRIDES[pair]
            else:
                family = SDK_BINARY_XML_FAMILY_OVERRIDES.get(pair[1])
                if family is not None and pair[0] in cast(set[str], family["owners"]):
                    override = cast(dict[str, str], family)
                else:
                    override = None

            if override is not None:
                observed_xml_overrides.add(pair)
                assert sdk_type == override["sdk_type"], pair
                assert prop.enum is None, pair
                datatype = DATATYPE_METADATA[prop.datatype]
                assert datatype.python_type == override["xml_python_type"], pair
                case = _case_for_pair(*pair)
                expected = cast(dict[str, object], case["expected"])
                assert expected["type"] == override["xml_python_type"], pair
                source_uri = override["source_uri"]
                source_locator = override.get("provenance_locator", override["source_locator"])
                assert any(
                    item.uri == source_uri and source_locator in item.locator
                    for item in prop.provenance
                ), (pair, source_uri, source_locator)
                continue

            if source_row["enum_values"]:
                if prop.enum is None:
                    observed_gaps.add(pair)
                continue

            expected_type = "float" if sdk_type in float_types else "int"
            datatype = DATATYPE_METADATA[prop.datatype]
            if datatype.python_type != expected_type or datatype.kind == "string":
                observed_gaps.add(pair)

    assert observed_xml_overrides == expected_xml_overrides
    assert observed_gaps == EXPECTED_CURRENT_SDK_NUMERIC_TYPE_GAPS


def test_font_charset_has_sourced_binary_numeric_to_xml_string_override() -> None:
    case = next(
        item for item in CASES if (item["owner_tag"], item["xml_attribute"]) == ("font", "charset")
    )
    override = SDK_BINARY_TYPE_XML_OVERRIDES[("font", "charset")]
    expected = cast(dict[str, object], case["expected"])
    assert case["source_xml"] == "iso-8859-1"
    assert expected == {"type": "str", "value": "iso-8859-1"}
    assert case["mutation_xml"] == "UTF-8"
    assert cast(dict[str, object], case["mutation"]) == {"type": "str", "value": "UTF-8"}
    assert override["sdk_type"] == "INT16"
    assert override["xml_python_type"] == "str"
    assert override["source_locator"] in (
        'CDXML example <font id="3" charset="iso-8859-1" name="Arial"/>'
    )


@pytest.mark.parametrize(
    ("owner_tag", "xml_attribute", "marker", "field_name", "lexical", "expected"),
    MAPPED_ENUM_ALTERNATIVES,
    ids=MAPPED_ENUM_ALTERNATIVE_IDS,
)
def test_every_mapped_dtd_enum_alternative_reads_writes_and_reloads(
    owner_tag: str,
    xml_attribute: str,
    marker: str,
    field_name: str,
    lexical: str,
    expected: object,
) -> None:
    feature_case = _case_for_pair(owner_tag, xml_attribute)
    document = CDXMLDocument.from_string(_make_case_xml(feature_case))
    target = _target(document, feature_case)
    target.raw_element.set(xml_attribute, lexical)
    assert target.raw_attributes[xml_attribute] == lexical

    actual = getattr(target, field_name)
    assert type(actual) is type(expected)
    if isinstance(expected, (BondDisplay, GraphicType)):
        assert actual is expected
    else:
        assert actual == expected

    setattr(target, field_name, expected)
    assert target.raw_attributes[xml_attribute] == lexical
    restored = CDXMLDocument.from_string(document.to_string())
    restored_target = _target(restored, feature_case)
    assert restored_target.raw_attributes[xml_attribute] == lexical
    reloaded = getattr(restored_target, field_name)
    assert type(reloaded) is type(expected)
    if isinstance(expected, (BondDisplay, GraphicType)):
        assert reloaded is expected
    else:
        assert reloaded == expected


@pytest.mark.parametrize(
    ("lexical", "expected"),
    tuple(EXPECTED_BOND_ORDER_XML_VALUES.items()),
    ids=tuple(f"b@Order={lexical}" for lexical in EXPECTED_BOND_ORDER_XML_VALUES),
)
def test_every_bond_order_xml_flag_reads_writes_and_reloads(
    lexical: str,
    expected: BondOrder,
) -> None:
    documented_values = ENUM_METADATA["bond_order"].values
    by_xml_value = {value.xml_value: value for value in documented_values}
    assert set(by_xml_value) == set(EXPECTED_BOND_ORDER_XML_VALUES)
    assert set(EXPECTED_BOND_ORDER_CDX_VALUES) == set(EXPECTED_BOND_ORDER_XML_VALUES)
    assert by_xml_value[lexical].cdx_value == EXPECTED_BOND_ORDER_CDX_VALUES[lexical]
    assert expected.value == EXPECTED_BOND_ORDER_CDX_VALUES[lexical]

    feature_case = _case_for_pair("b", "Order")
    document = CDXMLDocument.from_string(_make_case_xml(feature_case))
    bond = _target(document, feature_case)
    bond.raw_element.set("Order", lexical)
    assert bond.raw_attributes["Order"] == lexical
    assert bond.order is expected

    bond.order = expected
    assert bond.raw_attributes["Order"] == lexical
    restored = CDXMLDocument.from_string(document.to_string())
    restored_bond = _target(restored, feature_case)
    assert restored_bond.raw_attributes["Order"] == lexical
    assert restored_bond.order is expected


def test_bond_order_default_single_is_not_the_binary_unspecified_sentinel() -> None:
    assert SOURCED_DEFAULT_DIFFERENCES[("b", "Order")]["canonical_xml"] == "1"
    assert all(value.name != "UNSPECIFIED" for value in ENUM_METADATA["bond_order"].values)
    assert "UNSPECIFIED" not in BondOrder.__members__
    assert "0xffff" not in EXPECTED_BOND_ORDER_XML_VALUES
    assert "65535" not in EXPECTED_BOND_ORDER_XML_VALUES


def test_bond_order_flag_combinations_round_trip_as_xml_tokens() -> None:
    lexical = "2 1"
    expected = BondOrder.DOUBLE | BondOrder.SINGLE
    feature_case = _case_for_pair("b", "Order")
    document = CDXMLDocument.from_string(_make_case_xml(feature_case))
    bond = _target(document, feature_case)
    bond.raw_element.set("Order", lexical)
    assert bond.order == expected
    assert type(bond.order) is BondOrder

    bond.order = expected
    assert bond.raw_attributes["Order"] == "1 2"
    restored = CDXMLDocument.from_string(document.to_string())
    restored_bond = _target(restored, feature_case)
    assert restored_bond.raw_attributes["Order"] == "1 2"
    assert restored_bond.order == expected
    assert type(restored_bond.order) is BondOrder


def test_cdxml_root_facade_is_counted_separately_from_typed_element_models() -> None:
    document = CDXMLDocument.from_file(FIXTURE_PATH)
    assert type(document.root) is CDXMLRoot
    assert document.root.xml_tag == "CDXML"
    assert document.root.raw_attributes["{urn:vendor}root"] == "preserve-root"
    assert OBJECT_BY_XML_TAG["CDXML"] is CDXMLRoot


ROOT_ELEMENT_CASES = tuple(case for case in ELEMENT_CASES if case["xml_name"] == "CDXML")


@pytest.mark.parametrize("case", ROOT_ELEMENT_CASES, ids=lambda case: cast(str, case["case_id"]))
def test_root_creation_mutation_round_trip(case: dict[str, object]) -> None:
    case_id = cast(str, case["case_id"])
    assert cast(str, case["pytest_nodeid"]).endswith(f"[{case_id}]")
    assert case["assertions"] == [
        "exact_wrapper_type",
        "root_creation",
        "root_mutation",
        "element_round_trip",
    ]

    document = CDXMLDocument.from_string("<CDXML/>")
    root = document.root
    assert type(root) is _model_class(cast(str, case["expected_model"]))
    assert root.xml_tag == "CDXML"
    root.raw_element.set(VENDOR_CASE, case_id)
    root.line_width = 1.25
    assert root.raw_attributes["LineWidth"] == "1.25"
    assert root.line_width == 1.25

    restored = CDXMLDocument.from_string(document.to_string())
    restored_root = restored.root
    assert type(restored_root) is type(root)
    assert restored_root.raw_attributes[VENDOR_CASE] == case_id
    assert restored_root.raw_attributes["LineWidth"] == "1.25"
    assert type(restored_root.line_width) is float
    assert restored_root.line_width == 1.25


def test_cdxml_root_evidence_routes_only_marked_lifecycle_operations() -> None:
    case = ROOT_ELEMENT_CASES[0]
    node_id = cast(str, case["pytest_nodeid"])
    assertions = cast(list[str], case["assertions"])
    complete = {
        "dispatch": (node_id,),
        "mutation": (node_id,),
        "round_trip": (node_id,),
    }
    assert _element_operations("CDXML", case) == complete

    omitted_markers = {
        "exact_wrapper_type": {"dispatch"},
        "root_creation": {"dispatch", "mutation"},
        "root_mutation": {"mutation"},
        "element_round_trip": {"round_trip"},
    }
    for marker, omitted_operations in omitted_markers.items():
        incomplete = dict(case)
        incomplete["assertions"] = [item for item in assertions if item != marker]
        actual = _element_operations("CDXML", incomplete)
        assert set(actual) == set(complete)
        for operation, node_ids in complete.items():
            expected = () if operation in omitted_operations else node_ids
            assert actual[operation] == expected, (marker, operation)


def test_pinned_fixture_dispatches_every_current_generated_element_model() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    expected_tags = {element.xml_name for element in dtd.dtd_elements} | {"CDXML"}
    assert set(OBJECT_BY_XML_TAG) == expected_tags
    assert set(EXPECTED_MODEL_BY_TAG) == expected_tags
    for tag, model_name in EXPECTED_MODEL_BY_TAG.items():
        assert OBJECT_BY_XML_TAG[tag] is _model_class(model_name)


def test_unrelated_typed_edit_preserves_unknown_namespace_content_and_order() -> None:
    path = TEST_DIR.parent / "fixtures" / "full_schema" / "opaque_preservation.cdxml"
    document = CDXMLDocument.from_file(path)
    page = document.pages[0]
    altgroup_element = next(child for child in page.raw_element if child.tag == "altgroup")
    altgroup = document.wrap(altgroup_element)
    bracket = document.wrap(altgroup_element[0])
    node = document.find(Node)[0]

    expected_altgroup_type = OBJECT_BY_XML_TAG.get("altgroup", UnknownElement)
    assert type(altgroup) is expected_altgroup_type
    assert type(bracket) is UnknownElement
    assert bracket.xml_tag == "bracket"
    assert bracket.raw_attributes["{urn:vendor}marker"] == "undeclared-in-pinned-dtd"

    node.charge = -1
    assert node.raw_attributes["p"] == "001.250 02.500"
    assert node.raw_attributes["{urn:vendor}hint"] == "preserve-attribute"

    serialized = document.to_string()
    assert "keep comments, unknown nodes, and sibling order" in serialized
    assert '<v:opaque marker="preserve-element"' in serialized
    assert '<v:root-marker marker="preserve-root-child"' in serialized
    assert serialized.index("<altgroup") < serialized.index("<fragment")
    assert serialized.index('<n id="4"') < serialized.index("<v:opaque")
    assert serialized.index("<v:opaque") < serialized.index('<n id="5"')

    restored = CDXMLDocument.from_string(serialized)
    restored_node = restored.find(Node)[0]
    assert restored_node.charge == -1
    assert restored_node.raw_attributes["p"] == "001.250 02.500"
    restored_altgroup = next(
        restored.wrap(child) for child in restored.pages[0].raw_element if child.tag == "altgroup"
    )
    assert type(restored_altgroup) is expected_altgroup_type
    assert type(restored_altgroup.children[0]) is UnknownElement
    assert restored_altgroup.children[0].raw_attributes["{urn:vendor}marker"] == (
        "undeclared-in-pinned-dtd"
    )


def test_pinned_altgroup_bracket_child_is_preserved_as_undeclared_opaque_content() -> None:
    dtd = import_dtd(str(PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"))
    tags = {element.xml_name for element in dtd.dtd_elements}
    altgroup = next(element for element in dtd.dtd_elements if element.xml_name == "altgroup")
    assert "bracket" in altgroup.children
    assert "bracket" not in tags


ROOT_CREATION_TARGETS = {
    "page": ("collection", "pages"),
    "templategrid": ("collection", "template_grids"),
    "fonttable": ("method", "create_font_table"),
    "colortable": ("method", "create_color_table"),
}

CREATION_RECIPES: dict[str, dict[str, object]] = {
    "n": {"values": {"element": 6}},
    "b": {
        "precreate": (
            {"xml_name": "n", "bind": "begin", "values": {"element": 6}},
            {"xml_name": "n", "bind": "end", "values": {"element": 8}},
        ),
        "values": {"begin": {"ref": "begin"}, "end": {"ref": "end"}},
    },
    "t": {"children": ({"xml_name": "s", "values": {"content": "feature text"}},)},
    "s": {"values": {"content": "feature text"}},
    "graphic": {"values": {"graphic_type": GraphicType.RECTANGLE}},
    "scheme": {"children": ({"xml_name": "step", "values": {}},)},
    "fonttable": {
        "children": (
            {
                "xml_name": "font",
                "values": {"name": "Feature Font"},
            },
        )
    },
    "colortable": {
        "children": (
            {
                "xml_name": "color",
                "values": {"r": 0.25, "g": 0.5, "b": 0.75},
            },
        )
    },
    "font": {"values": {"name": "Feature Font"}},
    "color": {"values": {"r": 0.25, "g": 0.5, "b": 0.75}},
    "represent": {
        "precreate": (
            {
                "xml_name": "n",
                "bind": "represented_node",
                "values": {"element": 6},
                "parent": "fragment",
            },
        ),
        "values": {"attribute_id": 1, "object_reference": {"ref": "represented_node"}},
    },
    "sequence": {"values": {"sequence_identifier": "Feature Sequence"}},
    "crossreference": {
        "values": {
            "cross_reference_identifier": "Feature Reference",
            "cross_reference_sequence": "Feature Sequence",
        }
    },
    "regnum": {
        "values": {
            "registry_authority": "Feature Authority",
            "registry_number": "Feature Registry Number",
        }
    },
    "objecttag": {"values": {"name": "Feature Tag"}},
    "marker": {"values": {"name": "Feature Marker"}},
    "plasmidmarker": {"values": {"name": "Feature Marker"}},
    "border": {"values": {"side": Side.TOP}},
    "crossingbond": {
        "precreate": (
            {
                "xml_name": "n",
                "bind": "inner",
                "values": {"element": 6},
                "parent": "fragment",
            },
            {
                "xml_name": "n",
                "bind": "begin",
                "values": {"element": 6},
                "parent": "fragment",
            },
            {
                "xml_name": "n",
                "bind": "end",
                "values": {"element": 6},
                "parent": "fragment",
            },
            {
                "xml_name": "b",
                "bind": "bond",
                "values": {"begin": {"ref": "begin"}, "end": {"ref": "end"}},
                "parent": "fragment",
            },
        ),
        "values": {"bond_id": {"ref": "bond"}, "inner_atom_id": {"ref": "inner"}},
    },
}


def _source_contract_by_tag() -> dict[str, dict[str, object]]:
    rows = cast(list[dict[str, object]], SOURCE_CONTRACTS["elements"])
    return {cast(str, row["xml_name"]): row for row in rows}


SOURCE_CONTRACT_BY_TAG = _source_contract_by_tag()
SPEC_ID_BY_TAG = {metadata.xml_tag: spec_id for spec_id, metadata in OBJECT_METADATA.items()}


def _create_typed_child(
    parent: CDXMLDocument | CDXMLElement,
    xml_tag: str,
    values: dict[str, object],
) -> CDXMLElement:
    if isinstance(parent, CDXMLDocument):
        creator_kind, creator_name = ROOT_CREATION_TARGETS[xml_tag]
        if creator_kind == "collection":
            owner = parent if creator_name == "pages" else parent.root
            return cast(CDXMLElement, getattr(owner, creator_name).create(**values))
        return cast(CDXMLElement, getattr(parent, creator_name)())

    parent_spec_id = cast(str, type(parent).__spec_id__)
    child_spec_id = SPEC_ID_BY_TAG[xml_tag]
    child_metadata = next(
        child
        for child in OBJECT_METADATA[parent_spec_id].children
        if child.object_type == child_spec_id
    )
    collection = getattr(parent, child_metadata.collection_name)
    return cast(CDXMLElement, collection.create(**values))


def _recipe_values(
    recipe: dict[str, object], bindings: dict[str, CDXMLElement]
) -> dict[str, object]:
    values = cast(dict[str, object], recipe.get("values", {}))
    resolved: dict[str, object] = {}
    for name, value in values.items():
        if isinstance(value, dict) and set(value) == {"ref"}:
            resolved[name] = bindings[cast(str, value["ref"])]
        else:
            resolved[name] = value
    return resolved


def _create_with_recipe(
    parent: CDXMLDocument | CDXMLElement,
    xml_tag: str,
) -> CDXMLElement:
    recipe = CREATION_RECIPES.get(xml_tag, {})
    bindings: dict[str, CDXMLElement] = {}
    for requirement in cast(tuple[dict[str, object], ...], recipe.get("precreate", ())):
        precreate_parent = parent
        if requirement.get("parent") in {"page", "fragment"}:
            document = parent if isinstance(parent, CDXMLDocument) else parent.document
            if not document.pages:
                document.pages.create()
            page = document.pages[0]
            if requirement.get("parent") == "fragment":
                if not page.fragments:
                    page.fragments.create()
                precreate_parent = page.fragments[0]
            else:
                precreate_parent = page
        child = _create_with_values(
            precreate_parent,
            cast(str, requirement["xml_name"]),
            _recipe_values(requirement, bindings),
        )
        bindings[cast(str, requirement["bind"])] = child

    created = _create_typed_child(parent, xml_tag, _recipe_values(recipe, bindings))
    for required_child in cast(tuple[dict[str, object], ...], recipe.get("children", ())):
        _create_with_values(
            created,
            cast(str, required_child["xml_name"]),
            cast(dict[str, object], required_child["values"]),
        )
    return created


def _create_with_values(
    parent: CDXMLDocument | CDXMLElement,
    xml_tag: str,
    values: dict[str, object],
) -> CDXMLElement:
    created = _create_typed_child(parent, xml_tag, values)
    recipe = CREATION_RECIPES.get(xml_tag, {})
    for required_child in cast(tuple[dict[str, object], ...], recipe.get("children", ())):
        _create_with_values(
            created,
            cast(str, required_child["xml_name"]),
            cast(dict[str, object], required_child["values"]),
        )
    return created


def _create_from_source_route(document: CDXMLDocument, xml_tag: str) -> CDXMLElement:
    current: CDXMLDocument | CDXMLElement = document
    path = cast(list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["root_path"])
    for path_tag in path[1:]:
        current = _create_with_recipe(current, path_tag)
    return cast(CDXMLElement, current)


def _remove_from_parent(document: CDXMLDocument, value: CDXMLElement) -> None:
    parent = value.parent
    assert parent is not None
    if parent.xml_tag == "CDXML":
        child_spec_id = cast(str, type(value).__spec_id__)
        child_metadata = next(
            child
            for child in OBJECT_METADATA[cast(str, type(parent).__spec_id__)].children
            if child.object_type == child_spec_id
        )
        getattr(parent, child_metadata.collection_name).remove(value)
        return
    parent_spec_id = cast(str, type(parent).__spec_id__)
    child_spec_id = cast(str, type(value).__spec_id__)
    child_metadata = next(
        child
        for child in OBJECT_METADATA[parent_spec_id].children
        if child.object_type == child_spec_id
    )
    getattr(parent, child_metadata.collection_name).remove(value)


def _ensure_removal_preserves_minimum_children(
    document: CDXMLDocument, value: CDXMLElement
) -> tuple[CDXMLElement, ...]:
    parent = value.parent
    assert parent is not None
    xml_tag = value.xml_tag
    required_children = cast(
        dict[str, int], SOURCE_CONTRACT_BY_TAG[parent.xml_tag].get("minimum_child_counts", {})
    )
    minimum = required_children.get(xml_tag, 0)
    guards: list[CDXMLElement] = []
    count = sum(
        1 for child in parent.raw_element if isinstance(child.tag, str) and child.tag == xml_tag
    )
    while count <= minimum:
        guard = _create_with_recipe(parent, xml_tag)
        guard.raw_element.set("{urn:vendor}feature-guard", f"{parent.xml_tag}:{xml_tag}")
        required_attributes = cast(
            list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["required_attributes"]
        )
        assert set(required_attributes) <= set(guard.raw_attributes)
        assert all(
            guard.raw_attributes[name] == expected
            for name, expected in REMOVAL_GUARD_RAW_VALUE_ASSERTIONS.get(xml_tag, {}).items()
        )
        _assert_created_id_scope(document, guard)
        guards.append(guard)
        count += 1
    if minimum and not guards:
        existing_guard = next(
            document.wrap(child)
            for child in parent.raw_element
            if isinstance(child.tag, str)
            and child.tag == xml_tag
            and child is not value.raw_element
        )
        existing_guard.raw_element.set("{urn:vendor}feature-guard", f"{parent.xml_tag}:{xml_tag}")
        assert set(cast(list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["required_attributes"])) <= set(
            existing_guard.raw_attributes
        )
        assert all(
            existing_guard.raw_attributes[name] == expected
            for name, expected in REMOVAL_GUARD_RAW_VALUE_ASSERTIONS.get(xml_tag, {}).items()
        )
        _assert_created_id_scope(document, existing_guard)
        guards.append(existing_guard)
    return tuple(guards)


def _assert_created_id_scope(document: CDXMLDocument, value: CDXMLElement) -> None:
    metadata = OBJECT_METADATA[cast(str, type(value).__spec_id__)]
    assert metadata.id_scope == EXPECTED_ID_SCOPE_BY_TAG[value.xml_tag]
    id_properties = [prop for prop in metadata.properties.values() if prop.name == "id"]
    if metadata.id_scope == "none":
        assert not id_properties
        return
    assert len(id_properties) == 1
    object_id = getattr(value, id_properties[0].name)
    assert isinstance(object_id, int)
    if metadata.id_scope == "document":
        assert document.get(type(value), object_id) is value
    else:
        assert document.get(type(value), object_id) is None
        assert value.parent is not None
        assert value.parent.xml_tag == "fonttable"


def _element_case_id(case: dict[str, object]) -> str:
    return cast(str, case["case_id"])


CREATABLE_ELEMENT_CASES = tuple(
    case
    for case in ELEMENT_CASES
    if {"element_creation", "element_removal"} <= set(cast(list[str], case["assertions"]))
)


@pytest.mark.parametrize("case", CREATABLE_ELEMENT_CASES, ids=_element_case_id)
def test_element_create_remove_round_trip(case: dict[str, object]) -> None:
    xml_tag = cast(str, case["xml_name"])
    model_name = cast(str, case["expected_model"])
    expected_type = _model_class(model_name)
    case_id = cast(str, case["case_id"])
    nodeid = cast(str, case["pytest_nodeid"])
    assert nodeid.endswith(f"[{case_id}]")

    document = CDXMLDocument.from_string("<CDXML/>")
    created = _create_from_source_route(document, xml_tag)
    expected_parent_tag = cast(
        str,
        cast(list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["root_path"])[-2],
    )
    created.raw_element.set("{urn:vendor}feature-case", case_id)
    assert type(created) is expected_type
    assert created.parent is not None
    assert created.parent.xml_tag == expected_parent_tag
    required_attributes = cast(list[str], SOURCE_CONTRACT_BY_TAG[xml_tag]["required_attributes"])
    assert set(required_attributes) <= set(created.raw_attributes)
    _assert_created_id_scope(document, created)

    serialized = document.to_string()
    restored = CDXMLDocument.from_string(serialized)
    matches = [
        restored.wrap(element)
        for element in restored.tree.iter()
        if isinstance(element.tag, str) and element.get("{urn:vendor}feature-case") == case_id
    ]
    assert len(matches) == 1
    restored_target = matches[0]
    assert type(restored_target) is expected_type
    assert restored_target.xml_tag == xml_tag
    assert restored_target.parent is not None
    assert restored_target.parent.xml_tag == expected_parent_tag
    assert set(required_attributes) <= set(restored_target.raw_attributes)
    _assert_created_id_scope(restored, restored_target)

    parent = restored_target.parent
    assert parent is not None
    guards = _ensure_removal_preserves_minimum_children(restored, restored_target)
    children_before_removal = list(parent.raw_element)
    _remove_from_parent(restored, restored_target)
    assert list(parent.raw_element) == [
        child for child in children_before_removal if child is not restored_target.raw_element
    ]
    for guard in guards:
        assert guard.raw_element.getparent() is parent.raw_element

    assert not any(
        isinstance(element.tag, str) and element.get("{urn:vendor}feature-case") == case_id
        for element in restored.tree.iter()
    )
    after_removal = CDXMLDocument.from_string(restored.to_string())
    assert not any(
        isinstance(element.tag, str) and element.get("{urn:vendor}feature-case") == case_id
        for element in after_removal.tree.iter()
    )
    for guard in guards:
        marker = guard.raw_attributes["{urn:vendor}feature-guard"]
        restored_guard = next(
            after_removal.wrap(element)
            for element in after_removal.tree.iter()
            if isinstance(element.tag, str) and element.get("{urn:vendor}feature-guard") == marker
        )
        assert type(restored_guard) is expected_type
        assert set(required_attributes) <= set(restored_guard.raw_attributes)
        assert all(
            restored_guard.raw_attributes[name] == expected
            for name, expected in REMOVAL_GUARD_RAW_VALUE_ASSERTIONS.get(xml_tag, {}).items()
        )
        _assert_created_id_scope(after_removal, restored_guard)
