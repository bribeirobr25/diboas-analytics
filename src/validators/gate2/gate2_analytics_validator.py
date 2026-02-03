"""
Gate 2 Analytics Validator - Validates QR Board engine outputs.

Validates Battle Test, Monte Carlo, and Risk Metrics outputs
before they enter the Intelligence layer (Layer 4).
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Gate2ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Gate2ValidationStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class Gate2ValidationIssue:
    code: str
    severity: Gate2ValidationSeverity
    message: str
    field: Optional[str] = None
    actual_value: Any = None
    expected_value: Any = None
    remediation: str = ""


@dataclass
class Gate2ValidationResult:
    status: Gate2ValidationStatus
    issues: List[Gate2ValidationIssue] = field(default_factory=list)
    strategies_validated: int = 0
    metrics_validated: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_ms: int = 0

    @property
    def errors(self) -> List[Gate2ValidationIssue]:
        return [i for i in self.issues if i.severity == Gate2ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[Gate2ValidationIssue]:
        return [i for i in self.issues if i.severity == Gate2ValidationSeverity.WARNING]

    @property
    def passed(self) -> bool:
        return self.status != Gate2ValidationStatus.FAIL

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)


class Gate2AnalyticsValidator:
    """
    Gate 2: Analytics Validation (QR Board)

    Validates:
    1. Completeness - All 10 strategies have results
    2. Value Bounds - No impossible values
    3. Statistical Sanity - Distributions make sense
    4. Cross-Metric Coherence - Related metrics are consistent
    """

    EXPECTED_STRATEGIES = set(range(1, 11))
    REQUIRED_METRICS = [
        "var_95", "cvar_99", "sharpe_ratio",
        "max_drawdown", "median_return", "probability_of_loss"
    ]

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # Import here to avoid circular imports
        from src.validators.gate2.gate2_completeness_checker import Gate2CompletenessChecker
        from src.validators.gate2.gate2_bounds_validator import Gate2BoundsValidator
        from src.validators.gate2.gate2_statistical_sanity import Gate2StatisticalSanityChecker
        from src.validators.gate2.gate2_coherence_checker import Gate2CoherenceChecker

        self.completeness_checker = Gate2CompletenessChecker(self.config)
        self.bounds_validator = Gate2BoundsValidator(self.config)
        self.sanity_checker = Gate2StatisticalSanityChecker(self.config)
        self.coherence_checker = Gate2CoherenceChecker(self.config)

    def validate(
        self,
        battle_test_results: Dict[str, Any],
        monte_carlo_results: Dict[str, Any],
        risk_metrics: Dict[str, Any]
    ) -> Gate2ValidationResult:
        """Validate all analytics engine outputs."""
        start_time = datetime.utcnow()
        issues: List[Gate2ValidationIssue] = []

        # Package data for sub-validators
        data = {
            "battle_test": battle_test_results,
            "monte_carlo": monte_carlo_results,
            "risk_metrics": risk_metrics
        }

        # Run all validation checks
        try:
            issues.extend(self.completeness_checker.check(data))
            issues.extend(self.bounds_validator.validate(data))
            issues.extend(self.sanity_checker.check(data))
            issues.extend(self.coherence_checker.check(data))
        except Exception as e:
            logger.error(f"Gate 2 validation error: {e}")
            issues.append(Gate2ValidationIssue(
                code="G2-ERR-001",
                severity=Gate2ValidationSeverity.ERROR,
                message=f"Validation error: {str(e)}",
                remediation="Check input data format"
            ))

        # Determine status
        has_errors = any(i.severity == Gate2ValidationSeverity.ERROR for i in issues)
        has_warnings = any(i.severity == Gate2ValidationSeverity.WARNING for i in issues)

        if has_errors:
            status = Gate2ValidationStatus.FAIL
        elif has_warnings:
            status = Gate2ValidationStatus.WARN
        else:
            status = Gate2ValidationStatus.PASS

        duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return Gate2ValidationResult(
            status=status,
            issues=issues,
            strategies_validated=len(risk_metrics.get("strategies", {})),
            metrics_validated=len(self.REQUIRED_METRICS),
            duration_ms=duration_ms
        )
