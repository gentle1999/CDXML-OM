# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: geometry."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_6084a2921c686c634b1b,
    P_de89acc9d5ea200801b2,
    P_e15e424f40650239c2ee,
)
from ..provenance.sdk_page_geometry import (
    P_065b9cf7ea18d199733d,
    P_22bc9bccdda33c3eeecd,
    P_97a39ace4d07b8a558d5,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.geometry.geometric_feature": PropertyMetadata(
            owners=("geometry",),
            name="geometric_feature",
            xml_name="GeometricFeature",
            storage="attribute",
            cdx_id=2944,
            cdx_constant="kCDXProp_GeometricFeature",
            datatype="string",
            codec="string",
            required=False,
            default="Unknown",
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum="dtd.geometric_feature.4250a286",
            status="known",
            provenance=(
                P_e15e424f40650239c2ee,
                P_22bc9bccdda33c3eeecd,
            ),
            xml_aliases=(),
        ),
        "dtd.geometry.relation_value": PropertyMetadata(
            owners=("geometry",),
            name="relation_value",
            xml_name="RelationValue",
            storage="attribute",
            cdx_id=2945,
            cdx_constant="kCDXProp_RelationValue",
            datatype="float",
            codec="float",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_de89acc9d5ea200801b2,
                P_97a39ace4d07b8a558d5,
            ),
            xml_aliases=(),
        ),
        "sdk.geometry.point_is_directed": PropertyMetadata(
            owners=("geometry",),
            name="point_is_directed",
            xml_name="PointIsDirected",
            storage="attribute",
            cdx_id=2952,
            cdx_constant="kCDXProp_PointIsDirected",
            datatype="boolean",
            codec="bool",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_065b9cf7ea18d199733d,
                P_6084a2921c686c634b1b,
            ),
            xml_aliases=(),
        ),
    }
)
