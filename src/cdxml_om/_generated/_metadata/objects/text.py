# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Text ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_590282425b0c264512be
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Text",
    xml_tag="t",
    cdx_id=32774,
    cdx_constant="kCDXObj_Text",
    category="document_object",
    id_scope="document",
    allowed_parents=(
        "page",
        "group",
        "fragment",
        "node",
        "graphic",
        "alt_group",
        "object_tag",
        "sequence",
        "cross_reference",
        "gep_lane",
        "marker",
        "plasmid_map",
        "plasmid_marker",
    ),
    status="known",
    children=(
        ChildMetadata(
            object_type="text_run",
            collection_name="runs",
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
            "dtd.t.word_wrap_width": PROPERTY_METADATA["dtd.t.word_wrap_width"],
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.t.rotation_angle": PROPERTY_METADATA["dtd.t.rotation_angle"],
            "node.position": PROPERTY_METADATA["node.position"],
            "dtd.t.line_height": PROPERTY_METADATA["dtd.t.line_height"],
            "dtd.t.line_starts": PROPERTY_METADATA["dtd.t.line_starts"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_line_height": PROPERTY_METADATA["dtd.CDXML.label_line_height"],
            "dtd.CDXML.label_justification": PROPERTY_METADATA["dtd.CDXML.label_justification"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "dtd.CDXML.label_color": PROPERTY_METADATA["dtd.CDXML.label_color"],
            "dtd.t.label_alignment": PROPERTY_METADATA["dtd.t.label_alignment"],
            "dtd.t.justification": PROPERTY_METADATA["dtd.t.justification"],
            "dtd.CDXML.interpret_chemically": PROPERTY_METADATA["dtd.CDXML.interpret_chemically"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.CDXML.caption_size": PROPERTY_METADATA["dtd.CDXML.caption_size"],
            "dtd.CDXML.caption_line_height": PROPERTY_METADATA["dtd.CDXML.caption_line_height"],
            "dtd.CDXML.caption_justification": PROPERTY_METADATA["dtd.CDXML.caption_justification"],
            "dtd.CDXML.caption_font": PROPERTY_METADATA["dtd.CDXML.caption_font"],
            "dtd.CDXML.caption_face": PROPERTY_METADATA["dtd.CDXML.caption_face"],
            "dtd.CDXML.caption_color": PROPERTY_METADATA["dtd.CDXML.caption_color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
        }
    ),
    provenance=(P_590282425b0c264512be,),
)
