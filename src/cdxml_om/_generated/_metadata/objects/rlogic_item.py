# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the RLogicItem ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_1ea9f40328e4d60fe2f0
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="RLogicItem",
    xml_tag="rlogicitem",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("rlogic",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.rlogicitem.r_logic_rest_h": PROPERTY_METADATA["dtd.rlogicitem.r_logic_rest_h"],
            "dtd.rlogicitem.r_logic_occurrence": PROPERTY_METADATA[
                "dtd.rlogicitem.r_logic_occurrence"
            ],
            "dtd.rlogicitem.r_logic_if_then_group": PROPERTY_METADATA[
                "dtd.rlogicitem.r_logic_if_then_group"
            ],
            "dtd.rlogicitem.r_logic_group": PROPERTY_METADATA["dtd.rlogicitem.r_logic_group"],
        }
    ),
    provenance=(P_1ea9f40328e4d60fe2f0,),
)
