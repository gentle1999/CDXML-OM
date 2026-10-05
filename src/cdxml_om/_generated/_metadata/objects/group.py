# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Group ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_13953884cae6b4060ab2
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Group",
    xml_tag="group",
    cdx_id=32770,
    cdx_constant="kCDXObj_Group",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group", "alt_group"),
    status="known",
    children=(
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="fragment",
            collection_name="fragments",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="group",
            collection_name="groups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="graphic",
            collection_name="graphics",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="alt_group",
            collection_name="altgroups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="curve",
            collection_name="curves",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="reaction_step",
            collection_name="steps",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="reaction_scheme",
            collection_name="schemes",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="spectrum",
            collection_name="spectrums",
            min_occurs=0,
            max_occurs=None,
        ),
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
            object_type="plasmid_map",
            collection_name="plasmidmaps",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="rlogic",
            collection_name="rlogics",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="arrow",
            collection_name="arrows",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="bio_shape",
            collection_name="bioshapes",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "group.integral": PROPERTY_METADATA["group.integral"],
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_13953884cae6b4060ab2,),
)
