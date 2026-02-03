"""Tests for market triggers."""

import pytest
from src.triggers.market.price_movement_triggers import (
    BTCDropLevel3Trigger,
    BTCDropLevel4Trigger,
    ETHDropLevel3Trigger,
    SOLDropLevel3Trigger,
    SOLDropLevel4Trigger,
)
from src.triggers.market.volatility_triggers import (
    VIXSpikeLevel2Trigger,
    VIXSpikeLevel3Trigger,
    CryptoVolatilityTrigger,
)
from src.triggers.base import (
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
)


class TestBTCDropTriggers:
    """Tests for BTC price drop triggers."""

    def test_should_fire_l3_when_btc_drops_more_than_10_percent(self):
        """L3 trigger fires when BTC drops >10%."""
        trigger = BTCDropLevel3Trigger({})
        data = {"market_prices": {"btc": {"change_24h_pct": -12}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-BTC-L3"
        assert result.priority == IntelligenceTriggerPriority.P1_HIGH

    def test_should_not_fire_l3_when_btc_drops_less_than_10_percent(self):
        """L3 trigger does not fire when BTC drops <10%."""
        trigger = BTCDropLevel3Trigger({})
        data = {"market_prices": {"btc": {"change_24h_pct": -8}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_l4_when_btc_drops_more_than_20_percent(self):
        """L4 trigger fires when BTC drops >20%."""
        trigger = BTCDropLevel4Trigger({})
        data = {"market_prices": {"btc": {"change_24h_pct": -25}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-BTC-L4"
        assert result.priority == IntelligenceTriggerPriority.P0_CRITICAL

    def test_should_not_fire_on_positive_change(self):
        """Trigger does not fire on positive price change."""
        trigger = BTCDropLevel3Trigger({})
        data = {"market_prices": {"btc": {"change_24h_pct": 5}}}
        result = trigger.evaluate(data)
        assert result.fired is False


class TestETHDropTriggers:
    """Tests for ETH price drop triggers."""

    def test_should_fire_when_eth_drops_more_than_15_percent(self):
        """L3 trigger fires when ETH drops >15%."""
        trigger = ETHDropLevel3Trigger({})
        data = {"market_prices": {"eth": {"change_24h_pct": -18}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-ETH-L3"

    def test_should_not_fire_when_eth_drops_less_than_15_percent(self):
        """L3 trigger does not fire when ETH drops <15%."""
        trigger = ETHDropLevel3Trigger({})
        data = {"market_prices": {"eth": {"change_24h_pct": -10}}}
        result = trigger.evaluate(data)
        assert result.fired is False


class TestSOLDropTriggers:
    """Tests for SOL price drop triggers."""

    def test_should_fire_l3_when_sol_drops_more_than_20_percent(self):
        """L3 trigger fires when SOL drops >20%."""
        trigger = SOLDropLevel3Trigger({})
        data = {"market_prices": {"sol": {"change_24h_pct": -25}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-SOL-L3"

    def test_should_fire_l4_when_sol_drops_more_than_30_percent(self):
        """L4 trigger fires when SOL drops >30%."""
        trigger = SOLDropLevel4Trigger({})
        data = {"market_prices": {"sol": {"change_24h_pct": -35}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-SOL-L4"
        assert result.priority == IntelligenceTriggerPriority.P0_CRITICAL


class TestVIXTriggers:
    """Tests for VIX volatility triggers."""

    def test_should_fire_l2_when_vix_above_30(self):
        """L2 trigger fires when VIX >30."""
        trigger = VIXSpikeLevel2Trigger({})
        data = {"macro_indicators": {"vix": 35}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MACRO-VIX-L2"
        assert result.priority == IntelligenceTriggerPriority.P2_MEDIUM

    def test_should_not_fire_l2_when_vix_below_30(self):
        """L2 trigger does not fire when VIX <30."""
        trigger = VIXSpikeLevel2Trigger({})
        data = {"macro_indicators": {"vix": 25}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_l3_when_vix_above_40(self):
        """L3 trigger fires when VIX >40."""
        trigger = VIXSpikeLevel3Trigger({})
        data = {"macro_indicators": {"vix": 45}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MACRO-VIX-L3"
        assert result.priority == IntelligenceTriggerPriority.P1_HIGH


class TestCryptoVolatilityTrigger:
    """Tests for crypto volatility trigger."""

    def test_should_fire_when_volatility_2_std_above_mean(self):
        """Trigger fires when volatility is >2 std dev above mean."""
        trigger = CryptoVolatilityTrigger({})
        data = {"macro_indicators": {"crypto_volatility": {
            "current": 80,
            "mean_30d": 50,
            "std_30d": 10
        }}}  # z-score = 3
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_should_not_fire_when_volatility_within_normal(self):
        """Trigger does not fire when volatility is normal."""
        trigger = CryptoVolatilityTrigger({})
        data = {"macro_indicators": {"crypto_volatility": {
            "current": 55,
            "mean_30d": 50,
            "std_30d": 10
        }}}  # z-score = 0.5
        result = trigger.evaluate(data)
        assert result.fired is False


class TestMarketTriggerCategories:
    """Tests for market trigger categories."""

    def test_price_triggers_have_market_category(self):
        """Price movement triggers have market_condition category."""
        triggers = [
            BTCDropLevel3Trigger({}),
            ETHDropLevel3Trigger({}),
            SOLDropLevel3Trigger({}),
        ]
        for trigger in triggers:
            assert trigger.category == IntelligenceTriggerCategory.MARKET_CONDITION

    def test_vix_triggers_have_macro_category(self):
        """VIX triggers have macro_indicator category."""
        triggers = [
            VIXSpikeLevel2Trigger({}),
            VIXSpikeLevel3Trigger({}),
        ]
        for trigger in triggers:
            assert trigger.category == IntelligenceTriggerCategory.MACRO_INDICATOR
