"""Gate 2 Bounds Validator - Check values within valid bounds."""
import math
from typing import Any, Dict, List

from src.validators.gate2.gate2_analytics_validator import (
    Gate2ValidationIssue, Gate2ValidationSeverity
)


class Gate2BoundsValidator:
    """Validate that metric values are within valid bounds."""

    # Bounds from VALIDATION_GATES_CTO_HANDOFF_v2.md Section 4.3
    BOUNDS = {
        "var_95": {"min": 0, "max": 100, "unit": "%"},
        "cvar_99": {"min": 0, "max": 100, "unit": "%"},
        "sharpe_ratio": {"min": -5, "max": 10, "unit": "ratio"},  # Negative allowed
        "max_drawdown": {"min": 0, "max": 100, "unit": "%"},
        "probability_of_loss": {"min": 0, "max": 1, "unit": "probability"},
        "median_return": {"min": -100, "max": 500, "unit": "%"},
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def validate(self, data: Dict[str, Any]) -> List[Gate2ValidationIssue]:
        """Validate all metric bounds."""
        issues = []

        risk_metrics = data.get("risk_metrics", {}).get("strategies", {})

        for strategy_id, metrics in risk_metrics.items():
            # Check bounds
            issues.extend(self._check_bounds(strategy_id, metrics))

            # Check for invalid values (NaN, Inf)
            issues.extend(self._check_invalid_values(strategy_id, metrics))

        return issues

    def _check_bounds(
        self,
        strategy_id: str,
        metrics: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Check metric values against bounds."""
        issues = []

        for metric, bounds in self.BOUNDS.items():
            value = metrics.get(metric)

            if value is None:
                continue

            if value < bounds["min"]:
                issues.append(Gate2ValidationIssue(
                    code="G2-BND-001",
                    severity=Gate2ValidationSeverity.ERROR,
                    message=f"{metric} below minimum for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}.{metric}",
                    actual_value=value,
                    expected_value=f">= {bounds['min']} {bounds['unit']}",
                    remediation=f"Review {metric} calculation"
                ))

            if value > bounds["max"]:
                # Use ERROR for critical metrics, WARNING for others
                severity = Gate2ValidationSeverity.ERROR if metric in [
                    "var_95", "probability_of_loss"
                ] else Gate2ValidationSeverity.WARNING

                issues.append(Gate2ValidationIssue(
                    code="G2-BND-002",
                    severity=severity,
                    message=f"{metric} above maximum for strategy {strategy_id}",
                    field=f"risk_metrics.strategies.{strategy_id}.{metric}",
                    actual_value=value,
                    expected_value=f"<= {bounds['max']} {bounds['unit']}",
                    remediation=f"Review {metric} calculation (value seems extreme)"
                ))

        return issues

    def _check_invalid_values(
        self,
        strategy_id: str,
        metrics: Dict[str, Any]
    ) -> List[Gate2ValidationIssue]:
        """Check for NaN and Inf values."""
        issues = []

        for metric, value in metrics.items():
            if value is None:
                continue

            try:
                if math.isnan(value):
                    issues.append(Gate2ValidationIssue(
                        code="G2-INV-001",
                        severity=Gate2ValidationSeverity.ERROR,
                        message=f"NaN value in {metric} for strategy {strategy_id}",
                        field=f"risk_metrics.strategies.{strategy_id}.{metric}",
                        actual_value="NaN",
                        remediation="Fix calculation (check for 0/0 or sqrt of negative)"
                    ))
                elif math.isinf(value):
                    issues.append(Gate2ValidationIssue(
                        code="G2-INV-002",
                        severity=Gate2ValidationSeverity.ERROR,
                        message=f"Infinite value in {metric} for strategy {strategy_id}",
                        field=f"risk_metrics.strategies.{strategy_id}.{metric}",
                        actual_value="Inf",
                        remediation="Fix calculation (check for division by zero)"
                    ))
            except TypeError:
                pass  # Non-numeric values handled elsewhere

        return issues
