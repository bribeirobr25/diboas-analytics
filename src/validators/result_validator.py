"""
Validation rules for Battle Test and Monte Carlo results.

Implements CV-01 through CV-07 validation rules.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging

from config.settings import GAS_COSTS, MINIMUM_DEPOSITS, VALIDATION_TOLERANCE
from src.domain.simulation import BattleTestResult, MonteCarloResult

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Validation rule severity levels."""
    CRITICAL = 'critical'
    WARNING = 'warning'
    INFO = 'info'


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    rule_id: str
    passed: bool
    severity: Severity
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'rule_id': self.rule_id,
            'passed': self.passed,
            'severity': self.severity.value,
            'message': self.message,
            'value': self.value,
            'threshold': self.threshold
        }


class ResultValidator:
    """
    Validate Battle Test and Monte Carlo results.

    Rules:
    - CV-01: Portfolio value never negative (Critical)
    - CV-02: Drawdown between 0% and 100% (Critical)
    - CV-03: Stable strategies have 0% max drawdown (Warning)
    - CV-04: Final value >= deposited for stable strategies (Warning)
    - CV-05: Return % matches calculation (Critical)
    - CV-06: Net return > 0 after gas costs (Critical)
    - CV-07: Initial deposit >= per-strategy minimum (Warning)
    """

    # Stable strategies (0% crypto)
    STABLE_STRATEGIES = [1, 3, 5, 7, 9]

    def __init__(self):
        self.gas_costs = GAS_COSTS
        self.minimum_deposits = MINIMUM_DEPOSITS
        self.tolerance = VALIDATION_TOLERANCE

    def validate_cv01(self, portfolio_values: list[float]) -> ValidationResult:
        """
        CV-01: Portfolio value never negative.

        Severity: Critical
        """
        if not portfolio_values:
            return ValidationResult(
                rule_id='CV-01',
                passed=False,
                severity=Severity.CRITICAL,
                message='No portfolio values provided',
                value=None,
                threshold=0
            )

        min_value = min(portfolio_values)
        passed = min_value >= 0

        return ValidationResult(
            rule_id='CV-01',
            passed=passed,
            severity=Severity.CRITICAL,
            message='Portfolio value went negative' if not passed else 'OK',
            value=min_value,
            threshold=0
        )

    def validate_cv02(self, max_drawdown: float) -> ValidationResult:
        """
        CV-02: Drawdown between 0% and 100%.

        Severity: Critical
        """
        passed = 0 <= max_drawdown <= 100

        return ValidationResult(
            rule_id='CV-02',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Invalid drawdown: {max_drawdown:.2f}%' if not passed else 'OK',
            value=max_drawdown,
            threshold=100
        )

    def validate_cv03(self, strategy_id: int, max_drawdown: float) -> ValidationResult:
        """
        CV-03: Stable strategies (0% crypto) have 0% max drawdown.

        Severity: Warning (stable strategies should have no price exposure)
        """
        if strategy_id not in self.STABLE_STRATEGIES:
            return ValidationResult(
                rule_id='CV-03',
                passed=True,
                severity=Severity.INFO,
                message='Not a stable strategy, rule not applicable'
            )

        # Allow small tolerance for floating point errors
        passed = max_drawdown < 0.01  # Less than 0.01% is effectively 0

        return ValidationResult(
            rule_id='CV-03',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Stable strategy has {max_drawdown:.2f}% drawdown' if not passed else 'OK',
            value=max_drawdown,
            threshold=0
        )

    def validate_cv04(
        self,
        strategy_id: int,
        deposited: float,
        final_value: float
    ) -> ValidationResult:
        """
        CV-04: Final value >= deposited for stable strategies.

        Severity: Warning (stable strategies should never lose principal)
        """
        if strategy_id not in self.STABLE_STRATEGIES:
            return ValidationResult(
                rule_id='CV-04',
                passed=True,
                severity=Severity.INFO,
                message='Not a stable strategy, rule not applicable'
            )

        passed = final_value >= deposited

        return ValidationResult(
            rule_id='CV-04',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Stable strategy lost money: ${deposited:.2f} -> ${final_value:.2f}' if not passed else 'OK',
            value=final_value,
            threshold=deposited
        )

    def validate_cv05(
        self,
        deposited: float,
        final_value: float,
        reported_return: float
    ) -> ValidationResult:
        """
        CV-05: Return % matches calculation.

        Severity: Critical (data integrity)
        """
        if deposited <= 0:
            return ValidationResult(
                rule_id='CV-05',
                passed=False,
                severity=Severity.CRITICAL,
                message='Deposited amount must be positive',
                value=0,
                threshold=0
            )

        calculated_return = (final_value - deposited) / deposited * 100
        diff = abs(calculated_return - reported_return)
        passed = diff < self.tolerance

        return ValidationResult(
            rule_id='CV-05',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Return mismatch: calculated {calculated_return:.4f}% vs reported {reported_return:.4f}%' if not passed else 'OK',
            value=diff,
            threshold=self.tolerance
        )

    def validate_cv06(
        self,
        gross_return: float,
        tx_count: int,
        chain: str = 'arbitrum'
    ) -> ValidationResult:
        """
        CV-06: Net return > 0 after gas costs.

        Severity: Critical (user must profit)
        """
        gas_per_tx = self.gas_costs.get(chain, 0.30)
        total_gas = tx_count * gas_per_tx
        net_return = gross_return - total_gas
        passed = net_return > 0

        return ValidationResult(
            rule_id='CV-06',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Negative net return after ${total_gas:.2f} gas' if not passed else 'OK',
            value=net_return,
            threshold=0
        )

    def validate_cv07(
        self,
        strategy_id: int,
        initial_deposit: float
    ) -> ValidationResult:
        """
        CV-07: Initial deposit >= per-strategy minimum.

        Severity: Warning (below minimum is not economical)
        """
        min_required = self.minimum_deposits.get(strategy_id, 50)
        passed = initial_deposit >= min_required

        return ValidationResult(
            rule_id='CV-07',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Deposit ${initial_deposit:.2f} below minimum ${min_required}' if not passed else 'OK',
            value=initial_deposit,
            threshold=min_required
        )

    def validate_battle_test_result(
        self,
        result: BattleTestResult,
        initial_deposit: float = None
    ) -> list[ValidationResult]:
        """
        Run all applicable validations on a Battle Test result.

        Args:
            result: BattleTestResult to validate
            initial_deposit: Initial deposit (for CV-07)

        Returns:
            List of ValidationResult
        """
        validations = []

        # CV-01: Portfolio values (if available)
        if result.daily_values:
            validations.append(self.validate_cv01(result.daily_values))
        else:
            # Check final value at minimum
            validations.append(self.validate_cv01([result.final_value]))

        # CV-02: Drawdown range
        validations.append(self.validate_cv02(result.max_drawdown_pct))

        # CV-03: Stable strategy drawdown
        validations.append(self.validate_cv03(result.strategy_id, result.max_drawdown_pct))

        # CV-04: Stable strategy profit
        validations.append(self.validate_cv04(
            result.strategy_id,
            result.deposited,
            result.final_value
        ))

        # CV-05: Return calculation
        validations.append(self.validate_cv05(
            result.deposited,
            result.final_value,
            result.return_pct
        ))

        # CV-06: Gas costs (estimate tx count based on days)
        # Assume 2 tx per month (deposit + rebalance)
        months = result.days // 30
        tx_count = months * 2 + 1  # Initial deposit
        validations.append(self.validate_cv06(
            result.profit,
            tx_count,
            'arbitrum'  # Primary chain
        ))

        # CV-07: Minimum deposit
        if initial_deposit:
            validations.append(self.validate_cv07(result.strategy_id, initial_deposit))

        return validations

    def validate_monte_carlo_result(
        self,
        result: MonteCarloResult
    ) -> list[ValidationResult]:
        """
        Run validations on a Monte Carlo result.

        Args:
            result: MonteCarloResult to validate

        Returns:
            List of ValidationResult
        """
        validations = []

        # CV-01: Check for negative values in distribution
        if result.final_values is not None:
            min_value = float(result.final_values.min())
            validations.append(ValidationResult(
                rule_id='CV-01',
                passed=min_value >= 0,
                severity=Severity.CRITICAL,
                message=f'Simulation produced negative value: {min_value:.2f}' if min_value < 0 else 'OK',
                value=min_value,
                threshold=0
            ))

        # CV-02: Drawdown range
        validations.append(self.validate_cv02(result.p95_max_drawdown))

        # CV-03: Stable strategy - check probability of loss
        if result.strategy_id in self.STABLE_STRATEGIES:
            passed = result.prob_any_loss < 1.0  # Less than 1% prob of loss
            validations.append(ValidationResult(
                rule_id='CV-03',
                passed=passed,
                severity=Severity.WARNING,
                message=f'Stable strategy has {result.prob_any_loss:.1f}% probability of loss' if not passed else 'OK',
                value=result.prob_any_loss,
                threshold=1.0
            ))

        # CV-05: Return calculation sanity check
        calculated_return = (result.mean_final - result.total_deposited) / result.total_deposited * 100
        diff = abs(calculated_return - result.mean_return)
        validations.append(ValidationResult(
            rule_id='CV-05',
            passed=diff < 1.0,  # Allow 1% tolerance for Monte Carlo
            severity=Severity.CRITICAL,
            message=f'Return mismatch: {calculated_return:.2f}% vs {result.mean_return:.2f}%' if diff >= 1.0 else 'OK',
            value=diff,
            threshold=1.0
        ))

        return validations


class ValidationReport:
    """Generate validation report from results."""

    def __init__(self, validations: list[ValidationResult]):
        self.validations = validations

    @property
    def all_passed(self) -> bool:
        """Check if all validations passed."""
        return all(v.passed for v in self.validations)

    @property
    def critical_failures(self) -> list[ValidationResult]:
        """Get critical failures."""
        return [v for v in self.validations if not v.passed and v.severity == Severity.CRITICAL]

    @property
    def warnings(self) -> list[ValidationResult]:
        """Get warnings."""
        return [v for v in self.validations if not v.passed and v.severity == Severity.WARNING]

    @property
    def status(self) -> str:
        """Get overall status."""
        if self.critical_failures:
            return 'FAILED'
        elif self.warnings:
            return 'PASS_WITH_WARNINGS'
        else:
            return 'PASSED'

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'status': self.status,
            'total_rules': len(self.validations),
            'passed': sum(1 for v in self.validations if v.passed),
            'failed': sum(1 for v in self.validations if not v.passed),
            'critical_failures': len(self.critical_failures),
            'warnings': len(self.warnings),
            'validations': [v.to_dict() for v in self.validations]
        }
