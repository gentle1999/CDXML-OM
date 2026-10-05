# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: sequence."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import P_76475d1e0ff711709c49
from ..provenance.sdk_page_sequence import P_2feed98cf26f1380190b
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.sequence.sequence_identifier": PropertyMetadata(
            owners=("sequence",),
            name="sequence_identifier",
            xml_name="SequenceIdentifier",
            storage="attribute",
            cdx_id=3584,
            cdx_constant="kCDXProp_Sequence_Identifier",
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
                P_76475d1e0ff711709c49,
                P_2feed98cf26f1380190b,
            ),
            xml_aliases=(),
        ),
    }
)
