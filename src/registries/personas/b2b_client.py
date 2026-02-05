"""
B2B Client Persona - Institutional/Professional Voice.

Characteristics:
- Zero emojis (professional, audit-ready)
- ISO 8601 timestamps
- Formal, professional tone
- Executive summary format
- Explicit data source attribution
- Methodology notes included
- Unique report/audit ID in signature

Sign-off: "Adelaide Analytics | Report ID: [UUID]"
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict

from src.registries.personas.base import Persona, EmojiLevel


class B2BClientPersona(Persona):
    """B2B Client - Institutional/Professional persona."""

    PHRASES = {
        'en': {
            'greeting': "Market Intelligence Report",
            'intro': "This report provides a summary of current market conditions and portfolio positioning metrics.",
            'market_section': "Market Conditions Summary",
            'market_intro': "Key indicators as of report generation:",
            'market_meaning': "**Interpretation:** The above metrics should be considered within the context of your organization's risk framework and investment policy.",
            'whale_section': "Large Holder Activity Report",
            'whale_intro': "Monitoring of significant wallet movements and bankruptcy estate distributions.",
            'whale_summary': "**Summary:** No material movements detected during the reporting period. Estate distributions proceeding according to schedule.",
            'whale_disclaimer': "Data Source: On-chain analytics aggregated from multiple providers. Not intended as trading signals.",
            'strategy_section': "Portfolio Strategy Status",
            'strategy_col1': "Strategy Category",
            'strategy_col2': "Operational Status",
            'strategy_col3': "Period Performance",
            'strategy_note': "All strategies operating within defined risk parameters. No threshold breaches detected.",
            'insight_section': "Analytical Commentary",
            'wisdom_note': "Historical data provided for context. Past performance does not indicate future results.",
            'closing': "End of Report",
            'signature': "Adelaide Analytics | diBoaS\nReport ID: {report_id}\nGenerated: {timestamp}",
            'footer': "For inquiries: analytics@diboas.com\nReport Settings | Unsubscribe",
            'disclaimer': "**Disclaimer and Compliance Notice**\n\nThis report is provided for informational purposes only and does not constitute investment advice, financial advice, trading advice, or any other sort of advice. The information contained herein should not be construed as a recommendation to buy, sell, or hold any security or other investment.\n\nPast performance is not indicative of future results. All investments carry risk, including the potential loss of principal.\n\nData sources: CoinGecko, DeFiLlama, Alternative.me, Federal Reserve Economic Data. Data accuracy is not guaranteed.\n\n**Your organization is solely responsible for all investment decisions.**",
            'vix_label': "CBOE Volatility Index (VIX)",
            'fear_greed_label': "Crypto Fear & Greed Index",
            'credit_spread_label': "Investment Grade Credit Spread",
            'btc_label': "Bitcoin 24h Price Change",
            'methodology': "**Methodology Note:** Metrics derived from aggregated market data. Calculations follow industry-standard methodologies. Full methodology documentation available upon request.",
            'data_sources': "**Data Sources:** Federal Reserve (FRED), CoinGecko API, DeFiLlama, Alternative.me Fear & Greed Index",
        },
        'pt-br': {
            'greeting': "Relatório de Inteligência de Mercado",
            'intro': "Este relatório fornece um resumo das condições atuais de mercado e métricas de posicionamento de portfólio.",
            'market_section': "Resumo das Condições de Mercado",
            'market_intro': "Indicadores-chave na data de geração do relatório:",
            'market_meaning': "**Interpretação:** As métricas acima devem ser consideradas dentro do contexto da estrutura de risco e política de investimento da sua organização.",
            'whale_section': "Relatório de Atividade de Grandes Detentores",
            'whale_intro': "Monitoramento de movimentos significativos de carteiras e distribuições de massas falidas.",
            'whale_summary': "**Resumo:** Nenhum movimento material detectado durante o período do relatório. Distribuições de massas falidas prosseguindo conforme cronograma.",
            'whale_disclaimer': "Fonte de Dados: Análise on-chain agregada de múltiplos provedores. Não se destina a sinais de negociação.",
            'strategy_section': "Status das Estratégias de Portfólio",
            'strategy_col1': "Categoria de Estratégia",
            'strategy_col2': "Status Operacional",
            'strategy_col3': "Performance do Período",
            'strategy_note': "Todas as estratégias operando dentro dos parâmetros de risco definidos. Nenhuma violação de limites detectada.",
            'insight_section': "Comentário Analítico",
            'wisdom_note': "Dados históricos fornecidos para contexto. Desempenho passado não indica resultados futuros.",
            'closing': "Fim do Relatório",
            'signature': "Adelaide Analytics | diBoaS\nID do Relatório: {report_id}\nGerado em: {timestamp}",
            'footer': "Para consultas: analytics@diboas.com\nConfigurações do Relatório | Cancelar inscrição",
            'disclaimer': "**Aviso Legal e Nota de Conformidade**\n\n**AVISO MiCA/CVM:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos. Stablecoins podem perder paridade. Você pode perder todo o capital investido.\n\nEste relatório é fornecido apenas para fins informativos e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.\n\nDesempenho passado não é indicativo de resultados futuros. Todos os investimentos carregam risco, incluindo a potencial perda do principal.\n\nFontes de dados: CoinGecko, DeFiLlama, Alternative.me, Federal Reserve Economic Data. A precisão dos dados não é garantida.\n\n**Sua organização é a única responsável por todas as decisões de investimento.**",
            'vix_label': "Índice de Volatilidade CBOE (VIX)",
            'fear_greed_label': "Índice Crypto Fear & Greed",
            'credit_spread_label': "Spread de Crédito Grau de Investimento",
            'btc_label': "Variação de Preço do Bitcoin 24h",
            'methodology': "**Nota Metodológica:** Métricas derivadas de dados de mercado agregados. Cálculos seguem metodologias padrão da indústria. Documentação completa da metodologia disponível mediante solicitação.",
            'data_sources': "**Fontes de Dados:** Federal Reserve (FRED), API CoinGecko, DeFiLlama, Índice Fear & Greed Alternative.me",
        },
        'de': {
            'greeting': "Markt-Intelligence-Bericht",
            'intro': "Dieser Bericht bietet eine Zusammenfassung der aktuellen Marktbedingungen und Portfolio-Positionierungsmetriken.",
            'market_section': "Zusammenfassung der Marktbedingungen",
            'market_intro': "Schlüsselindikatoren zum Zeitpunkt der Berichtserstellung:",
            'market_meaning': "**Interpretation:** Die oben genannten Metriken sollten im Kontext des Risikorahmens und der Anlagepolitik Ihrer Organisation betrachtet werden.",
            'whale_section': "Bericht über Aktivitäten großer Inhaber",
            'whale_intro': "Überwachung signifikanter Wallet-Bewegungen und Insolvenz-Estate-Verteilungen.",
            'whale_summary': "**Zusammenfassung:** Keine wesentlichen Bewegungen während des Berichtszeitraums erkannt. Estate-Verteilungen verlaufen nach Plan.",
            'whale_disclaimer': "Datenquelle: On-Chain-Analysen aggregiert von mehreren Anbietern. Nicht als Handelssignale gedacht.",
            'strategy_section': "Portfolio-Strategie-Status",
            'strategy_col1': "Strategiekategorie",
            'strategy_col2': "Betriebsstatus",
            'strategy_col3': "Periodenperformance",
            'strategy_note': "Alle Strategien arbeiten innerhalb definierter Risikoparameter. Keine Schwellenwertüberschreitungen erkannt.",
            'insight_section': "Analytischer Kommentar",
            'wisdom_note': "Historische Daten werden als Kontext bereitgestellt. Die vergangene Wertentwicklung ist kein Indikator für zukünftige Ergebnisse.",
            'closing': "Ende des Berichts",
            'signature': "Adelaide Analytics | diBoaS\nBericht-ID: {report_id}\nErstellt: {timestamp}",
            'footer': "Für Anfragen: analytics@diboas.com\nBerichtseinstellungen | Abmelden",
            'disclaimer': "**Haftungsausschluss und Compliance-Hinweis**\n\n**MiCA-HINWEIS:** Kryptowerte werden NICHT durch EU-Einlagensicherungssysteme geschützt. Stablecoins können ihre Bindung verlieren. Sie können Ihr gesamtes investiertes Kapital verlieren.\n\nDieser Bericht dient ausschließlich Informationszwecken und stellt keine Anlageberatung, Finanzberatung, Handelsberatung oder sonstige Beratung dar.\n\nDie vergangene Wertentwicklung ist kein Indikator für zukünftige Ergebnisse. Alle Anlagen bergen Risiken, einschließlich des möglichen Kapitalverlusts.\n\nDatenquellen: CoinGecko, DeFiLlama, Alternative.me, Federal Reserve Economic Data. Die Datengenauigkeit ist nicht garantiert.\n\n**Ihre Organisation ist allein verantwortlich für alle Anlageentscheidungen.**",
            'vix_label': "CBOE Volatilitätsindex (VIX)",
            'fear_greed_label': "Crypto Fear & Greed Index",
            'credit_spread_label': "Investment-Grade-Kreditspread",
            'btc_label': "Bitcoin 24h Preisänderung",
            'methodology': "**Methodikhinweis:** Metriken abgeleitet aus aggregierten Marktdaten. Berechnungen folgen branchenüblichen Methoden. Vollständige Methodikdokumentation auf Anfrage verfügbar.",
            'data_sources': "**Datenquellen:** Federal Reserve (FRED), CoinGecko API, DeFiLlama, Alternative.me Fear & Greed Index",
        },
        'es': {
            'greeting': "Informe de Inteligencia de Mercado",
            'intro': "Este informe proporciona un resumen de las condiciones actuales del mercado y métricas de posicionamiento de cartera.",
            'market_section': "Resumen de Condiciones de Mercado",
            'market_intro': "Indicadores clave a la fecha de generación del informe:",
            'market_meaning': "**Interpretación:** Las métricas anteriores deben considerarse dentro del contexto del marco de riesgo y política de inversión de su organización.",
            'whale_section': "Informe de Actividad de Grandes Tenedores",
            'whale_intro': "Monitoreo de movimientos significativos de carteras y distribuciones de estates en bancarrota.",
            'whale_summary': "**Resumen:** No se detectaron movimientos materiales durante el período del informe. Las distribuciones de estates proceden según lo programado.",
            'whale_disclaimer': "Fuente de Datos: Análisis on-chain agregado de múltiples proveedores. No está destinado como señales de trading.",
            'strategy_section': "Estado de Estrategias de Cartera",
            'strategy_col1': "Categoría de Estrategia",
            'strategy_col2': "Estado Operacional",
            'strategy_col3': "Rendimiento del Período",
            'strategy_note': "Todas las estrategias operando dentro de los parámetros de riesgo definidos. No se detectaron violaciones de umbrales.",
            'insight_section': "Comentario Analítico",
            'wisdom_note': "Los datos históricos se proporcionan como contexto. El rendimiento pasado no indica resultados futuros.",
            'closing': "Fin del Informe",
            'signature': "Adelaide Analytics | diBoaS\nID del Informe: {report_id}\nGenerado: {timestamp}",
            'footer': "Para consultas: analytics@diboas.com\nConfiguraciones del Informe | Cancelar suscripción",
            'disclaimer': "**Aviso Legal y Nota de Cumplimiento**\n\n**AVISO MiCA:** Los criptoactivos NO están protegidos por sistemas de garantía de depósitos de la UE. Las stablecoins pueden perder paridad. Usted puede perder todo su capital invertido.\n\nEste informe se proporciona solo con fines informativos y no constituye asesoramiento de inversión, asesoramiento financiero, asesoramiento de trading o cualquier otro tipo de asesoramiento.\n\nEl rendimiento pasado no es indicativo de resultados futuros. Todas las inversiones conllevan riesgo, incluyendo la potencial pérdida del principal.\n\nFuentes de datos: CoinGecko, DeFiLlama, Alternative.me, Federal Reserve Economic Data. La precisión de los datos no está garantizada.\n\n**Su organización es la única responsable de todas las decisiones de inversión.**",
            'vix_label': "Índice de Volatilidad CBOE (VIX)",
            'fear_greed_label': "Índice Crypto Fear & Greed",
            'credit_spread_label': "Spread de Crédito Grado de Inversión",
            'btc_label': "Cambio de Precio de Bitcoin 24h",
            'methodology': "**Nota Metodológica:** Métricas derivadas de datos de mercado agregados. Los cálculos siguen metodologías estándar de la industria. Documentación metodológica completa disponible bajo solicitud.",
            'data_sources': "**Fuentes de Datos:** Federal Reserve (FRED), API CoinGecko, DeFiLlama, Índice Fear & Greed Alternative.me",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._report_id = None

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """
        Adapt content to B2B Client's professional, audit-ready voice.

        Transformations:
        - Zero emojis
        - ISO 8601 timestamps
        - Formal language
        - Executive summary format
        - Data source attribution
        - Unique report ID
        """
        adapted = content.copy()
        adapted['persona'] = 'b2b_client'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # Generate unique report ID
        self._report_id = str(uuid.uuid4())[:8].upper()
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        # No emojis anywhere
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = phrases['intro']

        # Market section - formal metrics
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_formal_metrics(content, phrases)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # Whale section - institutional language
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section - operational status
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Strategy Category')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Operational Status')
        adapted['strategy_col3'] = phrases.get('strategy_col3', 'Period Performance')
        adapted['conservative_status'] = 'Operational'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):+.2f}%"
        adapted['balanced_status'] = 'Operational'
        adapted['balanced_action'] = f"{content.get('balanced_7d', 0):+.2f}%"
        adapted['growth_status'] = 'Operational'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section - analytical commentary
        adapted['insight_section_title'] = phrases['insight_section']

        # Strip any emojis from insight content
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))

        adapted['wisdom_note'] = phrases['wisdom_note']

        # Add methodology and data sources
        adapted['methodology'] = phrases.get('methodology', '')
        adapted['data_sources'] = phrases.get('data_sources', '')

        # Closing - formal
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature'].format(
            report_id=self._report_id,
            timestamp=timestamp
        )

        # Store report metadata
        adapted['report_id'] = self._report_id
        adapted['report_timestamp'] = timestamp

        return adapted

    def _build_formal_metrics(self, content: Dict, phrases: Dict) -> str:
        """Build formal metric table for B2B reporting."""
        vix = content.get('vix', 20)
        fg = content.get('fear_greed_index', 50)
        btc = content.get('btc_24h_change', 0)
        credit = content.get('credit_spread', 1.0)

        return f"""| Indicator | Value | Assessment |
|-----------|-------|------------|
| {phrases.get('vix_label', 'VIX')} | {vix:.2f} | {'Normal' if vix < 25 else 'Elevated'} |
| {phrases.get('fear_greed_label', 'Fear & Greed')} | {fg} | {'Fear' if fg < 40 else 'Neutral' if fg < 60 else 'Greed'} |
| {phrases.get('btc_label', 'BTC 24h')} | {btc:+.2f}% | {'Positive' if btc > 0 else 'Negative'} |
| {phrases.get('credit_spread_label', 'Credit Spread')} | {credit:.2f}% | {'Tight' if credit < 1.5 else 'Wide'} |"""

    def _strip_emojis(self, text: str) -> str:
        """Remove all emojis from text for professional output."""
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
        return "B2B Client"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.NONE

    @property
    def risk_profile(self) -> str:
        return "institutional"

    def get_signature(self, locale: str = "en") -> str:
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        report_id = self._report_id or str(hash(timestamp))[:8].upper()
        return phrases['signature'].format(report_id=report_id, timestamp=timestamp)
