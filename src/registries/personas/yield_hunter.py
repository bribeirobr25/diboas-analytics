"""
Yield Hunter Persona - DeFi Native Voice.

Characteristics:
- Uses DeFi terminology WITHOUT explanation (APY, TVL, IL, LTV)
- Minimal emoji usage (1-3 per newsletter maximum)
- Assumes reader understands DeFi mechanics
- Focus on yield opportunities and protocol risk
- Technical but not overly formal
- Targets yield-focused strategies (6, 7 optionally)

Sign-off: "— Adelaide | diBoaS"
"""

from typing import Any, Dict

from src.registries.personas.base import Persona, EmojiLevel


class YieldHunterPersona(Persona):
    """Yield Hunter - Aggressive DeFi-native persona."""

    # Minimal emoji palette - only key indicators
    EMOJIS = {
        'yield_up': '📈',
        'yield_down': '📉',
        'warning': '⚠️',
    }

    PHRASES = {
        'en': {
            'greeting': "Yield update.",
            'intro': "Quick rundown on yield opportunities and protocol status. Here's what's moving.",
            'market_section': "Yield Environment",
            'market_intro': "Current conditions across protocols:",
            'market_meaning': "**Assessment:** Factor these conditions into your yield strategy positioning.",
            'whale_section': "Protocol TVL Movements",
            'whale_intro': "Tracking significant TVL shifts and whale migrations.",
            'whale_summary': "**TVL Status:** Major protocols stable. No significant outflows detected.",
            'whale_disclaimer': "TVL movements are informational. DYOR before repositioning.",
            'strategy_section': "Yield Matrix",
            'strategy_col1': "Protocol",
            'strategy_col2': "Current APY",
            'strategy_col3': "7d Δ",
            'strategy_note': "Yields fluctuate. IL risk exists on volatile pairs. Always check LTV ratios.",
            'insight_section': "Alpha Signal",
            'wisdom_note': "Past yields don't guarantee future returns. Protocol risk is real.",
            'closing': "Hunt wisely",
            'signature': "— Adelaide | diBoaS",
            'footer': "Reply with questions. [Settings](link) | [Unsubscribe](link)",
            'disclaimer': "**Risk Notice**\n\nDeFi protocols carry smart contract risk. Yields can drop to zero. IL can exceed gains. Not financial advice.\n\n**You manage your own risk.**",
            'vix_low': "VIX at {vix:.0f} — low vol environment favors yield farming",
            'vix_high': "VIX at {vix:.0f} — elevated. Consider de-risking positions",
            'apy_note': "APYs shown are variable and can change at any time",
            'tvl_healthy': "Protocol TVL healthy — liquidity depth adequate",
            'tvl_warning': "Monitor TVL — outflows detected this period",
            'il_warning': "IL risk elevated on volatile pairs",
            'credit_healthy': "Credit spreads tight — TradFi risk-on",
            'credit_warning': "Credit spreads widening — monitor DeFi contagion risk",
        },
        'pt-br': {
            'greeting': "Atualização de yields.",
            'intro': "Resumo rápido de oportunidades de yield e status dos protocolos.",
            'market_section': "Ambiente de Yields",
            'market_intro': "Condições atuais nos protocolos:",
            'market_meaning': "**Avaliação:** Considere essas condições no posicionamento da sua estratégia de yield.",
            'whale_section': "Movimentos de TVL",
            'whale_intro': "Monitorando mudanças significativas de TVL e migrações de baleias.",
            'whale_summary': "**Status TVL:** Protocolos principais estáveis. Sem saídas significativas.",
            'whale_disclaimer': "Movimentos de TVL são informativos. DYOR antes de reposicionar.",
            'strategy_section': "Matriz de Yields",
            'strategy_col1': "Protocolo",
            'strategy_col2': "APY Atual",
            'strategy_col3': "Δ 7d",
            'strategy_note': "Yields flutuam. Risco de IL existe em pares voláteis. Sempre verifique ratios de LTV.",
            'insight_section': "Sinal Alpha",
            'wisdom_note': "Yields passados não garantem retornos futuros. Risco de protocolo é real.",
            'closing': "Cace com sabedoria",
            'signature': "— Adelaide | diBoaS",
            'footer': "Responda com dúvidas. [Configurações](link) | [Cancelar inscrição](link)",
            'disclaimer': "**Aviso de Risco**\n\n**MiCA/CVM:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos. Stablecoins podem perder paridade.\n\nProtocolos DeFi carregam risco de smart contract. Yields podem cair a zero. IL pode exceder ganhos. Não é aconselhamento financeiro.\n\n**Você gerencia seu próprio risco.**",
            'vix_low': "VIX em {vix:.0f} — ambiente de baixa vol favorece yield farming",
            'vix_high': "VIX em {vix:.0f} — elevado. Considere reduzir exposição",
            'apy_note': "APYs mostrados são variáveis e podem mudar a qualquer momento",
            'tvl_healthy': "TVL do protocolo saudável — profundidade de liquidez adequada",
            'tvl_warning': "Monitore TVL — saídas detectadas neste período",
            'il_warning': "Risco de IL elevado em pares voláteis",
            'credit_healthy': "Spreads de crédito apertados — TradFi risk-on",
            'credit_warning': "Spreads de crédito alargando — monitore risco de contágio DeFi",
        },
        'de': {
            'greeting': "Yield-Update.",
            'intro': "Kurzer Überblick über Yield-Möglichkeiten und Protokollstatus. Hier ist, was sich bewegt.",
            'market_section': "Yield-Umgebung",
            'market_intro': "Aktuelle Bedingungen bei Protokollen:",
            'market_meaning': "**Bewertung:** Berücksichtigen Sie diese Bedingungen bei der Positionierung Ihrer Yield-Strategie.",
            'whale_section': "TVL-Bewegungen",
            'whale_intro': "Verfolgung signifikanter TVL-Verschiebungen und Whale-Migrationen.",
            'whale_summary': "**TVL-Status:** Große Protokolle stabil. Keine signifikanten Abflüsse erkannt.",
            'whale_disclaimer': "TVL-Bewegungen dienen zur Information. DYOR vor Neupositionierung.",
            'strategy_section': "Yield-Matrix",
            'strategy_col1': "Protokoll",
            'strategy_col2': "Aktueller APY",
            'strategy_col3': "7d Δ",
            'strategy_note': "Yields schwanken. IL-Risiko besteht bei volatilen Paaren. Prüfen Sie immer die LTV-Verhältnisse.",
            'insight_section': "Alpha-Signal",
            'wisdom_note': "Vergangene Yields garantieren keine zukünftigen Renditen. Protokollrisiko ist real.",
            'closing': "Jagen Sie klug",
            'signature': "— Adelaide | diBoaS",
            'footer': "Antworten Sie bei Fragen. [Einstellungen](link) | [Abmelden](link)",
            'disclaimer': "**Risikohinweis**\n\n**MiCA:** Kryptowerte werden NICHT durch EU-Einlagensicherungssysteme geschützt. Stablecoins können ihre Bindung verlieren.\n\nDeFi-Protokolle tragen Smart-Contract-Risiko. Yields können auf null fallen. IL kann Gewinne übersteigen. Keine Finanzberatung.\n\n**Sie verwalten Ihr eigenes Risiko.**",
            'vix_low': "VIX bei {vix:.0f} — niedriges Volatilitätsumfeld begünstigt Yield Farming",
            'vix_high': "VIX bei {vix:.0f} — erhöht. Erwägen Sie Risikoreduzierung",
            'apy_note': "Angezeigte APYs sind variabel und können sich jederzeit ändern",
            'tvl_healthy': "Protokoll-TVL gesund — Liquiditätstiefe ausreichend",
            'tvl_warning': "TVL überwachen — Abflüsse in diesem Zeitraum erkannt",
            'il_warning': "IL-Risiko bei volatilen Paaren erhöht",
            'credit_healthy': "Credit Spreads eng — TradFi Risk-On",
            'credit_warning': "Credit Spreads weiten sich — DeFi-Ansteckungsrisiko beobachten",
        },
        'es': {
            'greeting': "Actualización de yields.",
            'intro': "Resumen rápido de oportunidades de yield y estado de protocolos. Esto es lo que se mueve.",
            'market_section': "Entorno de Yields",
            'market_intro': "Condiciones actuales en los protocolos:",
            'market_meaning': "**Evaluación:** Considere estas condiciones en el posicionamiento de su estrategia de yield.",
            'whale_section': "Movimientos de TVL",
            'whale_intro': "Siguiendo cambios significativos de TVL y migraciones de ballenas.",
            'whale_summary': "**Estado TVL:** Protocolos principales estables. Sin salidas significativas detectadas.",
            'whale_disclaimer': "Los movimientos de TVL son informativos. DYOR antes de reposicionar.",
            'strategy_section': "Matriz de Yields",
            'strategy_col1': "Protocolo",
            'strategy_col2': "APY Actual",
            'strategy_col3': "Δ 7d",
            'strategy_note': "Los yields fluctúan. Existe riesgo de IL en pares volátiles. Siempre verifique los ratios de LTV.",
            'insight_section': "Señal Alpha",
            'wisdom_note': "Los yields pasados no garantizan rendimientos futuros. El riesgo de protocolo es real.",
            'closing': "Cace con sabiduría",
            'signature': "— Adelaide | diBoaS",
            'footer': "Responda con preguntas. [Configuración](link) | [Cancelar suscripción](link)",
            'disclaimer': "**Aviso de Riesgo**\n\n**MiCA:** Los criptoactivos NO están protegidos por sistemas de garantía de depósitos de la UE. Las stablecoins pueden perder paridad.\n\nLos protocolos DeFi conllevan riesgo de smart contract. Los yields pueden caer a cero. IL puede exceder ganancias. No es asesoramiento financiero.\n\n**Usted gestiona su propio riesgo.**",
            'vix_low': "VIX en {vix:.0f} — ambiente de baja volatilidad favorece yield farming",
            'vix_high': "VIX en {vix:.0f} — elevado. Considere reducir exposición",
            'apy_note': "Los APYs mostrados son variables y pueden cambiar en cualquier momento",
            'tvl_healthy': "TVL del protocolo saludable — profundidad de liquidez adecuada",
            'tvl_warning': "Monitoree TVL — salidas detectadas en este período",
            'il_warning': "Riesgo de IL elevado en pares volátiles",
            'credit_healthy': "Credit spreads ajustados — TradFi risk-on",
            'credit_warning': "Credit spreads ampliándose — monitoree riesgo de contagio DeFi",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """
        Adapt content to Yield Hunter's DeFi-native voice.

        Transformations:
        - Keep DeFi terminology (no simplification)
        - Minimal emojis (1-3 max)
        - Focus on yield metrics and protocol status
        - Direct, no-fluff communication
        """
        adapted = content.copy()
        adapted['persona'] = 'yield_hunter'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # No emoji in title
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = phrases['intro']

        # Market section - yield focused
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_yield_bullets(content, phrases)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # TVL/Whale section
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section - yield matrix
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Protocol')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Current APY')
        adapted['strategy_col3'] = phrases.get('strategy_col3', '7d Δ')

        # Use actual APY data if available
        adapted['conservative_status'] = f"{content.get('stable_apy', 5.0):.1f}%"
        adapted['conservative_action'] = f"{content.get('stable_7d_change', 0):+.2f}%"
        adapted['balanced_status'] = f"{content.get('balanced_apy', 8.0):.1f}%"
        adapted['balanced_action'] = f"{content.get('balanced_7d_change', 0):+.2f}%"
        adapted['growth_status'] = f"{content.get('growth_apy', 15.0):.1f}%"
        adapted['growth_action'] = f"{content.get('growth_7d_change', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section
        adapted['insight_section_title'] = phrases['insight_section']
        adapted['wisdom_note'] = phrases['wisdom_note']

        # Closing - direct
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_yield_bullets(self, content: Dict, phrases: Dict) -> str:
        """Build yield-focused market bullets."""
        bullets = []
        vix = content.get('vix', 20)

        # VIX assessment
        if vix < 20:
            bullets.append(f"- {phrases.get('vix_low', '').format(vix=vix)}")
        else:
            bullets.append(f"- {phrases.get('vix_high', '').format(vix=vix)}")

        # Credit spreads - DeFi correlation
        credit_spread = content.get('credit_spread', 1.0)
        if credit_spread < 1.5:
            bullets.append(f"- {phrases.get('credit_healthy', '')}")
        else:
            bullets.append(f"- {phrases.get('credit_warning', '')}")

        # TVL status
        tvl_change = content.get('tvl_24h_change', 0)
        if tvl_change >= -2:
            bullets.append(f"- {phrases.get('tvl_healthy', '')}")
        else:
            bullets.append(f"- {phrases.get('tvl_warning', '')}")

        # APY variability note
        bullets.append(f"- {phrases.get('apy_note', '')}")

        return '\n'.join(bullets)

    @property
    def name(self) -> str:
        return "Yield Hunter"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.MINIMAL

    @property
    def risk_profile(self) -> str:
        return "aggressive"

    def get_signature(self, locale: str = "en") -> str:
        return "— Adelaide | diBoaS"
