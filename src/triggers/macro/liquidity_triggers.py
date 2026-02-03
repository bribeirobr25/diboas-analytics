"""
Liquidity triggers - Monitor market liquidity conditions.

Track credit spreads and Fed liquidity:
- Credit spread widening (risk-off indicator)
- Fed balance sheet changes (liquidity impact)
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


# All strategies affected by liquidity conditions
ALL_STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@TriggerRegistry.register("macro_credit_spread_wide")
class CreditSpreadWideTrigger(IntelligenceTriggerBase):
    """Credit spreads widening >150bp (risk-off environment)."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-CS-L2"

    @property
    def trigger_name(self) -> str:
        return "Credit Spreads Widening"

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
        credit_data = macro_indicators.get("credit", {})

        # High yield spread over treasury (OAS)
        spread_bp = credit_data.get("hy_oas_bp", 0)
        threshold = self.config.get("threshold_bp", 150)  # 150 basis points
        fired = spread_bp > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=spread_bp,
            metadata={
                "hy_oas_bp": spread_bp,
                "ig_oas_bp": credit_data.get("ig_oas_bp"),
                "spread_change_1w": credit_data.get("spread_change_1w_bp"),
                "signal": "risk_off" if fired else "normal",
            },
        )


@TriggerRegistry.register("macro_fed_liquidity")
class FedLiquidityTrigger(IntelligenceTriggerBase):
    """Fed balance sheet contraction >$50B weekly (liquidity drain)."""

    @property
    def trigger_id(self) -> str:
        return "MACRO-FED-L2"

    @property
    def trigger_name(self) -> str:
        return "Fed Liquidity Contraction"

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
        fed_data = macro_indicators.get("fed", {})

        # Weekly change in balance sheet (negative = contraction)
        balance_change_b = fed_data.get("balance_sheet_change_weekly_b", 0)
        threshold = self.config.get("threshold_b", -50)  # -$50B
        fired = balance_change_b < threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=balance_change_b,
            metadata={
                "balance_sheet_change_weekly_b": balance_change_b,
                "total_balance_sheet_t": fed_data.get("total_balance_sheet_t"),
                "rrp_b": fed_data.get("reverse_repo_b"),
                "signal": "liquidity_drain" if fired else "normal",
            },
        )
