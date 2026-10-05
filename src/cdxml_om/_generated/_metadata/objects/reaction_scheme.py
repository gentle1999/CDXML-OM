# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ReactionScheme ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_c0375afa847e581fe858
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ReactionScheme",
    xml_tag="scheme",
    cdx_id=32781,
    cdx_constant="kCDXObj_ReactionScheme",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group"),
    status="known",
    children=(
        ChildMetadata(
            object_type="reaction_step",
            collection_name="steps",
            min_occurs=1,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_c0375afa847e581fe858,),
)
