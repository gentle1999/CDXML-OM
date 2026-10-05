# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the BracketedGroup ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_78aabad302bb065d18a6
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="BracketedGroup",
    xml_tag="bracketedgroup",
    cdx_id=32791,
    cdx_constant="kCDXObj_BracketedGroup",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "bracketed_group"),
    status="known",
    children=(
        ChildMetadata(
            object_type="bracket_attachment",
            collection_name="bracketattachments",
            min_occurs=1,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="bracketed_group",
            collection_name="bracketedgroups",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.bracketedgroup.bracketed_object_i_ds": PROPERTY_METADATA[
                "dtd.bracketedgroup.bracketed_object_i_ds"
            ],
            "dtd.bracketedgroup.sru_label": PROPERTY_METADATA["dtd.bracketedgroup.sru_label"],
            "dtd.bracketedgroup.repeat_count": PROPERTY_METADATA["dtd.bracketedgroup.repeat_count"],
            "dtd.graphic.polymer_repeat_pattern": PROPERTY_METADATA[
                "dtd.graphic.polymer_repeat_pattern"
            ],
            "dtd.graphic.polymer_flip_type": PROPERTY_METADATA["dtd.graphic.polymer_flip_type"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.bracketedgroup.component_order": PROPERTY_METADATA[
                "dtd.bracketedgroup.component_order"
            ],
            "dtd.graphic.bracket_usage": PROPERTY_METADATA["dtd.graphic.bracket_usage"],
        }
    ),
    provenance=(P_78aabad302bb065d18a6,),
)
