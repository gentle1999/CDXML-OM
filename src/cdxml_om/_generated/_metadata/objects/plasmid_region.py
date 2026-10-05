# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the PlasmidRegion ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_0fb307ce26c1d1783b42
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="PlasmidRegion",
    xml_tag="plasmidregion",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("plasmid_map",),
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
            object_type="plasmid_marker",
            collection_name="plasmidmarkers",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "arrow.tail_3d": PROPERTY_METADATA["arrow.tail_3d"],
            "dtd.plasmidregion.region_start": PROPERTY_METADATA["dtd.plasmidregion.region_start"],
            "dtd.plasmidregion.region_offset": PROPERTY_METADATA["dtd.plasmidregion.region_offset"],
            "dtd.plasmidregion.region_end": PROPERTY_METADATA["dtd.plasmidregion.region_end"],
            "dtd.arrow.minor_axis_end3_d": PROPERTY_METADATA["dtd.arrow.minor_axis_end3_d"],
            "dtd.arrow.major_axis_end3_d": PROPERTY_METADATA["dtd.arrow.major_axis_end3_d"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "common.id": PROPERTY_METADATA["common.id"],
            "arrow.head_size": PROPERTY_METADATA["arrow.head_size"],
            "arrow.head_3d": PROPERTY_METADATA["arrow.head_3d"],
            "arrow.fill_type": PROPERTY_METADATA["arrow.fill_type"],
            "dtd.graphic.fade_percent": PROPERTY_METADATA["dtd.graphic.fade_percent"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.plasmidregion.center3_d": PROPERTY_METADATA["dtd.plasmidregion.center3_d"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.arrow.arrow_shaft_spacing": PROPERTY_METADATA["dtd.arrow.arrow_shaft_spacing"],
            "dtd.plasmidregion.arrowhead_width": PROPERTY_METADATA[
                "dtd.plasmidregion.arrowhead_width"
            ],
            "arrow.arrowhead_type": PROPERTY_METADATA["arrow.arrowhead_type"],
            "arrow.arrowhead_tail": PROPERTY_METADATA["arrow.arrowhead_tail"],
            "arrow.arrowhead_head": PROPERTY_METADATA["arrow.arrowhead_head"],
            "dtd.arrow.arrowhead_center_size": PROPERTY_METADATA["dtd.arrow.arrowhead_center_size"],
            "dtd.graphic.angular_size": PROPERTY_METADATA["dtd.graphic.angular_size"],
        }
    ),
    provenance=(P_0fb307ce26c1d1783b42,),
)
