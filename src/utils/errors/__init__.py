"""
Error handling utilities with recovery suggestions.

Provides structured errors, graceful degradation, and
user-friendly error messages.
"""

from src.utils.errors.core import (
    ErrorCategory,
    RecoverySuggestion,
    DiBoaSError,
    _sanitize_message,
    SENSITIVE_ERROR_PATTERNS,
)
from src.utils.errors.types import (
    DataNotFoundError,
    DataCorruptError,
    NetworkError,
    ConfigurationError,
    CalculationError,
)
from src.utils.errors.handlers import (
    ERROR_SUGGESTIONS,
    get_suggestions_for_error,
    handle_error,
    graceful_degradation,
    ErrorCollector,
)

__all__ = [
    # Core
    'ErrorCategory',
    'RecoverySuggestion',
    'DiBoaSError',
    '_sanitize_message',
    'SENSITIVE_ERROR_PATTERNS',
    # Types
    'DataNotFoundError',
    'DataCorruptError',
    'NetworkError',
    'ConfigurationError',
    'CalculationError',
    # Handlers
    'ERROR_SUGGESTIONS',
    'get_suggestions_for_error',
    'handle_error',
    'graceful_degradation',
    'ErrorCollector',
]
