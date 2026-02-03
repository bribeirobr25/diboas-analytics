"""
Gate 3 Trigger Validator - Validates intelligence trigger outputs.

Implements validation rules from VALIDATION_GATES_CTO_HANDOFF_v2.md Section 5.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from src.triggers.base import (
    IntelligenceTriggerResult,
    IntelligenceTriggerPriority,
    IntelligenceTriggerAction,
)
from src.validators.gate3.gate3_validation_rules import (
    VALID_STRATEGY_IDS,
    VALID_PRIORITY_ACTIONS,
    get_valid_actions_for_priority,
)

logger = logging.getLogger(__name__)


@dataclass
class Gate3ValidationIssue:
    """Validation issue for trigger output."""
    code: str
    severity: str  # "error", "warning"
    message: str
    trigger_id: str
    field: Optional[str] = None
    value: Any = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "trigger_id": self.trigger_id,
            "field": self.field,
            "value": self.value,
        }


@dataclass
class Gate3ValidationResult:
    """Result of validating trigger outputs."""
    passed: bool
    issues: List[Gate3ValidationIssue] = field(default_factory=list)
    triggers_validated: int = 0
    triggers_fired: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def errors(self) -> List[Gate3ValidationIssue]:
        """Get error-level issues."""
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> List[Gate3ValidationIssue]:
        """Get warning-level issues."""
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def error_count(self) -> int:
        """Count of errors."""
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return len(self.warnings)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "passed": self.passed,
            "triggers_validated": self.triggers_validated,
            "triggers_fired": self.triggers_fired,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "timestamp": self.timestamp.isoformat(),
            "issues": [i.to_dict() for i in self.issues],
        }


class Gate3TriggerValidator:
    """
    Validates trigger outputs for correctness.

    Checks:
    1. Strategy IDs are valid (1-10)
    2. Priority-action consistency
    3. Required fields present
    4. Threshold vs actual value logic
    5. No duplicate trigger IDs in batch
    """

    def validate(
        self,
        results: List[IntelligenceTriggerResult]
    ) -> Gate3ValidationResult:
        """
        Validate a batch of trigger results.

        Args:
            results: List of trigger results to validate

        Returns:
            Gate3ValidationResult with pass/fail and issues
        """
        issues = []
        seen_trigger_ids: Set[str] = set()
        triggers_fired = 0

        for result in results:
            # Check for duplicates
            if result.trigger_id in seen_trigger_ids:
                issues.append(Gate3ValidationIssue(
                    code="G3-DUP-001",
                    severity="error",
                    message="Duplicate trigger ID in batch",
                    trigger_id=result.trigger_id
                ))
            seen_trigger_ids.add(result.trigger_id)

            # Count fired triggers
            if result.fired:
                triggers_fired += 1

            # Validate individual result
            issues.extend(self._validate_result(result))

        has_errors = any(i.severity == "error" for i in issues)

        return Gate3ValidationResult(
            passed=not has_errors,
            issues=issues,
            triggers_validated=len(results),
            triggers_fired=triggers_fired
        )

    def validate_single(
        self,
        result: IntelligenceTriggerResult
    ) -> Gate3ValidationResult:
        """
        Validate a single trigger result.

        Args:
            result: Single trigger result to validate

        Returns:
            Gate3ValidationResult with pass/fail and issues
        """
        return self.validate([result])

    def _validate_result(
        self,
        result: IntelligenceTriggerResult
    ) -> List[Gate3ValidationIssue]:
        """Validate a single trigger result."""
        issues = []

        # Check strategy IDs
        issues.extend(self._validate_strategy_ids(result))

        # Check priority-action consistency
        issues.extend(self._validate_priority_action(result))

        # Check required fields
        issues.extend(self._validate_required_fields(result))

        # Check threshold logic (only for fired triggers)
        if result.fired:
            issues.extend(self._validate_threshold_logic(result))

        return issues

    def _validate_strategy_ids(
        self,
        result: IntelligenceTriggerResult
    ) -> List[Gate3ValidationIssue]:
        """Check that all strategy IDs are valid (1-10)."""
        issues = []

        invalid_strategies = set(result.affected_strategies) - VALID_STRATEGY_IDS
        if invalid_strategies:
            issues.append(Gate3ValidationIssue(
                code="G3-STR-001",
                severity="error",
                message=f"Invalid strategy IDs: {sorted(invalid_strategies)}",
                trigger_id=result.trigger_id,
                field="affected_strategies",
                value=list(result.affected_strategies)
            ))

        # Warning if no strategies affected
        if not result.affected_strategies:
            issues.append(Gate3ValidationIssue(
                code="G3-STR-002",
                severity="warning",
                message="No affected strategies specified",
                trigger_id=result.trigger_id,
                field="affected_strategies",
                value=[]
            ))

        return issues

    def _validate_priority_action(
        self,
        result: IntelligenceTriggerResult
    ) -> List[Gate3ValidationIssue]:
        """Check priority-action consistency."""
        issues = []

        valid_actions = get_valid_actions_for_priority(result.priority)

        if valid_actions and result.action not in valid_actions:
            issues.append(Gate3ValidationIssue(
                code="G3-ACT-001",
                severity="warning",
                message=f"Action '{result.action.value}' unusual for priority '{result.priority.value}'",
                trigger_id=result.trigger_id,
                field="action",
                value=result.action.value
            ))

        return issues

    def _validate_required_fields(
        self,
        result: IntelligenceTriggerResult
    ) -> List[Gate3ValidationIssue]:
        """Check that required fields are present."""
        issues = []

        # Check condition_description
        if not result.condition_description:
            issues.append(Gate3ValidationIssue(
                code="G3-FLD-001",
                severity="warning",
                message="Missing condition_description",
                trigger_id=result.trigger_id,
                field="condition_description"
            ))

        # Check threshold for fired triggers
        if result.fired and result.threshold is None:
            issues.append(Gate3ValidationIssue(
                code="G3-FLD-002",
                severity="warning",
                message="Fired trigger missing threshold value",
                trigger_id=result.trigger_id,
                field="threshold"
            ))

        # Check actual_value for fired triggers
        if result.fired and result.actual_value is None:
            issues.append(Gate3ValidationIssue(
                code="G3-FLD-003",
                severity="warning",
                message="Fired trigger missing actual_value",
                trigger_id=result.trigger_id,
                field="actual_value"
            ))

        return issues

    def _validate_threshold_logic(
        self,
        result: IntelligenceTriggerResult
    ) -> List[Gate3ValidationIssue]:
        """Validate that actual value correctly triggered based on threshold."""
        issues = []

        # Skip if missing values
        if result.threshold is None or result.actual_value is None:
            return issues

        # Only validate numeric thresholds
        try:
            threshold = float(result.threshold)
            actual = float(result.actual_value)
        except (TypeError, ValueError):
            return issues  # Non-numeric thresholds are OK

        # Check if description implies direction
        desc_lower = (result.condition_description or "").lower()

        if ">" in desc_lower or "above" in desc_lower or "exceeds" in desc_lower:
            if actual <= threshold:
                issues.append(Gate3ValidationIssue(
                    code="G3-THR-001",
                    severity="error",
                    message=f"Fired but actual ({actual}) not > threshold ({threshold})",
                    trigger_id=result.trigger_id,
                    field="threshold_logic",
                    value={"actual": actual, "threshold": threshold}
                ))

        elif "<" in desc_lower or "below" in desc_lower or "drop" in desc_lower:
            if actual >= threshold:
                issues.append(Gate3ValidationIssue(
                    code="G3-THR-002",
                    severity="error",
                    message=f"Fired but actual ({actual}) not < threshold ({threshold})",
                    trigger_id=result.trigger_id,
                    field="threshold_logic",
                    value={"actual": actual, "threshold": threshold}
                ))

        return issues


class Gate3ValidationReport:
    """Generate validation report from results."""

    def __init__(self, result: Gate3ValidationResult):
        self.result = result

    @property
    def status(self) -> str:
        """Get overall status."""
        if self.result.error_count > 0:
            return "FAILED"
        elif self.result.warning_count > 0:
            return "PASS_WITH_WARNINGS"
        else:
            return "PASSED"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "triggers_validated": self.result.triggers_validated,
            "triggers_fired": self.result.triggers_fired,
            "error_count": self.result.error_count,
            "warning_count": self.result.warning_count,
            "timestamp": self.result.timestamp.isoformat(),
            "issues": [i.to_dict() for i in self.result.issues],
        }
