# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TLCSpot ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_8626b0a936e1cb109809
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="TLCSpot",
    xml_tag="tlcspot",
    cdx_id=32805,
    cdx_constant="kCDXObj_TLCSpot",
    category="document_object",
    id_scope="document",
    allowed_parents=("tlc_lane",),
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
            object_type="embedded_object",
            collection_name="embeddedobjects",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.page.width": PROPERTY_METADATA["dtd.page.width"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.tlcspot.tail_value": PROPERTY_METADATA["dtd.tlcspot.tail_value"],
            "dtd.tlcspot.show_rf": PROPERTY_METADATA["dtd.tlcspot.show_rf"],
            "dtd.tlcspot.rf": PROPERTY_METADATA["dtd.tlcspot.rf"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.page.height": PROPERTY_METADATA["dtd.page.height"],
            "dtd.curve.curve_type": PROPERTY_METADATA["dtd.curve.curve_type"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
        }
    ),
    provenance=(P_8626b0a936e1cb109809,),
)
