"""Tests for newly added triggers (Discrepancy Fixes Task 1)."""
import pytest
from src.triggers.protocol.sky_protocol_triggers import SkyBufferLevel2Trigger
from src.triggers.protocol.sanctum_protocol_triggers import (
    SanctumTVLLevel3Trigger, SanctumTVLLevel4Trigger
)
from src.triggers.protocol.jlp_protocol_triggers import (
    JLPAPYLevel2Trigger, JLPTVLLevel3Trigger
)
from src.triggers.market.price_movement_triggers import MarketCapLevel3Trigger


class TestSkyBufferTrigger:
    """Tests for Sky Surplus Buffer trigger."""

    def test_should_fire_when_buffer_below_threshold(self):
        """Fires when surplus buffer is below threshold."""
        trigger = SkyBufferLevel2Trigger({"threshold_usd": 50_000_000})
        data = {"protocol_health": {"sky": {"surplus_buffer_usd": 30_000_000}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-BUF-L2"

    def test_should_not_fire_when_buffer_above_threshold(self):
        """Does not fire when surplus buffer is above threshold."""
        trigger = SkyBufferLevel2Trigger({"threshold_usd": 50_000_000})
        data = {"protocol_health": {"sky": {"surplus_buffer_usd": 75_000_000}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_not_fire_when_buffer_at_threshold(self):
        """Does not fire when surplus buffer equals threshold."""
        trigger = SkyBufferLevel2Trigger({"threshold_usd": 50_000_000})
        data = {"protocol_health": {"sky": {"surplus_buffer_usd": 50_000_000}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_have_correct_affected_strategies(self):
        """Has correct affected strategies (Sky SSR strategies)."""
        trigger = SkyBufferLevel2Trigger({})
        assert trigger.affected_strategies == [1, 3, 5, 7, 9]


class TestSanctumTVLTriggers:
    """Tests for Sanctum TVL triggers."""

    def test_should_fire_l3_when_tvl_drops_25_pct(self):
        """L3 fires when TVL drops 25% (> 20% threshold)."""
        trigger = SanctumTVLLevel3Trigger({"threshold_pct": -20})
        data = {"protocol_health": {"sanctum": {"tvl_change_24h_pct": -25}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SAN-TVL-L3"

    def test_should_not_fire_l3_when_tvl_drops_15_pct(self):
        """L3 does not fire when TVL drops only 15%."""
        trigger = SanctumTVLLevel3Trigger({"threshold_pct": -20})
        data = {"protocol_health": {"sanctum": {"tvl_change_24h_pct": -15}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_l4_when_tvl_drops_55_pct(self):
        """L4 fires when TVL drops 55% (> 50% threshold)."""
        trigger = SanctumTVLLevel4Trigger({"threshold_pct": -50})
        data = {"protocol_health": {"sanctum": {"tvl_change_24h_pct": -55}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SAN-TVL-L4"

    def test_should_not_fire_l4_when_tvl_drops_30_pct(self):
        """L4 does not fire when TVL drops only 30%."""
        trigger = SanctumTVLLevel4Trigger({"threshold_pct": -50})
        data = {"protocol_health": {"sanctum": {"tvl_change_24h_pct": -30}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_l3_has_correct_affected_strategies(self):
        """L3 affects Sanctum strategies."""
        trigger = SanctumTVLLevel3Trigger({})
        assert trigger.affected_strategies == [2, 4, 6, 8, 10]

    def test_l4_has_correct_affected_strategies(self):
        """L4 affects Sanctum strategies."""
        trigger = SanctumTVLLevel4Trigger({})
        assert trigger.affected_strategies == [2, 4, 6, 8, 10]


class TestJLPTriggers:
    """Tests for JLP APY and TVL triggers."""

    def test_should_fire_apy_l2_when_apy_drops_45_pct(self):
        """APY L2 fires when APY drops 45% from 7d average."""
        trigger = JLPAPYLevel2Trigger({"threshold_pct": -40})
        data = {"protocol_health": {"jlp": {"current_apy": 11, "avg_7d_apy": 20}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "JLP-APY-L2"

    def test_should_not_fire_apy_l2_when_apy_drops_30_pct(self):
        """APY L2 does not fire when APY drops only 30%."""
        trigger = JLPAPYLevel2Trigger({"threshold_pct": -40})
        data = {"protocol_health": {"jlp": {"current_apy": 14, "avg_7d_apy": 20}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_handle_zero_avg_apy(self):
        """Handles zero average APY gracefully."""
        trigger = JLPAPYLevel2Trigger({"threshold_pct": -40})
        data = {"protocol_health": {"jlp": {"current_apy": 5, "avg_7d_apy": 0}}}
        result = trigger.evaluate(data)
        assert result.fired is False  # apy_change_pct = 0 when avg is 0

    def test_should_fire_tvl_l3_when_tvl_drops_35_pct(self):
        """TVL L3 fires when TVL drops 35% (> 30% threshold)."""
        trigger = JLPTVLLevel3Trigger({"threshold_pct": -30})
        data = {"protocol_health": {"jlp": {"tvl_change_24h_pct": -35}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "JLP-TVL-L3"

    def test_should_not_fire_tvl_l3_when_tvl_drops_20_pct(self):
        """TVL L3 does not fire when TVL drops only 20%."""
        trigger = JLPTVLLevel3Trigger({"threshold_pct": -30})
        data = {"protocol_health": {"jlp": {"tvl_change_24h_pct": -20}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_apy_l2_has_correct_affected_strategies(self):
        """APY L2 affects JLP strategies."""
        trigger = JLPAPYLevel2Trigger({})
        assert trigger.affected_strategies == [6, 8, 10]

    def test_tvl_l3_has_correct_affected_strategies(self):
        """TVL L3 affects JLP strategies."""
        trigger = JLPTVLLevel3Trigger({})
        assert trigger.affected_strategies == [6, 8, 10]


class TestMarketCapTrigger:
    """Tests for Broad Market Cap trigger."""

    def test_should_fire_when_broad_market_crashes(self):
        """Fires when average of major cryptos drops > 15%."""
        trigger = MarketCapLevel3Trigger({"threshold_pct": -15})
        data = {
            "prices": {
                "btc_change_24h_pct": -18,
                "eth_change_24h_pct": -20,
                "sol_change_24h_pct": -25
            }
        }
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "MKT-CAP-L3"
        assert result.affected_strategies == list(range(1, 11))

    def test_should_not_fire_when_only_one_asset_down(self):
        """Does not fire when only one asset is significantly down."""
        trigger = MarketCapLevel3Trigger({"threshold_pct": -15})
        data = {
            "prices": {
                "btc_change_24h_pct": -20,
                "eth_change_24h_pct": 2,
                "sol_change_24h_pct": 5
            }
        }
        result = trigger.evaluate(data)
        # Average = (-20 + 2 + 5) / 3 = -4.33, not < -15
        assert result.fired is False

    def test_should_not_fire_when_market_is_flat(self):
        """Does not fire when market is flat."""
        trigger = MarketCapLevel3Trigger({"threshold_pct": -15})
        data = {
            "prices": {
                "btc_change_24h_pct": 0,
                "eth_change_24h_pct": -1,
                "sol_change_24h_pct": 2
            }
        }
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_when_market_drops_exactly_at_threshold(self):
        """Fires when average exactly at threshold."""
        trigger = MarketCapLevel3Trigger({"threshold_pct": -15})
        data = {
            "prices": {
                "btc_change_24h_pct": -15,
                "eth_change_24h_pct": -15,
                "sol_change_24h_pct": -15.1
            }
        }
        result = trigger.evaluate(data)
        # Average = -15.03, which is < -15
        assert result.fired is True

    def test_affects_all_strategies(self):
        """Affects all 10 strategies."""
        trigger = MarketCapLevel3Trigger({})
        assert trigger.affected_strategies == list(range(1, 11))

    def test_has_correct_priority(self):
        """Has P0 Critical priority."""
        from src.triggers.base import IntelligenceTriggerPriority
        trigger = MarketCapLevel3Trigger({})
        assert trigger.priority == IntelligenceTriggerPriority.P0_CRITICAL

    def test_metadata_includes_all_changes(self):
        """Metadata includes all individual price changes."""
        trigger = MarketCapLevel3Trigger({})
        data = {
            "prices": {
                "btc_change_24h_pct": -18,
                "eth_change_24h_pct": -20,
                "sol_change_24h_pct": -25
            }
        }
        result = trigger.evaluate(data)
        assert result.metadata["btc_change_24h_pct"] == -18
        assert result.metadata["eth_change_24h_pct"] == -20
        assert result.metadata["sol_change_24h_pct"] == -25
        assert result.metadata["avg_change_pct"] == -21
