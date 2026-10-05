# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the RegistryNumber ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_46cd5f738f07c84565d6
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="RegistryNumber",
    xml_tag="regnum",
    cdx_id=32780,
    cdx_constant="kCDXObj_RegistryNumber",
    category="document_object",
    id_scope="document",
    allowed_parents=("fragment",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.regnum.registry_number": PROPERTY_METADATA["dtd.regnum.registry_number"],
            "dtd.regnum.registry_authority": PROPERTY_METADATA["dtd.regnum.registry_authority"],
        }
    ),
    provenance=(P_46cd5f738f07c84565d6,),
)
