# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: border."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import P_df36c467d7063a260a7b
from ..provenance.sdk_page_border import P_43174d4abb9e72ccbcfd
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.border.side": PropertyMetadata(
            owners=("border",),
            name="side",
            xml_name="Side",
            storage="attribute",
            cdx_id=2085,
            cdx_constant="kCDXProp_Side",
            datatype="string",
            codec="string",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum="dtd.side.5dd5ccc4",
            status="known",
            provenance=(
                P_df36c467d7063a260a7b,
                P_43174d4abb9e72ccbcfd,
            ),
            xml_aliases=(),
        ),
    }
)
