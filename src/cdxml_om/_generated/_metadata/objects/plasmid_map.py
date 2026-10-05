# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the PlasmidMap ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_7af2b8a54e18af073590
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="PlasmidMap",
    xml_tag="plasmidmap",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group"),
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
            object_type="plasmid_region",
            collection_name="plasmidregions",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="plasmid_marker",
            collection_name="plasmidmarkers",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="graphic",
            collection_name="graphics",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.plasmidmap.ring_radius": PROPERTY_METADATA["dtd.plasmidmap.ring_radius"],
            "node.position": PROPERTY_METADATA["node.position"],
            "dtd.plasmidmap.number_base_pairs": PROPERTY_METADATA[
                "dtd.plasmidmap.number_base_pairs"
            ],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
        }
    ),
    provenance=(P_7af2b8a54e18af073590,),
)
