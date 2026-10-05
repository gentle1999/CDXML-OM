# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: text."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_22a8e59cf144ba8fdae7,
    P_abeb6f73b7660d7c4189,
    P_c210207cf39d4bf44be9,
    P_f8c2b59ba7426994a22e,
)
from ..provenance.sdk_page_t import (
    P_2ee78659043a74ff84b0,
    P_44e7a80582322448e480,
    P_44e32e50ce7f08b4db3c,
    P_d870e8645f2b0f5e27c4,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.t.justification": PropertyMetadata(
            owners=("text",),
            name="justification",
            xml_name="Justification",
            storage="attribute",
            cdx_id=1793,
            cdx_constant="kCDXProp_Justification",
            datatype="string",
            codec="string",
            required=False,
            default="Left",
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum="dtd.justification.8e038579",
            status="known",
            provenance=(
                P_22a8e59cf144ba8fdae7,
                P_44e7a80582322448e480,
            ),
            xml_aliases=(),
        ),
        "dtd.t.label_alignment": PropertyMetadata(
            owners=("text",),
            name="label_alignment",
            xml_name="LabelAlignment",
            storage="attribute",
            cdx_id=1797,
            cdx_constant="kCDXProp_LabelAlignment",
            datatype="string",
            codec="string",
            required=False,
            default="Auto",
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum="dtd.label_justification.aa6f97a8",
            status="known",
            provenance=(
                P_abeb6f73b7660d7c4189,
                P_44e32e50ce7f08b4db3c,
            ),
            xml_aliases=(),
        ),
        "dtd.t.line_starts": PropertyMetadata(
            owners=("text",),
            name="line_starts",
            xml_name="LineStarts",
            storage="attribute",
            cdx_id=1796,
            cdx_constant="kCDXProp_LineStarts",
            datatype="integer_list",
            codec="uint16_list",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_f8c2b59ba7426994a22e,
                P_d870e8645f2b0f5e27c4,
            ),
            xml_aliases=(),
        ),
        "dtd.t.word_wrap_width": PropertyMetadata(
            owners=("text",),
            name="word_wrap_width",
            xml_name="WordWrapWidth",
            storage="attribute",
            cdx_id=1795,
            cdx_constant="kCDXProp_WordWrapWidth",
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
                P_c210207cf39d4bf44be9,
                P_2ee78659043a74ff84b0,
            ),
            xml_aliases=(),
        ),
    }
)
