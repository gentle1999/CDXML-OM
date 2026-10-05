# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Color ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_6b31a5ccca8524c49ed5
from ..provenance.sdk_color import P_82ed03ba20bb4747fecd
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Color",
    xml_tag="color",
    cdx_id=None,
    cdx_constant=None,
    category="local_resource",
    id_scope="none",
    allowed_parents=("color_table",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "color.r": PROPERTY_METADATA["color.r"],
            "color.b": PROPERTY_METADATA["color.b"],
            "color.g": PROPERTY_METADATA["color.g"],
        }
    ),
    provenance=(
        P_6b31a5ccca8524c49ed5,
        P_82ed03ba20bb4747fecd,
    ),
)
