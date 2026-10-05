"""Independent source-vector tests for CDXML irregular list and curve codecs."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from typing import cast

import pytest

from cdxml_om._generated.schema_metadata import PROPERTY_METADATA, PropertyMetadata
from cdxml_om.core.errors import CodecError
from cdxml_om.core.geometry import Point2D, Point3D
from cdxml_om.core.irregular_codecs import (
    CurvePoints2DCodec,
    CurvePoints3DCodec,
    ElementListCodec,
    GenericListCodec,
    UInt16ListCodec,
)
from cdxml_om.core.values import ElementList, GenericList

_PROPERTY = PROPERTY_METADATA["node.element"]


def _property(name: str) -> PropertyMetadata:
    return replace(_PROPERTY, name=name)


def test_element_and_generic_list_values_are_frozen_and_slotted() -> None:
    element_list = ElementList((9, 17, 35), negated=True)
    generic_list = GenericList(("R", "X", "A"), negated=True)

    assert element_list.elements == (9, 17, 35)
    assert generic_list.values == ("R", "X", "A")
    assert not hasattr(element_list, "__dict__")
    assert not hasattr(generic_list, "__dict__")
    with pytest.raises(FrozenInstanceError):
        element_list.negated = False  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        generic_list.negated = False  # type: ignore[misc]


def test_curve_points_2d_use_flat_xml_components_not_binary_count_prefix() -> None:
    # SDK CDXCurvePoints example: CDXML "1 2 3 4"; the binary UINT16 count is
    # a CDX-only prefix. See focused-properties.json source sdk_curve_points.
    codec = CurvePoints2DCodec()
    prop = _property("CurvePoints")
    parsed = codec.parse_xml("1 2 3 4", "curve.CurvePoints", prop)

    assert parsed == (Point2D(1.0, 2.0), Point2D(3.0, 4.0))
    encoded = codec.format_xml(parsed, "curve.CurvePoints", prop)
    assert encoded == "1.0 2.0 3.0 4.0"
    assert codec.parse_xml(encoded, "curve.CurvePoints", prop) == parsed


def test_curve_points_3d_use_flat_xml_components_not_binary_count_prefix() -> None:
    # SDK CDXCurvePoints3D example: CDXML "1 2 3 4 5 6"; no count appears in XML.
    codec = CurvePoints3DCodec()
    prop = _property("CurvePoints3D")
    parsed = codec.parse_xml("1 2 3 4 5 6", "curve.CurvePoints3D", prop)

    assert parsed == (Point3D(1.0, 2.0, 3.0), Point3D(4.0, 5.0, 6.0))
    encoded = codec.format_xml(parsed, "curve.CurvePoints3D", prop)
    assert encoded == "1.0 2.0 3.0 4.0 5.0 6.0"
    assert codec.parse_xml(encoded, "curve.CurvePoints3D", prop) == parsed


@pytest.mark.parametrize(
    "raw_value",
    ["1", "1 2 3", "1 2 3 4 5", "1 nan", "1 inf", "1 nope"],
)
def test_curve_points_2d_reject_malformed_and_nonfinite_arrays(raw_value: str) -> None:
    with pytest.raises(CodecError) as raised:
        CurvePoints2DCodec().parse_xml(raw_value, "curve.CurvePoints", _property("CurvePoints"))
    assert raised.value.property_id == "curve.CurvePoints"
    assert raised.value.raw_value == raw_value


@pytest.mark.parametrize("raw_value", ["1 2", "1 2 3 4", "1 2 3 4 5", "1 2 NaN"])
def test_curve_points_3d_reject_incomplete_or_nonfinite_arrays(raw_value: str) -> None:
    with pytest.raises(CodecError):
        CurvePoints3DCodec().parse_xml(raw_value, "curve.CurvePoints3D", _property("CurvePoints3D"))


def test_curve_point_formatting_rejects_wrong_dimensions_and_dynamic_bad_values() -> None:
    codec_2d = CurvePoints2DCodec()
    codec_3d = CurvePoints3DCodec()
    with pytest.raises(CodecError):
        codec_2d.format_xml((Point3D(1, 2, 3),), "curve.points", _property("CurvePoints"))
    with pytest.raises(CodecError):
        codec_3d.format_xml((Point2D(1, 2),), "curve.points3d", _property("CurvePoints3D"))
    with pytest.raises(CodecError):
        codec_2d.format_xml((Point2D(float("inf"), 0),), "curve.points", _property("CurvePoints"))
    with pytest.raises(CodecError):
        codec_2d.format_xml((Point2D(True, 0),), "curve.points", _property("CurvePoints"))
    with pytest.raises(CodecError):
        codec_3d.format_xml(
            (Point3D(1, 2, 3), Point2D(4, 5)), "curve.points3d", _property("CurvePoints3D")
        )


def test_uint16_list_boundaries_and_whitespace_round_trip() -> None:
    # SDK INT16ListWithCounts describes the count as CDX-only; XML is a flat
    # UINT16 value list. See focused-properties.json source sdk_int16_list_with_counts.
    codec = UInt16ListCodec()
    prop = _property("LineStarts")
    maximum = (1 << 16) - 1
    parsed = codec.parse_xml("\t0 12\n65535 ", "text.LineStarts", prop)

    assert parsed == (0, 12, maximum)
    assert codec.format_xml(parsed, "text.LineStarts", prop) == "0 12 65535"
    assert (
        codec.parse_xml(codec.format_xml(parsed, "text.LineStarts", prop), "text.LineStarts", prop)
        == parsed
    )


@pytest.mark.parametrize("raw_value", ["-1", "+1", "65536", "1_0", "0x10", "1 nope"])
def test_uint16_list_rejects_signed_nondecimal_and_out_of_range_values(
    raw_value: str,
) -> None:
    with pytest.raises(CodecError):
        UInt16ListCodec().parse_xml(raw_value, "text.LineStarts", _property("LineStarts"))


def test_uint16_list_rejects_integer_tokens_over_python_conversion_limit() -> None:
    with pytest.raises(CodecError):
        UInt16ListCodec().parse_xml("9" * 5000, "text.LineStarts", _property("LineStarts"))


@pytest.mark.parametrize("value", [[], (True,), (-1,), (65536,), (1, "2")])
def test_uint16_list_formatter_checks_container_and_each_uint16(value: object) -> None:
    with pytest.raises(CodecError):
        UInt16ListCodec().format_xml(value, "text.LineStarts", _property("LineStarts"))


def test_element_list_handles_optional_not_prefix_and_round_trips_values() -> None:
    # SDK CDXElementList examples include "9 17 35" and "NOT 9 17 35".
    codec = ElementListCodec()
    prop = _property("ElementList")

    ordinary = codec.parse_xml("9 17 35", "node.ElementList", prop)
    negated = codec.parse_xml("NOT 9 17 35", "node.ElementList", prop)
    assert ordinary == ElementList((9, 17, 35))
    assert negated == ElementList((9, 17, 35), negated=True)
    assert codec.format_xml(ordinary, "node.ElementList", prop) == "9 17 35"
    assert codec.format_xml(negated, "node.ElementList", prop) == "NOT 9 17 35"
    assert (
        codec.parse_xml(
            codec.format_xml(negated, "node.ElementList", prop), "node.ElementList", prop
        )
        == negated
    )


@pytest.mark.parametrize("raw_value", ["NOT", "not 9", "NOT -1", "NOT 65536", "9 xx"])
def test_element_list_rejects_invalid_prefix_and_bad_uint16_values(raw_value: str) -> None:
    with pytest.raises(CodecError):
        ElementListCodec().parse_xml(raw_value, "node.ElementList", _property("ElementList"))


@pytest.mark.parametrize(
    "value",
    [
        [],
        ElementList((True,)),
        ElementList((-1,)),
        ElementList((65536,)),
        ElementList((1,), negated=cast(bool, 1)),
        ElementList((), negated=True),
    ],
)
def test_element_list_formatter_rejects_invalid_container_and_values(value: object) -> None:
    with pytest.raises(CodecError):
        ElementListCodec().format_xml(value, "node.ElementList", _property("ElementList"))


def test_generic_list_handles_optional_not_prefix_without_chemistry_interpretation() -> None:
    # SDK CDXGenericList examples treat the XML series as string tokens and use
    # a leading NOT for its negated form; the codec assigns no chemistry meaning.
    codec = GenericListCodec()
    prop = _property("GenericList")

    ordinary = codec.parse_xml("R X A", "node.GenericList", prop)
    negated = codec.parse_xml("NOT R X A", "node.GenericList", prop)
    assert ordinary == GenericList(("R", "X", "A"))
    assert negated == GenericList(("R", "X", "A"), negated=True)
    assert codec.format_xml(ordinary, "node.GenericList", prop) == "R X A"
    assert codec.format_xml(negated, "node.GenericList", prop) == "NOT R X A"
    assert (
        codec.parse_xml(
            codec.format_xml(negated, "node.GenericList", prop), "node.GenericList", prop
        )
        == negated
    )


def test_generic_list_splits_only_on_xml_whitespace() -> None:
    codec = GenericListCodec()
    prop = _property("GenericList")
    value = "R\u00a0X"

    parsed = codec.parse_xml(value, "node.GenericList", prop)

    assert parsed == GenericList((value,))
    assert codec.format_xml(parsed, "node.GenericList", prop) == value


@pytest.mark.parametrize("raw_value", ["NOT", "R\x00X", "R\x01X", "R \ud800 X"])
def test_generic_list_rejects_not_only_and_non_xml_text(raw_value: str) -> None:
    with pytest.raises(CodecError):
        GenericListCodec().parse_xml(raw_value, "node.GenericList", _property("GenericList"))


@pytest.mark.parametrize(
    "value",
    [
        GenericList(("R X",)),
        GenericList(("R", "")),
        GenericList(("R\x00",)),
        GenericList(("NOT",), negated=False),
        GenericList(("R",), negated=cast(bool, 1)),
        GenericList((), negated=True),
        ("R", "X"),
    ],
)
def test_generic_list_formatter_rejects_ambiguous_or_invalid_tokens(value: object) -> None:
    with pytest.raises(CodecError):
        GenericListCodec().format_xml(value, "node.GenericList", _property("GenericList"))


def test_empty_xml_lists_map_to_empty_values_and_format_back_as_empty() -> None:
    """No source forbids zero-item lists; empty attributes remain distinct from omission."""
    property_by_name = {
        "CurvePoints": (CurvePoints2DCodec(), ()),
        "CurvePoints3D": (CurvePoints3DCodec(), ()),
        "LineStarts": (UInt16ListCodec(), ()),
        "ElementList": (ElementListCodec(), ElementList(())),
        "GenericList": (GenericListCodec(), GenericList(())),
    }
    for name, (codec, expected) in property_by_name.items():
        prop = _property(name)
        parsed = codec.parse_xml("", f"test.{name}", prop)
        assert parsed == expected
        assert codec.format_xml(parsed, f"test.{name}", prop) == ""
