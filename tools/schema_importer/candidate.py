"""Typed, immutable candidates that preserve imported source evidence."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Literal, cast

from tools.schema_importer.errors import ImporterError

SourceKind = Literal["dtd", "sdk-html"]
SDKNamespace = Literal["object", "property", "xml-only", "unknown"]
SDKRelation = Literal["inventory", "summary", "subobject", "property"]


@dataclass(frozen=True, slots=True)
class CandidateSource:
    kind: SourceKind
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class ContentModelCandidate:
    """A syntax tree for one DTD content model; it carries no runtime semantics."""

    kind: str
    occurrence: str
    name: str | None = None
    children: tuple[ContentModelCandidate, ...] = ()


@dataclass(frozen=True, slots=True)
class DTDAttributeCandidate:
    name: str
    declared_type: str
    required: bool
    default_kind: str
    default_value: str | None
    enum_values: tuple[str, ...]
    locator: str


@dataclass(frozen=True, slots=True)
class DTDElementCandidate:
    xml_name: str
    declaration_type: str
    content_model: ContentModelCandidate | None
    children: tuple[str, ...]
    attributes: tuple[DTDAttributeCandidate, ...]
    locator: str


@dataclass(frozen=True, slots=True)
class SDKEntryCandidate:
    namespace: SDKNamespace
    relation: SDKRelation
    display_name: str | None
    value_text: str | None
    cdx_id: int | None
    cdx_constant: str | None
    xml_name: str | None
    type_name: str | None
    owner_xml_name: str | None
    locator: str


@dataclass(frozen=True, slots=True)
class CandidateDocument:
    source: CandidateSource
    scope: str
    normalizations: tuple[str, ...] = ()
    dtd_elements: tuple[DTDElementCandidate, ...] = ()
    sdk_entries: tuple[SDKEntryCandidate, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready deterministic representation."""
        return {
            "format": "cdxml-om-schema-candidate",
            "format_version": 1,
            "source": asdict(self.source),
            "scope": self.scope,
            "normalizations": list(self.normalizations),
            "dtd_elements": [asdict(item) for item in self.dtd_elements],
            "sdk_entries": [asdict(item) for item in self.sdk_entries],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_json(cls, source: str) -> CandidateDocument:
        try:
            raw: object = json.loads(source)
        except json.JSONDecodeError as exc:
            raise ImporterError("CANDIDATE_JSON", str(exc), "candidate") from exc
        return candidate_from_dict(raw)


def _mapping(value: object, location: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ImporterError("CANDIDATE_SHAPE", "expected a JSON object", location)
    mapping: dict[str, object] = {}
    for key, child in cast(dict[object, object], value).items():
        if not isinstance(key, str):
            raise ImporterError("CANDIDATE_SHAPE", "object keys must be text", location)
        mapping[key] = child
    return mapping


def _string(item: Mapping[str, object], key: str, location: str) -> str:
    value = item.get(key)
    if not isinstance(value, str):
        raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be text", location)
    return value


def _optional_string(item: Mapping[str, object], key: str, location: str) -> str | None:
    value = item.get(key)
    if value is not None and not isinstance(value, str):
        raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be text or null", location)
    return value


def _optional_integer(item: Mapping[str, object], key: str, location: str) -> int | None:
    value = item.get(key)
    if value is not None and type(value) is not int:
        raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be an integer or null", location)
    return value


def _boolean(item: Mapping[str, object], key: str, location: str) -> bool:
    value = item.get(key)
    if type(value) is not bool:
        raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be a boolean", location)
    return value


def _string_tuple(item: Mapping[str, object], key: str, location: str) -> tuple[str, ...]:
    raw = item.get(key)
    if not isinstance(raw, list):
        raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be an array of text", location)
    entries: list[str] = []
    for entry in cast(list[object], raw):
        if not isinstance(entry, str):
            raise ImporterError("CANDIDATE_SHAPE", f"{key!r} must be an array of text", location)
        entries.append(entry)
    return tuple(entries)


def _content_model(value: object, location: str, depth: int = 0) -> ContentModelCandidate:
    if depth > 128:
        raise ImporterError("CANDIDATE_SHAPE", "content model nesting is too deep", location)
    item = _mapping(value, location)
    raw_children = item.get("children")
    if not isinstance(raw_children, list):
        raise ImporterError("CANDIDATE_SHAPE", "'children' must be an array", location)
    children = tuple(
        _content_model(child, f"{location}.children[{index}]", depth + 1)
        for index, child in enumerate(cast(list[object], raw_children))
    )
    return ContentModelCandidate(
        kind=_string(item, "kind", location),
        occurrence=_string(item, "occurrence", location),
        name=_optional_string(item, "name", location),
        children=children,
    )


def _dtd_attribute(value: object, location: str) -> DTDAttributeCandidate:
    item = _mapping(value, location)
    enum_values = _string_tuple(item, "enum_values", location)
    return DTDAttributeCandidate(
        name=_string(item, "name", location),
        declared_type=_string(item, "declared_type", location),
        required=_boolean(item, "required", location),
        default_kind=_string(item, "default_kind", location),
        default_value=_optional_string(item, "default_value", location),
        enum_values=enum_values,
        locator=_string(item, "locator", location),
    )


def _dtd_element(value: object, location: str) -> DTDElementCandidate:
    item = _mapping(value, location)
    raw_model = item.get("content_model")
    model = None if raw_model is None else _content_model(raw_model, f"{location}.content_model")
    raw_attributes = item.get("attributes")
    if not isinstance(raw_attributes, list):
        raise ImporterError("CANDIDATE_SHAPE", "'attributes' must be an array", location)
    attributes = tuple(
        _dtd_attribute(attribute, f"{location}.attributes[{index}]")
        for index, attribute in enumerate(cast(list[object], raw_attributes))
    )
    return DTDElementCandidate(
        xml_name=_string(item, "xml_name", location),
        declaration_type=_string(item, "declaration_type", location),
        content_model=model,
        children=_string_tuple(item, "children", location),
        attributes=attributes,
        locator=_string(item, "locator", location),
    )


def _sdk_entry(value: object, location: str) -> SDKEntryCandidate:
    item = _mapping(value, location)
    namespace = _string(item, "namespace", location)
    relation = _string(item, "relation", location)
    if namespace not in {"object", "property", "xml-only", "unknown"}:
        raise ImporterError("CANDIDATE_SHAPE", "invalid SDK namespace", location)
    if relation not in {"inventory", "summary", "subobject", "property"}:
        raise ImporterError("CANDIDATE_SHAPE", "invalid SDK relation", location)
    return SDKEntryCandidate(
        namespace=cast(SDKNamespace, namespace),
        relation=cast(SDKRelation, relation),
        display_name=_optional_string(item, "display_name", location),
        value_text=_optional_string(item, "value_text", location),
        cdx_id=_optional_integer(item, "cdx_id", location),
        cdx_constant=_optional_string(item, "cdx_constant", location),
        xml_name=_optional_string(item, "xml_name", location),
        type_name=_optional_string(item, "type_name", location),
        owner_xml_name=_optional_string(item, "owner_xml_name", location),
        locator=_string(item, "locator", location),
    )


def candidate_from_dict(value: object) -> CandidateDocument:
    """Validate and decode the versioned candidate JSON representation."""
    item = _mapping(value, "candidate")
    if item.get("format") != "cdxml-om-schema-candidate":
        raise ImporterError("CANDIDATE_FORMAT", "unrecognized candidate format", "candidate")
    if item.get("format_version") != 1:
        raise ImporterError(
            "CANDIDATE_VERSION", "unsupported candidate format version", "candidate"
        )
    raw_source = _mapping(item.get("source"), "candidate.source")
    kind = _string(raw_source, "kind", "candidate.source")
    if kind not in {"dtd", "sdk-html"}:
        raise ImporterError("CANDIDATE_SHAPE", "invalid source kind", "candidate.source")
    digest = _string(raw_source, "sha256", "candidate.source")
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ImporterError(
            "CANDIDATE_SHAPE", "source sha256 must be lowercase hex", "candidate.source"
        )
    source = CandidateSource(
        kind=cast(SourceKind, kind),
        path=_string(raw_source, "path", "candidate.source"),
        sha256=digest,
    )
    scope = _string(item, "scope", "candidate")
    raw_normalizations = item.get("normalizations", [])
    if not isinstance(raw_normalizations, list):
        raise ImporterError("CANDIDATE_SHAPE", "'normalizations' must be an array", "candidate")
    normalizations: list[str] = []
    for normalization in cast(list[object], raw_normalizations):
        if not isinstance(normalization, str):
            raise ImporterError(
                "CANDIDATE_SHAPE", "normalization descriptions must be text", "candidate"
            )
        normalizations.append(normalization)
    raw_elements = item.get("dtd_elements")
    raw_entries = item.get("sdk_entries")
    if not isinstance(raw_elements, list) or not isinstance(raw_entries, list):
        raise ImporterError(
            "CANDIDATE_SHAPE", "'dtd_elements' and 'sdk_entries' must be arrays", "candidate"
        )
    dtd_elements = tuple(
        _dtd_element(entry, f"candidate.dtd_elements[{index}]")
        for index, entry in enumerate(cast(list[object], raw_elements))
    )
    sdk_entries = tuple(
        _sdk_entry(entry, f"candidate.sdk_entries[{index}]")
        for index, entry in enumerate(cast(list[object], raw_entries))
    )
    if source.kind == "dtd" and sdk_entries:
        raise ImporterError("CANDIDATE_SHAPE", "DTD candidate contains SDK entries", "candidate")
    if source.kind == "sdk-html" and dtd_elements:
        raise ImporterError("CANDIDATE_SHAPE", "SDK candidate contains DTD elements", "candidate")
    return CandidateDocument(
        source=source,
        scope=scope,
        normalizations=tuple(normalizations),
        dtd_elements=dtd_elements,
        sdk_entries=sdk_entries,
    )
