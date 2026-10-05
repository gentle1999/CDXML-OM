# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the AltGroup ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_dbb6ede6f3f2c5b0b78d
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="AltGroup",
    xml_tag="altgroup",
    cdx_id=32778,
    cdx_constant="kCDXObj_NamedAlternativeGroup",
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
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="fragment",
            collection_name="fragments",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="group",
            collection_name="groups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="graphic",
            collection_name="graphics",
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
            "dtd.altgroup.valence": PROPERTY_METADATA["dtd.altgroup.valence"],
            "dtd.altgroup.text_frame": PROPERTY_METADATA["dtd.altgroup.text_frame"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "node.position": PROPERTY_METADATA["node.position"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.altgroup.group_frame": PROPERTY_METADATA["dtd.altgroup.group_frame"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_dbb6ede6f3f2c5b0b78d,),
)
