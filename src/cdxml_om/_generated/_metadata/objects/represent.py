# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Represent ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_4826a9cfcb494405b861
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Represent",
    xml_tag="represent",
    cdx_id=None,
    cdx_constant=None,
    category="property_element",
    id_scope="none",
    allowed_parents=("graphic",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.represent.attribute_id": PROPERTY_METADATA["dtd.represent.attribute_id"],
            "dtd.represent.object_reference": PROPERTY_METADATA["dtd.represent.object_reference"],
        }
    ),
    provenance=(P_4826a9cfcb494405b861,),
)
