# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Graphic ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_811ab172ea2532c9e985
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Graphic",
    xml_tag="graphic",
    cdx_id=32775,
    cdx_constant="kCDXObj_Graphic",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group", "fragment", "alt_group", "plasmid_map"),
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
            object_type="represent",
            collection_name="represents",
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
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "arrow.tail_3d": PROPERTY_METADATA["arrow.tail_3d"],
            "dtd.graphic.symbol_type": PROPERTY_METADATA["dtd.graphic.symbol_type"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.graphic.rectangle_type": PROPERTY_METADATA["dtd.graphic.rectangle_type"],
            "dtd.graphic.shadow_size": PROPERTY_METADATA["dtd.graphic.shadow_size"],
            "dtd.graphic.polymer_repeat_pattern": PROPERTY_METADATA[
                "dtd.graphic.polymer_repeat_pattern"
            ],
            "dtd.graphic.polymer_flip_type": PROPERTY_METADATA["dtd.graphic.polymer_flip_type"],
            "dtd.graphic.oval_type": PROPERTY_METADATA["dtd.graphic.oval_type"],
            "dtd.graphic.orbital_type": PROPERTY_METADATA["dtd.graphic.orbital_type"],
            "dtd.arrow.minor_axis_end3_d": PROPERTY_METADATA["dtd.arrow.minor_axis_end3_d"],
            "dtd.arrow.major_axis_end3_d": PROPERTY_METADATA["dtd.arrow.major_axis_end3_d"],
            "dtd.graphic.lip_size": PROPERTY_METADATA["dtd.graphic.lip_size"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "arrow.head_size": PROPERTY_METADATA["arrow.head_size"],
            "arrow.head_3d": PROPERTY_METADATA["arrow.head_3d"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "graphic.graphic_type": PROPERTY_METADATA["graphic.graphic_type"],
            "dtd.graphic.frame_type": PROPERTY_METADATA["dtd.graphic.frame_type"],
            "dtd.graphic.fade_percent": PROPERTY_METADATA["dtd.graphic.fade_percent"],
            "dtd.graphic.corner_radius": PROPERTY_METADATA["dtd.graphic.corner_radius"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.plasmidregion.center3_d": PROPERTY_METADATA["dtd.plasmidregion.center3_d"],
            "dtd.CDXML.caption_size": PROPERTY_METADATA["dtd.CDXML.caption_size"],
            "dtd.CDXML.caption_font": PROPERTY_METADATA["dtd.CDXML.caption_font"],
            "dtd.CDXML.caption_face": PROPERTY_METADATA["dtd.CDXML.caption_face"],
            "dtd.graphic.bracket_usage": PROPERTY_METADATA["dtd.graphic.bracket_usage"],
            "dtd.graphic.bracket_type": PROPERTY_METADATA["dtd.graphic.bracket_type"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.graphic.arrow_type": PROPERTY_METADATA["dtd.graphic.arrow_type"],
            "dtd.graphic.angular_size": PROPERTY_METADATA["dtd.graphic.angular_size"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_811ab172ea2532c9e985,),
)
