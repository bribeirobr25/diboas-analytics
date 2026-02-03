"""
End-to-end integration tests for the complete validation pipeline.

Tests the full flow: Data → Gate 1 → Triggers → Gate 3 → Adelaide → Gate 4 → Output
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import date, timedelta

from src.validators.gate1 import (
    Gate1SchemaValidator,
    Gate1ValidationReport,
)
from src.validators.gate3 import (
    Gate3TriggerValidator,
    Gate3ValidationReport,
)
from src.validators.clo import (
    CLOGate4Validator,
    CLOValidationInput,
    CLOJurisdiction,
    CLOValidationStatus,
)
from src.validators.gate_aggregator import (
    GateValidationAggregator,
    AggregatedValidationReport,
)
from src.triggers import (
    IntelligenceTriggerEvaluator,
    IntelligenceTriggerPriority,
)
from src.crisis import (
    CrisisLevelClassifier,
    CrisisLevel,
    CrisisRouter,
    CrisisFileBasedApprovalQueue,
)
from src.adelaide.adelaide_edition_tracker import AdelaideEditionTracker


class TestFullPipelineE2E:
    """End-to-end tests for the complete validation pipeline."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def sample_csv_data(self, temp_dir):
        """Create sample CSV files for Gate 1 validation."""
        # Create treasury_yields.csv with valid data
        csv_content = "date,us_2y,us_10y,us_30y\n"
        start_date = date(2024, 1, 1)
        for i in range(105):
            d = start_date + timedelta(days=i)
            csv_content += f"{d.isoformat()},4.5,4.2,4.8\n"

        csv_path = Path(temp_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        return temp_dir

    def test_full_pipeline_normal_flow(self, temp_dir):
        """Test full pipeline with normal content flow."""
        # Step 1: Create edition tracker (past spot-check period)
        tracker = AdelaideEditionTracker(
            state_file=Path(temp_dir) / "editions.json"
        )
        for _ in range(25):  # Move past spot-check
            tracker.record_edition("daily")

        assert tracker.requires_spot_check() is False

        # Step 2: Create compliant content
        content = """
        Weekly Market Update - Adelaide Newsletter #26

        Market conditions remain stable this week. Bitcoin is trading
        above $45,000 with steady price action.

        This is not investment advice. Past performance does not
        guarantee future results. Your capital is at risk.
        """

        # Step 3: Classify crisis level
        classifier = CrisisLevelClassifier()
        classification = classifier.classify(content)
        # Should be low crisis level (0-1)
        assert classification.level <= CrisisLevel.LEVEL_1_WATCH

        # Step 4: CLO Gate 4 validation
        clo_validator = CLOGate4Validator({})
        clo_input = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=classification.level,
            adelaide_edition_number=tracker.get_next_edition_number()
        )
        clo_result = clo_validator.validate(clo_input)

        # Should pass or warn (no errors)
        assert clo_result.status in [
            CLOValidationStatus.PASS,
            CLOValidationStatus.WARN
        ]
        assert clo_result.routing_decision == "auto_deliver"

    def test_full_pipeline_crisis_flow(self, temp_dir):
        """Test full pipeline with crisis content flow."""
        # Step 1: Crisis content
        content = """
        URGENT: Security Incident Alert

        We have confirmed a security breach affecting protocol funds.
        This is a critical situation requiring immediate attention.

        This is not investment advice.
        """

        # Step 2: Classify crisis level
        classifier = CrisisLevelClassifier()
        classification = classifier.classify(content)

        # Should be high crisis level
        assert classification.level >= CrisisLevel.LEVEL_4_ALERT
        assert classification.requires_human_approval is True

        # Step 3: Route to crisis queue
        queue = CrisisFileBasedApprovalQueue(queue_dir=temp_dir)
        router = CrisisRouter(approval_queue=queue)
        decision = router.route(content, classification)

        # Should be queued for approval
        assert decision.action == "queue"
        assert decision.request_id is not None
        assert len(decision.approvers) > 0

        # Step 4: Verify in queue
        request = queue.get(decision.request_id)
        assert request is not None
        assert request.status == "pending"

    def test_full_pipeline_trigger_to_clo(self, temp_dir):
        """Test trigger evaluation through CLO validation."""
        # Step 1: Create evaluator with fresh cooldowns
        evaluator = IntelligenceTriggerEvaluator(config={
            "default_cooldown_minutes": 0,
            "consolidate_alerts": False,
        })
        evaluator.cooldown_manager.state_file = Path(temp_dir) / "cooldowns.json"
        evaluator.cooldown_manager.cooldowns = {}

        # Step 2: Simulate market data with issues
        data = {
            "protocol_health": {
                "sky": {"usds_price": 0.92}  # 8% depeg
            },
            "market_prices": {
                "btc": {"change_24h_pct": -15}  # 15% drop
            }
        }

        # Step 3: Evaluate triggers
        results = evaluator.evaluate_all(data)
        fired = [r for r in results if r.fired]

        # Should have fired triggers
        assert len(fired) > 0

        # Step 4: Validate trigger outputs with Gate 3
        gate3_validator = Gate3TriggerValidator()
        gate3_result = gate3_validator.validate(results)

        # Gate 3 should pass
        assert gate3_result.passed is True

        # Step 5: Generate alert content
        alert_content = f"""
        Protocol Alert: Sky USDS Depeg

        Current peg: 0.92 (8% depeg detected)
        Affected strategies: {fired[0].affected_strategies if fired else []}

        This is not investment advice. Your capital is at risk.
        """

        # Step 6: CLO validation
        clo_validator = CLOGate4Validator({})
        clo_input = CLOValidationInput(
            content=alert_content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=3  # Warning level
        )
        clo_result = clo_validator.validate(clo_input)

        # Should pass with warnings
        assert clo_result.status in [
            CLOValidationStatus.PASS,
            CLOValidationStatus.WARN,
            CLOValidationStatus.HUMAN_REQUIRED
        ]

    def test_gate_aggregator_full_pipeline(self, sample_csv_data, temp_dir):
        """Test gate aggregator with all validation stages."""
        # Step 1: Gate 1 validation
        gate1_validator = Gate1SchemaValidator(data_dir=sample_csv_data)
        gate1_results = {"treasury_yields.csv": gate1_validator.validate_file("treasury_yields.csv")}

        # Step 2: Create trigger results for Gate 3
        from src.triggers.base import (
            IntelligenceTriggerResult,
            IntelligenceTriggerPriority,
            IntelligenceTriggerCategory,
            IntelligenceTriggerAction,
        )

        trigger_result = IntelligenceTriggerResult(
            trigger_id="TEST-001",
            trigger_name="Test Trigger",
            fired=True,
            priority=IntelligenceTriggerPriority.P2_MEDIUM,
            category=IntelligenceTriggerCategory.PROTOCOL_HEALTH,
            action=IntelligenceTriggerAction.PROTOCOL_ALERT,
            affected_strategies=[1, 3, 5],
            condition_description="Test condition above threshold",
            threshold=5.0,
            actual_value=10.0,
        )

        gate3_validator = Gate3TriggerValidator()
        gate3_result = gate3_validator.validate([trigger_result])

        # Step 3: Gate 4 CLO validation
        clo_validator = CLOGate4Validator({})
        clo_input = CLOValidationInput(
            content="This is not investment advice. Your capital is at risk.",
            jurisdiction=CLOJurisdiction.US,
        )
        gate4_result = clo_validator.validate(clo_input)

        # Step 4: Aggregate results
        aggregator = GateValidationAggregator()
        aggregator.add_gate1_result(gate1_results)
        aggregator.add_gate3_result(gate3_result)
        aggregator.add_gate4_result(gate4_result)

        report = aggregator.get_report()

        # All gates should pass or have warnings only
        assert len(report.gates) == 3
        assert report.gates_passed >= 2  # At least Gate 3 and Gate 4 should pass

    def test_spot_check_required_for_early_editions(self, temp_dir):
        """Test that early editions require spot-check."""
        tracker = AdelaideEditionTracker(
            state_file=Path(temp_dir) / "editions.json"
        )

        # Edition 1 should require spot-check
        assert tracker.requires_spot_check() is True

        # Record some editions
        for i in range(10):
            tracker.record_edition("daily")

        # Edition 11 should still require spot-check
        assert tracker.requires_spot_check() is True

        # After 20 editions
        for i in range(10):
            tracker.record_edition("daily")

        # Edition 21 should not require spot-check
        assert tracker.requires_spot_check() is False


class TestCrisisFlowE2E:
    """End-to-end tests for crisis communication flow."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_crisis_approval_workflow(self, temp_queue_dir):
        """Test complete crisis approval workflow."""
        # Step 1: Submit crisis content
        queue = CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)

        request_id = queue.submit(
            content="Crisis alert content",
            crisis_level=4,
            queue="crisis_alert_review",
            approvers=["clo_board", "ceo"],
            sla_minutes=75
        )

        assert request_id is not None

        # Step 2: Check pending
        pending = queue.get_pending()
        assert len(pending) == 1
        assert pending[0].status == "pending"

        # Step 3: Approve
        success = queue.approve(request_id, approved_by="ceo@company.com")
        assert success is True

        # Step 4: Verify no longer pending
        pending = queue.get_pending()
        assert len(pending) == 0

        # Step 5: Verify approved status
        request = queue.get(request_id)
        assert request.status == "approved"
        assert request.approved_by == "ceo@company.com"

    def test_crisis_rejection_workflow(self, temp_queue_dir):
        """Test crisis rejection workflow."""
        queue = CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)

        request_id = queue.submit(
            content="Crisis alert with issues",
            crisis_level=4,
            queue="crisis_alert_review",
            approvers=["clo_board"],
            sla_minutes=75
        )

        # Reject
        success = queue.reject(
            request_id,
            rejected_by="clo@company.com",
            reason="Content needs revision"
        )
        assert success is True

        # Verify rejected
        request = queue.get(request_id)
        assert request.status == "rejected"
        assert request.rejection_reason == "Content needs revision"


class TestValidationReport:
    """Tests for validation report generation."""

    def test_aggregated_report_to_json(self):
        """Test that aggregated report can be serialized to JSON."""
        from src.validators.gate_aggregator import (
            GateValidationAggregator,
            GateResult,
        )

        aggregator = GateValidationAggregator()

        # Add mock results
        aggregator.report.gates.append(GateResult(
            gate_id="Gate1",
            name="Schema Validation",
            passed=True,
            error_count=0,
            warning_count=2,
            items_validated=100
        ))

        aggregator.report.gates.append(GateResult(
            gate_id="Gate3",
            name="Trigger Validation",
            passed=True,
            error_count=0,
            warning_count=0,
            items_validated=10
        ))

        report = aggregator.get_report()
        report_dict = report.to_dict()

        # Should be JSON serializable
        json_str = json.dumps(report_dict)
        assert len(json_str) > 0

        # Verify structure
        parsed = json.loads(json_str)
        assert parsed["status"] == "PASS_WITH_WARNINGS"
        assert parsed["total_gates"] == 2
        assert parsed["gates_passed"] == 2
