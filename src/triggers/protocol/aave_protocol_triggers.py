"""
Aave Protocol triggers - Lending protocol health monitoring.

Aave is a decentralized lending protocol. These triggers monitor:
- Utilization rates
- Liquidation risk
- Interest rate spikes
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


# Strategies that may use Aave for yield or hedging
AAVE_AFFECTED_STRATEGIES = [3, 5, 7, 9, 10]


@TriggerRegistry.register("aave_utilization_l2")
class AaveUtilizationLevel2Trigger(IntelligenceTriggerBase):
    """Aave pool utilization >80% (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "AAVE-UTIL-L2"

    @property
    def trigger_name(self) -> str:
        return "Aave High Utilization Caution"

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
        return AAVE_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        aave_data = protocol_health.get("aave", {})

        utilization_pct = aave_data.get("utilization_pct", 0)
        threshold = self.config.get("threshold_pct", 80.0)
        fired = utilization_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(utilization_pct, 2),
            metadata={
                "utilization_pct": utilization_pct,
                "supply_apy": aave_data.get("supply_apy"),
                "borrow_apy": aave_data.get("borrow_apy"),
            },
        )


@TriggerRegistry.register("aave_liquidation_risk")
class AaveLiquidationRiskTrigger(IntelligenceTriggerBase):
    """Aave protocol-wide liquidation risk elevated."""

    @property
    def trigger_id(self) -> str:
        return "AAVE-LIQ-L2"

    @property
    def trigger_name(self) -> str:
        return "Aave Liquidation Risk Alert"

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
        return AAVE_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        aave_data = protocol_health.get("aave", {})

        # Check if liquidation volume is elevated
        liquidation_volume_24h = aave_data.get("liquidation_volume_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 10_000_000)  # $10M
        fired = liquidation_volume_24h > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=liquidation_volume_24h,
            metadata={
                "liquidation_volume_24h_usd": liquidation_volume_24h,
                "at_risk_positions_usd": aave_data.get("at_risk_positions_usd"),
                "health_factor_avg": aave_data.get("health_factor_avg"),
            },
        )
