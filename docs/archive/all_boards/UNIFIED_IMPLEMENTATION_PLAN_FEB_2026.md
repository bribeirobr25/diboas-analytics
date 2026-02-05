# diBoaS Analytics v3 — Unified Implementation Plan

**Document:** UNIFIED_IMPLEMENTATION_PLAN_FEB_2026.md  
**Created:** February 4, 2026  
**Author:** All Boards Consolidation  
**Launch Date:** February 12, 2026  
**Status:** READY FOR CLAUDE CODE EXECUTION

---

## Executive Summary

This document consolidates all pending tasks, fixes, and implementations from all boards into a single execution plan for Claude Code. Items are organized by priority and include explicit file paths, code changes, and verification steps.

### Board Sources
- **CLO Board:** AI Disclosure Implementation Spec
- **CMO Board:** Session 010 Deliverables (Personas, Localization, WhatsApp)
- **QR Board:** Post-Launch Implementation Plan
- **Rakia Board:** Data Collection, Metadata, Freshness SLAs, TradFi Gaps
- **Strategy Board:** Data Handoff, Pending Tasks
- **Rakia Audit (Current Session):** Implementation verification findings

### Priority Summary

| Priority | Count | Pre-Launch? | Total Effort |
|----------|-------|-------------|--------------|
| 🔴 P0 Critical | 8 | YES | ~8 hours |
| 🟠 P1 High | 6 | YES | ~6 hours |
| 🟡 P2 Medium | 8 | NO | ~12-15 days |
| 🟢 P3 Low | 4 | NO | ~5 days |

**Pre-Launch Total:** ~14 hours (2 days intensive work)

---

## 🔴 P0 CRITICAL — MUST FIX BEFORE FEB 12 LAUNCH

### P0-1: AI Disclosure Implementation (CLO Board)

**Status:** ❌ NOT IMPLEMENTED — California SB 942 non-compliant (34 days overdue)  
**Effort:** 1.5 hours  
**Owner:** CTO Board

#### Task P0-1A: Update localization.py with AI Disclosure text

**File:** `src/adelaide/localization.py`

**Action:** Add AI_DISCLOSURES dict and method

```python
# Add at module level after TRANSLATIONS dict
AI_DISCLOSURES = {
    'en': '🤖 This content was generated with artificial intelligence assistance.',
    'pt-br': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
    'de': '🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.',
    'es': '🤖 Este contenido fue generado con asistencia de inteligencia artificial.',
}

# Add to LocalizationEngine class
def get_ai_disclosure(self, locale: str = None) -> str:
    """Get AI disclosure text for locale (California SB 942 compliance)."""
    locale = locale or self.default_locale
    return AI_DISCLOSURES.get(locale, AI_DISCLOSURES['en'])
```

#### Task P0-1B: Update REGIONAL_DISCLAIMERS with AI disclosure FIRST

**File:** `src/adelaide/localization.py`

**Action:** Prepend AI disclosure to all REGIONAL_DISCLAIMERS

```python
REGIONAL_DISCLAIMERS = {
    'en': """**AI Disclosure**

This content was created with the assistance of artificial intelligence. All data, analysis, and market commentary are reviewed for accuracy, but AI-generated content may contain errors. You are encouraged to verify important information independently.

---

**Important Disclosures**
[rest of existing EN disclaimer]""",

    'pt-br': """**Transparência sobre Inteligência Artificial**

Este conteúdo foi elaborado com o auxílio de inteligência artificial. Todas as informações, análises e comentários de mercado são revisados para garantir precisão, mas conteúdos gerados por IA podem conter imprecisões. Recomendamos que você verifique informações importantes de forma independente antes de tomar decisões.

---

**Avisos Importantes de Conformidade**

**AVISO 1 - PROTEÇÃO AO INVESTIDOR:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos ou fundos de compensação ao investidor.

**AVISO 2 - RISCO DE PERDA:** O valor dos seus investimentos pode diminuir ou aumentar. Você pode perder parte ou todo o capital investido.

**AVISO 3 - ORIENTAÇÃO PROFISSIONAL:** Considere consultar um assessor financeiro ou profissional habilitado pela CVM para orientação específica à sua situação.

Este conteúdo é apenas para fins educacionais e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.

Desempenho passado não é indicativo de resultados futuros.

**Direito de reclamação:** [contato@diboas.com]

*Você decide o que é melhor para sua situação.*"""
}
```

#### Task P0-1C: Add Gate 4 AI Disclosure Validation

**File:** `src/validators/gate4/clo_disclaimer_validator.py`

**Action:** Add AI disclosure validation rules

```python
# Add to REQUIRED_DISCLAIMERS
{
    "id": "US-AI-001",
    "pattern": "artificial intelligence",
    "alternatives": ["ai-generated", "ai-assisted", "created with ai"],
    "regulatory_ref": "California SB 942",
    "jurisdictions": ["US", "ALL"],
},
{
    "id": "BR-AI-001",
    "pattern": "inteligência artificial",
    "alternatives": ["auxílio de ia", "gerado por ia"],
    "regulatory_ref": "CDC Art. 6 (Transparency)",
    "jurisdictions": ["BR"],
},
```

#### Task P0-1D: Update Adelaide templates

**File:** `src/adelaide/templates/*.md` (all templates)

**Action:** Add `{{ai_disclosure}}` placeholder after signature, before footer

```markdown
{{signature}}

---

{{ai_disclosure}}

{{footer}}
```

#### Task P0-1E: Update generator to include ai_disclosure

**File:** `src/adelaide/generator.py`

**Action:** In `_prepare_content_data()`, add:

```python
# AI Disclosure (California SB 942 compliance)
data['ai_disclosure'] = self.localization.get_ai_disclosure(locale)
```

**Verification:**
```bash
python main.py adelaide --persona=ana --locale=en | grep -i "artificial intelligence"
# Should find AI disclosure text
```

---

### P0-2: Copy Missing Data Files (Strategy Board)

**Status:** ❌ 12 files missing — disables triggers  
**Effort:** 0.5 hours  
**Owner:** CTO Board

#### Task P0-2A: Copy wallet tracker files

**Action:** Copy from project to data directory

```bash
cp /mnt/project/estate_wallet_tracker.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/whale_wallet_master_list.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/market_maker_wallet_tracker.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/protocol_treasury_tracker.csv /Users/simonekugler/Desktop/diboas-analytics/data/
```

#### Task P0-2B: Copy institutional flow files

```bash
cp /mnt/project/btc_etf_holdings.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/corporate_btc_holdings.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/institutional_13f.csv /Users/simonekugler/Desktop/diboas-analytics/data/
```

#### Task P0-2C: Copy macro indicator files

```bash
cp /mnt/project/aaii_sentiment.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/credit_spreads.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/global_liquidity.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/treasury_yields.csv /Users/simonekugler/Desktop/diboas-analytics/data/
cp /mnt/project/real_yields.csv /Users/simonekugler/Desktop/diboas-analytics/data/
```

**Verification:**
```bash
ls -la /Users/simonekugler/Desktop/diboas-analytics/data/*.csv | wc -l
# Should be 20 files
```

---

### P0-3: Fix PT-BR Localization Bugs (CMO Board)

**Status:** ❌ English phrases leaking into PT-BR output  
**Effort:** 1 hour  
**Owner:** CTO Board

#### Task P0-3A: Fix _build_market_bullets() English leakage

**File:** `src/registries/persona_registry.py`

**Action:** Replace hardcoded English in AnaPersona._build_market_bullets()

**Find this code:**
```python
bullets.append("- Banks and big companies are lending money freely — a good sign! 💚")
```

**Replace with:**
```python
bullets.append("- " + phrases.get('credit_healthy', 'Banks and big companies are lending money freely — a good sign! 💚'))
```

#### Task P0-3B: Add missing PT-BR phrases to AnaPersona.PHRASES

**File:** `src/registries/persona_registry.py`

**Action:** Add to AnaPersona.PHRASES['pt-br'] dict:

```python
'pt-br': {
    # ... existing phrases ...
    
    # Credit health phrase (was hardcoded English)
    'credit_healthy': 'Bancos e grandes empresas estão emprestando dinheiro livremente — um bom sinal! 💚',
    
    # Market section header
    'market_bullets_header': "**Veja o que os números dizem:**",
    
    # Whale section (if missing)
    'whale_mtgox': 'Bitcoin',
    'whale_mtgox_status': 'Pagando credores lentamente',
    'whale_ftx': 'Várias criptomoedas',
    'whale_ftx_status': 'Tribunais cuidando da distribuição',
    
    # Table headers
    'table_who': 'Quem',
    'table_what': 'O Que Têm',
    'table_happening': 'O Que Está Acontecendo',
}
```

#### Task P0-3C: Fix UTF-8 accents in localization.py

**File:** `src/adelaide/localization.py`

**Action:** Search and replace all ASCII approximations with proper UTF-8:

| Find | Replace |
|------|---------|
| `nao` | `não` |
| `voce` | `você` |
| `situacao` | `situação` |
| `informacao` | `informação` |
| `protecao` | `proteção` |
| `atencao` | `atenção` |
| `acoes` | `ações` |
| `decisoes` | `decisões` |
| `opcoes` | `opções` |
| `indice` | `índice` |
| `financas` | `finanças` |
| `comeca` | `começa` |

**Verification:**
```bash
python main.py adelaide --persona=ana --locale=pt-br > /tmp/ptbr_test.md
grep -c "Banks and big" /tmp/ptbr_test.md  # Should be 0
grep -c "Bancos e grandes" /tmp/ptbr_test.md  # Should be 1
```

---

### P0-4: Add Depeg Time-Window (Rakia Audit Finding)

**Status:** ❌ Instantaneous depeg triggers — false alarm risk  
**Effort:** 1 hour  
**Owner:** CTO Board

#### Task P0-4A: Update triggers.yaml with time-window parameter

**File:** `config/triggers.yaml`

**Action:** Add `min_duration_seconds` to stablecoin depeg triggers:

```yaml
stablecoin_depeg:
  usdc:
    - level: L2
      threshold_pct: 1.0
      min_duration_seconds: 300  # 5 minutes sustained
      description: "USDC >1% from peg for 5+ minutes"
    - level: L3
      threshold_pct: 2.0
      min_duration_seconds: 300
      description: "USDC >2% from peg for 5+ minutes"
    - level: L4
      threshold_pct: 5.0
      min_duration_seconds: 60  # 1 minute for crisis
      description: "USDC >5% from peg"
  usdt:
    - level: L2
      threshold_pct: 1.0
      min_duration_seconds: 300
      description: "USDT >1% from peg for 5+ minutes"
    - level: L3
      threshold_pct: 2.0
      min_duration_seconds: 300
      description: "USDT >2% from peg for 5+ minutes"
    - level: L4
      threshold_pct: 5.0
      min_duration_seconds: 60
      description: "USDT >5% from peg"
```

#### Task P0-4B: Update stablecoin_depeg_triggers.py

**File:** `src/triggers/protocol/stablecoin_depeg_triggers.py`

**Action:** Add time-window checking logic:

```python
def check_depeg_with_duration(
    self,
    current_price: float,
    historical_prices: List[Tuple[datetime, float]],
    threshold_pct: float,
    min_duration_seconds: int = 300
) -> bool:
    """
    Check if depeg has been sustained for minimum duration.
    
    Args:
        current_price: Current stablecoin price
        historical_prices: List of (timestamp, price) tuples
        threshold_pct: Depeg threshold percentage
        min_duration_seconds: Minimum duration to sustain depeg
        
    Returns:
        True if depeg sustained for min_duration
    """
    if abs(1.0 - current_price) * 100 < threshold_pct:
        return False  # Not currently depegged
    
    # Check how long it's been depegged
    cutoff_time = datetime.utcnow() - timedelta(seconds=min_duration_seconds)
    
    for timestamp, price in reversed(historical_prices):
        if timestamp < cutoff_time:
            break
        if abs(1.0 - price) * 100 < threshold_pct:
            return False  # Recovered within window
    
    return True  # Sustained depeg
```

**Verification:**
```bash
python -c "from src.triggers.protocol.stablecoin_depeg_triggers import *; print('Time-window implemented')"
```

---

### P0-5: Fix Persona Name Mismatch (Rakia Audit Finding)

**Status:** ❌ strategies.json uses names not in persona_registry  
**Effort:** 0.5 hours  
**Owner:** CTO Board

#### Task P0-5A: Update strategies.json target_user fields

**File:** `config/strategies.json`

**Action:** Replace non-existent persona names:

| Find | Replace |
|------|---------|
| `"Camila"` | `"Maria"` |
| `"Mariana"` | `"Maria"` |
| `"Bruno"` | `"Felipe"` |

**Verification:**
```bash
grep -E '"target_user"' config/strategies.json | sort | uniq
# Should only show: ana, maria, felipe
```

---

### P0-6: Collection Metadata Tracking (Rakia Board)

**Status:** ❌ No audit trail for data collection  
**Effort:** 1 hour  
**Owner:** CTO Board

#### Task P0-6A: Create collection_metadata.py

**File:** `src/utils/collection_metadata.py` (NEW FILE)

**Action:** Copy code from Rakia Board spec `COLLECTION_METADATA_TRACKING_SPEC.md`

Full implementation provided in board artifact. Key class: `CollectionMetadataTracker`

#### Task P0-6B: Create storage directory

```bash
mkdir -p /Users/simonekugler/Desktop/diboas-analytics/storage
```

#### Task P0-6C: Integrate with collectors

**File:** `src/commands/collect.py`

**Action:** Add tracker calls at start/end of collection

```python
from src.utils.collection_metadata import get_tracker

def run_collect(args):
    tracker = get_tracker()
    mode = "incremental" if getattr(args, 'append', False) else "backfill"
    tracker.start_run(mode=mode, triggered_by="cli")
    
    try:
        # ... existing collection logic ...
        
        # After each file saved:
        tracker.record_file_update(
            filename="crypto_prices.csv",
            rows_added=rows_added,
            total_rows=len(df),
            source="yahoo_live",
            date_range={"start": str(df['date'].min()), "end": str(df['date'].max())}
        )
        
        tracker.end_run(status="success")
    except Exception as e:
        tracker.record_error(source="aggregator", message=str(e))
        tracker.end_run(status="failed")
        raise
```

**Verification:**
```bash
python main.py collect --source crypto --output data/
cat storage/collection_metadata.json | head -20
# Should show last_run metadata
```

---

### P0-7: Dual Freshness SLAs (Rakia Board)

**Status:** ❌ Single SLA doesn't support Pulse vs Weekly  
**Effort:** 1.5 hours  
**Owner:** CTO Board

#### Task P0-7A: Create freshness_slas.py

**File:** `config/freshness_slas.py` (NEW FILE)

**Action:** Copy from Rakia Board spec `DUAL_FRESHNESS_SLAS_SPEC.md`

```python
"""
Freshness SLA definitions for Adelaide editions.
"""

FRESHNESS_SLAS = {
    "pulse": {
        "crypto_prices.csv": 4,         # 4h SLA
        "sentiment_indicators.csv": 4,
        "tradfi_benchmark_data.csv": 4,
        "defillama_historical_apy.csv": 8,
        "jito_historical_apy.csv": 8,
        "jupiter_jlp_historical_apy.csv": 8,
        "treasury_yields.csv": 24,
        "real_yields.csv": 24,
        "credit_spreads.csv": 24,
        # ... rest from spec
    },
    "weekly": {
        "crypto_prices.csv": 24,
        # ... all 24h SLAs
    }
}

PULSE_CRITICAL_FILES = ["crypto_prices.csv", "sentiment_indicators.csv"]
WEEKLY_CRITICAL_FILES = ["crypto_prices.csv", "defillama_historical_apy.csv", "treasury_yields.csv"]

def get_sla(filename: str, edition: str = "weekly") -> int:
    return FRESHNESS_SLAS.get(edition, FRESHNESS_SLAS["weekly"]).get(filename, 24)

def get_critical_files(edition: str = "weekly") -> list:
    return PULSE_CRITICAL_FILES if edition == "pulse" else WEEKLY_CRITICAL_FILES
```

#### Task P0-7B: Update gate1_freshness_checker.py

**File:** `src/validators/gate1/gate1_freshness_checker.py`

**Action:** Update to support edition parameter

```python
class Gate1FreshnessChecker:
    def __init__(self, edition: str = "weekly"):
        self.edition = edition
    
    def check(self, file_path, max_age_hours=None, filename=None):
        if max_age_hours is None:
            from config.freshness_slas import get_sla
            max_age_hours = get_sla(filename or file_path.name, self.edition)
        # ... rest of check logic
```

#### Task P0-7C: Add --edition CLI argument

**File:** `src/commands/validate_gate1_cmd.py`

**Action:** Add edition argument to parser

```python
parser.add_argument(
    '--edition',
    choices=['pulse', 'weekly'],
    default='weekly',
    help='Adelaide edition for SLA selection'
)
```

**Verification:**
```bash
python main.py validate-gate1 --data data/ --edition pulse
python main.py validate-gate1 --data data/ --edition weekly
# Both should complete, pulse may have warnings if data >4h old
```

---

### P0-8: TradFi Gap Handling (Rakia Board)

**Status:** ⚠️ Unknown — needs verification and implementation  
**Effort:** 1 hour  
**Owner:** CTO Board

#### Task P0-8A: Add forward-fill to Battle Test

**File:** `src/engines/battle_test.py`

**Action:** Add TradFi gap handling

```python
def _prepare_tradfi_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Prepare TradFi data with weekend/holiday gap handling."""
    tradfi_columns = ['spy_close', 'qqq_close', 'dia_close', 'iwm_close', 'vix_close']
    
    # Forward-fill within max 4 days (handles long weekends)
    df[tradfi_columns] = df[tradfi_columns].fillna(method='ffill', limit=4)
    
    # Track filled rows for disclosure
    df['tradfi_forward_filled'] = df[tradfi_columns].isna().any(axis=1)
    
    return df
```

#### Task P0-8B: Add forward-fill to Monte Carlo

**File:** `src/engines/monte_carlo.py`

**Action:** Skip missing days for correlation, forward-fill for simulation

```python
def _calculate_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlation excluding TradFi gaps."""
    complete = df.dropna(subset=self.tradfi_columns)
    return complete[self.correlation_columns].corr()
```

#### Task P0-8C: Add forward-fill to Regime Classifier

**File:** `src/adelaide/regime_classifier.py`

**Action:** Return last known regime when TradFi missing

```python
def classify(self, data: Dict) -> Tuple[str, Dict]:
    spy_close = data.get('spy_close')
    
    if spy_close is None or pd.isna(spy_close):
        return self._get_last_known_regime(), {
            "disclosure": "Using last known regime due to TradFi gap",
            "gap_type": "weekend_or_holiday"
        }
    
    return self._classify_regime(data), {}
```

**Verification:**
```bash
# Run on weekend data
python main.py adelaide --date 2026-02-01  # Saturday
# Should generate without crash, with disclosure if using old data
```

---

## 🟠 P1 HIGH PRIORITY — PRE-LAUNCH

### P1-1: Add Yield Hunter Persona (CMO Board)

**Status:** ❌ Not implemented  
**Effort:** 1.5 hours  
**Owner:** CTO Board

#### Task P1-1A: Add YieldHunterPersona class

**File:** `src/registries/persona_registry.py`

**Action:** Copy full implementation from CMO Board `new_personas_implementation.py`

Key characteristics:
- Registry key: `yield_hunter`
- Emoji level: MINIMAL (1-3 per newsletter)
- DeFi terminology without explanation
- Data-forward with yield comparisons
- Sign-off: "— Adelaide | diBoaS"

**Verification:**
```bash
python main.py adelaide --persona=yield_hunter --locale=en
# Should generate yield-focused output
```

---

### P1-2: Add B2B Client Persona (CMO Board)

**Status:** ❌ Not implemented  
**Effort:** 1.5 hours  
**Owner:** CTO Board

#### Task P1-2A: Add B2BClientPersona class

**File:** `src/registries/persona_registry.py`

**Action:** Copy full implementation from CMO Board `new_personas_implementation.py`

Key characteristics:
- Registry key: `b2b_client`
- Emoji level: NONE
- ISO timestamps, explicit data sources
- Methodology appendix
- Audit ID in signature

**Verification:**
```bash
python main.py adelaide --persona=b2b_client --locale=en
# Should generate institutional-format output with audit ID
```

---

### P1-3: Add WhatsApp Formatter (CMO Board)

**Status:** ❌ Not implemented  
**Effort:** 1.5 hours  
**Owner:** CTO Board

#### Task P1-3A: Create whatsapp_formatter.py

**File:** `src/adelaide/formatters/whatsapp_formatter.py` (NEW FILE)

**Action:** Copy implementation from CMO Board deliverables

Key features:
- Max 4096 characters
- Convert markdown tables to lists
- Strip unsupported formatting
- Truncate with link if too long

#### Task P1-3B: Register in output_registry.py

**File:** `src/registries/output_registry.py`

**Action:** Add import and registration

```python
from src.adelaide.formatters.whatsapp_formatter import register_whatsapp_formatter
register_whatsapp_formatter()
```

**Verification:**
```bash
python main.py adelaide --persona=ana --locale=pt-br --format=whatsapp
# Should generate <4096 char plain text
```

---

### P1-4: Verify All Triggers Fire (Strategy Board)

**Status:** ⏳ Pending data files  
**Effort:** 1 hour  
**Owner:** Strategy Board + CTO Board
**Dependency:** P0-2 (data files copied)

#### Task P1-4A: Run full pipeline test

```bash
cd /Users/simonekugler/Desktop/diboas-analytics
python main.py collect --source all --output data/
python main.py validate-gate1 --data data/
python main.py monte-carlo --all
python main.py battle-test
python main.py adelaide --persona=ana --locale=en
```

#### Task P1-4B: Verify trigger categories

**Acceptance Criteria:**
- [ ] Protocol triggers: ≥1 fires
- [ ] Market triggers: ≥1 fires  
- [ ] Wallet triggers: ≥1 fires (after data files copied)
- [ ] Macro triggers: ≥1 fires (after data files copied)

---

### P1-5: Update Gate 1 Schema Definitions (Rakia Board)

**Status:** ⚠️ Needs verification for new files  
**Effort:** 0.5 hours  
**Owner:** CTO Board

#### Task P1-5A: Add schemas for new/missing files

**File:** `src/validators/gate1/gate1_schema_definitions.py`

**Action:** Add schemas for all 12 copied files

```python
# Add to SCHEMAS dict:
"estate_wallet_tracker.csv": {
    "columns": ["wallet_address", "entity", "chain", "last_known_balance_usd", "last_updated", "notes"],
    "required": ["wallet_address", "entity", "chain"],
    "min_rows": 1,
},
"treasury_yields.csv": {
    "columns": ["date", "us_2y", "us_5y", "us_10y", "us_30y"],
    "required": ["date", "us_10y"],
    "min_rows": 1000,
    "max_age_hours": 24,
},
# ... etc for all 12 files
```

---

### P1-6: Add Append-Only Collection Mode (Rakia Board)

**Status:** ⚠️ Needs verification  
**Effort:** 1 hour  
**Owner:** CTO Board

#### Task P1-6A: Add --append flag to CLI

**File:** `main.py` (argparse)

```python
parser.add_argument('--append', action='store_true', help='Incremental mode: only add new data')
```

#### Task P1-6B: Add get_last_date() to base collector

**File:** `src/collectors/base.py`

```python
def get_last_date(self, file_path: Path) -> Optional[date]:
    """Get last date in existing CSV."""
    if not file_path.exists():
        return None
    df = pd.read_csv(file_path)
    if df.empty or 'date' not in df.columns:
        return None
    df['date'] = pd.to_datetime(df['date'])
    return df['date'].max().date()
```

#### Task P1-6C: Update daily_run.sh

**File:** `scripts/daily_run.sh`

```bash
python main.py collect --source all --append --output data/
```

---

## 🟡 P2 MEDIUM PRIORITY — POST-LAUNCH (March 2026)

### P2-1: Sharpe Ratio Refinement (QR Board)
**Effort:** 1.5 days  
**Target:** March 1, 2026  
**File:** `src/domain/simulation.py`

Use proper annualization formula with configurable risk-free rate.

### P2-2: Sortino Ratio Implementation (QR Board)
**Effort:** 1 day  
**Target:** March 3, 2026  
**File:** `src/domain/simulation.py`

Add downside-only volatility calculation.

### P2-3: Antithetic Variates Monte Carlo (QR Board)
**Effort:** 1.5 days  
**Target:** March 6, 2026  
**File:** `src/engines/monte_carlo.py`

Implement variance reduction using paired simulations.

### P2-4: Protocol Failure Scenarios (QR Board)
**Effort:** 2 days  
**Target:** March 10, 2026  
**Files:** 
- `config/protocol_failures.yaml` (NEW)
- `src/engines/protocol_failure.py` (NEW)

Add protocol-specific tail risk scenarios to Monte Carlo.

### P2-5: Rebalancing Engine (Strategy Board)
**Effort:** 2 days  
**Target:** March 15, 2026  
**File:** `src/engines/rebalancing.py` (NEW)

Implement drift detection and rebalancing suggestions.

### P2-6: Impermanent Loss Calculator (QR Board)
**Effort:** 1 day  
**Target:** March 4, 2026  
**File:** `src/utils/impermanent_loss.py` (NEW)

Add IL calculation for JLP and AMM positions.

### P2-7: Regime-Conditional Correlations (QR Board)
**Effort:** 1.5 days  
**Target:** March 8, 2026  
**File:** `src/engines/monte_carlo.py`

Implement correlation matrices that vary by market regime.

### P2-8: CDaR Implementation (QR Board)
**Effort:** 1 day  
**Target:** March 5, 2026  
**File:** `src/domain/simulation.py`

Add Conditional Drawdown at Risk metric.

---

## 🟢 P3 LOW PRIORITY — Q2 2026

### P3-1: Per-Trigger Cooldown Configuration
**Target:** Q2 2026

Different cooldown periods per trigger type.

### P3-2: Cross-Strategy Correlation Detection
**Target:** Q2 2026

Detect when multiple strategies face correlated risks.

### P3-3: ES/DE Locale Support
**Target:** Q2 2026

Full localization for Spanish and German.

### P3-4: Telegram Formatter
**Target:** Q2 2026

Similar to WhatsApp formatter.

---

## 📅 PRE-LAUNCH EXECUTION TIMELINE

```
Feb 5 (Day 1):
├── Morning: P0-2 (Copy data files) - 0.5h
├── Morning: P0-5 (Fix persona names) - 0.5h
├── Afternoon: P0-1 (AI Disclosure) - 1.5h
├── Afternoon: P0-3 (PT-BR fixes) - 1h
└── Evening: Verification tests

Feb 6 (Day 2):
├── Morning: P0-4 (Depeg time-window) - 1h
├── Morning: P0-6 (Collection metadata) - 1h
├── Afternoon: P0-7 (Dual freshness SLAs) - 1.5h
├── Afternoon: P0-8 (TradFi gap handling) - 1h
└── Evening: Full pipeline test

Feb 7 (Day 3):
├── Morning: P1-1, P1-2 (New personas) - 3h
├── Afternoon: P1-3 (WhatsApp formatter) - 1.5h
├── Afternoon: P1-4 (Trigger verification) - 1h
└── Evening: Integration tests

Feb 8-11: Buffer for bug fixes and final testing

Feb 12: 🚀 LAUNCH
```

---

## ✅ VERIFICATION CHECKLIST

### Data Files
- [ ] 20 CSV files in data/ directory
- [ ] All schemas validated by Gate 1

### AI Disclosure (CLO)
- [ ] AI disclosure in EN newsletter
- [ ] AI disclosure in PT-BR newsletter
- [ ] Gate 4 validates AI disclosure presence

### Localization (CMO)
- [ ] Zero English phrases in PT-BR output
- [ ] All UTF-8 accents correct
- [ ] Yield Hunter persona generates
- [ ] B2B Client persona generates
- [ ] WhatsApp formatter produces <4096 chars

### Data Pipeline (Rakia)
- [ ] collection_metadata.json created after run
- [ ] --edition pulse flag works
- [ ] --edition weekly flag works
- [ ] TradFi gaps handled (no crashes on weekends)

### Triggers (Strategy)
- [ ] Protocol triggers fire
- [ ] Market triggers fire
- [ ] Wallet triggers fire
- [ ] Macro triggers fire

### Full Pipeline
- [ ] `python main.py collect --source all --output data/` completes
- [ ] `python main.py validate-gate1` passes
- [ ] `python main.py monte-carlo --all` completes
- [ ] `python main.py battle-test` completes
- [ ] `python main.py adelaide --persona=ana --locale=en` completes
- [ ] `python main.py adelaide --persona=ana --locale=pt-br` completes
- [ ] Validation report: 70/70 rules PASS

---

## 📋 QUESTIONS FOR BAR

Before implementation, please confirm:

1. **Weekend Adelaide:** Generate with disclosure using Friday data, or skip weekend editions?

2. **EU Day 1:** Is EU MiCA compliance needed for Feb 12 launch? (Currently only BR CVM implemented)

3. **Yield Hunter/B2B Client:** Are these Day 1 requirements or can they be P1 (ready but not in main rotation)?

4. **WhatsApp Manual vs API:** Confirmed manual copy-paste for Day 1, WhatsApp API integration post-launch?

---

*Document created by Rakia Board consolidating all board artifacts*  
*Ready for Claude Code execution upon CEO approval*
