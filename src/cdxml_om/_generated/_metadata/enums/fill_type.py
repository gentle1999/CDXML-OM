# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the FillType enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_8e9a34a9de3a050b8509
from ..provenance.sdk_page_curve import P_ccca058d0f616be8c766
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="FillType",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="VALUE_NONE",
            xml_value="None",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="SOLID",
            xml_value="Solid",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="SHADED",
            xml_value="Shaded",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_8e9a34a9de3a050b8509,
        P_ccca058d0f616be8c766,
    ),
)
