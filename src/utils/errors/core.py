"""
Core error classes and types.

Contains base exception classes and enums.
"""

import re
from typing import Optional, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# Patterns that may contain sensitive data in error messages
SENSITIVE_ERROR_PATTERNS: Set[str] = frozenset([
    'api_key', 'apikey', 'api-key',
    'secret', 'token', 'password',
    'authorization', 'bearer',
    'credential', 'private_key',
])


def _sanitize_message(message: str) -> str:
    """
    Sanitize an error message by masking potentially sensitive data.

    Removes or masks:
    - API keys and tokens
    - File paths that might reveal system structure
    - IP addresses
    - Credentials

    Args:
        message: Raw error message

    Returns:
        Sanitized message safe for logging
    """
    if not message or not isinstance(message, str):
        return message or ""

    result = message

    # Mask API keys and tokens (generic patterns)
    # Pattern: key/token/secret followed by value
    result = re.sub(
        r'(?i)(api[_-]?key|token|secret|password|credential)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]{8,})',
        r'\1=***MASKED***',
        result
    )

    # Mask Bearer tokens
    result = re.sub(
        r'(?i)(bearer\s+)([a-zA-Z0-9_.-]{20,})',
        r'\1***MASKED***',
        result
    )

    # Mask JWT tokens
    result = re.sub(
        r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
        '***JWT_TOKEN_MASKED***',
        result
    )

    # Mask full file paths that might reveal system structure
    # Keep just the filename for context
    def mask_path(match):
        full_path = match.group(0)
        # Extract just the filename
        parts = full_path.replace('\\', '/').split('/')
        filename = parts[-1] if parts else full_path
        return f"[.../{filename}]"

    # Match common absolute paths
    result = re.sub(
        r'(?:/[a-zA-Z0-9_.-]+){3,}(?:/[a-zA-Z0-9_.-]+)+',
        mask_path,
        result
    )
    result = re.sub(
        r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\){2,}[^\\/:*?"<>|\r\n]*',
        mask_path,
        result
    )

    # Mask IP addresses (keep first octet for debugging)
    result = re.sub(
        r'\b(\d{1,3})\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        r'\1.***.***. ***',
        result
    )

    return result


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

    def format_safe_message(self) -> str:
        """
        Format error message with sensitive data masked.

        Safe for logging, external reporting, and display to users.

        Returns:
            Sanitized error message
        """
        sanitized_message = _sanitize_message(self.message)

        lines = [
            f"[{self.category.value.upper()}] {sanitized_message}",
            f"Timestamp: {datetime.utcnow().isoformat()}",
        ]

        if self.context:
            lines.append("Context:")
            for key, value in self.context.items():
                # Check if key suggests sensitive data
                key_lower = str(key).lower()
                if any(pattern in key_lower for pattern in SENSITIVE_ERROR_PATTERNS):
                    lines.append(f"  {key}: ***MASKED***")
                else:
                    sanitized_value = _sanitize_message(str(value))
                    lines.append(f"  {key}: {sanitized_value}")

        if self.original_error:
            original_msg = _sanitize_message(str(self.original_error))
            lines.append(f"Original error: {type(self.original_error).__name__}: {original_msg}")

        return "\n".join(lines)

    def to_safe_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary with sensitive data masked.

        Safe for serialization and external reporting.

        Returns:
            Dictionary representation with masked sensitive data
        """
        sanitized_context = {}
        for key, value in self.context.items():
            key_lower = str(key).lower()
            if any(pattern in key_lower for pattern in SENSITIVE_ERROR_PATTERNS):
                sanitized_context[key] = '***MASKED***'
            else:
                sanitized_context[key] = _sanitize_message(str(value))

        return {
            'message': _sanitize_message(self.message),
            'category': self.category.value,
            'context': sanitized_context,
            'timestamp': datetime.utcnow().isoformat(),
            'has_original_error': self.original_error is not None,
        }
