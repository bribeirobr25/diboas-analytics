# CLAUDE CODE HANDOFF — CTO BOARD REVIEW

**Document:** CLAUDE_CODE_HANDOFF_CTO_REVIEW.md  
**Created:** February 4, 2026  
**Source:** CEO_APPROVED_IMPLEMENTATION_PLAN_v2.md  
**Status:** 🔄 PENDING CTO BOARD REVIEW  
**Purpose:** Executable task list for Claude Code implementation

---

## Overview

This document provides Claude Code with specific, executable tasks derived from the CEO-approved implementation plan. Each task includes exact file paths, code changes, and verification commands.

**Total Tasks:** 19 P0 + 5 P1 = 24 tasks  
**Estimated Effort:** 28-30 hours  
**Deadline:** February 12, 2026

---

## Pre-Implementation Setup

```bash
# Verify working directory
cd /Users/simonekugler/Desktop/diboas-analytics

# Create backup
cp -r config/ config_backup_$(date +%Y%m%d)/
cp -r src/ src_backup_$(date +%Y%m%d)/

# Verify current state
ls -la data/*.csv | wc -l  # Should be 8
python main.py --help       # Verify CLI works
```

---

## TASK 1: Copy Missing Data Files

**Priority:** P0-02  
**Effort:** 30 minutes  
**Blocking:** All triggers dependent on missing data

### Execute

```bash
# Create data directory if not exists
mkdir -p data/

# Copy wallet trackers (4 files)
cp /mnt/project/estate_wallet_tracker.csv data/
cp /mnt/project/whale_wallet_master_list.csv data/
cp /mnt/project/market_maker_wallet_tracker.csv data/
cp /mnt/project/protocol_treasury_tracker.csv data/

# Copy institutional flows (3 files)
cp /mnt/project/btc_etf_holdings.csv data/
cp /mnt/project/corporate_btc_holdings.csv data/
cp /mnt/project/institutional_13f.csv data/

# Copy macro indicators (5 files)
cp /mnt/project/aaii_sentiment.csv data/
cp /mnt/project/credit_spreads.csv data/
cp /mnt/project/global_liquidity.csv data/
cp /mnt/project/treasury_yields.csv data/
cp /mnt/project/real_yields.csv data/
```

### Verify

```bash
ls -la data/*.csv | wc -l
# Expected: 20

# Verify file contents are not empty
for f in data/*.csv; do
  echo "$f: $(wc -l < "$f") lines"
done
```

---

## TASK 2: Fix Persona Name Mismatch

**Priority:** P0-05  
**Effort:** 30 minutes  
**File:** `config/strategies.json` (or `strategies_v2_1.json`)

### Find and Replace

Search for these persona names and replace:

| Find | Replace With |
|------|--------------|
| `"target_user": "Camila"` | `"target_user": "maria"` |
| `"target_user": "Mariana"` | `"target_user": "maria"` |
| `"target_user": "Bruno"` | `"target_user": "felipe"` |
| `"target_user": "Per"` | `"target_user": "maria"` |

### Verify

```bash
grep -E '"target_user"' config/strategies*.json | sort | uniq
# Should only show: "ana", "maria", "felipe"
# No "Camila", "Mariana", "Bruno", "Per"
```

---

## TASK 3: AI Disclosure Implementation

**Priority:** P0-01  
**Effort:** 1.5 hours  
**Files:** 
- `src/adelaide/localization.py`
- `src/adelaide/generator.py`
- `src/validators/gate4/clo_disclaimer_validator.py`

### 3.1 Add AI Disclosure Dictionary

**File:** `src/adelaide/localization.py`

Add at module level:

```python
AI_DISCLOSURES = {
    'en': '🤖 This content was generated with artificial intelligence assistance.',
    'pt-br': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
    'de': '🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.',
    'es': '🤖 Este contenido fue generado con asistencia de inteligencia artificial.',
}
```

### 3.2 Integrate AI Disclosure into Output

**File:** `src/adelaide/generator.py`

In the content generation method, add AI disclosure after signature, before footer:

```python
def _prepare_content_data(self, locale: str, persona: str, ...) -> dict:
    # ... existing code ...
    
    from .localization import AI_DISCLOSURES
    data['ai_disclosure'] = AI_DISCLOSURES.get(locale, AI_DISCLOSURES['en'])
    
    return data
```

### 3.3 Add Gate 4 Validation

**File:** `src/validators/gate4/clo_disclaimer_validator.py`

Add validation rule:

```python
def validate_ai_disclosure(self, content: str, locale: str) -> ValidationResult:
    """Validate AI disclosure is present per California SB 942."""
    ai_keywords = {
        'en': 'artificial intelligence',
        'pt-br': 'inteligência artificial',
        'de': 'künstlicher Intelligenz',
        'es': 'inteligencia artificial',
    }
    
    keyword = ai_keywords.get(locale, ai_keywords['en'])
    if keyword.lower() not in content.lower():
        return ValidationResult(
            passed=False,
            error=f"AI disclosure missing for locale {locale}. Required: {keyword}"
        )
    return ValidationResult(passed=True)
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=en | grep -i "artificial intelligence"
python main.py adelaide --persona=ana --locale=pt-br | grep -i "inteligência artificial"
# Both should return matches
```

---

## TASK 4: Fix PT-BR Localization Bugs

**Priority:** P0-03  
**Effort:** 1 hour  
**File:** `src/registries/persona_registry.py`

### 4.1 Find English Leakage

Search for hardcoded English strings in PT-BR code paths:

```bash
grep -n "Banks and big companies" src/registries/persona_registry.py
grep -n "a good sign" src/registries/persona_registry.py
```

### 4.2 Fix with Locale-Aware Phrases

Replace hardcoded strings with phrase lookups:

```python
# BEFORE (hardcoded English):
bullets.append("- Banks and big companies are lending money freely — a good sign! 💚")

# AFTER (locale-aware):
bullets.append("- " + self.phrases.get('credit_healthy', 
    'Banks and big companies are lending money freely — a good sign! 💚'))
```

### 4.3 Add PT-BR Phrase

In `AnaPersona` class, add to `PHRASES['pt-br']`:

```python
'credit_healthy': 'Bancos e grandes empresas estão emprestando dinheiro livremente — um bom sinal! 💚',
'credit_tightening': 'Bancos estão mais cautelosos com empréstimos — fique atento! 🟡',
'credit_stress': 'Empresas estão tendo dificuldade para conseguir empréstimos — sinal de alerta! 🔴',
```

### 4.4 Fix UTF-8 Accents

Verify file encoding is UTF-8:

```bash
file src/registries/persona_registry.py
# Should show: UTF-8 Unicode text
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=pt-br > /tmp/ptbr_test.md
grep -c "Banks and big" /tmp/ptbr_test.md    # Should be 0
grep -c "Bancos e grandes" /tmp/ptbr_test.md  # Should be >= 1
```

---

## TASK 5: Add Depeg Time-Window

**Priority:** P0-04  
**Effort:** 1 hour  
**Files:**
- `config/triggers.yaml`
- `src/triggers/protocol/stablecoin_depeg_triggers.py`

### 5.1 Update Trigger Configuration

**File:** `config/triggers.yaml`

```yaml
stablecoin_depeg:
  usdc:
    - level: L2
      threshold_pct: 1.0
      min_duration_seconds: 300  # 5 minutes sustained
    - level: L3
      threshold_pct: 2.0
      min_duration_seconds: 300
    - level: L4
      threshold_pct: 5.0
      min_duration_seconds: 60   # 1 minute for crisis level
  usdt:
    - level: L2
      threshold_pct: 1.0
      min_duration_seconds: 300
    - level: L3
      threshold_pct: 2.0
      min_duration_seconds: 300
    - level: L4
      threshold_pct: 5.0
      min_duration_seconds: 60
```

### 5.2 Add Time-Window Check in Trigger Logic

**File:** `src/triggers/protocol/stablecoin_depeg_triggers.py`

```python
def check_depeg_sustained(
    self, 
    current_price: float, 
    price_history: List[Tuple[datetime, float]],
    threshold_pct: float,
    min_duration_seconds: int
) -> bool:
    """Check if depeg has been sustained for minimum duration."""
    if abs(1.0 - current_price) * 100 < threshold_pct:
        return False  # Not currently depegged
    
    # Find how long depeg has been sustained
    now = datetime.utcnow()
    sustained_start = None
    
    for timestamp, price in reversed(price_history):
        if abs(1.0 - price) * 100 >= threshold_pct:
            sustained_start = timestamp
        else:
            break
    
    if sustained_start is None:
        return False
    
    duration = (now - sustained_start).total_seconds()
    return duration >= min_duration_seconds
```

### Verify

```bash
python -c "
from src.triggers.protocol.stablecoin_depeg_triggers import StablecoinDepegTrigger
trigger = StablecoinDepegTrigger()
print('Config loaded:', hasattr(trigger, 'min_duration_seconds'))
"
```

---

## TASK 6: Collection Metadata Tracking

**Priority:** P0-06  
**Effort:** 1 hour  
**Files:**
- `src/utils/collection_metadata.py` (create)
- `src/collectors/*.py` (integrate)

### 6.1 Create Metadata Tracker

**File:** `src/utils/collection_metadata.py`

```python
"""Collection metadata tracking for audit trail."""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

METADATA_FILE = Path("data/collection_metadata.json")

class CollectionMetadataTracker:
    """Track collection runs for data provenance."""
    
    def __init__(self):
        self.metadata = self._load()
    
    def _load(self) -> Dict[str, Any]:
        if METADATA_FILE.exists():
            return json.loads(METADATA_FILE.read_text())
        return {"collections": {}}
    
    def _save(self):
        METADATA_FILE.write_text(json.dumps(self.metadata, indent=2, default=str))
    
    def record_collection(
        self,
        source: str,
        rows_added: int,
        api_status: str,
        errors: Optional[list] = None
    ):
        """Record a collection run."""
        self.metadata["collections"][source] = {
            "last_run": datetime.utcnow().isoformat(),
            "rows_added": rows_added,
            "api_status": api_status,
            "errors": errors or [],
        }
        self._save()
    
    def get_last_run(self, source: str) -> Optional[datetime]:
        """Get last successful run timestamp for a source."""
        if source in self.metadata["collections"]:
            return datetime.fromisoformat(
                self.metadata["collections"][source]["last_run"]
            )
        return None
```

### 6.2 Integrate with Collectors

In each collector, add at end of collection:

```python
from src.utils.collection_metadata import CollectionMetadataTracker

tracker = CollectionMetadataTracker()
tracker.record_collection(
    source="fred",
    rows_added=len(new_rows),
    api_status="success",
    errors=[]
)
```

### Verify

```bash
python main.py collect --source fred
cat data/collection_metadata.json | jq '.collections.fred'
```

---

## TASK 7: Dual Freshness SLAs Config

**Priority:** P0-07  
**Effort:** 1.5 hours  
**Files:**
- `config/freshness_slas.py` (create)
- `src/validators/gate1/gate1_freshness_checker.py` (modify)

### 7.1 Create SLA Configuration

**File:** `config/freshness_slas.py`

```python
"""Dual freshness SLA configuration for Pulse vs Weekly editions."""

from typing import Dict

# SLA in hours
FRESHNESS_SLAS: Dict[str, Dict[str, int]] = {
    "pulse": {
        # 4-hour SLA for fast-moving data
        "crypto_prices.csv": 4,
        "sentiment_indicators.csv": 4,
        "defillama_historical_apy.csv": 4,
        "jito_historical_apy.csv": 4,
        "jupiter_jlp_historical_apy.csv": 4,
    },
    "weekly": {
        # 24-hour SLA for comprehensive analysis
        "crypto_prices.csv": 24,
        "defillama_historical_apy.csv": 24,
        "treasury_yields.csv": 24,
        "tradfi_benchmark_data.csv": 24,
        "rotation_indicators.csv": 24,
        "commodities.csv": 24,
        "credit_spreads.csv": 24,
        "global_liquidity.csv": 24,
        "sentiment_indicators.csv": 24,
        "aaii_sentiment.csv": 168,  # Weekly data, 7 days OK
    },
}

def get_sla_hours(filename: str, edition: str = "weekly") -> int:
    """Get SLA hours for a file and edition type."""
    edition_slas = FRESHNESS_SLAS.get(edition, FRESHNESS_SLAS["weekly"])
    return edition_slas.get(filename, 24)  # Default 24h
```

### 7.2 Update Gate 1 Freshness Checker

**File:** `src/validators/gate1/gate1_freshness_checker.py`

Add edition parameter:

```python
from config.freshness_slas import get_sla_hours

def check_freshness(self, filename: str, edition: str = "weekly") -> ValidationResult:
    """Check if file meets freshness SLA for the given edition."""
    sla_hours = get_sla_hours(filename, edition)
    file_age_hours = self._get_file_age_hours(filename)
    
    if file_age_hours > sla_hours:
        return ValidationResult(
            passed=False,
            error=f"{filename} is {file_age_hours:.1f}h old, exceeds {edition} SLA of {sla_hours}h"
        )
    return ValidationResult(passed=True)
```

### Verify

```bash
python -c "
from config.freshness_slas import get_sla_hours
print('Pulse crypto_prices SLA:', get_sla_hours('crypto_prices.csv', 'pulse'), 'hours')
print('Weekly crypto_prices SLA:', get_sla_hours('crypto_prices.csv', 'weekly'), 'hours')
"
# Expected: 4 hours, 24 hours
```

---

## TASK 8: TradFi Gap Handling

**Priority:** P0-08  
**Effort:** 1 hour  
**File:** `src/utils/tradfi_gap_handler.py` (create)

### Create Gap Handler

```python
"""Handle TradFi data gaps (weekends, holidays)."""
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

US_MARKET_HOLIDAYS_2026 = [
    "2026-01-01",  # New Year's Day
    "2026-01-19",  # MLK Day
    "2026-02-16",  # Presidents Day
    "2026-04-03",  # Good Friday
    "2026-05-25",  # Memorial Day
    "2026-07-03",  # Independence Day (observed)
    "2026-09-07",  # Labor Day
    "2026-11-26",  # Thanksgiving
    "2026-12-25",  # Christmas
]

def is_tradfi_closed(date: Optional[datetime] = None) -> bool:
    """Check if TradFi markets are closed."""
    date = date or datetime.utcnow()
    
    # Weekend check
    if date.weekday() >= 5:  # Saturday=5, Sunday=6
        return True
    
    # Holiday check
    date_str = date.strftime("%Y-%m-%d")
    if date_str in US_MARKET_HOLIDAYS_2026:
        return True
    
    return False

def forward_fill_tradfi_data(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Forward-fill TradFi data for gaps."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df = df.asfreq('D').ffill()  # Daily frequency, forward fill
    df = df.reset_index()
    return df

def get_last_trading_day(from_date: Optional[datetime] = None) -> datetime:
    """Get the most recent trading day."""
    date = from_date or datetime.utcnow()
    while is_tradfi_closed(date):
        date -= timedelta(days=1)
    return date
```

### Verify

```bash
python -c "
from src.utils.tradfi_gap_handler import is_tradfi_closed, get_last_trading_day
from datetime import datetime

# Test weekend
saturday = datetime(2026, 2, 7)  # Saturday
print('Saturday closed:', is_tradfi_closed(saturday))  # True

# Test trading day
friday = datetime(2026, 2, 6)  # Friday
print('Friday closed:', is_tradfi_closed(friday))  # False

print('Last trading day from Saturday:', get_last_trading_day(saturday))
"
```

---

## TASK 9: Yield Hunter Persona

**Priority:** P0-09  
**Effort:** 1.5 hours  
**File:** `src/registries/persona_registry.py`

### Add Yield Hunter Persona Class

```python
class YieldHunterPersona(BasePersona):
    """DeFi-native yield optimizer persona."""
    
    PERSONA_KEY = "yield_hunter"
    EMOJI_LEVEL = "minimal"  # 1-3 per newsletter max
    
    PHRASES = {
        'en': {
            'greeting': 'Yield update',
            'sign_off': '— Adelaide | diBoaS',
            'market_snapshot': 'Market Snapshot',
            'defi_yields': 'DeFi Yields',
            'risk_adjusted': 'Risk-Adjusted View',
            'protocol_health': 'Protocol Health',
            'action_items': 'Opportunities',
        },
        'pt-br': {
            'greeting': 'Atualização de rendimento',
            'sign_off': '— Adelaide | diBoaS',
            'market_snapshot': 'Snapshot do Mercado',
            'defi_yields': 'Rendimentos DeFi',
            'risk_adjusted': 'Visão Ajustada ao Risco',
            'protocol_health': 'Saúde dos Protocolos',
            'action_items': 'Oportunidades',
        },
        'de': {
            'greeting': 'Rendite-Update',
            'sign_off': '— Adelaide | diBoaS',
            # ... German phrases
        },
        'es': {
            'greeting': 'Actualización de rendimiento',
            'sign_off': '— Adelaide | diBoaS',
            # ... Spanish phrases
        },
    }
    
    TONE_GUIDELINES = """
    - DeFi-native terminology (no explanations needed)
    - Data-forward, minimal prose
    - APY/TVL/IL terminology assumed understood
    - Minimal emojis (1-3 max, only for emphasis)
    - Direct and concise
    - Skip basic crypto explanations
    """
    
    def format_greeting(self, locale: str) -> str:
        return self.phrases.get('greeting', 'Yield update')
    
    def get_emoji_budget(self) -> int:
        return 3  # Maximum 3 emojis per newsletter
```

### Register in Persona Registry

```python
PERSONA_REGISTRY = {
    'ana': AnaPersona,
    'maria': MariaPersona,
    'felipe': FelipePersona,
    'yield_hunter': YieldHunterPersona,
    'b2b_client': B2BClientPersona,  # Added in Task 10
}
```

### Verify

```bash
python main.py adelaide --persona=yield_hunter --locale=en
# Should generate without error
```

---

## TASK 10: B2B Client Persona

**Priority:** P0-10  
**Effort:** 1.5 hours  
**File:** `src/registries/persona_registry.py`

### Add B2B Client Persona Class

```python
class B2BClientPersona(BasePersona):
    """Institutional white-label persona."""
    
    PERSONA_KEY = "b2b_client"
    EMOJI_LEVEL = "none"  # Zero emojis
    
    PHRASES = {
        'en': {
            'greeting': 'Market Intelligence Report',
            'sign_off': 'Report ID: {audit_id}',
            'market_snapshot': 'Executive Summary',
            'defi_yields': 'DeFi Protocol Analysis',
            'risk_adjusted': 'Risk Metrics',
            'protocol_health': 'Protocol Status',
            'action_items': 'Recommended Actions',
            'data_sources': 'Data Sources',
            'timestamp': 'Report Generated',
        },
        'pt-br': {
            'greeting': 'Relatório de Inteligência de Mercado',
            'sign_off': 'ID do Relatório: {audit_id}',
            # ... PT-BR phrases
        },
        'de': {
            'greeting': 'Marktintelligenz-Bericht',
            'sign_off': 'Bericht-ID: {audit_id}',
            # ... German phrases
        },
        'es': {
            'greeting': 'Informe de Inteligencia de Mercado',
            'sign_off': 'ID del Informe: {audit_id}',
            # ... Spanish phrases
        },
    }
    
    TONE_GUIDELINES = """
    - Zero emojis (institutional tone)
    - ISO timestamps (YYYY-MM-DDTHH:MM:SSZ)
    - Explicit data source attribution
    - Audit-ready formatting
    - Include confidence intervals
    - Formal, professional language
    - Include report/audit ID
    """
    
    def format_greeting(self, locale: str) -> str:
        return self.phrases.get('greeting', 'Market Intelligence Report')
    
    def get_emoji_budget(self) -> int:
        return 0  # Zero emojis
    
    def format_sign_off(self, locale: str, audit_id: str = None) -> str:
        audit_id = audit_id or self._generate_audit_id()
        template = self.phrases.get('sign_off', 'Report ID: {audit_id}')
        return template.format(audit_id=audit_id)
    
    def _generate_audit_id(self) -> str:
        from datetime import datetime
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        return f"ADELAIDE-{hashlib.sha256(timestamp.encode()).hexdigest()[:8].upper()}"
```

### Verify

```bash
python main.py adelaide --persona=b2b_client --locale=en
# Should generate without emojis
# Should include Report ID
```

---

## TASK 11: DE Locale (German)

**Priority:** P0-11  
**Effort:** 1.5 hours  
**File:** `src/adelaide/localization.py`

### Add German Translations

```python
TRANSLATIONS = {
    # ... existing en, pt-br ...
    
    'de': {
        # Greetings
        'good_morning': 'Guten Morgen',
        'good_afternoon': 'Guten Tag',
        'good_evening': 'Guten Abend',
        'dear': 'Liebe(r)',
        
        # Sections
        'market_snapshot': 'Marktüberblick',
        'fear_greed_index': 'Angst-und-Gier-Index',
        'btc_dominance': 'BTC-Dominanz',
        'total_crypto_market': 'Gesamter Kryptomarkt',
        'defi_yields': 'DeFi-Renditen',
        'protocol_health': 'Protokoll-Status',
        'risk_assessment': 'Risikobewertung',
        'recommended_actions': 'Empfohlene Maßnahmen',
        
        # Risk levels
        'risk_low': 'Niedriges Risiko',
        'risk_medium': 'Mittleres Risiko',
        'risk_high': 'Hohes Risiko',
        
        # Actions
        'hold': 'Halten',
        'accumulate': 'Akkumulieren',
        'reduce': 'Reduzieren',
        'exit': 'Aussteigen',
        
        # Disclaimers
        'ai_disclosure': '🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.',
        'not_financial_advice': 'Dies ist keine Finanzberatung.',
        'mica_disclaimer': 'Gemäß EU-Verordnung 2023/1114 (MiCA): Krypto-Assets sind nicht reguliert und können hochriskant sein.',
    },
}
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=de
# Should generate in German
grep -c "Marktüberblick" output_de.md  # Should be >= 1
```

---

## TASK 12: ES Locale (Spanish)

**Priority:** P0-12  
**Effort:** 1.5 hours  
**File:** `src/adelaide/localization.py`

### Add Spanish Translations

```python
TRANSLATIONS = {
    # ... existing en, pt-br, de ...
    
    'es': {
        # Greetings
        'good_morning': 'Buenos días',
        'good_afternoon': 'Buenas tardes',
        'good_evening': 'Buenas noches',
        'dear': 'Querido/a',
        
        # Sections
        'market_snapshot': 'Panorama del Mercado',
        'fear_greed_index': 'Índice de Miedo y Codicia',
        'btc_dominance': 'Dominancia de BTC',
        'total_crypto_market': 'Mercado Cripto Total',
        'defi_yields': 'Rendimientos DeFi',
        'protocol_health': 'Estado del Protocolo',
        'risk_assessment': 'Evaluación de Riesgo',
        'recommended_actions': 'Acciones Recomendadas',
        
        # Risk levels
        'risk_low': 'Riesgo Bajo',
        'risk_medium': 'Riesgo Medio',
        'risk_high': 'Riesgo Alto',
        
        # Actions
        'hold': 'Mantener',
        'accumulate': 'Acumular',
        'reduce': 'Reducir',
        'exit': 'Salir',
        
        # Disclaimers
        'ai_disclosure': '🤖 Este contenido fue generado con asistencia de inteligencia artificial.',
        'not_financial_advice': 'Esto no es asesoramiento financiero.',
        'mica_disclaimer': 'Según el Reglamento UE 2023/1114 (MiCA): Los criptoactivos no están regulados y pueden ser de alto riesgo.',
    },
}
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=es
# Should generate in Spanish
grep -c "Panorama del Mercado" output_es.md  # Should be >= 1
```

---

## TASK 13: WhatsApp Formatter

**Priority:** P0-13  
**Effort:** 1.5 hours  
**File:** `src/adelaide/formatters/whatsapp_formatter.py` (create)

### Create WhatsApp Formatter

```python
"""WhatsApp message formatter for Adelaide output."""
import re
from typing import Optional

MAX_WHATSAPP_LENGTH = 4096

class WhatsAppFormatter:
    """Format Adelaide content for WhatsApp."""
    
    def format(self, content: str, website_url: str) -> str:
        """Convert Adelaide markdown to WhatsApp format."""
        # Convert markdown to WhatsApp format
        formatted = self._convert_markdown(content)
        
        # Truncate if needed
        if len(formatted) > MAX_WHATSAPP_LENGTH:
            formatted = self._truncate_with_link(formatted, website_url)
        
        return formatted
    
    def _convert_markdown(self, content: str) -> str:
        """Convert markdown to WhatsApp-compatible format."""
        result = content
        
        # Headers to bold
        result = re.sub(r'^#{1,6}\s+(.+)$', r'*\1*', result, flags=re.MULTILINE)
        
        # Bold: **text** or __text__ → *text*
        result = re.sub(r'\*\*(.+?)\*\*', r'*\1*', result)
        result = re.sub(r'__(.+?)__', r'*\1*', result)
        
        # Italic: *text* or _text_ → _text_ (keep as is)
        # Note: WhatsApp uses _ for italic
        
        # Tables → lists
        result = self._convert_tables_to_lists(result)
        
        # Remove markdown links, keep URL only
        result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\2', result)
        
        # Remove images
        result = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', result)
        
        return result.strip()
    
    def _convert_tables_to_lists(self, content: str) -> str:
        """Convert markdown tables to bullet lists."""
        lines = content.split('\n')
        result = []
        in_table = False
        headers = []
        
        for line in lines:
            if '|' in line and not line.strip().startswith('```'):
                if '---' in line:
                    continue  # Skip separator
                
                cells = [c.strip() for c in line.split('|') if c.strip()]
                
                if not in_table:
                    headers = cells
                    in_table = True
                else:
                    # Data row: format as "• header1: value1, header2: value2"
                    pairs = [f"{headers[i]}: {cells[i]}" for i in range(min(len(headers), len(cells)))]
                    result.append('• ' + ', '.join(pairs))
            else:
                if in_table:
                    in_table = False
                    headers = []
                result.append(line)
        
        return '\n'.join(result)
    
    def _truncate_with_link(self, content: str, url: str) -> str:
        """Truncate content and add link to full version."""
        suffix = f"\n\n📖 Leia a versão completa: {url}"
        max_content = MAX_WHATSAPP_LENGTH - len(suffix) - 10
        
        # Find good break point
        truncated = content[:max_content]
        last_newline = truncated.rfind('\n\n')
        if last_newline > max_content * 0.7:
            truncated = truncated[:last_newline]
        
        return truncated + "..." + suffix
```

### Register Formatter

**File:** `src/registries/output_registry.py`

```python
from src.adelaide.formatters.whatsapp_formatter import WhatsAppFormatter

OUTPUT_FORMATTERS = {
    # ... existing ...
    'whatsapp': WhatsAppFormatter(),
}
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=pt-br --format=whatsapp | wc -c
# Should be < 4096
```

---

## TASK 14: Telegram Formatter

**Priority:** P0-14  
**Effort:** 1.5 hours  
**File:** `src/adelaide/formatters/telegram_formatter.py` (create)

### Create Telegram Formatter

```python
"""Telegram message formatter for Adelaide output."""
import re

MAX_TELEGRAM_LENGTH = 4096

class TelegramFormatter:
    """Format Adelaide content for Telegram."""
    
    def format(self, content: str, website_url: str) -> str:
        """Convert Adelaide markdown to Telegram format."""
        formatted = self._convert_markdown(content)
        
        if len(formatted) > MAX_TELEGRAM_LENGTH:
            formatted = self._truncate_with_link(formatted, website_url)
        
        return formatted
    
    def _convert_markdown(self, content: str) -> str:
        """Convert markdown to Telegram-compatible format."""
        result = content
        
        # Headers to bold
        result = re.sub(r'^#{1,6}\s+(.+)$', r'*\1*', result, flags=re.MULTILINE)
        
        # Keep **bold** as *bold*
        result = re.sub(r'\*\*(.+?)\*\*', r'*\1*', result)
        
        # Keep _italic_ as _italic_
        
        # Links: [text](url) stays as is (Telegram supports this)
        
        # Remove tables (Telegram doesn't render well)
        result = self._remove_tables(result)
        
        # Remove images
        result = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', result)
        
        return result.strip()
    
    def _remove_tables(self, content: str) -> str:
        """Remove markdown tables, keep data as text."""
        lines = content.split('\n')
        result = []
        skip_table = False
        
        for line in lines:
            if '|' in line and '---' not in line:
                if not skip_table:
                    skip_table = True
                    result.append('_(Veja tabela completa no site)_')
            elif '---' in line and '|' in line:
                continue  # Skip table separator
            else:
                skip_table = False
                result.append(line)
        
        return '\n'.join(result)
    
    def _truncate_with_link(self, content: str, url: str) -> str:
        """Truncate and add link."""
        suffix = f"\n\n📖 [Leia mais]({url})"
        max_content = MAX_TELEGRAM_LENGTH - len(suffix) - 10
        
        truncated = content[:max_content]
        last_break = truncated.rfind('\n\n')
        if last_break > max_content * 0.7:
            truncated = truncated[:last_break]
        
        return truncated + "..." + suffix
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=en --format=telegram | wc -c
# Should be < 4096
```

---

## TASK 15: X/Twitter Formatter

**Priority:** P0-15  
**Effort:** 1 hour  
**File:** `src/adelaide/formatters/twitter_formatter.py` (create)

### Create Twitter Formatter

```python
"""Twitter/X formatter for Adelaide output."""

MAX_TWEET_LENGTH = 280

class TwitterFormatter:
    """Format Adelaide content for Twitter/X."""
    
    def format(self, content: str, website_url: str, locale: str = 'en') -> str:
        """Create tweet-sized teaser from Adelaide content."""
        # Extract key insight
        insight = self._extract_key_insight(content, locale)
        
        # Calculate available space for content
        url_length = 23  # Twitter shortens all URLs to ~23 chars
        available = MAX_TWEET_LENGTH - url_length - 2  # -2 for newlines
        
        # Truncate insight if needed
        if len(insight) > available:
            insight = insight[:available - 3] + "..."
        
        return f"{insight}\n\n{website_url}"
    
    def _extract_key_insight(self, content: str, locale: str) -> str:
        """Extract the most important insight for tweet."""
        # Look for market snapshot section
        lines = content.split('\n')
        
        # Find first substantive paragraph after greeting
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 50:
                # Found a content line
                # Clean it up for tweet
                clean = line.replace('**', '').replace('*', '')
                clean = clean.replace('_', '')
                
                # Add locale-specific hook
                hooks = {
                    'en': '📊 Adelaide Daily: ',
                    'pt-br': '📊 Adelaide Diária: ',
                    'de': '📊 Adelaide Täglich: ',
                    'es': '📊 Adelaide Diario: ',
                }
                
                hook = hooks.get(locale, hooks['en'])
                return hook + clean
        
        # Fallback
        return f"📊 Today's market analysis is ready."
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=en --format=twitter | wc -c
# Should be < 280
```

---

## TASK 16: LinkedIn Formatter

**Priority:** P0-16  
**Effort:** 1 hour  
**File:** `src/adelaide/formatters/linkedin_formatter.py` (create)

### Create LinkedIn Formatter

```python
"""LinkedIn formatter for Adelaide output (B2B focused)."""
import re

MAX_LINKEDIN_LENGTH = 3000

class LinkedInFormatter:
    """Format Adelaide content for LinkedIn."""
    
    def format(self, content: str, website_url: str) -> str:
        """Convert Adelaide content to LinkedIn format."""
        # For B2B: Keep professional, remove emojis if too many
        formatted = self._convert_to_linkedin(content)
        
        if len(formatted) > MAX_LINKEDIN_LENGTH:
            formatted = self._truncate_with_link(formatted, website_url)
        
        return formatted
    
    def _convert_to_linkedin(self, content: str) -> str:
        """Convert to LinkedIn-friendly format."""
        result = content
        
        # Remove markdown formatting (LinkedIn doesn't support it)
        result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)  # Remove bold
        result = re.sub(r'__(.+?)__', r'\1', result)
        result = re.sub(r'\*(.+?)\*', r'\1', result)  # Remove italic
        result = re.sub(r'_(.+?)_', r'\1', result)
        
        # Remove headers markers
        result = re.sub(r'^#{1,6}\s+', '', result, flags=re.MULTILINE)
        
        # Convert links to plain text with URL
        result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', result)
        
        # Remove images
        result = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', result)
        
        # Clean up extra whitespace
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result.strip()
    
    def _truncate_with_link(self, content: str, url: str) -> str:
        """Truncate and add link."""
        suffix = f"\n\n🔗 Read full analysis: {url}"
        max_content = MAX_LINKEDIN_LENGTH - len(suffix) - 10
        
        truncated = content[:max_content]
        last_break = truncated.rfind('\n\n')
        if last_break > max_content * 0.7:
            truncated = truncated[:last_break]
        
        return truncated + "..." + suffix
```

### Verify

```bash
python main.py adelaide --persona=b2b_client --locale=en --format=linkedin | wc -c
# Should be < 3000
```

---

## TASK 17: Substack Formatter

**Priority:** P0-17  
**Effort:** 1 hour  
**File:** `src/adelaide/formatters/substack_formatter.py` (create)

### Create Substack Formatter

```python
"""Substack newsletter formatter for Adelaide output."""

class SubstackFormatter:
    """Format Adelaide content for Substack email newsletter."""
    
    def format(self, content: str, website_url: str = None) -> str:
        """Convert Adelaide content to Substack-optimized format."""
        # Substack supports full markdown, but email clients vary
        formatted = self._optimize_for_email(content)
        
        # Add unsubscribe footer (Substack adds automatically, but good to have)
        footer = self._get_footer()
        
        return formatted + footer
    
    def _optimize_for_email(self, content: str) -> str:
        """Optimize content for email rendering."""
        result = content
        
        # Ensure images have alt text
        # (Substack handles images, but alt text helps accessibility)
        
        # Convert complex tables to simpler format
        # (Some email clients don't render markdown tables)
        
        # Add horizontal rules between major sections
        result = result.replace('\n## ', '\n---\n\n## ')
        
        return result
    
    def _get_footer(self) -> str:
        """Get standard Substack footer."""
        return """

---

📧 *Você está recebendo este email porque se inscreveu na Adelaide by diBoaS.*

🤖 Este conteúdo foi gerado com assistência de inteligência artificial.

⚠️ Isto não é aconselhamento financeiro. Faça sua própria pesquisa.
"""
```

### Verify

```bash
python main.py adelaide --persona=ana --locale=pt-br --format=substack
# Should generate full newsletter with footer
```

---

## TASK 18: FRED Error Fix

**Priority:** P0-18  
**Effort:** 1-2 hours  
**Files:** `src/collectors/fred_collector.py`

### Investigation Steps

1. **Run FRED collector and capture error:**
```bash
python main.py collect --source fred 2>&1 | tee fred_error.log
```

2. **Common type error patterns to look for:**
```python
# Issue: NaN or None values not handled
value = float(row.value)  # Fails if None

# Fix:
value = float(row.value) if row.value is not None else None
```

3. **Check for date parsing issues:**
```python
# Issue: String date not parsed
date = row.date  # String

# Fix:
from datetime import datetime
date = datetime.strptime(row.date, "%Y-%m-%d")
```

4. **Fix and verify:**
```bash
python main.py collect --source fred
cat data/fred_*.csv | head -20  # Should have data
```

### Verification

```bash
# Collect FRED data
python main.py collect --source fred

# Verify files created
ls -la data/treasury_yields.csv
ls -la data/real_yields.csv
ls -la data/credit_spreads.csv

# Verify data quality
python -c "
import pandas as pd
df = pd.read_csv('data/treasury_yields.csv')
print('Rows:', len(df))
print('Columns:', df.columns.tolist())
print('Sample:', df.head())
"
```

---

## TASK 19: Weekend Adelaide Support

**Priority:** P0-19  
**Effort:** 1 hour  
**File:** `src/adelaide/generator.py`

### Add Weekend Detection and Disclosure

```python
from datetime import datetime
from src.utils.tradfi_gap_handler import is_tradfi_closed, get_last_trading_day

WEEKEND_DISCLOSURES = {
    'en': '📅 Note: US stock markets were closed. TradFi data reflects the last trading day.',
    'pt-br': '📅 Nota: Os mercados de ações dos EUA estavam fechados. Dados TradFi refletem o último dia de negociação.',
    'de': '📅 Hinweis: Die US-Aktienmärkte waren geschlossen. TradFi-Daten spiegeln den letzten Handelstag wider.',
    'es': '📅 Nota: Los mercados bursátiles de EE.UU. estaban cerrados. Los datos TradFi reflejan el último día de negociación.',
}

class AdelaideGenerator:
    # ... existing code ...
    
    def _is_tradfi_closed(self) -> bool:
        """Check if TradFi markets are closed (weekend/holiday)."""
        return is_tradfi_closed()
    
    def _prepare_content_data(self, locale: str, persona: str, ...) -> dict:
        # ... existing code ...
        
        # Add weekend disclosure if applicable
        if self._is_tradfi_closed():
            data['weekend_disclosure'] = WEEKEND_DISCLOSURES.get(
                locale, WEEKEND_DISCLOSURES['en']
            )
            data['tradfi_data_date'] = get_last_trading_day().strftime("%Y-%m-%d")
        else:
            data['weekend_disclosure'] = None
            data['tradfi_data_date'] = datetime.utcnow().strftime("%Y-%m-%d")
        
        return data
```

### Update Template

Add to Adelaide template:

```markdown
{{#if weekend_disclosure}}
{{{weekend_disclosure}}}

{{/if}}
```

### Verify

```bash
# Run on a weekend (or mock)
python -c "
from datetime import datetime
# Simulate weekend
from unittest.mock import patch
with patch('src.adelaide.generator.datetime') as mock_dt:
    mock_dt.utcnow.return_value = datetime(2026, 2, 7)  # Saturday
    from src.adelaide.generator import AdelaideGenerator
    gen = AdelaideGenerator()
    print('Is weekend:', gen._is_tradfi_closed())
"
```

---

## Execution Checklist

### Day 1 (Feb 5)

- [ ] TASK 1: Copy data files
- [ ] TASK 2: Fix persona names
- [ ] TASK 18: FRED error investigation
- [ ] TASK 3: AI Disclosure

### Day 2 (Feb 6)

- [ ] TASK 4: PT-BR localization fixes
- [ ] TASK 5: Depeg time-window
- [ ] TASK 6: Collection metadata
- [ ] TASK 7: Dual freshness SLAs
- [ ] TASK 8: TradFi gap handling
- [ ] TASK 19: Weekend Adelaide

### Day 3 (Feb 7)

- [ ] TASK 9: Yield Hunter persona
- [ ] TASK 10: B2B Client persona
- [ ] TASK 11: DE locale
- [ ] TASK 12: ES locale

### Day 4 (Feb 8)

- [ ] TASK 13: WhatsApp formatter
- [ ] TASK 14: Telegram formatter
- [ ] TASK 15: Twitter formatter
- [ ] TASK 16: LinkedIn formatter
- [ ] TASK 17: Substack formatter

### Day 5-6 (Feb 9-10)

- [ ] P1 tasks (triggers, schemas, append mode)
- [ ] Integration testing
- [ ] Full 52-output generation test
- [ ] Bug fixes

### Day 7 (Feb 11)

- [ ] Final verification
- [ ] Sample outputs for all combinations
- [ ] Launch prep

### Launch (Feb 12)

- [ ] 🚀 GO LIVE

---

## Final Verification Command

```bash
# Generate all 52 outputs
./scripts/generate_all_adelaide.sh

# Verify counts
find outputs/ -name "*.md" -o -name "*.txt" | wc -l
# Expected: 52

# Verify compliance
python main.py validate-gate4 --all-outputs
# Expected: PASS
```

---

**Document End**

*Claude Code Handoff — CTO Board Review*  
*February 4, 2026*
