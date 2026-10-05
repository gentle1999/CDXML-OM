# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the BioShape ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_f6729c78df4f5528ce29
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="BioShape",
    xml_tag="bioshape",
    cdx_id=None,
    cdx_constant=None,
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
            object_type="curve",
            collection_name="curves",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.n.xyz": PROPERTY_METADATA["dtd.n.xyz"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.bioshape.pipe_width": PROPERTY_METADATA["dtd.bioshape.pipe_width"],
            "dtd.bioshape.neck_width": PROPERTY_METADATA["dtd.bioshape.neck_width"],
            "dtd.bioshape.neck_height": PROPERTY_METADATA["dtd.bioshape.neck_height"],
            "dtd.arrow.minor_axis_end3_d": PROPERTY_METADATA["dtd.arrow.minor_axis_end3_d"],
            "dtd.bioshape.membrane_start_angle": PROPERTY_METADATA[
                "dtd.bioshape.membrane_start_angle"
            ],
            "dtd.bioshape.membrane_minor_axis_size": PROPERTY_METADATA[
                "dtd.bioshape.membrane_minor_axis_size"
            ],
            "dtd.bioshape.membrane_major_axis_size": PROPERTY_METADATA[
                "dtd.bioshape.membrane_major_axis_size"
            ],
            "dtd.bioshape.membrane_end_angle": PROPERTY_METADATA["dtd.bioshape.membrane_end_angle"],
            "dtd.bioshape.membrane_element_size": PROPERTY_METADATA[
                "dtd.bioshape.membrane_element_size"
            ],
            "dtd.arrow.major_axis_end3_d": PROPERTY_METADATA["dtd.arrow.major_axis_end3_d"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.graphic.line_type": PROPERTY_METADATA["dtd.graphic.line_type"],
            "dtd.bioshape.immunoglobin_width": PROPERTY_METADATA["dtd.bioshape.immunoglobin_width"],
            "dtd.bioshape.immunoglobin_height": PROPERTY_METADATA[
                "dtd.bioshape.immunoglobin_height"
            ],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.bioshape.helix_protein_extra": PROPERTY_METADATA[
                "dtd.bioshape.helix_protein_extra"
            ],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "dtd.bioshape.golgi_width": PROPERTY_METADATA["dtd.bioshape.golgi_width"],
            "dtd.bioshape.golgi_length": PROPERTY_METADATA["dtd.bioshape.golgi_length"],
            "dtd.bioshape.golgi_height": PROPERTY_METADATA["dtd.bioshape.golgi_height"],
            "dtd.bioshape.gprotein_upper_height": PROPERTY_METADATA[
                "dtd.bioshape.gprotein_upper_height"
            ],
            "dtd.bioshape.gprotein_lower_height": PROPERTY_METADATA[
                "dtd.bioshape.gprotein_lower_height"
            ],
            "arrow.fill_type": PROPERTY_METADATA["arrow.fill_type"],
            "dtd.graphic.fade_percent": PROPERTY_METADATA["dtd.graphic.fade_percent"],
            "dtd.bioshape.enzyme_width": PROPERTY_METADATA["dtd.bioshape.enzyme_width"],
            "dtd.bioshape.enzyme_receptor_size": PROPERTY_METADATA[
                "dtd.bioshape.enzyme_receptor_size"
            ],
            "dtd.bioshape.enzyme_height": PROPERTY_METADATA["dtd.bioshape.enzyme_height"],
            "dtd.bioshape.dna_wave_width": PROPERTY_METADATA["dtd.bioshape.dna_wave_width"],
            "dtd.bioshape.dna_wave_offset": PROPERTY_METADATA["dtd.bioshape.dna_wave_offset"],
            "dtd.bioshape.dna_wave_length": PROPERTY_METADATA["dtd.bioshape.dna_wave_length"],
            "dtd.bioshape.dna_wave_height": PROPERTY_METADATA["dtd.bioshape.dna_wave_height"],
            "dtd.bioshape.cylinder_width": PROPERTY_METADATA["dtd.bioshape.cylinder_width"],
            "dtd.bioshape.cylinder_height": PROPERTY_METADATA["dtd.bioshape.cylinder_height"],
            "dtd.bioshape.cylinder_distance": PROPERTY_METADATA["dtd.bioshape.cylinder_distance"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.bioshape.bio_shape_type": PROPERTY_METADATA["dtd.bioshape.bio_shape_type"],
        }
    ),
    provenance=(P_f6729c78df4f5528ce29,),
)
