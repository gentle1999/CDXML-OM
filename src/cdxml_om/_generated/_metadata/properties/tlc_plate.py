# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: tlc_plate."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_78fcede0de017bc4cc8e,
    P_365a31f59db2770a82ba,
    P_b787ad9a61839496f7f1,
    P_bf0aad37dd400cf20054,
    P_ea42b21c0bdae0b0c6df,
)
from ..provenance.sdk_page_tlcplate import (
    P_01db9f3edc6052e39991,
    P_96fc5ce1d9b54a2e9a39,
    P_100b4ee09f11cbc0e760,
    P_756d80cf8ce60dc010a2,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.tlcplate.origin_fraction": PropertyMetadata(
            owners=("tlc_plate",),
            name="origin_fraction",
            xml_name="OriginFraction",
            storage="attribute",
            cdx_id=2720,
            cdx_constant="kCDXProp_TLC_OriginFraction",
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
                P_b787ad9a61839496f7f1,
                P_100b4ee09f11cbc0e760,
            ),
            xml_aliases=(),
        ),
        "dtd.tlcplate.show_origin": PropertyMetadata(
            owners=("tlc_plate",),
            name="show_origin",
            xml_name="ShowOrigin",
            storage="attribute",
            cdx_id=2722,
            cdx_constant="kCDXProp_TLC_ShowOrigin",
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
                P_78fcede0de017bc4cc8e,
                P_96fc5ce1d9b54a2e9a39,
            ),
            xml_aliases=(),
        ),
        "dtd.tlcplate.show_side_ticks": PropertyMetadata(
            owners=("tlc_plate",),
            name="show_side_ticks",
            xml_name="ShowSideTicks",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="boolean",
            codec="bool",
            required=False,
            default=False,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_ea42b21c0bdae0b0c6df,),
            xml_aliases=(),
        ),
        "dtd.tlcplate.show_solvent_front": PropertyMetadata(
            owners=("tlc_plate",),
            name="show_solvent_front",
            xml_name="ShowSolventFront",
            storage="attribute",
            cdx_id=2723,
            cdx_constant="kCDXProp_TLC_ShowSolventFront",
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
                P_365a31f59db2770a82ba,
                P_756d80cf8ce60dc010a2,
            ),
            xml_aliases=(),
        ),
        "dtd.tlcplate.solvent_front_fraction": PropertyMetadata(
            owners=("tlc_plate",),
            name="solvent_front_fraction",
            xml_name="SolventFrontFraction",
            storage="attribute",
            cdx_id=2721,
            cdx_constant="kCDXProp_TLC_SolventFrontFraction",
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
                P_bf0aad37dd400cf20054,
                P_01db9f3edc6052e39991,
            ),
            xml_aliases=(),
        ),
    }
)
