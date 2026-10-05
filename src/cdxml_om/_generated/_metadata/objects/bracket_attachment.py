# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the BracketAttachment ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_39cbdc5f55d4638594da
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="BracketAttachment",
    xml_tag="bracketattachment",
    cdx_id=32792,
    cdx_constant="kCDXObj_BracketAttachment",
    category="document_object",
    id_scope="document",
    allowed_parents=("bracketed_group",),
    status="known",
    children=(
        ChildMetadata(
            object_type="crossing_bond",
            collection_name="crossingbonds",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.bracketattachment.graphic_id": PROPERTY_METADATA[
                "dtd.bracketattachment.graphic_id"
            ],
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_39cbdc5f55d4638594da,),
)
