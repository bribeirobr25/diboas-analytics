"""
Sanctum Protocol triggers - LST (Liquid Staking Token) monitoring.

Sanctum provides liquid staking on Solana. These triggers monitor:
- APY drops (indicating reduced staking rewards)
- LST health (de-peg risk, validator issues)
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


# Strategies using Sanctum LST yields
SANCTUM_AFFECTED_STRATEGIES = [2, 4, 6]


@TriggerRegistry.register("sanctum_apy_drop_l2")
class SanctumAPYDropLevel2Trigger(IntelligenceTriggerBase):
    """Sanctum APY drop >30% vs 7-day average (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "SANCTUM-APY-L2"

    @property
    def trigger_name(self) -> str:
        return "Sanctum APY Drop"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PERFORMANCE_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return SANCTUM_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sanctum_data = protocol_health.get("sanctum", {})

        current_apy = sanctum_data.get("current_apy", 0)
        avg_apy_7d = sanctum_data.get("avg_apy_7d", current_apy or 1)

        # Avoid division by zero
        if avg_apy_7d == 0:
            apy_change_pct = 0
        else:
            apy_change_pct = ((current_apy - avg_apy_7d) / avg_apy_7d) * 100

        threshold = self.config.get("threshold_pct", -50.0)  # Changed from -30% to match spec
        fired = apy_change_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(apy_change_pct, 2),
            metadata={
                "current_apy": current_apy,
                "avg_apy_7d": avg_apy_7d,
                "apy_change_pct": apy_change_pct,
            },
        )


@TriggerRegistry.register("sanctum_lst_health")
class SanctumLSTHealthTrigger(IntelligenceTriggerBase):
    """Sanctum LST health concerns (price deviation or validator issues)."""

    @property
    def trigger_id(self) -> str:
        return "SANCTUM-LST-L2"

    @property
    def trigger_name(self) -> str:
        return "Sanctum LST Health Alert"

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
        return SANCTUM_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sanctum_data = protocol_health.get("sanctum", {})

        # Check LST price deviation from expected value
        lst_price = sanctum_data.get("lst_price", 1.0)
        expected_price = sanctum_data.get("expected_lst_price", 1.0)

        if expected_price == 0:
            price_deviation_pct = 0
        else:
            price_deviation_pct = abs((lst_price - expected_price) / expected_price) * 100

        # Check validator health score
        validator_health = sanctum_data.get("validator_health_score", 100)

        threshold_deviation = self.config.get("threshold_deviation_pct", 2.0)
        threshold_health = self.config.get("threshold_health_score", 80)

        fired = price_deviation_pct > threshold_deviation or validator_health < threshold_health

        return self._create_result(
            fired=fired,
            threshold={"deviation": threshold_deviation, "health": threshold_health},
            actual_value={"deviation": round(price_deviation_pct, 2), "health": validator_health},
            metadata={
                "lst_price": lst_price,
                "expected_price": expected_price,
                "price_deviation_pct": price_deviation_pct,
                "validator_health_score": validator_health,
            },
        )


@TriggerRegistry.register("sanctum_tvl_l3")
class SanctumTVLLevel3Trigger(IntelligenceTriggerBase):
    """Sanctum TVL drop >20% in 24h - Warning level."""

    @property
    def trigger_id(self) -> str:
        return "SAN-TVL-L3"

    @property
    def trigger_name(self) -> str:
        return "Sanctum TVL Drop Warning"

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
        return [2, 4, 6, 8, 10]  # Sanctum strategies

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sanctum_data = protocol_health.get("sanctum", {})
        tvl_change_24h = sanctum_data.get("tvl_change_24h_pct", 0)

        threshold = self.config.get("threshold_pct", -20)
        fired = tvl_change_24h < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"Sanctum TVL drop > {abs(threshold)}% in 24h",
            threshold=threshold,
            actual_value=tvl_change_24h,
            metadata={"tvl_change_24h_pct": tvl_change_24h}
        )


@TriggerRegistry.register("sanctum_tvl_l4")
class SanctumTVLLevel4Trigger(IntelligenceTriggerBase):
    """Sanctum TVL drop >50% in 24h - Critical level."""

    @property
    def trigger_id(self) -> str:
        return "SAN-TVL-L4"

    @property
    def trigger_name(self) -> str:
        return "Sanctum TVL Drop Critical"

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
        return [2, 4, 6, 8, 10]

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        sanctum_data = protocol_health.get("sanctum", {})
        tvl_change_24h = sanctum_data.get("tvl_change_24h_pct", 0)

        threshold = self.config.get("threshold_pct", -50)
        fired = tvl_change_24h < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"Sanctum TVL drop > {abs(threshold)}% in 24h",
            threshold=threshold,
            actual_value=tvl_change_24h,
            metadata={"tvl_change_24h_pct": tvl_change_24h}
        )
