"""Small typed descriptor interfaces consumed by generated model classes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, Self, TypeVar, overload

from cdxml_om.core.models import CDXMLElement

T = TypeVar("T")


class Field(Generic[T]):
    """Typed declaration for one XML attribute."""

    def __init__(self, property_id: str) -> None:
        self.property_id = property_id

    @overload
    def __get__(self, instance: None, owner: type[CDXMLElement] | None = None) -> Self: ...

    @overload
    def __get__(self, instance: CDXMLElement, owner: type[CDXMLElement] | None = None) -> T: ...

    def __get__(
        self, instance: CDXMLElement | None, owner: type[CDXMLElement] | None = None
    ) -> T | Field[T]:
        if instance is None:
            return self
        return instance.__cdxml_read_field__(self)

    def __set__(self, instance: CDXMLElement, value: T) -> None:
        instance.__cdxml_write_field__(self, value)


class RefField(Field[T], Generic[T]):
    """Typed declaration for an XML object-ID reference."""

    def __init__(
        self,
        property_id: str,
    ) -> None:
        super().__init__(property_id)


class RefListField(Field[tuple[T, ...]], Generic[T]):
    """Typed declaration for an XML whitespace-separated list of object IDs."""

    def __init__(self, property_id: str) -> None:
        super().__init__(property_id)


class ElementCollection(Generic[T]):
    """Typed live child collection with explicit create and remove operations."""

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError("XML-backed collections are not initialized")

    def __len__(self) -> int:
        raise NotImplementedError("XML-backed collections are not initialized")

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        raise NotImplementedError("XML-backed collections are not initialized")

    def all(self) -> list[T]:
        raise NotImplementedError("XML-backed collections are not initialized")

    def create(self, **values: object) -> T:
        raise NotImplementedError("XML-backed collections are not initialized")

    def remove(self, value: T) -> None:
        raise NotImplementedError("XML-backed collections are not initialized")


class ChildCollection(Generic[T]):
    """Typed declaration for a child-object collection."""

    def __init__(self, object_type: str, collection_name: str) -> None:
        self.object_type = object_type
        self.collection_name = collection_name

    @overload
    def __get__(self, instance: None, owner: type[CDXMLElement] | None = None) -> Self: ...

    @overload
    def __get__(
        self, instance: CDXMLElement, owner: type[CDXMLElement] | None = None
    ) -> ElementCollection[T]: ...

    def __get__(
        self, instance: CDXMLElement | None, owner: type[CDXMLElement] | None = None
    ) -> ChildCollection[T] | ElementCollection[T]:
        if instance is None:
            return self
        return instance.__cdxml_read_collection__(self)


__all__ = ["ChildCollection", "ElementCollection", "Field", "RefField", "RefListField"]
