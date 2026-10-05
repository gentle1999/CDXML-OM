# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: sg_component."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_1ae12c2e8e2113117c7c,
    P_24fdf1c75c445a2fa685,
    P_5512c082a3c2529475eb,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.sgcomponent.component_is_header": PropertyMetadata(
            owners=("sg_component",),
            name="component_is_header",
            xml_name="ComponentIsHeader",
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
            provenance=(P_1ae12c2e8e2113117c7c,),
            xml_aliases=(),
        ),
        "dtd.sgcomponent.component_is_reactant": PropertyMetadata(
            owners=("sg_component",),
            name="component_is_reactant",
            xml_name="ComponentIsReactant",
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
            provenance=(P_5512c082a3c2529475eb,),
            xml_aliases=(),
        ),
        "dtd.sgcomponent.component_reference_id": PropertyMetadata(
            owners=("sg_component",),
            name="component_reference_id",
            xml_name="ComponentReferenceID",
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
            provenance=(P_24fdf1c75c445a2fa685,),
            xml_aliases=(),
        ),
    }
)
