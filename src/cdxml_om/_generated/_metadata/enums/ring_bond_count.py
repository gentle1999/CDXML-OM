# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the RingBondCount enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_b566912330a8fa6847d7
from ..provenance.sdk_page_n import P_98d1a7488c697708526a
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="RingBondCount",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="SPIRO_OR_HIGHER",
            xml_value="SpiroOrHigher",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="FUSION",
            xml_value="Fusion",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="SIMPLE_RING",
            xml_value="SimpleRing",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="AS_DRAWN",
            xml_value="AsDrawn",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NO_RING_BONDS",
            xml_value="NoRingBonds",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_b566912330a8fa6847d7,
        P_98d1a7488c697708526a,
    ),
)
