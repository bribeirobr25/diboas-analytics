"""
CLO Validation types and base classes.

Defines the data structures and interfaces used by CLO Gate 4 validators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class CLOValidationStatus(Enum):
    """Validation result status."""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    HUMAN_REQUIRED = "human_required"


class CLOValidationSeverity(Enum):
    """Severity of validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class CLOJurisdiction(Enum):
    """
    Supported jurisdictions for compliance.

    Each jurisdiction has different regulatory requirements.
    UK is geo-blocked per FSMA Section 21.
    """
    EU = "EU"
    US = "US"
    BR = "BR"
    UK = "UK"  # Geo-blocked
    OTHER = "OTHER"


@dataclass
class CLOValidationIssue:
    """
    A single validation issue found during content review.

    Contains all context needed for remediation.
    """
    code: str
    severity: CLOValidationSeverity
    message: str
    field: Optional[str] = None
    actual_value: Any = None
    remediation: str = ""
    jurisdiction: Optional[str] = None
    regulatory_reference: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "field": self.field,
            "actual_value": self.actual_value,
            "remediation": self.remediation,
            "jurisdiction": self.jurisdiction,
            "regulatory_reference": self.regulatory_reference,
        }


@dataclass
class CLOValidationResult:
    """
    Result from CLO Gate 4 validation.

    Contains status, issues, and routing decision.
    """
    status: CLOValidationStatus
    issues: List[CLOValidationIssue] = field(default_factory=list)
    routing_decision: str = "auto_deliver"
    human_queue: Optional[str] = None
    sla_minutes: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        """Check if validation passed (PASS or WARN are acceptable)."""
        return self.status in [CLOValidationStatus.PASS, CLOValidationStatus.WARN]

    @property
    def requires_human(self) -> bool:
        """Check if human review is required."""
        return self.status == CLOValidationStatus.HUMAN_REQUIRED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status.value,
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues],
            "routing_decision": self.routing_decision,
            "human_queue": self.human_queue,
            "sla_minutes": self.sla_minutes,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class CLOValidationInput:
    """
    Input for CLO Gate 4 validation.

    Contains content and context needed for compliance checks.
    """
    content: str
    jurisdiction: CLOJurisdiction
    crisis_level: int = 0
    adelaide_edition_number: Optional[int] = None
    strategy_ids_mentioned: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CLOSubValidator(ABC):
    """
    Abstract base for CLO sub-validators.

    Each sub-validator checks a specific aspect of compliance.
    The main CLOGate4Validator orchestrates all sub-validators.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize with optional configuration."""
        self.config = config or {}

    @property
    @abstractmethod
    def validator_name(self) -> str:
        """Return validator name for logging and reporting."""
        pass

    @abstractmethod
    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Validate content and return any issues found.

        Args:
            input: Validation input with content and context

        Returns:
            List of validation issues (empty if none)
        """
        pass
