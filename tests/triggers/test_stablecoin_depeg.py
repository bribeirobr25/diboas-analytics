"""
Tests for USDC and USDT stablecoin depeg triggers.

Tests cover:
- All 6 triggers (USDC L2/L3/L4, USDT L2/L3/L4)
- Trigger firing at correct thresholds
- Trigger NOT firing below thresholds
- Correct priority levels
- Correct affected strategies
- Multiple data source formats
"""

import pytest
from src.triggers.protocol.stablecoin_depeg_triggers import (
    USDCDepegLevel2Trigger,
    USDCDepegLevel3Trigger,
    USDCDepegLevel4Trigger,
    USDTDepegLevel2Trigger,
    USDTDepegLevel3Trigger,
    USDTDepegLevel4Trigger,
    USDC_AFFECTED_STRATEGIES,
    USDT_AFFECTED_STRATEGIES,
)
from src.triggers.base import (
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
    IntelligenceTriggerAction,
)
from src.registries.trigger_registry import TriggerRegistry


class TestUSDCDepegLevel2Trigger:
    """Tests for USDC >1% depeg (Caution)."""

    @pytest.fixture
    def trigger(self):
        return USDCDepegLevel2Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDC-DEPEG-L2"

    def test_trigger_name(self, trigger):
        assert trigger.trigger_name == "USDC Depeg Caution"

    def test_priority_is_p2_medium(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P2_MEDIUM

    def test_category_is_protocol_health(self, trigger):
        assert trigger.category == IntelligenceTriggerCategory.PROTOCOL_HEALTH

    def test_action_is_protocol_alert(self, trigger):
        assert trigger.action == IntelligenceTriggerAction.PROTOCOL_ALERT

    def test_affected_strategies(self, trigger):
        assert trigger.affected_strategies == [1, 3, 5, 7, 9]

    def test_fires_when_depeg_above_1_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.985}}  # 1.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is True
        assert result.actual_value == 1.5

    def test_does_not_fire_when_depeg_below_1_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.995}}  # 0.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_fires_on_upward_depeg(self, trigger):
        data = {"stablecoin_prices": {"usdc": 1.015}}  # 1.5% up
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_reads_from_protocol_health_structure(self, trigger):
        data = {"protocol_health": {"usdc": {"price": 0.98}}}  # 2% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_reads_from_crypto_prices_structure(self, trigger):
        data = {"crypto_prices": {"usdc_close": 0.98}}  # 2% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_defaults_to_1_when_no_price_data(self, trigger):
        data = {}
        result = trigger.evaluate(data)
        assert result.fired is False
        assert result.actual_value == 0.0


class TestUSDCDepegLevel3Trigger:
    """Tests for USDC >2% depeg (Warning)."""

    @pytest.fixture
    def trigger(self):
        return USDCDepegLevel3Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDC-DEPEG-L3"

    def test_priority_is_p1_high(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P1_HIGH

    def test_action_is_crisis_template(self, trigger):
        assert trigger.action == IntelligenceTriggerAction.CRISIS_TEMPLATE

    def test_fires_when_depeg_above_2_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.975}}  # 2.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_does_not_fire_when_depeg_below_2_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.985}}  # 1.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is False


class TestUSDCDepegLevel4Trigger:
    """Tests for USDC >5% depeg (Critical)."""

    @pytest.fixture
    def trigger(self):
        return USDCDepegLevel4Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDC-DEPEG-L4"

    def test_priority_is_p0_critical(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P0_CRITICAL

    def test_action_is_crisis_template(self, trigger):
        assert trigger.action == IntelligenceTriggerAction.CRISIS_TEMPLATE

    def test_fires_when_depeg_above_5_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.94}}  # 6% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_does_not_fire_when_depeg_below_5_percent(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.96}}  # 4% depeg
        result = trigger.evaluate(data)
        assert result.fired is False


class TestUSDTDepegLevel2Trigger:
    """Tests for USDT >1% depeg (Caution)."""

    @pytest.fixture
    def trigger(self):
        return USDTDepegLevel2Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDT-DEPEG-L2"

    def test_trigger_name(self, trigger):
        assert trigger.trigger_name == "USDT Depeg Caution"

    def test_priority_is_p2_medium(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P2_MEDIUM

    def test_affected_strategies(self, trigger):
        assert trigger.affected_strategies == [1, 3, 5, 7, 9]

    def test_fires_when_depeg_above_1_percent(self, trigger):
        data = {"stablecoin_prices": {"usdt": 0.985}}  # 1.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_does_not_fire_when_depeg_below_1_percent(self, trigger):
        data = {"stablecoin_prices": {"usdt": 0.995}}  # 0.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is False

    def test_reads_from_crypto_prices_structure(self, trigger):
        data = {"crypto_prices": {"usdt_close": 0.98}}  # 2% depeg
        result = trigger.evaluate(data)
        assert result.fired is True


class TestUSDTDepegLevel3Trigger:
    """Tests for USDT >2% depeg (Warning)."""

    @pytest.fixture
    def trigger(self):
        return USDTDepegLevel3Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDT-DEPEG-L3"

    def test_priority_is_p1_high(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P1_HIGH

    def test_fires_when_depeg_above_2_percent(self, trigger):
        data = {"stablecoin_prices": {"usdt": 0.975}}  # 2.5% depeg
        result = trigger.evaluate(data)
        assert result.fired is True


class TestUSDTDepegLevel4Trigger:
    """Tests for USDT >5% depeg (Critical)."""

    @pytest.fixture
    def trigger(self):
        return USDTDepegLevel4Trigger({})

    def test_trigger_id(self, trigger):
        assert trigger.trigger_id == "USDT-DEPEG-L4"

    def test_priority_is_p0_critical(self, trigger):
        assert trigger.priority == IntelligenceTriggerPriority.P0_CRITICAL

    def test_fires_when_depeg_above_5_percent(self, trigger):
        data = {"stablecoin_prices": {"usdt": 0.94}}  # 6% depeg
        result = trigger.evaluate(data)
        assert result.fired is True


class TestTriggerRegistration:
    """Test that all triggers are properly registered."""

    def test_usdc_depeg_l2_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdc_depeg_l2")

    def test_usdc_depeg_l3_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdc_depeg_l3")

    def test_usdc_depeg_l4_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdc_depeg_l4")

    def test_usdt_depeg_l2_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdt_depeg_l2")

    def test_usdt_depeg_l3_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdt_depeg_l3")

    def test_usdt_depeg_l4_registered(self):
        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("usdt_depeg_l4")

    def test_can_instantiate_from_registry(self):
        registry = TriggerRegistry.get_instance()
        trigger = registry.get("usdc_depeg_l4", {})
        assert trigger.trigger_id == "USDC-DEPEG-L4"
        assert trigger.priority == IntelligenceTriggerPriority.P0_CRITICAL


class TestAffectedStrategies:
    """Test the affected strategies constant."""

    def test_usdc_affected_strategies_correct(self):
        assert USDC_AFFECTED_STRATEGIES == [1, 3, 5, 7, 9]

    def test_usdt_affected_strategies_correct(self):
        assert USDT_AFFECTED_STRATEGIES == [1, 3, 5, 7, 9]


class TestMetadata:
    """Test that trigger results include proper metadata."""

    @pytest.fixture
    def trigger(self):
        return USDCDepegLevel2Trigger({})

    def test_metadata_includes_price(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.985}}
        result = trigger.evaluate(data)
        assert "usdc_price" in result.metadata
        assert result.metadata["usdc_price"] == 0.985

    def test_metadata_includes_depeg_pct(self, trigger):
        data = {"stablecoin_prices": {"usdc": 0.985}}
        result = trigger.evaluate(data)
        assert "depeg_pct" in result.metadata
        assert abs(result.metadata["depeg_pct"] - 1.5) < 0.001


class TestConfigurableThreshold:
    """Test that thresholds can be configured."""

    def test_can_override_threshold_via_config(self):
        # Configure trigger to fire at 0.5% instead of 1%
        trigger = USDCDepegLevel2Trigger({"threshold_pct": 0.5})
        data = {"stablecoin_prices": {"usdc": 0.993}}  # 0.7% depeg
        result = trigger.evaluate(data)
        assert result.fired is True

    def test_default_threshold_used_when_not_configured(self):
        trigger = USDCDepegLevel2Trigger({})
        data = {"stablecoin_prices": {"usdc": 0.993}}  # 0.7% depeg
        result = trigger.evaluate(data)
        assert result.fired is False  # Below default 1% threshold
