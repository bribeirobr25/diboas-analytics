"""
Core validation classes.

Contains ValidationError and ValidationResult for structured error handling.
"""

from typing import List, Any
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Structured validation error with recovery suggestion."""
    field: str
    value: Any
    message: str
    suggestion: str
    severity: str = 'error'  # 'error', 'warning'

    def __str__(self):
        return f"{self.field}: {self.message}"

    def format_full(self) -> str:
        """Format error with suggestion."""
        return f"[{self.severity.upper()}] {self.field}: {self.message}\n  Suggestion: {self.suggestion}"


class ValidationResult:
    """Result of validation containing errors and warnings."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0

    def add_error(
        self,
        field: str,
        value: Any,
        message: str,
        suggestion: str
    ):
        """Add a validation error."""
        self.errors.append(ValidationError(
            field=field,
            value=value,
            message=message,
            suggestion=suggestion,
            severity='error'
        ))

    def add_warning(
        self,
        field: str,
        value: Any,
        message: str,
        suggestion: str
    ):
        """Add a validation warning."""
        self.warnings.append(ValidationError(
            field=field,
            value=value,
            message=message,
            suggestion=suggestion,
            severity='warning'
        ))

    def raise_if_invalid(self):
        """Raise ValueError if validation failed."""
        if not self.is_valid:
            error_messages = [e.format_full() for e in self.errors]
            raise ValueError(
                f"Validation failed with {len(self.errors)} error(s):\n" +
                "\n".join(error_messages)
            )

    def format_report(self) -> str:
        """Format all errors and warnings as a report."""
        lines = []

        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for e in self.errors:
                lines.append(f"  - {e.format_full()}")

        if self.warnings:
            lines.append(f"Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"  - {w.format_full()}")

        return "\n".join(lines) if lines else "Validation passed"
