"""Tests for protocol triggers."""

import pytest
from src.triggers.protocol.sky_protocol_triggers import (
    SkyUSDSDepegLevel2Trigger,
    SkyUSDSDepegLevel3Trigger,
    SkyUSDSDepegLevel4Trigger,
    SkyTVLDropLevel2Trigger,
    SkyTVLDropLevel3Trigger,
)
from src.triggers.protocol.sanctum_protocol_triggers import (
    SanctumAPYDropLevel2Trigger,
    SanctumLSTHealthTrigger,
)
from src.triggers.protocol.jlp_protocol_triggers import (
    JLPUtilizationLevel2Trigger,
    JLPUtilizationLevel3Trigger,
)
from src.triggers.protocol.aave_protocol_triggers import (
    AaveUtilizationLevel2Trigger,
    AaveLiquidationRiskTrigger,
)
from src.triggers.base import (
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
)


class TestSkyUSDSDepegTriggers:
    """Tests for Sky USDS depeg triggers."""

    def test_should_fire_when_usds_depegs_above_1_percent(self):
        """L2 trigger fires when depeg exceeds 1%."""
        trigger = SkyUSDSDepegLevel2Trigger({})
        data = {"protocol_health": {"sky": {"usds_price": 0.98}}}  # 2% depeg
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-DEPEG-L2"
        assert result.priority == IntelligenceTriggerPriority.P2_MEDIUM

    def test_should_not_fire_when_usds_within_1_percent(self):
        """L2 trigger does not fire when depeg is within 1%."""
        trigger = SkyUSDSDepegLevel2Trigger({})
        data = {"protocol_health": {"sky": {"usds_price": 0.995}}}  # 0.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_l3_when_usds_depegs_above_2_percent(self):
        """L3 trigger fires when depeg exceeds 2%."""
        trigger = SkyUSDSDepegLevel3Trigger({})
        data = {"protocol_health": {"sky": {"usds_price": 0.97}}}  # 3% depeg
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-DEPEG-L3"
        assert result.priority == IntelligenceTriggerPriority.P1_HIGH

    def test_should_fire_l4_when_usds_depegs_above_5_percent(self):
        """L4 trigger fires when depeg exceeds 5%."""
        trigger = SkyUSDSDepegLevel4Trigger({})
        data = {"protocol_health": {"sky": {"usds_price": 0.94}}}  # 6% depeg
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-DEPEG-L4"
        assert result.priority == IntelligenceTriggerPriority.P0_CRITICAL

    def test_should_not_fire_l4_when_depeg_below_5_percent(self):
        """L4 trigger does not fire when depeg is below 5%."""
        trigger = SkyUSDSDepegLevel4Trigger({})
        data = {"protocol_health": {"sky": {"usds_price": 0.96}}}  # 4% depeg
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_handle_missing_data_gracefully(self):
        """Trigger handles missing data without crashing."""
        trigger = SkyUSDSDepegLevel2Trigger({})
        data = {}  # No protocol_health
        result = trigger.evaluate(data)
        assert result.fired is False  # Default price is 1.0, no depeg

    def test_should_use_custom_threshold_from_config(self):
        """Trigger uses custom threshold from config."""
        trigger = SkyUSDSDepegLevel2Trigger({"threshold_pct": 0.5})
        data = {"protocol_health": {"sky": {"usds_price": 0.994}}}  # 0.6% depeg
        result = trigger.evaluate(data)
        assert result.fired is True


class TestSkyTVLDropTriggers:
    """Tests for Sky TVL drop triggers."""

    def test_should_fire_when_tvl_drops_more_than_10_percent(self):
        """L2 trigger fires when TVL drops >10%."""
        trigger = SkyTVLDropLevel2Trigger({})
        data = {"protocol_health": {"sky": {"tvl_change_24h_pct": -15}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-TVL-L2"

    def test_should_not_fire_when_tvl_stable(self):
        """L2 trigger does not fire when TVL is stable."""
        trigger = SkyTVLDropLevel2Trigger({})
        data = {"protocol_health": {"sky": {"tvl_change_24h_pct": -5}}}
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_should_fire_l3_when_tvl_drops_more_than_25_percent(self):
        """L3 trigger fires when TVL drops >25%."""
        trigger = SkyTVLDropLevel3Trigger({})
        data = {"protocol_health": {"sky": {"tvl_change_24h_pct": -30}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "SKY-TVL-L3"


class TestSanctumTriggers:
    """Tests for Sanctum protocol triggers."""

    def test_should_fire_when_apy_drops_more_than_50_percent(self):
        """APY trigger fires when drop exceeds 50% (per spec threshold)."""
        trigger = SanctumAPYDropLevel2Trigger({})
        data = {"protocol_health": {"sanctum": {"current_apy": 4.0, "avg_apy_7d": 10.0}}}
        result = trigger.evaluate(data)
        assert result.fired is True  # 60% drop exceeds -50% threshold

    def test_should_not_fire_when_apy_stable(self):
        """APY trigger does not fire when APY is stable."""
        trigger = SanctumAPYDropLevel2Trigger({})
        data = {"protocol_health": {"sanctum": {"current_apy": 9.0, "avg_apy_7d": 10.0}}}
        result = trigger.evaluate(data)
        assert result.fired is False  # 10% drop

    def test_should_fire_lst_health_when_deviation_high(self):
        """LST health trigger fires on price deviation."""
        trigger = SanctumLSTHealthTrigger({})
        data = {"protocol_health": {"sanctum": {
            "lst_price": 1.05,
            "expected_lst_price": 1.0,
            "validator_health_score": 90
        }}}
        result = trigger.evaluate(data)
        assert result.fired is True  # 5% deviation


class TestJLPTriggers:
    """Tests for JLP protocol triggers."""

    def test_should_fire_when_utilization_above_85_percent(self):
        """L2 trigger fires when utilization >85%."""
        trigger = JLPUtilizationLevel2Trigger({})
        data = {"protocol_health": {"jlp": {"utilization_pct": 90}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "JLP-UTIL-L2"

    def test_should_fire_l3_when_utilization_above_95_percent(self):
        """L3 trigger fires when utilization >95%."""
        trigger = JLPUtilizationLevel3Trigger({})
        data = {"protocol_health": {"jlp": {"utilization_pct": 97}}}
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.trigger_id == "JLP-UTIL-L3"
        assert result.priority == IntelligenceTriggerPriority.P1_HIGH


class TestAaveTriggers:
    """Tests for Aave protocol triggers."""

    def test_should_fire_when_utilization_above_80_percent(self):
        """L2 trigger fires when utilization >80%."""
        trigger = AaveUtilizationLevel2Trigger({})
        data = {"protocol_health": {"aave": {"utilization_pct": 85}}}
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_should_fire_when_liquidation_volume_high(self):
        """Liquidation trigger fires on high volume."""
        trigger = AaveLiquidationRiskTrigger({})
        data = {"protocol_health": {"aave": {"liquidation_volume_24h_usd": 15_000_000}}}
        result = trigger.evaluate(data)
        assert result.fired is True


class TestTriggerMetadata:
    """Tests for trigger metadata and properties."""

    def test_all_triggers_have_category(self):
        """All triggers have a category."""
        triggers = [
            SkyUSDSDepegLevel2Trigger({}),
            SanctumAPYDropLevel2Trigger({}),
            JLPUtilizationLevel2Trigger({}),
            AaveUtilizationLevel2Trigger({}),
        ]
        for trigger in triggers:
            assert trigger.category == IntelligenceTriggerCategory.PROTOCOL_HEALTH

    def test_all_triggers_have_affected_strategies(self):
        """All triggers list affected strategies."""
        triggers = [
            SkyUSDSDepegLevel2Trigger({}),
            SanctumAPYDropLevel2Trigger({}),
            JLPUtilizationLevel2Trigger({}),
            AaveUtilizationLevel2Trigger({}),
        ]
        for trigger in triggers:
            assert len(trigger.affected_strategies) > 0
