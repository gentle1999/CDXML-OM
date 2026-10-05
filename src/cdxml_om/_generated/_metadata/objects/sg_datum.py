# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the SGDatum ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_30d2c1be0bb31af0a84c
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="SGDatum",
    xml_tag="sgdatum",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("sg_component",),
    status="known",
    children=(
        ChildMetadata(
            object_type="object_tag",
            collection_name="objecttags",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="embedded_object",
            collection_name="embeddedobjects",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.sgdatum.sg_property_type": PROPERTY_METADATA["dtd.sgdatum.sg_property_type"],
            "dtd.sgdatum.sg_data_value": PROPERTY_METADATA["dtd.sgdatum.sg_data_value"],
            "dtd.sgdatum.sg_data_type": PROPERTY_METADATA["dtd.sgdatum.sg_data_type"],
            "dtd.sgdatum.is_read_only": PROPERTY_METADATA["dtd.sgdatum.is_read_only"],
            "dtd.sgdatum.is_hidden": PROPERTY_METADATA["dtd.sgdatum.is_hidden"],
            "dtd.sgdatum.is_edited": PROPERTY_METADATA["dtd.sgdatum.is_edited"],
        }
    ),
    provenance=(P_30d2c1be0bb31af0a84c,),
)
