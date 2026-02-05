"""
Security input validation utilities.

Provides path traversal checks, safe path validation, and filename sanitization
to prevent directory traversal attacks and other security issues.
"""

import re
import os
from pathlib import Path
from typing import Optional, Union, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PathSecurityError(Exception):
    """Raised when a path fails security validation."""

    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Path security error: {reason} (path: {path})")


# Allowed base directories for file operations
ALLOWED_DIRECTORIES: List[Path] = []


def set_allowed_directories(directories: List[Union[str, Path]]) -> None:
    """
    Set the allowed base directories for file operations.

    Args:
        directories: List of allowed base directories
    """
    global ALLOWED_DIRECTORIES
    ALLOWED_DIRECTORIES = [Path(d).resolve() for d in directories]


def is_path_traversal(path: Union[str, Path]) -> bool:
    """
    Check if a path contains directory traversal sequences.

    Args:
        path: Path to check

    Returns:
        True if path contains traversal sequences, False otherwise
    """
    path_str = str(path)

    # Check for common traversal patterns
    traversal_patterns = [
        '..',           # Parent directory
        '/./',          # Current directory (redundant)
        '\\..\\',       # Windows traversal
        '%2e%2e',       # URL-encoded ..
        '%252e%252e',   # Double URL-encoded ..
        '..%c0%af',     # Unicode encoding bypass
        '..%c1%9c',     # Unicode encoding bypass
    ]

    for pattern in traversal_patterns:
        if pattern in path_str.lower():
            return True

    # Check if normalized path differs from input (may indicate traversal)
    try:
        normalized = os.path.normpath(path_str)
        if '..' in normalized:
            return True
    except (ValueError, OSError):
        return True

    return False


def validate_safe_path(
    path: Union[str, Path],
    allowed_dirs: List[Union[str, Path]] = None,
    must_exist: bool = False,
    allow_symlinks: bool = False
) -> Path:
    """
    Validate that a path is safe for file operations.

    Args:
        path: Path to validate
        allowed_dirs: List of allowed base directories (uses global if None)
        must_exist: Whether the path must already exist
        allow_symlinks: Whether to allow symbolic links

    Returns:
        Resolved Path object if valid

    Raises:
        PathSecurityError: If path fails validation
    """
    path_obj = Path(path)

    # Check for traversal sequences first
    if is_path_traversal(path):
        raise PathSecurityError(str(path), "Path contains directory traversal sequences")

    # Resolve the path to absolute
    try:
        resolved = path_obj.resolve()
    except (OSError, ValueError) as e:
        raise PathSecurityError(str(path), f"Cannot resolve path: {e}")

    # Check if path must exist
    if must_exist and not resolved.exists():
        raise PathSecurityError(str(path), "Path does not exist")

    # Check for symbolic links if not allowed
    if not allow_symlinks and resolved.exists() and resolved.is_symlink():
        raise PathSecurityError(str(path), "Symbolic links are not allowed")

    # Check against allowed directories
    dirs_to_check = allowed_dirs or ALLOWED_DIRECTORIES
    if dirs_to_check:
        is_allowed = False
        for allowed_dir in dirs_to_check:
            allowed_resolved = Path(allowed_dir).resolve()
            try:
                resolved.relative_to(allowed_resolved)
                is_allowed = True
                break
            except ValueError:
                continue

        if not is_allowed:
            allowed_str = ", ".join(str(d) for d in dirs_to_check)
            raise PathSecurityError(
                str(path),
                f"Path is outside allowed directories: {allowed_str}"
            )

    return resolved


def validate_output_path(
    path: Union[str, Path],
    base_dir: Union[str, Path] = None
) -> Path:
    """
    Validate an output path and ensure it's within the allowed output directory.

    Args:
        path: Output path to validate
        base_dir: Required base directory for output

    Returns:
        Validated Path object

    Raises:
        PathSecurityError: If path is invalid or outside base_dir
    """
    path_obj = Path(path)

    # Check for traversal
    if is_path_traversal(path):
        raise PathSecurityError(str(path), "Output path contains directory traversal")

    # If base_dir specified, ensure path is within it
    if base_dir:
        base_resolved = Path(base_dir).resolve()

        # If path is relative, join with base
        if not path_obj.is_absolute():
            path_obj = base_resolved / path_obj

        resolved = path_obj.resolve()

        try:
            resolved.relative_to(base_resolved)
        except ValueError:
            raise PathSecurityError(
                str(path),
                f"Output path must be within {base_dir}"
            )

        return resolved

    return path_obj.resolve()


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename by removing unsafe characters.

    Args:
        filename: Filename to sanitize
        max_length: Maximum allowed filename length

    Returns:
        Sanitized filename
    """
    # Remove directory separators
    filename = filename.replace('/', '_').replace('\\', '_')

    # Remove null bytes and control characters
    filename = ''.join(c for c in filename if ord(c) >= 32 and c != '\x7f')

    # Remove other dangerous characters
    unsafe_chars = '<>:"|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')

    # Collapse multiple underscores
    filename = re.sub(r'_+', '_', filename)

    # Strip leading/trailing whitespace and dots
    filename = filename.strip('. \t\n\r')

    # Truncate if too long (preserve extension)
    if len(filename) > max_length:
        name_part, _, ext = filename.rpartition('.')
        if ext and len(ext) < 10:
            max_name = max_length - len(ext) - 1
            filename = f"{name_part[:max_name]}.{ext}"
        else:
            filename = filename[:max_length]

    # Ensure we have a valid filename
    if not filename or filename in ('.', '..'):
        filename = 'unnamed_file'

    return filename


def validate_date_format(
    date_str: str,
    formats: List[str] = None
) -> Optional[datetime]:
    """
    Validate and parse a date string securely.

    Args:
        date_str: Date string to validate
        formats: List of allowed date formats (default: YYYY-MM-DD)

    Returns:
        Parsed datetime or None if invalid
    """
    if not date_str or not isinstance(date_str, str):
        return None

    # Limit string length to prevent DoS
    if len(date_str) > 50:
        logger.warning(f"Date string too long: {len(date_str)} characters")
        return None

    allowed_formats = formats or ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y']

    for fmt in allowed_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None


def validate_identifier(
    identifier: str,
    pattern: str = r'^[a-zA-Z0-9_-]+$',
    max_length: int = 100
) -> bool:
    """
    Validate an identifier (e.g., API key name, source name).

    Args:
        identifier: String to validate
        pattern: Regex pattern for valid characters
        max_length: Maximum allowed length

    Returns:
        True if valid, False otherwise
    """
    if not identifier or not isinstance(identifier, str):
        return False

    if len(identifier) > max_length:
        return False

    return bool(re.match(pattern, identifier))
