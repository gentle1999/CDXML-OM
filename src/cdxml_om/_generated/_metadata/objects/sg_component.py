# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the SGComponent ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_68d1adea6d9e590a6e68
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="SGComponent",
    xml_tag="sgcomponent",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("stoichiometry_grid",),
    status="known",
    children=(
        ChildMetadata(
            object_type="object_tag",
            collection_name="objecttags",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="sg_datum",
            collection_name="sgdatums",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.sgcomponent.component_is_header": PROPERTY_METADATA[
                "dtd.sgcomponent.component_is_header"
            ],
            "dtd.page.width": PROPERTY_METADATA["dtd.page.width"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.sgcomponent.component_reference_id": PROPERTY_METADATA[
                "dtd.sgcomponent.component_reference_id"
            ],
            "dtd.sgcomponent.component_is_reactant": PROPERTY_METADATA[
                "dtd.sgcomponent.component_is_reactant"
            ],
        }
    ),
    provenance=(P_68d1adea6d9e590a6e68,),
)
