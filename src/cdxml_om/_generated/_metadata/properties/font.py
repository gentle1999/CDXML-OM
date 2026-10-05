# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: font."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_16c25492f533b4ca0a14,
    P_5176e735961a03d006fc,
    P_876915ae6e2f95b6c851,
)
from ..provenance.sdk_font import (
    P_98488763d35156d4da38,
    P_787743906240804b54b0,
)
from ..provenance.sdk_font_charset_xml import P_dd743b44ce13c0b28d37
from ..provenance.sdk_page_font import (
    P_9ab076e8f3c30c1b7157,
    P_873ad68633af49e6eed8,
    P_286011700606a39a91d8,
    P_c441b6a4ea0bd6427d23,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "font.charset": PropertyMetadata(
            owners=("font",),
            name="charset",
            xml_name="charset",
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
            provenance=(
                P_5176e735961a03d006fc,
                P_9ab076e8f3c30c1b7157,
                P_dd743b44ce13c0b28d37,
                P_873ad68633af49e6eed8,
            ),
            xml_aliases=(),
        ),
        "font.id": PropertyMetadata(
            owners=("font",),
            name="id",
            xml_name="id",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="local_id",
            codec="integer",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_98488763d35156d4da38,
                P_16c25492f533b4ca0a14,
                P_c441b6a4ea0bd6427d23,
            ),
            xml_aliases=(),
        ),
        "font.name": PropertyMetadata(
            owners=("font",),
            name="name",
            xml_name="name",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="string",
            codec="string",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_787743906240804b54b0,
                P_876915ae6e2f95b6c851,
                P_286011700606a39a91d8,
            ),
            xml_aliases=(),
        ),
    }
)
