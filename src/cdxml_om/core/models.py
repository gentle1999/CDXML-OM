"""XML-backed base types for generated CDXML declarations."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING, TypeVar, cast

from lxml import etree

if TYPE_CHECKING:
    from cdxml_om.core.document import CDXMLDocument
    from cdxml_om.core.fields import ChildCollection, ElementCollection, Field

T = TypeVar("T")


class CDXMLElement:
    """A stable typed view over one element in a retained XML tree."""

    __slots__ = ("_document", "_element")

    def __init__(self, document: CDXMLDocument, element: etree.Element) -> None:
        self._document = document
        self._element = element

    def __cdxml_read_field__(self, descriptor: Field[T]) -> T:
        return cast(T, self._document.read_field(self._element, descriptor.property_id))

    def __cdxml_write_field__(self, descriptor: Field[T], value: T) -> None:
        self._document.write_field(self._element, descriptor.property_id, value)

    def __cdxml_read_collection__(self, descriptor: ChildCollection[T]) -> ElementCollection[T]:
        return cast(
            "ElementCollection[T]",
            self._document.read_collection(self._element, descriptor.object_type),
        )

    @property
    def document(self) -> CDXMLDocument:
        return self._document

    @property
    def raw_element(self) -> etree.Element:
        """The original lxml node; direct edits bypass typed validation/mutation APIs."""
        return self._element

    @property
    def xml_tag(self) -> str:
        tag = self._element.tag
        return tag if isinstance(tag, str) else ""

    @property
    def raw_attributes(self) -> Mapping[str, str]:
        """A read-only snapshot of all attributes, including unknown ones."""
        return MappingProxyType(dict(self._element.attrib))

    @property
    def parent(self) -> CDXMLElement | None:
        parent = self._element.getparent()
        return self._document.wrap(parent) if parent is not None else None

    @property
    def children(self) -> tuple[CDXMLElement, ...]:
        return tuple(
            self._document.wrap(child) for child in self._element if isinstance(child.tag, str)
        )

    @property
    def text(self) -> str | None:
        return self._element.text

    @property
    def tail(self) -> str | None:
        return self._element.tail

    def raw_reference_id(self, property_id: str) -> int | tuple[int, ...] | None:
        """Read the encoded ID(s) for a schema-declared reference without resolving them."""
        return self._document.raw_reference_id(self._element, property_id)

    def raw_reference_ids(self, property_id: str) -> tuple[int, ...] | None:
        """Read raw IDs for a many-valued reference, without resolving targets."""
        value = self._document.raw_reference_id(self._element, property_id)
        if value is None:
            return None
        if isinstance(value, int):
            raise ValueError(f"{property_id!r} is not a many-valued reference")
        return value

    @property
    def plain_text(self) -> str:
        """Concatenate descendant CDXML rich-text run character data."""
        return "".join(
            text
            for child in self._element.iter()
            if isinstance(child.tag, str) and child.tag == "s"
            for text in child.itertext()
        )


class UnknownElement(CDXMLElement):
    """Navigable wrapper for tags absent from the exact generated registry."""

    __slots__ = ()

    @property
    def id(self) -> int | None:
        """Decoded common object ID when an unknown element has that attribute."""
        raw_value = self._element.get("id")
        if raw_value is None:
            return None
        return cast(int, self._document.decode_value("common.id", raw_value, self._element))


__all__ = ["CDXMLElement", "UnknownElement"]
