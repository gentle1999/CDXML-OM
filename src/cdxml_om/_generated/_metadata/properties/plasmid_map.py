# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: plasmid_map."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_e51381d743814a98fe38,
    P_f2f27f2aa9796719e97d,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.plasmidmap.number_base_pairs": PropertyMetadata(
            owners=("plasmid_map",),
            name="number_base_pairs",
            xml_name="NumberBasePairs",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_f2f27f2aa9796719e97d,),
            xml_aliases=(),
        ),
        "dtd.plasmidmap.ring_radius": PropertyMetadata(
            owners=("plasmid_map",),
            name="ring_radius",
            xml_name="RingRadius",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_e51381d743814a98fe38,),
            xml_aliases=(),
        ),
    }
)
