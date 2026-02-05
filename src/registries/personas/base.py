"""
Base classes for Adelaide personas.

Provides the abstract base class and shared utilities for all personas.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from enum import Enum


# Technical term replacements for simpler personas
TECHNICAL_TERMS = {
    'APY': 'yearly return',
    'TVL': 'total money in protocol',
    'DeFi': 'crypto savings',
    'smart contract': 'automated system',
    'impermanent loss': 'temporary value changes',
    'Sharpe ratio': 'risk-adjusted return',
    'drawdown': 'decline from peak',
    'volatility': 'price swings',
    'liquidity': 'available funds',
    'protocol': 'platform',
    'yield': 'return',
    'staking': 'earning rewards',
    'collateral': 'backed value',
}


class EmojiLevel(Enum):
    """Emoji usage level for personas."""
    NONE = "none"           # No emojis (Felipe, B2B)
    MINIMAL = "minimal"     # 1-3 emojis (Yield Hunter)
    MODERATE = "moderate"   # 3-8 emojis (Maria)
    HIGH = "high"           # 8-15 emojis (Ana)


class Persona(ABC):
    """
    Abstract base class for all Adelaide personas.

    Personas adapt content to different communication styles
    based on user risk profile and preferences.
    """

    @abstractmethod
    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """
        Adapt content to this persona's voice.

        Args:
            content: Base content to adapt (from Adelaide generator)
            locale: Language locale (en, pt-br, de, es)

        Returns:
            Adapted content with persona's voice
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return persona name."""
        pass

    @property
    @abstractmethod
    def emoji_level(self) -> EmojiLevel:
        """Return emoji usage level."""
        pass

    @property
    @abstractmethod
    def risk_profile(self) -> str:
        """
        Return target risk profile.

        Returns:
            One of: 'conservative', 'balanced', 'aggressive', 'institutional'
        """
        pass

    def get_signature(self, locale: str = "en") -> str:
        """Get persona's signature for newsletter sign-off."""
        return f"— {self.name}"
