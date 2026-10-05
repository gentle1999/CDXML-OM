"""Immutable typed values for irregular, structured CDXML lexical fields."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ElementList:
    """A CDX element-list payload represented by atomic-number values."""

    elements: tuple[int, ...]
    negated: bool = False


@dataclass(frozen=True, slots=True)
class GenericList:
    """A generic string list, optionally representing a NOT-list."""

    values: tuple[str, ...]
    negated: bool = False


__all__ = ["ElementList", "GenericList"]
