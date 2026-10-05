# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: rlogic_item."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_aaafb992e964608389ed,
    P_c32d7cd96a2ccfdd277e,
    P_ce64ad6b359d4db2d356,
    P_d0f463ff7f89ad57b31b,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.rlogicitem.r_logic_group": PropertyMetadata(
            owners=("rlogic_item",),
            name="r_logic_group",
            xml_name="RLogicGroup",
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
            provenance=(P_c32d7cd96a2ccfdd277e,),
            xml_aliases=(),
        ),
        "dtd.rlogicitem.r_logic_if_then_group": PropertyMetadata(
            owners=("rlogic_item",),
            name="r_logic_if_then_group",
            xml_name="RLogicIfThenGroup",
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
            provenance=(P_d0f463ff7f89ad57b31b,),
            xml_aliases=(),
        ),
        "dtd.rlogicitem.r_logic_occurrence": PropertyMetadata(
            owners=("rlogic_item",),
            name="r_logic_occurrence",
            xml_name="RLogicOccurrence",
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
            provenance=(P_aaafb992e964608389ed,),
            xml_aliases=(),
        ),
        "dtd.rlogicitem.r_logic_rest_h": PropertyMetadata(
            owners=("rlogic_item",),
            name="r_logic_rest_h",
            xml_name="RLogicRestH",
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
            provenance=(P_ce64ad6b359d4db2d356,),
            xml_aliases=(),
        ),
    }
)
