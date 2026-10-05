# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: tlc_spot."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_6b134746cf7f2a885508,
    P_84c0502c813af38f042e,
    P_fa81733dc9dbfe435971,
)
from ..provenance.sdk_page_tlcspot import (
    P_9f65b395878dfb0a6e76,
    P_491a81fb90a0e6edd6d9,
    P_e55eee85cf786039c8ca,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.tlcspot.rf": PropertyMetadata(
            owners=("tlc_spot",),
            name="rf",
            xml_name="Rf",
            storage="attribute",
            cdx_id=2736,
            cdx_constant="kCDXProp_TLC_Rf",
            datatype="float",
            codec="float",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_6b134746cf7f2a885508,
                P_491a81fb90a0e6edd6d9,
            ),
            xml_aliases=(),
        ),
        "dtd.tlcspot.show_rf": PropertyMetadata(
            owners=("tlc_spot",),
            name="show_rf",
            xml_name="ShowRf",
            storage="attribute",
            cdx_id=2738,
            cdx_constant="kCDXProp_TLC_ShowRf",
            datatype="boolean",
            codec="bool",
            required=False,
            default=False,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_84c0502c813af38f042e,
                P_9f65b395878dfb0a6e76,
            ),
            xml_aliases=(),
        ),
        "dtd.tlcspot.tail_value": PropertyMetadata(
            owners=("tlc_spot",),
            name="tail_value",
            xml_name="Tail",
            storage="attribute",
            cdx_id=2737,
            cdx_constant="kCDXProp_TLC_Tail",
            datatype="float",
            codec="float",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_fa81733dc9dbfe435971,
                P_e55eee85cf786039c8ca,
            ),
            xml_aliases=(),
        ),
    }
)
