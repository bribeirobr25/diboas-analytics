"""
Tests for Dream Mode export functionality.
"""

import pytest
from config.dream_mode import (
    DREAM_MODE_PATHS,
    DISCLAIMERS,
    BANK_COMPARISON,
    get_path_for_strategy,
    get_strategies_for_path
)


class TestDreamModePathMapping:
    """Test Dream Mode path mappings."""

    def test_all_strategies_mapped(self):
        """All 10 strategies should be mapped to exactly one path."""
        all_strategies = set()
        for path in DREAM_MODE_PATHS.values():
            all_strategies.update(path['strategies'])

        assert all_strategies == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    def test_no_duplicate_mappings(self):
        """Each strategy should only appear in one path."""
        all_strategies = []
        for path in DREAM_MODE_PATHS.values():
            all_strategies.extend(path['strategies'])

        # No duplicates
        assert len(all_strategies) == len(set(all_strategies))

    def test_safety_path_only_stable_strategies(self):
        """Safety path should only include 0% crypto strategies."""
        safety_strategies = DREAM_MODE_PATHS['safety']['strategies']
        assert safety_strategies == [1, 3, 5, 7, 9]

    def test_balance_path_moderate_crypto(self):
        """Balance path should include 30-40% crypto strategies."""
        balance_strategies = DREAM_MODE_PATHS['balance']['strategies']
        assert balance_strategies == [2, 4, 6]

    def test_growth_path_high_crypto(self):
        """Growth path should include 70-85% crypto strategies."""
        growth_strategies = DREAM_MODE_PATHS['growth']['strategies']
        assert growth_strategies == [8, 10]

    def test_get_path_for_strategy(self):
        """Test getting path for a given strategy."""
        assert get_path_for_strategy(1) == 'safety'
        assert get_path_for_strategy(2) == 'balance'
        assert get_path_for_strategy(10) == 'growth'

    def test_get_path_for_invalid_strategy_raises(self):
        """Invalid strategy ID should raise ValueError."""
        with pytest.raises(ValueError):
            get_path_for_strategy(99)

    def test_get_strategies_for_path(self):
        """Test getting strategies for a path."""
        assert get_strategies_for_path('safety') == [1, 3, 5, 7, 9]
        assert get_strategies_for_path('growth') == [8, 10]


class TestDisclaimers:
    """Test CLO-mandated disclaimers."""

    def test_all_required_disclaimers_present(self):
        """All required disclaimers should be present."""
        required = ['simulation', 'risk', 'not_advice', 'card_watermark', 'bank_comparison']
        for key in required:
            assert key in DISCLAIMERS
            assert len(DISCLAIMERS[key]) > 0

    def test_simulation_disclaimer_mentions_dates(self):
        """Simulation disclaimer should mention the date range."""
        assert '2022' in DISCLAIMERS['simulation']
        assert '2025' in DISCLAIMERS['simulation']

    def test_card_watermark_is_concise(self):
        """Card watermark should be concise for display."""
        assert len(DISCLAIMERS['card_watermark']) < 100


class TestBankComparison:
    """Test bank comparison configuration."""

    def test_bank_apy_is_reasonable(self):
        """Bank APY should be low (typical savings rate)."""
        assert 0 < BANK_COMPARISON['apy'] < 2.0

    def test_bank_source_specified(self):
        """Bank comparison should have source attribution."""
        assert 'source' in BANK_COMPARISON
        assert len(BANK_COMPARISON['source']) > 0


class TestPathProjections:
    """Test projection calculations."""

    def test_projection_multiplier_calculation(self):
        """Test that projection multipliers are calculated correctly."""
        from src.domain.dream_mode import PathProjection

        # 10% APY for 1 year = 1.10 multiplier
        proj = PathProjection(
            period='1_year',
            multiplier=1.10,
            bank_multiplier=1.005
        )

        assert proj.projected_value(1000) == 1100
        assert proj.bank_value(1000) == 1005
        assert proj.advantage_over_bank(1000) == 95

    def test_five_year_projection_compounds(self):
        """Test that 5-year projections compound correctly."""
        from src.domain.dream_mode import PathProjection

        # 10% APY for 5 years = (1.10)^5 = 1.61051
        proj = PathProjection(
            period='5_years',
            multiplier=1.6105,
            bank_multiplier=1.0253
        )

        # $1000 at 10% for 5 years
        assert round(proj.projected_value(1000), 0) == 1610
