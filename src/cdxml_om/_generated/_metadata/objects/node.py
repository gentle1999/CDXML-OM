# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Node ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_00360c0cbea36ee754be
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Node",
    xml_tag="n",
    cdx_id=32772,
    cdx_constant="kCDXObj_Node",
    category="document_object",
    id_scope="document",
    allowed_parents=("fragment",),
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
    ),
    properties=MappingProxyType(
        {
            "dtd.n.abnormal_valence": PROPERTY_METADATA["dtd.n.abnormal_valence"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.n.xyz": PROPERTY_METADATA["dtd.n.xyz"],
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.n.unsaturated_bonds": PROPERTY_METADATA["dtd.n.unsaturated_bonds"],
            "dtd.n.translation": PROPERTY_METADATA["dtd.n.translation"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.n.substituents_up_to": PROPERTY_METADATA["dtd.n.substituents_up_to"],
            "dtd.n.substituents_exactly": PROPERTY_METADATA["dtd.n.substituents_exactly"],
            "dtd.CDXML.show_terminal_carbon_labels": PROPERTY_METADATA[
                "dtd.CDXML.show_terminal_carbon_labels"
            ],
            "dtd.CDXML.show_non_terminal_carbon_labels": PROPERTY_METADATA[
                "dtd.CDXML.show_non_terminal_carbon_labels"
            ],
            "dtd.CDXML.show_atom_stereo": PROPERTY_METADATA["dtd.CDXML.show_atom_stereo"],
            "dtd.CDXML.show_atom_query": PROPERTY_METADATA["dtd.CDXML.show_atom_query"],
            "dtd.CDXML.show_atom_number": PROPERTY_METADATA["dtd.CDXML.show_atom_number"],
            "dtd.n.show_atom_id": PROPERTY_METADATA["dtd.n.show_atom_id"],
            "dtd.CDXML.show_atom_enhanced_stereo": PROPERTY_METADATA[
                "dtd.CDXML.show_atom_enhanced_stereo"
            ],
            "dtd.n.rxn_stereo": PROPERTY_METADATA["dtd.n.rxn_stereo"],
            "dtd.n.rxn_change": PROPERTY_METADATA["dtd.n.rxn_change"],
            "dtd.n.ring_bond_count": PROPERTY_METADATA["dtd.n.ring_bond_count"],
            "dtd.n.radical": PROPERTY_METADATA["dtd.n.radical"],
            "node.position": PROPERTY_METADATA["node.position"],
            "dtd.n.node_type": PROPERTY_METADATA["dtd.n.node_type"],
            "dtd.n.num_hydrogens": PROPERTY_METADATA["dtd.n.num_hydrogens"],
            "dtd.n.needs_clean": PROPERTY_METADATA["dtd.n.needs_clean"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.n.link_count_low": PROPERTY_METADATA["dtd.n.link_count_low"],
            "dtd.n.link_count_high": PROPERTY_METADATA["dtd.n.link_count_high"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "dtd.n.label_display": PROPERTY_METADATA["dtd.n.label_display"],
            "dtd.n.isotopic_abundance": PROPERTY_METADATA["dtd.n.isotopic_abundance"],
            "node.isotope": PROPERTY_METADATA["node.isotope"],
            "dtd.n.implicit_hydrogens": PROPERTY_METADATA["dtd.n.implicit_hydrogens"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.CDXML.hide_implicit_hydrogens": PROPERTY_METADATA[
                "dtd.CDXML.hide_implicit_hydrogens"
            ],
            "dtd.n.h_dot": PROPERTY_METADATA["dtd.n.h_dot"],
            "dtd.n.h_dash": PROPERTY_METADATA["dtd.n.h_dash"],
            "dtd.n.generic_nickname": PROPERTY_METADATA["dtd.n.generic_nickname"],
            "dtd.n.generic_list": PROPERTY_METADATA["dtd.n.generic_list"],
            "dtd.n.geometry": PROPERTY_METADATA["dtd.n.geometry"],
            "dtd.n.free_sites": PROPERTY_METADATA["dtd.n.free_sites"],
            "dtd.n.formula": PROPERTY_METADATA["dtd.n.formula"],
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.n.external_connection_num": PROPERTY_METADATA["dtd.n.external_connection_num"],
            "dtd.n.external_connection_type": PROPERTY_METADATA["dtd.n.external_connection_type"],
            "dtd.n.enhanced_stereo_type": PROPERTY_METADATA["dtd.n.enhanced_stereo_type"],
            "dtd.n.enhanced_stereo_group_num": PROPERTY_METADATA["dtd.n.enhanced_stereo_group_num"],
            "dtd.n.element_list": PROPERTY_METADATA["dtd.n.element_list"],
            "node.element": PROPERTY_METADATA["node.element"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "node.charge": PROPERTY_METADATA["node.charge"],
            "dtd.n.bond_ordering": PROPERTY_METADATA["dtd.n.bond_ordering"],
            "dtd.n.attachments": PROPERTY_METADATA["dtd.n.attachments"],
            "dtd.n.atom_number": PROPERTY_METADATA["dtd.n.atom_number"],
            "dtd.n.atom_id": PROPERTY_METADATA["dtd.n.atom_id"],
            "dtd.n.as_value": PROPERTY_METADATA["dtd.n.as_value"],
            "dtd.n.alt_group_id": PROPERTY_METADATA["dtd.n.alt_group_id"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_00360c0cbea36ee754be,),
)
