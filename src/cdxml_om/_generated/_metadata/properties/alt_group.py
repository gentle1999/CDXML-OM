# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: alt_group."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_22eb23be1512c47a72ca,
    P_988ff57dba41cfe3561a,
    P_c6ae1c78a360d159abf5,
)
from ..provenance.sdk_page_altgroup import (
    P_249d6d6cc59fc49329b5,
    P_631b83e755661f26bdda,
    P_970b519c6a6b54af4a29,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.altgroup.group_frame": PropertyMetadata(
            owners=("alt_group",),
            name="group_frame",
            xml_name="GroupFrame",
            storage="attribute",
            cdx_id=2817,
            cdx_constant="kCDXProp_NamedAlternativeGroup_GroupFrame",
            datatype="bounding_box",
            codec="bounding_box",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_22eb23be1512c47a72ca,
                P_631b83e755661f26bdda,
            ),
            xml_aliases=(),
        ),
        "dtd.altgroup.text_frame": PropertyMetadata(
            owners=("alt_group",),
            name="text_frame",
            xml_name="TextFrame",
            storage="attribute",
            cdx_id=2816,
            cdx_constant="kCDXProp_NamedAlternativeGroup_TextFrame",
            datatype="bounding_box",
            codec="bounding_box",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_c6ae1c78a360d159abf5,
                P_970b519c6a6b54af4a29,
            ),
            xml_aliases=(),
        ),
        "dtd.altgroup.valence": PropertyMetadata(
            owners=("alt_group",),
            name="valence",
            xml_name="Valence",
            storage="attribute",
            cdx_id=2818,
            cdx_constant="kCDXProp_NamedAlternativeGroup_Valence",
            datatype="integer",
            codec="integer",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_988ff57dba41cfe3561a,
                P_249d6d6cc59fc49329b5,
            ),
            xml_aliases=(),
        ),
    }
)
