"""
Yield curve triggers - Monitor recession indicators.

Track US Treasury yield curve movements:
- Inversion (2Y-10Y spread negative) - recession signal
- Steep curve (spread widening) - growth signal
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


# All strategies affected by macro conditions
ALL_STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@TriggerRegistry.register("macro_yield_curve_inversion")
class YieldCurveInversionTrigger(IntelligenceTriggerBase):
    """Yield curve inversion (2Y-10Y spread negative) - recession signal."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-YC-INV"

    @property
    def trigger_name(self) -> str:
        return "Yield Curve Inversion"

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
        yields = macro_indicators.get("treasury_yields", {})

        yield_2y = yields.get("2y", 0)
        yield_10y = yields.get("10y", 0)
        spread = yield_10y - yield_2y

        threshold = self.config.get("threshold", 0)  # Inversion when < 0
        fired = spread < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(spread, 3),
            metadata={
                "yield_2y": yield_2y,
                "yield_10y": yield_10y,
                "spread_2y_10y": spread,
                "signal": "recession_warning" if fired else "normal",
            },
        )


@TriggerRegistry.register("macro_yield_curve_steep")
class YieldCurveSteepTrigger(IntelligenceTriggerBase):
    """Yield curve steepening (spread >100bp) - potential growth signal."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-YC-STEEP"

    @property
    def trigger_name(self) -> str:
        return "Yield Curve Steepening"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.MACRO_INDICATOR

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P3_INFO

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.SMART_MONEY_INSIGHT

    @property
    def affected_strategies(self) -> List[int]:
        return ALL_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        macro_indicators = data.get("macro_indicators", {})
        yields = macro_indicators.get("treasury_yields", {})

        yield_2y = yields.get("2y", 0)
        yield_10y = yields.get("10y", 0)
        spread = yield_10y - yield_2y

        threshold = self.config.get("threshold", 1.0)  # 100bp = 1%
        fired = spread > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(spread, 3),
            metadata={
                "yield_2y": yield_2y,
                "yield_10y": yield_10y,
                "spread_2y_10y": spread,
                "signal": "growth_expected" if fired else "normal",
            },
        )
