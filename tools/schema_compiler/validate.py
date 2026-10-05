"""Schema consistency checks that run before any code is generated."""

from __future__ import annotations

import keyword
import re
from collections import Counter
from collections.abc import Hashable
from typing import TypeVar

from tools.schema_compiler.errors import SchemaIssue
from tools.schema_compiler.ir import Scalar, Schema

VALID_STATUSES = frozenset(
    {
        "known",
        "implemented",
        "typed",
        "tested",
        "round_trip_verified",
        "chemdraw_verified",
        "unsupported",
    }
)
EXCEPTION_RULES = frozenset(
    {
        "duplicate_object_cdx_id",
        "duplicate_property_cdx_id",
        "object_xml_tag_collision",
        "property_xml_name_collision",
        "invalid_object_namespace",
        "invalid_property_namespace",
        "invalid_property_link_count",
    }
)
XML_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
RESERVED_MODEL_NAMES = frozenset(
    {
        "_document",
        "_element",
        "_registry",
        "children",
        "raw_element",
        "raw_attributes",
        "xml_tag",
        "text",
        "tail",
        "plain_text",
        "raw_reference_id",
        "raw_reference_ids",
        "__cdxml_read_field__",
        "__cdxml_write_field__",
        "__cdxml_read_collection__",
        "document",
        "parent",
        "to_element",
        "to_file",
        "to_string",
        "validate",
        "__cdx_id__",
        "__spec_id__",
        "__xml_tag__",
    }
)
RESERVED_GENERATED_TYPE_NAMES = frozenset(
    {
        # Imports and module globals emitted by enums.py, models.py,
        # schema_metadata.py, schema_registry.py, and the generated package
        # initializer. A generated class/enum with any of these names can
        # shadow a base class, descriptor, annotation, or registry export.
        "Field",
        "RefField",
        "RefListField",
        "ChildCollection",
        "CDXMLElement",
        "CDXMLDocument",
        "ClassVar",
        "IntEnum",
        "IntFlag",
        "StrEnum",
        "Final",
        "Mapping",
        "MappingProxyType",
        "TypeAlias",
        "dataclass",
        "Scalar",
        "ProvenanceMetadata",
        "ChildMetadata",
        "DatatypeMetadata",
        "EnumValueMetadata",
        "EnumMetadata",
        "PropertyMetadata",
        "ObjectMetadata",
        "MODEL_REGISTRY",
        "OBJECT_BY_XML_TAG",
        "OBJECT_BY_SPEC_ID",
        "SCHEMA_HASH",
        "DATATYPE_METADATA",
        "ENUM_METADATA",
        "PROPERTY_METADATA",
        "OBJECT_METADATA",
        "VALIDATION_METADATA",
        "Point2D",
        "Point3D",
        "BoundingBox",
        "int",
        "str",
        "float",
        "bool",
        "list",
        "tuple",
    }
)
U = TypeVar("U", bound=Hashable)


def _default_matches(value: Scalar, python_type: str) -> bool:
    if python_type == "int":
        return type(value) is int
    if python_type == "float":
        return type(value) in {int, float}
    if python_type == "str":
        return isinstance(value, str)
    if python_type == "bool":
        return isinstance(value, bool)
    return True


def validate_schema(schema: Schema) -> tuple[SchemaIssue, ...]:
    """Return all detectable schema issues in stable order."""
    issues: list[SchemaIssue] = []

    def add(code: str, message: str, location: str) -> None:
        issues.append(SchemaIssue(code, message, location))

    exceptions_by_key: dict[tuple[str, str], str] = {}
    for exception in schema.exceptions:
        location = f"exception:{exception.id}"
        key = (exception.rule, exception.target)
        if exception.id in {item.id for item in schema.exceptions if item is not exception}:
            add("DUPLICATE_EXCEPTION", f"duplicate exception id {exception.id!r}", location)
        if key in exceptions_by_key:
            add("DUPLICATE_EXCEPTION", f"duplicate exception for {key!r}", location)
        exceptions_by_key[key] = exception.id
        if exception.rule not in EXCEPTION_RULES:
            add(
                "INVALID_EXCEPTION_RULE", f"unsupported exception rule {exception.rule!r}", location
            )
        if not exception.target or not exception.rationale.strip() or not exception.provenance:
            add(
                "INCOMPLETE_EXCEPTION",
                "exception requires target, rationale, and provenance",
                location,
            )

    used_exceptions: set[tuple[str, str]] = set()

    def report(code: str, message: str, location: str) -> None:
        key = (code.lower(), location)
        if key in exceptions_by_key:
            used_exceptions.add(key)
        else:
            add(code, message, location)

    def unique(items: list[tuple[U, str]], code: str, label: str) -> None:
        counts = Counter(value for value, _ in items)
        for value, location in items:
            if counts[value] > 1:
                report(code, f"duplicate {label} {value!r}", location)

    object_by_id = {item.id: item for item in schema.objects}
    property_by_id = {item.id: item for item in schema.properties}
    datatype_by_id = {item.id: item for item in schema.datatypes}
    enum_by_id = {item.id: item for item in schema.enums}

    unique(
        [(item.id, f"object:{item.id}") for item in schema.objects],
        "DUPLICATE_OBJECT_ID",
        "object id",
    )
    unique(
        [(item.python_name, f"object:{item.id}") for item in schema.objects],
        "DUPLICATE_PYTHON_NAME",
        "Python class name",
    )
    for obj in schema.objects:
        if obj.python_name in RESERVED_GENERATED_TYPE_NAMES:
            add(
                "RESERVED_GENERATED_TYPE_NAME",
                f"class name {obj.python_name!r} collides with a generated import or builtin",
                f"object:{obj.id}",
            )
    unique(
        [(item.xml_tag, f"object:{item.id}") for item in schema.objects],
        "OBJECT_XML_TAG_COLLISION",
        "XML object tag",
    )
    unique(
        [(item.id, f"property:{item.id}") for item in schema.properties],
        "DUPLICATE_PROPERTY_ID",
        "property id",
    )
    unique(
        [(item.id, f"datatype:{item.id}") for item in schema.datatypes],
        "DUPLICATE_DATATYPE_ID",
        "datatype id",
    )
    unique(
        [(item.id, f"enum:{item.id}") for item in schema.enums],
        "DUPLICATE_ENUM_ID",
        "enum id",
    )
    unique(
        [(item.python_name, f"enum:{item.id}") for item in schema.enums],
        "DUPLICATE_ENUM_NAME",
        "Python enum name",
    )
    for enum_spec in schema.enums:
        if enum_spec.python_name in RESERVED_GENERATED_TYPE_NAMES:
            add(
                "RESERVED_GENERATED_TYPE_NAME",
                f"enum name {enum_spec.python_name!r} collides with a generated import or builtin",
                f"enum:{enum_spec.id}",
            )
    for name in sorted(
        {item.python_name for item in schema.objects} & {item.python_name for item in schema.enums}
    ):
        add("MODEL_ENUM_NAME_COLLISION", f"name {name!r} is both a model and enum", "schema")

    owner_links: dict[str, list[str]] = {}
    for obj in schema.objects:
        for property_id in obj.properties:
            owner_links.setdefault(property_id, []).append(obj.id)

    object_numeric: list[tuple[int, str]] = []
    for obj in schema.objects:
        location = f"object:{obj.id}"
        if obj.status not in VALID_STATUSES:
            add("INVALID_STATUS", f"invalid status {obj.status!r}", location)
        if obj.id_scope not in {"document", "local", "none"}:
            add(
                "INVALID_ID_SCOPE",
                f"invalid ID scope {obj.id_scope!r}; expected document, local, or none",
                location,
            )
        id_property = next(
            (
                property_by_id[property_id]
                for property_id in obj.properties
                if property_id in property_by_id and property_by_id[property_id].name == "id"
            ),
            None,
        )
        has_id_property = id_property is not None
        if obj.id_scope != "none" and not has_id_property:
            add(
                "MISSING_SCOPED_ID_PROPERTY",
                "scoped object requires an object ID property",
                location,
            )
        if obj.id_scope == "document" and id_property is not None:
            if id_property.datatype != "object_id":
                add(
                    "DOCUMENT_ID_DATATYPE",
                    "document-scoped object IDs must use the object_id datatype",
                    location,
                )
        if obj.id_scope == "local" and id_property is not None:
            if id_property.datatype != "local_id":
                add(
                    "LOCAL_ID_DATATYPE",
                    "local object IDs must use the local_id datatype",
                    location,
                )
        if obj.id_scope == "none" and has_id_property:
            add(
                "UNSCOPED_ID_PROPERTY",
                "object without an ID scope cannot expose an ID property",
                location,
            )
        if not obj.provenance:
            add("MISSING_PROVENANCE", "object requires provenance", location)
        if not obj.python_name.isidentifier() or keyword.iskeyword(obj.python_name):
            add("INVALID_PYTHON_NAME", f"invalid class name {obj.python_name!r}", location)
        if not XML_NAME.fullmatch(obj.xml_tag):
            add("INVALID_XML_NAME", f"invalid XML tag {obj.xml_tag!r}", location)
        if obj.cdx_id is not None:
            if not 0x8000 <= obj.cdx_id <= 0xFFFF:
                report(
                    "INVALID_OBJECT_NAMESPACE",
                    f"object numeric ID {obj.cdx_id:#x} is outside the object-tag namespace",
                    location,
                )
            object_numeric.append((obj.cdx_id, location))
            if not obj.cdx_constant:
                add("MISSING_CDX_CONSTANT", "numeric object ID requires its CDX constant", location)
        elif obj.cdx_constant is not None:
            add("MISSING_CDX_ID", "CDX constant requires a numeric object ID", location)

        if len(set(obj.allowed_parents)) != len(obj.allowed_parents):
            add("DUPLICATE_PARENT", "allowed parent list contains a duplicate", location)
        for parent in obj.allowed_parents:
            if parent != "$document" and parent not in object_by_id:
                add("UNRESOLVED_PARENT", f"unresolved parent object {parent!r}", location)

        if len(set(obj.properties)) != len(obj.properties):
            add("DUPLICATE_PROPERTY_LINK", "property list contains a duplicate", location)
        for property_id in obj.properties:
            if property_id not in property_by_id:
                add("UNRESOLVED_PROPERTY", f"unresolved property {property_id!r}", location)

        collection_names: set[str] = set()
        for child in obj.children:
            if child.object_type not in object_by_id:
                add("UNRESOLVED_CHILD", f"unresolved child object {child.object_type!r}", location)
            if not child.collection_name.isidentifier() or keyword.iskeyword(child.collection_name):
                add(
                    "INVALID_COLLECTION_NAME",
                    f"invalid collection name {child.collection_name!r}",
                    location,
                )
            if child.collection_name in collection_names:
                add(
                    "CHILD_COLLECTION_COLLISION",
                    f"duplicate collection {child.collection_name!r}",
                    location,
                )
            if (
                child.collection_name in RESERVED_MODEL_NAMES
                or child.collection_name in RESERVED_GENERATED_TYPE_NAMES
            ):
                add(
                    "RESERVED_MODEL_NAME",
                    f"child collection name {child.collection_name!r} is reserved",
                    location,
                )
            collection_names.add(child.collection_name)
            if child.min_occurs < 0 or (
                child.max_occurs is not None and child.max_occurs < child.min_occurs
            ):
                add("INVALID_CARDINALITY", "invalid child occurrence bounds", location)

    unique(object_numeric, "DUPLICATE_OBJECT_CDX_ID", "object numeric ID")
    property_numeric: list[tuple[int, str]] = []
    xml_properties: list[tuple[tuple[str, str], str]] = []
    python_properties: list[tuple[tuple[str, str], str]] = []
    for prop in schema.properties:
        location = f"property:{prop.id}"
        if prop.status not in VALID_STATUSES:
            add("INVALID_STATUS", f"invalid status {prop.status!r}", location)
        if not prop.provenance:
            add("MISSING_PROVENANCE", "property requires provenance", location)
        if not prop.owners:
            add("UNRESOLVED_PROPERTY_OWNER", "property requires at least one owner", location)
        if len(set(prop.owners)) != len(prop.owners):
            add("DUPLICATE_PROPERTY_OWNER", "property owner list contains a duplicate", location)
        actual_owners = owner_links.get(prop.id, [])
        if len(actual_owners) != len(prop.owners) or set(actual_owners) != set(prop.owners):
            report(
                "INVALID_PROPERTY_LINK_COUNT",
                f"property is linked to {actual_owners!r}; expected owners {prop.owners!r}",
                location,
            )
        for owner in prop.owners:
            if owner not in object_by_id:
                add("UNRESOLVED_PROPERTY_OWNER", f"unresolved owner {owner!r}", location)
            if prop.storage == "attribute":
                xml_properties.append(((owner, prop.xml_name), location))
                xml_properties.extend(((owner, alias), location) for alias in prop.xml_aliases)
            python_properties.append(((owner, prop.name), location))

        if not prop.name.isidentifier() or keyword.iskeyword(prop.name):
            add("INVALID_PROPERTY_NAME", f"invalid Python field name {prop.name!r}", location)
        if prop.name in RESERVED_MODEL_NAMES or prop.name in RESERVED_GENERATED_TYPE_NAMES:
            add("RESERVED_MODEL_NAME", f"property name {prop.name!r} is reserved", location)
        if prop.storage not in {"attribute", "text"}:
            add("INVALID_PROPERTY_STORAGE", f"invalid storage {prop.storage!r}", location)
        if prop.storage == "attribute" and not XML_NAME.fullmatch(prop.xml_name):
            add("INVALID_XML_NAME", f"invalid XML property name {prop.xml_name!r}", location)
        if prop.storage != "attribute" and prop.xml_aliases:
            add(
                "INVALID_XML_ALIAS_STORAGE",
                "only attribute properties can have XML aliases",
                location,
            )
        if len(set(prop.xml_aliases)) != len(prop.xml_aliases):
            add("DUPLICATE_XML_ALIAS", "XML alias list contains a duplicate", location)
        if prop.xml_name in prop.xml_aliases:
            add("DUPLICATE_XML_ALIAS", "XML alias repeats the canonical name", location)
        for alias in prop.xml_aliases:
            if not XML_NAME.fullmatch(alias):
                add("INVALID_XML_NAME", f"invalid XML property alias {alias!r}", location)
        if prop.storage == "text" and prop.xml_name != prop.name:
            add(
                "INVALID_TEXT_STORAGE_NAME",
                "text-stored properties use their Python field name as the metadata name",
                location,
            )
        if prop.datatype not in datatype_by_id:
            add("UNRESOLVED_DATATYPE", f"unresolved datatype {prop.datatype!r}", location)
        if prop.codec is not None and not prop.codec.isidentifier():
            add("INVALID_CODEC", f"invalid codec name {prop.codec!r}", location)
        if prop.enum is not None:
            enum = enum_by_id.get(prop.enum)
            if enum is None:
                add("UNRESOLVED_ENUM", f"unresolved enum {prop.enum!r}", location)
            elif enum.underlying_datatype != prop.datatype:
                add("ENUM_DATATYPE_MISMATCH", "enum and property datatypes differ", location)

        if prop.cdx_id is not None:
            if not 0 <= prop.cdx_id < 0x8000:
                report(
                    "INVALID_PROPERTY_NAMESPACE",
                    f"property numeric ID {prop.cdx_id:#x} is outside the property namespace",
                    location,
                )
            property_numeric.append((prop.cdx_id, location))
            if not prop.cdx_constant:
                add(
                    "MISSING_CDX_CONSTANT",
                    "numeric property ID requires its CDX constant",
                    location,
                )
        elif prop.cdx_constant is not None:
            add("MISSING_CDX_ID", "CDX constant requires a numeric property ID", location)

        if prop.cardinality not in {"one", "many"}:
            add(
                "INVALID_CARDINALITY",
                f"invalid property cardinality {prop.cardinality!r}",
                location,
            )
        if prop.reference is not None:
            if prop.reference.target_type != "*" and prop.reference.target_type not in object_by_id:
                add(
                    "UNRESOLVED_REFERENCE_TARGET",
                    f"unresolved target {prop.reference.target_type!r}",
                    location,
                )
            if prop.datatype != "object_id":
                add("REFERENCE_DATATYPE", "object references must use object_id datatype", location)
            if prop.cardinality == "many" and not prop.reference.many:
                add(
                    "REFERENCE_CARDINALITY",
                    "many-valued reference must set reference.many",
                    location,
                )
            if prop.reference.many:
                effective_codec = prop.codec
                if effective_codec is None and prop.datatype in datatype_by_id:
                    effective_codec = datatype_by_id[prop.datatype].codec
                if effective_codec != "object_id_list":
                    add(
                        "REFERENCE_LIST_CODEC",
                        "many-valued object references must use the object_id_list codec",
                        location,
                    )
            if prop.cardinality == "one" and prop.reference.many:
                add("REFERENCE_CARDINALITY", "single reference cannot set reference.many", location)
        elif prop.cardinality == "many":
            add("UNSUPPORTED_MANY_PROPERTY", "many-valued properties must be references", location)

        if prop.default is not None:
            if prop.enum is not None and prop.enum in enum_by_id:
                enum = enum_by_id[prop.enum]
                if not any(value.xml_value == prop.default for value in enum.values):
                    add(
                        "INVALID_ENUM_DEFAULT",
                        f"default {prop.default!r} is not an enum XML value",
                        location,
                    )
            elif prop.reference is not None and prop.reference.many and prop.default == "":
                pass
            elif prop.datatype in datatype_by_id:
                python_type = datatype_by_id[prop.datatype].python_type
                if not _default_matches(prop.default, python_type):
                    add("INVALID_DEFAULT", f"default does not match {python_type}", location)

    unique(xml_properties, "PROPERTY_XML_NAME_COLLISION", "XML property name")
    unique(python_properties, "PROPERTY_PYTHON_NAME_COLLISION", "Python property name")
    unique(property_numeric, "DUPLICATE_PROPERTY_CDX_ID", "property numeric ID")

    for datatype in schema.datatypes:
        location = f"datatype:{datatype.id}"
        if datatype.status not in VALID_STATUSES:
            add("INVALID_STATUS", f"invalid status {datatype.status!r}", location)
        if not datatype.provenance:
            add("MISSING_PROVENANCE", "datatype requires provenance", location)
        if datatype.kind not in {
            "integer",
            "string",
            "float",
            "boolean",
            "geometry",
            "sequence",
            "structured",
        }:
            add("INVALID_DATATYPE_KIND", f"invalid kind {datatype.kind!r}", location)
        if not datatype.codec.isidentifier():
            add("INVALID_CODEC", f"invalid codec name {datatype.codec!r}", location)
        if datatype.minimum is not None and datatype.maximum is not None:
            if datatype.minimum > datatype.maximum:
                add("INVALID_DATATYPE_RANGE", "minimum exceeds maximum", location)
        if datatype.kind not in {"integer", "float"} and (
            datatype.minimum is not None or datatype.maximum is not None
        ):
            add("INVALID_DATATYPE_RANGE", "only numeric datatypes may set bounds", location)

    for enum in schema.enums:
        location = f"enum:{enum.id}"
        if enum.status not in VALID_STATUSES:
            add("INVALID_STATUS", f"invalid status {enum.status!r}", location)
        if not enum.provenance:
            add("MISSING_PROVENANCE", "enum requires provenance", location)
        if not enum.python_name.isidentifier() or keyword.iskeyword(enum.python_name):
            add("INVALID_ENUM_NAME", f"invalid Python enum name {enum.python_name!r}", location)
        if enum.underlying_datatype not in datatype_by_id:
            add(
                "UNRESOLVED_DATATYPE",
                f"unresolved enum underlying datatype {enum.underlying_datatype!r}",
                location,
            )
        if enum.representation not in {"int", "str", "intflag"}:
            add(
                "INVALID_ENUM_REPRESENTATION",
                f"invalid representation {enum.representation!r}",
                location,
            )
        if enum.representation in {"int", "intflag"} and enum.underlying_datatype != "integer":
            add("ENUM_REPRESENTATION_TYPE", "integer enum requires integer datatype", location)
        if enum.representation == "str" and enum.underlying_datatype != "string":
            add("ENUM_REPRESENTATION_TYPE", "string enum requires string datatype", location)
        if not enum.values:
            add("EMPTY_ENUM", "enum must define at least one value", location)

        for attribute, label in (("name", "member name"), ("xml_value", "XML enum value")):
            values: list[tuple[str | int, str]] = [
                (getattr(value, attribute), location) for value in enum.values
            ]
            unique(values, "DUPLICATE_ENUM_VALUE", label)
        unique(
            [(value.cdx_value, location) for value in enum.values if value.cdx_value is not None],
            "DUPLICATE_ENUM_VALUE",
            "CDX enum value",
        )
        for value in enum.values:
            if not value.name.isidentifier() or keyword.iskeyword(value.name):
                add("INVALID_ENUM_MEMBER", f"invalid member name {value.name!r}", location)
            if enum.representation in {"int", "intflag"} and value.cdx_value is None:
                add(
                    "MISSING_ENUM_CDX_VALUE",
                    "integer enum member requires a verified CDX numeric value",
                    location,
                )

    for obj in schema.objects:
        property_names = {
            property_by_id[property_id].name
            for property_id in obj.properties
            if property_id in property_by_id
        }
        for child in obj.children:
            if child.collection_name in property_names:
                add(
                    "MODEL_ATTRIBUTE_COLLISION",
                    f"child collection {child.collection_name!r} collides with property",
                    f"object:{obj.id}",
                )
            if (
                child.object_type in object_by_id
                and obj.id not in object_by_id[child.object_type].allowed_parents
            ):
                add(
                    "CHILD_PARENT_MISMATCH",
                    f"{child.object_type!r} does not allow parent {obj.id!r}",
                    f"object:{obj.id}",
                )

    for exception in schema.exceptions:
        key = (exception.rule, exception.target)
        if key not in used_exceptions:
            add(
                "UNUSED_EXCEPTION",
                f"exception {exception.id!r} matches no current issue",
                f"exception:{exception.id}",
            )
    return tuple(issues)
