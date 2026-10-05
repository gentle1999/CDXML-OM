# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the RxnParticipation enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_f89462db8aa4331452ab
from ..provenance.sdk_page_b import P_0a1df81d2115172b0071
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="RxnParticipation",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="REACTION_CENTER",
            xml_value="ReactionCenter",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="MAKE_OR_BREAK",
            xml_value="MakeOrBreak",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="CHANGE_TYPE",
            xml_value="ChangeType",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="MAKE_AND_CHANGE",
            xml_value="MakeAndChange",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NOT_REACTION_CENTER",
            xml_value="NotReactionCenter",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NO_CHANGE",
            xml_value="NoChange",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="UNMAPPED",
            xml_value="Unmapped",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_f89462db8aa4331452ab,
        P_0a1df81d2115172b0071,
    ),
)
