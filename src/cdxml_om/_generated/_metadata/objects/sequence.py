# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Sequence ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_4a4a52aab8c87acff745
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Sequence",
    xml_tag="sequence",
    cdx_id=32787,
    cdx_constant="kCDXObj_Sequence",
    category="document_object",
    id_scope="none",
    allowed_parents=("page",),
    status="known",
    children=(
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.sequence.sequence_identifier": PROPERTY_METADATA[
                "dtd.sequence.sequence_identifier"
            ],
        }
    ),
    provenance=(P_4a4a52aab8c87acff745,),
)
