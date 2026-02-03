"""
Localization Engine for Adelaide.

Handles translation and cultural adaptation for different locales.
Phase 1: String dictionary approach
Phase 2+: Can integrate translation APIs
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Supported locales
SUPPORTED_LOCALES = ['en', 'pt-br']

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Greetings
        'good_morning': 'Good morning',
        'good_afternoon': 'Good afternoon',
        'good_evening': 'Good evening',

        # Common phrases
        'dear': 'Dear',
        'friend': 'friend',
        'with_care': 'With care',
        'you_decide': 'You decide what\'s best for your situation.',

        # Market terms
        'market_snapshot': 'Market Snapshot',
        'fear_greed_index': 'Fear & Greed Index',
        'whale_watch': 'Whale Watch',
        'strategy_overview': 'Strategy Overview',

        # Labels
        'conservative': 'Conservative',
        'balanced': 'Balanced',
        'growth': 'Growth',
        'status': 'Status',
        'performance': 'Performance',

        # Status
        'normal': 'Normal',
        'elevated': 'Elevated',
        'warning': 'Warning',

        # Sentiments
        'extreme_fear': 'Extreme Fear',
        'fear': 'Fear',
        'neutral': 'Neutral',
        'greed': 'Greed',
        'extreme_greed': 'Extreme Greed',

        # Disclaimers
        'disclaimer_header': 'Important Disclosures',
        'not_financial_advice': 'This is educational content only, not financial advice.',
        'past_performance': 'Past performance does not guarantee future results.',
        'consult_adviser': 'Consider consulting a licensed financial adviser for personalized guidance.',

        # Ana-specific
        'dont_worry': "Don't worry, dear",
        'take_a_breath': "Let's take a breath together",
        'youre_doing_great': "You're doing great",
        'slow_and_steady': "Slow and steady",
    },

    'pt-br': {
        # Greetings
        'good_morning': 'Bom dia',
        'good_afternoon': 'Boa tarde',
        'good_evening': 'Boa noite',

        # Common phrases
        'dear': 'Querido(a)',
        'friend': 'amigo(a)',
        'with_care': 'Com carinho',
        'you_decide': 'Você decide o que é melhor para sua situacao.',

        # Market terms
        'market_snapshot': 'Panorama do Mercado',
        'fear_greed_index': 'Indice de Medo e Ganancia',
        'whale_watch': 'Monitoramento de Baleias',
        'strategy_overview': 'Visao das Estrategias',

        # Labels
        'conservative': 'Conservador',
        'balanced': 'Equilibrado',
        'growth': 'Crescimento',
        'status': 'Status',
        'performance': 'Desempenho',

        # Status
        'normal': 'Normal',
        'elevated': 'Elevado',
        'warning': 'Atencao',

        # Sentiments
        'extreme_fear': 'Medo Extremo',
        'fear': 'Medo',
        'neutral': 'Neutro',
        'greed': 'Ganancia',
        'extreme_greed': 'Ganancia Extrema',

        # Disclaimers
        'disclaimer_header': 'Avisos Importantes',
        'not_financial_advice': 'Este e conteudo educacional apenas, nao aconselhamento financeiro.',
        'past_performance': 'Desempenho passado nao garante resultados futuros.',
        'consult_adviser': 'Considere consultar um assessor financeiro licenciado para orientacao personalizada.',

        # Ana-specific
        'dont_worry': 'Nao se preocupe, querido(a)',
        'take_a_breath': 'Vamos respirar juntos',
        'youre_doing_great': 'Voce esta indo muito bem',
        'slow_and_steady': 'Devagar e sempre',

        # MiCA warning (required for EU/Brazil)
        'mica_warning': 'AVISO: Criptoativos NAO sao protegidos por esquemas de garantia de depositos da UE. Stablecoins podem perder paridade. Voce pode perder todo o capital.',
    }
}

# Regional disclaimers
REGIONAL_DISCLAIMERS = {
    'en': """**Important Disclosures**

This content is for educational purposes only and does not constitute investment advice, financial advice, trading advice, or any other sort of advice. diBoaS does not recommend that any cryptocurrency should be bought, sold, or held by you.

Past performance is not indicative of future results. The value of investments can go down as well as up, and you may lose some or all of your investment.

Consider consulting a licensed financial adviser for guidance specific to your situation.

*You decide what's best for your situation.*""",

    'pt-br': """**Avisos Importantes de Conformidade**

**AVISO 1 - PROTEÇÃO AO INVESTIDOR:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos ou fundos de compensação ao investidor.

**AVISO 2 - RISCO DE PERDA:** O valor dos seus investimentos pode diminuir ou aumentar. Você pode perder parte ou todo o capital investido.

**AVISO 3 - ORIENTAÇÃO PROFISSIONAL:** Considere consultar um assessor financeiro ou profissional habilitado pela CVM para orientação específica à sua situação.

Este conteúdo é apenas para fins educacionais e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.

Desempenho passado não é indicativo de resultados futuros.

**Direito de reclamação:** [contato@diboas.com]

*Você decide o que é melhor para sua situação.*"""
}


# Hypothetical performance disclaimers (SEC Marketing Rule compliance)
HYPOTHETICAL_DISCLAIMERS = {
    'en': (
        "⚠️ HYPOTHETICAL PERFORMANCE: This analysis is based on historical data "
        "and simulated results. Past performance does not guarantee future returns. "
        "Actual results may differ materially due to market conditions, execution, "
        "and other factors. These results reflect hindsight bias and should not be "
        "relied upon as indicative of future performance."
    ),
    'pt-br': (
        "⚠️ DESEMPENHO HIPOTÉTICO: Esta análise é baseada em dados históricos "
        "e resultados simulados. Desempenho passado não garante retornos futuros. "
        "Resultados reais podem diferir significativamente devido às condições de "
        "mercado, execução e outros fatores. Estes resultados refletem viés de "
        "retrospectiva e não devem ser considerados indicativos de desempenho futuro."
    )
}


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
