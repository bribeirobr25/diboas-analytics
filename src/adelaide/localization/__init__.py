"""
Adelaide Localization Package.

Handles translation and cultural adaptation for different locales.

Supported locales:
- en: English (US)
- pt-br: Portuguese (Brazil)
- de: German (formal Sie form)
- es: Spanish (Latin American)

Usage:
    from src.adelaide.localization import LocalizationEngine

    engine = LocalizationEngine()
    greeting = engine.get_greeting('pt-br')
    translated = engine.translate('market_snapshot', 'de')
"""

from src.adelaide.localization.engine import LocalizationEngine
from src.adelaide.localization.constants import (
    SUPPORTED_LOCALES,
    AI_DISCLOSURE,
    TRADFI_GAP_DISCLOSURE,
    REGIONAL_DISCLAIMERS,
    HYPOTHETICAL_DISCLAIMERS,
)
from src.adelaide.localization.locales import TRANSLATIONS

__all__ = [
    'LocalizationEngine',
    'SUPPORTED_LOCALES',
    'AI_DISCLOSURE',
    'TRADFI_GAP_DISCLOSURE',
    'REGIONAL_DISCLAIMERS',
    'HYPOTHETICAL_DISCLAIMERS',
    'TRANSLATIONS',
]
