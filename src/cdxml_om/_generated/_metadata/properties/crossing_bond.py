# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: crossing_bond."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_2a7bf702d7f014a04ad5,
    P_b4c517e90fbe12cf2dc7,
)
from ..provenance.sdk_page_crossingbond import (
    P_62f63259624260f21515,
    P_319abeb5599d15f033d9,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.crossingbond.bond_id": PropertyMetadata(
            owners=("crossing_bond",),
            name="bond_id",
            xml_name="BondID",
            storage="attribute",
            cdx_id=2604,
            cdx_constant="kCDXProp_Bracket_BondID",
            datatype="object_id",
            codec="object_id",
            required=True,
            default=None,
            cardinality="one",
            reference_target="bond",
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_2a7bf702d7f014a04ad5,
                P_319abeb5599d15f033d9,
            ),
            xml_aliases=(),
        ),
        "dtd.crossingbond.inner_atom_id": PropertyMetadata(
            owners=("crossing_bond",),
            name="inner_atom_id",
            xml_name="InnerAtomID",
            storage="attribute",
            cdx_id=2605,
            cdx_constant="kCDXProp_Bracket_InnerAtomID",
            datatype="object_id",
            codec="object_id",
            required=True,
            default=None,
            cardinality="one",
            reference_target="node",
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_b4c517e90fbe12cf2dc7,
                P_62f63259624260f21515,
            ),
            xml_aliases=(),
        ),
    }
)
