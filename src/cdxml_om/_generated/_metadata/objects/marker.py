# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Marker ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_63fa674613162cab9730
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Marker",
    xml_tag="marker",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("gep_band",),
    status="known",
    children=(
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
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
            object_type="curve",
            collection_name="curves",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.caption_justification": PROPERTY_METADATA["dtd.CDXML.caption_justification"],
            "dtd.objecttag.value": PROPERTY_METADATA["dtd.objecttag.value"],
            "dtd.objecttag.tag_type": PROPERTY_METADATA["dtd.objecttag.tag_type"],
            "dtd.objecttag.persistent": PROPERTY_METADATA["dtd.objecttag.persistent"],
            "dtd.objecttag.name": PROPERTY_METADATA["dtd.objecttag.name"],
            "dtd.marker.marker_offset": PROPERTY_METADATA["dtd.marker.marker_offset"],
            "dtd.marker.marker_angle": PROPERTY_METADATA["dtd.marker.marker_angle"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.objecttag.display_name": PROPERTY_METADATA["dtd.objecttag.display_name"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
        }
    ),
    provenance=(P_63fa674613162cab9730,),
)
