# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: registry_number."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_4e201b12de37e8297d3a,
    P_96cc5820bbd1e8b9ab60,
)
from ..provenance.sdk_page_regnum import (
    P_9b7e5371502a7f3204a5,
    P_3142e8a865aba91a538a,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.regnum.registry_authority": PropertyMetadata(
            owners=("registry_number",),
            name="registry_authority",
            xml_name="RegistryAuthority",
            storage="attribute",
            cdx_id=12,
            cdx_constant="kCDXProp_RegistryAuthority",
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
                P_4e201b12de37e8297d3a,
                P_9b7e5371502a7f3204a5,
            ),
            xml_aliases=(),
        ),
        "dtd.regnum.registry_number": PropertyMetadata(
            owners=("registry_number",),
            name="registry_number",
            xml_name="RegistryNumber",
            storage="attribute",
            cdx_id=11,
            cdx_constant="kCDXProp_RegistryNumber",
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
                P_96cc5820bbd1e8b9ab60,
                P_3142e8a865aba91a538a,
            ),
            xml_aliases=(),
        ),
    }
)
