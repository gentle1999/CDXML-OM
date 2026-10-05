# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: group."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import P_fe03a68991d95c9d2c61
from ..provenance.sdk_group import P_b7ae1aabb1946e3dce90
from ..provenance.sdk_page_group import P_7c9684041bb58e6240f2
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "group.integral": PropertyMetadata(
            owners=("group",),
            name="integral",
            xml_name="Integral",
            storage="attribute",
            cdx_id=4352,
            cdx_constant="kCDXProp_Group_Integral",
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
                P_b7ae1aabb1946e3dce90,
                P_fe03a68991d95c9d2c61,
                P_7c9684041bb58e6240f2,
            ),
            xml_aliases=(),
        ),
    }
)
