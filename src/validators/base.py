"""
Base validation types and utilities.

DRY Principle (Principle 4):
---------------------------
This module provides shared validation types to avoid duplicating
ValidationIssue, ValidationResult, and ValidationSeverity classes
across Gate 1, Gate 2, Gate 3, and CLO validators.

Existing validators can continue to use their own classes for
backward compatibility, but new validators should use these base classes.

Usage:
    from src.validators.base import (
        ValidationSeverity,
        ValidationStatus,
        BaseValidationIssue,
        BaseValidationResult,
    )

    @dataclass
    class MyValidationIssue(BaseValidationIssue):
        # Add any domain-specific fields
        my_custom_field: str = ""
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from src.utils.serialization import Serializable, make_json_safe


class ValidationSeverity(Enum):
    """
    Standard severity levels for validation issues.

    ERROR: Validation failed - must be fixed
    WARNING: Potential issue - should be reviewed
    INFO: Informational - no action required
    """
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationStatus(Enum):
    """
    Standard validation status values.

    PASS: All validations passed
    WARN: Passed with warnings
    FAIL: One or more errors found
    HUMAN_REQUIRED: Needs human review (CLO-specific)
    """
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    HUMAN_REQUIRED = "human_required"


@dataclass
class BaseValidationIssue(Serializable):
    """
    Base class for validation issues.

    Contains common fields used across all validation gates.
    Gate-specific validators can extend this with additional fields.
    """
    code: str
    severity: ValidationSeverity
    message: str
    field: Optional[str] = None
    actual_value: Any = None
    expected_value: Any = None
    remediation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "code": self.code,
            "severity": self.severity.value if isinstance(self.severity, Enum) else self.severity,
            "message": self.message,
            "field": self.field,
            "actual_value": make_json_safe(self.actual_value),
            "expected_value": make_json_safe(self.expected_value),
            "remediation": self.remediation,
        }

    @property
    def is_error(self) -> bool:
        """Check if this is an error-level issue."""
        return self.severity == ValidationSeverity.ERROR

    @property
    def is_warning(self) -> bool:
        """Check if this is a warning-level issue."""
        return self.severity == ValidationSeverity.WARNING


@dataclass
class BaseValidationResult(Serializable):
    """
    Base class for validation results.

    Contains common structure used across all validation gates.
    """
    status: ValidationStatus
    issues: List[BaseValidationIssue] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        """Check if validation passed (no errors)."""
        return self.status != ValidationStatus.FAIL

    @property
    def errors(self) -> List[BaseValidationIssue]:
        """Get all error-level issues."""
        return [i for i in self.issues if i.is_error]

    @property
    def warnings(self) -> List[BaseValidationIssue]:
        """Get all warning-level issues."""
        return [i for i in self.issues if i.is_warning]

    @property
    def error_count(self) -> int:
        """Count of errors."""
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return len(self.warnings)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "passed": self.passed,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [i.to_dict() for i in self.issues],
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": make_json_safe(self.metadata),
        }


@runtime_checkable
class Validator(Protocol):
    """
    Protocol for validator implementations.

    Any class implementing this protocol can be used as a validator.
    """

    def validate(self, data: Any) -> BaseValidationResult:
        """
        Validate data and return result.

        Args:
            data: Data to validate

        Returns:
            Validation result with status and issues
        """
        ...


def determine_status(issues: List[BaseValidationIssue]) -> ValidationStatus:
    """
    Determine overall validation status from list of issues.

    Args:
        issues: List of validation issues

    Returns:
        FAIL if any errors, WARN if only warnings, PASS otherwise
    """
    has_errors = any(
        i.severity == ValidationSeverity.ERROR
        for i in issues
    )
    has_warnings = any(
        i.severity == ValidationSeverity.WARNING
        for i in issues
    )

    if has_errors:
        return ValidationStatus.FAIL
    elif has_warnings:
        return ValidationStatus.WARN
    else:
        return ValidationStatus.PASS


def format_validation_report(result: BaseValidationResult) -> str:
    """
    Format a validation result as a human-readable report.

    Args:
        result: Validation result to format

    Returns:
        Formatted string report
    """
    lines = [
        f"Validation Status: {result.status.value.upper()}",
        f"Timestamp: {result.timestamp.isoformat()}",
        f"Errors: {result.error_count}, Warnings: {result.warning_count}",
        "",
    ]

    if result.errors:
        lines.append("ERRORS:")
        for i, issue in enumerate(result.errors, 1):
            lines.append(f"  {i}. [{issue.code}] {issue.message}")
            if issue.remediation:
                lines.append(f"     Remediation: {issue.remediation}")
        lines.append("")

    if result.warnings:
        lines.append("WARNINGS:")
        for i, issue in enumerate(result.warnings, 1):
            lines.append(f"  {i}. [{issue.code}] {issue.message}")
        lines.append("")

    return "\n".join(lines)
