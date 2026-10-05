# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Border ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_e02d77c862fa2d837afc
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Border",
    xml_tag="border",
    cdx_id=32800,
    cdx_constant="kCDXObj_Border",
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.border.side": PROPERTY_METADATA["dtd.border.side"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
        }
    ),
    provenance=(P_e02d77c862fa2d837afc,),
)
