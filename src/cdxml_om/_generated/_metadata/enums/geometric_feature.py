# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the GeometricFeature enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_0c9350bd2314935329b8
from ..provenance.sdk_page_geometry import P_22bc9bccdda33c3eeecd
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="GeometricFeature",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNKNOWN",
            xml_value="Unknown",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="POINT_FROM_POINT_POINT_DISTANCE",
            xml_value="PointFromPointPointDistance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="POINT_FROM_POINT_POINT_PERCENTAGE",
            xml_value="PointFromPointPointPercentage",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="POINT_FROM_POINT_NORMAL_DISTANCE",
            xml_value="PointFromPointNormalDistance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="LINE_FROM_POINTS",
            xml_value="LineFromPoints",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="PLANE_FROM_POINTS",
            xml_value="PlaneFromPoints",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="PLANE_FROM_POINT_LINE",
            xml_value="PlaneFromPointLine",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="CENTROID_FROM_POINTS",
            xml_value="CentroidFromPoints",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NORMAL_FROM_POINT_PLANE",
            xml_value="NormalFromPointPlane",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_0c9350bd2314935329b8,
        P_22bc9bccdda33c3eeecd,
    ),
)
