# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Curve ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_dc29d35302ad9d689716
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Curve",
    xml_tag="curve",
    cdx_id=32776,
    cdx_constant="kCDXObj_Curve",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group", "fragment", "marker", "plasmid_marker", "bio_shape"),
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
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.curve.head_width": PROPERTY_METADATA["dtd.curve.head_width"],
            "arrow.head_size": PROPERTY_METADATA["arrow.head_size"],
            "dtd.curve.head_center_size": PROPERTY_METADATA["dtd.curve.head_center_size"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "arrow.fill_type": PROPERTY_METADATA["arrow.fill_type"],
            "dtd.graphic.fade_percent": PROPERTY_METADATA["dtd.graphic.fade_percent"],
            "dtd.curve.curve_type": PROPERTY_METADATA["dtd.curve.curve_type"],
            "dtd.curve.curve_spacing": PROPERTY_METADATA["dtd.curve.curve_spacing"],
            "dtd.curve.curve_points3_d": PROPERTY_METADATA["dtd.curve.curve_points3_d"],
            "dtd.curve.curve_points": PROPERTY_METADATA["dtd.curve.curve_points"],
            "dtd.curve.closed": PROPERTY_METADATA["dtd.curve.closed"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.curve.arrowhead_type": PROPERTY_METADATA["dtd.curve.arrowhead_type"],
            "dtd.curve.arrowhead_tail": PROPERTY_METADATA["dtd.curve.arrowhead_tail"],
            "dtd.curve.arrowhead_head": PROPERTY_METADATA["dtd.curve.arrowhead_head"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_dc29d35302ad9d689716,),
)
