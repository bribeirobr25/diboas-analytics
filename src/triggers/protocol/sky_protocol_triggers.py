"""
Sky Protocol triggers - USDS depeg and TVL monitoring.

USDS is the Sky stablecoin. These triggers monitor for:
- Depeg events (price deviation from $1.00)
- TVL drops (indicating capital flight)
"""

from typing import Any, Dict, List

from src.triggers.base import (
    IntelligenceTriggerBase,
    IntelligenceTriggerResult,
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
    IntelligenceTriggerAction,
)
from src.registries.trigger_registry import TriggerRegistry


# Strategies using Sky SSR yield
SKY_AFFECTED_STRATEGIES = [1, 3, 5, 7, 9]


@TriggerRegistry.register("sky_usds_depeg_l2")
class SkyUSDSDepegLevel2Trigger(IntelligenceTriggerBase):
    """USDS depeg >1% (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "SKY-DEPEG-L2"

    @property
    def trigger_name(self) -> str:
        return "USDS Depeg Caution"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PROTOCOL_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        usds_price = protocol_health.get("sky", {}).get("usds_price", 1.0)

        depeg_pct = abs(usds_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 1.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usds_price": usds_price, "depeg_pct": depeg_pct},
        )


@TriggerRegistry.register("sky_usds_depeg_l3")
class SkyUSDSDepegLevel3Trigger(IntelligenceTriggerBase):
    """USDS depeg >2% (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "SKY-DEPEG-L3"

    @property
    def trigger_name(self) -> str:
        return "USDS Depeg Warning"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        usds_price = protocol_health.get("sky", {}).get("usds_price", 1.0)

        depeg_pct = abs(usds_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 2.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usds_price": usds_price, "depeg_pct": depeg_pct},
        )


@TriggerRegistry.register("sky_usds_depeg_l4")
class SkyUSDSDepegLevel4Trigger(IntelligenceTriggerBase):
    """USDS depeg >5% (Critical level)."""

    @property
    def trigger_id(self) -> str:
        return "SKY-DEPEG-L4"

    @property
    def trigger_name(self) -> str:
        return "USDS Depeg Critical"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P0_CRITICAL

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        usds_price = protocol_health.get("sky", {}).get("usds_price", 1.0)

        depeg_pct = abs(usds_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 5.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usds_price": usds_price, "depeg_pct": depeg_pct},
        )


@TriggerRegistry.register("sky_tvl_drop_l2")
class SkyTVLDropLevel2Trigger(IntelligenceTriggerBase):
    """Sky TVL drop >10% in 24h (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "SKY-TVL-L2"

    @property
    def trigger_name(self) -> str:
        return "Sky TVL Drop Caution"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PROTOCOL_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sky_data = protocol_health.get("sky", {})

        tvl_change_pct = sky_data.get("tvl_change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -10.0)
        fired = tvl_change_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(tvl_change_pct, 2),
            metadata={
                "current_tvl": sky_data.get("tvl"),
                "tvl_change_pct": tvl_change_pct,
            },
        )


@TriggerRegistry.register("sky_tvl_drop_l3")
class SkyTVLDropLevel3Trigger(IntelligenceTriggerBase):
    """Sky TVL drop >25% in 24h (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "SKY-TVL-L3"

    @property
    def trigger_name(self) -> str:
        return "Sky TVL Drop Warning"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sky_data = protocol_health.get("sky", {})

        tvl_change_pct = sky_data.get("tvl_change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -25.0)
        fired = tvl_change_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(tvl_change_pct, 2),
            metadata={
                "current_tvl": sky_data.get("tvl"),
                "tvl_change_pct": tvl_change_pct,
            },
        )


@TriggerRegistry.register("sky_buffer_l2")
class SkyBufferLevel2Trigger(IntelligenceTriggerBase):
    """Sky surplus buffer below threshold."""

    @property
    def trigger_id(self) -> str:
        return "SKY-BUF-L2"

    @property
    def trigger_name(self) -> str:
        return "Sky Surplus Buffer Low"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PROTOCOL_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return SKY_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sky_data = protocol_health.get("sky", {})
        surplus_buffer = sky_data.get("surplus_buffer_usd", float('inf'))

        threshold = self.config.get("threshold_usd", 50_000_000)  # $50M
        fired = surplus_buffer < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"Sky surplus buffer < ${threshold/1_000_000:.0f}M",
            threshold=threshold,
            actual_value=surplus_buffer,
            metadata={"surplus_buffer_usd": surplus_buffer}
        )
