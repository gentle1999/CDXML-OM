"""Structured validation of known CDXML schema constraints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from cdxml_om.core.models import CDXMLElement


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One schema-backed document validation finding."""

    code: str
    message: str
    element: CDXMLElement | None
    property_id: str | None = None
    severity: Literal["error", "warning"] = "error"


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Immutable snapshot of validation findings."""

    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")


__all__ = ["ValidationIssue", "ValidationReport"]
