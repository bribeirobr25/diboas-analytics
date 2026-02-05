"""
Checksum utilities for data integrity verification.

Provides file hashing and record counting.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.utils.audit.models import DataChecksum


def generate_checksum(filepath: Path, algorithm: str = 'sha256') -> str:
    """
    Generate checksum for a file.

    Args:
        filepath: Path to file
        algorithm: Hash algorithm (sha256, md5)

    Returns:
        Hex digest of file hash
    """
    hash_func = hashlib.new(algorithm)

    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def count_records(filepath: Path) -> Optional[int]:
    """
    Count records in a data file.

    Args:
        filepath: Path to file

    Returns:
        Number of records or None if not countable
    """
    suffix = filepath.suffix.lower()

    try:
        if suffix == '.csv':
            with open(filepath, 'r') as f:
                return sum(1 for _ in f) - 1  # Subtract header
        elif suffix == '.json':
            with open(filepath, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return len(data)
                elif isinstance(data, dict) and 'results' in data:
                    return len(data['results'])
        return None
    except Exception:
        return None


def create_data_checksum(filepath: Path) -> DataChecksum:
    """
    Create checksum record for a data file.

    Args:
        filepath: Path to file

    Returns:
        DataChecksum object
    """
    stat = filepath.stat()

    return DataChecksum(
        filepath=str(filepath.absolute()),
        filename=filepath.name,
        checksum=generate_checksum(filepath),
        algorithm='sha256',
        size_bytes=stat.st_size,
        last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
        record_count=count_records(filepath)
    )
