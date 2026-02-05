"""
Adelaide Personas Package.

Provides persona classes for content adaptation based on user profiles.

Personas available:
- AnaPersona: Conservative, warm grandmother voice (strategies 1, 3, 5, 7, 9)
- MariaPersona: Balanced, friendly teacher voice (strategies 2, 4, 6)
- FelipePersona: Aggressive, technical analyst voice (strategies 8, 10)
- YieldHunterPersona: DeFi-native, yield-focused voice
- B2BClientPersona: Institutional, audit-ready voice

Usage:
    from src.registries.persona_registry import PersonaRegistry

    persona = PersonaRegistry.get_instance().get("ana", {})
    adapted = persona.adapt(content, locale="en")
"""

from src.registries.personas.base import (
    Persona,
    EmojiLevel,
    TECHNICAL_TERMS,
)
from src.registries.personas.ana import AnaPersona
from src.registries.personas.maria import MariaPersona
from src.registries.personas.felipe import FelipePersona
from src.registries.personas.yield_hunter import YieldHunterPersona
from src.registries.personas.b2b_client import B2BClientPersona

__all__ = [
    'Persona',
    'EmojiLevel',
    'TECHNICAL_TERMS',
    'AnaPersona',
    'MariaPersona',
    'FelipePersona',
    'YieldHunterPersona',
    'B2BClientPersona',
]
