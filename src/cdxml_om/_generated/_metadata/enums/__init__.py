# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Read-only mapping of named enum metadata."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..types import EnumMetadata
from .amino_acid_termini import ENUM_METADATA_ENTRY as _enum_amino_acid_termini
from .arrow_type import ENUM_METADATA_ENTRY as _enum_arrow_type
from .arrowhead_side import ENUM_METADATA_ENTRY as _enum_arrowhead_side
from .arrowhead_type import ENUM_METADATA_ENTRY as _enum_arrowhead_type
from .bio_shape_type import ENUM_METADATA_ENTRY as _enum_bio_shape_type
from .bond_display import ENUM_METADATA_ENTRY as _enum_bond_display
from .bond_order import ENUM_METADATA_ENTRY as _enum_bond_order
from .bond_stereochemistry import ENUM_METADATA_ENTRY as _enum_bond_stereochemistry
from .bracket_type import ENUM_METADATA_ENTRY as _enum_bracket_type
from .bracket_usage import ENUM_METADATA_ENTRY as _enum_bracket_usage
from .caption_justification import ENUM_METADATA_ENTRY as _enum_caption_justification
from .connectivity import ENUM_METADATA_ENTRY as _enum_connectivity
from .constraint_type import ENUM_METADATA_ENTRY as _enum_constraint_type
from .double_position import ENUM_METADATA_ENTRY as _enum_double_position
from .drawing_space import ENUM_METADATA_ENTRY as _enum_drawing_space
from .external_connection_type import ENUM_METADATA_ENTRY as _enum_external_connection_type
from .fill_type import ENUM_METADATA_ENTRY as _enum_fill_type
from .geometric_feature import ENUM_METADATA_ENTRY as _enum_geometric_feature
from .graphic_type import ENUM_METADATA_ENTRY as _enum_graphic_type
from .isotopic_abundance import ENUM_METADATA_ENTRY as _enum_isotopic_abundance
from .justification import ENUM_METADATA_ENTRY as _enum_justification
from .label_alignment import ENUM_METADATA_ENTRY as _enum_label_alignment
from .label_display import ENUM_METADATA_ENTRY as _enum_label_display
from .label_justification import ENUM_METADATA_ENTRY as _enum_label_justification
from .line_type import ENUM_METADATA_ENTRY as _enum_line_type
from .no_go import ENUM_METADATA_ENTRY as _enum_no_go
from .node_geometry import ENUM_METADATA_ENTRY as _enum_node_geometry
from .node_stereochemistry import ENUM_METADATA_ENTRY as _enum_node_stereochemistry
from .node_type import ENUM_METADATA_ENTRY as _enum_node_type
from .orbital_type import ENUM_METADATA_ENTRY as _enum_orbital_type
from .page_definition import ENUM_METADATA_ENTRY as _enum_page_definition
from .polymer_flip_type import ENUM_METADATA_ENTRY as _enum_polymer_flip_type
from .polymer_repeat_pattern import ENUM_METADATA_ENTRY as _enum_polymer_repeat_pattern
from .positioning_type import ENUM_METADATA_ENTRY as _enum_positioning_type
from .radical import ENUM_METADATA_ENTRY as _enum_radical
from .ring_bond_count import ENUM_METADATA_ENTRY as _enum_ring_bond_count
from .rxn_participation import ENUM_METADATA_ENTRY as _enum_rxn_participation
from .rxn_stereo import ENUM_METADATA_ENTRY as _enum_rxn_stereo
from .sequence_type import ENUM_METADATA_ENTRY as _enum_sequence_type
from .side import ENUM_METADATA_ENTRY as _enum_side
from .spectrum_class import ENUM_METADATA_ENTRY as _enum_spectrum_class
from .spectrum_x_type import ENUM_METADATA_ENTRY as _enum_spectrum_x_type
from .spectrum_y_type import ENUM_METADATA_ENTRY as _enum_spectrum_y_type
from .symbol_type import ENUM_METADATA_ENTRY as _enum_symbol_type
from .tag_type import ENUM_METADATA_ENTRY as _enum_tag_type
from .topology import ENUM_METADATA_ENTRY as _enum_topology
from .translation import ENUM_METADATA_ENTRY as _enum_translation
from .unsaturated_bonds import ENUM_METADATA_ENTRY as _enum_unsaturated_bonds

ENUM_METADATA: Final[Mapping[str, EnumMetadata]] = MappingProxyType(
    {
        "dtd.amino_acid_termini.a05085d7": _enum_amino_acid_termini,
        "dtd.arrow_type.7aa56e9a": _enum_arrow_type,
        "dtd.arrowhead_side.ee4d6e99": _enum_arrowhead_side,
        "dtd.arrowhead_type.7f4897fa": _enum_arrowhead_type,
        "dtd.bio_shape_type.5423fc35": _enum_bio_shape_type,
        "bond_display": _enum_bond_display,
        "bond_order": _enum_bond_order,
        "dtd.bs.c9410bb4": _enum_bond_stereochemistry,
        "dtd.bracket_type.8269cca1": _enum_bracket_type,
        "dtd.bracket_usage.df42ccc5": _enum_bracket_usage,
        "dtd.caption_justification.a0380828": _enum_caption_justification,
        "dtd.connectivity.086332b0": _enum_connectivity,
        "dtd.constraint_type.eba13b7c": _enum_constraint_type,
        "dtd.double_position.94c4e4b1": _enum_double_position,
        "dtd.drawing_space.46069ac7": _enum_drawing_space,
        "dtd.external_connection_type.ade6bb36": _enum_external_connection_type,
        "dtd.fill_type.b141cafb": _enum_fill_type,
        "dtd.geometric_feature.4250a286": _enum_geometric_feature,
        "graphic_type": _enum_graphic_type,
        "dtd.isotopic_abundance.6221caac": _enum_isotopic_abundance,
        "dtd.justification.8e038579": _enum_justification,
        "dtd.label_alignment.aa6f97a8": _enum_label_alignment,
        "dtd.label_display.aa6f97a8": _enum_label_display,
        "dtd.label_justification.aa6f97a8": _enum_label_justification,
        "dtd.line_type.79d84f4b": _enum_line_type,
        "dtd.no_go.dbf92440": _enum_no_go,
        "dtd.node_geometry.8bcf7656": _enum_node_geometry,
        "dtd.as.a82c6cfb": _enum_node_stereochemistry,
        "dtd.node_type.18813628": _enum_node_type,
        "dtd.orbital_type.7ae4dc1f": _enum_orbital_type,
        "dtd.page_definition.5d48b9f1": _enum_page_definition,
        "dtd.polymer_flip_type.7cf04eb5": _enum_polymer_flip_type,
        "dtd.polymer_repeat_pattern.a2cadba9": _enum_polymer_repeat_pattern,
        "dtd.positioning_type.e8ee9663": _enum_positioning_type,
        "dtd.radical.6ba1138c": _enum_radical,
        "dtd.ring_bond_count.d444e4df": _enum_ring_bond_count,
        "dtd.rxn_participation.71b2b5ce": _enum_rxn_participation,
        "dtd.rxn_stereo.65b93c38": _enum_rxn_stereo,
        "dtd.sequence_type.35f3b725": _enum_sequence_type,
        "dtd.side.5dd5ccc4": _enum_side,
        "dtd.class.3a799156": _enum_spectrum_class,
        "dtd.x_type.a4fb96d1": _enum_spectrum_x_type,
        "dtd.y_type.b80d81f1": _enum_spectrum_y_type,
        "dtd.symbol_type.4aa0ee0c": _enum_symbol_type,
        "dtd.tag_type.e6aee297": _enum_tag_type,
        "dtd.topology.62163c3d": _enum_topology,
        "dtd.translation.24452af8": _enum_translation,
        "dtd.unsaturated_bonds.b4aa355d": _enum_unsaturated_bonds,
    }
)
