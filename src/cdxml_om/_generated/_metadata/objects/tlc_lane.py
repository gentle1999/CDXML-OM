# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TLCLane ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_57aa9d8d40800ec07874
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="TLCLane",
    xml_tag="tlclane",
    cdx_id=32804,
    cdx_constant="kCDXObj_TLCLane",
    category="document_object",
    id_scope="document",
    allowed_parents=("tlc_plate",),
    status="known",
    children=(
        ChildMetadata(
            object_type="object_tag",
            collection_name="objecttags",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="tlc_spot",
            collection_name="tlcspots",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "common.visible": PROPERTY_METADATA["common.visible"],
        }
    ),
    provenance=(P_57aa9d8d40800ec07874,),
)
