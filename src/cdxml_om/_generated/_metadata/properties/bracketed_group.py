# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: bracketed_group."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_76f02b5e1f18a78b51bf,
    P_106c8a8bf1d00ed9cc79,
    P_a679e8757f967ae517c8,
    P_dce65cfc2ad17d5333ee,
)
from ..provenance.sdk_page_bracketedgroup import (
    P_5adadf6580671e58ff3c,
    P_87e9a50d278962079dec,
    P_7181200b7682edef9009,
    P_f1fde384686371fddf9e,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.bracketedgroup.bracketed_object_i_ds": PropertyMetadata(
            owners=("bracketed_group",),
            name="bracketed_object_i_ds",
            xml_name="BracketedObjectIDs",
            storage="attribute",
            cdx_id=2599,
            cdx_constant="kCDXProp_BracketedObjects",
            datatype="object_id",
            codec="object_id_list",
            required=False,
            default=None,
            cardinality="many",
            reference_target="*",
            reference_many=True,
            enum=None,
            status="known",
            provenance=(
                P_a679e8757f967ae517c8,
                P_5adadf6580671e58ff3c,
            ),
            xml_aliases=(),
        ),
        "dtd.bracketedgroup.component_order": PropertyMetadata(
            owners=("bracketed_group",),
            name="component_order",
            xml_name="ComponentOrder",
            storage="attribute",
            cdx_id=2601,
            cdx_constant="kCDXProp_Bracket_ComponentOrder",
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
                P_106c8a8bf1d00ed9cc79,
                P_87e9a50d278962079dec,
            ),
            xml_aliases=(),
        ),
        "dtd.bracketedgroup.repeat_count": PropertyMetadata(
            owners=("bracketed_group",),
            name="repeat_count",
            xml_name="RepeatCount",
            storage="attribute",
            cdx_id=2600,
            cdx_constant="kCDXProp_Bracket_RepeatCount",
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
                P_76f02b5e1f18a78b51bf,
                P_f1fde384686371fddf9e,
            ),
            xml_aliases=(),
        ),
        "dtd.bracketedgroup.sru_label": PropertyMetadata(
            owners=("bracketed_group",),
            name="sru_label",
            xml_name="SRULabel",
            storage="attribute",
            cdx_id=2602,
            cdx_constant="kCDXProp_Bracket_SRULabel",
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_dce65cfc2ad17d5333ee,
                P_7181200b7682edef9009,
            ),
            xml_aliases=(),
        ),
    }
)
