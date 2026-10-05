"""Load the YAML canonical representation into YAML-independent schema IR."""

from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
from typing import TypeVar, cast

import yaml

from tools.schema_compiler.errors import SchemaError, SchemaIssue
from tools.schema_compiler.ir import (
    ChildSpec,
    DatatypeSpec,
    EnumSpec,
    EnumValueSpec,
    ObjectSpec,
    PropertySpec,
    ReferenceSpec,
    Scalar,
    Schema,
    SchemaException,
    SourceRef,
)
from tools.schema_compiler.sources import SOURCES

YamlMapping = dict[str, object]
T = TypeVar("T")
_EMPTY_LIST: list[object] = []


def _issue(code: str, message: str, location: str) -> SchemaError:
    return SchemaError((SchemaIssue(code, message, location),))


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent last-key-wins overwrites."""


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader,
    node: yaml.MappingNode,
) -> dict[Hashable, object]:
    loader.flatten_mapping(node)
    mapping: dict[Hashable, object] = {}
    for key_node, value_node in node.value:
        raw_key = cast(
            object,
            loader.construct_object(key_node, deep=True),  # pyright: ignore[reportUnknownMemberType]
        )
        if not isinstance(raw_key, Hashable):
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            )
        if raw_key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {raw_key!r}",
                key_node.start_mark,
            )
        value = cast(
            object,
            loader.construct_object(value_node, deep=True),  # pyright: ignore[reportUnknownMemberType]
        )
        mapping[raw_key] = value
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _mapping(value: object, location: str) -> YamlMapping:
    if not isinstance(value, dict):
        raise _issue("SCHEMA_SHAPE", "expected a YAML mapping", location)
    result: YamlMapping = {}
    raw_mapping = cast(dict[object, object], value)
    for key, child in raw_mapping.items():
        if not isinstance(key, str):
            raise _issue("SCHEMA_SHAPE", "mapping keys must be text", location)
        result[key] = child
    return result


def _list(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise _issue("SCHEMA_SHAPE", "expected a YAML list", location)
    return cast(list[object], value)


def _read_yaml(path: Path) -> YamlMapping:
    try:
        value: object = yaml.load(
            path.read_text(encoding="utf-8"),
            Loader=_UniqueKeySafeLoader,
        )
    except (OSError, yaml.YAMLError) as exc:
        raise _issue("SCHEMA_INPUT", str(exc), str(path)) from exc
    return _mapping(value, str(path))


def _required(item: YamlMapping, key: str, expected: type[T], location: str) -> T:
    value = item.get(key)
    if type(value) is not expected:
        raise _issue("SCHEMA_FIELD", f"{key!r} must be {expected.__name__}", location)
    return value


def _integer(value: object, key: str, location: str) -> int:
    if type(value) is not int:
        raise _issue("SCHEMA_FIELD", f"{key!r} must be an integer", location)
    return value


def _optional_integer(value: object, key: str, location: str) -> int | None:
    if value is not None and type(value) is not int:
        raise _issue("SCHEMA_FIELD", f"{key!r} must be an integer or null", location)
    return value


def _optional_number(value: object, key: str, location: str) -> int | float | None:
    if value is not None and type(value) not in {int, float}:
        raise _issue("SCHEMA_FIELD", f"{key!r} must be a number or null", location)
    return cast(int | float | None, value)


def _boolean(value: object, key: str, location: str) -> bool:
    if type(value) is not bool:
        raise _issue("SCHEMA_FIELD", f"{key!r} must be a boolean", location)
    return value


def _scalar(value: object, key: str, location: str) -> Scalar:
    if value is not None and not isinstance(value, (str, int, float, bool)):
        raise _issue("SCHEMA_FIELD", f"{key!r} must be a scalar", location)
    return value


def _string_list(value: object, key: str, location: str) -> tuple[str, ...]:
    entries = _list(value, location)
    if any(not isinstance(entry, str) for entry in entries):
        raise _issue("SCHEMA_FIELD", f"{key!r} must contain only strings", location)
    return tuple(cast(str, entry) for entry in entries)


def _refs(value: object, location: str) -> tuple[SourceRef, ...]:
    refs: list[SourceRef] = []
    for index, raw_item in enumerate(_list(value, location)):
        here = f"{location}[{index}]"
        item = _mapping(raw_item, here)
        source_id = _required(item, "source", str, here)
        locator = _required(item, "locator", str, here)
        if source_id not in SOURCES:
            raise _issue("UNKNOWN_SOURCE", f"unknown source {source_id!r}", here)
        if not locator.strip():
            raise _issue("SOURCE_LOCATOR", "locator must be non-empty text", here)
        refs.append(SourceRef(source_id, locator, SOURCES[source_id].uri))
    return tuple(refs)


def _records(item: YamlMapping, key: str, location: str) -> tuple[YamlMapping, ...]:
    result: list[YamlMapping] = []
    for index, value in enumerate(_list(item.get(key, _EMPTY_LIST), f"{location}.{key}")):
        result.append(_mapping(value, f"{location}.{key}[{index}]"))
    return tuple(result)


def _read_version(files: tuple[tuple[str, YamlMapping], ...]) -> int:
    versions = {_required(content, "version", int, f"{name}.yaml") for name, content in files}
    if len(versions) != 1:
        raise _issue("SCHEMA_VERSION", "canonical file versions differ", "schema/canonical")
    return next(iter(versions))


def load_schema(root: Path) -> Schema:
    """Read canonical files rooted at ``schema/canonical``."""
    canonical = root / "schema" / "canonical"
    raw_objects = _read_yaml(canonical / "objects.yaml")
    raw_properties = _read_yaml(canonical / "properties.yaml")
    raw_datatypes = _read_yaml(canonical / "datatypes.yaml")
    raw_enums = _read_yaml(canonical / "enums.yaml")
    version = _read_version(
        (
            ("objects", raw_objects),
            ("properties", raw_properties),
            ("datatypes", raw_datatypes),
            ("enums", raw_enums),
        )
    )

    objects: list[ObjectSpec] = []
    for index, item in enumerate(_records(raw_objects, "objects", "objects.yaml")):
        loc = f"objects.yaml:objects[{index}]"
        children = tuple(
            ChildSpec(
                object_type=_required(child, "object_type", str, f"{loc}.children[{child_index}]"),
                collection_name=_required(
                    child, "collection_name", str, f"{loc}.children[{child_index}]"
                ),
                min_occurs=_integer(
                    child.get("min_occurs", 0), "min_occurs", f"{loc}.children[{child_index}]"
                ),
                max_occurs=_optional_integer(
                    child.get("max_occurs"), "max_occurs", f"{loc}.children[{child_index}]"
                ),
            )
            for child_index, child in enumerate(_records(item, "children", loc))
        )
        cdx_id = _optional_integer(item.get("cdx_id"), "cdx_id", loc)
        raw_constant = item.get("cdx_constant")
        if raw_constant is not None and not isinstance(raw_constant, str):
            raise _issue("SCHEMA_FIELD", "'cdx_constant' must be a string or null", loc)
        objects.append(
            ObjectSpec(
                id=_required(item, "id", str, loc),
                python_name=_required(item, "python_name", str, loc),
                xml_tag=_required(item, "xml_tag", str, loc),
                cdx_id=cdx_id,
                cdx_constant=raw_constant,
                category=_required(item, "category", str, loc),
                id_scope=_required(item, "id_scope", str, loc),
                allowed_parents=_string_list(
                    item.get("allowed_parents", _EMPTY_LIST), "allowed_parents", loc
                ),
                children=children,
                properties=_string_list(item.get("properties", _EMPTY_LIST), "properties", loc),
                status=_required(item, "status", str, loc),
                provenance=_refs(item.get("provenance", _EMPTY_LIST), f"{loc}.provenance"),
            )
        )

    properties: list[PropertySpec] = []
    for index, item in enumerate(_records(raw_properties, "properties", "properties.yaml")):
        loc = f"properties.yaml:properties[{index}]"
        raw_owners = item.get("owners", item.get("owner"))
        owners: tuple[str, ...]
        if isinstance(raw_owners, str):
            owners = (raw_owners,)
        elif isinstance(raw_owners, list):
            owners = _string_list(cast(object, raw_owners), "owners", loc)
        else:
            raise _issue("SCHEMA_FIELD", "owner or owners must name object types", loc)

        raw_reference = item.get("reference")
        reference: ReferenceSpec | None = None
        if raw_reference is not None:
            reference = ReferenceSpec(
                target_type=_required({"target_type": raw_reference}, "target_type", str, loc),
                many=_boolean(item.get("reference_many", False), "reference_many", loc),
            )

        raw_codec = item.get("codec")
        if raw_codec is not None and not isinstance(raw_codec, str):
            raise _issue("SCHEMA_FIELD", "'codec' must be a string or null", loc)
        raw_constant = item.get("cdx_constant")
        if raw_constant is not None and not isinstance(raw_constant, str):
            raise _issue("SCHEMA_FIELD", "'cdx_constant' must be a string or null", loc)
        raw_enum = item.get("enum")
        if raw_enum is not None and not isinstance(raw_enum, str):
            raise _issue("SCHEMA_FIELD", "'enum' must be a string or null", loc)

        properties.append(
            PropertySpec(
                id=_required(item, "id", str, loc),
                owners=owners,
                name=_required(item, "name", str, loc),
                xml_name=_required(item, "xml_name", str, loc),
                storage=_required(item, "storage", str, loc) if "storage" in item else "attribute",
                datatype=_required(item, "datatype", str, loc),
                codec=raw_codec,
                cdx_id=_optional_integer(item.get("cdx_id"), "cdx_id", loc),
                cdx_constant=raw_constant,
                required=_boolean(item.get("required", False), "required", loc),
                default=_scalar(item.get("default"), "default", loc),
                cardinality=_required(item, "cardinality", str, loc)
                if "cardinality" in item
                else "one",
                reference=reference,
                enum=raw_enum,
                status=_required(item, "status", str, loc),
                provenance=_refs(item.get("provenance", _EMPTY_LIST), f"{loc}.provenance"),
                xml_aliases=_string_list(item.get("xml_aliases", _EMPTY_LIST), "xml_aliases", loc),
            )
        )

    datatypes: list[DatatypeSpec] = []
    for index, item in enumerate(_records(raw_datatypes, "datatypes", "datatypes.yaml")):
        loc = f"datatypes.yaml:datatypes[{index}]"
        datatypes.append(
            DatatypeSpec(
                id=_required(item, "id", str, loc),
                python_type=_required(item, "python_type", str, loc),
                kind=_required(item, "kind", str, loc),
                codec=_required(item, "codec", str, loc),
                minimum=_optional_number(item.get("minimum"), "minimum", loc),
                maximum=_optional_number(item.get("maximum"), "maximum", loc),
                status=_required(item, "status", str, loc),
                provenance=_refs(item.get("provenance", _EMPTY_LIST), f"{loc}.provenance"),
            )
        )

    enums: list[EnumSpec] = []
    for index, item in enumerate(_records(raw_enums, "enums", "enums.yaml")):
        loc = f"enums.yaml:enums[{index}]"
        enum_values: list[EnumValueSpec] = []
        for value_index, raw_value in enumerate(_records(item, "values", loc)):
            value_loc = f"{loc}.values[{value_index}]"
            enum_values.append(
                EnumValueSpec(
                    name=_required(raw_value, "name", str, value_loc),
                    xml_value=_required(raw_value, "xml_value", str, value_loc),
                    cdx_value=_optional_integer(raw_value.get("cdx_value"), "cdx_value", value_loc),
                )
            )
        enums.append(
            EnumSpec(
                id=_required(item, "id", str, loc),
                python_name=_required(item, "python_name", str, loc),
                underlying_datatype=_required(item, "underlying_datatype", str, loc),
                representation=_required(item, "representation", str, loc),
                values=tuple(enum_values),
                status=_required(item, "status", str, loc),
                provenance=_refs(item.get("provenance", []), f"{loc}.provenance"),
            )
        )

    exceptions = tuple(
        SchemaException(
            id=_required(item, "id", str, f"objects.yaml:exceptions[{index}]"),
            rule=_required(item, "rule", str, f"objects.yaml:exceptions[{index}]"),
            target=_required(item, "target", str, f"objects.yaml:exceptions[{index}]"),
            rationale=_required(item, "rationale", str, f"objects.yaml:exceptions[{index}]"),
            provenance=_refs(
                item.get("provenance", []), f"objects.yaml:exceptions[{index}].provenance"
            ),
        )
        for index, item in enumerate(_records(raw_objects, "exceptions", "objects.yaml"))
    )

    return Schema(
        version=version,
        objects=tuple(objects),
        properties=tuple(properties),
        datatypes=tuple(datatypes),
        enums=tuple(enums),
        exceptions=exceptions,
    )
