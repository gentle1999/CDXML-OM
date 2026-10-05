# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Bond ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_0b58f0d3b5f0fbb15469
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Bond",
    xml_tag="b",
    cdx_id=32773,
    cdx_constant="kCDXObj_Bond",
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
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.t.warning": PROPERTY_METADATA["dtd.t.warning"],
            "common.visible": PROPERTY_METADATA["common.visible"],
            "dtd.b.topology": PROPERTY_METADATA["dtd.b.topology"],
            "dtd.t.superseded_by": PROPERTY_METADATA["dtd.t.superseded_by"],
            "dtd.CDXML.show_bond_stereo": PROPERTY_METADATA["dtd.CDXML.show_bond_stereo"],
            "dtd.CDXML.show_bond_rxn": PROPERTY_METADATA["dtd.CDXML.show_bond_rxn"],
            "dtd.CDXML.show_bond_query": PROPERTY_METADATA["dtd.CDXML.show_bond_query"],
            "dtd.b.rxn_participation": PROPERTY_METADATA["dtd.b.rxn_participation"],
            "bond.order": PROPERTY_METADATA["bond.order"],
            "dtd.CDXML.margin_width": PROPERTY_METADATA["dtd.CDXML.margin_width"],
            "dtd.CDXML.line_width": PROPERTY_METADATA["dtd.CDXML.line_width"],
            "dtd.CDXML.label_size": PROPERTY_METADATA["dtd.CDXML.label_size"],
            "dtd.CDXML.label_font": PROPERTY_METADATA["dtd.CDXML.label_font"],
            "dtd.CDXML.label_face": PROPERTY_METADATA["dtd.CDXML.label_face"],
            "text.ignore_warnings": PROPERTY_METADATA["text.ignore_warnings"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.CDXML.hash_spacing": PROPERTY_METADATA["dtd.CDXML.hash_spacing"],
            "dtd.b.end_external_num": PROPERTY_METADATA["dtd.b.end_external_num"],
            "dtd.b.end_attach": PROPERTY_METADATA["dtd.b.end_attach"],
            "bond.end": PROPERTY_METADATA["bond.end"],
            "dtd.b.double_position": PROPERTY_METADATA["dtd.b.double_position"],
            "dtd.b.display2": PROPERTY_METADATA["dtd.b.display2"],
            "bond.display": PROPERTY_METADATA["bond.display"],
            "dtd.b.crossing_bondss": PROPERTY_METADATA["dtd.b.crossing_bondss"],
            "dtd.b.crossing_bonds": PROPERTY_METADATA["dtd.b.crossing_bonds"],
            "dtd.b.connectivity": PROPERTY_METADATA["dtd.b.connectivity"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.b.bs": PROPERTY_METADATA["dtd.b.bs"],
            "dtd.CDXML.bond_spacing_abs": PROPERTY_METADATA["dtd.CDXML.bond_spacing_abs"],
            "dtd.CDXML.bond_spacing": PROPERTY_METADATA["dtd.CDXML.bond_spacing"],
            "dtd.CDXML.bond_length": PROPERTY_METADATA["dtd.CDXML.bond_length"],
            "dtd.b.bond_circular_ordering": PROPERTY_METADATA["dtd.b.bond_circular_ordering"],
            "dtd.CDXML.bold_width": PROPERTY_METADATA["dtd.CDXML.bold_width"],
            "dtd.b.begin_external_num": PROPERTY_METADATA["dtd.b.begin_external_num"],
            "dtd.b.begin_attach": PROPERTY_METADATA["dtd.b.begin_attach"],
            "bond.begin": PROPERTY_METADATA["bond.begin"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_0b58f0d3b5f0fbb15469,),
)
