# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TagType enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_69071db921c6985ed82a
from ..provenance.sdk_page_objecttag import P_5fb05d0d7739b4cb8c06
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="TagType",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNKNOWN",
            xml_value="Unknown",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="STRING",
            xml_value="String",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="LONG",
            xml_value="Long",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="DOUBLE",
            xml_value="Double",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_69071db921c6985ed82a,
        P_5fb05d0d7739b4cb8c06,
    ),
)
