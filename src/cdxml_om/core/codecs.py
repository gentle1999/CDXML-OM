"""Metadata-driven codecs for lazily read CDXML attribute values."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Protocol, TypeVar, cast

from cdxml_om._generated import enums as generated_enums
from cdxml_om._generated.schema_metadata import (
    DATATYPE_METADATA,
    ENUM_METADATA,
    PROPERTY_METADATA,
    EnumMetadata,
    PropertyMetadata,
)
from cdxml_om.core.errors import CodecError
from cdxml_om.core.geometry import BoundingBox, Point2D, Point3D
from cdxml_om.core.irregular_codecs import (
    CurvePoints2DCodec,
    CurvePoints3DCodec,
    ElementListCodec,
    GenericListCodec,
    UInt16ListCodec,
)

T = TypeVar("T")


class Codec(Protocol[T]):
    """A typed XML codec for one metadata-selected value family."""

    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> T: ...

    def format_xml(self, value: T, property_id: str, prop: PropertyMetadata) -> str: ...


def _error(property_id: str, raw_value: str, prop: PropertyMetadata, reason: str) -> CodecError:
    return CodecError(
        f"cannot decode {property_id} ({prop.name}) value {raw_value!r}: {reason}",
        property_id=property_id,
        raw_value=raw_value,
    )


def _format_error(property_id: str, prop: PropertyMetadata, reason: str) -> CodecError:
    return CodecError(
        f"cannot encode {property_id} ({prop.name}): {reason}",
        property_id=property_id,
    )


def _validate_xml_text(value: str, property_id: str, prop: PropertyMetadata) -> str:
    """Reject strings libxml cannot safely serialize as XML 1.0 text."""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise _format_error(property_id, prop, "string is not UTF-8 encodable") from exc

    for character in value:
        codepoint = ord(character)
        valid = (
            codepoint in {0x9, 0xA, 0xD}
            or 0x20 <= codepoint <= 0xD7FF
            or 0xE000 <= codepoint <= 0xFFFD
            or 0x10000 <= codepoint <= 0x10FFFF
        )
        if not valid:
            raise _format_error(
                property_id,
                prop,
                f"character U+{codepoint:04X} is not permitted in XML 1.0",
            )
    return value


def _check_bounds(property_id: str, prop: PropertyMetadata, value: int | float) -> None:
    datatype = DATATYPE_METADATA[prop.datatype]
    if datatype.minimum is not None and value < datatype.minimum:
        raise _format_error(property_id, prop, f"value is below {datatype.minimum}")
    if datatype.maximum is not None and value > datatype.maximum:
        raise _format_error(property_id, prop, f"value is above {datatype.maximum}")


class _StringCodec(Codec[str]):
    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> str:
        del property_id, prop
        return raw_value

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if not isinstance(value, str):
            raise _format_error(property_id, prop, "expected str")
        return value


class _IntegerCodec(Codec[int]):
    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> int:
        try:
            value = int(raw_value)
        except ValueError as exc:
            raise _error(property_id, raw_value, prop, "expected an integer") from exc
        datatype = DATATYPE_METADATA[prop.datatype]
        if datatype.minimum is not None and value < datatype.minimum:
            raise _error(property_id, raw_value, prop, f"value is below {datatype.minimum}")
        if datatype.maximum is not None and value > datatype.maximum:
            raise _error(property_id, raw_value, prop, f"value is above {datatype.maximum}")
        return value

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if isinstance(value, bool) or not isinstance(value, int):
            raise _format_error(property_id, prop, "expected int")
        _check_bounds(property_id, prop, value)
        return str(value)


class _FloatCodec(Codec[float]):
    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> float:
        try:
            value = float(raw_value)
        except ValueError as exc:
            raise _error(property_id, raw_value, prop, "expected a float") from exc
        if not math.isfinite(value):
            raise _error(property_id, raw_value, prop, "value must be finite")
        datatype = DATATYPE_METADATA[prop.datatype]
        if datatype.minimum is not None and value < datatype.minimum:
            raise _error(property_id, raw_value, prop, f"value is below {datatype.minimum}")
        if datatype.maximum is not None and value > datatype.maximum:
            raise _error(property_id, raw_value, prop, f"value is above {datatype.maximum}")
        return value

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise _format_error(property_id, prop, "expected a number")
        try:
            numeric = float(value)
        except (OverflowError, ValueError) as exc:
            raise _format_error(
                property_id, prop, "number is outside the finite float range"
            ) from exc
        if not math.isfinite(numeric):
            raise _format_error(property_id, prop, "value must be finite")
        _check_bounds(property_id, prop, numeric)
        return repr(numeric)


class _BooleanCodec(Codec[bool]):
    _values = {
        "yes": True,
        "true": True,
        "1": True,
        "no": False,
        "false": False,
        "0": False,
    }

    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> bool:
        try:
            return self._values[raw_value.strip().lower()]
        except KeyError as exc:
            raise _error(
                property_id, raw_value, prop, "expected yes/no, true/false, or 1/0"
            ) from exc

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if not isinstance(value, bool):
            raise _format_error(property_id, prop, "expected bool")
        return "yes" if value else "no"


class _ObjectIDListCodec(Codec[tuple[int, ...]]):
    def parse_xml(
        self, raw_value: str, property_id: str, prop: PropertyMetadata
    ) -> tuple[int, ...]:
        tokens = raw_value.split()
        if not tokens:
            return ()
        try:
            values = tuple(int(token) for token in tokens)
        except ValueError as exc:
            raise _error(
                property_id, raw_value, prop, "expected a whitespace-separated ID list"
            ) from exc
        datatype = DATATYPE_METADATA["object_id"]
        for value in values:
            if datatype.minimum is not None and value < datatype.minimum:
                raise _error(property_id, raw_value, prop, f"object ID is below {datatype.minimum}")
            if datatype.maximum is not None and value > datatype.maximum:
                raise _error(property_id, raw_value, prop, f"object ID is above {datatype.maximum}")
        return values

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if not isinstance(value, tuple):
            raise _format_error(property_id, prop, "expected a tuple of object IDs")
        items = cast(tuple[object, ...], value)
        datatype = DATATYPE_METADATA["object_id"]
        for item in items:
            if isinstance(item, bool) or not isinstance(item, int):
                raise _format_error(property_id, prop, "object IDs must be integers")
            if datatype.minimum is not None and item < datatype.minimum:
                raise _format_error(property_id, prop, f"object ID is below {datatype.minimum}")
            if datatype.maximum is not None and item > datatype.maximum:
                raise _format_error(property_id, prop, f"object ID is above {datatype.maximum}")
        return " ".join(str(item) for item in items)


class _EnumCodec(Codec[Enum]):
    @staticmethod
    def _enum(enum_metadata: EnumMetadata) -> type[Enum]:
        return cast(type[Enum], getattr(generated_enums, enum_metadata.python_name))

    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> Enum:
        if prop.enum is None:
            raise _error(property_id, raw_value, prop, "enum metadata is absent")
        enum_metadata = ENUM_METADATA[prop.enum]
        enum_type = self._enum(enum_metadata)
        if enum_metadata.representation == "intflag":
            members = {member.xml_value: member for member in enum_metadata.values}
            tokens = raw_value.split()
            if not tokens:
                raise _error(property_id, raw_value, prop, "expected one or more flag values")
            combined = 0
            for token in tokens:
                member = members.get(token)
                if member is None:
                    raise _error(property_id, raw_value, prop, f"unknown flag token {token!r}")
                if member.cdx_value is None:
                    raise _error(property_id, raw_value, prop, "flag has no CDX numeric value")
                combined |= member.cdx_value
            try:
                return enum_type(combined)
            except ValueError as exc:
                raise _error(property_id, raw_value, prop, "unsupported flag combination") from exc

        for member in enum_metadata.values:
            if member.xml_value == raw_value:
                if enum_metadata.representation == "str":
                    enum_value: str | int = member.xml_value
                elif member.cdx_value is not None:
                    enum_value = member.cdx_value
                else:
                    raise _error(property_id, raw_value, prop, "enum has no CDX numeric value")
                try:
                    return enum_type(enum_value)
                except ValueError as exc:
                    raise _error(
                        property_id, raw_value, prop, "enum metadata is inconsistent"
                    ) from exc
        raise _error(property_id, raw_value, prop, f"unknown {enum_metadata.python_name} value")

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        if prop.enum is None:
            raise _format_error(property_id, prop, "enum metadata is absent")
        enum_metadata = ENUM_METADATA[prop.enum]
        enum_type = self._enum(enum_metadata)
        if not isinstance(value, Enum) or type(value) is not enum_type:
            raise _format_error(property_id, prop, f"expected exact enum type {enum_type.__name__}")

        if enum_metadata.representation == "str":
            string_value = cast(str, value.value)
            for member in enum_metadata.values:
                if member.xml_value == string_value:
                    return member.xml_value
            raise _format_error(property_id, prop, "string enum member is absent from metadata")

        numeric = int(cast(int, value.value))
        if enum_metadata.representation != "intflag":
            for member in enum_metadata.values:
                if member.cdx_value == numeric:
                    return member.xml_value
            raise _format_error(property_id, prop, "integer enum member is absent from metadata")

        remaining = numeric
        parts: list[str] = []
        for member in enum_metadata.values:
            if member.cdx_value and remaining & member.cdx_value == member.cdx_value:
                parts.append(member.xml_value)
                remaining &= ~member.cdx_value
        if remaining or not parts:
            raise _format_error(property_id, prop, "unsupported flag combination")
        return " ".join(parts)


@dataclass(frozen=True, slots=True)
class _GeometryCodec(Codec[object]):
    codec_name: str

    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> object:
        count = {"point_2d": 2, "point_3d": 3, "bounding_box": 4}[self.codec_name]
        tokens = raw_value.replace(",", " ").split()
        if len(tokens) != count:
            raise _error(property_id, raw_value, prop, f"expected {count} coordinate values")
        try:
            numbers = tuple(float(token) for token in tokens)
        except ValueError as exc:
            raise _error(
                property_id, raw_value, prop, "expected numeric coordinate values"
            ) from exc
        if not all(math.isfinite(number) for number in numbers):
            raise _error(property_id, raw_value, prop, "coordinate values must be finite")
        if self.codec_name == "point_2d":
            return Point2D(numbers[0], numbers[1])
        if self.codec_name == "point_3d":
            return Point3D(numbers[0], numbers[1], numbers[2])
        return BoundingBox(numbers[0], numbers[1], numbers[2], numbers[3])

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        numbers: tuple[float, ...]
        if self.codec_name == "point_2d" and isinstance(value, Point2D):
            numbers = (value.x, value.y)
        elif self.codec_name == "point_3d" and isinstance(value, Point3D):
            numbers = (value.x, value.y, value.z)
        elif self.codec_name == "bounding_box" and isinstance(value, BoundingBox):
            numbers = (value.left, value.top, value.right, value.bottom)
        else:
            raise _format_error(property_id, prop, f"expected the {self.codec_name} value type")
        number_values = cast(tuple[object, ...], numbers)
        numeric_values: list[float] = []
        for number in number_values:
            if isinstance(number, bool) or not isinstance(number, (int, float)):
                raise _format_error(property_id, prop, "coordinates must be numbers")
            try:
                numeric_values.append(float(number))
            except (OverflowError, ValueError) as exc:
                raise _format_error(
                    property_id, prop, "coordinate is outside the finite float range"
                ) from exc
        if not all(math.isfinite(number) for number in numeric_values):
            raise _format_error(property_id, prop, "coordinate values must be finite")
        return " ".join(repr(number) for number in numeric_values)


class _ObjectTagValueCodec(Codec[object]):
    """Encode ObjectTag.Value according to its sibling TagType attribute."""

    _tag_types = frozenset({"Unknown", "String", "Long", "Double"})

    def parse_xml(self, raw_value: str, property_id: str, prop: PropertyMetadata) -> object:
        return self.parse_with_context(raw_value, property_id, prop, None)

    def parse_with_context(
        self,
        raw_value: str,
        property_id: str,
        prop: PropertyMetadata,
        context_attributes: Mapping[str, str] | None,
    ) -> object:
        tag_type = (context_attributes or {}).get("TagType")
        if tag_type is not None and tag_type not in self._tag_types:
            raise _error(property_id, raw_value, prop, f"unknown TagType value {tag_type!r}")
        if tag_type == "Long":
            try:
                integer_value = int(raw_value)
            except ValueError as exc:
                raise _error(
                    property_id, raw_value, prop, "expected an INT32 ObjectTag value"
                ) from exc
            if not -(1 << 31) <= integer_value < (1 << 31):
                raise _error(property_id, raw_value, prop, "INT32 ObjectTag value is out of range")
            return integer_value
        if tag_type == "Double":
            try:
                float_value = float(raw_value)
            except ValueError as exc:
                raise _error(
                    property_id, raw_value, prop, "expected a FLOAT64 ObjectTag value"
                ) from exc
            if not math.isfinite(float_value):
                raise _error(property_id, raw_value, prop, "FLOAT64 ObjectTag value must be finite")
            return float_value
        # String, Unknown, and absent/Undefined TagType are preserved lexically.
        return raw_value

    def format_xml(self, value: object, property_id: str, prop: PropertyMetadata) -> str:
        return self.format_with_context(value, property_id, prop, None)

    def format_with_context(
        self,
        value: object,
        property_id: str,
        prop: PropertyMetadata,
        context_attributes: Mapping[str, str] | None,
    ) -> str:
        tag_type = (context_attributes or {}).get("TagType")
        if tag_type is not None and tag_type not in self._tag_types:
            raise _format_error(property_id, prop, f"unknown TagType value {tag_type!r}")
        if tag_type == "Long":
            if isinstance(value, bool) or not isinstance(value, int):
                raise _format_error(property_id, prop, "TagType Long requires an int value")
            if not -(1 << 31) <= value < (1 << 31):
                raise _format_error(property_id, prop, "TagType Long value is outside INT32 range")
            return str(value)
        if tag_type == "Double":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise _format_error(property_id, prop, "TagType Double requires a numeric value")
            try:
                numeric = float(value)
            except (OverflowError, ValueError) as exc:
                raise _format_error(
                    property_id, prop, "TagType Double value is outside the finite float range"
                ) from exc
            if not math.isfinite(numeric):
                raise _format_error(property_id, prop, "TagType Double value must be finite")
            return repr(numeric)
        if not isinstance(value, str):
            raise _format_error(
                property_id, prop, "String, Unknown, and Undefined TagType require a str value"
            )
        return value


_CODECS: Mapping[str, Codec[object]] = MappingProxyType(
    {
        "string": cast(Codec[object], _StringCodec()),
        "integer": cast(Codec[object], _IntegerCodec()),
        "object_id": cast(Codec[object], _IntegerCodec()),
        "float": cast(Codec[object], _FloatCodec()),
        "bool": cast(Codec[object], _BooleanCodec()),
        "object_id_list": cast(Codec[object], _ObjectIDListCodec()),
        "enum": cast(Codec[object], _EnumCodec()),
        "bond_order": cast(Codec[object], _EnumCodec()),
        "point_2d": _GeometryCodec("point_2d"),
        "point_3d": _GeometryCodec("point_3d"),
        "bounding_box": _GeometryCodec("bounding_box"),
        "curve_points2d": cast(Codec[object], CurvePoints2DCodec()),
        "curve_points3d": cast(Codec[object], CurvePoints3DCodec()),
        "uint16_list": cast(Codec[object], UInt16ListCodec()),
        "element_list": cast(Codec[object], ElementListCodec()),
        "generic_list": cast(Codec[object], GenericListCodec()),
        "object_tag_value": cast(Codec[object], _ObjectTagValueCodec()),
    }
)


def decode_property_value(
    property_id: str,
    raw_value: str,
    *,
    context_attributes: Mapping[str, str] | None = None,
) -> object:
    """Decode one raw XML attribute with its generated property metadata."""
    prop = PROPERTY_METADATA[property_id]
    codec_name = "enum" if prop.enum is not None else prop.codec
    codec = _CODECS.get(codec_name)
    if codec is None:
        raise CodecError(
            f"unsupported codec {codec_name!r} for property {property_id!r}",
            property_id=property_id,
            raw_value=raw_value,
        )
    if codec_name == "object_tag_value":
        contextual = cast(_ObjectTagValueCodec, codec)
        return contextual.parse_with_context(raw_value, property_id, prop, context_attributes)
    return codec.parse_xml(raw_value, property_id, prop)


def supports_property_codec(property_id: str) -> bool:
    """Return whether the runtime has both decode and encode behavior for a property."""
    prop = PROPERTY_METADATA[property_id]
    codec_name = "enum" if prop.enum is not None else prop.codec
    return codec_name in _CODECS


def encode_property_value(
    property_id: str,
    value: object,
    *,
    context_attributes: Mapping[str, str] | None = None,
) -> str:
    """Encode a typed value using generated metadata (used by mutation APIs)."""
    prop = PROPERTY_METADATA[property_id]
    codec_name = "enum" if prop.enum is not None else prop.codec
    codec = _CODECS.get(codec_name)
    if codec is None:
        raise CodecError(
            f"unsupported codec {codec_name!r} for property {property_id!r}",
            property_id=property_id,
        )
    if codec_name == "object_tag_value":
        contextual = cast(_ObjectTagValueCodec, codec)
        formatted = contextual.format_with_context(value, property_id, prop, context_attributes)
    else:
        formatted = codec.format_xml(value, property_id, prop)
    return _validate_xml_text(formatted, property_id, prop)


__all__ = ["Codec", "decode_property_value", "encode_property_value"]
