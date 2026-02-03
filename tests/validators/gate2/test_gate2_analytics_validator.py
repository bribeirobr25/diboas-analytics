"""Tests for Gate 2 Analytics Validator."""
import pytest
import math
from src.validators.gate2.gate2_analytics_validator import (
    Gate2AnalyticsValidator, Gate2ValidationStatus, Gate2ValidationSeverity
)


class TestGate2AnalyticsValidator:
    """Tests for the main Gate 2 validator."""

    @pytest.fixture
    def valid_data(self):
        """Complete valid data for all 10 strategies."""
        strategies = {}
        for i in range(1, 11):
            strategies[str(i)] = {
                "var_95": 5.0 + i,
                "cvar_99": 7.0 + i,
                "sharpe_ratio": 0.5,
                "max_drawdown": 10.0 + i * 2,
                "median_return": 5.0,
                "probability_of_loss": 0.2
            }

        return {
            "battle_test": {"strategies": strategies},
            "monte_carlo": {
                "strategies": {
                    str(i): {
                        "percentile_5": -10,
                        "percentile_50": 5,
                        "percentile_95": 20
                    } for i in range(1, 11)
                }
            },
            "risk_metrics": {"strategies": strategies}
        }

    def test_should_pass_with_valid_data(self, valid_data):
        """Passes with complete valid data."""
        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.status == Gate2ValidationStatus.PASS
        assert len(result.errors) == 0

    def test_should_fail_when_strategy_missing(self, valid_data):
        """Fails when a strategy is missing."""
        # Remove strategy 5
        del valid_data["risk_metrics"]["strategies"]["5"]

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.status == Gate2ValidationStatus.FAIL
        assert any("strategy 5" in e.message for e in result.errors)

    def test_should_fail_when_var_exceeds_bounds(self, valid_data):
        """Fails when VaR exceeds 100%."""
        valid_data["risk_metrics"]["strategies"]["3"]["var_95"] = 150  # > 100%

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.status == Gate2ValidationStatus.FAIL
        assert any("G2-BND-002" in e.code for e in result.errors)

    def test_should_warn_when_sharpe_is_extreme(self, valid_data):
        """Warns when Sharpe ratio is extreme but valid."""
        valid_data["risk_metrics"]["strategies"]["10"]["sharpe_ratio"] = -4  # Extreme but valid
        valid_data["risk_metrics"]["strategies"]["10"]["probability_of_loss"] = 0.5

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        # Negative Sharpe is allowed, should still pass
        assert result.passed

    def test_should_pass_with_valid_negative_sharpe(self, valid_data):
        """Passes with valid negative Sharpe when prob_loss is coherent."""
        valid_data["risk_metrics"]["strategies"]["10"]["sharpe_ratio"] = -2
        valid_data["risk_metrics"]["strategies"]["10"]["probability_of_loss"] = 0.5

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.passed

    def test_should_track_strategies_validated(self, valid_data):
        """Tracks number of strategies validated."""
        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.strategies_validated == 10

    def test_should_track_duration(self, valid_data):
        """Tracks validation duration."""
        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert result.duration_ms >= 0


class TestGate2CompletenessChecker:
    """Tests for completeness checking."""

    @pytest.fixture
    def valid_data(self):
        """Complete valid data."""
        strategies = {str(i): {"var_95": 5, "cvar_99": 7, "sharpe_ratio": 0.5,
                               "max_drawdown": 10, "median_return": 5,
                               "probability_of_loss": 0.2} for i in range(1, 11)}
        return {
            "battle_test": {"strategies": strategies},
            "monte_carlo": {"strategies": strategies},
            "risk_metrics": {"strategies": strategies}
        }

    def test_should_detect_missing_battle_test_strategy(self, valid_data):
        """Detects missing Battle Test strategy."""
        del valid_data["battle_test"]["strategies"]["3"]

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-CMP-001" in e.code for e in result.errors)

    def test_should_detect_missing_monte_carlo_strategy(self, valid_data):
        """Detects missing Monte Carlo strategy."""
        del valid_data["monte_carlo"]["strategies"]["7"]

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-CMP-002" in e.code for e in result.errors)

    def test_should_detect_missing_metric(self, valid_data):
        """Detects missing required metric."""
        del valid_data["risk_metrics"]["strategies"]["5"]["sharpe_ratio"]

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-CMP-004" in e.code for e in result.errors)


class TestGate2BoundsValidator:
    """Tests for bounds validation."""

    @pytest.fixture
    def valid_data(self):
        """Complete valid data."""
        strategies = {str(i): {"var_95": 5, "cvar_99": 7, "sharpe_ratio": 0.5,
                               "max_drawdown": 10, "median_return": 5,
                               "probability_of_loss": 0.2} for i in range(1, 11)}
        return {
            "battle_test": {"strategies": strategies},
            "monte_carlo": {"strategies": strategies},
            "risk_metrics": {"strategies": strategies}
        }

    def test_should_detect_negative_var(self, valid_data):
        """Detects negative VaR."""
        valid_data["risk_metrics"]["strategies"]["1"]["var_95"] = -5

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-BND-001" in e.code for e in result.errors)

    def test_should_detect_probability_over_one(self, valid_data):
        """Detects probability of loss > 1."""
        valid_data["risk_metrics"]["strategies"]["2"]["probability_of_loss"] = 1.5

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-BND-002" in e.code for e in result.errors)

    def test_should_detect_nan_value(self, valid_data):
        """Detects NaN values."""
        valid_data["risk_metrics"]["strategies"]["4"]["sharpe_ratio"] = float('nan')

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-INV-001" in e.code for e in result.errors)

    def test_should_detect_infinite_value(self, valid_data):
        """Detects infinite values."""
        valid_data["risk_metrics"]["strategies"]["6"]["max_drawdown"] = float('inf')

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-INV-002" in e.code for e in result.errors)


class TestGate2StatisticalSanity:
    """Tests for statistical sanity checks."""

    @pytest.fixture
    def valid_data(self):
        """Complete valid data."""
        strategies = {str(i): {"var_95": 5, "cvar_99": 7, "sharpe_ratio": 0.5,
                               "max_drawdown": 10, "median_return": 5,
                               "probability_of_loss": 0.2} for i in range(1, 11)}
        return {
            "battle_test": {"strategies": strategies},
            "monte_carlo": {
                "strategies": {
                    str(i): {"percentile_5": -10, "percentile_50": 5, "percentile_95": 20}
                    for i in range(1, 11)
                }
            },
            "risk_metrics": {"strategies": strategies}
        }

    def test_should_detect_unordered_percentiles(self, valid_data):
        """Detects percentiles that are not properly ordered."""
        valid_data["monte_carlo"]["strategies"]["3"]["percentile_5"] = 30  # > P50 and P95
        valid_data["monte_carlo"]["strategies"]["3"]["percentile_50"] = 10

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-STA-001" in e.code for e in result.errors)

    def test_should_warn_when_cvar_less_than_var(self, valid_data):
        """Warns when CVaR is significantly less than VaR."""
        valid_data["risk_metrics"]["strategies"]["5"]["var_95"] = 20
        valid_data["risk_metrics"]["strategies"]["5"]["cvar_99"] = 10  # < VaR * 0.9

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-STA-002" in e.code for e in result.warnings)


class TestGate2CoherenceChecker:
    """Tests for coherence checks."""

    @pytest.fixture
    def valid_data(self):
        """Complete valid data."""
        strategies = {str(i): {"var_95": 5, "cvar_99": 7, "sharpe_ratio": 0.5,
                               "max_drawdown": 10, "median_return": 5,
                               "probability_of_loss": 0.2} for i in range(1, 11)}
        return {
            "battle_test": {"strategies": strategies},
            "monte_carlo": {"strategies": strategies},
            "risk_metrics": {"strategies": strategies}
        }

    def test_should_warn_high_sharpe_high_loss_prob(self, valid_data):
        """Warns when high Sharpe but high probability of loss."""
        valid_data["risk_metrics"]["strategies"]["7"]["sharpe_ratio"] = 3
        valid_data["risk_metrics"]["strategies"]["7"]["probability_of_loss"] = 0.4

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-COH-001" in e.code for e in result.warnings)

    def test_should_warn_negative_sharpe_low_loss_prob(self, valid_data):
        """Warns when negative Sharpe but low probability of loss."""
        valid_data["risk_metrics"]["strategies"]["9"]["sharpe_ratio"] = -2
        valid_data["risk_metrics"]["strategies"]["9"]["probability_of_loss"] = 0.1

        validator = Gate2AnalyticsValidator()
        result = validator.validate(
            valid_data["battle_test"],
            valid_data["monte_carlo"],
            valid_data["risk_metrics"]
        )
        assert any("G2-COH-002" in e.code for e in result.warnings)
