"""
Estate wallet triggers - Monitor large legacy holdings.

Track movements from known estate wallets:
- Mt. Gox: ~141K BTC held from 2014 hack
- FTX: Bankruptcy estate distributions
- Government seizures: Silk Road, ransomware, etc.

NOTE: Actual wallet addresses are sensitive data.
DataAccessPolicy restricts estate data to internal tier only.
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


# All strategies affected by large market movements
ALL_STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@TriggerRegistry.register("estate_movement_info")
class EstateMovementInfoTrigger(IntelligenceTriggerBase):
    """Estate wallet movement >$10M (Info level)."""

    @property
    def trigger_id(self) -> str:
        return "EST-MOV-INFO"

    @property
    def trigger_name(self) -> str:
        return "Estate Movement Detected"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.ESTATE_WALLET

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P3_INFO

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.INTERNAL_ONLY

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        wallet_activity = data.get("wallet_activity", {})
        estate_data = wallet_activity.get("estate", {})

        movement_usd = estate_data.get("movement_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 10_000_000)  # $10M
        fired = movement_usd > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=movement_usd,
            metadata={
                "movement_24h_usd": movement_usd,
                "source": estate_data.get("source"),  # e.g., "mt_gox", "ftx"
                "direction": estate_data.get("direction"),  # "inflow" or "outflow"
            },
        )


@TriggerRegistry.register("estate_movement_l2")
class EstateMovementLevel2Trigger(IntelligenceTriggerBase):
    """Estate wallet movement >$50M (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "EST-MOV-L2"

    @property
    def trigger_name(self) -> str:
        return "Significant Estate Movement"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.ESTATE_WALLET

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
        estate_data = wallet_activity.get("estate", {})

        movement_usd = estate_data.get("movement_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 50_000_000)  # $50M
        fired = movement_usd > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=movement_usd,
            metadata={
                "movement_24h_usd": movement_usd,
                "source": estate_data.get("source"),
                "direction": estate_data.get("direction"),
                "exchange_destination": estate_data.get("exchange_destination"),
            },
        )


@TriggerRegistry.register("estate_movement_l3")
class EstateMovementLevel3Trigger(IntelligenceTriggerBase):
    """Estate wallet movement >$100M (Warning level - potential market impact)."""

    @property
    def trigger_id(self) -> str:
        return "EST-MOV-L3"

    @property
    def trigger_name(self) -> str:
        return "Major Estate Movement Warning"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.ESTATE_WALLET

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        wallet_activity = data.get("wallet_activity", {})
        estate_data = wallet_activity.get("estate", {})

        movement_usd = estate_data.get("movement_24h_usd", 0)
        threshold = self.config.get("threshold_usd", 100_000_000)  # $100M
        fired = movement_usd > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=movement_usd,
            metadata={
                "movement_24h_usd": movement_usd,
                "source": estate_data.get("source"),
                "direction": estate_data.get("direction"),
                "exchange_destination": estate_data.get("exchange_destination"),
                "warning": "Large estate movement may cause market volatility",
            },
        )
