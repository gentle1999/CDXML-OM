# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Read-only mapping of canonical ObjectSpec metadata objects."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..types import ObjectMetadata
from .alt_group import OBJECT_METADATA_ENTRY as _object_alt_group
from .annotation import OBJECT_METADATA_ENTRY as _object_annotation
from .arrow import OBJECT_METADATA_ENTRY as _object_arrow
from .bio_shape import OBJECT_METADATA_ENTRY as _object_bio_shape
from .bond import OBJECT_METADATA_ENTRY as _object_bond
from .border import OBJECT_METADATA_ENTRY as _object_border
from .bracket_attachment import OBJECT_METADATA_ENTRY as _object_bracket_attachment
from .bracketed_group import OBJECT_METADATA_ENTRY as _object_bracketed_group
from .cdxml_root import OBJECT_METADATA_ENTRY as _object_cdxml_root
from .chemical_property import OBJECT_METADATA_ENTRY as _object_chemical_property
from .color import OBJECT_METADATA_ENTRY as _object_color
from .color_table import OBJECT_METADATA_ENTRY as _object_color_table
from .colored_molecular_area import OBJECT_METADATA_ENTRY as _object_colored_molecular_area
from .constraint import OBJECT_METADATA_ENTRY as _object_constraint
from .cross_reference import OBJECT_METADATA_ENTRY as _object_cross_reference
from .crossing_bond import OBJECT_METADATA_ENTRY as _object_crossing_bond
from .curve import OBJECT_METADATA_ENTRY as _object_curve
from .embedded_object import OBJECT_METADATA_ENTRY as _object_embedded_object
from .font import OBJECT_METADATA_ENTRY as _object_font
from .font_table import OBJECT_METADATA_ENTRY as _object_font_table
from .fragment import OBJECT_METADATA_ENTRY as _object_fragment
from .geometry import OBJECT_METADATA_ENTRY as _object_geometry
from .gep_band import OBJECT_METADATA_ENTRY as _object_gep_band
from .gep_lane import OBJECT_METADATA_ENTRY as _object_gep_lane
from .gep_plate import OBJECT_METADATA_ENTRY as _object_gep_plate
from .graphic import OBJECT_METADATA_ENTRY as _object_graphic
from .group import OBJECT_METADATA_ENTRY as _object_group
from .marker import OBJECT_METADATA_ENTRY as _object_marker
from .node import OBJECT_METADATA_ENTRY as _object_node
from .object_tag import OBJECT_METADATA_ENTRY as _object_object_tag
from .page import OBJECT_METADATA_ENTRY as _object_page
from .plasmid_map import OBJECT_METADATA_ENTRY as _object_plasmid_map
from .plasmid_marker import OBJECT_METADATA_ENTRY as _object_plasmid_marker
from .plasmid_region import OBJECT_METADATA_ENTRY as _object_plasmid_region
from .reaction_scheme import OBJECT_METADATA_ENTRY as _object_reaction_scheme
from .reaction_step import OBJECT_METADATA_ENTRY as _object_reaction_step
from .registry_number import OBJECT_METADATA_ENTRY as _object_registry_number
from .represent import OBJECT_METADATA_ENTRY as _object_represent
from .rlogic import OBJECT_METADATA_ENTRY as _object_rlogic
from .rlogic_item import OBJECT_METADATA_ENTRY as _object_rlogic_item
from .sequence import OBJECT_METADATA_ENTRY as _object_sequence
from .sg_component import OBJECT_METADATA_ENTRY as _object_sg_component
from .sg_datum import OBJECT_METADATA_ENTRY as _object_sg_datum
from .spectrum import OBJECT_METADATA_ENTRY as _object_spectrum
from .splitter import OBJECT_METADATA_ENTRY as _object_splitter
from .stoichiometry_grid import OBJECT_METADATA_ENTRY as _object_stoichiometry_grid
from .table import OBJECT_METADATA_ENTRY as _object_table
from .template_grid import OBJECT_METADATA_ENTRY as _object_template_grid
from .text import OBJECT_METADATA_ENTRY as _object_text
from .text_run import OBJECT_METADATA_ENTRY as _object_text_run
from .tlc_lane import OBJECT_METADATA_ENTRY as _object_tlc_lane
from .tlc_plate import OBJECT_METADATA_ENTRY as _object_tlc_plate
from .tlc_spot import OBJECT_METADATA_ENTRY as _object_tlc_spot

OBJECT_METADATA: Final[Mapping[str, ObjectMetadata]] = MappingProxyType(
    {
        "alt_group": _object_alt_group,
        "annotation": _object_annotation,
        "arrow": _object_arrow,
        "bio_shape": _object_bio_shape,
        "bond": _object_bond,
        "border": _object_border,
        "bracket_attachment": _object_bracket_attachment,
        "bracketed_group": _object_bracketed_group,
        "cdxml_root": _object_cdxml_root,
        "chemical_property": _object_chemical_property,
        "color": _object_color,
        "color_table": _object_color_table,
        "colored_molecular_area": _object_colored_molecular_area,
        "constraint": _object_constraint,
        "cross_reference": _object_cross_reference,
        "crossing_bond": _object_crossing_bond,
        "curve": _object_curve,
        "embedded_object": _object_embedded_object,
        "font": _object_font,
        "font_table": _object_font_table,
        "fragment": _object_fragment,
        "geometry": _object_geometry,
        "gep_band": _object_gep_band,
        "gep_lane": _object_gep_lane,
        "gep_plate": _object_gep_plate,
        "graphic": _object_graphic,
        "group": _object_group,
        "marker": _object_marker,
        "node": _object_node,
        "object_tag": _object_object_tag,
        "page": _object_page,
        "plasmid_map": _object_plasmid_map,
        "plasmid_marker": _object_plasmid_marker,
        "plasmid_region": _object_plasmid_region,
        "reaction_scheme": _object_reaction_scheme,
        "reaction_step": _object_reaction_step,
        "registry_number": _object_registry_number,
        "represent": _object_represent,
        "rlogic": _object_rlogic,
        "rlogic_item": _object_rlogic_item,
        "sequence": _object_sequence,
        "sg_component": _object_sg_component,
        "sg_datum": _object_sg_datum,
        "spectrum": _object_spectrum,
        "splitter": _object_splitter,
        "stoichiometry_grid": _object_stoichiometry_grid,
        "table": _object_table,
        "template_grid": _object_template_grid,
        "text": _object_text,
        "text_run": _object_text_run,
        "tlc_lane": _object_tlc_lane,
        "tlc_plate": _object_tlc_plate,
        "tlc_spot": _object_tlc_spot,
    }
)
