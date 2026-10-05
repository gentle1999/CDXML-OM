# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Annotation ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_45320a91cd399063417b
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Annotation",
    xml_tag="annotation",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=(
        "page",
        "group",
        "fragment",
        "text",
        "node",
        "bond",
        "graphic",
        "arrow",
        "curve",
        "alt_group",
        "geometry",
        "constraint",
        "spectrum",
        "embedded_object",
        "table",
        "tlc_plate",
        "tlc_lane",
        "tlc_spot",
        "gep_plate",
        "gep_lane",
        "gep_band",
        "marker",
        "stoichiometry_grid",
        "plasmid_map",
        "plasmid_region",
        "plasmid_marker",
        "bio_shape",
    ),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.annotation.content": PROPERTY_METADATA["dtd.annotation.content"],
            "dtd.annotation.keyword": PROPERTY_METADATA["dtd.annotation.keyword"],
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_45320a91cd399063417b,),
)
