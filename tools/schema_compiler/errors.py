"""Structured schema compiler diagnostics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SchemaIssue:
    code: str
    message: str
    location: str = "schema"

    def __str__(self) -> str:
        return f"{self.code} at {self.location}: {self.message}"


class SchemaError(Exception):
    """Raised when canonical schema input cannot be loaded or validated."""

    def __init__(self, issues: tuple[SchemaIssue, ...]) -> None:
        self.issues = issues
        super().__init__("\n".join(map(str, issues)))
