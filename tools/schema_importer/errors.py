"""Structured diagnostics for offline source importing."""

from __future__ import annotations


class ImporterError(Exception):
    """An expected input, parsing, or output-safety failure."""

    def __init__(self, code: str, message: str, location: str) -> None:
        self.code = code
        self.message = message
        self.location = location
        super().__init__(f"{code} at {location}: {message}")

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "location": self.location}
