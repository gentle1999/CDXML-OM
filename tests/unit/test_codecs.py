import math
from dataclasses import replace

import pytest

import cdxml_om.core.codecs as codecs
from cdxml_om import BondDisplay, BondOrder
from cdxml_om._generated.schema_metadata import DATATYPE_METADATA, PROPERTY_METADATA
from cdxml_om.core.errors import CodecError
from cdxml_om.core.geometry import BoundingBox, Point2D, Point3D

BASE_PROPERTY = PROPERTY_METADATA["node.element"]


def custom_property(
    codec_name: str,
    *,
    datatype: str = "integer",
    enum: str | None = None,
):
    return replace(BASE_PROPERTY, codec=codec_name, datatype=datatype, enum=enum)


def parse(codec_name: str, raw_value: str, prop: object) -> object:
    return codecs._CODECS[codec_name].parse_xml(raw_value, "test.value", prop)  # type: ignore[arg-type]


def format_value(codec_name: str, value: object, prop: object) -> str:
    return codecs._CODECS[codec_name].format_xml(value, "test.value", prop)  # type: ignore[arg-type]


@pytest.fixture
def bounded_float_property(monkeypatch: pytest.MonkeyPatch):
    datatypes = dict(DATATYPE_METADATA)
    datatypes["test_float"] = replace(
        DATATYPE_METADATA["integer"],
        codec="float",
        minimum=-10.0,
        maximum=10.0,
    )
    monkeypatch.setattr(codecs, "DATATYPE_METADATA", datatypes)
    return custom_property("float", datatype="test_float")


def test_string_codec_preserves_text_and_requires_strings() -> None:
    prop = custom_property("string", datatype="string")

    assert parse("string", "  C1 & C2  ", prop) == "  C1 & C2  "
    assert format_value("string", "  C1 & C2  ", prop) == "  C1 & C2  "
    with pytest.raises(CodecError):
        format_value("string", 12, prop)


def test_integer_codec_parses_formats_and_rejects_bool() -> None:
    prop = custom_property("integer")

    assert parse("integer", "-42", prop) == -42
    assert format_value("integer", -42, prop) == "-42"
    with pytest.raises(CodecError) as error:
        parse("integer", "forty-two", prop)
    assert error.value.property_id == "test.value"
    assert error.value.raw_value == "forty-two"
    with pytest.raises(CodecError):
        format_value("integer", True, prop)


def test_float_codec_preserves_precision_and_checks_finite_bounds(
    bounded_float_property,
) -> None:
    prop = bounded_float_property
    codec = codecs._CODECS["float"]
    value = float("1.2345678901234567")

    assert codec.parse_xml("-10", "test.float", prop) == -10.0
    assert codec.parse_xml("10", "test.float", prop) == 10.0
    encoded = codec.format_xml(value, "test.float", prop)
    assert encoded == repr(value)
    assert codec.parse_xml(encoded, "test.float", prop) == value
    assert codec.format_xml(1, "test.float", prop) == "1.0"

    for raw in ("10.1", "-10.1", "nan", "inf", "-inf"):
        with pytest.raises(CodecError):
            codec.parse_xml(raw, "test.float", prop)
    for bad_value in (10.1, -10.1, math.nan, math.inf, -math.inf, True):
        with pytest.raises(CodecError):
            codec.format_xml(bad_value, "test.float", prop)


def test_boolean_codec_accepts_xml_spellings_and_writes_canonical_values() -> None:
    prop = custom_property("bool")
    codec = codecs._CODECS["bool"]

    for raw in ("yes", "TRUE", " 1 "):
        assert codec.parse_xml(raw, "test.bool", prop) is True
    for raw in ("no", "False", " 0 "):
        assert codec.parse_xml(raw, "test.bool", prop) is False
    assert codec.format_xml(True, "test.bool", prop) == "yes"
    assert codec.format_xml(False, "test.bool", prop) == "no"
    with pytest.raises(CodecError) as error:
        codec.parse_xml("maybe", "test.bool", prop)
    assert error.value.raw_value == "maybe"
    with pytest.raises(CodecError):
        codec.format_xml(1, "test.bool", prop)


def test_object_ids_enforce_uint32_boundaries_and_bool_is_not_an_id() -> None:
    property_id = "common.id"
    maximum = 2**32 - 1

    assert codecs.decode_property_value(property_id, "0") == 0
    assert codecs.decode_property_value(property_id, str(maximum)) == maximum
    assert codecs.encode_property_value(property_id, 0) == "0"
    assert codecs.encode_property_value(property_id, maximum) == str(maximum)
    for raw in ("-1", str(maximum + 1)):
        with pytest.raises(CodecError) as error:
            codecs.decode_property_value(property_id, raw)
        assert error.value.property_id == property_id
        assert error.value.raw_value == raw
    for value in (True, -1, maximum + 1):
        with pytest.raises(CodecError):
            codecs.encode_property_value(property_id, value)


def test_object_id_list_parses_whitespace_and_checks_each_uint32_value() -> None:
    prop = custom_property("object_id_list", datatype="object_id")
    codec = codecs._CODECS["object_id_list"]
    maximum = 2**32 - 1

    assert codec.parse_xml("", "test.ids", prop) == ()
    assert codec.parse_xml(" \t\n ", "test.ids", prop) == ()
    values = (0, 12, maximum)
    assert codec.parse_xml("\t0 12\n4294967295 ", "test.ids", prop) == values
    assert codec.format_xml(values, "test.ids", prop) == "0 12 4294967295"
    assert codec.format_xml((), "test.ids", prop) == ""

    for raw in ("1 nope", "-1", str(maximum + 1)):
        with pytest.raises(CodecError):
            codec.parse_xml(raw, "test.ids", prop)
    for value in ([1, 2], (True,), (-1,), (maximum + 1,)):
        with pytest.raises(CodecError):
            codec.format_xml(value, "test.ids", prop)


def test_integer_enum_codec_uses_exact_type_and_xml_values() -> None:
    assert codecs.decode_property_value("bond.display", "WedgedHashEnd") is (
        BondDisplay.WEDGED_HASH_END
    )
    assert codecs.encode_property_value("bond.display", BondDisplay.SOLID) == "Solid"

    with pytest.raises(CodecError) as error:
        codecs.decode_property_value("bond.display", "wedgedHashEnd")
    assert error.value.property_id == "bond.display"
    assert error.value.raw_value == "wedgedHashEnd"
    with pytest.raises(CodecError):
        codecs.encode_property_value("bond.display", BondOrder.SINGLE)


def test_intflag_uses_xml_triple_value_and_formats_combined_flags_lexically() -> None:
    triple = codecs.decode_property_value("bond.order", "3")
    assert triple is BondOrder.TRIPLE
    assert triple.value == 4
    assert codecs.encode_property_value("bond.order", BondOrder.TRIPLE) == "3"

    combined = codecs.decode_property_value("bond.order", "2 1")
    assert combined == BondOrder.SINGLE | BondOrder.DOUBLE
    assert codecs.encode_property_value("bond.order", combined) == "1 2"
    documented_values = {
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
    for lexical, expected in documented_values.items():
        decoded = codecs.decode_property_value("bond.order", lexical)
        assert decoded is expected
        assert codecs.encode_property_value("bond.order", expected) == lexical
    with pytest.raises(CodecError):
        codecs.decode_property_value("bond.order", "7")
    with pytest.raises(CodecError):
        codecs.encode_property_value("bond.order", BondOrder(0x10000))


def test_point2d_parse_format_precision_and_bad_dynamic_values() -> None:
    parsed = codecs.decode_property_value("node.position", "0.1, -2.25")
    assert parsed == Point2D(0.1, -2.25)
    assert codecs.encode_property_value("node.position", parsed) == "0.1 -2.25"

    bad = Point2D("bad", 2)  # type: ignore[arg-type]
    with pytest.raises(CodecError):
        codecs.encode_property_value("node.position", bad)
    with pytest.raises(CodecError):
        codecs.encode_property_value("node.position", Point2D(math.inf, 0))
    for raw in ("1", "1 2 3", "bad 2", "nan 2", "inf 2"):
        with pytest.raises(CodecError):
            codecs.decode_property_value("node.position", raw)


def test_point3d_requires_three_xml_coordinates() -> None:
    prop = custom_property("point_3d", datatype="point_3d")
    codec = codecs._CODECS["point_3d"]
    value = codec.parse_xml("1, 0.3333333333333333, -5", "test.point3d", prop)

    assert value == Point3D(1.0, 0.3333333333333333, -5.0)
    assert codec.format_xml(value, "test.point3d", prop) == "1.0 0.3333333333333333 -5.0"
    with pytest.raises(CodecError):
        codec.parse_xml("1 2 3 4", "test.point3d", prop)
    with pytest.raises(CodecError):
        codec.format_xml(Point2D(1, 2), "test.point3d", prop)


def test_bounding_box_requires_four_xml_coordinates() -> None:
    prop = custom_property("bounding_box", datatype="bounding_box")
    codec = codecs._CODECS["bounding_box"]
    value = codec.parse_xml("10 20 30 40", "test.bbox", prop)

    assert value == BoundingBox(10.0, 20.0, 30.0, 40.0)
    assert codec.format_xml(value, "test.bbox", prop) == "10.0 20.0 30.0 40.0"
    with pytest.raises(CodecError):
        codec.parse_xml("10 20 30", "test.bbox", prop)
    with pytest.raises(CodecError):
        codec.parse_xml("10 20 30 40 50", "test.bbox", prop)
    with pytest.raises(CodecError):
        codec.parse_xml("10 20 inf 40", "test.bbox", prop)
