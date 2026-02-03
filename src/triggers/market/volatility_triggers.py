"""
Volatility triggers - VIX and crypto volatility monitoring.

Monitor market-wide volatility indicators:
- VIX (fear gauge) spikes
- Crypto-specific volatility measures
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


# All strategies affected by macro volatility
ALL_STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@TriggerRegistry.register("macro_vix_spike_l2")
class VIXSpikeLevel2Trigger(IntelligenceTriggerBase):
    """VIX >30 (Caution level - elevated fear)."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-VIX-L2"

    @property
    def trigger_name(self) -> str:
        return "VIX Elevated Caution"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MACRO_INDICATOR

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
        macro_indicators = data.get("macro_indicators", {})
        vix_value = macro_indicators.get("vix", 0)

        threshold = self.config.get("threshold", 30)
        fired = vix_value > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(vix_value, 2),
            metadata={
                "vix_value": vix_value,
                "vix_change_1d": macro_indicators.get("vix_change_1d"),
            },
        )


@TriggerRegistry.register("macro_vix_spike_l3")
class VIXSpikeLevel3Trigger(IntelligenceTriggerBase):
    """VIX >40 (Warning level - high fear)."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-VIX-L3"

    @property
    def trigger_name(self) -> str:
        return "VIX High Fear Warning"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MACRO_INDICATOR

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
        macro_indicators = data.get("macro_indicators", {})
        vix_value = macro_indicators.get("vix", 0)

        threshold = self.config.get("threshold", 40)
        fired = vix_value > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(vix_value, 2),
            metadata={
                "vix_value": vix_value,
                "vix_change_1d": macro_indicators.get("vix_change_1d"),
                "warning": "Extreme market fear - consider risk reduction",
            },
        )


@TriggerRegistry.register("crypto_volatility_spike")
class CryptoVolatilityTrigger(IntelligenceTriggerBase):
    """Crypto implied volatility spike (>2 std dev from 30d mean)."""

    @property
    def trigger_id(self) -> str:
        return "MKT-CVOL-L2"

    @property
    def trigger_name(self) -> str:
        return "Crypto Volatility Spike"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MARKET_CONDITION

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P2_MEDIUM

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PERFORMANCE_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        macro_indicators = data.get("macro_indicators", {})
        crypto_vol = macro_indicators.get("crypto_volatility", {})

        current_vol = crypto_vol.get("current", 0)
        mean_30d = crypto_vol.get("mean_30d", current_vol or 1)
        std_30d = crypto_vol.get("std_30d", 1)

        # Calculate z-score
        if std_30d == 0:
            z_score = 0
        else:
            z_score = (current_vol - mean_30d) / std_30d

        threshold = self.config.get("threshold_std", 2.0)
        fired = z_score > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(z_score, 2),
            metadata={
                "current_volatility": current_vol,
                "mean_30d": mean_30d,
                "std_30d": std_30d,
                "z_score": z_score,
            },
        )
