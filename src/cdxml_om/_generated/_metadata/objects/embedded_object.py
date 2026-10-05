# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the EmbeddedObject ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_65fa42010abd4d0f64fd
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="EmbeddedObject",
    xml_tag="embeddedobject",
    cdx_id=32777,
    cdx_constant="kCDXObj_EmbeddedObject",
    category="document_object",
    id_scope="document",
    allowed_parents=("page", "tlc_spot", "gep_band", "sg_datum"),
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
            "dtd.embeddedobject.windows_metafile": PROPERTY_METADATA[
                "dtd.embeddedobject.windows_metafile"
            ],
            "dtd.embeddedobject.uncompressed_windows_metafile_size": PROPERTY_METADATA[
                "dtd.embeddedobject.uncompressed_windows_metafile_size"
            ],
            "dtd.embeddedobject.uncompressed_ole_object_size": PROPERTY_METADATA[
                "dtd.embeddedobject.uncompressed_ole_object_size"
            ],
            "dtd.embeddedobject.uncompressed_enhanced_metafile_size": PROPERTY_METADATA[
                "dtd.embeddedobject.uncompressed_enhanced_metafile_size"
            ],
            "dtd.embeddedobject.tiff": PROPERTY_METADATA["dtd.embeddedobject.tiff"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.t.rotation_angle": PROPERTY_METADATA["dtd.t.rotation_angle"],
            "dtd.embeddedobject.png": PROPERTY_METADATA["dtd.embeddedobject.png"],
            "dtd.embeddedobject.pdf": PROPERTY_METADATA["dtd.embeddedobject.pdf"],
            "dtd.embeddedobject.ole_object": PROPERTY_METADATA["dtd.embeddedobject.ole_object"],
            "dtd.embeddedobject.mac_pict": PROPERTY_METADATA["dtd.embeddedobject.mac_pict"],
            "dtd.embeddedobject.jpeg": PROPERTY_METADATA["dtd.embeddedobject.jpeg"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.embeddedobject.gif": PROPERTY_METADATA["dtd.embeddedobject.gif"],
            "dtd.embeddedobject.enhanced_metafile": PROPERTY_METADATA[
                "dtd.embeddedobject.enhanced_metafile"
            ],
            "dtd.embeddedobject.edition_alias": PROPERTY_METADATA[
                "dtd.embeddedobject.edition_alias"
            ],
            "dtd.embeddedobject.edition": PROPERTY_METADATA["dtd.embeddedobject.edition"],
            "dtd.embeddedobject.compressed_windows_metafile": PROPERTY_METADATA[
                "dtd.embeddedobject.compressed_windows_metafile"
            ],
            "dtd.embeddedobject.compressed_ole_object": PROPERTY_METADATA[
                "dtd.embeddedobject.compressed_ole_object"
            ],
            "dtd.embeddedobject.compressed_enhanced_metafile": PROPERTY_METADATA[
                "dtd.embeddedobject.compressed_enhanced_metafile"
            ],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.embeddedobject.bmp": PROPERTY_METADATA["dtd.embeddedobject.bmp"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_65fa42010abd4d0f64fd,),
)
