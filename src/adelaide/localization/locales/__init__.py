"""
Locale translations package.

Each locale file contains the TRANSLATIONS dictionary for that language.
"""

from src.adelaide.localization.locales.en import TRANSLATIONS_EN
from src.adelaide.localization.locales.pt_br import TRANSLATIONS_PT_BR
from src.adelaide.localization.locales.de import TRANSLATIONS_DE
from src.adelaide.localization.locales.es import TRANSLATIONS_ES

# Combined translations dictionary
TRANSLATIONS = {
    'en': TRANSLATIONS_EN,
    'pt-br': TRANSLATIONS_PT_BR,
    'de': TRANSLATIONS_DE,
    'es': TRANSLATIONS_ES,
}

__all__ = [
    'TRANSLATIONS',
    'TRANSLATIONS_EN',
    'TRANSLATIONS_PT_BR',
    'TRANSLATIONS_DE',
    'TRANSLATIONS_ES',
]
