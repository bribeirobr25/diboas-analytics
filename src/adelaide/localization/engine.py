"""
Localization Engine for Adelaide.

Handles translation and cultural adaptation for different locales.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

from src.adelaide.localization.constants import (
    SUPPORTED_LOCALES,
    AI_DISCLOSURE,
    TRADFI_GAP_DISCLOSURE,
    REGIONAL_DISCLAIMERS,
    HYPOTHETICAL_DISCLAIMERS,
)
from src.adelaide.localization.locales import TRANSLATIONS

logger = logging.getLogger(__name__)


class LocalizationEngine:
    """
    Localization engine for Adelaide content.

    Handles translation and cultural adaptation.

    Usage:
        engine = LocalizationEngine()
        translated = engine.localize(content, 'pt-br')
    """

    def __init__(self, default_locale: str = 'en'):
        """Initialize with default locale."""
        self.default_locale = default_locale

    def translate(self, key: str, locale: str = None) -> str:
        """
        Translate a key to the specified locale.

        Args:
            key: Translation key
            locale: Target locale (default: self.default_locale)

        Returns:
            Translated string or key if not found
        """
        locale = locale or self.default_locale

        if locale not in TRANSLATIONS:
            logger.warning(f"Unsupported locale: {locale}, falling back to en")
            locale = 'en'

        translations = TRANSLATIONS.get(locale, {})
        return translations.get(key, TRANSLATIONS['en'].get(key, key))

    def get_greeting(self, locale: str = None, hour: int = None) -> str:
        """
        Get time-appropriate greeting.

        Args:
            locale: Target locale
            hour: Hour of day (0-23), defaults to current

        Returns:
            Localized greeting
        """
        if hour is None:
            hour = datetime.now().hour

        if 5 <= hour < 12:
            key = 'good_morning'
        elif 12 <= hour < 18:
            key = 'good_afternoon'
        else:
            key = 'good_evening'

        return self.translate(key, locale)

    def get_disclaimer(self, locale: str = None) -> str:
        """Get full disclaimer for locale."""
        locale = locale or self.default_locale
        return REGIONAL_DISCLAIMERS.get(locale, REGIONAL_DISCLAIMERS['en'])

    def get_hypothetical_disclaimer(self, locale: str = None) -> str:
        """
        Get hypothetical performance disclaimer for locale.

        Required for Monte Carlo and Battle Test outputs per SEC Marketing Rule.
        """
        locale = locale or self.default_locale
        return HYPOTHETICAL_DISCLAIMERS.get(locale, HYPOTHETICAL_DISCLAIMERS['en'])

    def get_ai_disclosure(self, locale: str = None) -> str:
        """
        Get AI disclosure for locale.

        Required for California SB 942 compliance.
        Placement: After signature, before footer/disclaimers.

        Args:
            locale: Target locale

        Returns:
            Localized AI disclosure string
        """
        locale = locale or self.default_locale
        return AI_DISCLOSURE.get(locale, AI_DISCLOSURE['en'])

    def get_tradfi_gap_disclosure(
        self,
        gap_type: str,
        locale: str = None,
        data_date: str = None
    ) -> str:
        """
        Get TradFi gap disclosure for locale.

        Used when US stock markets are closed (weekends/holidays)
        or when data is not yet available (pre-market close).

        Args:
            gap_type: Type of gap ('weekend', 'holiday', 'pre_market_close')
            locale: Target locale
            data_date: Optional date string to include in disclosure

        Returns:
            Localized TradFi gap disclosure string, or empty string if no gap
        """
        locale = locale or self.default_locale

        if gap_type not in TRADFI_GAP_DISCLOSURE:
            return ""

        disclosure = TRADFI_GAP_DISCLOSURE[gap_type].get(
            locale, TRADFI_GAP_DISCLOSURE[gap_type]['en']
        )

        # Optionally append the specific date
        if data_date:
            date_suffix = {
                'en': f" (Data as of {data_date})",
                'pt-br': f" (Dados de {data_date})",
                'de': f" (Daten vom {data_date})",
                'es': f" (Datos del {data_date})",
            }
            disclosure += date_suffix.get(locale, date_suffix['en'])

        return disclosure

    def format_number(self, value: float, locale: str = None) -> str:
        """Format number for locale."""
        locale = locale or self.default_locale

        if locale == 'pt-br':
            # Brazilian format: 1.234,56
            return f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            # US/UK format: 1,234.56
            return f"{value:,.2f}"

    def format_currency(self, value: float, locale: str = None, currency: str = 'USD') -> str:
        """Format currency for locale."""
        locale = locale or self.default_locale
        formatted = self.format_number(value, locale)

        if currency == 'USD':
            return f"${formatted}"
        elif currency == 'EUR':
            if locale == 'pt-br':
                return f"{formatted} EUR"
            return f"EUR {formatted}"
        elif currency == 'BRL':
            return f"R$ {formatted}"
        else:
            return f"{formatted} {currency}"

    def format_percent(self, value: float, locale: str = None, show_sign: bool = True) -> str:
        """Format percentage for locale."""
        locale = locale or self.default_locale

        if show_sign:
            sign = '+' if value > 0 else ''
        else:
            sign = ''

        if locale == 'pt-br':
            return f"{sign}{value:.2f}%".replace('.', ',')
        else:
            return f"{sign}{value:.2f}%"

    def localize_content(self, content: Dict[str, Any], locale: str = None) -> Dict[str, Any]:
        """
        Localize a content dictionary.

        Translates known keys and formats numbers/currencies.

        Args:
            content: Content dictionary
            locale: Target locale

        Returns:
            Localized content dictionary
        """
        locale = locale or self.default_locale
        localized = content.copy()

        # Add localized strings
        localized['locale'] = locale
        localized['greeting'] = self.get_greeting(locale)
        localized['disclaimer'] = self.get_disclaimer(locale)
        localized['ai_disclosure'] = self.get_ai_disclosure(locale)
        localized['you_decide'] = self.translate('you_decide', locale)

        # Translate known keys
        for key in ['market_snapshot', 'fear_greed_index', 'whale_watch', 'strategy_overview']:
            if key in localized:
                localized[f'{key}_label'] = self.translate(key, locale)

        return localized

    def get_fear_greed_label(self, value: int, locale: str = None) -> str:
        """Get localized Fear & Greed label."""
        locale = locale or self.default_locale

        if value <= 20:
            return self.translate('extreme_fear', locale)
        elif value <= 40:
            return self.translate('fear', locale)
        elif value <= 60:
            return self.translate('neutral', locale)
        elif value <= 80:
            return self.translate('greed', locale)
        else:
            return self.translate('extreme_greed', locale)

    @staticmethod
    def is_supported(locale: str) -> bool:
        """Check if locale is supported."""
        return locale in SUPPORTED_LOCALES

    @staticmethod
    def get_supported_locales() -> list:
        """Get list of supported locales."""
        return SUPPORTED_LOCALES.copy()
