"""Monotonic document object-ID allocation."""

from __future__ import annotations

from collections.abc import Iterable

from cdxml_om._generated.schema_metadata import DATATYPE_METADATA
from cdxml_om.core.errors import IDAllocationError


class IdManager:
    """Allocates unused positive IDs and never reuses a reserved ID."""

    __slots__ = ("_used", "_minimum", "_maximum", "_start", "_next")

    def __init__(
        self,
        reserved_ids: Iterable[int] = (),
        *,
        datatype_id: str = "object_id",
    ) -> None:
        datatype = DATATYPE_METADATA[datatype_id]
        minimum = datatype.minimum
        maximum = datatype.maximum
        if not isinstance(minimum, int):
            minimum = 0
        if not isinstance(maximum, int):
            raise RuntimeError(f"{datatype_id} datatype must have an integer maximum")
        self._minimum = minimum
        self._maximum = maximum
        self._start = max(1, minimum)
        self._used = {
            value
            for value in reserved_ids
            if not isinstance(value, bool) and minimum <= value <= maximum
        }
        self._next = self._start

    def reserve(self, object_id: int) -> None:
        if self._minimum <= object_id <= self._maximum:
            self._used.add(object_id)

    def allocate(self, additionally_reserved: Iterable[int] = ()) -> int:
        candidate = self.next_available(additionally_reserved)
        self._used.add(candidate)
        self._next = candidate + 1 if candidate < self._maximum else self._start
        return candidate

    def next_available(self, additionally_reserved: Iterable[int] = ()) -> int:
        reserved_now = set(additionally_reserved)
        candidate = self._next
        capacity = self._maximum - self._start + 1
        for _ in range(min(capacity, len(self._used | reserved_now) + 1)):
            if candidate not in self._used and candidate not in reserved_now:
                return candidate
            candidate = candidate + 1 if candidate < self._maximum else self._start
        raise IDAllocationError("no unused positive uint32 object ID remains")

    def is_reserved(self, object_id: int) -> bool:
        return object_id in self._used


__all__ = ["IdManager"]
