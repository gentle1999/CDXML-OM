# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ReactionStep ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_65fc4d09c9a4b4342e0c
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ReactionStep",
    xml_tag="step",
    cdx_id=32782,
    cdx_constant="kCDXObj_ReactionStep",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group", "reaction_scheme"),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "reaction_step.reactants": PROPERTY_METADATA["reaction_step.reactants"],
            "reaction_step.products": PROPERTY_METADATA["reaction_step.products"],
            "dtd.step.reaction_step_plusses": PROPERTY_METADATA["dtd.step.reaction_step_plusses"],
            "dtd.step.reaction_step_objects_below_arrow": PROPERTY_METADATA[
                "dtd.step.reaction_step_objects_below_arrow"
            ],
            "dtd.step.reaction_step_objects_above_arrow": PROPERTY_METADATA[
                "dtd.step.reaction_step_objects_above_arrow"
            ],
            "dtd.step.reaction_step_atom_map_manual": PROPERTY_METADATA[
                "dtd.step.reaction_step_atom_map_manual"
            ],
            "dtd.step.reaction_step_atom_map_auto": PROPERTY_METADATA[
                "dtd.step.reaction_step_atom_map_auto"
            ],
            "dtd.step.reaction_step_atom_map": PROPERTY_METADATA["dtd.step.reaction_step_atom_map"],
            "reaction_step.arrows": PROPERTY_METADATA["reaction_step.arrows"],
        }
    ),
    provenance=(P_65fc4d09c9a4b4342e0c,),
)
