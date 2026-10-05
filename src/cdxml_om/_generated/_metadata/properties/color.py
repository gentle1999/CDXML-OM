# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: color."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_78bf66efe87149d8abc1,
    P_96219d4310673e6d4c15,
    P_e87c730f2e1bca5c0351,
)
from ..provenance.sdk_color import (
    P_3876728f8ce07e3464c1,
    P_aec287375754c4943da4,
    P_f9d6530514e1937ff0c2,
)
from ..provenance.sdk_page_color import (
    P_7c39aec10eca75445a43,
    P_27efd77ba6d8c6aed77d,
    P_3874e21ce76508caec52,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "color.b": PropertyMetadata(
            owners=("color",),
            name="b",
            xml_name="b",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="unit_interval",
            codec="float",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_3876728f8ce07e3464c1,
                P_96219d4310673e6d4c15,
                P_27efd77ba6d8c6aed77d,
            ),
            xml_aliases=(),
        ),
        "color.g": PropertyMetadata(
            owners=("color",),
            name="g",
            xml_name="g",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="unit_interval",
            codec="float",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_f9d6530514e1937ff0c2,
                P_e87c730f2e1bca5c0351,
                P_7c39aec10eca75445a43,
            ),
            xml_aliases=(),
        ),
        "color.r": PropertyMetadata(
            owners=("color",),
            name="r",
            xml_name="r",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="unit_interval",
            codec="float",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_aec287375754c4943da4,
                P_78bf66efe87149d8abc1,
                P_3874e21ce76508caec52,
            ),
            xml_aliases=(),
        ),
    }
)
