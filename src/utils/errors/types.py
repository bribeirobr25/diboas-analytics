"""
Specific error types for different failure scenarios.

Each error type includes appropriate recovery suggestions.
"""

from src.utils.errors.core import DiBoaSError, ErrorCategory, RecoverySuggestion


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
