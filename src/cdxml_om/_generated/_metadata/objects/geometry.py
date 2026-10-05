# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Geometry ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_175f537e2f94b1331f74
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Geometry",
    xml_tag="geometry",
    cdx_id=32801,
    cdx_constant="kCDXObj_Geometry",
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
    status="known",
    children=(
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
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.geometry.relation_value": PROPERTY_METADATA["dtd.geometry.relation_value"],
            "dtd.CDXML.name": PROPERTY_METADATA["dtd.CDXML.name"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.geometry.geometric_feature": PROPERTY_METADATA["dtd.geometry.geometric_feature"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.geometry.basis_objects": PROPERTY_METADATA["dtd.geometry.basis_objects"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "dtd.CDXML.label_color": PROPERTY_METADATA["dtd.CDXML.label_color"],
            "dtd.CDXML.bond_length": PROPERTY_METADATA["dtd.CDXML.bond_length"],
            "sdk.geometry.point_is_directed": PROPERTY_METADATA["sdk.geometry.point_is_directed"],
        }
    ),
    provenance=(P_175f537e2f94b1331f74,),
)
