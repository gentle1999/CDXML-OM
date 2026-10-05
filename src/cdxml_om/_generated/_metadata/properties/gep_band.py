# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: gep_band."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_544d4dae60d21a9c7ab8,
    P_597e5f12d4d41dbdefc9,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.gepband.band_value": PropertyMetadata(
            owners=("gep_band",),
            name="band_value",
            xml_name="BandValue",
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
            provenance=(P_544d4dae60d21a9c7ab8,),
            xml_aliases=(),
        ),
        "dtd.gepband.show_value": PropertyMetadata(
            owners=("gep_band",),
            name="show_value",
            xml_name="ShowValue",
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
            provenance=(P_597e5f12d4d41dbdefc9,),
            xml_aliases=(),
        ),
    }
)
