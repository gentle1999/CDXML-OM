# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Topology enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_4bf5ec97e74bc6473030
from ..provenance.sdk_page_b import P_e56396bbe3c10900c893
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="Topology",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNSPECIFIED",
            xml_value="Unspecified",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="RING",
            xml_value="Ring",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="CHAIN",
            xml_value="Chain",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="RING_OR_CHAIN",
            xml_value="RingOrChain",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_4bf5ec97e74bc6473030,
        P_e56396bbe3c10900c893,
    ),
)
