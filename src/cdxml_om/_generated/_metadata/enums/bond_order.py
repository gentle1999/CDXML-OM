# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the BondOrder enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_801c2c2b387f286306ca
from ..provenance.sdk_bond import P_2bc112fb03b8ea75ed40
from ..provenance.sdk_bond_order import P_848222e269e6d1d97def
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="BondOrder",
    underlying_datatype="integer",
    representation="intflag",
    values=(
        EnumValueMetadata(
            name="SINGLE",
            xml_value="1",
            cdx_value=1,
        ),
        EnumValueMetadata(
            name="DOUBLE",
            xml_value="2",
            cdx_value=2,
        ),
        EnumValueMetadata(
            name="TRIPLE",
            xml_value="3",
            cdx_value=4,
        ),
        EnumValueMetadata(
            name="QUADRUPLE",
            xml_value="4",
            cdx_value=8,
        ),
        EnumValueMetadata(
            name="QUINTUPLE",
            xml_value="5",
            cdx_value=16,
        ),
        EnumValueMetadata(
            name="SEXTUPLE",
            xml_value="6",
            cdx_value=32,
        ),
        EnumValueMetadata(
            name="HALF",
            xml_value="0.5",
            cdx_value=64,
        ),
        EnumValueMetadata(
            name="AROMATIC",
            xml_value="1.5",
            cdx_value=128,
        ),
        EnumValueMetadata(
            name="TWO_AND_HALF",
            xml_value="2.5",
            cdx_value=256,
        ),
        EnumValueMetadata(
            name="THREE_AND_HALF",
            xml_value="3.5",
            cdx_value=512,
        ),
        EnumValueMetadata(
            name="FOUR_AND_HALF",
            xml_value="4.5",
            cdx_value=1024,
        ),
        EnumValueMetadata(
            name="FIVE_AND_HALF",
            xml_value="5.5",
            cdx_value=2048,
        ),
        EnumValueMetadata(
            name="DATIVE",
            xml_value="dative",
            cdx_value=4096,
        ),
        EnumValueMetadata(
            name="IONIC",
            xml_value="ionic",
            cdx_value=8192,
        ),
        EnumValueMetadata(
            name="HYDROGEN",
            xml_value="hydrogen",
            cdx_value=16384,
        ),
        EnumValueMetadata(
            name="THREE_CENTER",
            xml_value="threecenter",
            cdx_value=32768,
        ),
    ),
    status="known",
    provenance=(
        P_2bc112fb03b8ea75ed40,
        P_848222e269e6d1d97def,
        P_801c2c2b387f286306ca,
    ),
)
