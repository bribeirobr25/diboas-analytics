"""
Tests for Battle Test engine.
"""

import pytest
from datetime import date


class TestBattleTestScenarios:
    """Test Battle Test scenarios configuration."""

    def test_scenario_a_values(self):
        """Test Scenario A (Felipe) values."""
        from src.engines.battle_test import SCENARIOS

        assert SCENARIOS['A']['initial_deposit'] == 10000
        assert SCENARIOS['A']['monthly_dca'] == 200

    def test_scenario_b_values(self):
        """Test Scenario B (Ana) values."""
        from src.engines.battle_test import SCENARIOS

        assert SCENARIOS['B']['initial_deposit'] == 5
        assert SCENARIOS['B']['monthly_dca'] == 5

    def test_scenario_c_has_all_strategies(self):
        """Test Scenario C has minimums for all strategies."""
        from src.engines.battle_test import SCENARIOS

        minimums = SCENARIOS['C']['minimums']
        for strategy_id in range(1, 11):
            assert strategy_id in minimums
            assert 'initial' in minimums[strategy_id]
            assert 'monthly' in minimums[strategy_id]


class TestBattleTestResult:
    """Test BattleTestResult dataclass."""

    def test_result_creation(self):
        """Test creating a BattleTestResult."""
        from src.domain.simulation import BattleTestResult

        result = BattleTestResult(
            strategy_id=1,
            strategy_name='Safe Harbor',
            scenario='$10,000 + $200/mo',
            period_start=date(2022, 5, 1),
            period_end=date(2025, 12, 31),
            days=1334,
            deposited=18600,
            final_value=20445,
            profit=1845,
            return_pct=9.9,
            max_drawdown_pct=0.0
        )

        assert result.strategy_id == 1
        assert result.is_profitable is True
        assert result.max_drawdown_pct == 0.0

    def test_annualized_return(self):
        """Test annualized return calculation."""
        from src.domain.simulation import BattleTestResult

        result = BattleTestResult(
            strategy_id=1,
            strategy_name='Test',
            scenario='Test',
            period_start=date(2022, 1, 1),
            period_end=date(2024, 12, 31),
            days=1096,  # ~3 years
            deposited=10000,
            final_value=13310,  # 10% annual = 1.1^3
            profit=3310,
            return_pct=33.1,
            max_drawdown_pct=0.0
        )

        # Should be approximately 10% annual
        assert 9.0 < result.annualized_return < 11.0

    def test_to_dict(self):
        """Test conversion to dictionary."""
        from src.domain.simulation import BattleTestResult

        result = BattleTestResult(
            strategy_id=1,
            strategy_name='Safe Harbor',
            scenario='Test',
            period_start=date(2022, 5, 1),
            period_end=date(2025, 12, 31),
            days=1334,
            deposited=18600,
            final_value=20445,
            profit=1845,
            return_pct=9.9,
            max_drawdown_pct=0.0
        )

        d = result.to_dict()
        assert d['strategy_id'] == 1
        assert d['deposited'] == 18600
        assert d['return_pct'] == 9.9


class TestJLPCalculation:
    """Test JLP return calculations."""

    def test_jlp_daily_return(self):
        """Test JLP daily return calculation."""
        from src.utils.proxies import calculate_jlp_daily_return

        # 1% SOL return, 0.5% ETH return, 0.5% BTC return, 25% APY
        daily_return = calculate_jlp_daily_return(
            sol_return=0.01,
            eth_return=0.005,
            btc_return=0.005,
            jlp_apy=25.0
        )

        # Basket: 0.45*0.01 + 0.27*0.005 + 0.27*0.005 = 0.0072
        # Fee: 25/365/100 = 0.000685
        # Total: ~0.0079
        assert 0.007 < daily_return < 0.009

    def test_jlp_negative_returns(self):
        """Test JLP with negative price returns."""
        from src.utils.proxies import calculate_jlp_daily_return

        # All crypto down 5%
        daily_return = calculate_jlp_daily_return(
            sol_return=-0.05,
            eth_return=-0.05,
            btc_return=-0.05,
            jlp_apy=25.0
        )

        # Basket: -5% + fee = negative
        assert daily_return < 0
