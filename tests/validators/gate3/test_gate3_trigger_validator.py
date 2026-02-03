"""Tests for Gate 3 Trigger Validator."""

import pytest
from datetime import datetime

from src.triggers.base import (
    IntelligenceTriggerResult,
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
    IntelligenceTriggerAction,
)
from src.validators.gate3 import (
    Gate3TriggerValidator,
    Gate3ValidationResult,
    Gate3ValidationReport,
    Gate3ValidationIssue,
    VALID_STRATEGY_IDS,
    VALID_PRIORITY_ACTIONS,
    get_valid_actions_for_priority,
)


def make_trigger_result(
    trigger_id: str = "TEST-001",
    trigger_name: str = "Test Trigger",
    fired: bool = True,
    priority: IntelligenceTriggerPriority = IntelligenceTriggerPriority.P2_MEDIUM,
    category: IntelligenceTriggerCategory = IntelligenceTriggerCategory.PROTOCOL_HEALTH,
    action: IntelligenceTriggerAction = IntelligenceTriggerAction.PROTOCOL_ALERT,
    affected_strategies: list = None,
    condition_description: str = "Test condition",
    threshold: float = 5.0,
    actual_value: float = 10.0,
) -> IntelligenceTriggerResult:
    """Helper to create trigger results for testing."""
    if affected_strategies is None:
        affected_strategies = [1, 3, 5]
    return IntelligenceTriggerResult(
        trigger_id=trigger_id,
        trigger_name=trigger_name,
        fired=fired,
        priority=priority,
        category=category,
        action=action,
        affected_strategies=affected_strategies,
        condition_description=condition_description,
        threshold=threshold,
        actual_value=actual_value,
    )


class TestGate3ValidationRules:
    """Tests for validation rules."""

    def test_should_have_10_valid_strategy_ids(self):
        """Valid strategy IDs are 1-10."""
        assert VALID_STRATEGY_IDS == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    def test_should_have_priority_action_mapping(self):
        """Priority-action mapping is defined."""
        assert len(VALID_PRIORITY_ACTIONS) == 4
        assert IntelligenceTriggerPriority.P0_CRITICAL in VALID_PRIORITY_ACTIONS

    def test_should_get_valid_actions_for_p0(self):
        """P0 should only allow crisis template."""
        actions = get_valid_actions_for_priority(IntelligenceTriggerPriority.P0_CRITICAL)
        assert IntelligenceTriggerAction.CRISIS_TEMPLATE in actions
        assert len(actions) == 1

    def test_should_get_valid_actions_for_p2(self):
        """P2 should allow multiple actions."""
        actions = get_valid_actions_for_priority(IntelligenceTriggerPriority.P2_MEDIUM)
        assert IntelligenceTriggerAction.PROTOCOL_ALERT in actions
        assert IntelligenceTriggerAction.SMART_MONEY_INSIGHT in actions

    def test_should_get_valid_actions_for_p3(self):
        """P3 should allow internal only."""
        actions = get_valid_actions_for_priority(IntelligenceTriggerPriority.P3_INFO)
        assert IntelligenceTriggerAction.INTERNAL_ONLY in actions


class TestGate3TriggerValidator:
    """Tests for main trigger validator."""

    @pytest.fixture
    def validator(self):
        """Create validator."""
        return Gate3TriggerValidator()

    def test_should_pass_valid_trigger(self, validator):
        """Valid trigger passes validation."""
        result = make_trigger_result()
        validation = validator.validate([result])

        assert validation.passed is True
        assert validation.error_count == 0

    def test_should_fail_invalid_strategy_id(self, validator):
        """Invalid strategy ID fails validation."""
        result = make_trigger_result(affected_strategies=[1, 3, 15])  # 15 is invalid
        validation = validator.validate([result])

        assert validation.passed is False
        assert any(i.code == "G3-STR-001" for i in validation.issues)

    def test_should_warn_empty_strategies(self, validator):
        """Empty affected_strategies warns."""
        result = make_trigger_result(affected_strategies=[])
        validation = validator.validate([result])

        assert any(i.code == "G3-STR-002" for i in validation.issues)
        assert any(i.severity == "warning" for i in validation.issues)

    def test_should_fail_duplicate_trigger_ids(self, validator):
        """Duplicate trigger IDs fail validation."""
        result1 = make_trigger_result(trigger_id="SAME-ID")
        result2 = make_trigger_result(trigger_id="SAME-ID")
        validation = validator.validate([result1, result2])

        assert validation.passed is False
        assert any(i.code == "G3-DUP-001" for i in validation.issues)

    def test_should_warn_unusual_priority_action(self, validator):
        """Unusual priority-action combination warns."""
        # P0 with INTERNAL_ONLY is unusual
        result = make_trigger_result(
            priority=IntelligenceTriggerPriority.P0_CRITICAL,
            action=IntelligenceTriggerAction.INTERNAL_ONLY
        )
        validation = validator.validate([result])

        assert any(i.code == "G3-ACT-001" for i in validation.issues)

    def test_should_pass_valid_priority_action(self, validator):
        """Valid priority-action combination passes."""
        result = make_trigger_result(
            priority=IntelligenceTriggerPriority.P0_CRITICAL,
            action=IntelligenceTriggerAction.CRISIS_TEMPLATE
        )
        validation = validator.validate([result])

        assert not any(i.code == "G3-ACT-001" for i in validation.issues)

    def test_should_warn_missing_condition_description(self, validator):
        """Missing condition_description warns."""
        result = make_trigger_result(condition_description="")
        validation = validator.validate([result])

        assert any(i.code == "G3-FLD-001" for i in validation.issues)

    def test_should_warn_missing_threshold_for_fired(self, validator):
        """Fired trigger missing threshold warns."""
        result = make_trigger_result(fired=True, threshold=None)
        validation = validator.validate([result])

        assert any(i.code == "G3-FLD-002" for i in validation.issues)

    def test_should_warn_missing_actual_value_for_fired(self, validator):
        """Fired trigger missing actual_value warns."""
        result = make_trigger_result(fired=True, actual_value=None)
        validation = validator.validate([result])

        assert any(i.code == "G3-FLD-003" for i in validation.issues)

    def test_should_not_warn_missing_values_for_not_fired(self, validator):
        """Non-fired trigger doesn't need threshold/actual."""
        result = make_trigger_result(fired=False, threshold=None, actual_value=None)
        validation = validator.validate([result])

        assert not any(i.code == "G3-FLD-002" for i in validation.issues)
        assert not any(i.code == "G3-FLD-003" for i in validation.issues)

    def test_should_fail_threshold_logic_above(self, validator):
        """Fails when 'above' threshold but actual is below."""
        result = make_trigger_result(
            fired=True,
            condition_description="Depeg above 5%",
            threshold=5.0,
            actual_value=3.0  # Below threshold
        )
        validation = validator.validate([result])

        assert validation.passed is False
        assert any(i.code == "G3-THR-001" for i in validation.issues)

    def test_should_pass_threshold_logic_above(self, validator):
        """Passes when 'above' threshold and actual is above."""
        result = make_trigger_result(
            fired=True,
            condition_description="Depeg above 5%",
            threshold=5.0,
            actual_value=10.0  # Above threshold
        )
        validation = validator.validate([result])

        assert not any(i.code == "G3-THR-001" for i in validation.issues)

    def test_should_fail_threshold_logic_below(self, validator):
        """Fails when 'below' threshold but actual is above."""
        result = make_trigger_result(
            fired=True,
            condition_description="Price drop below -10%",
            threshold=-10.0,
            actual_value=-5.0  # Above threshold (less negative)
        )
        validation = validator.validate([result])

        assert validation.passed is False
        assert any(i.code == "G3-THR-002" for i in validation.issues)

    def test_should_pass_threshold_logic_below(self, validator):
        """Passes when 'below' threshold and actual is below."""
        result = make_trigger_result(
            fired=True,
            condition_description="Price drop below -10%",
            threshold=-10.0,
            actual_value=-15.0  # Below threshold
        )
        validation = validator.validate([result])

        assert not any(i.code == "G3-THR-002" for i in validation.issues)

    def test_should_count_triggers_correctly(self, validator):
        """Counts validated and fired triggers."""
        results = [
            make_trigger_result(trigger_id="T1", fired=True),
            make_trigger_result(trigger_id="T2", fired=False),
            make_trigger_result(trigger_id="T3", fired=True),
        ]
        validation = validator.validate(results)

        assert validation.triggers_validated == 3
        assert validation.triggers_fired == 2

    def test_should_validate_single_result(self, validator):
        """Can validate a single result."""
        result = make_trigger_result()
        validation = validator.validate_single(result)

        assert validation.triggers_validated == 1


class TestGate3ValidationResult:
    """Tests for validation result."""

    def test_should_report_errors_and_warnings(self):
        """Result separates errors and warnings."""
        result = Gate3ValidationResult(
            passed=False,
            issues=[
                Gate3ValidationIssue("E1", "error", "Error 1", "T1"),
                Gate3ValidationIssue("W1", "warning", "Warning 1", "T1"),
                Gate3ValidationIssue("E2", "error", "Error 2", "T2"),
            ],
            triggers_validated=2
        )

        assert result.error_count == 2
        assert result.warning_count == 1
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

    def test_should_convert_to_dict(self):
        """Result converts to dictionary."""
        result = Gate3ValidationResult(
            passed=True,
            triggers_validated=5,
            triggers_fired=2
        )
        data = result.to_dict()

        assert data["passed"] is True
        assert data["triggers_validated"] == 5
        assert data["triggers_fired"] == 2
        assert "timestamp" in data


class TestGate3ValidationReport:
    """Tests for validation report."""

    def test_should_report_passed_status(self):
        """Report shows passed status."""
        result = Gate3ValidationResult(passed=True, triggers_validated=5)
        report = Gate3ValidationReport(result)

        assert report.status == "PASSED"

    def test_should_report_failed_status(self):
        """Report shows failed status when errors."""
        result = Gate3ValidationResult(
            passed=False,
            issues=[Gate3ValidationIssue("E1", "error", "Error", "T1")],
            triggers_validated=5
        )
        report = Gate3ValidationReport(result)

        assert report.status == "FAILED"

    def test_should_report_warnings_status(self):
        """Report shows warning status when only warnings."""
        result = Gate3ValidationResult(
            passed=True,
            issues=[Gate3ValidationIssue("W1", "warning", "Warning", "T1")],
            triggers_validated=5
        )
        report = Gate3ValidationReport(result)

        assert report.status == "PASS_WITH_WARNINGS"

    def test_should_convert_to_dict(self):
        """Report converts to dictionary."""
        result = Gate3ValidationResult(passed=True, triggers_validated=5)
        report = Gate3ValidationReport(result)
        data = report.to_dict()

        assert data["status"] == "PASSED"
        assert data["triggers_validated"] == 5
