# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ObjectTag ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_3f4a0fdb9e9d93eccd4e
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ObjectTag",
    xml_tag="objecttag",
    cdx_id=32785,
    cdx_constant="kCDXObj_ObjectTag",
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
        "stoichiometry_grid",
        "sg_component",
        "sg_datum",
        "plasmid_map",
        "plasmid_region",
        "plasmid_marker",
        "bio_shape",
    ),
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
            "dtd.objecttag.display_name": PROPERTY_METADATA["dtd.objecttag.display_name"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.objecttag.value": PROPERTY_METADATA["dtd.objecttag.value"],
            "dtd.objecttag.tracking": PROPERTY_METADATA["dtd.objecttag.tracking"],
            "dtd.objecttag.tag_type": PROPERTY_METADATA["dtd.objecttag.tag_type"],
            "dtd.objecttag.positioning_type": PROPERTY_METADATA["dtd.objecttag.positioning_type"],
            "dtd.objecttag.positioning_offset": PROPERTY_METADATA[
                "dtd.objecttag.positioning_offset"
            ],
            "dtd.objecttag.positioning_angle": PROPERTY_METADATA["dtd.objecttag.positioning_angle"],
            "dtd.objecttag.persistent": PROPERTY_METADATA["dtd.objecttag.persistent"],
            "dtd.objecttag.name": PROPERTY_METADATA["dtd.objecttag.name"],
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_3f4a0fdb9e9d93eccd4e,),
)
