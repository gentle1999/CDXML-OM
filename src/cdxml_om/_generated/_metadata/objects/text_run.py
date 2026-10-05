# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TextRun ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_74ead76ebaf5d7c26110
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="TextRun",
    xml_tag="s",
    cdx_id=None,
    cdx_constant=None,
    category="text_run",
    id_scope="none",
    allowed_parents=("text", "rlogic"),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "text_run.alpha": PROPERTY_METADATA["text_run.alpha"],
            "text_run.size": PROPERTY_METADATA["text_run.size"],
            "text_run.font_id": PROPERTY_METADATA["text_run.font_id"],
            "text_run.face": PROPERTY_METADATA["text_run.face"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "text_run.content": PROPERTY_METADATA["text_run.content"],
        }
    ),
    provenance=(P_74ead76ebaf5d7c26110,),
)
