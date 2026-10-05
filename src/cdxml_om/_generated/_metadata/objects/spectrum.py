# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Spectrum ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_fc2f634f6de00ae8b413
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Spectrum",
    xml_tag="spectrum",
    cdx_id=32784,
    cdx_constant="kCDXObj_Spectrum",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "group"),
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
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.spectrum.y_type": PROPERTY_METADATA["dtd.spectrum.y_type"],
            "dtd.spectrum.y_scale": PROPERTY_METADATA["dtd.spectrum.y_scale"],
            "dtd.spectrum.y_low": PROPERTY_METADATA["dtd.spectrum.y_low"],
            "dtd.spectrum.y_axis_label": PROPERTY_METADATA["dtd.spectrum.y_axis_label"],
            "dtd.spectrum.x_type": PROPERTY_METADATA["dtd.spectrum.x_type"],
            "dtd.spectrum.x_spacing": PROPERTY_METADATA["dtd.spectrum.x_spacing"],
            "dtd.spectrum.x_low": PROPERTY_METADATA["dtd.spectrum.x_low"],
            "dtd.spectrum.x_axis_label": PROPERTY_METADATA["dtd.spectrum.x_axis_label"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.spectrum.class_name": PROPERTY_METADATA["dtd.spectrum.class_name"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "spectrum.data": PROPERTY_METADATA["spectrum.data"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_fc2f634f6de00ae8b413,),
)
