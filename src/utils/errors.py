"""
Error handling utilities with recovery suggestions.

Provides structured errors, graceful degradation, and
user-friendly error messages.
"""

import sys
import traceback
import logging
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    """Categories of errors for appropriate handling."""
    DATA_MISSING = 'data_missing'
    DATA_CORRUPT = 'data_corrupt'
    NETWORK = 'network'
    CONFIGURATION = 'configuration'
    VALIDATION = 'validation'
    CALCULATION = 'calculation'
    PERMISSION = 'permission'
    UNKNOWN = 'unknown'


@dataclass
class RecoverySuggestion:
    """A suggested recovery action."""
    action: str
    command: Optional[str] = None
    priority: int = 1  # 1 = highest


@dataclass
class DiBoaSError(Exception):
    """
    Base exception with recovery suggestions.

    Provides structured error information for better user experience
    and debugging.
    """
    message: str
    category: ErrorCategory = ErrorCategory.UNKNOWN
    suggestions: list = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    original_error: Optional[Exception] = None

    def __str__(self):
        return self.message

    def format_user_message(self) -> str:
        """Format error message for end users."""
        lines = [
            f"Error: {self.message}",
            ""
        ]

        if self.suggestions:
            lines.append("Suggested actions:")
            for i, suggestion in enumerate(self.suggestions, 1):
                if isinstance(suggestion, RecoverySuggestion):
                    lines.append(f"  {i}. {suggestion.action}")
                    if suggestion.command:
                        lines.append(f"     Command: {suggestion.command}")
                else:
                    lines.append(f"  {i}. {suggestion}")

        return "\n".join(lines)

    def format_debug_message(self) -> str:
        """Format detailed error message for debugging."""
        lines = [
            f"[{self.category.value.upper()}] {self.message}",
            f"Timestamp: {datetime.utcnow().isoformat()}",
        ]

        if self.context:
            lines.append("Context:")
            for key, value in self.context.items():
                lines.append(f"  {key}: {value}")

        if self.original_error:
            lines.append(f"Original error: {type(self.original_error).__name__}: {self.original_error}")

        if self.suggestions:
            lines.append("Suggestions:")
            for s in self.suggestions:
                if isinstance(s, RecoverySuggestion):
                    lines.append(f"  - {s.action}")
                else:
                    lines.append(f"  - {s}")

        return "\n".join(lines)


class DataNotFoundError(DiBoaSError):
    """Raised when required data files are missing."""

    def __init__(
        self,
        filepath: str,
        data_type: str = 'data',
        **kwargs
    ):
        suggestions = [
            RecoverySuggestion(
                action="Run data collection to download required files",
                command="python main.py collect --offline"
            ),
            RecoverySuggestion(
                action="Check if the file exists at the expected location",
                command=f"ls -la {filepath}"
            ),
            RecoverySuggestion(
                action="Verify data directory is correctly configured",
                priority=2
            )
        ]

        super().__init__(
            message=f"Required {data_type} file not found: {filepath}",
            category=ErrorCategory.DATA_MISSING,
            suggestions=suggestions,
            context={'filepath': filepath, 'data_type': data_type},
            **kwargs
        )


class DataCorruptError(DiBoaSError):
    """Raised when data file is corrupt or malformed."""

    def __init__(
        self,
        filepath: str,
        reason: str,
        **kwargs
    ):
        suggestions = [
            RecoverySuggestion(
                action="Re-download the data file",
                command="python main.py collect --all"
            ),
            RecoverySuggestion(
                action="Check file format and encoding",
                priority=2
            ),
            RecoverySuggestion(
                action="Restore from backup if available",
                priority=3
            )
        ]

        super().__init__(
            message=f"Data file is corrupt or malformed: {filepath}. Reason: {reason}",
            category=ErrorCategory.DATA_CORRUPT,
            suggestions=suggestions,
            context={'filepath': filepath, 'reason': reason},
            **kwargs
        )


class NetworkError(DiBoaSError):
    """Raised when network operations fail."""

    def __init__(
        self,
        operation: str,
        url: str = None,
        **kwargs
    ):
        suggestions = [
            RecoverySuggestion(
                action="Check your internet connection",
                priority=1
            ),
            RecoverySuggestion(
                action="Use offline mode with bundled data",
                command="python main.py collect --offline"
            ),
            RecoverySuggestion(
                action="Retry the operation later",
                priority=3
            )
        ]

        context = {'operation': operation}
        if url:
            context['url'] = url

        super().__init__(
            message=f"Network error during {operation}",
            category=ErrorCategory.NETWORK,
            suggestions=suggestions,
            context=context,
            **kwargs
        )


class ConfigurationError(DiBoaSError):
    """Raised when configuration is invalid."""

    def __init__(
        self,
        config_file: str,
        issue: str,
        **kwargs
    ):
        suggestions = [
            RecoverySuggestion(
                action="Check configuration file syntax",
                command=f"python -m json.tool {config_file}"
            ),
            RecoverySuggestion(
                action="Restore default configuration",
                priority=2
            ),
            RecoverySuggestion(
                action="Review configuration documentation",
                priority=3
            )
        ]

        super().__init__(
            message=f"Configuration error in {config_file}: {issue}",
            category=ErrorCategory.CONFIGURATION,
            suggestions=suggestions,
            context={'config_file': config_file, 'issue': issue},
            **kwargs
        )


class CalculationError(DiBoaSError):
    """Raised when calculations produce invalid results."""

    def __init__(
        self,
        operation: str,
        reason: str,
        **kwargs
    ):
        suggestions = [
            RecoverySuggestion(
                action="Check input data for anomalies",
                priority=1
            ),
            RecoverySuggestion(
                action="Run with verbose logging for details",
                command="python main.py <command> --verbose"
            ),
            RecoverySuggestion(
                action="Report issue if problem persists",
                priority=3
            )
        ]

        super().__init__(
            message=f"Calculation error in {operation}: {reason}",
            category=ErrorCategory.CALCULATION,
            suggestions=suggestions,
            context={'operation': operation, 'reason': reason},
            **kwargs
        )


# Error recovery suggestions database
ERROR_SUGGESTIONS: Dict[str, list] = {
    'FileNotFoundError': [
        "Check if the file path is correct",
        "Run 'python main.py collect --offline' to load bundled data",
        "Verify the data directory exists"
    ],
    'PermissionError': [
        "Check file permissions",
        "Run with appropriate user privileges",
        "Verify output directory is writable"
    ],
    'JSONDecodeError': [
        "Check file for syntax errors",
        "Verify file is not corrupted",
        "Re-download or restore from backup"
    ],
    'ConnectionError': [
        "Check internet connection",
        "Use offline mode: python main.py collect --offline",
        "Check if API endpoints are accessible"
    ],
    'ValueError': [
        "Check input values are in expected format",
        "Review command line arguments",
        "Run with --verbose for more details"
    ],
    'KeyError': [
        "Check data file structure",
        "Verify configuration matches expected format",
        "Run with --verbose for more details"
    ]
}


def get_suggestions_for_error(error: Exception) -> list:
    """
    Get recovery suggestions for a standard exception.

    Args:
        error: The exception

    Returns:
        List of suggestion strings
    """
    error_type = type(error).__name__
    return ERROR_SUGGESTIONS.get(error_type, [
        "Check the error message for details",
        "Run with --verbose for more information",
        "Review the documentation"
    ])


def handle_error(
    error: Exception,
    context: str = '',
    exit_on_error: bool = True,
    verbose: bool = False
) -> None:
    """
    Handle an error with appropriate messaging.

    Args:
        error: The exception to handle
        context: Additional context about where error occurred
        exit_on_error: Whether to exit the program
        verbose: Whether to show full traceback
    """
    # Log the error
    if verbose:
        logger.exception(f"Error in {context}: {error}")
    else:
        logger.error(f"Error in {context}: {error}")

    # Print user-friendly message
    print(f"\nError: {error}")

    if context:
        print(f"Context: {context}")

    # Get and print suggestions
    if isinstance(error, DiBoaSError):
        print(error.format_user_message())
    else:
        suggestions = get_suggestions_for_error(error)
        if suggestions:
            print("\nSuggested actions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")

    if verbose:
        print("\nFull traceback:")
        traceback.print_exc()

    if exit_on_error:
        sys.exit(1)


def graceful_degradation(
    fallback_value: Any = None,
    fallback_func: Callable = None,
    error_message: str = None,
    log_level: str = 'warning'
):
    """
    Decorator for graceful degradation on error.

    Instead of crashing, returns a fallback value and logs the error.

    Args:
        fallback_value: Value to return on error
        fallback_func: Function to call for fallback value
        error_message: Custom error message
        log_level: Logging level ('warning', 'error', 'info')

    Example:
        @graceful_degradation(fallback_value=[], error_message="Could not load data")
        def load_data():
            return api.fetch_data()
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = error_message or f"{func.__name__} failed: {e}"

                log_func = getattr(logger, log_level, logger.warning)
                log_func(f"{msg} - using fallback")

                if fallback_func:
                    return fallback_func()
                return fallback_value

        return wrapper
    return decorator


class ErrorCollector:
    """
    Collect multiple errors before reporting.

    Useful for validation that should report all errors,
    not just the first one.
    """

    def __init__(self):
        self.errors: list = []
        self.warnings: list = []

    def add_error(self, error: Exception, context: str = ''):
        """Add an error to the collection."""
        self.errors.append({
            'error': error,
            'context': context,
            'timestamp': datetime.utcnow()
        })

    def add_warning(self, message: str, context: str = ''):
        """Add a warning to the collection."""
        self.warnings.append({
            'message': message,
            'context': context,
            'timestamp': datetime.utcnow()
        })

    @property
    def has_errors(self) -> bool:
        """Check if any errors were collected."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if any warnings were collected."""
        return len(self.warnings) > 0

    def raise_if_errors(self):
        """Raise exception if errors were collected."""
        if self.has_errors:
            messages = [
                f"[{e['context']}] {e['error']}" if e['context'] else str(e['error'])
                for e in self.errors
            ]
            raise DiBoaSError(
                message=f"Multiple errors occurred:\n" + "\n".join(f"  - {m}" for m in messages),
                category=ErrorCategory.VALIDATION,
                context={'error_count': len(self.errors)}
            )

    def format_report(self) -> str:
        """Format all errors and warnings as a report."""
        lines = []

        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for e in self.errors:
                ctx = f" [{e['context']}]" if e['context'] else ""
                lines.append(f"  - {e['error']}{ctx}")

        if self.warnings:
            lines.append(f"Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                ctx = f" [{w['context']}]" if w['context'] else ""
                lines.append(f"  - {w['message']}{ctx}")

        return "\n".join(lines) if lines else "No errors or warnings"
