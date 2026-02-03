"""
Input validation utilities for CLI arguments and data.

Provides validators with clear error messages and recovery suggestions.
"""

import os
from datetime import date, datetime
from pathlib import Path
from typing import Optional, List, Any, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    """Structured validation error with recovery suggestion."""
    field: str
    value: Any
    message: str
    suggestion: str
    severity: str = 'error'  # 'error', 'warning'

    def __str__(self):
        return f"{self.field}: {self.message}"

    def format_full(self) -> str:
        """Format error with suggestion."""
        return f"[{self.severity.upper()}] {self.field}: {self.message}\n  Suggestion: {self.suggestion}"


class ValidationResult:
    """Result of validation containing errors and warnings."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0

    def add_error(
        self,
        field: str,
        value: Any,
        message: str,
        suggestion: str
    ):
        """Add a validation error."""
        self.errors.append(ValidationError(
            field=field,
            value=value,
            message=message,
            suggestion=suggestion,
            severity='error'
        ))

    def add_warning(
        self,
        field: str,
        value: Any,
        message: str,
        suggestion: str
    ):
        """Add a validation warning."""
        self.warnings.append(ValidationError(
            field=field,
            value=value,
            message=message,
            suggestion=suggestion,
            severity='warning'
        ))

    def raise_if_invalid(self):
        """Raise ValueError if validation failed."""
        if not self.is_valid:
            error_messages = [e.format_full() for e in self.errors]
            raise ValueError(
                f"Validation failed with {len(self.errors)} error(s):\n" +
                "\n".join(error_messages)
            )

    def format_report(self) -> str:
        """Format all errors and warnings as a report."""
        lines = []

        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for e in self.errors:
                lines.append(f"  - {e.format_full()}")

        if self.warnings:
            lines.append(f"Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"  - {w.format_full()}")

        return "\n".join(lines) if lines else "Validation passed"


class InputValidator:
    """
    Validator for CLI inputs and configuration.

    Collects all validation errors before raising, providing
    comprehensive feedback to users.
    """

    def __init__(self):
        self.result = ValidationResult()

    def validate_strategy_id(
        self,
        strategy_id: Optional[int],
        field_name: str = 'strategy'
    ) -> Optional[int]:
        """
        Validate strategy ID is in valid range (1-10).

        Args:
            strategy_id: Strategy ID to validate (None is allowed)
            field_name: Field name for error messages

        Returns:
            Validated strategy ID or None
        """
        if strategy_id is None:
            return None

        if not isinstance(strategy_id, int):
            self.result.add_error(
                field=field_name,
                value=strategy_id,
                message=f"Must be an integer, got {type(strategy_id).__name__}",
                suggestion="Use --strategy 1 through --strategy 10"
            )
            return None

        if strategy_id < 1 or strategy_id > 10:
            self.result.add_error(
                field=field_name,
                value=strategy_id,
                message=f"Strategy ID {strategy_id} is out of range",
                suggestion="Valid strategies are 1-10. Use --strategy 1 for Safe Harbor, --strategy 10 for Full Throttle"
            )
            return None

        return strategy_id

    def validate_date(
        self,
        date_str: Optional[str],
        field_name: str = 'date',
        min_date: date = None,
        max_date: date = None
    ) -> Optional[date]:
        """
        Validate and parse date string.

        Args:
            date_str: Date string in YYYY-MM-DD format
            field_name: Field name for error messages
            min_date: Minimum allowed date
            max_date: Maximum allowed date

        Returns:
            Parsed date or None
        """
        if date_str is None:
            return None

        try:
            parsed = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            self.result.add_error(
                field=field_name,
                value=date_str,
                message=f"Invalid date format: '{date_str}'",
                suggestion="Use YYYY-MM-DD format (e.g., 2022-05-01)"
            )
            return None

        if min_date and parsed < min_date:
            self.result.add_error(
                field=field_name,
                value=date_str,
                message=f"Date {parsed} is before minimum {min_date}",
                suggestion=f"Use a date on or after {min_date}"
            )
            return None

        if max_date and parsed > max_date:
            self.result.add_error(
                field=field_name,
                value=date_str,
                message=f"Date {parsed} is after maximum {max_date}",
                suggestion=f"Use a date on or before {max_date}"
            )
            return None

        return parsed

    def validate_date_range(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        start_field: str = 'start_date',
        end_field: str = 'end_date'
    ) -> tuple[Optional[date], Optional[date]]:
        """
        Validate a date range.

        Args:
            start_date: Start date string
            end_date: End date string
            start_field: Field name for start date
            end_field: Field name for end date

        Returns:
            Tuple of (start_date, end_date) or (None, None)
        """
        start = self.validate_date(start_date, start_field)
        end = self.validate_date(end_date, end_field)

        if start and end and start > end:
            self.result.add_error(
                field=f'{start_field}/{end_field}',
                value=f'{start_date} to {end_date}',
                message=f"Start date ({start}) is after end date ({end})",
                suggestion="Ensure start date is before end date"
            )
            return None, None

        return start, end

    def validate_positive_int(
        self,
        value: Optional[int],
        field_name: str,
        min_value: int = 1,
        max_value: int = None
    ) -> Optional[int]:
        """
        Validate a positive integer.

        Args:
            value: Value to validate
            field_name: Field name for error messages
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Returns:
            Validated value or None
        """
        if value is None:
            return None

        if not isinstance(value, int):
            self.result.add_error(
                field=field_name,
                value=value,
                message=f"Must be an integer, got {type(value).__name__}",
                suggestion=f"Provide an integer value for {field_name}"
            )
            return None

        if value < min_value:
            self.result.add_error(
                field=field_name,
                value=value,
                message=f"Value {value} is below minimum {min_value}",
                suggestion=f"Use a value of at least {min_value}"
            )
            return None

        if max_value and value > max_value:
            self.result.add_error(
                field=field_name,
                value=value,
                message=f"Value {value} exceeds maximum {max_value}",
                suggestion=f"Use a value no greater than {max_value}"
            )
            return None

        return value

    def validate_simulations(
        self,
        n_simulations: int,
        field_name: str = 'simulations'
    ) -> int:
        """
        Validate Monte Carlo simulation count.

        Args:
            n_simulations: Number of simulations
            field_name: Field name for error messages

        Returns:
            Validated simulation count
        """
        validated = self.validate_positive_int(
            n_simulations,
            field_name,
            min_value=100,
            max_value=100000
        )

        if validated and validated < 1000:
            self.result.add_warning(
                field=field_name,
                value=n_simulations,
                message=f"Low simulation count ({n_simulations}) may produce unreliable results",
                suggestion="Use at least 1000 simulations for statistically significant results, 5000 recommended"
            )

        return validated or 5000  # Default

    def validate_file_exists(
        self,
        filepath: Union[str, Path],
        field_name: str = 'file'
    ) -> Optional[Path]:
        """
        Validate that a file exists.

        Args:
            filepath: Path to file
            field_name: Field name for error messages

        Returns:
            Path object if file exists, None otherwise
        """
        path = Path(filepath)

        if not path.exists():
            self.result.add_error(
                field=field_name,
                value=str(filepath),
                message=f"File not found: {filepath}",
                suggestion=f"Check the path exists or run data collection first"
            )
            return None

        if not path.is_file():
            self.result.add_error(
                field=field_name,
                value=str(filepath),
                message=f"Path is not a file: {filepath}",
                suggestion=f"Provide a path to a file, not a directory"
            )
            return None

        return path

    def validate_output_dir(
        self,
        dirpath: Union[str, Path],
        field_name: str = 'output_dir',
        create: bool = True
    ) -> Optional[Path]:
        """
        Validate output directory (create if needed).

        Args:
            dirpath: Path to directory
            field_name: Field name for error messages
            create: Whether to create if doesn't exist

        Returns:
            Path object if valid, None otherwise
        """
        path = Path(dirpath)

        if not path.exists():
            if create:
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created output directory: {path}")
                except OSError as e:
                    self.result.add_error(
                        field=field_name,
                        value=str(dirpath),
                        message=f"Cannot create directory: {e}",
                        suggestion="Check permissions or use a different path"
                    )
                    return None
            else:
                self.result.add_error(
                    field=field_name,
                    value=str(dirpath),
                    message=f"Directory not found: {dirpath}",
                    suggestion="Create the directory or specify an existing path"
                )
                return None

        if not path.is_dir():
            self.result.add_error(
                field=field_name,
                value=str(dirpath),
                message=f"Path is not a directory: {dirpath}",
                suggestion="Provide a path to a directory"
            )
            return None

        return path

    def validate_scenario(
        self,
        scenario: str,
        field_name: str = 'scenario'
    ) -> str:
        """
        Validate Battle Test scenario.

        Args:
            scenario: Scenario identifier (A, B, or C)
            field_name: Field name for error messages

        Returns:
            Validated scenario
        """
        valid_scenarios = ['A', 'B', 'C']

        if scenario not in valid_scenarios:
            self.result.add_error(
                field=field_name,
                value=scenario,
                message=f"Invalid scenario: '{scenario}'",
                suggestion="Use A (Felipe - $10K), B (Ana - $5), or C (Per-strategy minimum)"
            )
            return 'A'  # Default

        return scenario

    def get_result(self) -> ValidationResult:
        """Get validation result."""
        return self.result

    def raise_if_invalid(self):
        """Raise if validation failed."""
        self.result.raise_if_invalid()


def validate_cli_args(args) -> ValidationResult:
    """
    Validate CLI arguments from argparse.

    Args:
        args: Parsed argparse namespace

    Returns:
        ValidationResult with any errors/warnings
    """
    validator = InputValidator()

    # Validate based on command
    command = getattr(args, 'command', None)

    if command == 'battle-test':
        validator.validate_strategy_id(getattr(args, 'strategy', None))
        validator.validate_scenario(getattr(args, 'scenario', 'A'))

        start = getattr(args, 'start_date', None)
        end = getattr(args, 'end_date', None)
        if start or end:
            validator.validate_date_range(start, end)

    elif command == 'monte-carlo':
        validator.validate_strategy_id(getattr(args, 'strategy', None))
        validator.validate_simulations(getattr(args, 'simulations', 5000))

        seed = getattr(args, 'seed', None)
        if seed is not None:
            validator.validate_positive_int(seed, 'seed', min_value=0)

    elif command == 'dream-mode-export':
        output = getattr(args, 'output', None)
        if output:
            validator.validate_output_dir(Path(output).parent)

    return validator.get_result()


def require_data_files(files: List[str]) -> ValidationResult:
    """
    Validate that required data files exist.

    Args:
        files: List of required file paths

    Returns:
        ValidationResult with any errors
    """
    validator = InputValidator()

    for filepath in files:
        validator.validate_file_exists(filepath, f"data_file:{Path(filepath).name}")

    return validator.get_result()
