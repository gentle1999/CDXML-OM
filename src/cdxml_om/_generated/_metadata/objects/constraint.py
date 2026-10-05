# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Constraint ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_554819d67afe2459f692
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Constraint",
    xml_tag="constraint",
    cdx_id=32802,
    cdx_constant="kCDXObj_Constraint",
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
            "dtd.constraint.point_is_directed": PROPERTY_METADATA[
                "dtd.constraint.point_is_directed"
            ],
            "dtd.CDXML.name": PROPERTY_METADATA["dtd.CDXML.name"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.constraint.ignore_unconnected_atoms": PROPERTY_METADATA[
                "dtd.constraint.ignore_unconnected_atoms"
            ],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "dtd.constraint.dihedral_is_chiral": PROPERTY_METADATA[
                "dtd.constraint.dihedral_is_chiral"
            ],
            "dtd.constraint.constraint_type": PROPERTY_METADATA["dtd.constraint.constraint_type"],
            "dtd.constraint.constraint_min": PROPERTY_METADATA["dtd.constraint.constraint_min"],
            "dtd.constraint.constraint_max": PROPERTY_METADATA["dtd.constraint.constraint_max"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.geometry.basis_objects": PROPERTY_METADATA["dtd.geometry.basis_objects"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "dtd.CDXML.label_color": PROPERTY_METADATA["dtd.CDXML.label_color"],
            "dtd.CDXML.bond_length": PROPERTY_METADATA["dtd.CDXML.bond_length"],
        }
    ),
    provenance=(P_554819d67afe2459f692,),
)
