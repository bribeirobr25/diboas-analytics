"""Gate 2 Coherence Checker - Cross-metric consistency."""
from typing import Any, Dict, List

from src.validators.gate2.gate2_analytics_validator import (
    Gate2ValidationIssue, Gate2ValidationSeverity
)


class Gate2CoherenceChecker:
    """Check that related metrics are internally consistent."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.historical_change_threshold = self.config.get(
            "historical_change_threshold", 0.50
        )

    def check(self, data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Run all coherence checks."""
        issues = []

        risk_metrics = data.get("risk_metrics", {}).get("strategies", {})
        battle_test = data.get("battle_test", {}).get("strategies", {})

        for strategy_id, rm_data in risk_metrics.items():
            bt_data = battle_test.get(str(strategy_id), {})

            issues.extend(self._check_sharpe_prob_loss(strategy_id, rm_data))
            issues.extend(self._check_drawdown_consistency(strategy_id, rm_data, bt_data))

        return issues

    def _check_sharpe_prob_loss(
        self,
        strategy_id: str,
        rm_data: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """High Sharpe should correlate with low probability of loss."""
        issues = []

        sharpe = rm_data.get("sharpe_ratio")
        prob_loss = rm_data.get("probability_of_loss")

        if sharpe is not None and prob_loss is not None:
            # High positive Sharpe with high loss probability is suspicious
            if sharpe > 2 and prob_loss > 0.3:
                issues.append(Gate2ValidationIssue(
                    code="G2-COH-001",
                    severity=Gate2ValidationSeverity.WARNING,
                    message=f"High Sharpe with high loss probability for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}",
                    actual_value=f"Sharpe={sharpe}, P(loss)={prob_loss}",
                    expected_value="High Sharpe typically means lower P(loss)",
                    remediation="Verify calculations are using consistent data"
                ))

            # Negative Sharpe should correlate with high loss probability
            if sharpe < -1 and prob_loss < 0.2:
                issues.append(Gate2ValidationIssue(
                    code="G2-COH-002",
                    severity=Gate2ValidationSeverity.WARNING,
                    message=f"Negative Sharpe with low loss probability for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}",
                    actual_value=f"Sharpe={sharpe}, P(loss)={prob_loss}",
                    expected_value="Negative Sharpe typically means higher P(loss)",
                    remediation="Verify calculations are using consistent data"
                ))

        return issues

    def _check_drawdown_consistency(
        self,
        strategy_id: str,
        rm_data: Dict[str, Any],
        bt_data: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Risk Metrics max_dd should be consistent with Battle Test scenarios."""
        issues = []

        rm_max_dd = rm_data.get("max_drawdown")

        # Get worst drawdown from Battle Test scenarios
        scenarios = bt_data.get("scenarios", {})
        bt_max_dd = 0
        for scenario_name, scenario_data in scenarios.items():
            scenario_dd = scenario_data.get("max_drawdown", 0)
            bt_max_dd = max(bt_max_dd, scenario_dd)

        if rm_max_dd is not None and bt_max_dd > 0:
            # Risk metrics drawdown should be at least as bad as worst scenario
            if rm_max_dd < bt_max_dd * 0.5:
                issues.append(Gate2ValidationIssue(
                    code="G2-COH-003",
                    severity=Gate2ValidationSeverity.WARNING,
                    message=f"Max drawdown inconsistency for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}.max_drawdown",
                    actual_value=f"Risk Metrics={rm_max_dd}%, Battle Test worst={bt_max_dd}%",
                    expected_value="Risk Metrics max_dd >= Battle Test worst case",
                    remediation="Verify drawdown calculations use same methodology"
                ))

        return issues
