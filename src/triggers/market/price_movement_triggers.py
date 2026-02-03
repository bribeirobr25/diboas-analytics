"""
Price movement triggers - Major crypto price drops.

Monitor significant price declines in major cryptocurrencies:
- BTC drops (10%, 20% thresholds)
- ETH drops (15% threshold)
- SOL drops (20%, 30% thresholds)
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


# Most strategies have some crypto exposure
CRYPTO_AFFECTED_STRATEGIES = [3, 4, 5, 6, 7, 8, 9, 10]
SOL_AFFECTED_STRATEGIES = [2, 4, 6, 8, 9, 10]


@TriggerRegistry.register("mkt_btc_drop_l3")
class BTCDropLevel3Trigger(IntelligenceTriggerBase):
    """BTC price drop >10% in 24h (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-BTC-L3"

    @property
    def trigger_name(self) -> str:
        return "BTC Significant Drop"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return CRYPTO_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        market_prices = data.get("market_prices", {})
        btc_data = market_prices.get("btc", {})

        change_24h_pct = btc_data.get("change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -10.0)
        fired = change_24h_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(change_24h_pct, 2),
            metadata={
                "btc_price": btc_data.get("price"),
                "change_24h_pct": change_24h_pct,
                "volume_24h": btc_data.get("volume_24h"),
            },
        )


@TriggerRegistry.register("mkt_btc_drop_l4")
class BTCDropLevel4Trigger(IntelligenceTriggerBase):
    """BTC price drop >20% in 24h (Critical level)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-BTC-L4"

    @property
    def trigger_name(self) -> str:
        return "BTC Crash Alert"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P0_CRITICAL

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return CRYPTO_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        market_prices = data.get("market_prices", {})
        btc_data = market_prices.get("btc", {})

        change_24h_pct = btc_data.get("change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -20.0)
        fired = change_24h_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(change_24h_pct, 2),
            metadata={
                "btc_price": btc_data.get("price"),
                "change_24h_pct": change_24h_pct,
                "volume_24h": btc_data.get("volume_24h"),
            },
        )


@TriggerRegistry.register("mkt_eth_drop_l3")
class ETHDropLevel3Trigger(IntelligenceTriggerBase):
    """ETH price drop >15% in 24h (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-ETH-L3"

    @property
    def trigger_name(self) -> str:
        return "ETH Significant Drop"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return CRYPTO_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        market_prices = data.get("market_prices", {})
        eth_data = market_prices.get("eth", {})

        change_24h_pct = eth_data.get("change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -15.0)
        fired = change_24h_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(change_24h_pct, 2),
            metadata={
                "eth_price": eth_data.get("price"),
                "change_24h_pct": change_24h_pct,
                "volume_24h": eth_data.get("volume_24h"),
            },
        )


@TriggerRegistry.register("mkt_sol_drop_l3")
class SOLDropLevel3Trigger(IntelligenceTriggerBase):
    """SOL price drop >20% in 24h (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-SOL-L3"

    @property
    def trigger_name(self) -> str:
        return "SOL Significant Drop"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return SOL_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        market_prices = data.get("market_prices", {})
        sol_data = market_prices.get("sol", {})

        change_24h_pct = sol_data.get("change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -20.0)
        fired = change_24h_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(change_24h_pct, 2),
            metadata={
                "sol_price": sol_data.get("price"),
                "change_24h_pct": change_24h_pct,
                "volume_24h": sol_data.get("volume_24h"),
            },
        )


@TriggerRegistry.register("mkt_sol_drop_l4")
class SOLDropLevel4Trigger(IntelligenceTriggerBase):
    """SOL price drop >30% in 24h (Critical level)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-SOL-L4"

    @property
    def trigger_name(self) -> str:
        return "SOL Crash Alert"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P0_CRITICAL

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return SOL_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        market_prices = data.get("market_prices", {})
        sol_data = market_prices.get("sol", {})

        change_24h_pct = sol_data.get("change_24h_pct", 0)
        threshold = self.config.get("threshold_pct", -30.0)
        fired = change_24h_pct < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(change_24h_pct, 2),
            metadata={
                "sol_price": sol_data.get("price"),
                "change_24h_pct": change_24h_pct,
                "volume_24h": sol_data.get("volume_24h"),
            },
        )


@TriggerRegistry.register("market_cap_l3")
class MarketCapLevel3Trigger(IntelligenceTriggerBase):
    """Broad crypto market cap drop - Warning level."""

    @property
    def trigger_id(self) -> str:
        return "MKT-CAP-L3"

    @property
    def trigger_name(self) -> str:
        return "Broad Market Crash Warning"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P0_CRITICAL

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.CRISIS_TEMPLATE

    @property
    def affected_strategies(self) -> List[int]:
        return list(range(1, 11))  # All strategies

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        prices = data.get("prices", {})

        # Check if multiple major assets are down significantly
        btc_change = prices.get("btc_change_24h_pct", 0)
        eth_change = prices.get("eth_change_24h_pct", 0)
        sol_change = prices.get("sol_change_24h_pct", 0)

        # Average of major crypto changes
        avg_change = (btc_change + eth_change + sol_change) / 3

        threshold = self.config.get("threshold_pct", -15)
        fired = avg_change < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"Broad market avg drop > {abs(threshold)}%",
            threshold=threshold,
            actual_value=round(avg_change, 2),
            metadata={
                "btc_change_24h_pct": btc_change,
                "eth_change_24h_pct": eth_change,
                "sol_change_24h_pct": sol_change,
                "avg_change_pct": avg_change
            }
        )
