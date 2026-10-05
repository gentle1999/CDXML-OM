"""Exact tag dispatch and identity-preserving wrapper/object indexes."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, cast

from lxml import etree

from cdxml_om._generated.schema_metadata import DATATYPE_METADATA, OBJECT_METADATA
from cdxml_om._generated.schema_registry import OBJECT_BY_XML_TAG
from cdxml_om.core.codecs import decode_property_value
from cdxml_om.core.errors import CodecError, MutationError, ReferenceResolutionError
from cdxml_om.core.models import CDXMLElement, UnknownElement

if TYPE_CHECKING:
    from cdxml_om.core.document import CDXMLDocument

T = TypeVar("T", bound=CDXMLElement)
_SPEC_ID_BY_MODEL = {
    OBJECT_BY_XML_TAG[metadata.xml_tag]: spec_id
    for spec_id, metadata in OBJECT_METADATA.items()
    if metadata.xml_tag in OBJECT_BY_XML_TAG
}


@dataclass(frozen=True, slots=True)
class ObjectReference:
    """One parseable raw reference attribute targeting a document ID."""

    source: CDXMLElement
    property_id: str
    target_id: int


class ModelRegistry(Mapping[str, type[CDXMLElement]]):
    """Read-only registry matching XML tags exactly (including namespaces)."""

    __slots__ = ()

    def __getitem__(self, xml_tag: str) -> type[CDXMLElement]:
        return OBJECT_BY_XML_TAG[xml_tag]

    def __iter__(self) -> Iterator[str]:
        return iter(OBJECT_BY_XML_TAG)

    def __len__(self) -> int:
        return len(OBJECT_BY_XML_TAG)

    def for_tag(self, xml_tag: str) -> type[CDXMLElement] | None:
        return OBJECT_BY_XML_TAG.get(xml_tag)


MODEL_REGISTRY = ModelRegistry()


class ObjectRegistry:
    """Caches wrapper identity and resolves current modeled object IDs by tree scan."""

    __slots__ = ("_document", "_tree", "_wrappers")

    def __init__(self, document: CDXMLDocument, tree: etree.ElementTree) -> None:
        self._document = document
        self._tree = tree
        self._wrappers: dict[etree.Element, CDXMLElement] = {}

    def wrap(self, element: etree.Element) -> CDXMLElement:
        wrapper = self._wrappers.get(element)
        if wrapper is not None:
            return wrapper
        model = MODEL_REGISTRY.for_tag(element.tag) if isinstance(element.tag, str) else None
        if model is None and element.tag == "CDXML" and element.getparent() is None:
            wrapper_type = CDXMLElement
        else:
            wrapper_type = model or UnknownElement
        wrapper = wrapper_type(self._document, element)
        self._wrappers[element] = wrapper
        return wrapper

    def by_id(
        self,
        object_id: object,
        model_type: type[T] | None = None,
    ) -> T | CDXMLElement | None:
        if isinstance(object_id, bool) or not isinstance(object_id, int):
            raise TypeError("object ID lookup requires an integer (not bool)")
        datatype = DATATYPE_METADATA["object_id"]
        if datatype.minimum is not None and object_id < datatype.minimum:
            raise ValueError(f"object ID must be at least {datatype.minimum}")
        if datatype.maximum is not None and object_id > datatype.maximum:
            raise ValueError(f"object ID must be at most {datatype.maximum}")
        elements = self.elements_by_id(object_id)
        if len(elements) > 1:
            raise ReferenceResolutionError(
                f"object ID {object_id} is ambiguous across {len(elements)} XML elements"
            )
        wrappers = [self.wrap(element) for element in elements]
        if model_type is not None:
            wrappers = [wrapper for wrapper in wrappers if isinstance(wrapper, model_type)]
        if not wrappers:
            return None
        if model_type is not None:
            return cast(T, wrappers[0])
        return wrappers[0]

    def elements_by_id(self, object_id: int) -> tuple[etree.Element, ...]:
        """Return all document-scoped modeled nodes with this valid ID."""
        datatype = DATATYPE_METADATA["object_id"]
        if datatype.minimum is not None and object_id < datatype.minimum:
            raise ValueError(f"object ID must be at least {datatype.minimum}")
        if datatype.maximum is not None and object_id > datatype.maximum:
            raise ValueError(f"object ID must be at most {datatype.maximum}")
        elements: list[etree.Element] = []
        for element in self._tree.iter():
            if not isinstance(element.tag, str) or element.tag not in OBJECT_BY_XML_TAG:
                # Unknown tags may use `id` for non-object resources (font,
                # color, and similar tables); no global scope is inferred.
                continue
            model = OBJECT_BY_XML_TAG[element.tag]
            spec_id = _SPEC_ID_BY_MODEL[model]
            metadata = OBJECT_METADATA[spec_id]
            if metadata.id_scope != "document":
                continue
            id_property = next(
                (
                    prop_id
                    for prop_id, prop in metadata.properties.items()
                    if prop.name == "id" and prop.datatype == "object_id"
                ),
                None,
            )
            if id_property is None:
                continue
            prop = metadata.properties[id_property]
            raw_id = element.get(prop.xml_name)
            if raw_id is None:
                continue
            try:
                candidate_id = decode_property_value(id_property, raw_id)
            except CodecError:
                continue
            if candidate_id == object_id:
                elements.append(element)
        return tuple(elements)

    def references_to(self, target: CDXMLElement) -> tuple[ObjectReference, ...]:
        """List parseable raw references matching a same-document wrapper's current ID."""
        if target.document is not self._document:
            raise MutationError("reference target belongs to a different document")
        model = type(target)
        spec_id = _SPEC_ID_BY_MODEL.get(model)
        if spec_id is None or OBJECT_METADATA[spec_id].id_scope != "document":
            raise MutationError("reference target has no document-scoped object ID")
        metadata = OBJECT_METADATA[spec_id]
        id_property = next(
            (
                prop_id
                for prop_id, prop in metadata.properties.items()
                if prop.name == "id" and prop.datatype == "object_id"
            ),
            None,
        )
        if id_property is None:
            raise MutationError("reference target model has no object ID property")
        raw_id = target.raw_element.get(metadata.properties[id_property].xml_name)
        if raw_id is None:
            return ()
        try:
            target_id = decode_property_value(id_property, raw_id)
        except CodecError:
            return ()
        if not isinstance(target_id, int) or isinstance(target_id, bool):
            return ()

        references: list[ObjectReference] = []
        for element in self._tree.iter():
            if not isinstance(element.tag, str) or element.tag not in OBJECT_BY_XML_TAG:
                continue
            source_model = OBJECT_BY_XML_TAG[element.tag]
            source_spec_id = _SPEC_ID_BY_MODEL[source_model]
            source_metadata = OBJECT_METADATA[source_spec_id]
            for property_id, prop in source_metadata.properties.items():
                if prop.reference_target is None:
                    continue
                raw_value = element.get(prop.xml_name)
                if raw_value is None:
                    continue
                try:
                    value = decode_property_value(property_id, raw_value)
                except CodecError:
                    continue
                values: tuple[object, ...] = (
                    cast(tuple[object, ...], value) if isinstance(value, tuple) else (value,)
                )
                if target_id in values:
                    references.append(ObjectReference(self.wrap(element), property_id, target_id))
        return tuple(references)


__all__ = ["MODEL_REGISTRY", "ModelRegistry", "ObjectReference", "ObjectRegistry"]
