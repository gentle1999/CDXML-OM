# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the IsotopicAbundance enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_fd7e4fbc0ccf51807e53
from ..provenance.sdk_page_n import P_15cd3ce19528adb3e7ba
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="IsotopicAbundance",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ANY",
            xml_value="Any",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NATURAL",
            xml_value="Natural",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ENRICHED",
            xml_value="Enriched",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="DEFICIENT",
            xml_value="Deficient",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NONNATURAL",
            xml_value="Nonnatural",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_fd7e4fbc0ccf51807e53,
        P_15cd3ce19528adb3e7ba,
    ),
)
