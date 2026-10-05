# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ColorTable ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_a73e93bb1f0b75dc6d04
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ColorTable",
    xml_tag="colortable",
    cdx_id=None,
    cdx_constant=None,
    category="resource_table",
    id_scope="none",
    allowed_parents=("cdxml_root",),
    status="known",
    children=(
        ChildMetadata(
            object_type="color",
            collection_name="colors",
            min_occurs=1,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.colortable.xml_id": PROPERTY_METADATA["dtd.colortable.xml_id"],
        }
    ),
    provenance=(P_a73e93bb1f0b75dc6d04,),
)
