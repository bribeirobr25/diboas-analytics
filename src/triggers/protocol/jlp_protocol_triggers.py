"""
JLP (Jupiter LP) Protocol triggers - Utilization monitoring.

JLP is the liquidity provider pool for Jupiter. These triggers monitor:
- Utilization rates (high utilization = withdrawal risk)
- Pool health metrics
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


# Strategies using JLP yields
JLP_AFFECTED_STRATEGIES = [8, 9, 10]


@TriggerRegistry.register("jlp_utilization_l2")
class JLPUtilizationLevel2Trigger(IntelligenceTriggerBase):
    """JLP utilization >85% (Caution level)."""

    @property
    def trigger_id(self) -> str:
        return "JLP-UTIL-L2"

    @property
    def trigger_name(self) -> str:
        return "JLP High Utilization Caution"

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
        return JLP_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        jlp_data = protocol_health.get("jlp", {})

        utilization_pct = jlp_data.get("utilization_pct", 0)
        threshold = self.config.get("threshold_pct", 85.0)
        fired = utilization_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(utilization_pct, 2),
            metadata={
                "utilization_pct": utilization_pct,
                "total_assets": jlp_data.get("total_assets"),
                "borrowed_assets": jlp_data.get("borrowed_assets"),
            },
        )


@TriggerRegistry.register("jlp_utilization_l3")
class JLPUtilizationLevel3Trigger(IntelligenceTriggerBase):
    """JLP utilization >95% (Warning level - withdrawal risk)."""

    @property
    def trigger_id(self) -> str:
        return "JLP-UTIL-L3"

    @property
    def trigger_name(self) -> str:
        return "JLP Critical Utilization Warning"

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
        return JLP_AFFECTED_STRATEGIES

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        jlp_data = protocol_health.get("jlp", {})

        utilization_pct = jlp_data.get("utilization_pct", 0)
        threshold = self.config.get("threshold_pct", 95.0)
        fired = utilization_pct > threshold

        return self._create_result(
            fired=fired,
            threshold=threshold,
            actual_value=round(utilization_pct, 2),
            metadata={
                "utilization_pct": utilization_pct,
                "total_assets": jlp_data.get("total_assets"),
                "borrowed_assets": jlp_data.get("borrowed_assets"),
                "warning": "High utilization may impact withdrawals",
            },
        )


@TriggerRegistry.register("jlp_apy_l2")
class JLPAPYLevel2Trigger(IntelligenceTriggerBase):
    """JLP APY drop >40% from 7d average."""

    @property
    def trigger_id(self) -> str:
        return "JLP-APY-L2"

    @property
    def trigger_name(self) -> str:
        return "JLP APY Drop Caution"

    @property
    def category(self) -> IntelligenceTriggerCategory:
        return IntelligenceTriggerCategory.PROTOCOL_HEALTH

    @property
    def priority(self) -> IntelligenceTriggerPriority:
        return IntelligenceTriggerPriority.P1_HIGH

    @property
    def action(self) -> IntelligenceTriggerAction:
        return IntelligenceTriggerAction.PERFORMANCE_ALERT

    @property
    def affected_strategies(self) -> List[int]:
        return [6, 8, 10]  # JLP strategies

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        jlp_data = protocol_health.get("jlp", {})

        current_apy = jlp_data.get("current_apy", 0)
        avg_7d_apy = jlp_data.get("avg_7d_apy", current_apy)

        if avg_7d_apy > 0:
            apy_change_pct = ((current_apy - avg_7d_apy) / avg_7d_apy) * 100
        else:
            apy_change_pct = 0

        threshold = self.config.get("threshold_pct", -40)
        fired = apy_change_pct < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"JLP APY drop > {abs(threshold)}% from 7d avg",
            threshold=threshold,
            actual_value=round(apy_change_pct, 2),
            metadata={
                "current_apy": current_apy,
                "avg_7d_apy": avg_7d_apy,
                "apy_change_pct": apy_change_pct
            }
        )


@TriggerRegistry.register("jlp_tvl_l3")
class JLPTVLLevel3Trigger(IntelligenceTriggerBase):
    """JLP TVL drop >30% in 24h."""

    @property
    def trigger_id(self) -> str:
        return "JLP-TVL-L3"

    @property
    def trigger_name(self) -> str:
        return "JLP TVL Drop Warning"

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
        return [6, 8, 10]

    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        protocol_health = data.get("protocol_health", {})
        jlp_data = protocol_health.get("jlp", {})
        tvl_change_24h = jlp_data.get("tvl_change_24h_pct", 0)

        threshold = self.config.get("threshold_pct", -30)
        fired = tvl_change_24h < threshold

        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"JLP TVL drop > {abs(threshold)}% in 24h",
            threshold=threshold,
            actual_value=tvl_change_24h,
            metadata={"tvl_change_24h_pct": tvl_change_24h}
        )
