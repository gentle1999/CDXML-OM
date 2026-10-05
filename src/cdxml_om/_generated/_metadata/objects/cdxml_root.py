# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the CDXMLRoot ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_c35dfc2ee15aff46afd0
from ..provenance.sdk_objects import P_39449c3015fe27b4fa8d
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="CDXMLRoot",
    xml_tag="CDXML",
    cdx_id=32768,
    cdx_constant="kCDXObj_Document",
    category="document_root",
    id_scope="none",
    allowed_parents=(),
    status="known",
    children=(
        ChildMetadata(
            object_type="color_table",
            collection_name="color_tables",
            min_occurs=0,
            max_occurs=1,
        ),
        ChildMetadata(
            object_type="font_table",
            collection_name="font_tables",
            min_occurs=0,
            max_occurs=1,
        ),
        ChildMetadata(
            object_type="page",
            collection_name="pages",
            min_occurs=1,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="template_grid",
            collection_name="template_grids",
            min_occurs=0,
            max_occurs=1,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.CDXML.show_residue_id": PROPERTY_METADATA["dtd.CDXML.show_residue_id"],
            "dtd.CDXML.rxn_autonumber_style": PROPERTY_METADATA["dtd.CDXML.rxn_autonumber_style"],
            "dtd.CDXML.rxn_autonumber_start": PROPERTY_METADATA["dtd.CDXML.rxn_autonumber_start"],
            "dtd.CDXML.rxn_autonumber_format": PROPERTY_METADATA["dtd.CDXML.rxn_autonumber_format"],
            "dtd.CDXML.rxn_autonumber_conditions": PROPERTY_METADATA[
                "dtd.CDXML.rxn_autonumber_conditions"
            ],
            "dtd.CDXML.residue_wrap_count": PROPERTY_METADATA["dtd.CDXML.residue_wrap_count"],
            "dtd.CDXML.residue_block_count": PROPERTY_METADATA["dtd.CDXML.residue_block_count"],
            "dtd.CDXML.chem_prop_p_ka": PROPERTY_METADATA["dtd.CDXML.chem_prop_p_ka"],
            "dtd.CDXML.chem_prop_log_s": PROPERTY_METADATA["dtd.CDXML.chem_prop_log_s"],
            "dtd.CDXML.chem_prop_fragment_label": PROPERTY_METADATA[
                "dtd.CDXML.chem_prop_fragment_label"
            ],
            "dtd.CDXML.chem_prop_id": PROPERTY_METADATA["dtd.CDXML.chem_prop_id"],
            "dtd.CDXML.win_print_info": PROPERTY_METADATA["dtd.CDXML.win_print_info"],
            "dtd.CDXML.window_size": PROPERTY_METADATA["dtd.CDXML.window_size"],
            "dtd.CDXML.window_position": PROPERTY_METADATA["dtd.CDXML.window_position"],
            "dtd.CDXML.window_is_zoomed": PROPERTY_METADATA["dtd.CDXML.window_is_zoomed"],
            "dtd.CDXML.show_terminal_carbon_labels": PROPERTY_METADATA[
                "dtd.CDXML.show_terminal_carbon_labels"
            ],
            "dtd.CDXML.show_sequence_unlinked_branches": PROPERTY_METADATA[
                "dtd.CDXML.show_sequence_unlinked_branches"
            ],
            "dtd.CDXML.show_sequence_termini": PROPERTY_METADATA["dtd.CDXML.show_sequence_termini"],
            "dtd.CDXML.show_sequence_bonds": PROPERTY_METADATA["dtd.CDXML.show_sequence_bonds"],
            "dtd.CDXML.show_non_terminal_carbon_labels": PROPERTY_METADATA[
                "dtd.CDXML.show_non_terminal_carbon_labels"
            ],
            "dtd.CDXML.show_bond_stereo": PROPERTY_METADATA["dtd.CDXML.show_bond_stereo"],
            "dtd.CDXML.show_bond_rxn": PROPERTY_METADATA["dtd.CDXML.show_bond_rxn"],
            "dtd.CDXML.show_bond_query": PROPERTY_METADATA["dtd.CDXML.show_bond_query"],
            "dtd.CDXML.show_atom_stereo": PROPERTY_METADATA["dtd.CDXML.show_atom_stereo"],
            "dtd.CDXML.show_atom_query": PROPERTY_METADATA["dtd.CDXML.show_atom_query"],
            "dtd.CDXML.show_atom_number": PROPERTY_METADATA["dtd.CDXML.show_atom_number"],
            "dtd.CDXML.show_atom_enhanced_stereo": PROPERTY_METADATA[
                "dtd.CDXML.show_atom_enhanced_stereo"
            ],
            "dtd.CDXML.print_margins": PROPERTY_METADATA["dtd.CDXML.print_margins"],
            "dtd.CDXML.name": PROPERTY_METADATA["dtd.CDXML.name"],
            "dtd.CDXML.modification_user_name": PROPERTY_METADATA[
                "dtd.CDXML.modification_user_name"
            ],
            "dtd.CDXML.modification_program": PROPERTY_METADATA["dtd.CDXML.modification_program"],
            "dtd.CDXML.modification_date": PROPERTY_METADATA["dtd.CDXML.modification_date"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.magnification": PROPERTY_METADATA["dtd.CDXML.magnification"],
            "dtd.CDXML.mac_print_info": PROPERTY_METADATA["dtd.CDXML.mac_print_info"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_line_height": PROPERTY_METADATA["dtd.CDXML.label_line_height"],
            "dtd.CDXML.label_justification": PROPERTY_METADATA["dtd.CDXML.label_justification"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "dtd.CDXML.label_color": PROPERTY_METADATA["dtd.CDXML.label_color"],
            "dtd.CDXML.interpret_chemically": PROPERTY_METADATA["dtd.CDXML.interpret_chemically"],
            "dtd.CDXML.hide_implicit_hydrogens": PROPERTY_METADATA[
                "dtd.CDXML.hide_implicit_hydrogens"
            ],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "dtd.CDXML.fractional_widths": PROPERTY_METADATA["dtd.CDXML.fractional_widths"],
            "dtd.CDXML.fix_in_place_gap": PROPERTY_METADATA["dtd.CDXML.fix_in_place_gap"],
            "dtd.CDXML.fix_in_place_extent": PROPERTY_METADATA["dtd.CDXML.fix_in_place_extent"],
            "dtd.CDXML.creation_user_name": PROPERTY_METADATA["dtd.CDXML.creation_user_name"],
            "dtd.CDXML.creation_program": PROPERTY_METADATA["dtd.CDXML.creation_program"],
            "dtd.CDXML.creation_date": PROPERTY_METADATA["dtd.CDXML.creation_date"],
            "dtd.CDXML.comment": PROPERTY_METADATA["dtd.CDXML.comment"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.CDXML.chem_propt_psa": PROPERTY_METADATA["dtd.CDXML.chem_propt_psa"],
            "dtd.CDXML.chem_prop_name": PROPERTY_METADATA["dtd.CDXML.chem_prop_name"],
            "dtd.CDXML.chem_prop_mr": PROPERTY_METADATA["dtd.CDXML.chem_prop_mr"],
            "dtd.CDXML.chem_prop_m_over_z": PROPERTY_METADATA["dtd.CDXML.chem_prop_m_over_z"],
            "dtd.CDXML.chem_prop_mol_wt": PROPERTY_METADATA["dtd.CDXML.chem_prop_mol_wt"],
            "dtd.CDXML.chem_prop_melting_pt": PROPERTY_METADATA["dtd.CDXML.chem_prop_melting_pt"],
            "dtd.CDXML.chem_prop_log_p": PROPERTY_METADATA["dtd.CDXML.chem_prop_log_p"],
            "dtd.CDXML.chem_prop_henry": PROPERTY_METADATA["dtd.CDXML.chem_prop_henry"],
            "dtd.CDXML.chem_prop_gibbs": PROPERTY_METADATA["dtd.CDXML.chem_prop_gibbs"],
            "dtd.CDXML.chem_prop_formula": PROPERTY_METADATA["dtd.CDXML.chem_prop_formula"],
            "dtd.CDXML.chem_prop_exact_mass": PROPERTY_METADATA["dtd.CDXML.chem_prop_exact_mass"],
            "dtd.CDXML.chem_prop_e_form": PROPERTY_METADATA["dtd.CDXML.chem_prop_e_form"],
            "dtd.CDXML.chem_prop_crit_vol": PROPERTY_METADATA["dtd.CDXML.chem_prop_crit_vol"],
            "dtd.CDXML.chem_prop_crit_temp": PROPERTY_METADATA["dtd.CDXML.chem_prop_crit_temp"],
            "dtd.CDXML.chem_prop_crit_pres": PROPERTY_METADATA["dtd.CDXML.chem_prop_crit_pres"],
            "dtd.CDXML.chem_prop_cmr": PROPERTY_METADATA["dtd.CDXML.chem_prop_cmr"],
            "dtd.CDXML.chem_prop_c_log_p": PROPERTY_METADATA["dtd.CDXML.chem_prop_c_log_p"],
            "dtd.CDXML.chem_prop_boiling_pt": PROPERTY_METADATA["dtd.CDXML.chem_prop_boiling_pt"],
            "dtd.CDXML.chem_prop_analysis": PROPERTY_METADATA["dtd.CDXML.chem_prop_analysis"],
            "dtd.CDXML.chain_angle": PROPERTY_METADATA["dtd.CDXML.chain_angle"],
            "dtd.CDXML.cartridge_data": PROPERTY_METADATA["dtd.CDXML.cartridge_data"],
            "dtd.CDXML.caption_size": PROPERTY_METADATA["dtd.CDXML.caption_size"],
            "dtd.CDXML.caption_line_height": PROPERTY_METADATA["dtd.CDXML.caption_line_height"],
            "dtd.CDXML.caption_justification": PROPERTY_METADATA["dtd.CDXML.caption_justification"],
            "dtd.CDXML.caption_font": PROPERTY_METADATA["dtd.CDXML.caption_font"],
            "dtd.CDXML.caption_face": PROPERTY_METADATA["dtd.CDXML.caption_face"],
            "dtd.CDXML.caption_color": PROPERTY_METADATA["dtd.CDXML.caption_color"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bond_spacing_abs": PROPERTY_METADATA["dtd.CDXML.bond_spacing_abs"],
            "dtd.CDXML.bond_spacing": PROPERTY_METADATA["dtd.CDXML.bond_spacing"],
            "dtd.CDXML.bond_length": PROPERTY_METADATA["dtd.CDXML.bond_length"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
            "dtd.CDXML.bgalpha": PROPERTY_METADATA["dtd.CDXML.bgalpha"],
            "dtd.CDXML.amino_acid_termini": PROPERTY_METADATA["dtd.CDXML.amino_acid_termini"],
        }
    ),
    provenance=(
        P_c35dfc2ee15aff46afd0,
        P_39449c3015fe27b4fa8d,
    ),
)
