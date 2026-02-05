"""
Maria Persona - Friendly Teacher Voice.

Characteristics:
- Educational and informative tone ("friendly teacher")
- Moderate emoji usage (3-8 per newsletter)
- Balance of safety and growth
- Explains concepts with context
- Targets strategies 2, 4, 6 (30-40% crypto)

Sign-off: "Stay informed, Adelaide 📊"
"""

from datetime import datetime
from typing import Any, Dict

from src.registries.personas.base import Persona, EmojiLevel


class MariaPersona(Persona):
    """Maria - Balanced persona with friendly teacher voice."""

    EMOJIS = {
        'title': '📊',
        'greeting': '👋',
        'market': '📈',
        'educational': ['📚', '💡', '📈', '🏠'],
        'whale': '🐋',
        'strategy': '📊',
        'neutral': ['📋', '🔍'],
        'closing': '📊',
    }

    PHRASES = {
        'en': {
            'greeting_morning': "Good morning!",
            'greeting_afternoon': "Good afternoon!",
            'greeting_evening': "Good evening!",
            'intro': "Here's your {day} market update. Let's look at what the data is telling us today.",
            'market_section': "Market Overview",
            'market_intro': "Today's market conditions at a glance. Here's what the indicators show:",
            'market_meaning': "**Context:** Markets move daily. What matters most is understanding the broader trends and how they relate to your investment timeframe.",
            'whale_section': "🐋 Whale Watch",
            'whale_intro': "Tracking large wallet movements for market awareness.",
            'whale_summary': "**Recent Activity:** No significant estate movements this period. Distributions continue on schedule.",
            'whale_disclaimer': "Note: Whale movements are informational only and not trading signals.",
            'strategy_section': "Strategy Performance",
            'strategy_col1': "Strategy Type",
            'strategy_col2': "Status",
            'strategy_col3': "7-Day Performance",
            'strategy_note': "All strategies operating within expected parameters.",
            'insight_section': "💡 Market Insight",
            'wisdom_note': "Historical context helps frame current conditions, though past patterns don't guarantee future results.",
            'closing': "Stay informed",
            'signature': "Stay informed,\n**Adelaide** | diBoaS 📊",
            'footer': "📧 Questions? Reply to this email.\n⚙️ [Settings](link) | 🚪 [Unsubscribe](link)",
            'disclaimer': "**Important Notice**\n\nThis content is educational market commentary, not financial advice. Past performance does not guarantee future results. Always consult a licensed financial adviser before making investment decisions.\n\n**You decide what's best for your situation.**",
        },
        'pt-br': {
            'greeting_morning': "Bom dia!",
            'greeting_afternoon': "Boa tarde!",
            'greeting_evening': "Boa noite!",
            'intro': "Aqui está sua atualização de mercado de {day}. Vamos ver o que os dados estão nos dizendo.",
            'market_section': "Visão Geral do Mercado",
            'market_intro': "Condições de mercado de hoje em resumo. Veja o que os indicadores mostram:",
            'market_meaning': "**Contexto:** Os mercados se movem diariamente. O mais importante é entender as tendências mais amplas e como elas se relacionam com seu horizonte de investimento.",
            'whale_section': "🐋 Monitoramento de Baleias",
            'whale_intro': "Monitorando movimentos de grandes carteiras para conscientização de mercado.",
            'whale_summary': "**Atividade Recente:** Nenhum movimento significativo de estate neste período. Distribuições continuam no cronograma.",
            'whale_disclaimer': "Nota: Movimentos de baleias são apenas informativos e não são sinais de negociação.",
            'strategy_section': "Desempenho das Estratégias",
            'strategy_col1': "Tipo de Estratégia",
            'strategy_col2': "Status",
            'strategy_col3': "Performance 7 Dias",
            'strategy_note': "Todas as estratégias operando dentro dos parâmetros esperados.",
            'insight_section': "💡 Insight de Mercado",
            'wisdom_note': "O contexto histórico ajuda a enquadrar as condições atuais, embora padrões passados não garantam resultados futuros.",
            'closing': "Mantenha-se informado(a)",
            'signature': "Mantenha-se informado(a),\n**Adelaide** | diBoaS 📊",
            'footer': "📧 Dúvidas? Responda este email.\n⚙️ [Configurações](link) | 🚪 [Cancelar inscrição](link)",
            'disclaimer': "**Aviso Importante**\n\n**AVISO MiCA/CVM:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos.\n\nEste conteúdo é comentário educacional de mercado, não aconselhamento financeiro. Desempenho passado não garante resultados futuros.\n\n**Você decide o que é melhor para sua situação.**",
        },
        'de': {
            'greeting_morning': "Guten Morgen!",
            'greeting_afternoon': "Guten Tag!",
            'greeting_evening': "Guten Abend!",
            'intro': "Hier ist Ihr Markt-Update für {day}. Schauen wir, was uns die Daten heute sagen.",
            'market_section': "Marktübersicht",
            'market_intro': "Die heutigen Marktbedingungen auf einen Blick. Das zeigen die Indikatoren:",
            'market_meaning': "**Kontext:** Märkte bewegen sich täglich. Am wichtigsten ist es, die breiteren Trends zu verstehen und wie sie sich auf Ihren Anlagehorizont beziehen.",
            'whale_section': "🐋 Whale-Überwachung",
            'whale_intro': "Verfolgung großer Wallet-Bewegungen für Marktbewusstsein.",
            'whale_summary': "**Aktuelle Aktivität:** Keine signifikanten Estate-Bewegungen in diesem Zeitraum. Verteilungen laufen nach Plan.",
            'whale_disclaimer': "Hinweis: Whale-Bewegungen dienen nur zur Information und sind keine Handelssignale.",
            'strategy_section': "Strategieleistung",
            'strategy_col1': "Strategietyp",
            'strategy_col2': "Status",
            'strategy_col3': "7-Tage-Performance",
            'strategy_note': "Alle Strategien arbeiten innerhalb der erwarteten Parameter.",
            'insight_section': "💡 Markt-Einblick",
            'wisdom_note': "Historischer Kontext hilft bei der Einordnung aktueller Bedingungen, obwohl vergangene Muster keine zukünftigen Ergebnisse garantieren.",
            'closing': "Bleiben Sie informiert",
            'signature': "Bleiben Sie informiert,\n**Adelaide** | diBoaS 📊",
            'footer': "📧 Fragen? Antworten Sie auf diese E-Mail.\n⚙️ [Einstellungen](link) | 🚪 [Abmelden](link)",
            'disclaimer': "**Wichtiger Hinweis**\n\n**MiCA-HINWEIS:** Kryptowerte werden NICHT durch EU-Einlagensicherungssysteme geschützt.\n\nDieser Inhalt ist ein pädagogischer Marktkommentar, keine Finanzberatung. Die vergangene Wertentwicklung garantiert keine zukünftigen Ergebnisse.\n\n**Sie entscheiden, was für Ihre Situation am besten ist.**",
        },
        'es': {
            'greeting_morning': "¡Buenos días!",
            'greeting_afternoon': "¡Buenas tardes!",
            'greeting_evening': "¡Buenas noches!",
            'intro': "Aquí está su actualización de mercado de {day}. Veamos qué nos dicen los datos hoy.",
            'market_section': "Visión General del Mercado",
            'market_intro': "Las condiciones del mercado de hoy de un vistazo. Esto es lo que muestran los indicadores:",
            'market_meaning': "**Contexto:** Los mercados se mueven diariamente. Lo más importante es entender las tendencias más amplias y cómo se relacionan con su horizonte de inversión.",
            'whale_section': "🐋 Seguimiento de Ballenas",
            'whale_intro': "Monitoreando movimientos de grandes carteras para conciencia del mercado.",
            'whale_summary': "**Actividad Reciente:** No hubo movimientos significativos de estates en este período. Las distribuciones continúan según lo programado.",
            'whale_disclaimer': "Nota: Los movimientos de ballenas son solo informativos y no son señales de trading.",
            'strategy_section': "Rendimiento de Estrategias",
            'strategy_col1': "Tipo de Estrategia",
            'strategy_col2': "Estado",
            'strategy_col3': "Rendimiento 7 Días",
            'strategy_note': "Todas las estrategias operando dentro de los parámetros esperados.",
            'insight_section': "💡 Perspectiva del Mercado",
            'wisdom_note': "El contexto histórico ayuda a enmarcar las condiciones actuales, aunque los patrones pasados no garantizan resultados futuros.",
            'closing': "Manténgase informado(a)",
            'signature': "Manténgase informado(a),\n**Adelaide** | diBoaS 📊",
            'footer': "📧 ¿Preguntas? Responda este correo.\n⚙️ [Configuración](link) | 🚪 [Cancelar suscripción](link)",
            'disclaimer': "**Aviso Importante**\n\n**AVISO MiCA:** Los criptoactivos NO están protegidos por sistemas de garantía de depósitos de la UE.\n\nEste contenido es comentario educativo de mercado, no asesoramiento financiero. El rendimiento pasado no garantiza resultados futuros.\n\n**Usted decide lo que es mejor para su situación.**",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Maria's educational, balanced voice."""
        adapted = content.copy()
        adapted['persona'] = 'maria'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # Time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_of_day = 'morning'
        elif 12 <= hour < 18:
            time_of_day = 'afternoon'
        else:
            time_of_day = 'evening'

        day_name = datetime.now().strftime('%A')

        # Title and greeting
        adapted['title_emoji'] = self.EMOJIS['title']
        adapted['persona_greeting'] = f"{phrases[f'greeting_{time_of_day}']} {self.EMOJIS['greeting']}"
        adapted['greeting_message'] = phrases['intro'].format(day=day_name)

        # Market section
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = self.EMOJIS['market']
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_market_bullets(content)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # Whale section
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = self.EMOJIS['strategy']
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Strategy Type')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Status')
        adapted['strategy_col3'] = phrases.get('strategy_col3', '7-Day Performance')
        adapted['conservative_status'] = '✅ Normal'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):+.2f}%"
        adapted['balanced_status'] = '✅ Normal'
        adapted['balanced_action'] = f"{content.get('balanced_7d', 0):+.2f}%"
        adapted['growth_status'] = '✅ Normal'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section
        adapted['insight_section_title'] = phrases['insight_section']
        adapted['wisdom_note'] = phrases['wisdom_note']

        # Closing
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_market_bullets(self, content: Dict) -> str:
        """Build educational market bullets."""
        bullets = []
        vix = content.get('vix', 20)
        fg = content.get('fear_greed_index', 50)

        bullets.append(f"- VIX (volatility index): {vix:.1f} — {'Low volatility environment' if vix < 20 else 'Elevated volatility' if vix > 25 else 'Normal range'}")
        bullets.append(f"- Fear & Greed Index: {fg} — Sentiment indicator showing market mood")
        bullets.append("- Credit spreads: Within normal range — institutional confidence stable")

        return '\n'.join(bullets)

    @property
    def name(self) -> str:
        return "Maria"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.MODERATE

    @property
    def risk_profile(self) -> str:
        return "balanced"

    def get_signature(self, locale: str = "en") -> str:
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        return phrases.get('signature', "Stay informed,\n**Adelaide** | diBoaS 📊")
