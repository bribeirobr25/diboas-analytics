"""
CLI argument validation functions.

Provides validation for argparse arguments and data file requirements.

Principle 8 (Security):
-----------------------
All CLI inputs are validated before processing to prevent:
- Path traversal attacks
- Invalid parameter ranges
- Malformed input exploitation
"""

import sys
from pathlib import Path
from typing import List, Optional

from src.utils.validation.core import ValidationResult
from src.utils.validation.input_validator import InputValidator
from src.utils.security.input_validation import (
    is_path_traversal,
    PathSecurityError,
)


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
            _validate_path_security(validator, output, 'output')
            validator.validate_output_dir(Path(output).parent)

    elif command == 'collect':
        data_path = getattr(args, 'data', None)
        if data_path:
            _validate_path_security(validator, data_path, 'data')

    elif command == 'health':
        # No special validation needed for health
        pass

    # Validate any file path arguments across all commands
    for attr_name in ['output', 'data', 'config', 'input']:
        path_value = getattr(args, attr_name, None)
        if path_value:
            _validate_path_security(validator, path_value, attr_name)

    return validator.get_result()


def _validate_path_security(
    validator: InputValidator,
    path: str,
    field_name: str
) -> None:
    """
    Validate a path for security issues (traversal attacks).

    Args:
        validator: InputValidator instance to add errors to
        path: Path string to validate
        field_name: Field name for error messages
    """
    if is_path_traversal(path):
        validator.result.add_error(
            field=field_name,
            value=path,
            message=f"Path contains directory traversal sequences",
            suggestion="Use absolute paths or paths without '..' sequences"
        )


def print_validation_errors(
    result: ValidationResult,
    command: str = None,
    exit_on_error: bool = True
) -> bool:
    """
    Print validation errors and warnings in a user-friendly format.

    Args:
        result: ValidationResult to print
        command: Command name for context
        exit_on_error: Whether to exit on errors (default True)

    Returns:
        True if there were errors, False otherwise
    """
    if result.is_valid and not result.warnings:
        return False

    # Print errors
    if result.errors:
        cmd_context = f" for '{command}'" if command else ""
        print(f"\n\033[91mValidation errors{cmd_context}:\033[0m")
        for error in result.errors:
            print(f"  \033[91m✗\033[0m {error.field}: {error.message}")
            if error.suggestion:
                print(f"    \033[90m→ {error.suggestion}\033[0m")

    # Print warnings
    if result.warnings:
        print(f"\n\033[93mValidation warnings:\033[0m")
        for warning in result.warnings:
            print(f"  \033[93m⚠\033[0m {warning.field}: {warning.message}")
            if warning.suggestion:
                print(f"    \033[90m→ {warning.suggestion}\033[0m")

    print()  # Empty line

    if result.errors and exit_on_error:
        sys.exit(1)

    return bool(result.errors)


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
