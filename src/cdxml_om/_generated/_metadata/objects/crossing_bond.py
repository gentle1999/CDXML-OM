# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the CrossingBond ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_c6984ac2c1a7a879adc7
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="CrossingBond",
    xml_tag="crossingbond",
    cdx_id=32793,
    cdx_constant="kCDXObj_CrossingBond",
    category="document_object",
    id_scope="document",
    allowed_parents=("bracket_attachment",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.crossingbond.bond_id": PROPERTY_METADATA["dtd.crossingbond.bond_id"],
            "dtd.crossingbond.inner_atom_id": PROPERTY_METADATA["dtd.crossingbond.inner_atom_id"],
            "common.id": PROPERTY_METADATA["common.id"],
        }
    ),
    provenance=(P_c6984ac2c1a7a879adc7,),
)
