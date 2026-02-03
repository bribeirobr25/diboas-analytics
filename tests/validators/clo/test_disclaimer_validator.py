"""Tests for CLO disclaimer validator."""

import pytest
from src.validators.clo.clo_disclaimer_validator import CLODisclaimerValidator
from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOJurisdiction,
    CLOValidationSeverity,
)


class TestDisclaimerValidator:
    """Tests for CLODisclaimerValidator."""

    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        return CLODisclaimerValidator({})

    def test_should_fail_when_us_disclaimer_missing(self, validator):
        """Fails when US disclaimers are missing."""
        input_data = CLOValidationInput(
            content="This is a newsletter about investing.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any(i.jurisdiction == "US" for i in issues)
        assert all(i.severity == CLOValidationSeverity.ERROR for i in issues)

    def test_should_pass_when_us_disclaimers_present(self, validator):
        """Passes when US disclaimers are present."""
        input_data = CLOValidationInput(
            content="This is not investment advice. Past performance does not guarantee future results.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0

    def test_should_accept_alternative_disclaimer_phrases(self, validator):
        """Accepts alternative disclaimer phrases."""
        input_data = CLOValidationInput(
            content="This content is for informational purposes only. Historical performance may not repeat.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        # Should accept alternatives
        assert len([i for i in issues if "not investment advice" in i.message]) == 0

    def test_should_fail_when_eu_disclaimer_missing(self, validator):
        """Fails when EU disclaimers are missing."""
        input_data = CLOValidationInput(
            content="This is a newsletter about investing.",
            jurisdiction=CLOJurisdiction.EU
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any(i.jurisdiction == "EU" for i in issues)

    def test_should_pass_when_eu_disclaimers_present(self, validator):
        """Passes when EU disclaimers are present."""
        input_data = CLOValidationInput(
            content="This is not investment advice. Your capital is at risk.",
            jurisdiction=CLOJurisdiction.EU
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0

    def test_should_fail_when_brazil_disclaimer_missing(self, validator):
        """Fails when Brazil disclaimers are missing."""
        input_data = CLOValidationInput(
            content="Este é um boletim informativo sobre investimentos.",
            jurisdiction=CLOJurisdiction.BR
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0

    def test_should_pass_when_brazil_disclaimer_present(self, validator):
        """Passes when Brazil disclaimers are present with CVM 3-part structure."""
        # Brazil requires CVM 3-part structure:
        # 1. Investor protection warning
        # 2. Loss warning
        # 3. Professional advice
        input_data = CLOValidationInput(
            content="""
            Investimentos envolvem riscos de perda.
            Criptoativos NÃO são protegidos por esquemas de garantia.
            Você pode perder todo o capital investido.
            Consulte um profissional habilitado pela CVM.
            """,
            jurisdiction=CLOJurisdiction.BR
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0, f"Unexpected issues: {[(i.code, i.message) for i in issues]}"

    def test_should_include_regulatory_reference(self, validator):
        """Issues include regulatory reference."""
        input_data = CLOValidationInput(
            content="This is a newsletter.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) > 0
        assert any(i.regulatory_reference for i in issues)

    def test_should_be_case_insensitive(self, validator):
        """Detection is case insensitive."""
        input_data = CLOValidationInput(
            content="THIS IS NOT INVESTMENT ADVICE. PAST PERFORMANCE DOES NOT PREDICT FUTURE RESULTS.",
            jurisdiction=CLOJurisdiction.US
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0

    def test_should_have_no_requirements_for_other_jurisdiction(self, validator):
        """No specific requirements for OTHER jurisdiction."""
        input_data = CLOValidationInput(
            content="This is a newsletter.",
            jurisdiction=CLOJurisdiction.OTHER
        )
        issues = validator.validate(input_data)
        assert len(issues) == 0
