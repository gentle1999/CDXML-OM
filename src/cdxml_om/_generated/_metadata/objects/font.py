# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Font ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_a2a3cd36107f37a47ccd
from ..provenance.sdk_font import P_e2b47ddc4cde18d7ae1a
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Font",
    xml_tag="font",
    cdx_id=None,
    cdx_constant=None,
    category="local_resource",
    id_scope="local",
    allowed_parents=("font_table",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "font.charset": PROPERTY_METADATA["font.charset"],
            "font.name": PROPERTY_METADATA["font.name"],
            "font.id": PROPERTY_METADATA["font.id"],
        }
    ),
    provenance=(
        P_a2a3cd36107f37a47ccd,
        P_e2b47ddc4cde18d7ae1a,
    ),
)
