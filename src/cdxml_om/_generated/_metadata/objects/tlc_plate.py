# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TLCPlate ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_68b6569bfcf940357add
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="TLCPlate",
    xml_tag="tlcplate",
    cdx_id=32803,
    cdx_constant="kCDXObj_TLCPlate",
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
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
            object_type="tlc_lane",
            collection_name="tlclanes",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.tlcplate.transparent": PROPERTY_METADATA["dtd.tlcplate.transparent"],
            "dtd.tlcplate.top_right": PROPERTY_METADATA["dtd.tlcplate.top_right"],
            "dtd.tlcplate.top_left": PROPERTY_METADATA["dtd.tlcplate.top_left"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.tlcplate.solvent_front_fraction": PROPERTY_METADATA[
                "dtd.tlcplate.solvent_front_fraction"
            ],
            "dtd.tlcplate.show_solvent_front": PROPERTY_METADATA["dtd.tlcplate.show_solvent_front"],
            "dtd.tlcplate.show_side_ticks": PROPERTY_METADATA["dtd.tlcplate.show_side_ticks"],
            "dtd.tlcplate.show_origin": PROPERTY_METADATA["dtd.tlcplate.show_origin"],
            "dtd.tlcplate.show_borders": PROPERTY_METADATA["dtd.tlcplate.show_borders"],
            "dtd.tlcplate.origin_fraction": PROPERTY_METADATA["dtd.tlcplate.origin_fraction"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.tlcplate.bottom_right": PROPERTY_METADATA["dtd.tlcplate.bottom_right"],
            "dtd.tlcplate.bottom_left": PROPERTY_METADATA["dtd.tlcplate.bottom_left"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_68b6569bfcf940357add,),
)
