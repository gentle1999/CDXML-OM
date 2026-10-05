"""Machine-readable review diff from imported evidence to canonical schema."""

from __future__ import annotations

from dataclasses import asdict

from tools.schema_compiler.ir import ObjectSpec, PropertySpec, Schema
from tools.schema_importer.candidate import (
    CandidateDocument,
    ContentModelCandidate,
    DTDAttributeCandidate,
    DTDElementCandidate,
    SDKEntryCandidate,
)

DiffEntry = dict[str, object]


def _entry(kind: str, target: str, **evidence: object) -> DiffEntry:
    serializable = {
        key: asdict(value)
        if isinstance(
            value,
            (ContentModelCandidate, DTDAttributeCandidate, DTDElementCandidate, SDKEntryCandidate),
        )
        else value
        for key, value in evidence.items()
    }
    return {"kind": kind, "target": target, **serializable}


def _object_properties(schema: Schema, obj: ObjectSpec) -> tuple[PropertySpec, ...]:
    ids = set(obj.properties)
    return tuple(prop for prop in schema.properties if prop.id in ids)


def _dtd_diff(candidate: CandidateDocument, schema: Schema) -> list[DiffEntry]:
    differences: list[DiffEntry] = []
    object_by_tag = {obj.xml_tag: obj for obj in schema.objects}
    dtd_by_tag = {item.xml_name: item for item in candidate.dtd_elements}

    for item in candidate.dtd_elements:
        obj = object_by_tag.get(item.xml_name)
        if obj is None:
            differences.append(_entry("added", f"object:{item.xml_name}", evidence=item))
            continue

        properties = _object_properties(schema, obj)
        canonical_attributes = {
            prop.xml_name: prop for prop in properties if prop.storage == "attribute"
        }
        source_attributes = {attribute.name: attribute for attribute in item.attributes}
        for name, attribute in source_attributes.items():
            prop = canonical_attributes.get(name)
            if prop is None:
                differences.append(
                    _entry(
                        "added",
                        f"attribute:{item.xml_name}.{name}",
                        evidence=attribute,
                    )
                )
                continue
            if attribute.required != prop.required:
                differences.append(
                    _entry(
                        "changed",
                        f"attribute:{item.xml_name}.{name}",
                        field="required",
                        canonical=prop.required,
                        candidate=attribute.required,
                        evidence=attribute,
                    )
                )
            canonical_default = None if prop.default is None else str(prop.default)
            if attribute.default_value != canonical_default:
                differences.append(
                    _entry(
                        "changed",
                        f"attribute:{item.xml_name}.{name}.default",
                        canonical=canonical_default,
                        candidate=attribute.default_value,
                        candidate_default_kind=attribute.default_kind,
                        interpretation="lexical comparison only; no datatype normalization applied",
                        evidence=attribute,
                    )
                )

            canonical_enum: tuple[str, ...] | None = None
            if prop.enum is not None:
                enum = next((value for value in schema.enums if value.id == prop.enum), None)
                if enum is not None:
                    canonical_enum = tuple(value.xml_value for value in enum.values)
            source_enum = attribute.enum_values or None
            if source_enum != canonical_enum and (
                source_enum is not None or canonical_enum is not None
            ):
                differences.append(
                    _entry(
                        "changed",
                        f"attribute:{item.xml_name}.{name}.enum_values",
                        canonical=None if canonical_enum is None else list(canonical_enum),
                        candidate=None if source_enum is None else list(source_enum),
                        interpretation="raw lexical alternatives; no enum normalization applied",
                        evidence=attribute,
                    )
                )

            if attribute.declared_type.casefold() != "cdata":
                differences.append(
                    _entry(
                        "changed",
                        f"attribute:{item.xml_name}.{name}.declared_type",
                        canonical=prop.datatype,
                        candidate=attribute.declared_type,
                        interpretation="raw DTD declared type; no datatype mapping applied",
                        evidence=attribute,
                    )
                )

        for name, prop in canonical_attributes.items():
            if name not in source_attributes:
                differences.append(
                    _entry(
                        "missing",
                        f"attribute:{item.xml_name}.{name}",
                        canonical_property_id=prop.id,
                    )
                )

        canonical_children = tuple(
            child.xml_tag
            for child in schema.objects
            if any(link.object_type == child.id for link in obj.children)
        )
        if set(item.children) != set(canonical_children):
            differences.append(
                _entry(
                    "changed",
                    f"children:{item.xml_name}",
                    canonical=list(canonical_children),
                    candidate=list(item.children),
                    evidence=item.content_model,
                )
            )

    for obj in schema.objects:
        if obj.xml_tag not in dtd_by_tag:
            differences.append(
                _entry("missing", f"object:{obj.xml_tag}", canonical_object_id=obj.id)
            )
    return differences


def _sdk_expected_namespace(obj: ObjectSpec) -> str:
    if obj.cdx_id is not None or obj.cdx_constant is not None:
        return "object"
    return "xml-only"


def _sdk_diff(candidate: CandidateDocument, schema: Schema) -> list[DiffEntry]:
    differences: list[DiffEntry] = []
    objects_by_xml = {obj.xml_tag: obj for obj in schema.objects}

    if candidate.scope == "inventory":
        seen: set[str] = set()
        for item in candidate.sdk_entries:
            if item.relation != "inventory":
                continue
            obj = objects_by_xml.get(item.xml_name or "")
            if obj is None:
                differences.append(
                    _entry(
                        "added",
                        f"sdk:{item.namespace}:{item.xml_name or item.cdx_constant}",
                        evidence=item,
                    )
                )
                continue
            seen.add(obj.id)
            expected_namespace = _sdk_expected_namespace(obj)
            if item.namespace != expected_namespace:
                differences.append(
                    _entry(
                        "changed",
                        f"namespace:{obj.xml_tag}",
                        field="CDX namespace",
                        canonical=expected_namespace,
                        candidate=item.namespace,
                        evidence=item,
                    )
                )
            if item.cdx_id != obj.cdx_id:
                differences.append(
                    _entry(
                        "changed",
                        f"object:{obj.xml_tag}.cdx_id",
                        canonical=obj.cdx_id,
                        candidate=item.cdx_id,
                        candidate_lexical=item.value_text,
                        evidence=item,
                    )
                )
            if item.cdx_constant != obj.cdx_constant:
                differences.append(
                    _entry(
                        "changed",
                        f"object:{obj.xml_tag}.cdx_constant",
                        canonical=obj.cdx_constant,
                        candidate=item.cdx_constant,
                        evidence=item,
                    )
                )
        for obj in schema.objects:
            if (obj.cdx_id is not None or obj.cdx_constant is not None) and obj.id not in seen:
                differences.append(
                    _entry("missing", f"object:{obj.xml_tag}", canonical_object_id=obj.id)
                )
        return differences

    summaries = [item for item in candidate.sdk_entries if item.relation == "summary"]
    for item in summaries:
        obj = objects_by_xml.get(item.xml_name or "")
        if obj is None:
            differences.append(
                _entry("added", f"object:{item.xml_name or item.cdx_constant}", evidence=item)
            )
            continue
        expected_namespace = _sdk_expected_namespace(obj)
        if item.namespace != expected_namespace:
            differences.append(
                _entry(
                    "changed",
                    f"namespace:{obj.xml_tag}",
                    field="CDX namespace",
                    canonical=expected_namespace,
                    candidate=item.namespace,
                    evidence=item,
                )
            )
        if item.cdx_id != obj.cdx_id:
            differences.append(
                _entry(
                    "changed",
                    f"object:{obj.xml_tag}.cdx_id",
                    canonical=obj.cdx_id,
                    candidate=item.cdx_id,
                    candidate_lexical=item.value_text,
                    evidence=item,
                )
            )
        if item.cdx_constant != obj.cdx_constant:
            differences.append(
                _entry(
                    "changed",
                    f"object:{obj.xml_tag}.cdx_constant",
                    canonical=obj.cdx_constant,
                    candidate=item.cdx_constant,
                    evidence=item,
                )
            )

    properties_by_tag = {
        obj.xml_tag: {prop.xml_name: prop for prop in _object_properties(schema, obj)}
        for obj in schema.objects
    }
    observed: dict[str, set[str]] = {}
    for item in candidate.sdk_entries:
        if item.relation != "property" or item.xml_name is None:
            continue
        owner_tag = item.owner_xml_name or ""
        owner = objects_by_xml.get(owner_tag)
        prop = properties_by_tag.get(owner_tag, {}).get(item.xml_name)
        observed.setdefault(owner_tag, set()).add(item.xml_name)
        target = f"property:{owner_tag}.{item.xml_name}"
        if owner is None or prop is None:
            differences.append(_entry("added", target, evidence=item))
            continue
        if item.cdx_id != prop.cdx_id:
            differences.append(
                _entry(
                    "changed",
                    f"{target}.cdx_id",
                    canonical=prop.cdx_id,
                    candidate=item.cdx_id,
                    candidate_lexical=item.value_text,
                    evidence=item,
                )
            )
        if item.cdx_constant != prop.cdx_constant:
            differences.append(
                _entry(
                    "changed",
                    f"{target}.cdx_constant",
                    canonical=prop.cdx_constant,
                    candidate=item.cdx_constant,
                    evidence=item,
                )
            )
        if item.type_name is not None and item.type_name != prop.datatype:
            differences.append(
                _entry(
                    "changed",
                    f"{target}.type_evidence",
                    canonical=prop.datatype,
                    candidate=item.type_name,
                    interpretation="raw SDK type evidence; no normalization applied",
                    evidence=item,
                )
            )

    for item in summaries:
        owner_tag = item.xml_name or ""
        for name, prop in properties_by_tag.get(owner_tag, {}).items():
            if name not in observed.get(owner_tag, set()):
                differences.append(
                    _entry("missing", f"property:{owner_tag}.{name}", canonical_property_id=prop.id)
                )
    return differences


def compare_candidate(candidate: CandidateDocument, schema: Schema) -> dict[str, object]:
    """Compare source evidence without converting its syntax into semantics."""
    if candidate.source.kind == "dtd":
        differences = _dtd_diff(candidate, schema)
    else:
        differences = _sdk_diff(candidate, schema)
    differences.sort(key=lambda item: (str(item["kind"]), str(item["target"])))
    return {
        "format": "cdxml-om-schema-diff",
        "format_version": 1,
        "candidate_source": {
            "kind": candidate.source.kind,
            "path": candidate.source.path,
            "sha256": candidate.source.sha256,
        },
        "candidate_scope": candidate.scope,
        "canonical_schema_version": schema.version,
        "differences": differences,
        "summary": {
            "added": sum(item["kind"] == "added" for item in differences),
            "changed": sum(item["kind"] == "changed" for item in differences),
            "missing": sum(item["kind"] == "missing" for item in differences),
        },
    }
