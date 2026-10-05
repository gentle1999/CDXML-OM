# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the CrossReference ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_c8fc593f4e78e61c9fb7
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="CrossReference",
    xml_tag="crossreference",
    cdx_id=32788,
    cdx_constant="kCDXObj_CrossReference",
    category="document_object",
    id_scope="none",
    allowed_parents=("page",),
    status="known",
    children=(
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.crossreference.cross_reference_container": PROPERTY_METADATA[
                "dtd.crossreference.cross_reference_container"
            ],
            "dtd.crossreference.cross_reference_sequence": PROPERTY_METADATA[
                "dtd.crossreference.cross_reference_sequence"
            ],
            "dtd.crossreference.cross_reference_identifier": PROPERTY_METADATA[
                "dtd.crossreference.cross_reference_identifier"
            ],
            "dtd.crossreference.cross_reference_document": PROPERTY_METADATA[
                "dtd.crossreference.cross_reference_document"
            ],
        }
    ),
    provenance=(P_c8fc593f4e78e61c9fb7,),
)
