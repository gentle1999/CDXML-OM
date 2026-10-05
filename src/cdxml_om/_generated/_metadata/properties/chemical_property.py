# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: chemical_property."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_2fce81cad22761d26b1b,
    P_83b2b7b707c4453850bd,
    P_623eec0f24b4fd627440,
    P_107670a853dfa0a4834b,
    P_ccc819cdca1c3043ddff,
)
from ..provenance.sdk_page_chemicalproperty import (
    P_1c001f3047230cb97452,
    P_783a310b77b6d03cd350,
    P_df02b4a7a137dd774ddd,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.chemicalproperty.chemical_property_display_id": PropertyMetadata(
            owners=("chemical_property",),
            name="chemical_property_display_id",
            xml_name="ChemicalPropertyDisplayID",
            storage="attribute",
            cdx_id=2993,
            cdx_constant="kCDXProp_ChemicalPropertyDisplayID",
            datatype="object_id",
            codec="object_id",
            required=False,
            default=None,
            cardinality="one",
            reference_target="*",
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_2fce81cad22761d26b1b,
                P_1c001f3047230cb97452,
            ),
            xml_aliases=(),
        ),
        "dtd.chemicalproperty.chemical_property_is_active": PropertyMetadata(
            owners=("chemical_property",),
            name="chemical_property_is_active",
            xml_name="ChemicalPropertyIsActive",
            storage="attribute",
            cdx_id=2994,
            cdx_constant="kCDXProp_ChemicalPropertyIsActive",
            datatype="boolean",
            codec="bool",
            required=False,
            default=False,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_83b2b7b707c4453850bd,
                P_df02b4a7a137dd774ddd,
            ),
            xml_aliases=(),
        ),
        "dtd.chemicalproperty.chemical_property_type": PropertyMetadata(
            owners=("chemical_property",),
            name="chemical_property_type",
            xml_name="ChemicalPropertyType",
            storage="attribute",
            cdx_id=2992,
            cdx_constant="kCDXProp_ChemicalPropertyType",
            datatype="integer",
            codec="integer",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_107670a853dfa0a4834b,
                P_783a310b77b6d03cd350,
            ),
            xml_aliases=(),
        ),
        "dtd.chemicalproperty.chemically_significant": PropertyMetadata(
            owners=("chemical_property",),
            name="chemically_significant",
            xml_name="ChemicallySignificant",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="boolean",
            codec="bool",
            required=False,
            default=False,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_ccc819cdca1c3043ddff,),
            xml_aliases=(),
        ),
        "dtd.chemicalproperty.external_bonds": PropertyMetadata(
            owners=("chemical_property",),
            name="external_bonds",
            xml_name="ExternalBonds",
            storage="attribute",
            cdx_id=None,
            cdx_constant=None,
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(P_623eec0f24b4fd627440,),
            xml_aliases=(),
        ),
    }
)
