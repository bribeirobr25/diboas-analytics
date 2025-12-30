"""
Configuration hashing utilities for audit trail.

Generates hashes of configuration to track changes.
"""

import hashlib
import json
from pathlib import Path
from typing import Any


def hash_config(config: dict) -> str:
    """
    Generate SHA-256 hash of a configuration dictionary.

    Args:
        config: Configuration dictionary

    Returns:
        Hex string of hash (first 12 characters)
    """
    # Serialize to JSON with sorted keys for consistency
    config_str = json.dumps(config, sort_keys=True, default=str)
    hash_obj = hashlib.sha256(config_str.encode())
    return hash_obj.hexdigest()[:12]


def hash_file(filepath: Path) -> str:
    """
    Generate SHA-256 hash of a file.

    Args:
        filepath: Path to file

    Returns:
        Hex string of hash (first 12 characters)
    """
    hash_obj = hashlib.sha256()

    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()[:12]


def hash_strategies(strategies: list[dict]) -> str:
    """
    Generate hash of strategy definitions.

    Args:
        strategies: List of strategy dictionaries

    Returns:
        Hex string of hash
    """
    # Extract only allocation-relevant fields
    simplified = []
    for s in strategies:
        simplified.append({
            'id': s.get('id'),
            'allocations': s.get('allocations'),
            'crypto_pct': s.get('crypto_pct')
        })

    return hash_config({'strategies': simplified})


def generate_run_id(prefix: str = 'run') -> str:
    """
    Generate unique run ID.

    Format: {prefix}-{timestamp}-{random}

    Args:
        prefix: Prefix for the ID

    Returns:
        Unique run ID string
    """
    import time
    import random

    timestamp = int(time.time())
    random_suffix = ''.join(random.choices('abcdef0123456789', k=6))

    return f"{prefix}-{timestamp}-{random_suffix}"


def verify_config_hash(config: dict, expected_hash: str) -> bool:
    """
    Verify that a configuration matches an expected hash.

    Args:
        config: Configuration dictionary
        expected_hash: Expected hash value

    Returns:
        True if hashes match
    """
    actual_hash = hash_config(config)
    return actual_hash == expected_hash
