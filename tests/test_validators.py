"""
Tests for validation rules CV-01 through CV-07.
"""

import pytest
from src.validators.result_validator import ResultValidator, Severity


class TestCV01PortfolioNeverNegative:
    """CV-01: Portfolio value never negative."""

    def test_all_positive_values_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv01([100, 150, 200, 180])
        assert result.passed is True
        assert result.severity == Severity.CRITICAL

    def test_negative_value_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv01([100, 50, -10, 20])
        assert result.passed is False
        assert result.severity == Severity.CRITICAL
        assert result.value == -10

    def test_zero_value_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv01([100, 50, 0])
        assert result.passed is True

    def test_empty_list_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv01([])
        assert result.passed is False


class TestCV02DrawdownRange:
    """CV-02: Drawdown between 0% and 100%."""

    def test_valid_drawdown_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv02(25.5)
        assert result.passed is True

    def test_zero_drawdown_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv02(0.0)
        assert result.passed is True

    def test_100_percent_drawdown_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv02(100.0)
        assert result.passed is True

    def test_negative_drawdown_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv02(-5.0)
        assert result.passed is False
        assert result.severity == Severity.CRITICAL

    def test_over_100_drawdown_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv02(150.0)
        assert result.passed is False


class TestCV03StableStrategyDrawdown:
    """CV-03: Stable strategies have 0% max drawdown."""

    def test_stable_strategy_zero_drawdown_passes(self):
        validator = ResultValidator()
        # Strategy 1 (Safe Harbor) is stable
        result = validator.validate_cv03(strategy_id=1, max_drawdown=0.0)
        assert result.passed is True

    def test_stable_strategy_small_drawdown_passes(self):
        validator = ResultValidator()
        # Allow tiny floating point error
        result = validator.validate_cv03(strategy_id=1, max_drawdown=0.005)
        assert result.passed is True

    def test_stable_strategy_with_drawdown_warns(self):
        validator = ResultValidator()
        result = validator.validate_cv03(strategy_id=1, max_drawdown=5.0)
        assert result.passed is False
        assert result.severity == Severity.WARNING

    def test_crypto_strategy_drawdown_ok(self):
        validator = ResultValidator()
        # Strategy 2 (Stable Growth) has crypto exposure
        result = validator.validate_cv03(strategy_id=2, max_drawdown=10.0)
        assert result.passed is True
        assert result.severity == Severity.INFO


class TestCV04StableStrategyProfit:
    """CV-04: Final value >= deposited for stable strategies."""

    def test_stable_strategy_profit_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv04(
            strategy_id=1,
            deposited=10000,
            final_value=11000
        )
        assert result.passed is True

    def test_stable_strategy_break_even_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv04(
            strategy_id=1,
            deposited=10000,
            final_value=10000
        )
        assert result.passed is True

    def test_stable_strategy_loss_warns(self):
        validator = ResultValidator()
        result = validator.validate_cv04(
            strategy_id=1,
            deposited=10000,
            final_value=9500
        )
        assert result.passed is False
        assert result.severity == Severity.WARNING

    def test_crypto_strategy_loss_ok(self):
        validator = ResultValidator()
        result = validator.validate_cv04(
            strategy_id=10,  # Full Throttle
            deposited=10000,
            final_value=5000
        )
        assert result.passed is True


class TestCV05ReturnCalculation:
    """CV-05: Return % matches calculation."""

    def test_correct_return_passes(self):
        validator = ResultValidator()
        # 10% return: 10000 -> 11000
        result = validator.validate_cv05(
            deposited=10000,
            final_value=11000,
            reported_return=10.0
        )
        assert result.passed is True

    def test_incorrect_return_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv05(
            deposited=10000,
            final_value=11000,
            reported_return=15.0  # Wrong!
        )
        assert result.passed is False
        assert result.severity == Severity.CRITICAL

    def test_small_rounding_difference_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv05(
            deposited=10000,
            final_value=11000,
            reported_return=10.001  # Very close
        )
        assert result.passed is True

    def test_zero_deposit_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv05(
            deposited=0,
            final_value=100,
            reported_return=100.0
        )
        assert result.passed is False


class TestCV06GasCosts:
    """CV-06: Net return > 0 after gas costs."""

    def test_profitable_after_gas_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv06(
            gross_return=100,
            tx_count=10,
            chain='arbitrum'
        )
        # Gas: 10 * $0.30 = $3
        # Net: $100 - $3 = $97
        assert result.passed is True

    def test_unprofitable_after_gas_fails(self):
        validator = ResultValidator()
        result = validator.validate_cv06(
            gross_return=2,
            tx_count=10,
            chain='arbitrum'
        )
        # Gas: 10 * $0.30 = $3
        # Net: $2 - $3 = -$1
        assert result.passed is False
        assert result.severity == Severity.CRITICAL

    def test_solana_lower_gas(self):
        validator = ResultValidator()
        result = validator.validate_cv06(
            gross_return=0.10,
            tx_count=10,
            chain='solana'
        )
        # Gas: 10 * $0.005 = $0.05
        # Net: $0.10 - $0.05 = $0.05
        assert result.passed is True


class TestCV07MinimumDeposit:
    """CV-07: Initial deposit >= per-strategy minimum."""

    def test_above_minimum_passes(self):
        validator = ResultValidator()
        # Strategy 1 minimum: $50
        result = validator.validate_cv07(strategy_id=1, initial_deposit=100)
        assert result.passed is True

    def test_at_minimum_passes(self):
        validator = ResultValidator()
        result = validator.validate_cv07(strategy_id=1, initial_deposit=50)
        assert result.passed is True

    def test_below_minimum_warns(self):
        validator = ResultValidator()
        result = validator.validate_cv07(strategy_id=1, initial_deposit=25)
        assert result.passed is False
        assert result.severity == Severity.WARNING

    def test_full_throttle_minimum(self):
        validator = ResultValidator()
        # Strategy 10 minimum: $200
        result = validator.validate_cv07(strategy_id=10, initial_deposit=50)
        assert result.passed is False

        result = validator.validate_cv07(strategy_id=10, initial_deposit=200)
        assert result.passed is True


class TestValidationReport:
    """Test validation report aggregation."""

    def test_all_passed_status(self):
        from src.validators.result_validator import ValidationResult, ValidationReport

        validations = [
            ValidationResult('CV-01', True, Severity.CRITICAL, 'OK'),
            ValidationResult('CV-02', True, Severity.CRITICAL, 'OK'),
        ]
        report = ValidationReport(validations)

        assert report.status == 'PASSED'
        assert report.all_passed is True
        assert len(report.critical_failures) == 0

    def test_critical_failure_status(self):
        from src.validators.result_validator import ValidationResult, ValidationReport

        validations = [
            ValidationResult('CV-01', False, Severity.CRITICAL, 'Failed'),
            ValidationResult('CV-02', True, Severity.CRITICAL, 'OK'),
        ]
        report = ValidationReport(validations)

        assert report.status == 'FAILED'
        assert len(report.critical_failures) == 1

    def test_warning_status(self):
        from src.validators.result_validator import ValidationResult, ValidationReport

        validations = [
            ValidationResult('CV-01', True, Severity.CRITICAL, 'OK'),
            ValidationResult('CV-03', False, Severity.WARNING, 'Warning'),
        ]
        report = ValidationReport(validations)

        assert report.status == 'PASS_WITH_WARNINGS'
        assert len(report.warnings) == 1
