"""Tests for CLO prohibited terms validator."""

import pytest
from src.validators.clo.clo_prohibited_terms_validator import CLOProhibitedTermsValidator
from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOJurisdiction,
    CLOValidationSeverity,
)


class TestProhibitedTermsValidator:
    """Tests for CLOProhibitedTermsValidator."""

    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        return CLOProhibitedTermsValidator({})

    def test_should_block_when_guaranteed_detected(self, validator):
        """Detects 'guaranteed' as prohibited."""
        input_data = CLOValidationInput(
            content="This investment offers guaranteed returns!",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any("guaranteed" in i.message.lower() for i in issues)
        assert all(i.severity == CLOValidationSeverity.ERROR for i in issues)

    def test_should_block_when_risk_free_detected(self, validator):
        """Detects 'risk-free' as prohibited."""
        input_data = CLOValidationInput(
            content="This is a risk-free investment opportunity.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any("risk-free" in i.actual_value.lower() for i in issues)

    def test_should_block_when_cannot_lose_detected(self, validator):
        """Detects 'cannot lose' as prohibited."""
        input_data = CLOValidationInput(
            content="You cannot lose with this strategy.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0

    def test_should_pass_when_clean_content(self, validator):
        """Passes when no prohibited terms found."""
        input_data = CLOValidationInput(
            content="This strategy carries inherent risks. Past performance does not predict future results.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0

    def test_should_detect_us_specific_terms(self, validator):
        """Detects US-specific prohibited terms."""
        input_data = CLOValidationInput(
            content="You should invest in this strategy now!",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any(i.jurisdiction == "US" for i in issues)

    def test_should_detect_brazil_specific_terms(self, validator):
        """Detects Brazil-specific prohibited terms."""
        input_data = CLOValidationInput(
            content="Lucro garantido com este investimento!",
            jurisdiction=CLOJurisdiction.BR
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any(i.jurisdiction == "BR" for i in issues)

    def test_should_be_case_insensitive(self, validator):
        """Detection is case insensitive."""
        input_data = CLOValidationInput(
            content="GUARANTEED RETURNS",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0

    def test_should_detect_multiple_violations(self, validator):
        """Detects multiple prohibited terms."""
        input_data = CLOValidationInput(
            content="This is a guaranteed, risk-free, 100% safe investment!",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) >= 3

    def test_should_include_remediation(self, validator):
        """Issues include remediation guidance."""
        input_data = CLOValidationInput(
            content="This is guaranteed profit.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert all(i.remediation for i in issues)
