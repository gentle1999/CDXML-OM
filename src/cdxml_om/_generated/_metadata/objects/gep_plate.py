# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the GEPPlate ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_b1a202edcef3c07fb3ab
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="GEPPlate",
    xml_tag="gepplate",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
    status="known",
    children=(
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="gep_lane",
            collection_name="geplanes",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.gepplate.axis_width": PROPERTY_METADATA["dtd.gepplate.axis_width"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.gepplate.unit_id": PROPERTY_METADATA["dtd.gepplate.unit_id"],
            "dtd.tlcplate.transparent": PROPERTY_METADATA["dtd.tlcplate.transparent"],
            "dtd.tlcplate.top_right": PROPERTY_METADATA["dtd.tlcplate.top_right"],
            "dtd.tlcplate.top_left": PROPERTY_METADATA["dtd.tlcplate.top_left"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.gepplate.start_range": PROPERTY_METADATA["dtd.gepplate.start_range"],
            "dtd.gepplate.show_scale": PROPERTY_METADATA["dtd.gepplate.show_scale"],
            "dtd.tlcplate.show_borders": PROPERTY_METADATA["dtd.tlcplate.show_borders"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.gepplate.label_text": PROPERTY_METADATA["dtd.gepplate.label_text"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.gepplate.labels_angle": PROPERTY_METADATA["dtd.gepplate.labels_angle"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "dtd.gepplate.end_range": PROPERTY_METADATA["dtd.gepplate.end_range"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.tlcplate.bottom_right": PROPERTY_METADATA["dtd.tlcplate.bottom_right"],
            "dtd.tlcplate.bottom_left": PROPERTY_METADATA["dtd.tlcplate.bottom_left"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
        }
    ),
    provenance=(P_b1a202edcef3c07fb3ab,),
)
