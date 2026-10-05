# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: represent."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_6d2ecec6555e2ba327e6,
    P_922c573e28eaa3b69f58,
)
from ..provenance.sdk_page_represent import (
    P_8245ba4f95380798abb1,
    P_dc02755c7a5dc3079e9b,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.represent.attribute_id": PropertyMetadata(
            owners=("represent",),
            name="attribute_id",
            xml_name="attribute",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="integer",
            codec="integer",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_922c573e28eaa3b69f58,
                P_8245ba4f95380798abb1,
            ),
            xml_aliases=(),
        ),
        "dtd.represent.object_reference": PropertyMetadata(
            owners=("represent",),
            name="object_reference",
            xml_name="object",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="object_id",
            codec="object_id",
            required=True,
            default=None,
            cardinality="one",
            reference_target="*",
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_6d2ecec6555e2ba327e6,
                P_dc02755c7a5dc3079e9b,
            ),
            xml_aliases=(),
        ),
    }
)
