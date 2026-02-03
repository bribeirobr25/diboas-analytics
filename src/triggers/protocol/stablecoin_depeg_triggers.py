"""
USDC and USDT depeg monitoring triggers.

These stablecoins are used in Aave and Compound protocols, affecting
strategies that have allocations to those lending protocols.

Thresholds (per handoff specification):
- L2: >1% depeg (P2_MEDIUM) - Caution
- L3: >2% depeg (P1_HIGH) - Warning
- L4: >5% depeg (P0_CRITICAL) - Crisis

Data source: CoinGecko collector (usdc_close, usdt_close columns)
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


# Strategies using USDC-exposed protocols (Aave, Compound)
# Source: strategies.json allocations as of 2026-02-03
# Strategies 1, 3, 5, 7, 9 use Aave and/or Compound
USDC_AFFECTED_STRATEGIES = [1, 3, 5, 7, 9]
USDT_AFFECTED_STRATEGIES = [1, 3, 5, 7, 9]


# =============================================================================
# USDC Depeg Triggers
# =============================================================================


@TriggerRegistry.register("usdc_depeg_l2")
class USDCDepegLevel2Trigger(IntelligenceTriggerBase):
    """USDC depeg >1% (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "USDC-DEPEG-L2"

    @property
    def trigger_name(self) -> str:
        return "USDC Depeg Caution"

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
        return USDC_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """
        Evaluate USDC price for >1% depeg.

        Looks for usdc_price in:
        1. protocol_health.usdc.price
        2. stablecoin_prices.usdc
        3. crypto_prices.usdc_close
        """
        usdc_price = self._get_usdc_price(data)

        depeg_pct = abs(usdc_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 1.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdc_price": usdc_price, "depeg_pct": depeg_pct},
        )

    def _get_usdc_price(self, data: Dict[str, Any]) -> float:
        """Extract USDC price from various data structures."""
        # Try protocol_health structure
        protocol_health = data.get("protocol_health", {})
        if "usdc" in protocol_health:
            return protocol_health["usdc"].get("price", 1.0)

        # Try stablecoin_prices structure
        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdc" in stablecoin_prices:
            return stablecoin_prices["usdc"]

        # Try crypto_prices structure (from CoinGecko collector)
        crypto_prices = data.get("crypto_prices", {})
        if "usdc_close" in crypto_prices:
            return crypto_prices["usdc_close"]

        # Default to $1.00 (no depeg)
        return 1.0


@TriggerRegistry.register("usdc_depeg_l3")
class USDCDepegLevel3Trigger(IntelligenceTriggerBase):
    """USDC depeg >2% (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "USDC-DEPEG-L3"

    @property
    def trigger_name(self) -> str:
        return "USDC Depeg Warning"

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
        return USDC_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """Evaluate USDC price for >2% depeg."""
        usdc_price = self._get_usdc_price(data)

        depeg_pct = abs(usdc_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 2.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdc_price": usdc_price, "depeg_pct": depeg_pct},
        )

    def _get_usdc_price(self, data: Dict[str, Any]) -> float:
        """Extract USDC price from various data structures."""
        protocol_health = data.get("protocol_health", {})
        if "usdc" in protocol_health:
            return protocol_health["usdc"].get("price", 1.0)

        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdc" in stablecoin_prices:
            return stablecoin_prices["usdc"]

        crypto_prices = data.get("crypto_prices", {})
        if "usdc_close" in crypto_prices:
            return crypto_prices["usdc_close"]

        return 1.0


@TriggerRegistry.register("usdc_depeg_l4")
class USDCDepegLevel4Trigger(IntelligenceTriggerBase):
    """USDC depeg >5% (Critical level)."""

    @property
    def trigger_id(self) -> str:
        return "USDC-DEPEG-L4"

    @property
    def trigger_name(self) -> str:
        return "USDC Depeg Critical"

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
        return USDC_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """Evaluate USDC price for >5% depeg (crisis level)."""
        usdc_price = self._get_usdc_price(data)

        depeg_pct = abs(usdc_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 5.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdc_price": usdc_price, "depeg_pct": depeg_pct},
        )

    def _get_usdc_price(self, data: Dict[str, Any]) -> float:
        """Extract USDC price from various data structures."""
        protocol_health = data.get("protocol_health", {})
        if "usdc" in protocol_health:
            return protocol_health["usdc"].get("price", 1.0)

        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdc" in stablecoin_prices:
            return stablecoin_prices["usdc"]

        crypto_prices = data.get("crypto_prices", {})
        if "usdc_close" in crypto_prices:
            return crypto_prices["usdc_close"]

        return 1.0


# =============================================================================
# USDT Depeg Triggers
# =============================================================================


@TriggerRegistry.register("usdt_depeg_l2")
class USDTDepegLevel2Trigger(IntelligenceTriggerBase):
    """USDT depeg >1% (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "USDT-DEPEG-L2"

    @property
    def trigger_name(self) -> str:
        return "USDT Depeg Caution"

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
        return USDT_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """Evaluate USDT price for >1% depeg."""
        usdt_price = self._get_usdt_price(data)

        depeg_pct = abs(usdt_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 1.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdt_price": usdt_price, "depeg_pct": depeg_pct},
        )

    def _get_usdt_price(self, data: Dict[str, Any]) -> float:
        """Extract USDT price from various data structures."""
        protocol_health = data.get("protocol_health", {})
        if "usdt" in protocol_health:
            return protocol_health["usdt"].get("price", 1.0)

        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdt" in stablecoin_prices:
            return stablecoin_prices["usdt"]

        crypto_prices = data.get("crypto_prices", {})
        if "usdt_close" in crypto_prices:
            return crypto_prices["usdt_close"]

        return 1.0


@TriggerRegistry.register("usdt_depeg_l3")
class USDTDepegLevel3Trigger(IntelligenceTriggerBase):
    """USDT depeg >2% (Warning level)."""

    @property
    def trigger_id(self) -> str:
        return "USDT-DEPEG-L3"

    @property
    def trigger_name(self) -> str:
        return "USDT Depeg Warning"

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
        return USDT_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """Evaluate USDT price for >2% depeg."""
        usdt_price = self._get_usdt_price(data)

        depeg_pct = abs(usdt_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 2.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdt_price": usdt_price, "depeg_pct": depeg_pct},
        )

    def _get_usdt_price(self, data: Dict[str, Any]) -> float:
        """Extract USDT price from various data structures."""
        protocol_health = data.get("protocol_health", {})
        if "usdt" in protocol_health:
            return protocol_health["usdt"].get("price", 1.0)

        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdt" in stablecoin_prices:
            return stablecoin_prices["usdt"]

        crypto_prices = data.get("crypto_prices", {})
        if "usdt_close" in crypto_prices:
            return crypto_prices["usdt_close"]

        return 1.0


@TriggerRegistry.register("usdt_depeg_l4")
class USDTDepegLevel4Trigger(IntelligenceTriggerBase):
    """USDT depeg >5% (Critical level)."""

    @property
    def trigger_id(self) -> str:
        return "USDT-DEPEG-L4"

    @property
    def trigger_name(self) -> str:
        return "USDT Depeg Critical"

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
        return USDT_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """Evaluate USDT price for >5% depeg (crisis level)."""
        usdt_price = self._get_usdt_price(data)

        depeg_pct = abs(usdt_price - 1.0) * 100
        threshold = self.config.get("threshold_pct", 5.0)
        fired = depeg_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(depeg_pct, 3),
            metadata={"usdt_price": usdt_price, "depeg_pct": depeg_pct},
        )

    def _get_usdt_price(self, data: Dict[str, Any]) -> float:
        """Extract USDT price from various data structures."""
        protocol_health = data.get("protocol_health", {})
        if "usdt" in protocol_health:
            return protocol_health["usdt"].get("price", 1.0)

        stablecoin_prices = data.get("stablecoin_prices", {})
        if "usdt" in stablecoin_prices:
            return stablecoin_prices["usdt"]

        crypto_prices = data.get("crypto_prices", {})
        if "usdt_close" in crypto_prices:
            return crypto_prices["usdt_close"]

        return 1.0
