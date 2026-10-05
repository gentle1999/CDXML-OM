# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Table ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_f8db23098d8227b92f5f
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Table",
    xml_tag="table",
    cdx_id=32790,
    cdx_constant="kCDXObj_Table",
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
    status="known",
    children=(
        ChildMetadata(
            object_type="page",
            collection_name="pages",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="object_tag",
            collection_name="objecttags",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_f8db23098d8227b92f5f,),
)
