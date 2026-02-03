"""
Strategy allocation validators.

Validates strategy configurations against business rules:
- Sky protocol concentration cap (30% max)
- Allocation sums must equal 100%
- Crypto percentages must match allocations
"""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from src.domain.strategy import Strategy

logger = logging.getLogger(__name__)

# Sky protocol concentration cap (Strategy Board mandate, Feb 2026)
MAX_SKY_ALLOCATION = 0.30
FLOAT_TOLERANCE = 0.0001


def validate_sky_cap(strategies: List[Dict[str, Any]]) -> List[str]:
    """
    Validate no strategy exceeds 30% Sky allocation.

    The Strategy Board mandated a maximum 30% concentration in any single
    protocol to reduce risk. This applies to all Sky allocations.

    Args:
        strategies: List of strategy dicts with 'allocations' field

    Returns:
        List of violation messages (empty = valid)
    """
    violations = []

    for s in strategies:
        strategy_id = s.get('id', 'unknown')
        strategy_name = s.get('name', 'unknown')
        sky = s.get('allocations', {}).get('stable', {}).get('sky', 0)

        if sky > MAX_SKY_ALLOCATION + FLOAT_TOLERANCE:
            violations.append(
                f"Strategy {strategy_id} ({strategy_name}): Sky at {sky*100:.1f}% exceeds 30% cap"
            )

    return violations


def validate_allocations_sum(strategies: List[Dict[str, Any]]) -> List[str]:
    """
    Validate all strategy allocations sum to 100%.

    Args:
        strategies: List of strategy dicts

    Returns:
        List of violation messages (empty = valid)
    """
    violations = []

    for s in strategies:
        strategy_id = s.get('id', 'unknown')
        strategy_name = s.get('name', 'unknown')

        stable_sum = sum(s.get('allocations', {}).get('stable', {}).values())
        crypto_sum = sum(s.get('allocations', {}).get('crypto', {}).values())
        total = stable_sum + crypto_sum

        if abs(total - 1.0) > FLOAT_TOLERANCE:
            violations.append(
                f"Strategy {strategy_id} ({strategy_name}): Allocations sum to {total*100:.1f}%, not 100%"
            )

    return violations


def validate_crypto_pct_matches(strategies: List[Dict[str, Any]]) -> List[str]:
    """
    Validate crypto_pct field matches actual crypto allocations.

    Args:
        strategies: List of strategy dicts

    Returns:
        List of violation messages (empty = valid)
    """
    violations = []

    for s in strategies:
        strategy_id = s.get('id', 'unknown')
        strategy_name = s.get('name', 'unknown')

        declared_crypto_pct = s.get('crypto_pct', 0) / 100  # Convert from percentage
        actual_crypto_sum = sum(s.get('allocations', {}).get('crypto', {}).values())

        if abs(declared_crypto_pct - actual_crypto_sum) > FLOAT_TOLERANCE:
            violations.append(
                f"Strategy {strategy_id} ({strategy_name}): crypto_pct={declared_crypto_pct*100:.0f}% "
                f"doesn't match crypto allocations sum={actual_crypto_sum*100:.0f}%"
            )

    return violations


def validate_all(strategies: List[Dict[str, Any]]) -> List[str]:
    """
    Run all strategy validations.

    Args:
        strategies: List of strategy dicts

    Returns:
        List of all violation messages (empty = all valid)
    """
    violations = []
    violations.extend(validate_sky_cap(strategies))
    violations.extend(validate_allocations_sum(strategies))
    violations.extend(validate_crypto_pct_matches(strategies))
    return violations


def validate_strategies_json(filepath: str = 'config/strategies.json') -> bool:
    """
    Load and validate strategies.json file.

    Args:
        filepath: Path to strategies.json

    Returns:
        True if all validations pass

    Raises:
        ValueError: If any validation fails
    """
    import json
    from pathlib import Path

    with open(Path(filepath)) as f:
        data = json.load(f)

    strategies = data.get('strategies', [])
    violations = validate_all(strategies)

    if violations:
        for v in violations:
            logger.error(v)
        raise ValueError(f"Strategy validation failed: {len(violations)} violations found")

    logger.info(f"All {len(strategies)} strategies passed validation")
    return True
