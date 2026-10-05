"""Deterministic build-time Python and schema-lock generation."""

from __future__ import annotations

import hashlib
import json
import keyword
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

from tools.schema_compiler.ir import (
    EnumSpec,
    ObjectSpec,
    PropertySpec,
    Schema,
    SourceRef,
)

GENERATOR_VERSION = "0.2.0"
NOTICE = "# AUTO-GENERATED. DO NOT EDIT DIRECTLY.\n"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def schema_hash(root: Path) -> tuple[str, dict[str, str]]:
    canonical = root / "schema" / "canonical"
    inputs = sorted(canonical.glob("*.yaml"))
    input_hashes = {
        path.relative_to(root).as_posix(): _sha256(path.read_bytes()) for path in inputs
    }
    digest = hashlib.sha256()
    for name, checksum in input_hashes.items():
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(checksum.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest(), input_hashes


def source_hashes(root: Path) -> dict[str, str]:
    sources = root / "schema" / "sources"
    if not sources.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): _sha256(path.read_bytes())
        for path in sorted(sources.rglob("*"))
        if path.is_file() and path.name != "README.md"
    }


def _property_python_type(prop: PropertySpec, schema: Schema) -> str:
    if prop.reference is not None:
        value = (
            "CDXMLElement"
            if prop.reference.target_type == "*"
            else next(
                item.python_name for item in schema.objects if item.id == prop.reference.target_type
            )
        )
        if prop.reference.many:
            value = f"tuple[{value}, ...]"
    elif prop.enum is not None:
        value = next(item.python_name for item in schema.enums if item.id == prop.enum)
    else:
        value = next(item.python_type for item in schema.datatypes if item.id == prop.datatype)
    if prop.reference is not None and prop.reference.many:
        return value
    if not prop.required and prop.default is None:
        return f"{value} | None"
    return value


def _model_order(schema: Schema) -> tuple[ObjectSpec, ...]:
    """Order model shells by their collection/reference dependencies."""
    objects = {item.id: item for item in schema.objects}
    properties = {item.id: item for item in schema.properties}
    visited: set[str] = set()
    active: set[str] = set()
    ordered: list[ObjectSpec] = []

    def visit(object_id: str) -> None:
        if object_id in visited or object_id in active:
            return
        active.add(object_id)
        item = objects[object_id]
        dependencies = [child.object_type for child in item.children]
        dependencies.extend(
            prop.reference.target_type
            for property_id in item.properties
            if (prop := properties[property_id]).reference is not None
            and prop.reference.target_type != "*"
        )
        for dependency in dict.fromkeys(dependencies):
            visit(dependency)
        active.remove(object_id)
        visited.add(object_id)
        ordered.append(item)

    for item in schema.objects:
        visit(item.id)
    return tuple(ordered)


def _enum_source(enum: EnumSpec) -> list[str]:
    base_class = {"int": "IntEnum", "str": "StrEnum", "intflag": "IntFlag"}[enum.representation]
    class_lines = [f"class {enum.python_name}({base_class}):"]
    if enum.representation == "str":
        class_lines.extend(
            f"    {value.name} = {json.dumps(value.xml_value, ensure_ascii=True)}"
            for value in enum.values
        )
    else:
        class_lines.extend(f"    {value.name} = {value.cdx_value}" for value in enum.values)
    return class_lines


def _models(schema: Schema) -> str:
    lines = [
        NOTICE.rstrip("\n"),
        '"""Statically generated classes for the canonical CDXML schema subset."""',
        "from __future__ import annotations",
        "",
        "from typing import ClassVar",
        "",
        "from cdxml_om.core.fields import ChildCollection, Field, RefField, RefListField",
    ]
    used_datatypes = {prop.datatype for prop in schema.properties}
    datatypes = {item.id: item for item in schema.datatypes}
    geometry_types = sorted(
        {
            symbol
            for datatype_id in used_datatypes
            if (datatype := datatypes[datatype_id]).kind == "geometry"
            for symbol in ("Point2D", "Point3D", "BoundingBox")
            if symbol in datatype.python_type
        }
    )
    if geometry_types:
        lines.append(f"from cdxml_om.core.geometry import {', '.join(geometry_types)}")
    custom_value_types = sorted(
        {
            datatype.python_type
            for datatype_id in used_datatypes
            if (datatype := datatypes[datatype_id]).kind == "structured"
            and datatype.python_type in {"ElementList", "GenericList"}
        }
    )
    lines.extend(["from cdxml_om.core.models import CDXMLElement"])
    if custom_value_types:
        lines.append(f"from cdxml_om.core.values import {', '.join(custom_value_types)}")
    lines.append("")
    enum_names = sorted(
        {
            enum.python_name
            for prop in schema.properties
            if prop.enum is not None
            for enum in schema.enums
            if enum.id == prop.enum
        },
        key=str.casefold,
    )
    if enum_names:
        lines.append(f"from .enums import {', '.join(enum_names)}")
    lines.extend(["", ""])

    properties = {prop.id: prop for prop in schema.properties}
    object_names = {item.id: item.python_name for item in schema.objects}
    for obj in _model_order(schema):
        lines.extend(
            [
                f"class {obj.python_name}(CDXMLElement):",
                f"    __spec_id__: ClassVar[str] = {json.dumps(obj.id)}",
                "    __slots__ = ()",
            ]
        )
        for property_id in obj.properties:
            prop = properties[property_id]
            value_type = _property_python_type(prop, schema)
            descriptor = (
                "RefListField"
                if prop.reference is not None and prop.reference.many
                else "RefField"
                if prop.reference is not None
                else "Field"
            )
            descriptor_type = value_type
            if prop.reference is not None and prop.reference.many:
                descriptor_type = (
                    "CDXMLElement"
                    if prop.reference.target_type == "*"
                    else next(
                        item.python_name
                        for item in schema.objects
                        if item.id == prop.reference.target_type
                    )
                )
            lines.extend(
                [
                    f"    {prop.name}: {descriptor}[{descriptor_type}] = {descriptor}(",
                    f"        property_id={json.dumps(prop.id)}",
                    "    )",
                ]
            )
        for child in obj.children:
            target_name = object_names[child.object_type]
            lines.extend(
                [
                    f"    {child.collection_name}: ChildCollection[{target_name}] = "
                    "ChildCollection(",
                    f"        object_type={json.dumps(child.object_type)},",
                    f"        collection_name={json.dumps(child.collection_name)},",
                    "    )",
                ]
            )
        lines.extend(["", ""])
    return "\n".join(lines).rstrip() + "\n"


def _enums(schema: Schema) -> str:
    bases = {"int": "IntEnum", "str": "StrEnum", "intflag": "IntFlag"}
    imports = ", ".join(sorted({bases[item.representation] for item in schema.enums}))
    lines = [
        NOTICE.rstrip("\n"),
        '"""Statically generated enums from canonical schema."""',
        "",
        f"from enum import {imports}",
        "",
    ]
    for index, enum in enumerate(schema.enums):
        if index:
            lines.append("")
        lines.extend(_enum_source(enum))
    return "\n".join(lines).rstrip() + "\n"


def _registry(schema: Schema) -> str:
    object_imports = sorted(schema.objects, key=lambda item: item.python_name.casefold())
    object_entries = sorted(schema.objects, key=lambda item: item.id)
    lines = [
        NOTICE.rstrip("\n"),
        '"""Generated static model registry."""',
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
        "from cdxml_om.core.models import CDXMLElement",
        "",
        "from .models import (",
        *(f"    {item.python_name}," for item in object_imports),
        ")",
        "from .schema_metadata import SCHEMA_HASH as SCHEMA_HASH",
        "",
        "MODEL_REGISTRY: Final[Mapping[str, type[CDXMLElement]]] = MappingProxyType(",
        "    {",
        *(f"        {json.dumps(item.id)}: {item.python_name}," for item in object_entries),
        "    }",
        ")",
        "OBJECT_BY_XML_TAG: Final[Mapping[str, type[CDXMLElement]]] = MappingProxyType(",
        "    {",
        *(
            f"        {json.dumps(item.xml_tag)}: {item.python_name},"
            for item in sorted(schema.objects, key=lambda item: item.xml_tag)
        ),
        "    }",
        ")",
        "OBJECT_BY_SPEC_ID: Final[Mapping[str, type[CDXMLElement]]] = MODEL_REGISTRY",
        "",
    ]
    return "\n".join(lines)


def _literal(value: object) -> str:
    """Render supported schema data as valid deterministic Python literals."""
    if value is None:
        return "None"
    if value is True:
        return "True"
    if value is False:
        return "False"
    if isinstance(value, str):
        if len(value) <= 64:
            return json.dumps(value, ensure_ascii=True)
        chunks = [value[index : index + 48] for index in range(0, len(value), 48)]
        return "(\n" + "\n".join(json.dumps(chunk, ensure_ascii=True) for chunk in chunks) + "\n)"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, tuple):
        tuple_items = cast(tuple[object, ...], value)
        rendered = ", ".join(_literal(item) for item in tuple_items)
        return f"({rendered}{',' if len(tuple_items) == 1 else ''})"
    if isinstance(value, list):
        list_items = cast(list[object], value)
        return f"[{', '.join(_literal(item) for item in list_items)}]"
    if isinstance(value, dict):
        entries = cast(dict[object, object], value)
        pairs = ", ".join(f"{_literal(key)}: {_literal(item)}" for key, item in entries.items())
        return f"{{{pairs}}}"
    raise TypeError(f"unsupported Python literal value: {type(value).__name__}")


def _module_component(value: str) -> str:
    """Normalize a schema name for a semantic generated-module filename."""
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    snake = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", snake)
    component = re.sub(r"[^A-Za-z0-9_]+", "_", snake).strip("_").lower()
    if not component or component[0].isdigit():
        component = f"schema_{component}"
    if keyword.iskeyword(component) or component == "__init__":
        component = f"{component}_module"
    return component


def _metadata_type_module() -> str:
    lines = [
        NOTICE.rstrip("\n"),
        '"""Immutable type definitions shared by generated metadata."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from dataclasses import dataclass",
        "from typing import TypeAlias",
        "",
        "Scalar: TypeAlias = str | int | float | bool | None",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class ProvenanceMetadata:",
        "    uri: str",
        "    locator: str",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class ChildMetadata:",
        "    object_type: str",
        "    collection_name: str",
        "    min_occurs: int",
        "    max_occurs: int | None",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class DatatypeMetadata:",
        "    python_type: str",
        "    kind: str",
        "    codec: str",
        "    minimum: int | float | None",
        "    maximum: int | float | None",
        "    status: str",
        "    provenance: tuple[ProvenanceMetadata, ...]",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class EnumValueMetadata:",
        "    name: str",
        "    xml_value: str",
        "    cdx_value: int | None",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class EnumMetadata:",
        "    python_name: str",
        "    underlying_datatype: str",
        "    representation: str",
        "    values: tuple[EnumValueMetadata, ...]",
        "    status: str",
        "    provenance: tuple[ProvenanceMetadata, ...]",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class PropertyMetadata:",
        "    owners: tuple[str, ...]",
        "    name: str",
        "    xml_name: str",
        "    storage: str",
        "    cdx_id: int | None",
        "    cdx_constant: str | None",
        "    datatype: str",
        "    codec: str",
        "    required: bool",
        "    default: Scalar",
        "    cardinality: str",
        "    reference_target: str | None",
        "    reference_many: bool",
        "    enum: str | None",
        "    status: str",
        "    provenance: tuple[ProvenanceMetadata, ...]",
        "    xml_aliases: tuple[str, ...] = ()",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class ObjectMetadata:",
        "    python_name: str",
        "    xml_tag: str",
        "    cdx_id: int | None",
        "    cdx_constant: str | None",
        "    category: str",
        "    id_scope: str",
        "    allowed_parents: tuple[str, ...]",
        "    status: str",
        "    provenance: tuple[ProvenanceMetadata, ...]",
        "    children: tuple[ChildMetadata, ...]",
        "    properties: Mapping[str, PropertyMetadata]",
        "",
    ]
    return "\n".join(lines)


def _schema_metadata_refs(schema: Schema) -> tuple[SourceRef, ...]:
    refs: set[SourceRef] = set()
    for datatype in schema.datatypes:
        refs.update(datatype.provenance)
    for enum in schema.enums:
        refs.update(enum.provenance)
    for prop in schema.properties:
        refs.update(prop.provenance)
    for obj in schema.objects:
        refs.update(obj.provenance)
    return tuple(
        sorted(
            refs,
            key=lambda ref: (ref.uri, ref.locator, ref.source),
        )
    )


def _source_uri_module(refs: tuple[SourceRef, ...]) -> str:
    uris: dict[str, str] = {}
    for ref in refs:
        previous = uris.setdefault(ref.source, ref.uri)
        if previous != ref.uri:
            raise ValueError(f"schema provenance source {ref.source!r} has conflicting URIs")
    lines = [
        NOTICE.rstrip("\n"),
        '"""Pooled, static source URI constants for generated metadata."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
        "SOURCE_URIS: Final[Mapping[str, str]] = MappingProxyType(",
        "    {",
    ]
    lines.extend(
        f"        {_literal(source)}: {_literal(uri)}," for source, uri in sorted(uris.items())
    )
    lines.extend(["    }", ")", ""])
    return "\n".join(lines)


def _provenance_modules(
    refs: tuple[SourceRef, ...],
) -> tuple[dict[str, str], dict[tuple[str, str], tuple[str, str]]]:
    """Emit stable content-addressed provenance values in source-named modules."""
    outputs: dict[str, str] = {
        "src/cdxml_om/_generated/_metadata/types.py": _metadata_type_module(),
        "src/cdxml_om/_generated/_metadata/sources.py": _source_uri_module(refs),
        "src/cdxml_om/_generated/_metadata/provenance/__init__.py": (
            NOTICE.rstrip("\n") + '\n"""Source-organized provenance constants."""\n'
        ),
    }
    source_for_uri: dict[str, str] = {}
    source_module_by_id: dict[str, str] = {}
    for ref in refs:
        source_for_uri[ref.uri] = min(source_for_uri.get(ref.uri, ref.source), ref.source)
        module = _module_component(ref.source)
        previous_source = source_module_by_id.setdefault(module, ref.source)
        if previous_source != ref.source:
            raise ValueError(
                f"provenance source IDs {previous_source!r} and {ref.source!r} normalize to "
                f"the same module {module!r}"
            )

    symbols: dict[tuple[str, str], tuple[str, str]] = {}
    by_source: dict[str, list[tuple[str, str]]] = {}
    symbol_identities: dict[str, tuple[str, str]] = {}
    for uri, locator in sorted({(ref.uri, ref.locator) for ref in refs}):
        source = source_for_uri[uri]
        module = _module_component(source)
        digest = hashlib.sha256(f"{uri}\0{locator}".encode()).hexdigest()
        symbol = f"P_{digest[:20]}"
        identity = (uri, locator)
        previous_identity = symbol_identities.setdefault(symbol, identity)
        if previous_identity != identity:
            raise ValueError(f"provenance key collision for {symbol}")
        symbols[identity] = (module, symbol)
        by_source.setdefault(module, []).append((symbol, locator))

    for module, entries in sorted(by_source.items()):
        source_id = source_module_by_id[module]
        lines = [
            NOTICE.rstrip("\n"),
            f'"""Provenance records sourced from {source_id}."""',
            "from __future__ import annotations",
            "",
            "from ..sources import SOURCE_URIS",
            "from ..types import ProvenanceMetadata",
            "",
        ]
        for symbol, locator in sorted(entries):
            lines.extend(
                [
                    f"{symbol} = ProvenanceMetadata(",
                    f"    uri=SOURCE_URIS[{_literal(source_id)}],",
                    f"    locator={_literal(locator)},",
                    ")",
                ]
            )
        lines.append("")
        outputs[f"src/cdxml_om/_generated/_metadata/provenance/{module}.py"] = "\n".join(lines)

    return outputs, symbols


def _provenance_import_lines(
    refs: tuple[SourceRef, ...],
    symbols: dict[tuple[str, str], tuple[str, str]],
    *,
    nested: bool,
) -> list[str]:
    prefix = ".." if nested else "."
    imports: dict[str, set[str]] = {}
    for ref in refs:
        module, symbol = symbols[(ref.uri, ref.locator)]
        imports.setdefault(module, set()).add(symbol)
    lines: list[str] = []
    for module, symbols_for_module in sorted(imports.items()):
        names = sorted(symbols_for_module)
        if len(names) == 1:
            lines.append(f"from {prefix}provenance.{module} import {names[0]}")
            continue
        lines.append(f"from {prefix}provenance.{module} import (")
        lines.extend(f"    {name}," for name in names)
        lines.append(")")
    return lines


def _emit_provenance_refs(
    lines: list[str],
    refs: tuple[SourceRef, ...],
    symbols: dict[tuple[str, str], tuple[str, str]],
    indent: int,
) -> None:
    padding = " " * indent
    unique_refs = tuple(dict.fromkeys((ref.uri, ref.locator) for ref in refs))
    lines.append(f"{padding}provenance=(")
    lines.extend(f"{padding}    {symbols[identity][1]}," for identity in unique_refs)
    lines.append(f"{padding}),")


def _metadata_datatypes(
    schema: Schema,
    symbols: dict[tuple[str, str], tuple[str, str]],
) -> str:
    lines = [
        NOTICE.rstrip("\n"),
        '"""Generated datatype metadata."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
    ]
    lines.extend(
        _provenance_import_lines(
            tuple(ref for datatype in schema.datatypes for ref in datatype.provenance),
            symbols,
            nested=False,
        )
    )
    lines.extend(
        [
            "from .types import DatatypeMetadata",
            "",
            "DATATYPE_METADATA: Final[Mapping[str, DatatypeMetadata]] = MappingProxyType(",
            "    {",
        ]
    )
    for datatype in schema.datatypes:
        lines.extend(
            [
                f"        {_literal(datatype.id)}: DatatypeMetadata(",
                f"            python_type={_literal(datatype.python_type)},",
                f"            kind={_literal(datatype.kind)},",
                f"            codec={_literal(datatype.codec)},",
                f"            minimum={_literal(datatype.minimum)},",
                f"            maximum={_literal(datatype.maximum)},",
                f"            status={_literal(datatype.status)},",
            ]
        )
        _emit_provenance_refs(lines, datatype.provenance, symbols, 12)
        lines.append("        ),")
    lines.extend(["    }", ")", ""])
    return "\n".join(lines)


def _metadata_enum_outputs(
    schema: Schema,
    symbols: dict[tuple[str, str], tuple[str, str]],
) -> dict[str, str]:
    outputs: dict[str, str] = {
        "src/cdxml_om/_generated/_metadata/enums/__init__.py": (
            NOTICE.rstrip("\n") + '\n"""Named generated enum metadata."""\n'
        )
    }
    modules: dict[str, EnumSpec] = {}
    for enum in sorted(schema.enums, key=lambda item: item.id):
        module = _module_component(enum.python_name)
        previous = modules.get(module)
        if previous is not None:
            raise ValueError(
                f"enum specs {previous.id!r} and {enum.id!r} normalize to module {module!r}"
            )
        modules[module] = enum
        lines = [
            NOTICE.rstrip("\n"),
            f'"""Metadata for the {enum.python_name} enum spec."""',
            "from __future__ import annotations",
            "",
            "from ..types import EnumMetadata, EnumValueMetadata",
        ]
        lines.extend(_provenance_import_lines(enum.provenance, symbols, nested=True))
        lines.extend(
            [
                "",
                "ENUM_METADATA_ENTRY = EnumMetadata(",
                f"    python_name={_literal(enum.python_name)},",
                f"    underlying_datatype={_literal(enum.underlying_datatype)},",
                f"    representation={_literal(enum.representation)},",
                "    values=(",
            ]
        )
        for value in enum.values:
            lines.extend(
                [
                    "        EnumValueMetadata(",
                    f"            name={_literal(value.name)},",
                    f"            xml_value={_literal(value.xml_value)},",
                    f"            cdx_value={_literal(value.cdx_value)},",
                    "        ),",
                ]
            )
        lines.extend(
            [
                "    ),",
                f"    status={_literal(enum.status)},",
            ]
        )
        _emit_provenance_refs(lines, enum.provenance, symbols, 4)
        lines.extend([")", ""])
        outputs[f"src/cdxml_om/_generated/_metadata/enums/{module}.py"] = "\n".join(lines)

    aggregator = [
        NOTICE.rstrip("\n"),
        '"""Read-only mapping of named enum metadata."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
    ]
    for module in sorted(modules):
        aggregator.append(f"from .{module} import ENUM_METADATA_ENTRY as _enum_{module}")
    aggregator.extend(
        [
            "",
            "from ..types import EnumMetadata",
            "",
            "ENUM_METADATA: Final[Mapping[str, EnumMetadata]] = MappingProxyType(",
            "    {",
        ]
    )
    for module, enum in sorted(modules.items()):
        aggregator.append(f"        {_literal(enum.id)}: _enum_{module},")
    aggregator.extend(["    }", ")", ""])
    outputs["src/cdxml_om/_generated/_metadata/enums/__init__.py"] = "\n".join(aggregator)
    return outputs


def _property_group(prop: PropertySpec) -> str:
    owner = next(iter(prop.owners), None)
    if owner is None:
        raise ValueError(f"property spec {prop.id!r} has no owner for module grouping")
    if len(prop.owners) > 1:
        return "shared"
    module = _module_component(owner)
    return f"owner_{module}" if module == "shared" else module


def _metadata_property_outputs(
    schema: Schema,
    symbols: dict[tuple[str, str], tuple[str, str]],
) -> dict[str, str]:
    outputs: dict[str, str] = {
        "src/cdxml_om/_generated/_metadata/properties/__init__.py": (
            NOTICE.rstrip("\n") + '\n"""Logical-owner property metadata groups."""\n'
        )
    }
    grouped: dict[str, list[PropertySpec]] = {}
    for prop in schema.properties:
        grouped.setdefault(_property_group(prop), []).append(prop)

    for module, properties in sorted(grouped.items()):
        properties.sort(key=lambda item: item.id)
        lines = [
            NOTICE.rstrip("\n"),
            f'"""Properties grouped by logical schema owner: {module}."""',
            "from __future__ import annotations",
            "",
            "from collections.abc import Mapping",
            "from types import MappingProxyType",
            "from typing import Final",
            "",
        ]
        references = tuple(ref for prop in properties for ref in prop.provenance)
        lines.extend(_provenance_import_lines(references, symbols, nested=True))
        lines.extend(
            [
                "from ..types import PropertyMetadata",
                "",
                "PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = "
                "MappingProxyType(",
                "    {",
            ]
        )
        for prop in properties:
            reference_target = prop.reference.target_type if prop.reference is not None else None
            reference_many = prop.reference.many if prop.reference is not None else False
            datatype = next(item for item in schema.datatypes if item.id == prop.datatype)
            lines.extend(
                [
                    f"        {_literal(prop.id)}: PropertyMetadata(",
                    f"            owners={_literal(prop.owners)},",
                    f"            name={_literal(prop.name)},",
                    f"            xml_name={_literal(prop.xml_name)},",
                    f"            storage={_literal(prop.storage)},",
                    f"            cdx_id={_literal(prop.cdx_id)},",
                    f"            cdx_constant={_literal(prop.cdx_constant)},",
                    f"            datatype={_literal(prop.datatype)},",
                    f"            codec={_literal(prop.codec or datatype.codec)},",
                    f"            required={_literal(prop.required)},",
                    f"            default={_literal(prop.default)},",
                    f"            cardinality={_literal(prop.cardinality)},",
                    f"            reference_target={_literal(reference_target)},",
                    f"            reference_many={_literal(reference_many)},",
                    f"            enum={_literal(prop.enum)},",
                    f"            status={_literal(prop.status)},",
                ]
            )
            _emit_provenance_refs(lines, prop.provenance, symbols, 12)
            lines.extend(
                [
                    f"            xml_aliases={_literal(prop.xml_aliases)},",
                    "        ),",
                ]
            )
        lines.extend(["    }", ")", ""])
        outputs[f"src/cdxml_om/_generated/_metadata/properties/{module}.py"] = "\n".join(lines)

    aggregator = [
        NOTICE.rstrip("\n"),
        '"""Read-only mapping of canonical property metadata objects."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
    ]
    for module in sorted(grouped):
        aggregator.append(f"from .{module} import PROPERTY_METADATA_GROUP as _properties_{module}")
    aggregator.extend(
        [
            "",
            "from ..types import PropertyMetadata",
            "",
            "PROPERTY_METADATA: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(",
            "    {",
        ]
    )
    for module in sorted(grouped):
        aggregator.append(f"        **_properties_{module},")
    aggregator.extend(["    }", ")", ""])
    outputs["src/cdxml_om/_generated/_metadata/properties/__init__.py"] = "\n".join(aggregator)
    return outputs


def _metadata_object_outputs(
    schema: Schema,
    symbols: dict[tuple[str, str], tuple[str, str]],
) -> dict[str, str]:
    outputs: dict[str, str] = {
        "src/cdxml_om/_generated/_metadata/objects/__init__.py": (
            NOTICE.rstrip("\n") + '\n"""One static metadata module per ObjectSpec."""\n'
        )
    }
    modules: dict[str, ObjectSpec] = {}
    for obj in sorted(schema.objects, key=lambda item: item.id):
        module = _module_component(obj.id)
        previous = modules.get(module)
        if previous is not None:
            raise ValueError(
                f"object specs {previous.id!r} and {obj.id!r} normalize to module {module!r}"
            )
        modules[module] = obj
        lines = [
            NOTICE.rstrip("\n"),
            f'"""Metadata for the {obj.python_name} ObjectSpec."""',
            "from __future__ import annotations",
            "",
            "from types import MappingProxyType",
            "",
        ]
        lines.extend(_provenance_import_lines(obj.provenance, symbols, nested=True))
        metadata_types = "ChildMetadata, ObjectMetadata" if obj.children else "ObjectMetadata"
        lines.extend(
            [
                "from ..properties import PROPERTY_METADATA",
                f"from ..types import {metadata_types}",
                "",
                "OBJECT_METADATA_ENTRY = ObjectMetadata(",
                f"    python_name={_literal(obj.python_name)},",
                f"    xml_tag={_literal(obj.xml_tag)},",
                f"    cdx_id={_literal(obj.cdx_id)},",
                f"    cdx_constant={_literal(obj.cdx_constant)},",
                f"    category={_literal(obj.category)},",
                f"    id_scope={_literal(obj.id_scope)},",
                f"    allowed_parents={_literal(obj.allowed_parents)},",
                f"    status={_literal(obj.status)},",
                "    children=(",
            ]
        )
        for child in obj.children:
            lines.extend(
                [
                    "        ChildMetadata(",
                    f"            object_type={_literal(child.object_type)},",
                    f"            collection_name={_literal(child.collection_name)},",
                    f"            min_occurs={_literal(child.min_occurs)},",
                    f"            max_occurs={_literal(child.max_occurs)},",
                    "        ),",
                ]
            )
        lines.extend(
            [
                "    ),",
                "    properties=MappingProxyType(",
                "        {",
            ]
        )
        for property_id in obj.properties:
            key = _literal(property_id)
            lines.append(f"            {key}: PROPERTY_METADATA[{key}],")
        lines.extend(["        }", "    ),"])
        _emit_provenance_refs(lines, obj.provenance, symbols, 4)
        lines.extend([")", ""])
        outputs[f"src/cdxml_om/_generated/_metadata/objects/{module}.py"] = "\n".join(lines)

    aggregator = [
        NOTICE.rstrip("\n"),
        '"""Read-only mapping of canonical ObjectSpec metadata objects."""',
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from types import MappingProxyType",
        "from typing import Final",
        "",
    ]
    for module in sorted(modules):
        aggregator.append(f"from .{module} import OBJECT_METADATA_ENTRY as _object_{module}")
    aggregator.extend(
        [
            "",
            "from ..types import ObjectMetadata",
            "",
            "OBJECT_METADATA: Final[Mapping[str, ObjectMetadata]] = MappingProxyType(",
            "    {",
        ]
    )
    for module, obj in sorted(modules.items()):
        aggregator.append(f"        {_literal(obj.id)}: _object_{module},")
    aggregator.extend(["    }", ")", ""])
    outputs["src/cdxml_om/_generated/_metadata/objects/__init__.py"] = "\n".join(aggregator)
    return outputs


def _semantic_metadata_outputs(schema: Schema, current_hash: str) -> dict[str, str]:
    refs = _schema_metadata_refs(schema)
    outputs, provenance_symbols = _provenance_modules(refs)
    outputs["src/cdxml_om/_generated/_metadata/datatypes.py"] = _metadata_datatypes(
        schema, provenance_symbols
    )
    outputs.update(_metadata_enum_outputs(schema, provenance_symbols))
    outputs.update(_metadata_property_outputs(schema, provenance_symbols))
    outputs.update(_metadata_object_outputs(schema, provenance_symbols))
    outputs["src/cdxml_om/_generated/_metadata/__init__.py"] = "\n".join(
        [
            NOTICE.rstrip("\n"),
            '"""Static generated schema metadata organized by logical spec."""',
            "from __future__ import annotations",
            "",
            "from .datatypes import DATATYPE_METADATA as DATATYPE_METADATA",
            "from .enums import ENUM_METADATA as ENUM_METADATA",
            "from .objects import OBJECT_METADATA as OBJECT_METADATA",
            "from .properties import PROPERTY_METADATA as PROPERTY_METADATA",
            "",
            "VALIDATION_METADATA = OBJECT_METADATA",
            "",
        ]
    )
    facade = [
        NOTICE.rstrip("\n"),
        '"""Stable import facade for generated immutable schema metadata."""',
        "from __future__ import annotations",
        "",
        "from typing import Final",
        "",
        "from ._metadata import (",
        "    DATATYPE_METADATA as DATATYPE_METADATA,",
        "    ENUM_METADATA as ENUM_METADATA,",
        "    OBJECT_METADATA as OBJECT_METADATA,",
        "    PROPERTY_METADATA as PROPERTY_METADATA,",
        "    VALIDATION_METADATA as VALIDATION_METADATA,",
        ")",
        "from ._metadata.types import (",
        "    ChildMetadata as ChildMetadata,",
        "    DatatypeMetadata as DatatypeMetadata,",
        "    EnumMetadata as EnumMetadata,",
        "    EnumValueMetadata as EnumValueMetadata,",
        "    ObjectMetadata as ObjectMetadata,",
        "    PropertyMetadata as PropertyMetadata,",
        "    ProvenanceMetadata as ProvenanceMetadata,",
        "    Scalar as Scalar,",
        ")",
        "",
        f"SCHEMA_HASH: Final[str] = {_literal(current_hash)}",
        "",
    ]
    outputs["src/cdxml_om/_generated/schema_metadata.py"] = "\n".join(facade)
    return outputs


def _generated_init(schema: Schema) -> str:
    enum_names = sorted((item.python_name for item in schema.enums), key=str.casefold)
    object_names = sorted((item.python_name for item in schema.objects), key=str.casefold)
    registry_names = ["MODEL_REGISTRY", "OBJECT_BY_SPEC_ID", "OBJECT_BY_XML_TAG", "SCHEMA_HASH"]
    metadata_names = [
        "DATATYPE_METADATA",
        "ENUM_METADATA",
        "OBJECT_METADATA",
        "PROPERTY_METADATA",
        "VALIDATION_METADATA",
    ]
    all_names = enum_names + object_names + registry_names + metadata_names
    lines = [
        NOTICE.rstrip("\n"),
        '"""Statically generated public schema exports."""',
        *(f"from .enums import {name} as {name}" for name in enum_names),
        *(f"from .models import {name} as {name}" for name in object_names),
        *(f"from .schema_metadata import {name} as {name}" for name in metadata_names),
        *(f"from .schema_registry import {name} as {name}" for name in registry_names),
        "__all__ = [",
        *(f"    {_literal(name)}," for name in all_names),
        "]",
        "",
    ]
    return "\n".join(lines)


def compile_outputs(schema: Schema, root: Path) -> dict[str, str]:
    current_hash, input_hashes = schema_hash(root)
    lock = {
        "schema_version": schema.version,
        "schema_hash": current_hash,
        "generator_version": GENERATOR_VERSION,
        "input_hashes": input_hashes,
        "source_hashes": source_hashes(root),
    }
    outputs = {
        "src/cdxml_om/_generated/__init__.py": _generated_init(schema),
        "src/cdxml_om/_generated/enums.py": _enums(schema),
        "src/cdxml_om/_generated/models.py": _models(schema),
        "src/cdxml_om/_generated/schema_registry.py": _registry(schema),
        "schema/schema.lock.json": json.dumps(lock, indent=2, sort_keys=True) + "\n",
    }
    outputs.update(_semantic_metadata_outputs(schema, current_hash))
    formatted: dict[str, str] = {}
    for relative, contents in outputs.items():
        if relative.endswith(".py"):
            sorted_imports = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ruff",
                    "check",
                    "--select",
                    "I,F401",
                    "--fix",
                    "--config",
                    str(root / "pyproject.toml"),
                    "--stdin-filename",
                    relative,
                    "-",
                ],
                cwd=root,
                input=contents,
                capture_output=True,
                check=False,
                text=True,
            )
            if sorted_imports.returncode:
                raise RuntimeError(
                    f"Ruff could not sort generated imports in {relative}: "
                    f"{sorted_imports.stderr.strip()}"
                )
            contents = sorted_imports.stdout
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ruff",
                    "format",
                    "--config",
                    str(root / "pyproject.toml"),
                    "--stdin-filename",
                    relative,
                    "-",
                ],
                cwd=root,
                input=contents,
                capture_output=True,
                check=False,
                text=True,
            )
            if result.returncode:
                raise RuntimeError(
                    f"Ruff could not format generated {relative}: {result.stderr.strip()}"
                )
            contents = result.stdout
        formatted[relative] = contents
    return formatted


def write_outputs(outputs: dict[str, str], root: Path) -> None:
    for relative, contents in sorted(outputs.items()):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(contents, encoding="utf-8", newline="\n")
    generated_directory = root / "src" / "cdxml_om" / "_generated"
    expected_python = {
        (root / relative).resolve()
        for relative in outputs
        if relative.startswith("src/cdxml_om/_generated/") and relative.endswith(".py")
    }
    if generated_directory.exists():
        for path in sorted(generated_directory.rglob("*.py")):
            if path.resolve() in expected_python:
                continue
            if not path.read_text(encoding="utf-8").startswith(NOTICE):
                raise RuntimeError(
                    f"refusing to remove non-generated Python file {path.relative_to(root)}"
                )
            path.unlink()


def compare_outputs(outputs: dict[str, str], root: Path) -> tuple[str, ...]:
    differences: list[str] = []
    for relative, expected in sorted(outputs.items()):
        path = root / relative
        if not path.exists():
            differences.append(f"missing generated file: {relative}")
        elif path.read_text(encoding="utf-8") != expected:
            differences.append(f"generated file is stale: {relative}")

    generated_directory = root / "src" / "cdxml_om" / "_generated"
    expected_python = {
        Path(relative).relative_to("src/cdxml_om/_generated").as_posix()
        for relative in outputs
        if relative.startswith("src/cdxml_om/_generated/")
    }
    if generated_directory.exists():
        for path in sorted(generated_directory.rglob("*.py")):
            actual_relative = path.relative_to(generated_directory).as_posix()
            if actual_relative not in expected_python:
                differences.append(
                    f"unexpected generated file: {path.relative_to(root).as_posix()}"
                )
    return tuple(differences)
