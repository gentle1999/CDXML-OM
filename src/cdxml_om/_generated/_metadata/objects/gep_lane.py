# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the GEPLane ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_25c46b8039882988a8f1
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="GEPLane",
    xml_tag="geplane",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("gep_plate",),
    status="known",
    children=(
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="gep_band",
            collection_name="gepbands",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.gepplate.label_text": PROPERTY_METADATA["dtd.gepplate.label_text"],
        }
    ),
    provenance=(P_25c46b8039882988a8f1,),
)
