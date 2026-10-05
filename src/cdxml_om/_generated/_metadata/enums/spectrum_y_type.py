# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the SpectrumYType enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_6b1ccef09b09b4c12169
from ..provenance.sdk_page_spectrum import P_0728064a13812f7abe08
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="SpectrumYType",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNKNOWN",
            xml_value="Unknown",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ABSORBANCE",
            xml_value="Absorbance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="TRANSMITTANCE",
            xml_value="Transmittance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="PERCENT_TRANSMITTANCE",
            xml_value="PercentTransmittance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="OTHER",
            xml_value="Other",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ARBITRARY_UNITS",
            xml_value="ArbitraryUnits",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_6b1ccef09b09b4c12169,
        P_0728064a13812f7abe08,
    ),
)
