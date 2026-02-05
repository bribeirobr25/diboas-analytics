"""Tests for CLI validation with security checks.

Tests the enhanced CLI validation including:
- Path traversal detection
- Strategy ID range validation
- Simulation bounds validation
- Error printing functionality
"""

import pytest
from argparse import Namespace
from io import StringIO
import sys

from src.utils.validation.cli import (
    validate_cli_args,
    print_validation_errors,
    require_data_files,
    _validate_path_security,
)
from src.utils.validation.input_validator import InputValidator


class TestPathTraversalValidation:
    """Tests for path traversal security validation."""

    def test_should_detect_parent_directory_traversal(self):
        """Detects ../.. traversal attempts."""
        args = Namespace(
            command='collect',
            data='../../../etc/passwd',
            offline=False
        )
        result = validate_cli_args(args)
        assert not result.is_valid
        assert any('traversal' in str(e.message).lower() for e in result.errors)

    def test_should_detect_url_encoded_traversal(self):
        """Detects URL-encoded traversal."""
        args = Namespace(
            command='dream-mode-export',
            output='outputs/%2e%2e/%2e%2e/malicious.json'
        )
        result = validate_cli_args(args)
        assert not result.is_valid

    def test_should_allow_safe_relative_paths(self):
        """Allows safe relative paths."""
        args = Namespace(
            command='dream-mode-export',
            output='./outputs/dream_mode_data.json'
        )
        result = validate_cli_args(args)
        # Should not have traversal errors (may have other issues if dir doesn't exist)
        traversal_errors = [e for e in result.errors if 'traversal' in str(e.message).lower()]
        assert len(traversal_errors) == 0

    def test_should_allow_absolute_paths(self):
        """Allows absolute paths without traversal."""
        args = Namespace(
            command='dream-mode-export',
            output='/tmp/diboas/output.json'
        )
        result = validate_cli_args(args)
        traversal_errors = [e for e in result.errors if 'traversal' in str(e.message).lower()]
        assert len(traversal_errors) == 0


class TestStrategyValidation:
    """Tests for strategy ID validation."""

    def test_should_accept_valid_strategy_ids(self):
        """Accepts strategy IDs 1-10."""
        for strategy_id in range(1, 11):
            args = Namespace(
                command='battle-test',
                strategy=strategy_id,
                scenario='A',
                start_date=None,
                end_date=None
            )
            result = validate_cli_args(args)
            strategy_errors = [e for e in result.errors if 'strategy' in e.field.lower()]
            assert len(strategy_errors) == 0, f"Strategy {strategy_id} should be valid"

    def test_should_reject_strategy_below_range(self):
        """Rejects strategy ID 0."""
        args = Namespace(
            command='battle-test',
            strategy=0,
            scenario='A',
            start_date=None,
            end_date=None
        )
        result = validate_cli_args(args)
        assert not result.is_valid
        assert any('strategy' in e.field.lower() for e in result.errors)

    def test_should_reject_strategy_above_range(self):
        """Rejects strategy ID > 10."""
        args = Namespace(
            command='battle-test',
            strategy=99,
            scenario='A',
            start_date=None,
            end_date=None
        )
        result = validate_cli_args(args)
        assert not result.is_valid
        assert any('strategy' in e.field.lower() for e in result.errors)

    def test_should_allow_none_strategy(self):
        """Allows None strategy (run all strategies)."""
        args = Namespace(
            command='battle-test',
            strategy=None,
            scenario='A',
            start_date=None,
            end_date=None
        )
        result = validate_cli_args(args)
        strategy_errors = [e for e in result.errors if 'strategy' in e.field.lower()]
        assert len(strategy_errors) == 0


class TestSimulationValidation:
    """Tests for Monte Carlo simulation validation."""

    def test_should_accept_valid_simulation_count(self):
        """Accepts simulation count in valid range."""
        args = Namespace(
            command='monte-carlo',
            strategy=1,
            simulations=5000,
            seed=42
        )
        result = validate_cli_args(args)
        sim_errors = [e for e in result.errors if 'simulations' in e.field.lower()]
        assert len(sim_errors) == 0

    def test_should_warn_on_low_simulations(self):
        """Warns when simulation count is low."""
        args = Namespace(
            command='monte-carlo',
            strategy=1,
            simulations=500,  # Low but valid
            seed=42
        )
        result = validate_cli_args(args)
        # Should have warning but no error
        assert any('simulation' in w.field.lower() for w in result.warnings)
        sim_errors = [e for e in result.errors if 'simulations' in e.field.lower()]
        assert len(sim_errors) == 0

    def test_should_reject_too_few_simulations(self):
        """Rejects simulation count below minimum."""
        args = Namespace(
            command='monte-carlo',
            strategy=1,
            simulations=50,  # Below 100 minimum
            seed=42
        )
        result = validate_cli_args(args)
        assert not result.is_valid
        assert any('simulations' in e.field.lower() for e in result.errors)

    def test_should_reject_too_many_simulations(self):
        """Rejects simulation count above maximum."""
        args = Namespace(
            command='monte-carlo',
            strategy=1,
            simulations=999999,  # Above 100000 max
            seed=42
        )
        result = validate_cli_args(args)
        assert not result.is_valid
        assert any('simulations' in e.field.lower() for e in result.errors)


class TestHealthCommandValidation:
    """Tests for health command (minimal validation)."""

    def test_should_pass_health_with_no_args(self):
        """Health command with no args passes validation."""
        args = Namespace(command='health')
        result = validate_cli_args(args)
        assert result.is_valid


class TestPrintValidationErrors:
    """Tests for validation error printing."""

    def test_should_return_false_when_valid(self):
        """Returns False when no errors."""
        from src.utils.validation.core import ValidationResult
        result = ValidationResult()
        has_errors = print_validation_errors(result, exit_on_error=False)
        assert has_errors is False

    def test_should_return_true_when_errors_exist(self, capsys):
        """Returns True when errors exist."""
        from src.utils.validation.core import ValidationResult
        result = ValidationResult()
        result.add_error(
            field='test_field',
            value='bad_value',
            message='Test error message',
            suggestion='Fix it'
        )
        has_errors = print_validation_errors(result, exit_on_error=False)
        assert has_errors is True

        # Check output
        captured = capsys.readouterr()
        assert 'test_field' in captured.out
        assert 'Test error message' in captured.out

    def test_should_include_suggestions(self, capsys):
        """Includes suggestions in output."""
        from src.utils.validation.core import ValidationResult
        result = ValidationResult()
        result.add_error(
            field='strategy',
            value=99,
            message='Invalid strategy',
            suggestion='Use 1-10'
        )
        print_validation_errors(result, exit_on_error=False)
        captured = capsys.readouterr()
        assert 'Use 1-10' in captured.out

    def test_should_print_warnings(self, capsys):
        """Prints warnings when present."""
        from src.utils.validation.core import ValidationResult
        result = ValidationResult()
        result.add_warning(
            field='simulations',
            value=500,
            message='Low count',
            suggestion='Use 5000+'
        )
        print_validation_errors(result, exit_on_error=False)
        captured = capsys.readouterr()
        assert 'Low count' in captured.out
        assert 'warnings' in captured.out.lower()


class TestRequireDataFiles:
    """Tests for data file requirement validation."""

    def test_should_fail_when_file_missing(self, tmp_path):
        """Fails when required file doesn't exist."""
        missing_file = str(tmp_path / 'nonexistent.csv')
        result = require_data_files([missing_file])
        assert not result.is_valid
        assert any('not found' in e.message.lower() for e in result.errors)

    def test_should_pass_when_file_exists(self, tmp_path):
        """Passes when required file exists."""
        existing_file = tmp_path / 'test_data.csv'
        existing_file.write_text('col1,col2\n1,2')
        result = require_data_files([str(existing_file)])
        file_errors = [e for e in result.errors if 'data_file' in e.field]
        assert len(file_errors) == 0


class TestInternalValidatePathSecurity:
    """Tests for internal path security validation helper."""

    def test_should_add_error_for_traversal(self):
        """Adds error when traversal detected."""
        validator = InputValidator()
        _validate_path_security(validator, '../../../etc/passwd', 'test_path')
        result = validator.get_result()
        assert not result.is_valid
        assert any('traversal' in e.message.lower() for e in result.errors)

    def test_should_not_add_error_for_safe_path(self):
        """Does not add error for safe paths."""
        validator = InputValidator()
        _validate_path_security(validator, './outputs/result.json', 'test_path')
        result = validator.get_result()
        traversal_errors = [e for e in result.errors if 'traversal' in e.message.lower()]
        assert len(traversal_errors) == 0
