"""Immutable schema intermediate representation, independent of YAML."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

Scalar: TypeAlias = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class SourceRef:
    source: str
    locator: str
    uri: str


@dataclass(frozen=True, slots=True)
class ReferenceSpec:
    target_type: str
    many: bool = False


@dataclass(frozen=True, slots=True)
class ChildSpec:
    object_type: str
    collection_name: str
    min_occurs: int = 0
    max_occurs: int | None = None


@dataclass(frozen=True, slots=True)
class DatatypeSpec:
    id: str
    python_type: str
    kind: str
    codec: str
    minimum: int | float | None
    maximum: int | float | None
    status: str
    provenance: tuple[SourceRef, ...]


@dataclass(frozen=True, slots=True)
class EnumValueSpec:
    name: str
    xml_value: str
    cdx_value: int | None


@dataclass(frozen=True, slots=True)
class EnumSpec:
    id: str
    python_name: str
    underlying_datatype: str
    representation: str
    values: tuple[EnumValueSpec, ...]
    status: str
    provenance: tuple[SourceRef, ...]


@dataclass(frozen=True, slots=True)
class PropertySpec:
    id: str
    owners: tuple[str, ...]
    name: str
    xml_name: str
    storage: str
    datatype: str
    codec: str | None
    cdx_id: int | None
    cdx_constant: str | None
    required: bool
    default: Scalar
    cardinality: str
    reference: ReferenceSpec | None
    enum: str | None
    status: str
    provenance: tuple[SourceRef, ...]
    xml_aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObjectSpec:
    id: str
    python_name: str
    xml_tag: str
    cdx_id: int | None
    cdx_constant: str | None
    category: str
    id_scope: str
    allowed_parents: tuple[str, ...]
    children: tuple[ChildSpec, ...]
    properties: tuple[str, ...]
    status: str
    provenance: tuple[SourceRef, ...]


@dataclass(frozen=True, slots=True)
class SchemaException:
    id: str
    rule: str
    target: str
    rationale: str
    provenance: tuple[SourceRef, ...]


@dataclass(frozen=True, slots=True)
class Schema:
    version: int
    objects: tuple[ObjectSpec, ...]
    properties: tuple[PropertySpec, ...]
    datatypes: tuple[DatatypeSpec, ...]
    enums: tuple[EnumSpec, ...]
    exceptions: tuple[SchemaException, ...] = ()
