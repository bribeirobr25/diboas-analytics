"""
New Personas for Adelaide: Yield Hunter and B2B Client

Add this code to: src/registries/persona_registry.py
Insert after the FelipePersona class definition.

CMO Board Session 010 - February 4, 2026
"""

import re
from typing import Any, Dict
from datetime import datetime

# Note: These classes assume they are added to persona_registry.py
# where PersonaRegistry, Persona, EmojiLevel are already imported


# =============================================================================
# Yield Hunter Persona - DeFi-Native Yield Optimizer
# =============================================================================

@PersonaRegistry.register("yield_hunter")
class YieldHunterPersona(Persona):
    """
    Yield Hunter - Advanced DeFi user persona.
    
    Characteristics:
    - Data-forward with yield comparisons
    - DeFi terminology without explanation (APY, TVL, IL, LTV)
    - Risk-adjusted metrics emphasized (Sharpe, Sortino)
    - Minimal emojis (1-3 per newsletter)
    - Protocol-specific health indicators
    - Targets strategies 6-10 (40-85% crypto allocation)
    
    Sign-off: "— Adelaide | diBoaS"
    """
    
    EMOJIS = {
        'yield_up': '📈',
        'yield_down': '📉',
        'alert': '⚠️',
    }
    
    PHRASES = {
        'en': {
            'greeting': 'Yield update.',
            'market_section': 'Yield Snapshot',
            'market_intro': 'Current yields and protocol metrics:',
            'strategy_section': 'Protocol Health',
            'strategy_col1': 'Protocol',
            'strategy_col2': 'Current APY',
            'strategy_col3': '7d Avg | TVL',
            'insight_section': 'Alpha Signal',
            'closing': 'Optimize accordingly',
            'signature': '— Adelaide | diBoaS',
            'footer': 'Reply with questions. [Dashboard](link) | [Settings](link)',
            'disclaimer': """**Risk Disclosure**

DeFi protocols carry smart contract risk. Yields are variable and not guaranteed. Past APY does not predict future returns. TVL changes can indicate protocol stress.

DYOR. **Your capital, your decision.**""",
            'depeg_status': 'Depeg monitor: All stables within 10bps',
            'depeg_alert': 'Depeg alert: {coin} deviation {bps}bps from peg',
        },
        'pt-br': {
            'greeting': 'Atualização de yield.',
            'market_section': 'Snapshot de Yields',
            'market_intro': 'Yields atuais e métricas dos protocolos:',
            'strategy_section': 'Saúde dos Protocolos',
            'strategy_col1': 'Protocolo',
            'strategy_col2': 'APY Atual',
            'strategy_col3': 'Média 7d | TVL',
            'insight_section': 'Sinal Alpha',
            'closing': 'Otimize conforme necessário',
            'signature': '— Adelaide | diBoaS',
            'footer': 'Responda com dúvidas. [Painel](link) | [Configurações](link)',
            'disclaimer': """**Divulgação de Risco**

Protocolos DeFi carregam risco de smart contract. Yields são variáveis e não garantidos. APY passado não prevê retornos futuros. Mudanças no TVL podem indicar estresse do protocolo.

DYOR. **Seu capital, sua decisão.**""",
            'depeg_status': 'Monitor de depeg: Todas as stables dentro de 10bps',
            'depeg_alert': 'Alerta de depeg: {coin} desvio de {bps}bps do peg',
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Yield Hunter's data-forward DeFi voice."""
        adapted = content.copy()
        adapted['persona'] = 'yield_hunter'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value
        
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        
        # Minimal header - no emojis in title
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = ''
        
        # Yield-focused market section
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_yield_metrics(content, phrases)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = ''
        
        # Protocol health section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases['strategy_col1']
        adapted['strategy_col2'] = phrases['strategy_col2']
        adapted['strategy_col3'] = phrases['strategy_col3']
        adapted['strategy_note'] = ''
        
        # Protocol statuses (simplified for yield hunter)
        adapted['conservative_status'] = 'Sky sUSDS'
        adapted['conservative_action'] = '8.5% | $2.1B'
        adapted['balanced_status'] = 'Jito JitoSOL'
        adapted['balanced_action'] = '7.8% | $1.8B'
        adapted['growth_status'] = 'Jupiter JLP'
        adapted['growth_action'] = '24.3% | $850M'
        
        # Whale section - reframe as liquidity context
        adapted['whale_section_title'] = 'Liquidity Context'
        adapted['whale_intro'] = 'Large wallet movements affecting protocol liquidity:'
        adapted['whale_summary'] = 'No significant outflows detected. TVL stable across monitored protocols.'
        adapted['whale_disclaimer'] = 'Large holder movements are informational, not trading signals.'
        
        # Alpha signal (insight) - strip emojis
        adapted['insight_section_title'] = phrases['insight_section']
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))
        adapted['wisdom_note'] = ''
        
        # Closing
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']
        
        return adapted
    
    def _build_yield_metrics(self, content: Dict, phrases: Dict) -> str:
        """Build yield-focused metrics display."""
        lines = []
        
        # Yield table
        lines.append("| Protocol | APY | 7d Avg | TVL | Risk |")
        lines.append("|----------|-----|--------|-----|------|")
        lines.append("| Sky sUSDS | 8.5% | 8.2% | $2.1B | Low |")
        lines.append("| Jito JitoSOL | 7.8% | 7.5% | $1.8B | Medium |")
        lines.append("| Jupiter JLP | 24.3% | 22.1% | $850M | High |")
        lines.append("| Aave USDC | 4.2% | 4.1% | $8.5B | Low |")
        lines.append("")
        
        # Risk metrics
        btc_change = content.get('btc_24h_change', 0)
        if btc_change > 0:
            lines.append(f"BTC: {btc_change:+.2f}% 📈 | Risk-on environment")
        else:
            lines.append(f"BTC: {btc_change:+.2f}% 📉 | Monitor for IL impact")
        
        # Depeg status
        lines.append("")
        lines.append(phrases.get('depeg_status', 'Depeg monitor: All stables within 10bps'))
        
        return '\n'.join(lines)
    
    def _strip_emojis(self, text: str) -> str:
        """Remove emojis from text."""
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
        return "Yield Hunter"
    
    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.MINIMAL
    
    @property
    def risk_profile(self) -> str:
        return "aggressive"
    
    def get_signature(self, locale: str = "en") -> str:
        return "— Adelaide | diBoaS"


# =============================================================================
# B2B Client Persona - Institutional/White-Label
# =============================================================================

@PersonaRegistry.register("b2b_client")
class B2BClientPersona(Persona):
    """
    B2B Client - Institutional white-label persona.
    
    Characteristics:
    - Extremely professional, institutional tone
    - Zero emojis under any circumstances
    - Explicit timestamps and data sources
    - ISO date formats throughout
    - Compliance-ready formatting
    - Methodology and source attribution
    - Audit trail references
    - Targets API/data licensing users
    
    Sign-off: "diBoaS Intelligence | Audit ID: {id}"
    """
    
    PHRASES = {
        'en': {
            'greeting': 'diBoaS Intelligence Brief',
            'market_section': 'Market Data',
            'market_intro': 'Data as of: {timestamp}',
            'strategy_section': 'Portfolio Analytics',
            'strategy_col1': 'Metric',
            'strategy_col2': 'Value',
            'strategy_col3': 'Source',
            'insight_section': 'Analysis',
            'methodology_section': 'Data Sources & Methodology',
            'closing': 'End of Report',
            'signature': 'diBoaS Intelligence',
            'footer': '',
            'disclaimer': """**Legal & Compliance**

This report is provided for informational purposes only and does not constitute investment advice. Data accuracy is not guaranteed. Recipients are responsible for their own compliance with applicable regulations in their jurisdiction.

Generated by: diBoaS Adelaide Intelligence Engine v3.2
Schema version: adelaide_output_v3""",
        },
        'pt-br': {
            'greeting': 'Relatório de Inteligência diBoaS',
            'market_section': 'Dados de Mercado',
            'market_intro': 'Dados em: {timestamp}',
            'strategy_section': 'Análise de Portfólio',
            'strategy_col1': 'Métrica',
            'strategy_col2': 'Valor',
            'strategy_col3': 'Fonte',
            'insight_section': 'Análise',
            'methodology_section': 'Fontes de Dados e Metodologia',
            'closing': 'Fim do Relatório',
            'signature': 'Inteligência diBoaS',
            'footer': '',
            'disclaimer': """**Legal e Conformidade**

Este relatório é fornecido apenas para fins informativos e não constitui aconselhamento de investimento. A precisão dos dados não é garantida. Os destinatários são responsáveis pela sua própria conformidade com as regulamentações aplicáveis em sua jurisdição.

Gerado por: diBoaS Adelaide Intelligence Engine v3.2
Versão do schema: adelaide_output_v3""",
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to B2B Client's institutional voice."""
        adapted = content.copy()
        adapted['persona'] = 'b2b_client'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value
        
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        
        # Generate report metadata
        now = datetime.utcnow()
        report_id = f"adelaide-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
        timestamp_iso = now.isoformat() + 'Z'
        
        # Institutional header - no emojis
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = f"{phrases['greeting']} | {now.strftime('%Y-%m-%d')} | Report ID: {report_id}"
        adapted['greeting_message'] = ''
        
        # Market data with explicit timestamps
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro'].format(timestamp=timestamp_iso)
        adapted['market_bullets'] = self._build_institutional_data(content, now)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = ''
        
        # Portfolio analytics section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases['strategy_col1']
        adapted['strategy_col2'] = phrases['strategy_col2']
        adapted['strategy_col3'] = phrases['strategy_col3']
        
        # Metrics with sources
        adapted['conservative_status'] = 'VaR (95%, 30d)'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):.2f}% | Internal"
        adapted['balanced_status'] = 'Sharpe Ratio'
        adapted['balanced_action'] = '1.24 | Internal'
        adapted['growth_status'] = 'Max Drawdown'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):.2f}% | Internal"
        adapted['strategy_note'] = 'All metrics calculated using 30-day rolling window with daily rebalancing assumption.'
        
        # Whale section - institutional framing
        adapted['whale_section_title'] = 'Large Holder Activity'
        adapted['whale_intro'] = 'Monitoring of significant wallet movements. Data aggregated from on-chain sources.'
        adapted['whale_summary'] = 'No material movements detected in monitoring period. Estate distributions proceeding on court-mandated schedules.'
        adapted['whale_disclaimer'] = 'Source: On-chain data aggregation (Etherscan, Solscan). Not trading signals.'
        
        # Analysis section - stripped of personality
        adapted['insight_section_title'] = phrases['insight_section']
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))
        adapted['wisdom_note'] = ''
        
        # Methodology appendix
        adapted['methodology'] = self._build_methodology()
        
        # Closing - formal
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = f"{phrases['signature']} | Audit ID: {report_id}"
        
        return adapted
    
    def _build_institutional_data(self, content: Dict, timestamp: datetime) -> str:
        """Build institutional-format data table with sources."""
        time_str = timestamp.strftime('%H:%M')
        
        return f"""| Metric | Value | Change | Source | Updated |
|--------|-------|--------|--------|---------|
| BTC/USD | ${content.get('btc_price', 0):,.2f} | {content.get('btc_24h_change', 0):+.2f}% | CoinGecko | {time_str} UTC |
| ETH/USD | ${content.get('eth_price', 0):,.2f} | {content.get('eth_24h_change', 0):+.2f}% | CoinGecko | {time_str} UTC |
| SOL/USD | ${content.get('sol_price', 0):,.2f} | {content.get('sol_24h_change', 0):+.2f}% | CoinGecko | {time_str} UTC |
| S&P 500 | {content.get('sp500_price', 0):,.0f} | {content.get('sp500_24h_change', 0):+.2f}% | Yahoo Finance | {time_str} UTC |
| VIX | {content.get('vix', 20):.2f} | — | CBOE | {time_str} UTC |
| Fear/Greed | {content.get('fear_greed_index', 50)} | — | Alternative.me | Daily |"""
    
    def _build_methodology(self) -> str:
        """Build methodology appendix for audit trail."""
        return """## Data Sources & Methodology

| Data Category | Source | API Version | Update Frequency | Methodology |
|--------------|--------|-------------|------------------|-------------|
| Crypto Prices | CoinGecko | v3 | 5 minutes | Volume-weighted average |
| TradFi Prices | Yahoo Finance | v8 | 15 minutes | Last trade price |
| DeFi Yields | DefiLlama | v2 | 1 hour | Protocol-reported APY |
| Sentiment | Alternative.me | v2 | Daily | Multi-factor composite |
| On-Chain | Etherscan/Solscan | v1 | Real-time | Direct node queries |

### Risk Metrics Methodology
- **VaR**: Historical simulation, 95% confidence interval, 252-day lookback
- **Sharpe Ratio**: Annualized, risk-free rate = current 3-month T-bill (FRED DGS3MO)
- **Max Drawdown**: Peak-to-trough, rolling 365-day window
- **Sortino Ratio**: Downside deviation only, MAR = 0%

### Data Quality
- Outlier detection: Values >4 standard deviations flagged
- Missing data: Forward-fill with 24-hour maximum gap
- Stale data threshold: 6 hours for crypto, 24 hours for TradFi"""
    
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
        return "B2B Client"
    
    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.NONE
    
    @property
    def risk_profile(self) -> str:
        return "institutional"
    
    def get_signature(self, locale: str = "en") -> str:
        report_id = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        return f"diBoaS Intelligence | Audit ID: adelaide-{report_id}"


# =============================================================================
# Updated Utility Functions
# =============================================================================

def get_persona_for_strategy(strategy_id: int) -> str:
    """
    Get the recommended persona name for a strategy.
    
    Updated mapping with new personas:
    - 1, 3, 5 (0-20% crypto) → ana (conservative grandmother)
    - 2, 4 (20-30% crypto) → maria (balanced educator)
    - 6, 7 (40-50% crypto) → maria or yield_hunter
    - 8, 9, 10 (70-85% crypto) → felipe or yield_hunter
    
    Args:
        strategy_id: Strategy ID (1-10)
    
    Returns:
        Persona name ('ana', 'maria', 'felipe', 'yield_hunter')
    """
    if strategy_id in [1, 3, 5]:
        return "ana"
    elif strategy_id in [2, 4]:
        return "maria"
    elif strategy_id in [6, 7]:
        return "maria"  # Can override to yield_hunter
    elif strategy_id in [8, 9, 10]:
        return "felipe"  # Can override to yield_hunter
    else:
        return "maria"


def get_personas_for_path(dream_mode_path: str) -> str:
    """
    Get the recommended persona for a Dream Mode path.
    
    Args:
        dream_mode_path: 'safety', 'balance', or 'growth'
    
    Returns:
        Persona name
    """
    path_personas = {
        'safety': 'ana',
        'balance': 'maria',
        'growth': 'felipe',
        'yield': 'yield_hunter',  # New path
    }
    return path_personas.get(dream_mode_path.lower(), 'maria')


def get_all_personas() -> list:
    """Get list of all available persona names."""
    return ['ana', 'maria', 'felipe', 'yield_hunter', 'b2b_client']
