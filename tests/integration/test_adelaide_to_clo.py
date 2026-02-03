"""Integration tests for Adelaide to CLO validation pipeline."""

import pytest
import tempfile

from src.validators.clo.clo_gate4_validator import CLOGate4Validator
from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOJurisdiction,
    CLOValidationStatus,
)
from src.crisis.crisis_level_classifier import CrisisLevelClassifier, CrisisLevel
from src.crisis.crisis_router import CrisisRouter
from src.crisis.crisis_approval_queue import CrisisFileBasedApprovalQueue
from src.adelaide.adelaide_edition_tracker import AdelaideEditionTracker


class TestAdelaideToCLOPipeline:
    """Integration tests for Adelaide content to CLO validation pipeline."""

    @pytest.fixture
    def clo_validator(self):
        """Create CLO Gate 4 validator."""
        return CLOGate4Validator({})

    @pytest.fixture
    def classifier(self):
        """Create crisis classifier."""
        return CrisisLevelClassifier()

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def router(self, temp_queue_dir):
        """Create crisis router with temp queue."""
        queue = CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)
        return CrisisRouter(approval_queue=queue)

    def test_should_auto_approve_clean_content(self, clo_validator):
        """Clean content is auto-approved."""
        content = """
        Weekly Market Update

        This week saw moderate growth across major markets.

        DISCLAIMER: This is not investment advice. Past performance
        does not guarantee future results.
        """

        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=0
        )

        result = clo_validator.validate(input_data)

        assert result.status == CLOValidationStatus.PASS
        assert result.routing_decision == "auto_deliver"
        assert result.requires_human is False

    def test_should_block_content_with_prohibited_terms(self, clo_validator):
        """Content with prohibited terms is blocked."""
        content = """
        Amazing Investment Opportunity!

        This is a guaranteed profit strategy with risk-free returns.
        You cannot lose money with this approach!
        """

        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=0
        )

        result = clo_validator.validate(input_data)

        assert result.status == CLOValidationStatus.FAIL
        assert result.routing_decision == "block"
        assert len(result.issues) > 0

    def test_should_route_crisis_content_to_queue(self, clo_validator, classifier, router):
        """Crisis content is routed to approval queue."""
        content = """
        URGENT: Security Incident

        We are monitoring a potential security concern with one of our protocols.
        This is not investment advice.
        """

        # Classify crisis level
        classification = classifier.classify(content)
        assert classification.level >= CrisisLevel.LEVEL_3_WARNING

        # Route based on classification
        decision = router.route(content, classification)

        assert decision.action == "queue"
        assert decision.request_id is not None
        assert len(decision.approvers) > 0

    def test_should_require_spot_check_for_early_editions(self, clo_validator):
        """Early Adelaide editions require spot-check."""
        content = """
        Adelaide Newsletter #5

        This week's market analysis.
        This is not investment advice. Past performance does not guarantee future results.
        """

        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=0,
            adelaide_edition_number=5
        )

        result = clo_validator.validate(input_data)

        assert result.status == CLOValidationStatus.HUMAN_REQUIRED
        assert result.human_queue == "adelaide_spot_check"

    def test_should_not_require_spot_check_after_20_editions(self, clo_validator):
        """Later editions don't require spot-check."""
        content = """
        Adelaide Newsletter #25

        This week's market analysis.
        This is not investment advice. Past performance does not guarantee future results.
        """

        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=0,
            adelaide_edition_number=25
        )

        result = clo_validator.validate(input_data)

        # Should proceed to normal validation
        assert result.status in [CLOValidationStatus.PASS, CLOValidationStatus.WARN]


class TestEditionTrackerIntegration:
    """Integration tests for Adelaide edition tracking."""

    @pytest.fixture
    def tracker(self):
        """Create edition tracker with temp file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            return AdelaideEditionTracker(state_file=f.name)

    def test_should_track_editions_and_determine_spot_check(self, tracker):
        """Edition tracker integrates with spot-check determination."""
        # First 20 editions require spot-check
        for i in range(1, 21):
            assert tracker.requires_spot_check() is True
            tracker.record_edition("daily")

        # Edition 21 should not require spot-check
        assert tracker.requires_spot_check() is False

    def test_should_use_edition_number_in_clo_validation(self, tracker):
        """Edition number flows through to CLO validation."""
        clo_validator = CLOGate4Validator({})

        # Get next edition number
        edition_num = tracker.get_next_edition_number()

        content = "This is not investment advice. Past performance does not guarantee future results."
        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            adelaide_edition_number=edition_num
        )

        result = clo_validator.validate(input_data)

        # Edition 1 should require spot-check
        if edition_num <= 20:
            assert result.status == CLOValidationStatus.HUMAN_REQUIRED


class TestFullPipelineIntegration:
    """Full pipeline integration tests."""

    def test_full_pipeline_normal_content(self):
        """Test full pipeline with normal content."""
        # 1. Edition tracker
        tracker = AdelaideEditionTracker(
            state_file=tempfile.mktemp(suffix='.json')
        )
        for _ in range(25):  # Move past spot-check
            tracker.record_edition("daily")

        # 2. Create content
        content = """
        Weekly Market Update - Adelaide Newsletter

        Market conditions remain stable this week.

        This is not investment advice. Past performance does not
        guarantee future results.
        """

        # 3. Classify crisis level
        classifier = CrisisLevelClassifier()
        classification = classifier.classify(content)
        assert classification.level == CrisisLevel.LEVEL_0_NORMAL

        # 4. CLO validation
        clo_validator = CLOGate4Validator({})
        input_data = CLOValidationInput(
            content=content,
            jurisdiction=CLOJurisdiction.US,
            crisis_level=classification.level,
            adelaide_edition_number=tracker.get_next_edition_number()
        )
        result = clo_validator.validate(input_data)

        # Should auto-approve
        assert result.status == CLOValidationStatus.PASS
        assert result.routing_decision == "auto_deliver"
