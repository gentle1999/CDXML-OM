# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the TemplateGrid ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_b5c40a3b5c72846c63b5
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="TemplateGrid",
    xml_tag="templategrid",
    cdx_id=32779,
    cdx_constant="kCDXObj_TemplateGrid",
    category="document_object",
    id_scope="none",
    allowed_parents=("cdxml_root",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.templategrid.extent": PROPERTY_METADATA["dtd.templategrid.extent"],
            "dtd.templategrid.pane_height": PROPERTY_METADATA["dtd.templategrid.pane_height"],
            "dtd.templategrid.num_rows": PROPERTY_METADATA["dtd.templategrid.num_rows"],
            "dtd.templategrid.num_columns": PROPERTY_METADATA["dtd.templategrid.num_columns"],
        }
    ),
    provenance=(P_b5c40a3b5c72846c63b5,),
)
