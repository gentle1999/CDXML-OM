# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: plasmid_region."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_56a5f7a27b6402dee903,
    P_b1f38137da57d5bab9dc,
    P_cea7d078aaf0751475a8,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.plasmidregion.region_end": PropertyMetadata(
            owners=("plasmid_region",),
            name="region_end",
            xml_name="RegionEnd",
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
            provenance=(P_cea7d078aaf0751475a8,),
            xml_aliases=(),
        ),
        "dtd.plasmidregion.region_offset": PropertyMetadata(
            owners=("plasmid_region",),
            name="region_offset",
            xml_name="RegionOffset",
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
            provenance=(P_b1f38137da57d5bab9dc,),
            xml_aliases=(),
        ),
        "dtd.plasmidregion.region_start": PropertyMetadata(
            owners=("plasmid_region",),
            name="region_start",
            xml_name="RegionStart",
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
            provenance=(P_56a5f7a27b6402dee903,),
            xml_aliases=(),
        ),
    }
)
