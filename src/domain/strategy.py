"""
Strategy domain model for diBoaS Analytics.

Represents an investment strategy with its allocations and risk parameters.
"""

from dataclasses import dataclass, field
from typing import Optional
import json
from pathlib import Path


@dataclass
class StrategyAllocation:
    """Allocation to a single protocol."""
    protocol: str
    weight: float  # 0.0 to 1.0

    def __post_init__(self):
        if not 0 <= self.weight <= 1:
            raise ValueError(f"Weight must be between 0 and 1, got {self.weight}")


@dataclass
class Strategy:
    """
    Investment strategy definition.

    Represents one of the 10 diBoaS investment strategies.
    """
    id: int
    name: str
    goal: str
    crypto_pct: int  # 0-100
    risk_tier: str
    stable_allocations: dict[str, float] = field(default_factory=dict)
    crypto_allocations: dict[str, float] = field(default_factory=dict)
    target_apy_range: Optional[str] = None
    target_user: Optional[str] = None
    variance_warning: Optional[str] = None

    def __post_init__(self):
        # Validate allocations sum to 1.0
        total = sum(self.stable_allocations.values()) + sum(self.crypto_allocations.values())
        if not 0.99 <= total <= 1.01:  # Allow small floating point error
            raise ValueError(f"Strategy {self.id} allocations sum to {total}, expected 1.0")

        # Validate crypto_pct matches crypto allocations
        actual_crypto = sum(self.crypto_allocations.values()) * 100
        if abs(actual_crypto - self.crypto_pct) > 1:  # Allow 1% tolerance
            raise ValueError(
                f"Strategy {self.id} crypto_pct ({self.crypto_pct}) doesn't match "
                f"crypto allocations ({actual_crypto})"
            )

    @property
    def is_stable_only(self) -> bool:
        """Check if strategy has no crypto exposure."""
        return self.crypto_pct == 0

    @property
    def all_allocations(self) -> dict[str, float]:
        """Get all allocations combined."""
        return {**self.stable_allocations, **self.crypto_allocations}

    def get_chain_allocations(self) -> dict[str, float]:
        """Get allocations grouped by chain."""
        from config.protocols import PROTOCOLS
        chains = {}
        for protocol, weight in self.all_allocations.items():
            chain = PROTOCOLS.get(protocol, {}).get('chain', 'unknown')
            chains[chain] = chains.get(chain, 0) + weight
        return chains


class StrategyLoader:
    """Load strategies from JSON configuration."""

    @staticmethod
    def load_from_file(filepath: Path) -> list[Strategy]:
        """Load all strategies from a JSON file."""
        with open(filepath) as f:
            data = json.load(f)

        strategies = []
        for s in data['strategies']:
            strategy = Strategy(
                id=s['id'],
                name=s['name'],
                goal=s['goal'],
                crypto_pct=s['crypto_pct'],
                risk_tier=s.get('risk_tier', 'Unknown'),
                stable_allocations=s['allocations'].get('stable', {}),
                crypto_allocations=s['allocations'].get('crypto', {}),
                target_apy_range=s.get('target_apy_range'),
                target_user=s.get('target_user'),
                variance_warning=s.get('variance_warning')
            )
            strategies.append(strategy)

        return strategies

    @staticmethod
    def load_default() -> list[Strategy]:
        """Load strategies from default config location."""
        from config.settings import CONFIG_DIR
        return StrategyLoader.load_from_file(CONFIG_DIR / 'strategies.json')

    @staticmethod
    def get_strategy_by_id(strategy_id: int, strategies: list['Strategy'] = None) -> 'Strategy':
        """Get a single strategy by ID."""
        if strategies is None:
            strategies = StrategyLoader.load_default()

        for s in strategies:
            if s.id == strategy_id:
                return s
        raise ValueError(f"Strategy {strategy_id} not found")

    @staticmethod
    def get_stable_strategies(strategies: list['Strategy'] = None) -> list['Strategy']:
        """Get all strategies with 0% crypto exposure."""
        if strategies is None:
            strategies = StrategyLoader.load_default()
        return [s for s in strategies if s.is_stable_only]

    @staticmethod
    def get_crypto_strategies(strategies: list['Strategy'] = None) -> list['Strategy']:
        """Get all strategies with crypto exposure."""
        if strategies is None:
            strategies = StrategyLoader.load_default()
        return [s for s in strategies if not s.is_stable_only]
