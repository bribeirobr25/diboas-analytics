"""
Felipe Persona - Technical Analyst Voice.

Characteristics:
- Data-forward, analytical tone ("technical analyst")
- Zero emojis (only warning indicators)
- Focus on returns and opportunities
- Technical language, precise numbers
- Indicator matrices and regime analysis
- Targets strategies 8, 10 (70-85% crypto)

Sign-off: "— Adelaide"
"""

import re
from typing import Any, Dict

from src.registries.personas.base import Persona, EmojiLevel


class FelipePersona(Persona):
    """Felipe - Aggressive/Technical persona with analytical voice."""

    PHRASES = {
        'en': {
            'greeting': "Morning. Here's today's data.",
            'intro': "Daily briefing. Current regime analysis and key metrics follow.",
            'market_section': "Market Regime Analysis",
            'market_intro': "Current market conditions and indicator signals:",
            'market_meaning': "**Regime Assessment:** Review indicator confluence for positioning decisions.",
            'whale_section': "Estate Wallet Status",
            'whale_intro': "Tracking bankruptcy estate distributions and large holder movements.",
            'whale_summary': "**Activity:** No large movements detected. Distributions on schedule.",
            'whale_disclaimer': "Estate tracking is informational. Not a trading signal.",
            'strategy_section': "Strategy Matrix",
            'strategy_col1': "Strategy",
            'strategy_col2': "Status",
            'strategy_col3': "7d Return",
            'strategy_note': "All strategies within risk parameters. No triggers activated.",
            'insight_section': "Technical Analysis",
            'wisdom_note': "Historical correlations noted. Past patterns are not predictive.",
            'closing': "Execute accordingly",
            'signature': "— Adelaide | diBoaS",
            'footer': "Reply with questions. [Settings](link) | [Unsubscribe](link)",
            'disclaimer': "**Disclaimer**\n\nPast performance ≠ future results. Capital at risk. Not financial advice. DYOR.\n\n**Your call.**",
        },
        'pt-br': {
            'greeting': "Bom dia. Dados de hoje.",
            'intro': "Briefing diário. Análise de regime e métricas principais.",
            'market_section': "Análise de Regime de Mercado",
            'market_intro': "Condições atuais de mercado e sinais de indicadores:",
            'market_meaning': "**Avaliação de Regime:** Revise a confluência de indicadores para decisões de posicionamento.",
            'whale_section': "Status de Carteiras Estate",
            'whale_intro': "Monitorando distribuições de estates falidos e movimentos de grandes detentores.",
            'whale_summary': "**Atividade:** Nenhum movimento grande detectado. Distribuições no cronograma.",
            'whale_disclaimer': "Monitoramento de estates é informativo. Não é sinal de negociação.",
            'strategy_section': "Matriz de Estratégias",
            'strategy_col1': "Estratégia",
            'strategy_col2': "Status",
            'strategy_col3': "Retorno 7d",
            'strategy_note': "Todas as estratégias dentro dos parâmetros de risco. Nenhum trigger ativado.",
            'insight_section': "Análise Técnica",
            'wisdom_note': "Correlações históricas notadas. Padrões passados não são preditivos.",
            'closing': "Execute conforme necessário",
            'signature': "— Adelaide | diBoaS",
            'footer': "Responda com dúvidas. [Configurações](link) | [Cancelar inscrição](link)",
            'disclaimer': "**Aviso**\n\n**MiCA/CVM:** Criptoativos sem garantia de depósito.\n\nDesempenho passado ≠ resultados futuros. Capital em risco. Não é aconselhamento financeiro.\n\n**Sua decisão.**",
        },
        'de': {
            'greeting': "Morgen. Hier sind die heutigen Daten.",
            'intro': "Tägliches Briefing. Regime-Analyse und Schlüsselmetriken folgen.",
            'market_section': "Marktregime-Analyse",
            'market_intro': "Aktuelle Marktbedingungen und Indikatorsignale:",
            'market_meaning': "**Regime-Bewertung:** Überprüfen Sie die Indikatorkonvergenz für Positionierungsentscheidungen.",
            'whale_section': "Estate-Wallet-Status",
            'whale_intro': "Verfolgung von Insolvenz-Estate-Verteilungen und großen Halter-Bewegungen.",
            'whale_summary': "**Aktivität:** Keine großen Bewegungen erkannt. Verteilungen im Zeitplan.",
            'whale_disclaimer': "Estate-Tracking dient zur Information. Kein Handelssignal.",
            'strategy_section': "Strategie-Matrix",
            'strategy_col1': "Strategie",
            'strategy_col2': "Status",
            'strategy_col3': "7d-Rendite",
            'strategy_note': "Alle Strategien innerhalb der Risikoparameter. Keine Trigger aktiviert.",
            'insight_section': "Technische Analyse",
            'wisdom_note': "Historische Korrelationen notiert. Vergangene Muster sind nicht prädiktiv.",
            'closing': "Entsprechend handeln",
            'signature': "— Adelaide | diBoaS",
            'footer': "Antworten Sie bei Fragen. [Einstellungen](link) | [Abmelden](link)",
            'disclaimer': "**Haftungsausschluss**\n\n**MiCA:** Kryptowerte ohne Einlagensicherung.\n\nVergangene Performance ≠ zukünftige Ergebnisse. Kapital in Gefahr. Keine Finanzberatung.\n\n**Ihre Entscheidung.**",
        },
        'es': {
            'greeting': "Buenos días. Datos de hoy.",
            'intro': "Briefing diario. Análisis de régimen y métricas clave a continuación.",
            'market_section': "Análisis de Régimen de Mercado",
            'market_intro': "Condiciones actuales del mercado y señales de indicadores:",
            'market_meaning': "**Evaluación de Régimen:** Revise la confluencia de indicadores para decisiones de posicionamiento.",
            'whale_section': "Estado de Carteras Estate",
            'whale_intro': "Seguimiento de distribuciones de estates en bancarrota y movimientos de grandes tenedores.",
            'whale_summary': "**Actividad:** No se detectaron movimientos grandes. Distribuciones según cronograma.",
            'whale_disclaimer': "El seguimiento de estates es informativo. No es señal de trading.",
            'strategy_section': "Matriz de Estrategias",
            'strategy_col1': "Estrategia",
            'strategy_col2': "Estado",
            'strategy_col3': "Retorno 7d",
            'strategy_note': "Todas las estrategias dentro de los parámetros de riesgo. Ningún trigger activado.",
            'insight_section': "Análisis Técnico",
            'wisdom_note': "Correlaciones históricas notadas. Los patrones pasados no son predictivos.",
            'closing': "Ejecute según corresponda",
            'signature': "— Adelaide | diBoaS",
            'footer': "Responda con preguntas. [Configuración](link) | [Cancelar suscripción](link)",
            'disclaimer': "**Aviso**\n\n**MiCA:** Criptoactivos sin garantía de depósito.\n\nRendimiento pasado ≠ resultados futuros. Capital en riesgo. No es asesoramiento financiero.\n\n**Su decisión.**",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Felipe's technical, data-forward voice."""
        adapted = content.copy()
        adapted['persona'] = 'felipe'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # No emojis
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = phrases['intro']

        # Market section - technical
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_indicator_matrix(content)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # Whale section - technical
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section - metrics focused
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Strategy')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Status')
        adapted['strategy_col3'] = phrases.get('strategy_col3', '7d Return')
        adapted['conservative_status'] = 'Active'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):+.2f}%"
        adapted['balanced_status'] = 'Active'
        adapted['balanced_action'] = f"{content.get('balanced_7d', 0):+.2f}%"
        adapted['growth_status'] = 'Active'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section
        adapted['insight_section_title'] = phrases['insight_section']

        # Strip emojis from insight content
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))

        adapted['wisdom_note'] = phrases['wisdom_note']

        # Closing - direct
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_indicator_matrix(self, content: Dict) -> str:
        """Build technical indicator matrix."""
        btc = content.get('btc_24h_change', 0)
        fg = content.get('fear_greed_index', 50)
        vix = content.get('vix', 20)

        btc_signal = 'Bullish' if btc > 2 else 'Bearish' if btc < -2 else 'Neutral'
        fg_signal = 'Oversold' if fg < 25 else 'Overbought' if fg > 75 else 'Neutral'
        vix_signal = 'Risk-On' if vix < 20 else 'Risk-Off' if vix > 30 else 'Neutral'

        return f"""| Indicator | Value | Signal |
|-----------|-------|--------|
| BTC 24h | {btc:+.2f}% | {btc_signal} |
| Fear/Greed | {fg} | {fg_signal} |
| VIX | {vix:.1f} | {vix_signal} |"""

    def _strip_emojis(self, text: str) -> str:
        """Remove all emojis from text."""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', text).strip()

    @property
    def name(self) -> str:
        return "Felipe"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.NONE

    @property
    def risk_profile(self) -> str:
        return "aggressive"

    def get_signature(self, locale: str = "en") -> str:
        return "— Adelaide | diBoaS"
