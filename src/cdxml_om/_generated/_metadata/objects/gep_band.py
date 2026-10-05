# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the GEPBand ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_cc83d6956b10d5f525a9
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="GEPBand",
    xml_tag="gepband",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("gep_lane",),
    status="known",
    children=(
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
        ChildMetadata(
            object_type="marker",
            collection_name="markers",
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
            "dtd.gepband.show_value": PROPERTY_METADATA["dtd.gepband.show_value"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.page.height": PROPERTY_METADATA["dtd.page.height"],
            "dtd.curve.curve_type": PROPERTY_METADATA["dtd.curve.curve_type"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.gepband.band_value": PROPERTY_METADATA["dtd.gepband.band_value"],
        }
    ),
    provenance=(P_cc83d6956b10d5f525a9,),
)
