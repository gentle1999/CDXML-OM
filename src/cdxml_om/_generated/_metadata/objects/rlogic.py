# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the RLogic ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_41c8cfa8d00cd9c35413
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="RLogic",
    xml_tag="rlogic",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group"),
    status="known",
    children=(
        ChildMetadata(
            object_type="text_run",
            collection_name="runs",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="rlogic_item",
            collection_name="rlogicitems",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "node.position": PROPERTY_METADATA["node.position"],
            "dtd.t.line_height": PROPERTY_METADATA["dtd.t.line_height"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
        }
    ),
    provenance=(P_41c8cfa8d00cd9c35413,),
)
