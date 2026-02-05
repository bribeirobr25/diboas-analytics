"""
Error handling utilities and decorators.

Provides error handling, graceful degradation, and error collection.
"""

import sys
import traceback
import logging
from typing import Dict, Any, Callable
from datetime import datetime

from src.utils.errors.core import DiBoaSError, ErrorCategory

logger = logging.getLogger(__name__)


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
