# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Generated datatype metadata."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from .provenance.revvity_dtd import (
    P_837cbeedc852e8fdfcaa,
    P_3625871724cf81deb77e,
)
from .provenance.sdk_color import P_dbc992db016b528359ac
from .provenance.sdk_coordinates import (
    P_3be2a23955e4b28c1835,
    P_a08febc14435733f6824,
    P_f38a196ca2cb2a06c507,
)
from .provenance.sdk_curve_points import P_5634d699407c2aba4ac7
from .provenance.sdk_curve_points_3d import P_12ec435fae68da8c006b
from .provenance.sdk_element_list import P_ae2b5c35b1e5f5531a87
from .provenance.sdk_generic_list import P_b70bf323475139b1592b
from .provenance.sdk_int16_list_with_counts import P_311f530b4a740ae96dbf
from .provenance.sdk_intro import (
    P_893ec2d6a291d7965562,
    P_b7bbfd49819468120091,
    P_c569026a405718c6a207,
)
from .provenance.sdk_object_id import P_b3a5647325392ef5b676
from .provenance.sdk_object_tag_type import P_12ae08cd93d47ebe2fcb
from .provenance.sdk_object_tag_value import P_299c60a333d6ca0e5455
from .types import DatatypeMetadata

DATATYPE_METADATA: Final[Mapping[str, DatatypeMetadata]] = MappingProxyType(
    {
        "object_id": DatatypeMetadata(
            python_type="int",
            kind="integer",
            codec="object_id",
            minimum=0,
            maximum=4294967295,
            status="known",
            provenance=(P_b3a5647325392ef5b676,),
        ),
        "integer": DatatypeMetadata(
            python_type="int",
            kind="integer",
            codec="integer",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_b7bbfd49819468120091,),
        ),
        "local_id": DatatypeMetadata(
            python_type="int",
            kind="integer",
            codec="integer",
            minimum=0,
            maximum=65535,
            status="known",
            provenance=(
                P_893ec2d6a291d7965562,
                P_837cbeedc852e8fdfcaa,
            ),
        ),
        "string": DatatypeMetadata(
            python_type="str",
            kind="string",
            codec="string",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_b7bbfd49819468120091,),
        ),
        "float": DatatypeMetadata(
            python_type="float",
            kind="float",
            codec="float",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_c569026a405718c6a207,),
        ),
        "unit_interval": DatatypeMetadata(
            python_type="float",
            kind="float",
            codec="float",
            minimum=0,
            maximum=1,
            status="known",
            provenance=(P_dbc992db016b528359ac,),
        ),
        "boolean": DatatypeMetadata(
            python_type="bool",
            kind="boolean",
            codec="bool",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_3625871724cf81deb77e,),
        ),
        "point_2d": DatatypeMetadata(
            python_type="Point2D",
            kind="geometry",
            codec="point_2d",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_3be2a23955e4b28c1835,),
        ),
        "point_3d": DatatypeMetadata(
            python_type="Point3D",
            kind="geometry",
            codec="point_3d",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_f38a196ca2cb2a06c507,),
        ),
        "bounding_box": DatatypeMetadata(
            python_type="BoundingBox",
            kind="geometry",
            codec="bounding_box",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_a08febc14435733f6824,),
        ),
        "curve_points_2d": DatatypeMetadata(
            python_type="tuple[Point2D, ...]",
            kind="geometry",
            codec="curve_points2d",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_5634d699407c2aba4ac7,),
        ),
        "curve_points_3d": DatatypeMetadata(
            python_type="tuple[Point3D, ...]",
            kind="geometry",
            codec="curve_points3d",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_12ec435fae68da8c006b,),
        ),
        "integer_list": DatatypeMetadata(
            python_type="tuple[int, ...]",
            kind="sequence",
            codec="uint16_list",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_311f530b4a740ae96dbf,),
        ),
        "element_list": DatatypeMetadata(
            python_type="ElementList",
            kind="structured",
            codec="element_list",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_ae2b5c35b1e5f5531a87,),
        ),
        "generic_list": DatatypeMetadata(
            python_type="GenericList",
            kind="structured",
            codec="generic_list",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(P_b70bf323475139b1592b,),
        ),
        "object_tag_value": DatatypeMetadata(
            python_type="int | float | str",
            kind="structured",
            codec="object_tag_value",
            minimum=None,
            maximum=None,
            status="known",
            provenance=(
                P_12ae08cd93d47ebe2fcb,
                P_299c60a333d6ca0e5455,
            ),
        ),
    }
)
