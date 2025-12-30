"""
Tests for Monte Carlo simulation engine.
"""

import pytest
import numpy as np


class TestMonteCarloRegimes:
    """Test Monte Carlo regime configuration."""

    def test_all_regimes_defined(self):
        """All expected regimes should be defined."""
        from src.engines.monte_carlo import MonteCarloEngine

        expected = ['bull', 'bear', 'crash', 'recovery']
        for regime in expected:
            assert regime in MonteCarloEngine.REGIMES

    def test_regime_parameters(self):
        """Each regime should have required parameters."""
        from src.engines.monte_carlo import MonteCarloEngine

        for regime, params in MonteCarloEngine.REGIMES.items():
            assert 'mean_mult' in params
            assert 'vol_mult' in params
            assert 'duration' in params

    def test_crash_regime_negative_mean(self):
        """Crash regime should have negative mean multiplier."""
        from src.engines.monte_carlo import MonteCarloEngine

        assert MonteCarloEngine.REGIMES['crash']['mean_mult'] < 0

    def test_crash_regime_high_volatility(self):
        """Crash regime should have high volatility."""
        from src.engines.monte_carlo import MonteCarloEngine

        crash_vol = MonteCarloEngine.REGIMES['crash']['vol_mult']
        bull_vol = MonteCarloEngine.REGIMES['bull']['vol_mult']
        assert crash_vol > bull_vol


class TestMonteCarloTransitions:
    """Test Markov transition matrix."""

    def test_transitions_sum_to_one(self):
        """Transition probabilities should sum to 1."""
        from src.engines.monte_carlo import MonteCarloEngine

        for regime, transitions in MonteCarloEngine.TRANSITIONS.items():
            total = sum(transitions.values())
            assert abs(total - 1.0) < 0.001

    def test_bull_stays_bull_mostly(self):
        """Bull regime should mostly stay in bull."""
        from src.engines.monte_carlo import MonteCarloEngine

        assert MonteCarloEngine.TRANSITIONS['bull']['bull'] > 0.7

    def test_crash_transitions_to_recovery(self):
        """Crash should have high probability of transitioning to recovery."""
        from src.engines.monte_carlo import MonteCarloEngine

        assert MonteCarloEngine.TRANSITIONS['crash']['recovery'] >= 0.5


class TestMonteCarloResult:
    """Test MonteCarloResult dataclass."""

    def test_result_creation(self):
        """Test creating a MonteCarloResult."""
        from src.domain.simulation import MonteCarloResult

        result = MonteCarloResult(
            strategy_id=1,
            strategy_name='Safe Harbor',
            simulations=5000,
            horizon_months=48,
            total_deposited=19400,
            mean_final=22000,
            median_final=21500,
            std_final=1500,
            mean_return=13.4,
            median_return=10.8,
            prob_any_loss=0.0,
            prob_loss_10pct=0.0,
            prob_loss_20pct=0.0,
            prob_loss_50pct=0.0,
            var_95=19000,
            cvar_95=18500,
            var_99=18000,
            cvar_99=17500,
            p5_final=19000,
            p95_final=25000,
            mean_max_drawdown=0.0,
            p95_max_drawdown=0.0
        )

        assert result.strategy_id == 1
        assert result.simulations == 5000
        assert result.prob_any_loss == 0.0

    def test_confidence_interval(self):
        """Test 90% confidence interval property."""
        from src.domain.simulation import MonteCarloResult

        result = MonteCarloResult(
            strategy_id=1,
            strategy_name='Test',
            simulations=5000,
            horizon_months=48,
            total_deposited=19400,
            mean_final=22000,
            median_final=21500,
            std_final=1500,
            mean_return=13.4,
            median_return=10.8,
            prob_any_loss=0.0,
            prob_loss_10pct=0.0,
            prob_loss_20pct=0.0,
            prob_loss_50pct=0.0,
            var_95=19000,
            cvar_95=18500,
            var_99=18000,
            cvar_99=17500,
            p5_final=18000,
            p95_final=26000,
            mean_max_drawdown=0.0,
            p95_max_drawdown=0.0
        )

        ci = result.confidence_interval_90
        assert ci == (18000, 26000)


class TestMaxDrawdownCalculation:
    """Test maximum drawdown calculation."""

    def test_no_drawdown(self):
        """Path with no decline should have 0 drawdown."""
        from src.engines.monte_carlo import MonteCarloEngine

        engine = MonteCarloEngine(n_simulations=100)
        path = np.array([100, 110, 120, 130, 140])
        drawdown = engine._calculate_max_drawdown(path)
        assert drawdown == 0.0

    def test_simple_drawdown(self):
        """Test simple drawdown calculation."""
        from src.engines.monte_carlo import MonteCarloEngine

        engine = MonteCarloEngine(n_simulations=100)
        # Peak at 100, drops to 80, then recovers
        path = np.array([80, 100, 80, 90])
        drawdown = engine._calculate_max_drawdown(path)
        # Should be 20% (100 -> 80)
        assert abs(drawdown - 0.2) < 0.001

    def test_multiple_drawdowns(self):
        """Test finding maximum of multiple drawdowns."""
        from src.engines.monte_carlo import MonteCarloEngine

        engine = MonteCarloEngine(n_simulations=100)
        # First drawdown: 100 -> 90 (10%)
        # Second drawdown: 120 -> 80 (33%)
        path = np.array([100, 90, 120, 80, 100])
        drawdown = engine._calculate_max_drawdown(path)
        # Should be ~33%
        assert abs(drawdown - 0.333) < 0.01
