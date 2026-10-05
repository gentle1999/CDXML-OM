"""Codecs for flattened point arrays and CDX list datatype families."""

from __future__ import annotations

import math
import re
from typing import cast

from cdxml_om._generated.schema_metadata import PropertyMetadata
from cdxml_om.core.errors import CodecError
from cdxml_om.core.geometry import Point2D, Point3D
from cdxml_om.core.values import ElementList, GenericList

_UINT16_MAX = (1 << 16) - 1
_XML_WHITESPACE = " \t\r\n"
_XML_WHITESPACE_RUN = re.compile(r"[ \t\r\n]+")
_UNSIGNED_INTEGER = re.compile(r"[0-9]+\Z")
_DECIMAL_NUMBER = re.compile(r"[+-]?(?:(?:[0-9]+(?:\.[0-9]*)?)|(?:\.[0-9]+))(?:[eE][+-]?[0-9]+)?\Z")


def _decode_error(
    property_id: str,
    raw_value: str,
    prop: PropertyMetadata,
    reason: str,
) -> CodecError:
    return CodecError(
        f"cannot decode {property_id} ({prop.name}) value {raw_value!r}: {reason}",
        property_id=property_id,
        raw_value=raw_value,
    )


def _encode_error(
    property_id: str,
    prop: PropertyMetadata,
    reason: str,
) -> CodecError:
    return CodecError(
        f"cannot encode {property_id} ({prop.name}): {reason}",
        property_id=property_id,
    )


def _valid_xml_10_text(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return all(
        ord(character) in {0x9, 0xA, 0xD}
        or 0x20 <= ord(character) <= 0xD7FF
        or 0xE000 <= ord(character) <= 0xFFFD
        or 0x10000 <= ord(character) <= 0x10FFFF
        for character in value
    )


def _check_xml_text_for_decode(
    raw_value: str,
    property_id: str,
    prop: PropertyMetadata,
) -> None:
    if not _valid_xml_10_text(raw_value):
        raise _decode_error(
            property_id, raw_value, prop, "contains a character not allowed in XML 1.0"
        )


def _check_xml_text_for_encode(
    value: str,
    property_id: str,
    prop: PropertyMetadata,
) -> None:
    if not _valid_xml_10_text(value):
        raise _encode_error(property_id, prop, "contains a character not allowed in XML 1.0")


def _parse_uint16(
    token: str,
    raw_value: str,
    property_id: str,
    prop: PropertyMetadata,
) -> int:
    if _UNSIGNED_INTEGER.fullmatch(token) is None:
        raise _decode_error(
            property_id, raw_value, prop, f"expected an unsigned integer, got {token!r}"
        )
    try:
        value = int(token)
    except ValueError as exc:
        raise _decode_error(
            property_id, raw_value, prop, "integer token exceeds supported conversion limits"
        ) from exc
    if value > _UINT16_MAX:
        raise _decode_error(property_id, raw_value, prop, f"value is above {_UINT16_MAX}")
    return value


def _format_uint16(value: object, property_id: str, prop: PropertyMetadata) -> str:
    if isinstance(value, bool) or not isinstance(value, int):
        raise _encode_error(property_id, prop, "values must be integers")
    if value < 0:
        raise _encode_error(property_id, prop, "value is below 0")
    if value > _UINT16_MAX:
        raise _encode_error(property_id, prop, f"value is above {_UINT16_MAX}")
    return str(value)


def _parse_finite_number(
    token: str,
    raw_value: str,
    property_id: str,
    prop: PropertyMetadata,
) -> float:
    if _DECIMAL_NUMBER.fullmatch(token) is None:
        raise _decode_error(
            property_id, raw_value, prop, f"expected a decimal number, got {token!r}"
        )
    try:
        value = float(token)
    except (OverflowError, ValueError) as exc:
        raise _decode_error(
            property_id, raw_value, prop, "number is outside the finite float range"
        ) from exc
    if not math.isfinite(value):
        raise _decode_error(property_id, raw_value, prop, "coordinate values must be finite")
    return value


def _format_finite_number(
    value: object,
    property_id: str,
    prop: PropertyMetadata,
) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise _encode_error(property_id, prop, "coordinates must be numbers")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise _encode_error(
            property_id, prop, "coordinate is outside the finite float range"
        ) from exc
    if not math.isfinite(number):
        raise _encode_error(property_id, prop, "coordinate values must be finite")
    return repr(number)


def _list_tokens(
    raw_value: str,
    property_id: str,
    prop: PropertyMetadata,
) -> list[str]:
    _check_xml_text_for_decode(raw_value, property_id, prop)
    # No source declares that a zero-length list is invalid. Treat an empty
    # attribute as a zero-item collection; omission is still represented separately.
    stripped = raw_value.strip(_XML_WHITESPACE)
    if not stripped:
        return []
    return _XML_WHITESPACE_RUN.split(stripped)


class CurvePoints2DCodec:
    """Decode CDXCurvePoints as flat, whitespace-separated X/Y components."""

    def parse_xml(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
    ) -> tuple[Point2D, ...]:
        tokens = _list_tokens(raw_value, property_id, prop)
        if len(tokens) % 2 != 0:
            raise _decode_error(
                property_id, raw_value, prop, "expected an even number of 2D components"
            )
        values = [_parse_finite_number(token, raw_value, property_id, prop) for token in tokens]
        return tuple(
            Point2D(values[index], values[index + 1]) for index in range(0, len(values), 2)
        )

    def format_xml(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
    ) -> str:
        if not isinstance(value, tuple):
            raise _encode_error(property_id, prop, "expected a tuple of Point2D values")
        points = cast(tuple[object, ...], value)
        encoded: list[str] = []
        for point in points:
            if not isinstance(point, Point2D):
                raise _encode_error(property_id, prop, "expected only Point2D values")
            encoded.append(_format_finite_number(point.x, property_id, prop))
            encoded.append(_format_finite_number(point.y, property_id, prop))
        result = " ".join(encoded)
        _check_xml_text_for_encode(result, property_id, prop)
        return result


class CurvePoints3DCodec:
    """Decode CDXCurvePoints3D as flat X/Y/Z component triples."""

    def parse_xml(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
    ) -> tuple[Point3D, ...]:
        tokens = _list_tokens(raw_value, property_id, prop)
        if len(tokens) % 3 != 0:
            raise _decode_error(
                property_id, raw_value, prop, "expected a multiple of three 3D components"
            )
        values = [_parse_finite_number(token, raw_value, property_id, prop) for token in tokens]
        return tuple(
            Point3D(values[index], values[index + 1], values[index + 2])
            for index in range(0, len(values), 3)
        )

    def format_xml(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
    ) -> str:
        if not isinstance(value, tuple):
            raise _encode_error(property_id, prop, "expected a tuple of Point3D values")
        points = cast(tuple[object, ...], value)
        encoded: list[str] = []
        for point in points:
            if not isinstance(point, Point3D):
                raise _encode_error(property_id, prop, "expected only Point3D values")
            encoded.extend(
                (
                    _format_finite_number(point.x, property_id, prop),
                    _format_finite_number(point.y, property_id, prop),
                    _format_finite_number(point.z, property_id, prop),
                )
            )
        result = " ".join(encoded)
        _check_xml_text_for_encode(result, property_id, prop)
        return result


class UInt16ListCodec:
    """Decode a nonempty whitespace-separated CDXML UINT16 value series."""

    def parse_xml(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
    ) -> tuple[int, ...]:
        tokens = _list_tokens(raw_value, property_id, prop)
        return tuple(_parse_uint16(token, raw_value, property_id, prop) for token in tokens)

    def format_xml(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
    ) -> str:
        if not isinstance(value, tuple):
            raise _encode_error(property_id, prop, "expected a tuple of UINT16 values")
        items = cast(tuple[object, ...], value)
        result = " ".join(_format_uint16(item, property_id, prop) for item in items)
        _check_xml_text_for_encode(result, property_id, prop)
        return result


class ElementListCodec:
    """Decode UINT16 element values with the CDXML ``NOT`` list prefix."""

    def parse_xml(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
    ) -> ElementList:
        tokens = _list_tokens(raw_value, property_id, prop)
        negated = bool(tokens and tokens[0] == "NOT")
        elements = tokens[1:] if negated else tokens
        if negated and not elements:
            raise _decode_error(
                property_id, raw_value, prop, "NOT must be followed by element values"
            )
        parsed = tuple(_parse_uint16(token, raw_value, property_id, prop) for token in elements)
        return ElementList(parsed, negated=negated)

    def format_xml(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
    ) -> str:
        if not isinstance(value, ElementList):
            raise _encode_error(property_id, prop, "expected ElementList")
        raw_elements: object = getattr(value, "elements", None)
        raw_negated: object = getattr(value, "negated", None)
        if not isinstance(raw_elements, tuple):
            raise _encode_error(property_id, prop, "elements must be a tuple")
        if not isinstance(raw_negated, bool):
            raise _encode_error(property_id, prop, "negated must be bool")
        elements = cast(tuple[object, ...], raw_elements)
        negated = raw_negated
        if not elements and negated:
            raise _encode_error(property_id, prop, "NOT must be followed by element values")
        parts = [_format_uint16(item, property_id, prop) for item in elements]
        result = ("NOT " if negated else "") + " ".join(parts)
        _check_xml_text_for_encode(result, property_id, prop)
        return result


class GenericListCodec:
    """Decode a whitespace-separated string series with an optional ``NOT``."""

    def parse_xml(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
    ) -> GenericList:
        tokens = _list_tokens(raw_value, property_id, prop)
        negated = bool(tokens and tokens[0] == "NOT")
        values = tokens[1:] if negated else tokens
        if negated and not values:
            raise _decode_error(property_id, raw_value, prop, "NOT must be followed by list values")
        return GenericList(tuple(values), negated=negated)

    def format_xml(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
    ) -> str:
        if not isinstance(value, GenericList):
            raise _encode_error(property_id, prop, "expected GenericList")
        raw_values: object = getattr(value, "values", None)
        raw_negated: object = getattr(value, "negated", None)
        if not isinstance(raw_values, tuple):
            raise _encode_error(property_id, prop, "values must be a tuple")
        if not isinstance(raw_negated, bool):
            raise _encode_error(property_id, prop, "negated must be bool")
        values = cast(tuple[object, ...], raw_values)
        negated = raw_negated
        if not values and negated:
            raise _encode_error(property_id, prop, "NOT must be followed by list values")
        string_values: list[str] = []
        for item in values:
            if not isinstance(item, str) or not item:
                raise _encode_error(
                    property_id, prop, "generic list values must be non-empty strings"
                )
            if any(character in _XML_WHITESPACE for character in item):
                raise _encode_error(
                    property_id,
                    prop,
                    "generic list values cannot contain whitespace separators",
                )
            _check_xml_text_for_encode(item, property_id, prop)
            string_values.append(item)
        if not negated and string_values and string_values[0] == "NOT":
            raise _encode_error(
                property_id,
                prop,
                "a non-negated list cannot start with the reserved NOT prefix",
            )
        result = ("NOT " if negated else "") + " ".join(string_values)
        _check_xml_text_for_encode(result, property_id, prop)
        return result


__all__ = [
    "CurvePoints2DCodec",
    "CurvePoints3DCodec",
    "ElementListCodec",
    "GenericListCodec",
    "UInt16ListCodec",
]
