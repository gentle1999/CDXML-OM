# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Arrow ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_095cf9121daff10bfe21
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Arrow",
    xml_tag="arrow",
    cdx_id=32807,
    cdx_constant="kCDXObj_Arrow",
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
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "arrow.tail_3d": PROPERTY_METADATA["arrow.tail_3d"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.arrow.no_go": PROPERTY_METADATA["dtd.arrow.no_go"],
            "dtd.arrow.minor_axis_end3_d": PROPERTY_METADATA["dtd.arrow.minor_axis_end3_d"],
            "dtd.arrow.major_axis_end3_d": PROPERTY_METADATA["dtd.arrow.major_axis_end3_d"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "arrow.head_size": PROPERTY_METADATA["arrow.head_size"],
            "arrow.head_3d": PROPERTY_METADATA["arrow.head_3d"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "arrow.fill_type": PROPERTY_METADATA["arrow.fill_type"],
            "dtd.graphic.fade_percent": PROPERTY_METADATA["dtd.graphic.fade_percent"],
            "dtd.arrow.dipole": PROPERTY_METADATA["dtd.arrow.dipole"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.plasmidregion.center3_d": PROPERTY_METADATA["dtd.plasmidregion.center3_d"],
            "dtd.CDXML.caption_size": PROPERTY_METADATA["dtd.CDXML.caption_size"],
            "dtd.CDXML.caption_font": PROPERTY_METADATA["dtd.CDXML.caption_font"],
            "dtd.CDXML.caption_face": PROPERTY_METADATA["dtd.CDXML.caption_face"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.arrow.arrow_target": PROPERTY_METADATA["dtd.arrow.arrow_target"],
            "dtd.arrow.arrow_source": PROPERTY_METADATA["dtd.arrow.arrow_source"],
            "dtd.arrow.arrow_shaft_spacing": PROPERTY_METADATA["dtd.arrow.arrow_shaft_spacing"],
            "arrow.arrowhead_type": PROPERTY_METADATA["arrow.arrowhead_type"],
            "arrow.arrowhead_tail": PROPERTY_METADATA["arrow.arrowhead_tail"],
            "dtd.plasmidregion.arrowhead_width": PROPERTY_METADATA[
                "dtd.plasmidregion.arrowhead_width"
            ],
            "arrow.arrowhead_head": PROPERTY_METADATA["arrow.arrowhead_head"],
            "dtd.arrow.arrowhead_center_size": PROPERTY_METADATA["dtd.arrow.arrowhead_center_size"],
            "dtd.arrow.arrow_equilibrium_ratio": PROPERTY_METADATA[
                "dtd.arrow.arrow_equilibrium_ratio"
            ],
            "dtd.graphic.angular_size": PROPERTY_METADATA["dtd.graphic.angular_size"],
        }
    ),
    provenance=(P_095cf9121daff10bfe21,),
)
