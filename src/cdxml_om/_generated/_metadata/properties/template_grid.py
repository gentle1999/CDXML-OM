# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: template_grid."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_03dab709f6a237545e8f,
    P_56ca9e445873f0207b1c,
    P_bf5bc4a520866ab96d62,
    P_c78b52656804f429e88b,
)
from ..provenance.sdk_page_templategrid import (
    P_4bd28e0d3deb38873451,
    P_4057d17482a5ac57007b,
    P_881579fde7e8fdfa0e9b,
    P_eaab2545c8d0bcd187e5,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.templategrid.extent": PropertyMetadata(
            owners=("template_grid",),
            name="extent",
            xml_name="extent",
            storage="attribute",
            cdx_id=514,
            cdx_constant="kCDXProp_2DExtent",
            datatype="point_2d",
            codec="point_2d",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_c78b52656804f429e88b,
                P_eaab2545c8d0bcd187e5,
            ),
            xml_aliases=(),
        ),
        "dtd.templategrid.num_columns": PropertyMetadata(
            owners=("template_grid",),
            name="num_columns",
            xml_name="NumColumns",
            storage="attribute",
            cdx_id=4098,
            cdx_constant="kCDXProp_Template_NumColumns",
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
                P_56ca9e445873f0207b1c,
                P_4bd28e0d3deb38873451,
            ),
            xml_aliases=(),
        ),
        "dtd.templategrid.num_rows": PropertyMetadata(
            owners=("template_grid",),
            name="num_rows",
            xml_name="NumRows",
            storage="attribute",
            cdx_id=4097,
            cdx_constant="kCDXProp_Template_NumRows",
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
                P_bf5bc4a520866ab96d62,
                P_881579fde7e8fdfa0e9b,
            ),
            xml_aliases=(),
        ),
        "dtd.templategrid.pane_height": PropertyMetadata(
            owners=("template_grid",),
            name="pane_height",
            xml_name="PaneHeight",
            storage="attribute",
            cdx_id=4096,
            cdx_constant="kCDXProp_Template_PaneHeight",
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
                P_03dab709f6a237545e8f,
                P_4057d17482a5ac57007b,
            ),
            xml_aliases=(),
        ),
    }
)
