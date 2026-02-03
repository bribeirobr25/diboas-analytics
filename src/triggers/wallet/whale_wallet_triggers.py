"""
Whale wallet triggers - Monitor large holder activity.

Track movements from known whale wallets:
- Large single movements (>$25M)
- Accumulation patterns
- Distribution patterns (potential selling pressure)

NOTE: Specific wallet addresses are restricted.
DataAccessPolicy limits whale data based on client tier.
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


# All strategies affected by whale movements
ALL_STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@TriggerRegistry.register("whale_movement_l2")
class WhaleMovementLevel2Trigger(IntelligenceTriggerBase):
    """Whale wallet movement >$25M (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "WHALE-MOV-L2"

    @property
    def trigger_name(self) -> str:
        return "Whale Movement Detected"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.WHALE_ACTIVITY

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.SMART_MONEY_INSIGHT

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        wallet_activity = data.get("wallet_activity", {})
        whale_data = wallet_activity.get("whale", {})

        movement_usd = whale_data.get("largest_movement_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 25_000_000)  # $25M
        fired = movement_usd > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=movement_usd,
            metadata={
                "largest_movement_24h_usd": movement_usd,
                "total_whale_volume_24h": whale_data.get("total_volume_24h_usd"),
                "movement_count": whale_data.get("movement_count"),
            },
        )


@TriggerRegistry.register("whale_accumulation")
class WhaleAccumulationTrigger(IntelligenceTriggerBase):
    """Whale accumulation pattern detected (bullish signal)."""

    @property
    def trigger_id(self) -> str:
        return "WHALE-ACC-L2"

    @property
    def trigger_name(self) -> str:
        return "Whale Accumulation Detected"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.WHALE_ACTIVITY

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.SMART_MONEY_INSIGHT

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        wallet_activity = data.get("wallet_activity", {})
        whale_data = wallet_activity.get("whale", {})

        # Net flow positive = accumulation
        net_flow_usd = whale_data.get("net_flow_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 50_000_000)  # $50M net inflow
        fired = net_flow_usd > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=net_flow_usd,
            metadata={
                "net_flow_24h_usd": net_flow_usd,
                "inflow_usd": whale_data.get("inflow_24h_usd"),
                "outflow_usd": whale_data.get("outflow_24h_usd"),
                "signal": "bullish" if fired else "neutral",
            },
        )


@TriggerRegistry.register("whale_distribution")
class WhaleDistributionTrigger(IntelligenceTriggerBase):
    """Whale distribution pattern detected (bearish signal - potential selling)."""

    @property
    def trigger_id(self) -> str:
        return "WHALE-DIST-L2"

    @property
    def trigger_name(self) -> str:
        return "Whale Distribution Detected"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.WHALE_ACTIVITY

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.SMART_MONEY_INSIGHT

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        wallet_activity = data.get("wallet_activity", {})
        whale_data = wallet_activity.get("whale", {})

        # Net flow negative = distribution (selling pressure)
        net_flow_usd = whale_data.get("net_flow_24h_usd", 0)
        threshold = self.config.get("threshold_usd", -50_000_000)  # $50M net outflow
        fired = net_flow_usd < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=net_flow_usd,
            metadata={
                "net_flow_24h_usd": net_flow_usd,
                "inflow_usd": whale_data.get("inflow_24h_usd"),
                "outflow_usd": whale_data.get("outflow_24h_usd"),
                "exchange_inflow_pct": whale_data.get("exchange_inflow_pct"),
                "signal": "bearish" if fired else "neutral",
                "warning": "Whales may be selling - monitor for price pressure",
            },
        )
