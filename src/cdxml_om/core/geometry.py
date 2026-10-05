"""Immutable coordinate values used by CDXML datatype codecs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Point3D:
    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class BoundingBox:
    left: float
    top: float
    right: float
    bottom: float


__all__ = ["BoundingBox", "Point2D", "Point3D"]
