"""Gate 2 Statistical Sanity - Check statistical properties make sense."""
from typing import Any, Dict, List

from src.validators.gate2.gate2_analytics_validator import (
    Gate2ValidationIssue, Gate2ValidationSeverity
)


class Gate2StatisticalSanityChecker:
    """Check that statistical properties are internally consistent."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def check(self, data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Run all statistical sanity checks."""
        issues = []

        monte_carlo = data.get("monte_carlo", {}).get("strategies", {})
        risk_metrics = data.get("risk_metrics", {}).get("strategies", {})

        for strategy_id in risk_metrics.keys():
            mc_data = monte_carlo.get(str(strategy_id), {})
            rm_data = risk_metrics.get(str(strategy_id), {})

            issues.extend(self._check_percentile_ordering(strategy_id, mc_data))
            issues.extend(self._check_cvar_var_relationship(strategy_id, rm_data))
            issues.extend(self._check_risk_tier_alignment(strategy_id, rm_data))

        return issues

    def _check_percentile_ordering(
        self,
        strategy_id: str,
        mc_data: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Check that percentiles are properly ordered (P5 < P50 < P95)."""
        issues = []

        p5 = mc_data.get("percentile_5")
        p50 = mc_data.get("percentile_50")
        p95 = mc_data.get("percentile_95")

        if all(v is not None for v in [p5, p50, p95]):
            if not (p5 <= p50 <= p95):
                issues.append(Gate2ValidationIssue(
                    code="G2-STA-001",
                    severity=Gate2ValidationSeverity.ERROR,
                    message=f"Percentiles not ordered for strategy {strategy_id}",
                    field=f"monte_carlo.strategies.{strategy_id}",
                    actual_value=f"P5={p5}, P50={p50}, P95={p95}",
                    expected_value="P5 <= P50 <= P95",
                    remediation="Check Monte Carlo calculation"
                ))

        return issues

    def _check_cvar_var_relationship(
        self,
        strategy_id: str,
        rm_data: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Check that CVaR >= VaR (Expected Shortfall >= VaR)."""
        issues = []

        var_95 = rm_data.get("var_95")
        cvar_99 = rm_data.get("cvar_99")

        if var_95 is not None and cvar_99 is not None:
            # CVaR should be >= VaR (more extreme tail measure)
            # Both are expressed as positive loss percentages
            if cvar_99 < var_95 * 0.9:  # Allow some tolerance
                issues.append(Gate2ValidationIssue(
                    code="G2-STA-002",
                    severity=Gate2ValidationSeverity.WARNING,
                    message=f"CVaR < VaR for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}",
                    actual_value=f"VaR95={var_95}, CVaR99={cvar_99}",
                    expected_value="CVaR99 >= VaR95",
                    remediation="Verify tail risk calculations"
                ))

        return issues

    def _check_risk_tier_alignment(
        self,
        strategy_id: str,
        rm_data: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Check that risk metrics align with expected risk tier."""
        issues = []

        # Risk tiers from strategy definitions
        RISK_TIERS = {
            "1": "minimal", "2": "low", "3": "minimal", "4": "low-medium",
            "5": "minimal", "6": "medium", "7": "minimal", "8": "high",
            "9": "low", "10": "very-high"
        }

        tier = RISK_TIERS.get(str(strategy_id), "unknown")
        var_95 = rm_data.get("var_95", 0)

        # High risk strategies should have higher VaR
        if tier in ["high", "very-high"] and var_95 < 5:
            issues.append(Gate2ValidationIssue(
                code="G2-STA-003",
                severity=Gate2ValidationSeverity.WARNING,
                message=f"Low VaR for high-risk strategy {strategy_id}",
                field=f"risk_metrics.strategies.{strategy_id}.var_95",
                actual_value=var_95,
                expected_value=">= 5% for high-risk strategy",
                remediation="Verify risk tier alignment"
            ))

        return issues
