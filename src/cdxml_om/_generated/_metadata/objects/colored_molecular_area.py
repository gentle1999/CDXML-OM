# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ColoredMolecularArea ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_edda57b6e5ed0a228932
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ColoredMolecularArea",
    xml_tag="coloredmoleculararea",
    cdx_id=None,
    cdx_constant=None,
    category="document_object",
    id_scope="document",
    allowed_parents=("fragment",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.geometry.basis_objects": PROPERTY_METADATA["dtd.geometry.basis_objects"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
        }
    ),
    provenance=(P_edda57b6e5ed0a228932,),
)
