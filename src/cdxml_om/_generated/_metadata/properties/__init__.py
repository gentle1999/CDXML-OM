# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Read-only mapping of canonical property metadata objects."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..types import PropertyMetadata
from .alt_group import PROPERTY_METADATA_GROUP as _properties_alt_group
from .annotation import PROPERTY_METADATA_GROUP as _properties_annotation
from .arrow import PROPERTY_METADATA_GROUP as _properties_arrow
from .bio_shape import PROPERTY_METADATA_GROUP as _properties_bio_shape
from .bond import PROPERTY_METADATA_GROUP as _properties_bond
from .border import PROPERTY_METADATA_GROUP as _properties_border
from .bracket_attachment import PROPERTY_METADATA_GROUP as _properties_bracket_attachment
from .bracketed_group import PROPERTY_METADATA_GROUP as _properties_bracketed_group
from .cdxml_root import PROPERTY_METADATA_GROUP as _properties_cdxml_root
from .chemical_property import PROPERTY_METADATA_GROUP as _properties_chemical_property
from .color import PROPERTY_METADATA_GROUP as _properties_color
from .constraint import PROPERTY_METADATA_GROUP as _properties_constraint
from .cross_reference import PROPERTY_METADATA_GROUP as _properties_cross_reference
from .crossing_bond import PROPERTY_METADATA_GROUP as _properties_crossing_bond
from .curve import PROPERTY_METADATA_GROUP as _properties_curve
from .embedded_object import PROPERTY_METADATA_GROUP as _properties_embedded_object
from .font import PROPERTY_METADATA_GROUP as _properties_font
from .fragment import PROPERTY_METADATA_GROUP as _properties_fragment
from .geometry import PROPERTY_METADATA_GROUP as _properties_geometry
from .gep_band import PROPERTY_METADATA_GROUP as _properties_gep_band
from .gep_plate import PROPERTY_METADATA_GROUP as _properties_gep_plate
from .graphic import PROPERTY_METADATA_GROUP as _properties_graphic
from .group import PROPERTY_METADATA_GROUP as _properties_group
from .node import PROPERTY_METADATA_GROUP as _properties_node
from .object_tag import PROPERTY_METADATA_GROUP as _properties_object_tag
from .page import PROPERTY_METADATA_GROUP as _properties_page
from .plasmid_map import PROPERTY_METADATA_GROUP as _properties_plasmid_map
from .plasmid_region import PROPERTY_METADATA_GROUP as _properties_plasmid_region
from .reaction_step import PROPERTY_METADATA_GROUP as _properties_reaction_step
from .registry_number import PROPERTY_METADATA_GROUP as _properties_registry_number
from .represent import PROPERTY_METADATA_GROUP as _properties_represent
from .rlogic_item import PROPERTY_METADATA_GROUP as _properties_rlogic_item
from .sequence import PROPERTY_METADATA_GROUP as _properties_sequence
from .sg_component import PROPERTY_METADATA_GROUP as _properties_sg_component
from .sg_datum import PROPERTY_METADATA_GROUP as _properties_sg_datum
from .shared import PROPERTY_METADATA_GROUP as _properties_shared
from .spectrum import PROPERTY_METADATA_GROUP as _properties_spectrum
from .template_grid import PROPERTY_METADATA_GROUP as _properties_template_grid
from .text import PROPERTY_METADATA_GROUP as _properties_text
from .text_run import PROPERTY_METADATA_GROUP as _properties_text_run
from .tlc_plate import PROPERTY_METADATA_GROUP as _properties_tlc_plate
from .tlc_spot import PROPERTY_METADATA_GROUP as _properties_tlc_spot

PROPERTY_METADATA: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        **_properties_alt_group,
        **_properties_annotation,
        **_properties_arrow,
        **_properties_bio_shape,
        **_properties_bond,
        **_properties_border,
        **_properties_bracket_attachment,
        **_properties_bracketed_group,
        **_properties_cdxml_root,
        **_properties_chemical_property,
        **_properties_color,
        **_properties_constraint,
        **_properties_cross_reference,
        **_properties_crossing_bond,
        **_properties_curve,
        **_properties_embedded_object,
        **_properties_font,
        **_properties_fragment,
        **_properties_geometry,
        **_properties_gep_band,
        **_properties_gep_plate,
        **_properties_graphic,
        **_properties_group,
        **_properties_node,
        **_properties_object_tag,
        **_properties_page,
        **_properties_plasmid_map,
        **_properties_plasmid_region,
        **_properties_reaction_step,
        **_properties_registry_number,
        **_properties_represent,
        **_properties_rlogic_item,
        **_properties_sequence,
        **_properties_sg_component,
        **_properties_sg_datum,
        **_properties_shared,
        **_properties_spectrum,
        **_properties_template_grid,
        **_properties_text,
        **_properties_text_run,
        **_properties_tlc_plate,
        **_properties_tlc_spot,
    }
)
