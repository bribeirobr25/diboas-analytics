"""
Gate 3 Trigger Validators - Validates intelligence trigger outputs.

Validates trigger results for:
- Valid strategy IDs (1-10)
- Priority-action consistency
- Required fields present
- Threshold vs actual value logic
- No duplicate trigger IDs
"""

from src.validators.gate3.gate3_trigger_validator import (
    Gate3ValidationIssue,
    Gate3ValidationResult,
    Gate3TriggerValidator,
    Gate3ValidationReport,
)
from src.validators.gate3.gate3_validation_rules import (
    VALID_STRATEGY_IDS,
    VALID_PRIORITY_ACTIONS,
    get_valid_actions_for_priority,
)

__all__ = [
    # Validator
    "Gate3ValidationIssue",
    "Gate3ValidationResult",
    "Gate3TriggerValidator",
    "Gate3ValidationReport",
    # Rules
    "VALID_STRATEGY_IDS",
    "VALID_PRIORITY_ACTIONS",
    "get_valid_actions_for_priority",
]
