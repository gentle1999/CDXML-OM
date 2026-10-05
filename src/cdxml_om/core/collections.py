"""Live XML-backed child collection views."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from typing import Generic, TypeVar, overload

from cdxml_om.core.fields import ElementCollection

T = TypeVar("T")


class XMLBackedCollection(ElementCollection[T], Generic[T]):
    """A live view whose members are resolved from the retained DOM on access."""

    __slots__ = ("_load", "_create", "_remove")

    def __init__(
        self,
        load: Callable[[], tuple[T, ...]],
        create: Callable[[Mapping[str, object]], T],
        remove: Callable[[T], None],
    ) -> None:
        self._load = load
        self._create = create
        self._remove = remove

    def __iter__(self) -> Iterator[T]:
        return iter(self._load())

    def __len__(self) -> int:
        return len(self._load())

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        items = self._load()
        if isinstance(index, slice):
            return list(items[index])
        return items[index]

    def all(self) -> list[T]:
        return list(self._load())

    def create(self, **values: object) -> T:
        return self._create(values)

    def remove(self, value: T) -> None:
        self._remove(value)


__all__ = ["XMLBackedCollection"]
