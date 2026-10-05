# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: annotation."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_335e229f55c391796aa0,
    P_a43c25dc2bdeb3241d09,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.annotation.content": PropertyMetadata(
            owners=("annotation",),
            name="content",
            xml_name="Content",
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
            provenance=(P_a43c25dc2bdeb3241d09,),
            xml_aliases=(),
        ),
        "dtd.annotation.keyword": PropertyMetadata(
            owners=("annotation",),
            name="keyword",
            xml_name="Keyword",
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
            provenance=(P_335e229f55c391796aa0,),
            xml_aliases=(),
        ),
    }
)
