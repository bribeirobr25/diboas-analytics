# Claude Code Implementation Handoff
## diBoaS Analytics v3 — February 12, 2026 Launch

**Document Version:** 2.0  
**Date:** February 3, 2026  
**Target:** Public launch, Brazil Day 1  
**Available Dev Days:** 9 (Feb 3-12)

---

## SECTION 0: Quick Start

**Before making any changes, verify the environment works.**

### Project Location
```
Repository: diboas-analytics
Branch: main (or current working branch)
Project root = repository root
```

### Environment Setup
- Python version: Check `pyproject.toml` or `requirements.txt`
- Install dependencies per project conventions
- Required env vars: `FRED_API_KEY`, `COINGECKO_API_KEY` (check `config/settings.py`)

### Verify Current State
```bash
# 1. Run tests
pytest tests/ -v --tb=short

# 2. Verify config loads
python -c "from config.settings import settings; print('Config OK')"

# 3. Check existing data files
ls -la data/*.csv

# 4. View current strategy allocations
python -c "import json; print(json.dumps(json.load(open('config/strategies.json'))['strategies'][0], indent=2))"
```

**Expected:** Tests pass, config loads without error, CSV files exist, strategies load as JSON.

---

## SECTION 1: Executive Context

### Scope Clarifications (from CEO)

| Clarification | Implication |
|---------------|-------------|
| **Brazil is Day 1** | CVM compliance is P0, not P1 |
| **Adelaide is NOT LLM-based** | AI disclosure requirements deferred (6+ months) |
| **Rebalancing/drift is platform-side** | Analytics only identifies need; don't build rebalancing logic |
| **WhatsApp/Telegram posts are manual** | No automated formatter needed for launch |
| **v4/Macro/Mine is nice-to-have** | Focus on v3; don't block launch for v4 features |

### What "Launch" Means
- Public release of fully working v3 analytics pipeline
- Adelaide newsletter generation operational
- Gate 4 compliance validation passing for all target jurisdictions

---

## SECTION 2: Architecture Context

### Core Patterns

**Registry Pattern:** All major components use decorator-based registration:
```python
@CollectorRegistry.register("name")
class MyCollector(Collector):
    ...
```

**Base Classes:**
| Class | Location | Status |
|-------|----------|--------|
| `Collector` | `src/registries/collector_registry.py` | ✅ Active — all collectors inherit from this |
| `DataProvider` | `src/collectors/base.py` | ❌ Dead code — unused, ignore it |

**Gate 4 Compliance:** Fully implemented with 6 sub-validators in `src/validators/clo/`. Orchestrated by `CLOGate4Validator`.

**Triggers:** Use `IntelligenceTriggerBase` from `src/triggers/base.py`. See `sky_protocol_triggers.py` for the pattern to follow.

### Config Source of Truth

| Config File | Status | How It's Loaded |
|-------------|--------|-----------------|
| `config/strategies.json` | ✅ Active | `StrategyLoader` class |
| `config/settings.py` | ✅ Active | Singleton `Settings` class |
| `config/clo_compliance.yaml` | ⚠️ Partial | Exists but some validators hardcode rules instead of loading |
| `config/triggers.yaml` | ❌ Not loaded | Appears to be documentation only; triggers use instantiation config |
| `src/adelaide/localization.py` | ✅ Active | Python dicts for translations (not YAML) |

**Warning:** Config drift exists. Some YAML files are not actually loaded at runtime. Verify before assuming edits take effect.

### Known Architectural Issues (Context Only — Don't Fix Pre-Launch)

- **Type instability:** Aggregator returns DataFrame OR dict on error — downstream must handle both
- **Silent failures:** Empty DataFrame from API failure looks identical to "no data exists"
- **No notification backends:** Triggers fire but don't alert anyone (interface exists, no implementations)
- **Cooldown file has no locking:** Concurrent CLI runs could corrupt `trigger_cooldowns.json`

These are real issues but NOT launch blockers. Don't refactor them pre-launch.

---

## SECTION 3: P0 — Critical Blocking Items

### P0-1: Safe Data Persistence

**Why it's blocking:** Collectors overwrite CSV files directly. If API returns empty data, historical data is destroyed. If write crashes mid-operation, file corrupts.

**Current state:** All collectors use `df.to_csv(filepath)` with no protection.

**Acceptance criteria:**
- Empty DataFrames are rejected (logged, not saved)
- Writes use atomic pattern (no partial/corrupt files possible)
- Zero-byte files never created
- Failed collections don't destroy existing good data

**Where to look:**
- `src/collectors/*.py` — individual collectors
- `src/registries/collector_registry.py` — `Collector` base class
- Consider creating utility in `src/utils/`

**Suggested approach** (Claude Code decides implementation):
```python
# Example pattern — adapt as appropriate for the codebase
def safe_write(df: pd.DataFrame, filepath: str) -> bool:
    if df is None or df.empty:
        logger.warning(f"Rejecting empty write to {filepath}")
        return False
    
    temp_path = f"{filepath}.tmp"
    df.to_csv(temp_path, index=False)
    os.replace(temp_path, filepath)  # Atomic on POSIX
    return True
```

---

### P0-2: Sky 30% Concentration Cap

**Why it's blocking:** Strategy Board approved 30% max for Sky protocol. Current strategies have 50-70%.

**Current state:** `config/strategies.json` has Sky allocations exceeding 30% in strategies 1, 2, 3, etc.

**Acceptance criteria:**
- No strategy has Sky allocation > 30%
- Validation fails if cap is violated
- Changes reflected in strategy output

**Where to look:**
- `config/strategies.json` — allocation values (decimals: `0.30` = 30%)
- Allocations are nested: `strategies[].allocations.stable.sky`
- Consider adding validation in `src/validators/` or strategy loader

**Note:** This is primarily a config change, but consider adding a validator to prevent future violations.

---

### P0-3: CVM 3-Part Warning (Brazil)

**Why it's blocking:** Brazilian CVM regulation requires three-part disclosure structure. Current implementation has single phrase check only.

**Current state:** 
- Validator checks for "investimentos envolvem riscos" (or alternatives)
- No structural validation of 3-part format
- `src/adelaide/localization.py` has `REGIONAL_DISCLAIMERS['pt-br']` but incomplete

**Acceptance criteria:**
- PT-BR output contains all 3 required parts:
  1. "Not protected by investor compensation schemes"
  2. "Value may fluctuate, may lose capital"
  3. "Consult qualified professional"
- Gate 4 validation enforces structure, not just phrase presence

**Where to look:**
- `src/adelaide/localization.py` — `TRANSLATIONS['pt-br']` and `REGIONAL_DISCLAIMERS`
- `src/validators/clo/clo_disclaimer_validator.py` — current validation logic
- Templates in `src/adelaide/templates/`

**Important:** Load disclaimer text from localization, don't hardcode new strings in validator. Avoid adding more config drift.

---

### P0-4: Hypothetical Performance Disclaimer

**Why it's blocking:** SEC Marketing Rule and general compliance require disclaimers on backtested/simulated results.

**Current state:** Monte Carlo and Battle Test outputs don't include required disclaimer language.

**Acceptance criteria:**
- Any output containing backtest/simulation data includes disclaimer
- Disclaimer states: hypothetical nature, hindsight bias, no guarantee of future results
- Applied consistently across all output formats

**Where to look:**
- `src/engines/monte_carlo.py` — result generation
- `src/engines/battle_test.py` — result generation
- `src/domain/simulation.py` — result dataclasses (`MonteCarloResult`, `BattleTestResult`)
- Output formatters in `src/registries/output_registry.py`

---

### P0-5a: USDC/USDT Price Collection

**Why it's blocking:** User safety. Strategies use Aave/Compound which are USDC-exposed. Cannot monitor depeg without price data.

**Current state:** `coingecko_collector.py` only fetches BTC, ETH, SOL:
```python
COIN_IDS = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'sol': 'solana',
}
```

**Acceptance criteria:**
- USDC and USDT prices collected
- Prices appear in output CSV
- Collection doesn't break existing functionality

**Where to look:**
- `src/collectors/coingecko_collector.py` — `COIN_IDS` dict
- CoinGecko IDs: `'usdc': 'usd-coin'`, `'usdt': 'tether'`

---

### P0-5b: Stablecoin Depeg Triggers

**Why it's blocking:** Safety-critical alerting. If USDC depegs and newsletter says "all stable," that's a trust/safety failure.

**Current state:** USDS depeg triggers exist in `sky_protocol_triggers.py`. No USDC/USDT equivalents.

**Acceptance criteria:**
- Triggers fire when USDC or USDT deviates from $1.00 by configured threshold
- Follow existing trigger severity pattern (L2 >1%, L3 >2%, L4 >5%)
- Affected strategies mapped correctly

**Where to look:**
- `src/triggers/protocol/sky_protocol_triggers.py` — pattern to follow
- `src/triggers/base.py` — `IntelligenceTriggerBase`
- `src/registries/trigger_registry.py` — registration pattern

---

## SECTION 4: P1 — High Priority (If Time Permits)

| ID | Task | Notes |
|----|------|-------|
| **P1-1** | MiCA Verbatim (EU) | Current EU validation is MiFID-generic, not MiCA Article 68 specific |
| **P1-2** | Sortino Ratio | Sharpe exists (rough approximation); Sortino missing from Monte Carlo |
| **P1-3** | Collection Metadata | Track when/where data was collected for audit trail |
| **P1-4** | Refine Sharpe Calculation | Current implementation is approximate; consider proper calculation |

---

## SECTION 5: P2 — Post-Launch

- **Config Unification:** Create central loader, eliminate drift between YAML and hardcoded values
- **Notification Backend:** Implement at least one (Slack/email) so triggers actually alert someone
- **Release Gate Automation:** `release_gate.py` for automated GO/NO-GO checks
- **Run Summary Artifact:** Emit `run_report.json` with collection status, gate results, runtime
- **Legacy Code Cleanup:** Remove unused `DataProvider` class
- **v4 Truth Contract Templates:** Prep for next version

---

## SECTION 6: Key Files Reference

| Purpose | Location | Why Relevant |
|---------|----------|--------------|
| Collector base class | `src/registries/collector_registry.py` | Extend for new collectors or add save utility |
| Strategy config | `config/strategies.json` | Sky cap values live here |
| Localization | `src/adelaide/localization.py` | CVM warnings go here |
| Gate 4 validators | `src/validators/clo/*.py` | Compliance validation logic |
| USDS depeg trigger | `src/triggers/protocol/sky_protocol_triggers.py` | Pattern for USDC/USDT triggers |
| CoinGecko collector | `src/collectors/coingecko_collector.py` | Add stablecoin IDs here |
| HTTP client | `src/collectors/http_client.py` | Rate limiting, retry logic |
| Template engine | `src/adelaide/templates.py` | Custom Mustache-like syntax |

---

## SECTION 7: Verification Checklist

### Positive Tests

```bash
# Sky cap verification
python -c "
import json
with open('config/strategies.json') as f:
    data = json.load(f)
for s in data['strategies']:
    sky = s.get('allocations', {}).get('stable', {}).get('sky', 0)
    if sky > 0.30:
        print(f'FAIL: Strategy {s[\"id\"]} has Sky at {sky*100}%')
print('Sky cap check complete')
"

# CVM 3-part check (after generating PT-BR output)
grep -c "não é protegido\|pode perder\|profissional habilitado" output/adelaide_pt-br.md

# Stablecoin prices collected
head -5 data/crypto_prices.csv | grep -i "usdc\|usdt"

# Gate 4 passes
python -c "from src.validators.clo import CLOGate4Validator; print('Gate 4 loads OK')"
```

### Negative Tests (Failure Scenarios)

| Test | Expected Behavior |
|------|-------------------|
| Pass empty DataFrame to save utility | Rejection logged, no file written |
| Simulate API failure → run collector | No overwrite of existing good data |
| Run Gate 4 with missing BR disclaimer | Returns FAIL status |
| Fire same trigger twice within cooldown | Second fire blocked by cooldown manager |

---

## SECTION 8: What's NOT in Scope

**Do not implement:**
- AI disclosure (Adelaide not LLM-based yet)
- Rebalancing/drift calculation logic (platform-side concern)
- WhatsApp message formatter (manual posts for launch)
- Yield Hunter / B2B Client personas (post-launch)
- Notification backends (post-launch)

**Do not refactor:**
- Registry system architecture
- Base class hierarchy (don't try to "fix" DataProvider)
- Config loading patterns (document drift, don't unify pre-launch)
- Aggregator return types (known issue, defer)

**Explicit instruction:** Focus on P0 items. Resist the urge to clean up architectural issues — they're real but not launch-blocking.

---

## SECTION 9: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Data corruption during write | Medium | High | P0-1 (atomic writes + empty rejection) |
| Missed USDC/USDT depeg | Low | Critical | P0-5a/b (price collection + triggers) |
| CVM non-compliance (Brazil) | High | Critical (fines) | P0-3 (3-part structure) |
| SEC disclaimer missing | High | High | P0-4 (hypothetical performance) |
| Sky concentration violation | High | Medium | P0-2 (cap enforcement) |
| Config drift confusion | Medium | Low | Document in handoff; defer fix |

---

## Appendix: Decision Authority

| Domain | Authority | Notes |
|--------|-----------|-------|
| Compliance changes | CLO Board / Legal | Any disclaimer text changes |
| Strategy changes | Strategy Board | Allocation percentages, caps |
| Gate 4 overrides | None | No override mechanism pre-launch |
| Architecture decisions | Claude Code discretion | Within P0/P1 scope |

---

## Summary: Priority Order

1. **P0-1:** Safe Data Persistence (prevents data loss)
2. **P0-3:** CVM 3-Warning (Brazil Day 1 legal requirement)
3. **P0-2:** Sky 30% Cap (Strategy Board mandate)
4. **P0-4:** Hypothetical Performance Disclaimer (SEC compliance)
5. **P0-5a:** USDC/USDT Price Collection (data prerequisite)
6. **P0-5b:** Stablecoin Depeg Triggers (safety alerting)

**Estimated P0 effort:** 15-20 hours (2-3 focused days)

---

*Document prepared for Claude Code implementation — February 3, 2026*
