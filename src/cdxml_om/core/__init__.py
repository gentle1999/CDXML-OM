"""Handwritten runtime primitives shared by generated model declarations."""

from cdxml_om.core.errors import (
    CDXMLError,
    CodecError,
    IDAllocationError,
    MutationError,
    ParseError,
    ReferenceResolutionError,
)
from cdxml_om.core.fields import ChildCollection, ElementCollection, Field, RefField
from cdxml_om.core.geometry import BoundingBox, Point2D, Point3D
from cdxml_om.core.models import CDXMLElement, UnknownElement

__all__ = [
    "BoundingBox",
    "CDXMLElement",
    "CDXMLError",
    "ChildCollection",
    "CodecError",
    "ElementCollection",
    "Field",
    "IDAllocationError",
    "MutationError",
    "ParseError",
    "Point2D",
    "Point3D",
    "RefField",
    "ReferenceResolutionError",
    "UnknownElement",
]
