"""Structured errors raised by document parsing and typed access."""

from __future__ import annotations


class CDXMLError(Exception):
    """Base class for CDXML-OM errors."""


class ParseError(CDXMLError):
    """The input is malformed XML or is not a CDXML document."""


class CodecError(CDXMLError):
    """A known XML value cannot be decoded using its schema codec."""

    def __init__(
        self,
        message: str,
        *,
        property_id: str | None = None,
        raw_value: str | None = None,
        xml_tag: str | None = None,
    ) -> None:
        super().__init__(message)
        self.property_id = property_id
        self.raw_value = raw_value
        self.xml_tag = xml_tag


class ReferenceResolutionError(CDXMLError):
    """A typed object-ID reference is missing, invalid, or ambiguous."""


class MutationError(CDXMLError):
    """A typed edit or child-object operation cannot be applied safely."""

    def __init__(self, message: str, *, property_id: str | None = None) -> None:
        super().__init__(message)
        self.property_id = property_id


class IDAllocationError(MutationError):
    """No unused positive uint32 object ID remains in the document."""


__all__ = [
    "CDXMLError",
    "CodecError",
    "IDAllocationError",
    "MutationError",
    "ParseError",
    "ReferenceResolutionError",
]
