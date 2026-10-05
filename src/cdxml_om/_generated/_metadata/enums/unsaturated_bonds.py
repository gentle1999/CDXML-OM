# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the UnsaturatedBonds enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_5d62a4de4dd12922a138
from ..provenance.sdk_page_n import P_f78a5124e97cd1256bf4
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="UnsaturatedBonds",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="MUST_BE_ABSENT",
            xml_value="MustBeAbsent",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="MUST_BE_PRESENT",
            xml_value="MustBePresent",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_5d62a4de4dd12922a138,
        P_f78a5124e97cd1256bf4,
    ),
)
