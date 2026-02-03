"""
Safe file I/O utilities with atomic writes and empty rejection.

This module provides safe file writing utilities that:
1. Reject empty/None data to prevent data loss
2. Use atomic writes (temp file + rename) to prevent corruption
3. Ensure durability with fsync before rename
4. Clean up temp files on failure

Usage:
    from src.utils.file_io import safe_write_csv, safe_write_json, safe_write_text

    # For collectors - strict mode (rejects empty)
    safe_write_csv(df, "data/prices.csv")

    # For reporters - may allow empty (no signals today)
    safe_write_csv(df, "output/signals.csv", allow_empty=True)
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd

logger = logging.getLogger(__name__)


def safe_write_csv(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    min_rows: int = 1,
    allow_empty: bool = False,
) -> bool:
    """
    Atomic CSV write with empty rejection.

    Protects against:
    - Data loss from empty API responses overwriting good data
    - Partial/corrupt files from interrupted writes
    - Race conditions with PID-based temp filenames

    Args:
        df: DataFrame to write
        filepath: Target file path
        min_rows: Minimum rows required (default 1)
        allow_empty: If True, allows empty DataFrames (for reporters with "no signals")

    Returns:
        True if written successfully, False if rejected

    Raises:
        Exception: Re-raises any write errors after cleanup
    """
    filepath = Path(filepath)

    # Reject empty/None DataFrames
    if df is None:
        logger.warning(f"Rejecting None write to {filepath}")
        return False

    if df.empty and not allow_empty:
        logger.warning(f"Rejecting empty DataFrame write to {filepath}")
        return False

    if len(df) < min_rows and not allow_empty:
        logger.warning(
            f"Rejecting write to {filepath}: {len(df)} rows < min {min_rows}"
        )
        return False

    # Temp file in SAME directory (required for atomic os.replace on same filesystem)
    # PID in filename prevents collision with concurrent processes
    temp_path = filepath.parent / f"{filepath.name}.{os.getpid()}.tmp"

    try:
        # Write with BOM for Portuguese character support in Excel
        df.to_csv(temp_path, index=False, encoding="utf-8-sig")

        # Flush and sync to disk (durability, not just atomicity)
        # Use "rb" mode - we just need the file descriptor for fsync, don't modify content
        with open(temp_path, "rb") as f:
            os.fsync(f.fileno())

        # Atomic rename (on POSIX systems)
        os.replace(temp_path, filepath)
        logger.info(f"Successfully wrote {len(df)} rows to {filepath}")
        return True

    except Exception as e:
        logger.error(f"Write failed for {filepath}: {e}")
        # Cleanup orphan temp file
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_error}")
        raise


def safe_write_json(
    data: Dict[str, Any],
    filepath: Union[str, Path],
    allow_none: bool = False,
) -> bool:
    """
    Atomic JSON write with validation.

    Args:
        data: Dictionary to write as JSON
        filepath: Target file path
        allow_none: If True, allows None data (writes empty dict)

    Returns:
        True if written successfully, False if rejected

    Raises:
        Exception: Re-raises any write errors after cleanup
    """
    filepath = Path(filepath)

    if data is None:
        if allow_none:
            data = {}
        else:
            logger.warning(f"Rejecting None write to {filepath}")
            return False

    temp_path = filepath.parent / f"{filepath.name}.{os.getpid()}.tmp"

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, filepath)
        logger.info(f"Successfully wrote JSON to {filepath}")
        return True

    except Exception as e:
        logger.error(f"JSON write failed for {filepath}: {e}")
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_error}")
        raise


def safe_write_text(
    content: str,
    filepath: Union[str, Path],
    allow_empty: bool = False,
) -> bool:
    """
    Atomic text/markdown write with validation.

    Args:
        content: Text content to write
        filepath: Target file path
        allow_empty: If True, allows empty strings

    Returns:
        True if written successfully, False if rejected

    Raises:
        Exception: Re-raises any write errors after cleanup
    """
    filepath = Path(filepath)

    if content is None:
        logger.warning(f"Rejecting None write to {filepath}")
        return False

    if not content.strip() and not allow_empty:
        logger.warning(f"Rejecting empty text write to {filepath}")
        return False

    temp_path = filepath.parent / f"{filepath.name}.{os.getpid()}.tmp"

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, filepath)
        logger.info(f"Successfully wrote text to {filepath}")
        return True

    except Exception as e:
        logger.error(f"Text write failed for {filepath}: {e}")
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_error}")
        raise
