"""
Log masking utilities for sensitive data protection.

Provides functions to mask API keys, tokens, and PII in log output
to prevent accidental exposure of sensitive information.
"""

import re
import logging
from typing import Dict, Any, Optional, List, Pattern
from functools import lru_cache


# Patterns for sensitive data that should be masked
SENSITIVE_PATTERNS: Dict[str, Pattern] = {
    # API Keys (various formats) - min 8 chars to catch most keys
    # Group 1: key name with optional separator, Group 2: the value
    'api_key': re.compile(
        r'(?i)(api[_-]?key|apikey|key)(["\']?\s*[:=]\s*["\']?)([a-zA-Z0-9_-]{8,})',
        re.IGNORECASE
    ),
    # Bearer tokens - min 10 chars
    'bearer_token': re.compile(
        r'(?i)(bearer\s+)([a-zA-Z0-9_.-]{10,})',
        re.IGNORECASE
    ),
    # Generic secrets - min 6 chars
    # Group 1: key name, Group 2: separator, Group 3: value
    'secret': re.compile(
        r'(?i)(secret|password|passwd|token)(["\']?\s*[:=]\s*["\']?)([^\s"\']{6,})',
        re.IGNORECASE
    ),
    # JWT tokens
    'jwt': re.compile(
        r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'
    ),
    # Credit card numbers (basic pattern)
    'credit_card': re.compile(
        r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    ),
    # Email addresses (for PII masking)
    'email': re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    ),
    # IP addresses
    'ip_address': re.compile(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ),
}

# Keywords that indicate a value should be masked
SENSITIVE_KEYWORDS = frozenset([
    'api_key', 'apikey', 'api-key',
    'secret', 'secret_key', 'secretkey',
    'password', 'passwd', 'pwd',
    'token', 'access_token', 'refresh_token',
    'private_key', 'privatekey',
    'auth', 'authorization',
    'credential', 'credentials',
    'fred_api_key', 'coingecko_api_key',
    'etherscan_api_key', 'helius_api_key',
    'slack_webhook', 'webhook_url',
    'pagerduty_api_key',
])


def mask_value(value: str, visible_chars: int = 4) -> str:
    """
    Mask a sensitive value, keeping only first few characters visible.

    Args:
        value: Value to mask
        visible_chars: Number of characters to keep visible at start

    Returns:
        Masked value
    """
    if not value:
        return value

    if len(value) <= visible_chars:
        return '*' * len(value)

    return value[:visible_chars] + '*' * (len(value) - visible_chars)


def mask_sensitive_values(
    text: str,
    patterns: Dict[str, Pattern] = None,
    visible_chars: int = 4
) -> str:
    """
    Mask sensitive values in a text string.

    Args:
        text: Text potentially containing sensitive data
        patterns: Custom patterns to use (defaults to SENSITIVE_PATTERNS)
        visible_chars: Characters to keep visible

    Returns:
        Text with sensitive values masked
    """
    if not text or not isinstance(text, str):
        return text

    patterns = patterns or SENSITIVE_PATTERNS
    result = text

    # Apply each pattern
    for name, pattern in patterns.items():
        if name == 'api_key' or name == 'secret':
            # 3-group patterns: (key_name)(separator)(value)
            def key_replacer(match, vc=visible_chars):
                key_name = match.group(1)
                separator = match.group(2)
                value = match.group(3)
                return f"{key_name}{separator}{mask_value(value, vc)}"
            result = pattern.sub(key_replacer, result)
        elif name == 'bearer_token':
            # 2-group pattern: (bearer )(token)
            def bearer_replacer(match, vc=visible_chars):
                prefix = match.group(1)
                value = match.group(2)
                return f"{prefix}{mask_value(value, vc)}"
            result = pattern.sub(bearer_replacer, result)
        elif name == 'jwt':
            # JWT tokens - mask middle and end parts
            def jwt_replacer(match):
                token = match.group(0)
                parts = token.split('.')
                if len(parts) == 3:
                    return f"{parts[0][:20]}...{mask_value(parts[2], 4)}"
                return mask_value(token, 10)
            result = pattern.sub(jwt_replacer, result)
        elif name == 'credit_card':
            # Credit cards - show only last 4 digits
            def cc_replacer(match):
                cc = re.sub(r'[-\s]', '', match.group(0))
                return f"****-****-****-{cc[-4:]}"
            result = pattern.sub(cc_replacer, result)
        elif name == 'email':
            # Emails - mask the local part
            def email_replacer(match):
                email = match.group(0)
                local, domain = email.rsplit('@', 1)
                masked_local = mask_value(local, 2)
                return f"{masked_local}@{domain}"
            result = pattern.sub(email_replacer, result)
        elif name == 'ip_address':
            # IP addresses - mask last two octets
            def ip_replacer(match):
                ip = match.group(0)
                parts = ip.split('.')
                return f"{parts[0]}.{parts[1]}.***.***"
            result = pattern.sub(ip_replacer, result)

    return result


def mask_dict_values(
    data: Dict[str, Any],
    sensitive_keys: frozenset = None,
    visible_chars: int = 4
) -> Dict[str, Any]:
    """
    Mask sensitive values in a dictionary.

    Args:
        data: Dictionary potentially containing sensitive data
        sensitive_keys: Keys to mask (defaults to SENSITIVE_KEYWORDS)
        visible_chars: Characters to keep visible

    Returns:
        Dictionary with sensitive values masked
    """
    if not isinstance(data, dict):
        return data

    sensitive_keys = sensitive_keys or SENSITIVE_KEYWORDS
    result = {}

    for key, value in data.items():
        key_lower = str(key).lower()

        if key_lower in sensitive_keys or any(kw in key_lower for kw in sensitive_keys):
            # This key contains sensitive data
            if isinstance(value, str):
                result[key] = mask_value(value, visible_chars)
            elif isinstance(value, dict):
                result[key] = mask_dict_values(value, sensitive_keys, visible_chars)
            elif value is not None:
                result[key] = '***MASKED***'
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = mask_dict_values(value, sensitive_keys, visible_chars)
        elif isinstance(value, str):
            # Check if the string value contains sensitive data
            result[key] = mask_sensitive_values(value, visible_chars=visible_chars)
        elif isinstance(value, list):
            result[key] = [
                mask_dict_values(item, sensitive_keys, visible_chars)
                if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def get_masked_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a copy of configuration with sensitive values masked.

    Useful for logging configuration at startup without exposing secrets.

    Args:
        config: Configuration dictionary

    Returns:
        Configuration with sensitive values masked
    """
    return mask_dict_values(config)


class SensitiveFilter(logging.Filter):
    """
    Logging filter that masks sensitive values in log messages.

    Usage:
        logger = logging.getLogger('mylogger')
        logger.addFilter(SensitiveFilter())
    """

    def __init__(
        self,
        patterns: Dict[str, Pattern] = None,
        visible_chars: int = 4,
        name: str = ''
    ):
        """
        Initialize the filter.

        Args:
            patterns: Custom patterns to mask
            visible_chars: Characters to keep visible
            name: Filter name
        """
        super().__init__(name)
        self.patterns = patterns or SENSITIVE_PATTERNS
        self.visible_chars = visible_chars

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record, masking sensitive values.

        Args:
            record: Log record to filter

        Returns:
            True (always allows the record through, just modifies it)
        """
        # Mask the main message
        if record.msg and isinstance(record.msg, str):
            record.msg = mask_sensitive_values(
                record.msg,
                self.patterns,
                self.visible_chars
            )

        # Mask any arguments
        if record.args:
            if isinstance(record.args, dict):
                record.args = mask_dict_values(record.args, visible_chars=self.visible_chars)
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    mask_sensitive_values(str(arg), self.patterns, self.visible_chars)
                    if isinstance(arg, str) else arg
                    for arg in record.args
                )

        return True


def setup_sensitive_logging(
    logger: logging.Logger = None,
    patterns: Dict[str, Pattern] = None
) -> None:
    """
    Add sensitive data filtering to a logger.

    Args:
        logger: Logger to configure (root logger if None)
        patterns: Custom patterns to mask
    """
    target_logger = logger or logging.getLogger()
    sensitive_filter = SensitiveFilter(patterns=patterns)
    target_logger.addFilter(sensitive_filter)
