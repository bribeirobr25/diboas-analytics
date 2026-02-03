"""Gate 2 Completeness Checker - Ensures all strategies have results."""
from typing import Any, Dict, List

from src.validators.gate2.gate2_analytics_validator import (
    Gate2ValidationIssue, Gate2ValidationSeverity
)


class Gate2CompletenessChecker:
    """Check that all 10 strategies have complete results."""

    EXPECTED_STRATEGIES = set(range(1, 11))
    REQUIRED_METRICS = [
        "var_95", "cvar_99", "sharpe_ratio",
        "max_drawdown", "median_return", "probability_of_loss"
    ]

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def check(self, data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Check completeness of all analytics outputs."""
        issues = []

        # Check Battle Test
        issues.extend(self._check_battle_test(data.get("battle_test", {})))

        # Check Monte Carlo
        issues.extend(self._check_monte_carlo(data.get("monte_carlo", {})))

        # Check Risk Metrics
        issues.extend(self._check_risk_metrics(data.get("risk_metrics", {})))

        return issues

    def _check_battle_test(self, bt_data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Check Battle Test completeness."""
        issues = []
        strategies = bt_data.get("strategies", {})

        actual = {int(s) for s in strategies.keys()}
        missing = self.EXPECTED_STRATEGIES - actual

        for strategy_id in missing:
            issues.append(Gate2ValidationIssue(
                code="G2-CMP-001",
                severity=Gate2ValidationSeverity.ERROR,
                message=f"Missing Battle Test results for strategy {strategy_id}",
                field=f"battle_test.strategies.{strategy_id}",
                remediation=f"Run Battle Test for strategy {strategy_id}"
            ))

        return issues

    def _check_monte_carlo(self, mc_data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Check Monte Carlo completeness."""
        issues = []
        strategies = mc_data.get("strategies", {})

        actual = {int(s) for s in strategies.keys()}
        missing = self.EXPECTED_STRATEGIES - actual

        for strategy_id in missing:
            issues.append(Gate2ValidationIssue(
                code="G2-CMP-002",
                severity=Gate2ValidationSeverity.ERROR,
                message=f"Missing Monte Carlo results for strategy {strategy_id}",
                field=f"monte_carlo.strategies.{strategy_id}",
                remediation=f"Run Monte Carlo for strategy {strategy_id}"
            ))

        return issues

    def _check_risk_metrics(self, rm_data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Check Risk Metrics completeness."""
        issues = []
        strategies = rm_data.get("strategies", {})

        # Check all strategies present
        actual = {int(s) for s in strategies.keys()}
        missing = self.EXPECTED_STRATEGIES - actual

        for strategy_id in missing:
            issues.append(Gate2ValidationIssue(
                code="G2-CMP-003",
                severity=Gate2ValidationSeverity.ERROR,
                message=f"Missing Risk Metrics for strategy {strategy_id}",
                field=f"risk_metrics.strategies.{strategy_id}",
                remediation=f"Calculate risk metrics for strategy {strategy_id}"
            ))

        # Check all required metrics for each strategy
        for strategy_id, metrics in strategies.items():
            for metric in self.REQUIRED_METRICS:
                if metric not in metrics or metrics[metric] is None:
                    issues.append(Gate2ValidationIssue(
                        code="G2-CMP-004",
                        severity=Gate2ValidationSeverity.ERROR,
                        message=f"Missing {metric} for strategy {strategy_id}",
                        field=f"risk_metrics.strategies.{strategy_id}.{metric}",
                        remediation=f"Calculate {metric} for strategy {strategy_id}"
                    ))

        return issues
