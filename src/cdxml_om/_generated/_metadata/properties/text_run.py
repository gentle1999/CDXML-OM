# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: text_run."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_4a085cbff93341e59660,
    P_7bf8806571b6030d687f,
    P_9bb3399ad41f75c75d82,
    P_33e9acb63fba0ac7a48a,
    P_dec4b48a3262026c9a86,
)
from ..provenance.sdk_page_s import (
    P_02888b786608e41cf9c1,
    P_4e008ce016e96fee5346,
    P_c801f592dc0bcaaa8546,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "text_run.alpha": PropertyMetadata(
            owners=("text_run",),
            name="alpha",
            xml_name="alpha",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="float",
            codec="float",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_4a085cbff93341e59660,),
            xml_aliases=(),
        ),
        "text_run.content": PropertyMetadata(
            owners=("text_run",),
            name="content",
            xml_name="content",
            storage="text",
            cdx_id=None,
            cdx_constant=None,
            datatype="string",
            codec="string",
            required=True,
            default="",
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_33e9acb63fba0ac7a48a,),
            xml_aliases=(),
        ),
        "text_run.face": PropertyMetadata(
            owners=("text_run",),
            name="face",
            xml_name="face",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
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
                P_dec4b48a3262026c9a86,
                P_4e008ce016e96fee5346,
            ),
            xml_aliases=(),
        ),
        "text_run.font_id": PropertyMetadata(
            owners=("text_run",),
            name="font_id",
            xml_name="font",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="local_id",
            codec="integer",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_9bb3399ad41f75c75d82,
                P_02888b786608e41cf9c1,
            ),
            xml_aliases=(),
        ),
        "text_run.size": PropertyMetadata(
            owners=("text_run",),
            name="size",
            xml_name="size",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="float",
            codec="float",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_7bf8806571b6030d687f,
                P_c801f592dc0bcaaa8546,
            ),
            xml_aliases=(),
        ),
    }
)
