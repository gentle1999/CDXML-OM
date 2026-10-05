# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Fragment ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_277dbc58a2c33497dc11
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Fragment",
    xml_tag="fragment",
    cdx_id=32771,
    cdx_constant="kCDXObj_Fragment",
    category="chemical_structure",
    id_scope="document",
    allowed_parents=("page", "group", "node", "alt_group"),
    status="known",
    children=(
        ChildMetadata(
            object_type="node",
            collection_name="nodes",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="bond",
            collection_name="bonds",
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
            object_type="graphic",
            collection_name="graphics",
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
            object_type="registry_number",
            collection_name="regnums",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="colored_molecular_area",
            collection_name="coloredmolecularareas",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.fragment.absolute": PROPERTY_METADATA["dtd.fragment.absolute"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.fragment.weight": PROPERTY_METADATA["dtd.fragment.weight"],
            "dtd.fragment.sequence_type": PROPERTY_METADATA["dtd.fragment.sequence_type"],
            "dtd.fragment.racemic": PROPERTY_METADATA["dtd.fragment.racemic"],
            "dtd.fragment.relative": PROPERTY_METADATA["dtd.fragment.relative"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.fragment.formula": PROPERTY_METADATA["dtd.fragment.formula"],
            "dtd.fragment.connection_order": PROPERTY_METADATA["dtd.fragment.connection_order"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
        }
    ),
    provenance=(P_277dbc58a2c33497dc11,),
)
