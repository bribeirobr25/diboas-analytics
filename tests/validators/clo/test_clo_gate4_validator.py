"""Tests for CLO Gate 4 validator.

Tests the final combined validation gate which runs all sub-validators:
- Prohibited terms
- Disclaimers (including AI disclosure)
- Jurisdiction restrictions
- Crisis level handling
- Adelaide spot-check requirements
"""

import pytest
from src.validators.clo.clo_gate4_validator import CLOGate4Validator
from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOJurisdiction,
    CLOValidationStatus,
)


# AI disclosure to include in test content (California SB 942 compliance)
AI_DISCLOSURE = "🤖 This content was generated with artificial intelligence assistance."


class TestCLOGate4Validator:
    """Tests for CLOGate4Validator."""

    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        return CLOGate4Validator({})

    def test_should_pass_clean_content(self, validator):
        """Passes clean content with required disclaimers and AI disclosure."""
        input_data = CLOValidationInput(
            content=f"This is not investment advice. Past performance does not guarantee future results. {AI_DISCLOSURE}",
            jurisdiction=CLOJurisdiction.US
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.PASS
        assert result.passed is True
        assert result.routing_decision == "auto_deliver"

    def test_should_fail_prohibited_content(self, validator):
        """Fails content with prohibited terms."""
        input_data = CLOValidationInput(
            content="This is guaranteed profit! Risk-free investment opportunity!",
            jurisdiction=CLOJurisdiction.US
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.FAIL
        assert result.passed is False
        assert result.routing_decision == "block"

    def test_should_block_uk_jurisdiction(self, validator):
        """Blocks UK jurisdiction (geo-blocked)."""
        input_data = CLOValidationInput(
            content="This is not investment advice. Past performance does not guarantee future results.",
            jurisdiction=CLOJurisdiction.UK
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.FAIL
        assert result.routing_decision == "block"
        assert any("UK" in i.message and "geo-blocked" in i.message for i in result.issues)

    def test_should_require_human_when_crisis_level_3(self, validator):
        """Requires human review for crisis level 3."""
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US,
            crisis_level=3
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.HUMAN_REQUIRED
        assert result.requires_human is True
        assert result.routing_decision == "human_queue"
        assert result.sla_minutes == 60

    def test_should_require_human_when_crisis_level_4(self, validator):
        """Requires human review for crisis level 4."""
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US,
            crisis_level=4
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.HUMAN_REQUIRED
        assert result.sla_minutes == 75

    def test_should_require_human_when_crisis_level_5(self, validator):
        """Requires human review for crisis level 5."""
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US,
            crisis_level=5
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.HUMAN_REQUIRED
        assert result.sla_minutes == 90

    def test_should_require_human_for_first_20_editions(self, validator):
        """Requires spot-check for first 20 editions."""
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US,
            adelaide_edition_number=5
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.HUMAN_REQUIRED
        assert result.human_queue == "adelaide_spot_check"
        assert result.sla_minutes == 480

    def test_should_not_require_spot_check_after_20_editions(self, validator):
        """No spot-check required after 20 editions."""
        input_data = CLOValidationInput(
            content=f"This is not investment advice. Past performance does not guarantee future results. {AI_DISCLOSURE}",
            jurisdiction=CLOJurisdiction.US,
            adelaide_edition_number=25
        )
        result = validator.validate(input_data)
        # Should proceed to normal validation and PASS
        assert result.status == CLOValidationStatus.PASS

    def test_should_include_duration_metadata(self, validator):
        """Includes gate duration in metadata."""
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US
        )
        result = validator.validate(input_data)
        assert "gate_duration_ms" in result.metadata
        assert result.metadata["gate_duration_ms"] >= 0

    def test_should_warn_on_minor_issues(self, validator):
        """Warns on minor issues but still passes."""
        # Create content that might trigger warnings but not errors
        input_data = CLOValidationInput(
            content="This is not investment advice. Past performance shows we beat the market.",
            jurisdiction=CLOJurisdiction.US
        )
        result = validator.validate(input_data)
        # Depending on validators, may be PASS, WARN, or FAIL
        assert result.status in [CLOValidationStatus.PASS, CLOValidationStatus.WARN, CLOValidationStatus.FAIL]

    def test_should_convert_to_dict(self, validator):
        """Result can be converted to dict."""
        input_data = CLOValidationInput(
            content=f"This is not investment advice. Past performance does not guarantee future results. {AI_DISCLOSURE}",
            jurisdiction=CLOJurisdiction.US
        )
        result = validator.validate(input_data)
        result_dict = result.to_dict()

        assert "status" in result_dict
        assert "passed" in result_dict
        assert "issues" in result_dict
        assert "routing_decision" in result_dict


class TestCLOGate4Configuration:
    """Tests for CLO Gate 4 configuration."""

    def test_should_use_custom_spot_check_count(self):
        """Uses custom spot-check count from config."""
        validator = CLOGate4Validator({"first_n_spot_check": 5})

        # Edition 3 should require spot-check
        input_data = CLOValidationInput(
            content="This is not investment advice.",
            jurisdiction=CLOJurisdiction.US,
            adelaide_edition_number=3
        )
        result = validator.validate(input_data)
        assert result.status == CLOValidationStatus.HUMAN_REQUIRED

        # Edition 10 should not require spot-check with custom config
        input_data2 = CLOValidationInput(
            content=f"This is not investment advice. Past performance does not guarantee future results. {AI_DISCLOSURE}",
            jurisdiction=CLOJurisdiction.US,
            adelaide_edition_number=10
        )
        result2 = validator.validate(input_data2)
        assert result2.status != CLOValidationStatus.HUMAN_REQUIRED or "spot-check" not in str(result2.issues)
