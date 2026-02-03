"""
Tests for CVM 3-part disclaimer validation for Brazil.

The CVM (Comissão de Valores Mobiliários) requires 3 specific parts:
1. BR-CVM-001: Not protected by investor schemes
2. BR-CVM-002: Risk of capital loss
3. BR-CVM-003: Consult qualified professional
"""

import pytest
from src.validators.clo.clo_disclaimer_validator import CLODisclaimerValidator
from src.validators.clo.clo_validation_types import CLOValidationInput, CLOJurisdiction


class TestCVMStructureValidation:
    """Tests for CVM 3-part structure validation."""

    @pytest.fixture
    def validator(self):
        return CLODisclaimerValidator({})

    def test_should_pass_with_all_three_parts(self, validator):
        """Content with all 3 CVM required parts should pass."""
        content = """
        **Avisos Importantes de Conformidade**

        **AVISO 1:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos.

        **AVISO 2:** Você pode perder todo o capital investido.

        **AVISO 3:** Consulte um profissional habilitado pela CVM para orientação.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, f"Unexpected CVM issues: {[i.code for i in cvm_issues]}"

    def test_should_fail_missing_protection_warning(self, validator):
        """Missing investor protection warning should fail."""
        content = """
        Você pode perder todo o capital investido.
        Consulte um profissional habilitado pela CVM.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert any('BR-CVM-001' in i.code for i in cvm_issues), "Should fail BR-CVM-001"

    def test_should_fail_missing_loss_warning(self, validator):
        """Missing capital loss warning should fail."""
        content = """
        Criptoativos NÃO são protegidos por esquemas de garantia.
        Consulte um profissional habilitado pela CVM.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert any('BR-CVM-002' in i.code for i in cvm_issues), "Should fail BR-CVM-002"

    def test_should_fail_missing_professional_advice(self, validator):
        """Missing professional advice recommendation should fail."""
        content = """
        Criptoativos NÃO são protegidos por esquemas de garantia.
        Você pode perder todo o capital investido.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert any('BR-CVM-003' in i.code for i in cvm_issues), "Should fail BR-CVM-003"

    def test_should_fail_with_all_missing(self, validator):
        """Content with all 3 parts missing should have 3 CVM issues."""
        content = """
        Este é apenas conteúdo educacional.
        Informações gerais sobre o mercado.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 3, f"Should have 3 CVM issues, got {len(cvm_issues)}"

    def test_should_handle_markdown_formatting(self, validator):
        """Markdown formatting should not affect validation."""
        content = """
        **AVISO:** Criptoativos **NÃO** são protegidos.
        Você pode **perder** todo o capital.
        Consulte um **profissional habilitado**.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, f"Markdown formatting broke validation: {[i.code for i in cvm_issues]}"

    def test_should_handle_accent_variations(self, validator):
        """Accent variations should be handled by normalization."""
        # Using ASCII approximations that might appear in some systems
        content = """
        Criptoativos NAO sao protegidos por esquemas.
        Voce pode perder todo o capital.
        Consulte um assessor financeiro.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, f"ASCII variations broke validation: {[i.code for i in cvm_issues]}"

    def test_should_handle_case_variations(self, validator):
        """Case variations should not affect validation."""
        content = """
        CRIPTOATIVOS NÃO SÃO PROTEGIDOS POR ESQUEMAS.
        você pode PERDER todo o CAPITAL.
        consulte um PROFISSIONAL HABILITADO.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, f"Case variations broke validation: {[i.code for i in cvm_issues]}"

    def test_should_not_apply_cvm_to_us_jurisdiction(self, validator):
        """CVM validation should only apply to BR jurisdiction."""
        content = """
        This content doesn't have CVM disclaimers.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.US)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, "CVM validation should not apply to US jurisdiction"

    def test_should_not_apply_cvm_to_eu_jurisdiction(self, validator):
        """CVM validation should only apply to BR jurisdiction."""
        content = """
        This content doesn't have CVM disclaimers.
        """
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.EU)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, "CVM validation should not apply to EU jurisdiction"


class TestCVMLocalizationIntegration:
    """Test that the localization file contains valid CVM disclaimers."""

    @pytest.fixture
    def validator(self):
        return CLODisclaimerValidator({})

    def test_pt_br_regional_disclaimer_passes_cvm(self, validator):
        """The PT-BR regional disclaimer should pass CVM validation."""
        from src.adelaide.localization import REGIONAL_DISCLAIMERS

        content = REGIONAL_DISCLAIMERS.get('pt-br', '')
        input_data = CLOValidationInput(content=content, jurisdiction=CLOJurisdiction.BR)
        issues = validator.validate(input_data)

        cvm_issues = [i for i in issues if 'BR-CVM' in i.code]
        assert len(cvm_issues) == 0, f"PT-BR disclaimer fails CVM: {[(i.code, i.message) for i in cvm_issues]}"


class TestNormalization:
    """Tests for content normalization."""

    @pytest.fixture
    def validator(self):
        return CLODisclaimerValidator({})

    def test_normalize_removes_markdown_asterisks(self, validator):
        """Normalization should remove markdown asterisks."""
        result = validator._normalize_for_validation("**bold** text")
        assert "**" not in result
        assert "bold" in result

    def test_normalize_removes_markdown_headers(self, validator):
        """Normalization should remove markdown headers."""
        result = validator._normalize_for_validation("## Header\nText")
        assert "##" not in result

    def test_normalize_converts_to_lowercase(self, validator):
        """Normalization should lowercase content."""
        result = validator._normalize_for_validation("UPPERCASE TEXT")
        assert result == "uppercase text"

    def test_normalize_strips_accents(self, validator):
        """Normalization should strip accent marks."""
        result = validator._normalize_for_validation("são não ação proteção")
        assert "ã" not in result
        assert "ç" not in result
        # After stripping, should contain base characters
        assert "sao" in result
        assert "nao" in result
