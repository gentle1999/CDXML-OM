# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: bracket_attachment."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import P_94b7aa7feae35cdf820b
from ..provenance.sdk_page_bracketattachment import P_8fe87b73fa990c29bc23
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.bracketattachment.graphic_id": PropertyMetadata(
            owners=("bracket_attachment",),
            name="graphic_id",
            xml_name="GraphicID",
            storage="attribute",
            cdx_id=2603,
            cdx_constant="kCDXProp_Bracket_GraphicID",
            datatype="object_id",
            codec="object_id",
            required=False,
            default=None,
            cardinality="one",
            reference_target="*",
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_94b7aa7feae35cdf820b,
                P_8fe87b73fa990c29bc23,
            ),
            xml_aliases=(),
        ),
    }
)
