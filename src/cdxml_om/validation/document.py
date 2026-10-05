"""Validation rules implemented from generated schema metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast

from lxml import etree

from cdxml_om._generated.schema_metadata import OBJECT_METADATA, PROPERTY_METADATA
from cdxml_om._generated.schema_registry import OBJECT_BY_XML_TAG
from cdxml_om.core.attributes import read_property_attribute
from cdxml_om.core.codecs import decode_property_value
from cdxml_om.core.errors import CodecError
from cdxml_om.core.models import CDXMLElement
from cdxml_om.validation import ValidationIssue, ValidationReport

if TYPE_CHECKING:
    from cdxml_om.core.document import CDXMLDocument

_SPEC_ID_BY_XML_TAG = {metadata.xml_tag: spec_id for spec_id, metadata in OBJECT_METADATA.items()}


def validate_document(document: CDXMLDocument) -> ValidationReport:
    """Check supported schema constraints without changing the retained tree."""
    tree = document.tree
    wrap = document.wrap
    issues: list[ValidationIssue] = []
    known_nodes: list[tuple[etree.Element, CDXMLElement, str]] = []

    def add(
        code: str,
        message: str,
        element: etree.Element,
        property_id: str | None = None,
        *,
        severity: Literal["error", "warning"] = "error",
    ) -> None:
        issues.append(ValidationIssue(code, message, wrap(element), property_id, severity))

    for element in tree.iter():
        if not isinstance(element.tag, str):
            continue
        model_type = OBJECT_BY_XML_TAG.get(element.tag)
        if model_type is None:
            continue
        object_id = _SPEC_ID_BY_XML_TAG[element.tag]
        metadata = OBJECT_METADATA[object_id]
        known_nodes.append((element, wrap(element), object_id))

        parent = element.getparent()
        parent_spec_id: str | None = None
        if parent is not None and isinstance(parent.tag, str):
            if parent.tag in _SPEC_ID_BY_XML_TAG:
                parent_spec_id = _SPEC_ID_BY_XML_TAG[parent.tag]
            elif parent.tag == "CDXML":
                parent_spec_id = "$document"
        if element is not tree.getroot():
            if parent is not None and parent_spec_id is None:
                add(
                    "unvalidated-parent",
                    "parent tag is not modeled; its child constraints are not validated",
                    element,
                    severity="warning",
                )
            elif parent_spec_id not in metadata.allowed_parents:
                add(
                    "invalid-parent",
                    f"{metadata.python_name} is not allowed beneath "
                    f"{parent_spec_id or 'an unknown element'}",
                    element,
                )

        for prop_id, prop in metadata.properties.items():
            raw_value: str | None
            if prop.storage == "text":
                raw_value = (
                    (element.text or "") + "".join(child.tail or "" for child in element)
                    if element.tag == "spectrum"
                    else "".join(element.itertext())
                )
            else:
                try:
                    raw_value, _ = read_property_attribute(element, prop, prop_id)
                except CodecError as exc:
                    add("conflicting-property-alias", str(exc), element, prop_id)
                    continue
            if raw_value is None:
                if prop.required and prop.default is None:
                    add(
                        "missing-required-property",
                        f"required XML attribute {prop.xml_name!r} is missing",
                        element,
                        prop_id,
                    )
                continue
            try:
                decode_property_value(prop_id, raw_value, context_attributes=dict(element.attrib))
            except CodecError as exc:
                add("invalid-value", str(exc), element, prop_id)

        for child_spec in metadata.children:
            child_meta = OBJECT_METADATA[child_spec.object_type]
            actual_children = sum(
                1
                for child in element
                if isinstance(child.tag, str) and child.tag == child_meta.xml_tag
            )
            if actual_children < child_spec.min_occurs or (
                child_spec.max_occurs is not None and actual_children > child_spec.max_occurs
            ):
                upper_bound = (
                    child_spec.max_occurs if child_spec.max_occurs is not None else "unbounded"
                )
                add(
                    "child-cardinality",
                    f"{metadata.python_name}.{child_spec.collection_name} contains "
                    f"{actual_children}; expected {child_spec.min_occurs}.."
                    f"{upper_bound}",
                    element,
                )

    ids_by_value: dict[int, list[tuple[etree.Element, CDXMLElement]]] = {}
    local_ids_by_scope: dict[tuple[etree.Element, int], list[tuple[etree.Element, str]]] = {}
    for element, wrapper, object_spec_id in known_nodes:
        metadata = OBJECT_METADATA[object_spec_id]
        if metadata.id_scope == "none":
            continue
        id_prop = next(
            (prop_id for prop_id, prop in metadata.properties.items() if prop.name == "id"),
            None,
        )
        if id_prop is None:
            continue
        prop = PROPERTY_METADATA[id_prop]
        raw_id = element.get(prop.xml_name)
        if raw_id is None:
            continue
        try:
            object_id_value = decode_property_value(id_prop, raw_id)
        except CodecError:
            continue
        if not isinstance(object_id_value, int) or isinstance(object_id_value, bool):
            continue
        if metadata.id_scope == "document":
            ids_by_value.setdefault(object_id_value, []).append((element, wrapper))
        elif metadata.id_scope == "local":
            parent = element.getparent()
            if parent is not None:
                local_ids_by_scope.setdefault((parent, object_id_value), []).append(
                    (element, id_prop)
                )

    for numeric_id, matching_objects in ids_by_value.items():
        if len(matching_objects) > 1:
            for element, _ in matching_objects:
                add(
                    "duplicate-id",
                    f"document-scoped object ID {numeric_id} occurs {len(matching_objects)} times",
                    element,
                    "common.id",
                )

    for (scope_element, local_id), matching_local_ids in local_ids_by_scope.items():
        if len(matching_local_ids) > 1:
            scope_name = (
                scope_element.tag if isinstance(scope_element.tag, str) else "unknown table"
            )
            for element, property_id in matching_local_ids:
                add(
                    "duplicate-local-id",
                    f"local ID {local_id} occurs {len(matching_local_ids)} times in {scope_name!r}",
                    element,
                    property_id,
                )

    for element, _, object_spec_id in known_nodes:
        metadata = OBJECT_METADATA[object_spec_id]
        for property_id, prop in metadata.properties.items():
            if prop.reference_target is None:
                continue
            try:
                raw_value, _ = read_property_attribute(element, prop, property_id)
            except CodecError:
                # The property pass above reports conflicting spellings once.
                continue
            if raw_value is None:
                continue
            try:
                target_ids = decode_property_value(property_id, raw_value)
            except CodecError:
                continue
            values: tuple[object, ...] = (
                cast(tuple[object, ...], target_ids)
                if isinstance(target_ids, tuple)
                else (target_ids,)
            )
            expected = (
                OBJECT_METADATA[prop.reference_target] if prop.reference_target != "*" else None
            )
            for target_id in values:
                if not isinstance(target_id, int) or isinstance(target_id, bool):
                    continue
                target_matches = ids_by_value.get(target_id, [])
                if not target_matches:
                    add(
                        "dangling-reference",
                        f"{property_id} refers to missing object ID {target_id}",
                        element,
                        property_id,
                    )
                elif len(target_matches) > 1:
                    add(
                        "ambiguous-reference",
                        f"{property_id} refers to ambiguous object ID {target_id}",
                        element,
                        property_id,
                    )
                else:
                    actual_tag = target_matches[0][0].tag
                    if not isinstance(actual_tag, str):
                        continue
                    actual_spec_id = _SPEC_ID_BY_XML_TAG[actual_tag]
                    actual_model = OBJECT_BY_XML_TAG[actual_tag]
                    if prop.reference_target != "*" and actual_spec_id != prop.reference_target:
                        expected_name = (
                            expected.python_name if expected is not None else "a document object"
                        )
                        add(
                            "wrong-reference-target",
                            f"{property_id} targets {actual_model.__name__}, "
                            f"expected {expected_name}",
                            element,
                            property_id,
                        )

    return ValidationReport(tuple(issues))


__all__ = ["validate_document"]
