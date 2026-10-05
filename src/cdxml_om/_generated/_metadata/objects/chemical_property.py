# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ChemicalProperty ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_4b997bfda21d93622793
from ..types import ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="ChemicalProperty",
    xml_tag="chemicalproperty",
    cdx_id=32806,
    cdx_constant="kCDXObj_ChemicalProperty",
    category="document_object",
    id_scope="document",
    allowed_parents=("page",),
    status="known",
    children=(),
    properties=MappingProxyType(
        {
            "dtd.geometry.basis_objects": PROPERTY_METADATA["dtd.geometry.basis_objects"],
            "dtd.chemicalproperty.external_bonds": PROPERTY_METADATA[
                "dtd.chemicalproperty.external_bonds"
            ],
            "dtd.objecttag.positioning_type": PROPERTY_METADATA["dtd.objecttag.positioning_type"],
            "dtd.objecttag.positioning_offset": PROPERTY_METADATA[
                "dtd.objecttag.positioning_offset"
            ],
            "dtd.objecttag.positioning_angle": PROPERTY_METADATA["dtd.objecttag.positioning_angle"],
            "dtd.CDXML.name": PROPERTY_METADATA["dtd.CDXML.name"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.chemicalproperty.chemical_property_type": PROPERTY_METADATA[
                "dtd.chemicalproperty.chemical_property_type"
            ],
            "dtd.chemicalproperty.chemically_significant": PROPERTY_METADATA[
                "dtd.chemicalproperty.chemically_significant"
            ],
            "dtd.chemicalproperty.chemical_property_is_active": PROPERTY_METADATA[
                "dtd.chemicalproperty.chemical_property_is_active"
            ],
            "dtd.chemicalproperty.chemical_property_display_id": PROPERTY_METADATA[
                "dtd.chemicalproperty.chemical_property_display_id"
            ],
        }
    ),
    provenance=(P_4b997bfda21d93622793,),
)
