"""Shared XML attribute spelling resolution for generated property metadata."""

from __future__ import annotations

from lxml import etree

from cdxml_om._generated.schema_metadata import PropertyMetadata
from cdxml_om.core.errors import CodecError


def property_xml_names(prop: PropertyMetadata) -> tuple[str, ...]:
    """Return a property's canonical XML name followed by sourced aliases."""
    return (prop.xml_name, *prop.xml_aliases)


def read_property_attribute(
    element: etree.Element, prop: PropertyMetadata, property_id: str
) -> tuple[str | None, str | None]:
    """Return one present attribute spelling, or reject conflicting spellings.

    Attribute resolution stays lazy: a document containing both names parses
    and retains its raw tree; only typed access or validation reports conflict.
    The returned name lets mutation preserve the spelling present in the input.
    """
    present = [name for name in property_xml_names(prop) if name in element.attrib]
    if len(present) > 1:
        values = ", ".join(f"{name}={element.get(name)!r}" for name in present)
        raise CodecError(
            f"property {property_id!r} has conflicting XML spellings: {values}",
            property_id=property_id,
            raw_value=values,
            xml_tag=element.tag if isinstance(element.tag, str) else None,
        )
    if not present:
        return None, None
    name = present[0]
    return element.get(name), name


__all__ = ["property_xml_names", "read_property_attribute"]
