# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Immutable type definitions shared by generated metadata."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TypeAlias

Scalar: TypeAlias = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class ProvenanceMetadata:
    uri: str
    locator: str


@dataclass(frozen=True, slots=True)
class ChildMetadata:
    object_type: str
    collection_name: str
    min_occurs: int
    max_occurs: int | None


@dataclass(frozen=True, slots=True)
class DatatypeMetadata:
    python_type: str
    kind: str
    codec: str
    minimum: int | float | None
    maximum: int | float | None
    status: str
    provenance: tuple[ProvenanceMetadata, ...]


@dataclass(frozen=True, slots=True)
class EnumValueMetadata:
    name: str
    xml_value: str
    cdx_value: int | None


@dataclass(frozen=True, slots=True)
class EnumMetadata:
    python_name: str
    underlying_datatype: str
    representation: str
    values: tuple[EnumValueMetadata, ...]
    status: str
    provenance: tuple[ProvenanceMetadata, ...]


@dataclass(frozen=True, slots=True)
class PropertyMetadata:
    owners: tuple[str, ...]
    name: str
    xml_name: str
    storage: str
    cdx_id: int | None
    cdx_constant: str | None
    datatype: str
    codec: str
    required: bool
    default: Scalar
    cardinality: str
    reference_target: str | None
    reference_many: bool
    enum: str | None
    status: str
    provenance: tuple[ProvenanceMetadata, ...]
    xml_aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObjectMetadata:
    python_name: str
    xml_tag: str
    cdx_id: int | None
    cdx_constant: str | None
    category: str
    id_scope: str
    allowed_parents: tuple[str, ...]
    status: str
    provenance: tuple[ProvenanceMetadata, ...]
    children: tuple[ChildMetadata, ...]
    properties: Mapping[str, PropertyMetadata]
