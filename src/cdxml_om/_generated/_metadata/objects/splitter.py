# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Splitter ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_b8dace1b20cfb3672e44
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Splitter",
    xml_tag="splitter",
    cdx_id=32789,
    cdx_constant="kCDXObj_Splitter",
    category="document_object",
    id_scope="none",
    allowed_parents=("page",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "node.position": PROPERTY_METADATA["node.position"],
            "dtd.page.page_definition": PROPERTY_METADATA["dtd.page.page_definition"],
        }
    ),
    provenance=(P_b8dace1b20cfb3672e44,),
)
