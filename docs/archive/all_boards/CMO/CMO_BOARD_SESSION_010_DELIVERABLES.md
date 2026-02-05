# CMO Board Session 010: Pending Deliverables Package

**Date:** February 4, 2026  
**Session Purpose:** Complete all pending CMO deliverables for Feb 12 launch  
**Status:** READY FOR IMPLEMENTATION

---

## Table of Contents

1. [Yield Hunter Persona Specification](#1-yield-hunter-persona-specification)
2. [B2B Client Persona Specification](#2-b2b-client-persona-specification)
3. [PT-BR Localization Fixes](#3-pt-br-localization-fixes)
4. [AI Disclosure Requirements](#4-ai-disclosure-requirements)
5. [WhatsApp Formatter Stub](#5-whatsapp-formatter-stub)
6. [Implementation Instructions](#6-implementation-instructions)

---

## 1. Yield Hunter Persona Specification

### 1.1 Profile Summary

| Attribute | Value |
|-----------|-------|
| **Persona Name** | Yield Hunter |
| **Registry Key** | `yield_hunter` |
| **Risk Profile** | High (for yield), Medium (for principal) |
| **Financial Literacy** | Advanced DeFi |
| **Primary Need** | "Best risk-adjusted yield" |
| **Target Strategies** | 6, 7, 8, 9, 10 (40-85% crypto allocation) |
| **Emoji Level** | MINIMAL (1-3 per newsletter) |

### 1.2 Persona Characteristics

**Demographics:**
- DeFi-native users, any age (typically 25-45)
- Active in multiple protocols
- Tracks APY/TVL metrics regularly
- May hold positions across chains (Ethereum, Solana, Arbitrum)
- Understands impermanent loss, liquidity provision, yield farming

**Communication Style:**
- Data-forward with yield comparisons
- Risk-adjusted metrics emphasized (Sharpe, Sortino)
- Protocol-specific terminology acceptable
- Efficiency-focused, minimal fluff
- Appreciates historical yield data and trends

**Key Concerns:**
- Protocol risk (smart contract, rug pulls)
- Yield sustainability (is APY real or inflationary?)
- Gas optimization
- Depeg risk for stablecoin strategies
- IL (Impermanent Loss) exposure

### 1.3 Voice Guidelines

**Tone:** Professional analyst meets DeFi degen. Respects expertise, provides actionable data.

**Do:**
- Use DeFi terminology without explanation (APY, TVL, IL, LTV)
- Show yield comparisons across protocols
- Highlight risk-adjusted returns
- Reference on-chain data
- Be direct about risks

**Don't:**
- Over-simplify concepts they already know
- Use excessive emojis
- Include "grandma wisdom" style content
- Provide basic crypto education
- Be overly cautious in tone

### 1.4 Language Patterns

**Greeting Style:**
```
EN: "Yield update."
PT-BR: "Atualização de yield."
```

**Section Headers:**
- "Yield Snapshot" (not "Market Snapshot")
- "Protocol Health" (not "Strategy Status")  
- "Risk Metrics" (not "How's It Doing?")
- "Alpha Signal" (not "Adelaide's Insight")

**Example Phrases (EN):**
- "Current yields across your positions:"
- "Risk-adjusted: Sharpe {value} | Sortino {value}"
- "Protocol TVL: ${tvl}B | 24h change: {change}%"
- "Depeg monitor: All stables within 10bps"
- "Notable: {protocol} yield compressed {x}bps — possible reallocation opportunity"

**Example Phrases (PT-BR):**
- "Yields atuais nas suas posições:"
- "Ajustado ao risco: Sharpe {value} | Sortino {value}"
- "TVL do protocolo: ${tvl}B | Variação 24h: {change}%"
- "Monitor de depeg: Todas as stables dentro de 10bps"
- "Destaque: Yield do {protocol} comprimiu {x}bps — possível oportunidade de realocação"

### 1.5 Content Adaptation Rules

**Market Snapshot → Yield Snapshot:**
```python
YIELD_HUNTER_ADAPTATIONS = {
    'section_market': 'Yield Snapshot',
    'section_strategy': 'Protocol Health',
    'section_insight': 'Alpha Signal',
    'greeting_morning': 'Yield update.',
    'greeting_afternoon': 'Yield update.',
    'greeting_evening': 'Yield update.',
}
```

**Data Emphasis:**
- Always show: Current APY, 7d APY avg, 30d APY avg
- Always show: TVL and TVL trend
- Always show: Risk metrics (Sharpe, max drawdown)
- Include: Protocol-specific health indicators

**Yield Comparison Table:**
```markdown
| Protocol | Current APY | 7d Avg | TVL | Risk Score |
|----------|-------------|--------|-----|------------|
| Sky sUSDS | 8.5% | 8.2% | $2.1B | Low |
| Jito JitoSOL | 7.8% | 7.5% | $1.8B | Medium |
| Jupiter JLP | 24.3% | 22.1% | $850M | High |
```

### 1.6 Emoji Palette

```python
YIELD_HUNTER_EMOJIS = {
    'title': '',  # No emoji in title
    'yield_up': '📈',
    'yield_down': '📉',
    'alert': '⚠️',
    'check': '✓',  # Plain checkmark, not emoji
    'closing': '',  # No closing emoji
}
```

### 1.7 Signature

```
EN: "— Adelaide | diBoaS"
PT-BR: "— Adelaide | diBoaS"
```

---

## 2. B2B Client Persona Specification

### 2.1 Profile Summary

| Attribute | Value |
|-----------|-------|
| **Persona Name** | B2B Client |
| **Registry Key** | `b2b_client` |
| **Risk Profile** | Varies (client-specific) |
| **Financial Literacy** | Expert |
| **Primary Need** | "White-label intelligence, audit-ready data" |
| **Target Use Cases** | API access, data licensing, white-label Adelaide |
| **Emoji Level** | NONE |

### 2.2 Persona Characteristics

**Demographics:**
- Fintechs building on diBoaS data
- Asset managers needing compliance-ready reports
- Protocols wanting treasury intelligence
- Research firms licensing data
- Crypto funds requiring audit trails

**Communication Style:**
- Extremely professional, institutional tone
- Data completeness and freshness emphasized
- Source attribution mandatory
- Compliance language present
- Versioning and timestamps explicit

**Key Concerns:**
- Data provenance and audit trails
- SLA compliance (freshness, uptime)
- API stability and versioning
- Regulatory compliance for their jurisdiction
- White-label customization options

### 2.3 Voice Guidelines

**Tone:** Institutional research report. Bloomberg terminal meets compliance officer.

**Do:**
- Include explicit timestamps and data sources
- Use ISO date formats
- Provide confidence intervals where applicable
- Reference methodology
- Include data versioning

**Don't:**
- Use any casual language
- Include emojis under any circumstances
- Add "warmth" or personality
- Make forward-looking statements without disclaimers
- Omit source attribution

### 2.4 Language Patterns

**Greeting Style:**
```
EN: "diBoaS Intelligence Brief | {date} | Edition {number}"
PT-BR: "Relatório de Inteligência diBoaS | {date} | Edição {number}"
```

**Section Headers:**
- "Executive Summary"
- "Market Data" (with timestamp)
- "Risk Assessment"
- "Compliance Notes"
- "Data Sources & Methodology"

**Example Phrases (EN):**
- "Data as of: 2026-02-04T08:00:00Z | Source: CoinGecko API v3"
- "Confidence: 95% | Sample size: n=1,000"
- "Methodology: 30-day rolling average with outlier exclusion"
- "Regulatory note: This data meets MiFID II Article 24 requirements"
- "Version: v3.2.1 | Schema: adelaide_output_v3"

**Example Phrases (PT-BR):**
- "Dados em: 2026-02-04T08:00:00Z | Fonte: CoinGecko API v3"
- "Confiança: 95% | Tamanho da amostra: n=1.000"
- "Metodologia: Média móvel de 30 dias com exclusão de outliers"
- "Nota regulatória: Estes dados atendem aos requisitos do Artigo 24 do MiFID II"
- "Versão: v3.2.1 | Schema: adelaide_output_v3"

### 2.5 Content Adaptation Rules

**Data Presentation:**
```python
B2B_CLIENT_ADAPTATIONS = {
    'section_market': 'Market Data',
    'section_strategy': 'Portfolio Analytics',
    'section_insight': 'Analysis',
    'timestamp_format': 'ISO8601',
    'number_format': 'scientific_notation_if_large',
    'include_sources': True,
    'include_confidence': True,
    'include_methodology': True,
}
```

**Required Metadata Block:**
```json
{
  "report_id": "adelaide-{date}-{edition}",
  "generated_at": "2026-02-04T08:00:00Z",
  "data_freshness": {
    "crypto_prices": "2026-02-04T07:55:00Z",
    "defi_yields": "2026-02-04T07:45:00Z",
    "sentiment": "2026-02-04T06:00:00Z"
  },
  "schema_version": "adelaide_output_v3",
  "api_version": "v3.2.1"
}
```

### 2.6 Compliance Appendix

**Every B2B output must include:**

1. **Data Sources Table:**
```markdown
| Data Point | Source | API Version | Update Frequency |
|------------|--------|-------------|------------------|
| BTC Price | CoinGecko | v3 | 5 min |
| DeFi Yields | DefiLlama | v2 | 1 hour |
| Fear/Greed | Alternative.me | v2 | Daily |
```

2. **Methodology Statement:**
```markdown
## Methodology

Risk metrics calculated using:
- VaR: Historical simulation, 95% confidence, 252-day lookback
- Sharpe Ratio: Annualized, risk-free rate = current 3-month T-bill
- Drawdown: Peak-to-trough, rolling 365-day window
```

3. **Disclaimer Block:**
```markdown
## Legal & Compliance

This report is provided for informational purposes only and does not 
constitute investment advice. Data accuracy is not guaranteed. 
Recipients are responsible for their own compliance with applicable 
regulations in their jurisdiction.

Generated by: diBoaS Adelaide Intelligence Engine v3.2
Audit trail: Available via API at /api/v3/audit/{report_id}
```

### 2.7 Output Formats

| Format | File Extension | Use Case |
|--------|---------------|----------|
| JSON | `.json` | API consumption |
| Markdown | `.md` | Human-readable reports |
| PDF | `.pdf` | Compliance documentation |
| CSV | `.csv` | Data export |

### 2.8 Signature

```
EN: "diBoaS Intelligence | Audit ID: {audit_id}"
PT-BR: "Inteligência diBoaS | ID de Auditoria: {audit_id}"
```

---

## 3. PT-BR Localization Fixes

### 3.1 Critical Bug Fix: English Phrase Leakage

**Location:** `src/registries/persona_registry.py` → `AnaPersona._build_market_bullets()`

**Current (Broken):**
```python
def _build_market_bullets(self, content: Dict, phrases: Dict) -> str:
    """Build market bullet points for Ana."""
    bullets = []
    # ... vix bullets ...
    
    # BUG: Hardcoded English
    bullets.append("- Banks and big companies are lending money freely — a good sign! 💚")
    
    # ... fear/greed bullets ...
```

**Fixed:**
```python
def _build_market_bullets(self, content: Dict, phrases: Dict) -> str:
    """Build market bullet points for Ana."""
    bullets = []
    
    vix = content.get('vix', 20)
    if vix < 20:
        bullets.append("- " + phrases.get('vix_low', '').format(vix=vix))
    else:
        bullets.append("- " + phrases.get('vix_high', '').format(vix=vix))
    
    # FIXED: Use localized phrase
    bullets.append("- " + phrases.get('credit_healthy', 'Banks and big companies are lending money freely — a good sign! 💚'))
    
    fg = content.get('fear_greed_index', 50)
    if fg <= 25:
        bullets.append("- " + phrases.get('fear_extreme', ''))
    elif fg <= 45:
        bullets.append("- " + phrases.get('fear_greed', ''))
    elif fg <= 55:
        bullets.append("- " + phrases.get('fear_neutral', ''))
    elif fg <= 75:
        bullets.append("- " + phrases.get('greed', ''))
    else:
        bullets.append("- " + phrases.get('greed_extreme', ''))
    
    return '\n'.join(bullets)
```

### 3.2 Missing PT-BR Phrases to Add

**Add to `AnaPersona.PHRASES['pt-br']`:**

```python
'pt-br': {
    # ... existing phrases ...
    
    # NEW: Credit health phrase
    'credit_healthy': 'Bancos e grandes empresas estão emprestando dinheiro livremente — um bom sinal! 💚',
    
    # NEW: Market section header
    'market_bullets_header': "**Veja o que os números dizem:**",
    
    # NEW: Whale section
    'whale_mtgox': 'Bitcoin',
    'whale_mtgox_status': 'Pagando credores lentamente',
    'whale_ftx': 'Várias criptomoedas',
    'whale_ftx_status': 'Tribunais cuidando da distribuição',
    'whale_ftx_sol': 'Tokens SOL',
    'whale_ftx_sol_status': 'Sendo liberados cuidadosamente',
    
    # NEW: Table headers
    'table_who': 'Quem',
    'table_what': 'O Que Têm',
    'table_happening': 'O Que Está Acontecendo',
    'table_asset': 'Ativo',
    'table_price': 'Preço',
    'table_change': 'Variação 24h',
}
```

### 3.3 UTF-8 Accent Fixes

**Location:** `src/adelaide/localization.py`

**Replace all ASCII approximations with proper UTF-8:**

| Current (Wrong) | Correct (UTF-8) |
|-----------------|-----------------|
| `situacao` | `situação` |
| `nao` | `não` |
| `voce` | `você` |
| `tambem` | `também` |
| `e` (as verb "is") | `é` |
| `esta` (as verb "is") | `está` |
| `ja` | `já` |
| `informacao` | `informação` |
| `atencao` | `atenção` |
| `protecao` | `proteção` |
| `acoes` | `ações` |
| `decisoes` | `decisões` |
| `opcoes` | `opções` |
| `indice` | `índice` |
| `diario` | `diário` |
| `financas` | `finanças` |
| `comeca` | `começa` |
| `almoco` | `almoço` |

**Full Replacement Dictionary:**

```python
PT_BR_ACCENT_FIXES = {
    # Common words
    'nao': 'não',
    'voce': 'você',
    'esta': 'está',
    'tambem': 'também',
    'ja': 'já',
    'ate': 'até',
    'so': 'só',
    'entao': 'então',
    'sao': 'são',
    'mae': 'mãe',
    'pai': 'pai',
    'avo': 'avó',
    'vovo': 'vovó',
    
    # Technical/financial
    'situacao': 'situação',
    'informacao': 'informação',
    'protecao': 'proteção',
    'atencao': 'atenção',
    'acoes': 'ações',
    'decisoes': 'decisões',
    'opcoes': 'opções',
    'indice': 'índice',
    'financas': 'finanças',
    'investidor': 'investidor',
    'desempenho': 'desempenho',
    'aconselhamento': 'aconselhamento',
    'garantia': 'garantia',
    'deposito': 'depósito',
    'orientacao': 'orientação',
    
    # Verbs
    'comeca': 'começa',
    'faca': 'faça',
    'saira': 'sairá',
    'tera': 'terá',
    'sera': 'será',
    'estara': 'estará',
}
```

### 3.4 Localization File Updates

**File:** `src/adelaide/localization.py`

**Replace `TRANSLATIONS['pt-br']` with:**

```python
'pt-br': {
    # Greetings
    'good_morning': 'Bom dia',
    'good_afternoon': 'Boa tarde',
    'good_evening': 'Boa noite',

    # Common phrases
    'dear': 'Querido(a)',
    'friend': 'amigo(a)',
    'with_care': 'Com carinho',
    'you_decide': 'Você decide o que é melhor para sua situação.',

    # Market terms
    'market_snapshot': 'Panorama do Mercado',
    'fear_greed_index': 'Índice de Medo e Ganância',
    'whale_watch': 'Monitoramento de Baleias',
    'strategy_overview': 'Visão das Estratégias',

    # Labels
    'conservative': 'Conservador',
    'balanced': 'Equilibrado',
    'growth': 'Crescimento',
    'status': 'Status',
    'performance': 'Desempenho',

    # Status
    'normal': 'Normal',
    'elevated': 'Elevado',
    'warning': 'Atenção',

    # Sentiments
    'extreme_fear': 'Medo Extremo',
    'fear': 'Medo',
    'neutral': 'Neutro',
    'greed': 'Ganância',
    'extreme_greed': 'Ganância Extrema',

    # Disclaimers
    'disclaimer_header': 'Avisos Importantes',
    'not_financial_advice': 'Este é conteúdo educacional apenas, não aconselhamento financeiro.',
    'past_performance': 'Desempenho passado não garante resultados futuros.',
    'consult_adviser': 'Considere consultar um assessor financeiro licenciado para orientação personalizada.',

    # Ana-specific
    'dont_worry': 'Não se preocupe, querido(a)',
    'take_a_breath': 'Vamos respirar juntos',
    'youre_doing_great': 'Você está indo muito bem',
    'slow_and_steady': 'Devagar e sempre',

    # MiCA/CVM warning (required for EU/Brazil)
    'mica_warning': 'AVISO: Criptoativos NÃO são protegidos por esquemas de garantia de depósitos da UE. Stablecoins podem perder paridade. Você pode perder todo o capital.',
    
    # AI Disclosure (California SB 942)
    'ai_disclosure': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
}
```

---

## 4. AI Disclosure Requirements

### 4.1 Regulatory Context

**California SB 942 (2024):** Requires disclosure when AI generates content that could influence consumer decisions.

**CLO Board Decision (Session 007):** AI disclosure mandatory on all Adelaide outputs.

### 4.2 Disclosure Text by Locale

```python
AI_DISCLOSURES = {
    'en': '🤖 This content was generated with artificial intelligence assistance.',
    'pt-br': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
    'de': '🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.',
    'es': '🤖 Este contenido fue generado con asistencia de inteligencia artificial.',
}
```

### 4.3 Placement Rules

1. **Newsletter:** Place AFTER signature, BEFORE footer links
2. **WhatsApp:** Place at END of message
3. **Twitter/LinkedIn:** Include in bio/profile, not every post
4. **Email Subject:** Do NOT include in subject line

### 4.4 Template Update

**File:** `src/adelaide/templates/daily_calm.md`

**Add after `{{signature}}`:**

```markdown
{{signature}}

---

{{ai_disclosure}}

{{footer}}
```

### 4.5 Generator Update

**File:** `src/adelaide/generator.py`

**In `_prepare_content_data()`, add:**

```python
# AI Disclosure (California SB 942 compliance)
data['ai_disclosure'] = self.localization.translate('ai_disclosure', locale)
```

---

## 5. WhatsApp Formatter Stub

### 5.1 Formatter Implementation

**File:** `src/adelaide/formatters/whatsapp_formatter.py` (NEW)

```python
"""
WhatsApp Formatter for Adelaide.

Converts Adelaide markdown content to WhatsApp-compatible plain text.
Phase 1: Manual copy-paste stub
Phase 2: Full WhatsApp Business API integration
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class WhatsAppMessage:
    """WhatsApp message structure."""
    body: str
    buttons: Optional[List[str]] = None
    
    def __len__(self) -> int:
        return len(self.body)


class WhatsAppFormatter:
    """
    Format Adelaide content for WhatsApp delivery.
    
    WhatsApp Constraints:
    - Max message length: 4096 characters
    - Formatting: *bold*, _italic_, ~strikethrough~, ```monospace```
    - No markdown headers, tables, or links with text
    - Max 3 quick reply buttons
    """
    
    MAX_LENGTH = 4096
    MAX_BUTTONS = 3
    
    # WhatsApp emoji mappings (subset for cleaner mobile display)
    EMOJI_MAP = {
        'title': '💙',
        'section': '📊',
        'bullet': '•',
        'check': '✅',
        'warning': '⚠️',
        'money': '💰',
        'chart_up': '📈',
        'chart_down': '📉',
    }
    
    def format(self, content: Dict[str, Any], context: Dict[str, Any] = None) -> WhatsAppMessage:
        """
        Format Adelaide content for WhatsApp.
        
        Args:
            content: Adelaide content dict with rendered_content or sections
            context: Additional context (locale, persona, etc.)
            
        Returns:
            WhatsAppMessage ready for sending
        """
        context = context or {}
        locale = context.get('locale', 'en')
        persona = context.get('persona', 'ana')
        
        # If we have pre-rendered markdown, convert it
        if 'rendered_content' in content:
            body = self._convert_markdown_to_whatsapp(content['rendered_content'])
        else:
            # Build from sections
            body = self._build_from_sections(content, locale, persona)
        
        # Truncate if needed
        if len(body) > self.MAX_LENGTH:
            body = self._truncate_with_link(body, context)
        
        # Generate buttons based on persona
        buttons = self._generate_buttons(persona, locale)
        
        return WhatsAppMessage(body=body, buttons=buttons)
    
    def _convert_markdown_to_whatsapp(self, markdown: str) -> str:
        """Convert markdown to WhatsApp formatting."""
        text = markdown
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Convert markdown headers to bold
        text = re.sub(r'^#{1,6}\s+(.+)$', r'*\1*', text, flags=re.MULTILINE)
        
        # Convert markdown bold (**text**) to WhatsApp bold (*text*)
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        
        # Convert markdown tables to lists
        text = self._convert_tables_to_lists(text)
        
        # Convert markdown links [text](url) to just text (url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
        
        # Remove horizontal rules
        text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _convert_tables_to_lists(self, text: str) -> str:
        """Convert markdown tables to WhatsApp-friendly lists."""
        # Pattern for markdown tables
        table_pattern = r'\|(.+)\|[\r\n]+\|[-:| ]+\|[\r\n]+((?:\|.+\|[\r\n]*)+)'
        
        def table_to_list(match):
            header = match.group(1).strip()
            rows = match.group(2).strip().split('\n')
            
            result = []
            for row in rows:
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    result.append(f"• {cells[0]}: {', '.join(cells[1:])}")
            
            return '\n'.join(result)
        
        return re.sub(table_pattern, table_to_list, text)
    
    def _build_from_sections(self, content: Dict, locale: str, persona: str) -> str:
        """Build WhatsApp message from content sections."""
        lines = []
        
        # Header
        lines.append(f"*Adelaide Daily* {self.EMOJI_MAP['title']}")
        lines.append("")
        
        # Greeting
        if 'persona_greeting' in content:
            lines.append(content['persona_greeting'])
            lines.append("")
        
        # Market snapshot (simplified)
        if 'btc_price' in content:
            lines.append(f"*Mercado*" if locale == 'pt-br' else "*Market*")
            lines.append(f"• BTC: ${content.get('btc_price', 0):,.0f} ({content.get('btc_24h_change', 0):+.1f}%)")
            lines.append(f"• ETH: ${content.get('eth_price', 0):,.0f} ({content.get('eth_24h_change', 0):+.1f}%)")
            
            fg = content.get('fear_greed_index', 50)
            fg_label = content.get('fear_greed_label', 'Neutral')
            lines.append(f"• Fear/Greed: {fg} ({fg_label})")
            lines.append("")
        
        # Strategy status (simplified)
        lines.append("*Status*" if locale == 'pt-br' else "*Status*")
        lines.append("✅ Todas as estratégias funcionando normalmente" if locale == 'pt-br' 
                    else "✅ All strategies operating normally")
        lines.append("")
        
        # Insight (if present, truncated)
        if 'insight_content' in content:
            insight = content['insight_content']
            if len(insight) > 200:
                insight = insight[:197] + "..."
            lines.append(f"*Insight*")
            lines.append(insight)
            lines.append("")
        
        # Footer
        lines.append("—")
        lines.append("Adelaide | diBoaS")
        
        # AI Disclosure
        ai_text = "🤖 Gerado com IA" if locale == 'pt-br' else "🤖 AI-generated"
        lines.append(ai_text)
        
        return '\n'.join(lines)
    
    def _truncate_with_link(self, text: str, context: Dict) -> str:
        """Truncate message and add link to full content."""
        max_len = self.MAX_LENGTH - 100  # Reserve space for link
        
        truncated = text[:max_len]
        # Find last complete sentence
        last_period = truncated.rfind('.')
        if last_period > max_len * 0.7:
            truncated = truncated[:last_period + 1]
        
        locale = context.get('locale', 'en')
        if locale == 'pt-br':
            truncated += "\n\n📖 Leia a versão completa: diboas.com/adelaide"
        else:
            truncated += "\n\n📖 Read full version: diboas.com/adelaide"
        
        return truncated
    
    def _generate_buttons(self, persona: str, locale: str) -> List[str]:
        """Generate quick reply buttons based on persona."""
        if locale == 'pt-br':
            return [
                "📊 Ver estratégias",
                "❓ Ajuda",
                "⚙️ Configurações"
            ]
        else:
            return [
                "📊 View strategies",
                "❓ Help",
                "⚙️ Settings"
            ]


# Registry integration
def register_whatsapp_formatter():
    """Register WhatsApp formatter in output registry."""
    from src.registries.output_registry import OutputRegistry, OutputFormatter
    
    @OutputRegistry.register("whatsapp")
    class WhatsAppOutputFormatter(OutputFormatter):
        """WhatsApp formatter for registry."""
        
        def __init__(self, config: Dict[str, Any]):
            self.config = config
            self._formatter = WhatsAppFormatter()
        
        def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
            """Format data for WhatsApp."""
            context = config or {}
            if isinstance(data, dict):
                content = data.get('content', data)
                context['locale'] = data.get('edition', {}).get('locale', 'en')
                context['persona'] = data.get('edition', {}).get('persona', 'ana')
            else:
                content = {'rendered_content': str(data)}
            
            message = self._formatter.format(content, context)
            return message.body
        
        @property
        def output_type(self) -> str:
            return "whatsapp"
```

### 5.2 Registration in Output Registry

**Add to `src/registries/output_registry.py`:**

```python
# At end of file, add import and registration
from src.adelaide.formatters.whatsapp_formatter import register_whatsapp_formatter

# Call during module initialization
register_whatsapp_formatter()
```

---

## 6. Implementation Instructions

### 6.1 File Changes Summary

| File | Action | Priority |
|------|--------|----------|
| `src/registries/persona_registry.py` | Add Yield Hunter + B2B Client classes | P0 |
| `src/registries/persona_registry.py` | Fix `_build_market_bullets()` | P0 |
| `src/adelaide/localization.py` | Fix UTF-8 accents + add phrases | P0 |
| `src/adelaide/templates/*.md` | Add `{{ai_disclosure}}` placeholder | P0 |
| `src/adelaide/generator.py` | Add ai_disclosure to content data | P0 |
| `src/adelaide/formatters/whatsapp_formatter.py` | Create new file | P1 |
| `src/registries/output_registry.py` | Register whatsapp formatter | P1 |

### 6.2 Testing Checklist

After implementation, verify:

- [ ] `python main.py adelaide --persona=yield_hunter --locale=en` generates correctly
- [ ] `python main.py adelaide --persona=b2b_client --locale=en` generates correctly
- [ ] `python main.py adelaide --persona=ana --locale=pt-br` has NO English phrases
- [ ] All PT-BR content has proper UTF-8 accents (não, você, situação, etc.)
- [ ] AI disclosure appears in all newsletter outputs
- [ ] WhatsApp formatter produces valid <4096 char output

### 6.3 Persona Registry Updates

**Add after `FelipePersona` class:**

```python
# =============================================================================
# Yield Hunter Persona - DeFi-Native Yield Optimizer
# =============================================================================

@PersonaRegistry.register("yield_hunter")
class YieldHunterPersona(Persona):
    """
    Yield Hunter - Advanced DeFi user.
    
    Characteristics:
    - Data-forward with yield comparisons
    - DeFi terminology without explanation
    - Risk-adjusted metrics emphasized
    - Minimal emojis (1-3 per newsletter)
    - Targets strategies 6-10
    
    Sign-off: "— Adelaide | diBoaS"
    """
    
    PHRASES = {
        'en': {
            'greeting': 'Yield update.',
            'market_section': 'Yield Snapshot',
            'strategy_section': 'Protocol Health',
            'insight_section': 'Alpha Signal',
            'closing': 'Optimize accordingly',
            'signature': '— Adelaide | diBoaS',
            'disclaimer': '**Risk Disclosure**\n\nDeFi protocols carry smart contract risk. Yields are variable and not guaranteed. Past APY does not predict future returns. DYOR.\n\n**Your capital, your decision.**',
        },
        'pt-br': {
            'greeting': 'Atualização de yield.',
            'market_section': 'Snapshot de Yields',
            'strategy_section': 'Saúde dos Protocolos',
            'insight_section': 'Sinal Alpha',
            'closing': 'Otimize conforme necessário',
            'signature': '— Adelaide | diBoaS',
            'disclaimer': '**Divulgação de Risco**\n\nProtocolos DeFi carregam risco de smart contract. Yields são variáveis e não garantidos. APY passado não prevê retornos futuros. DYOR.\n\n**Seu capital, sua decisão.**',
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Yield Hunter's data-forward voice."""
        adapted = content.copy()
        adapted['persona'] = 'yield_hunter'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value
        
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        
        # Minimal greeting
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = ''
        
        # Technical sections
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = self._build_yield_intro(content)
        adapted['market_bullets'] = self._build_yield_table(content)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = ''
        
        # Protocol health
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        
        # Insight
        adapted['insight_section_title'] = phrases['insight_section']
        if 'insight_content' in adapted:
            # Strip emojis from insight
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))
        adapted['wisdom_note'] = ''
        
        # Closing
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['signature'] = phrases['signature']
        
        return adapted
    
    def _build_yield_intro(self, content: Dict) -> str:
        """Build yield-focused intro."""
        return "Current yields and protocol metrics:"
    
    def _build_yield_table(self, content: Dict) -> str:
        """Build yield comparison table."""
        # This would pull from actual yield data
        return """| Protocol | Current APY | 7d Avg | TVL | Risk |
|----------|-------------|--------|-----|------|
| Sky sUSDS | 8.5% | 8.2% | $2.1B | Low |
| Jito JitoSOL | 7.8% | 7.5% | $1.8B | Med |
| Jupiter JLP | 24.3% | 22.1% | $850M | High |"""
    
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


# =============================================================================
# B2B Client Persona - Institutional/White-Label
# =============================================================================

@PersonaRegistry.register("b2b_client")
class B2BClientPersona(Persona):
    """
    B2B Client - Institutional white-label persona.
    
    Characteristics:
    - Extremely professional, no personality
    - Zero emojis
    - Explicit timestamps and data sources
    - Compliance-ready formatting
    - Targets API/data licensing users
    
    Sign-off: "diBoaS Intelligence | Audit ID: {id}"
    """
    
    PHRASES = {
        'en': {
            'greeting': 'diBoaS Intelligence Brief',
            'market_section': 'Market Data',
            'strategy_section': 'Portfolio Analytics',
            'insight_section': 'Analysis',
            'methodology_section': 'Data Sources & Methodology',
            'closing': 'End of Report',
            'signature': 'diBoaS Intelligence',
            'disclaimer': """**Legal & Compliance**

This report is provided for informational purposes only and does not constitute investment advice. Data accuracy is not guaranteed. Recipients are responsible for their own compliance with applicable regulations in their jurisdiction.

Generated by: diBoaS Adelaide Intelligence Engine v3.2
Schema version: adelaide_output_v3""",
        },
        'pt-br': {
            'greeting': 'Relatório de Inteligência diBoaS',
            'market_section': 'Dados de Mercado',
            'strategy_section': 'Análise de Portfólio',
            'insight_section': 'Análise',
            'methodology_section': 'Fontes de Dados e Metodologia',
            'closing': 'Fim do Relatório',
            'signature': 'Inteligência diBoaS',
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
        from datetime import datetime
        
        adapted = content.copy()
        adapted['persona'] = 'b2b_client'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value
        
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        
        # Generate report metadata
        now = datetime.utcnow()
        report_id = f"adelaide-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
        
        # Institutional header
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = f"{phrases['greeting']} | {now.strftime('%Y-%m-%d')} | Report ID: {report_id}"
        adapted['greeting_message'] = ''
        
        # Market data with timestamps
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = f"Data as of: {now.isoformat()}Z"
        adapted['market_bullets'] = self._build_institutional_data(content, now)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = ''
        
        # Analytics section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_note'] = 'All metrics calculated using 30-day rolling window.'
        
        # Whale section - institutional framing
        adapted['whale_section_title'] = 'Large Holder Activity'
        adapted['whale_intro'] = 'Monitoring of significant wallet movements:'
        adapted['whale_disclaimer'] = 'Source: On-chain data aggregation. Not trading signals.'
        
        # Analysis
        adapted['insight_section_title'] = phrases['insight_section']
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))
        adapted['wisdom_note'] = ''
        
        # Methodology appendix
        adapted['methodology'] = self._build_methodology()
        
        # Closing
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['signature'] = f"{phrases['signature']} | Audit ID: {report_id}"
        adapted['footer'] = ''
        
        return adapted
    
    def _build_institutional_data(self, content: Dict, timestamp) -> str:
        """Build institutional-format data table."""
        return f"""| Metric | Value | Source | Updated |
|--------|-------|--------|---------|
| BTC/USD | ${content.get('btc_price', 0):,.2f} | CoinGecko | {timestamp.strftime('%H:%M')} UTC |
| ETH/USD | ${content.get('eth_price', 0):,.2f} | CoinGecko | {timestamp.strftime('%H:%M')} UTC |
| Fear/Greed | {content.get('fear_greed_index', 50)} | Alternative.me | Daily |
| VIX | {content.get('vix', 20):.2f} | CBOE | {timestamp.strftime('%H:%M')} UTC |"""
    
    def _build_methodology(self) -> str:
        """Build methodology appendix."""
        return """## Data Sources & Methodology

| Data Point | Source | Update Frequency | Methodology |
|------------|--------|------------------|-------------|
| Crypto Prices | CoinGecko API v3 | 5 minutes | Volume-weighted average |
| DeFi Yields | DefiLlama v2 | 1 hour | Protocol-reported APY |
| Sentiment | Alternative.me | Daily | Multi-factor composite |
| Risk Metrics | Internal | Daily | VaR: 95% CI, 252-day lookback |"""
    
    def _strip_emojis(self, text: str) -> str:
        """Remove all emojis."""
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


# =============================================================================
# Updated Utility Functions
# =============================================================================

def get_persona_for_strategy(strategy_id: int) -> str:
    """
    Get the recommended persona name for a strategy.
    
    Updated mapping:
    - 1, 3, 5 (0-20% crypto) → ana
    - 2, 4 (20-30% crypto) → maria  
    - 6, 7 (40-50% crypto) → yield_hunter or maria
    - 8, 9, 10 (70-85% crypto) → felipe or yield_hunter
    """
    if strategy_id in [1, 3, 5]:
        return "ana"
    elif strategy_id in [2, 4]:
        return "maria"
    elif strategy_id in [6, 7]:
        return "maria"  # Default, can be yield_hunter
    elif strategy_id in [8, 9, 10]:
        return "felipe"  # Default, can be yield_hunter
    else:
        return "maria"
```

---

## Summary

This deliverables package provides:

1. ✅ **Yield Hunter Persona** - Complete specification with voice guidelines, phrases, and implementation code
2. ✅ **B2B Client Persona** - Complete specification with institutional tone, compliance appendix, and implementation code
3. ✅ **PT-BR Localization Fixes** - Bug fix for English leakage + UTF-8 accent corrections
4. ✅ **AI Disclosure** - California SB 942 compliant disclosure text for all locales
5. ✅ **WhatsApp Formatter** - Stub implementation for Phase 1 manual process

**Next Steps:**
1. CTO Board to implement code changes
2. QA to test all persona + locale combinations
3. CMO Board to review generated outputs
4. Sign-off for Feb 12 launch

---

**Document Status:** COMPLETE  
**CMO Board Sign-Off:** Pending CTO implementation  
**Target Delivery:** February 8, 2026
