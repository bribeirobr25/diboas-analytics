"""
Validator Registry for result validation.

Wraps existing ResultValidator in a registry pattern for pluggable architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


class Validator(ABC):
    """
    Abstract base class for all validators.

    All validators must implement the validate() method.
    """

    @abstractmethod
    def validate(self, data: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate data and return results.

        Args:
            data: Data to validate (type depends on validator)
            config: Optional validation configuration

        Returns:
            Validation result (type depends on validator)
        """
        pass

    def get_name(self) -> str:
        """Get the validator name for logging."""
        return self.__class__.__name__


class ValidatorRegistry(Registry[Validator]):
    """
    Registry for validators.

    Usage:
        validator = ValidatorRegistry.get_instance().get("result_validator", {})
        report = validator.validate(battle_test_results)
    """
    pass


# =============================================================================
# Wrapped Implementations
# =============================================================================

@ValidatorRegistry.register("result_validator")
class ResultValidatorPlugin(Validator):
    """
    Wrapper for ResultValidator (CV-01 through CV-07).

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.validators.result_validator import ResultValidator
        self.config = config
        self._validator = ResultValidator()

    def validate(self, data: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate simulation results.

        Args:
            data: Can be:
                - BattleTestResult or list of BattleTestResult
                - MonteCarloResult or list of MonteCarloResult
                - Dict with 'type' key indicating result type
            config: Optional config with:
                - initial_deposit: For CV-07 validation

        Returns:
            ValidationReport or list of ValidationResult
        """
        from src.validators.result_validator import ValidationReport
        from src.domain.simulation import BattleTestResult, MonteCarloResult

        config = config or {}
        initial_deposit = config.get('initial_deposit')

        logger.info(f"Running validation on {type(data).__name__}")

        # Handle list of results
        if isinstance(data, list):
            all_validations = []
            for item in data:
                validations = self._validate_single(item, initial_deposit)
                all_validations.extend(validations)
            return ValidationReport(all_validations)

        # Handle single result
        validations = self._validate_single(data, initial_deposit)
        return ValidationReport(validations)

    def _validate_single(self, result: Any, initial_deposit: Optional[float] = None) -> List:
        """Validate a single result."""
        from src.domain.simulation import BattleTestResult, MonteCarloResult

        if isinstance(result, BattleTestResult):
            return self._validator.validate_battle_test_result(result, initial_deposit)
        elif isinstance(result, MonteCarloResult):
            return self._validator.validate_monte_carlo_result(result)
        else:
            logger.warning(f"Unknown result type: {type(result)}")
            return []

    # ==========================================================================
    # Direct access to individual validation rules
    # ==========================================================================

    def validate_cv01(self, portfolio_values: List[float]):
        """CV-01: Portfolio value never negative."""
        return self._validator.validate_cv01(portfolio_values)

    def validate_cv02(self, max_drawdown: float):
        """CV-02: Drawdown between 0% and 100%."""
        return self._validator.validate_cv02(max_drawdown)

    def validate_cv03(self, strategy_id: int, max_drawdown: float):
        """CV-03: Stable strategies have 0% max drawdown."""
        return self._validator.validate_cv03(strategy_id, max_drawdown)

    def validate_cv04(self, strategy_id: int, deposited: float, final_value: float):
        """CV-04: Final value >= deposited for stable strategies."""
        return self._validator.validate_cv04(strategy_id, deposited, final_value)

    def validate_cv05(self, deposited: float, final_value: float, reported_return: float):
        """CV-05: Return % matches calculation."""
        return self._validator.validate_cv05(deposited, final_value, reported_return)

    def validate_cv06(self, gross_return: float, tx_count: int, chain: str = 'arbitrum'):
        """CV-06: Net return > 0 after gas costs."""
        return self._validator.validate_cv06(gross_return, tx_count, chain)

    def validate_cv07(self, strategy_id: int, initial_deposit: float):
        """CV-07: Initial deposit >= per-strategy minimum."""
        return self._validator.validate_cv07(strategy_id, initial_deposit)

    def validate_battle_test_result(self, result, initial_deposit: float = None):
        """Validate a Battle Test result with all applicable rules."""
        return self._validator.validate_battle_test_result(result, initial_deposit)

    def validate_monte_carlo_result(self, result):
        """Validate a Monte Carlo result with all applicable rules."""
        return self._validator.validate_monte_carlo_result(result)


@ValidatorRegistry.register("data_validator")
class DataValidatorPlugin(Validator):
    """
    Validator for input data quality.

    Checks data integrity before processing by engines.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def validate(self, data: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate input data quality.

        Args:
            data: DataFrame or dict of DataFrames to validate
            config: Optional config with:
                - require_columns: List of required columns
                - date_range: (start, end) expected date range

        Returns:
            Dict with validation results
        """
        import pandas as pd

        config = config or {}
        results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        if isinstance(data, pd.DataFrame):
            data = {'data': data}

        for name, df in data.items():
            if not isinstance(df, pd.DataFrame):
                continue

            # Check empty
            if df.empty:
                results['warnings'].append(f"{name}: DataFrame is empty")

            # Check required columns
            required = config.get('require_columns', [])
            missing = [col for col in required if col not in df.columns]
            if missing:
                results['errors'].append(f"{name}: Missing columns {missing}")
                results['valid'] = False

            # Check date column
            if 'date' in df.columns:
                try:
                    dates = pd.to_datetime(df['date'])
                    if dates.isna().any():
                        results['warnings'].append(f"{name}: Some dates could not be parsed")
                except Exception as e:
                    results['errors'].append(f"{name}: Date parsing error: {e}")
                    results['valid'] = False

            # Check for nulls in critical columns
            critical_cols = config.get('critical_columns', [])
            for col in critical_cols:
                if col in df.columns and df[col].isna().any():
                    null_count = df[col].isna().sum()
                    results['warnings'].append(f"{name}: {null_count} null values in '{col}'")

        logger.info(f"Data validation: valid={results['valid']}, errors={len(results['errors'])}")
        return results
