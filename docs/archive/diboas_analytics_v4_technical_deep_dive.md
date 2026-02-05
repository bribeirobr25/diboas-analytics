# diBoaS Analytics v4 - Complete Technical Deep Dive

## Executive Summary

diBoaS Analytics v4 represents a fundamental architectural shift from **"smart analytics"** to **"provable intelligence"**. While v3 focused on validation and analysis, v4 introduces a **Zero-Trust architecture** where every claim must have a cryptographic receipt (Evidence Pack), every data feed must have a formal contract (Truth Contract), and publication is **blocked by default** unless the entire system is healthy.

The core philosophy: **"If you can't prove it, you can't publish it."**

---

## 1. Technology Stack & Architecture

### 1.1 Architectural Philosophy: Zero-Trust Intelligence

| Principle | v3 Approach | v4 Approach |
|-----------|-------------|-------------|
| **Data Ingestion** | Collectors fetch data | "No contract = no ingest" |
| **Publication** | Manual pipeline execution | "No evidence pack = no publish" |
| **Compliance** | Gate 4 exists | Gate 4 is a deterministic firewall |
| **Audit Trail** | Limited logging | Full cryptographic receipts |
| **System Health** | Advisory | **Arbiter** (RED = blocked) |

### 1.2 Core Technologies (Specification Layer)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Contract Format** | YAML | Truth Contract definitions |
| **Evidence Format** | YAML/JSON | Evidence Pack receipts |
| **Schema Validation** | JSON Schema | CI-enforced contract validation |
| **Hashing** | SHA-256 | Data lineage and reproducibility |
| **Time Format** | ISO 8601 | Timestamps and durations |
| **Configuration** | YAML | Gate rules, thresholds, routing |

### 1.3 6-Layer Architecture (vs v3's 5 Layers)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LAYER 0: INGESTION                          │
│         Raw data collection (No contract = no ingest)               │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Raw Data
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: RAW VALIDATION                          │
│             Gate 1 (Schema, Missingness, Freshness)                │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Validated Raw
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   LAYER 2: CLEAN CANONICAL                          │
│           Unit conversion, derivations, forward-fill                │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Clean Data
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  LAYER 3: CLEAN VALIDATION                          │
│          Gate 2 (Reconciliation, Derivation, Stale Checks)         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Validated Clean
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  LAYER 4: INTELLIGENCE ENGINE                       │
│    Gate 3 (Signal generation, Event classes, Evidence Packs)       │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Signals + Evidence
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 LAYER 5: RENDERING & DISTRIBUTION                   │
│      Gate 4 (Compliance firewall, disclaimers, channels)           │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Published Edition
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   LAYER 6: TELEMETRY & COORDINATION                 │
│        Publication eligibility, tasks, dashboards, MTTR            │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.4 Project Structure (Recommended)

```
diboas-analytics/
├── docs/v4/
│   ├── 00_INDEX.md                    # Master index (always current)
│   ├── spec/                          # Normative specifications
│   │   ├── 01_v4_progress_summary.md
│   │   ├── 03_v4_truth_contract_spec.md
│   │   ├── 05_v4_evidence_pack_spec.md
│   │   ├── 06_v4_adelaide_weekly_output_contract.md
│   │   ├── 07_v4_telemetry_dashboard_spec.md
│   │   ├── 08_gate4_compliance_ruleset_v1.md
│   │   ├── 11_trust_score_v1.md
│   │   ├── 17_v4_strategic_positioning_and_user_tiers.md
│   │   └── 18_v4_event_class_definitions_v1.md
│   └── contracts/                     # Contract registries
│       ├── 02_v4_phase0_core_contracts.md
│       ├── 13_v4_data_collection_plan_zero_budget.md
│       └── 16_v4_phase0_5_global_macro_extension_pack.md
├── contracts/
│   └── truth_contracts/
│       ├── phase0/                    # 23 core contracts
│       ├── phase0_5/                  # Global macro extension
│       ├── derived/                   # Derived metrics
│       └── deprecated/                # Old contracts
├── config/
│   ├── trust_score/
│   │   ├── trust_score_v1_weights.yaml
│   │   └── cc_map_v1.yaml
│   ├── gate4/
│   │   ├── gate4_language_pack_en_v1.yaml
│   │   ├── gate4_language_pack_ptbr_v1.yaml
│   │   └── classifier_thresholds_v1.yaml
│   ├── telemetry/
│   │   ├── alert_thresholds_v1.yaml
│   │   └── publication_eligibility_v1.yaml
│   └── events/
│       ├── routing_policy_v1.yaml
│       ├── public_alert_limits_v1.yaml
│       └── event_thresholds_v1.yaml
├── samples/
│   └── adelaide/weekly/2026w05/
│       ├── adelaide_weekly_2026w05_v3.md
│       ├── telemetry_snapshot.json
│       ├── gate4_findings.yaml
│       └── evidence_packs/
│           ├── ep_2026w05_sig_01.yaml
│           └── ...
├── schema/
│   ├── truth_contract.schema.json
│   ├── evidence_pack.schema.json
│   ├── adelaide_weekly.schema.json
│   └── event_snapshot.schema.json
├── governance/
│   ├── CHANGELOG.md
│   ├── APPROVALS.md
│   └── decisions/
│       ├── ADR-0001-v4-truth-contracts.md
│       └── ...
└── tools/
    ├── collectors/
    ├── validators/
    ├── generators/
    ├── gate4/
    ├── telemetry/
    └── events/
```

### 1.5 4 Golden Rules (Non-Negotiable)

```python
# These rules are HARD-CODED into the system and cannot be bypassed

GOLDEN_RULES = {
    1: "No contract = no ingest",      # Every feed needs a Truth Contract
    2: "No evidence pack = no publish", # Every signal needs a receipt
    3: "Gate 4 is mandatory",           # Publication firewall for all content
    4: "Telemetry is the arbiter",      # RED = blocked, no exceptions
}
```

### 1.6 Code Standards & Governance

**Document Versioning:**
- Specs use `major.minor.patch` versioning
- Material changes require QR Board review
- `00_INDEX.md` must always be current

**Contract Change Control:**
```yaml
change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7
```

**Board Responsibilities:**

| Board | Responsibility |
|-------|----------------|
| **CTO Board** | Ingestion, pipeline, telemetry, enforcement |
| **Rakia/Data Board** | Contracts, sources, transformations |
| **QR Board** | Validation rules, thresholds, contract approvals |
| **Strategy Board** | Signal policy, scenario framing, severity/horizon |
| **Compliance Board** | Gate 4 ruleset, disclaimers, jurisdiction posture |

---

## 2. Data Collection & Monitoring

### 2.1 Phase 0: Trust Spine MVP (23 Core Contracts)

**Objective:** Smallest set of contracts capable of producing one reproducible, audit-ready weekly edition.

#### A) Rates & Macro (7 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `rates_us2y_yield_v1` | Critical | EOD | Short-term rate benchmark |
| `rates_us10y_yield_v1` | Critical | EOD | Long-term rate benchmark |
| `rates_us30y_yield_v1` | Critical | EOD | Ultra-long rate benchmark |
| `rates_2s10s_spread_v1` | High | EOD | Yield curve shape (derived) |
| `rates_us10y_real_yield_v1` | Critical | EOD | Inflation-adjusted rates (proxy) |
| `macro_us_inflation_breakeven_10y_v1` | High | EOD | Inflation expectations (proxy) |
| `macro_global_liquidity_proxy_v1` | High | ~14d lag | Global liquidity conditions |

#### B) TradFi Risk & Positioning (4 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `fx_usd_index_proxy_v1` | High | EOD | Dollar strength |
| `equity_spx_proxy_v1` | High | EOD | Equity market proxy |
| `vol_vix_proxy_v1` | Medium | EOD | Market fear gauge |
| `credit_hy_ig_spread_proxy_v1` | High | EOD | Credit stress |

#### C) Crypto Spot & Structure (6 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `crypto_btc_spot_usd_v1` | Critical | Hourly | Bitcoin price |
| `crypto_eth_spot_usd_v1` | Critical | Hourly | Ethereum price |
| `crypto_btc_perps_funding_v1` | High | Hourly | BTC leverage sentiment |
| `crypto_btc_perps_open_interest_v1` | High | Hourly | BTC positioning |
| `crypto_eth_perps_funding_v1` | High | Hourly | ETH leverage sentiment |
| `crypto_eth_perps_open_interest_v1` | High | Hourly | ETH positioning |

#### D) Stablecoins (2 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `stablecoin_total_supply_v1` | High | Daily | Crypto liquidity plumbing |
| `stablecoin_depeg_events_v1` | **Critical** | **15m** | Early warning (smoke alarm) |

#### E) DeFi Baseline (2 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `defi_bluechip_tvl_v1` | High | Daily | On-chain expansion/contraction |
| `defi_yield_benchmark_v1` | High | Daily | DeFi yield composite |

#### F) RWA Bridge (2 contracts)

| Contract ID | Risk Tier | Cadence | Purpose |
|-------------|-----------|---------|---------|
| `rwa_tokenized_treasury_tvl_nav_v1` | High | EOD | TradFi/DeFi bridge |
| `rwa_tokenized_treasury_net_flows_v1` | High | EOD | Capital flows (derived) |

### 2.2 Phase 0.5: Global Macro Extension Pack

**Purpose:** Add high-signal non-US/global anchors without breaking Phase 0 reliability.

**Rule:** Phase 0.5 must NOT block Phase 0 publication unless explicitly referenced.

#### Japan Exception (Critical for Global Liquidity)

| Contract ID | Priority | Cadence | Purpose |
|-------------|----------|---------|---------|
| `fx_usdjpy_spot_v1` | **Critical** | Daily | USD/JPY regime shifts |
| `rates_jp10y_yield_proxy_daily_v1` | **Critical** | Daily | Japan yield (proxy) |
| `rates_jp10y_yield_oecd_monthly_v1` | Medium | Monthly | Long-history context |
| `rates_jp_policy_rate_v1` | High | Monthly | Policy regime confirmation |

#### Financial Stress Anchor

| Contract ID | Priority | Cadence | Purpose |
|-------------|----------|---------|---------|
| `macro_us_nfci_v1` | High | Weekly | Broad financial conditions |

#### Commodities Pulse

| Contract ID | Priority | Cadence | Purpose |
|-------------|----------|---------|---------|
| `commod_wti_spot_v1` | Medium | Daily | Energy/inflation pressure |
| `commod_copper_spot_v1` | Medium | Daily | Industrial demand proxy |

#### Brazil Pack (Regional Context)

| Contract ID | Priority | Cadence | Purpose |
|-------------|----------|---------|---------|
| `rates_br_selic_v1` | Medium | Daily | Brazil borrowing conditions |
| `equity_br_ibovespa_proxy_v1` | Low | Daily | Brazil equity context |

### 2.3 SLA Definitions (Dual-SLA System)

**Key Innovation:** v4 separates internal pipeline health from publication readiness.

| SLA Type | Purpose | Effect of Breach |
|----------|---------|------------------|
| **internal_sla** | Pipeline health monitoring | Create task, send alert |
| **publication_sla** | Hard publication blocker | **Block publication** |

**Default SLA Targets:**

| Contract Group | Internal SLA | Publication SLA | Notes |
|----------------|--------------|-----------------|-------|
| Rates / TradFi proxies | <24h | <48h | TradFi holidays allowed |
| Macro liquidity proxy | <14d | <14d | **Lag disclosure required** |
| Crypto spot/perps | <60m | <12h | **No forward-fill allowed** |
| Stablecoin depeg events | <15m | <4h | Critical escalation |
| DeFi TVL/yield | <24h | <48h | Composite disclosures |
| RWA TVL/flows | <48h | <72h | Issuer lag disclosure |
| Japan (Phase 0.5) | <24h | <48h | Required for EC-07 |
| NFCI (Phase 0.5) | <7d | <14d | Weekly release |
| Brazil (Phase 0.5) | <48h | <72h | Holiday-aware |

### 2.4 Source Tiering ($0 Budget Reality)

| Tier | Examples | Trust Level | Policy |
|------|----------|-------------|--------|
| **Tier 1** | FRED, central banks | High | Store `retrieved_at_ts` + vintage fields |
| **Tier 2** | DeFiLlama, aggregators | Medium | Fallbacks + drift tracking + reconciliation |
| **Tier 3** | Exchange APIs, scraped | Lower | Multi-venue aggregate + stale checks mandatory |

### 2.5 Data Collection Endpoints

#### FRED (Tier 1 - Macro Backbone)
```
Base: https://api.stlouisfed.org/fred/series/observations
      ?series_id={SERIES}&api_key={KEY}&file_type=json

Series IDs:
- Yields: DGS2, DGS10, DGS30
- Real yield: DFII10
- Breakeven: T10YIE
- VIX proxy: VIXCLS
- SPX proxy: SP500
- USD: DTWEXBGS
- HY OAS: BAMLH0A0HYM2
- NFCI: NFCI
- WTI: DCOILWTICO
- USD/JPY: DEXJPUS
```

#### Brazil Central Bank SGS (Tier 1)
```
Base: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{SERIE}/dados
      ?formato=json&dataInicial=01/01/2010

Series: SELIC = 11
```

### 2.6 Heartbeat Collector (Orchestration)

**Single orchestrated collector to prevent rate-limit chaos:**

```python
# Collector tick schedule
SCHEDULE = {
    "every_tick": [  # Runs every hour
        "crypto_spot",
        "perps_funding_oi",
        "depeg_checks"
    ],
    "hour_00_utc": [  # Daily at midnight
        "fred_macro_tradfi",
        "defi_tvl_yields",
        "rwa_tvl_flows"
    ],
    "pre_publish": {  # Sunday 04:00 UTC (before eligibility check)
        "trigger": "Sunday 04:00 UTC",
        "refresh": ["crypto", "perps", "stables", "near_breach_slas"]
    }
}
```

### 2.7 Final Truth Snapshot (Edition Snapshot Semantics)

**Critical Concept:** Single timestamp determining edition eligibility.

```yaml
final_truth_snapshot_ts: "Sunday 04:00 UTC"  # Default, configurable

Rules:
  - For each referenced contract: select latest observation where asof_ts <= final_truth_snapshot_ts
  - If ANY referenced contract is:
      - missing
      - stale beyond publication_sla
      - FAIL at Gate 1/2
      - has unresolved high/critical reconciliation diffs (7d)
    Then:
      - Telemetry => RED
      - Publication => BLOCKED
      - Tasks => created with severity by risk tier
```

### 2.8 Forward-Fill Policy (Critical Difference from v3)

| Asset Class | Forward-Fill | Rationale |
|-------------|--------------|-----------|
| **Crypto** | **FORBIDDEN** | 24/7 markets; forward-fill creates ghost data |
| **TradFi** | Allowed with disclosure | Weekends/holidays are real; must disclose |

```yaml
# Example: Crypto contract
forward_fill_policy:
  allowed: false
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "Crypto is 24/7. Forward-fill creates ghost data. Forbidden."

# Example: TradFi contract
forward_fill_policy:
  allowed: true
  max_window: "P1D"
  disclosure_label: "forward_fill_applied"
  notes: "Allowed for TradFi holidays/weekends. Must disclose if applied."
```

### 2.9 Failure Mode Defenses ($0 Reality)

#### Ghost Updates (Timestamps Move, Values Freeze)
```yaml
gate2_validations:
  - id: "G2-STALE-VALUE-001"
    stale_value_check:
      enabled: true
      window_n_updates: 4
      rule: "if value unchanged for N consecutive expected updates"
      severity_by_risk_tier:
        critical: "FAIL"
        high: "PASS_WITH_FLAGS"
        medium: "PASS_WITH_FLAGS"
        low: "FLAG_ONLY"
```

#### Zombie APIs (200 OK but Null/Zero)
```yaml
gate2_validations:
  - id: "G2-NULL-ZERO-FLOOR-001"
    null_zero_floor_check:
      enabled: true
      field: "value"
      null_is_fail: true
      zero_is_fail: false  # Set true only if zero is invalid
      severity_by_risk_tier:
        critical: "FAIL"
        high: "FAIL"
        medium: "PASS_WITH_FLAGS"
        low: "FLAG_ONLY"
```

#### Methodology Drift (Tier 2/3 Providers)
```yaml
methodology_drift_policy:
  enabled: true
  on_detected_change: "set_pass_with_flags_and_create_task"
  detection_signals:
    - "provider_version_changed"
    - "parser_transform_hash_changed"
    - "schema_changed"
  required_disclosure_label: "methodology_change"
```

---

## 3. Market Indicators & User Value

### 3.1 What v4 Tracks (by Domain)

#### Macro Gravity (Rates & Inflation)

| Indicator | Contract | Thresholds | User Value |
|-----------|----------|------------|------------|
| US 2Y Yield | `rates_us2y_yield_v1` | N/A | Short-term rate pressure |
| US 10Y Yield | `rates_us10y_yield_v1` | N/A | Long-term borrowing cost |
| 2s10s Spread | `rates_2s10s_spread_v1` | Inversion watch | Yield curve shape |
| Real Yields | `rates_us10y_real_yield_v1` | Delta > 25bp | Inflation-adjusted pressure |
| Breakeven | `macro_us_inflation_breakeven_10y_v1` | N/A | Inflation expectations |

#### Risk & Stress

| Indicator | Contract | Thresholds | User Value |
|-----------|----------|------------|------------|
| VIX | `vol_vix_proxy_v1` | >30 (elevated), >40 (crisis) | Market fear |
| USD Index | `fx_usd_index_proxy_v1` | N/A | Dollar strength pressure |
| Credit Spreads | `credit_hy_ig_spread_proxy_v1` | Widening | Borrowing stress |
| NFCI (Phase 0.5) | `macro_us_nfci_v1` | N/A | Broad financial conditions |

#### Crypto Markets

| Indicator | Contract | Thresholds | User Value |
|-----------|----------|------------|------------|
| BTC Price | `crypto_btc_spot_usd_v1` | N/A | Market leader |
| ETH Price | `crypto_eth_spot_usd_v1` | N/A | DeFi benchmark |
| BTC Funding | `crypto_btc_perps_funding_v1` | Negative = cautious | Leverage sentiment |
| BTC Open Interest | `crypto_btc_perps_open_interest_v1` | Delta < -5% | Positioning |

#### Stablecoins (Smoke Alarms)

| Indicator | Contract | Thresholds | User Value |
|-----------|----------|------------|------------|
| Total Supply | `stablecoin_total_supply_v1` | N/A | Crypto liquidity |
| Depeg Events | `stablecoin_depeg_events_v1` | **Any event** | **Critical early warning** |

#### DeFi & RWA

| Indicator | Contract | Thresholds | User Value |
|-----------|----------|------------|------------|
| Blue-chip TVL | `defi_bluechip_tvl_v1` | < -10% 2w | On-chain contraction |
| Yield Benchmark | `defi_yield_benchmark_v1` | N/A (methodology-sensitive) | DeFi yield baseline |
| Tokenized Treasury | `rwa_tokenized_treasury_tvl_nav_v1` | N/A | TradFi/DeFi bridge |

### 3.2 User Value by Tier

| User Type | Tier | What They Receive | User Value |
|-----------|------|-------------------|------------|
| **Normal users** | A | Weekly "weather report" | Situational awareness without hype |
| **Interested learners** | B | + explicit drivers, confidence | Learn to think in scenarios |
| **Experts/traders** | C | + Evidence Packs, structured data | Save time; cleaned reality |
| **Local businesses** | A+ | + inflation/energy/credit pulse | Early cost/financing awareness |
| **SMBs** | B | + "financing climate" framing | Pressure-test plans |
| **Treasury clients** | C | + regime classification, audit | Board-friendly traceability |

### 3.3 What diBoaS Detects vs Cannot Detect

**Strong Detection Capability:**
- Liquidity tightening/easing regimes
- Risk-off cascades (stress clusters)
- Crypto leverage unwind patterns
- Stablecoin stress events
- Japan carry stress (with Phase 0.5)
- Credit stress widening

**Partial Detection:**
- Capital rotation (needs sector witnesses for "complete")

**Cannot Detect (by design):**
- Micro-catalysts (ETF headlines, lawsuits, tweets)
- Specific price predictions
- Individual company events

---

## 4. Gate System Deep Dive

### 4.1 4 Gates Overview

| Gate | Layer | Purpose | Checks |
|------|-------|---------|--------|
| **Gate 1** | 1 | Raw validation | Schema, missingness, freshness, basic sanity |
| **Gate 2** | 3 | Clean validation | Unit enforcement, derivation, reconciliation, stale/zombie |
| **Gate 3** | 4 | Intelligence validation | Signal schema, confidence, invalidation, severity |
| **Gate 4** | 5 | Compliance firewall | Language, disclaimers, disclosures, channels |

### 4.2 Gate 1: Raw Validation

**Validation IDs:**
```yaml
gate1_raw:
  - id: "G1-SCHEMA-001"  # Required columns, types
  - id: "G1-FRESH-001"   # Not stale vs internal_sla
  - id: "G1-SANITY-001"  # Basic bounds (e.g., APY not negative)
```

**Failure Actions:**
- Create task with priority based on risk_tier
- Do NOT promote to clean layer
- Log to telemetry

### 4.3 Gate 2: Clean Validation

**Validation IDs:**
```yaml
gate2_clean:
  - id: "G2-UNIT-001"    # Unit conversion correct
  - id: "G2-DERIVE-001"  # Derivation formula executed correctly
  - id: "G2-RECON-001"   # Canonical vs fallback within tolerance
  - id: "G2-STALE-VALUE-001"  # Ghost feed detection
  - id: "G2-NULL-ZERO-FLOOR-001"  # Zombie API detection
```

**Reconciliation Policy:**
```yaml
reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 0.0005    # e.g., 0.05 basis points
    relative: 0.01      # e.g., 1% deviation
  on_breach: "block_clean_promote_and_create_task"
```

### 4.4 Gate 3: Intelligence Validation

**Signal Schema Requirements:**
```yaml
signal:
  id: "sig_xxx_v1"
  headline: "Short headline"
  why_it_matters: "Plain-language explanation"
  horizon: "1-8 weeks | 1-3 months | 3-12 months"
  severity: "low | medium | high"
  confidence:
    score: 0.72
    label: "low | medium | high"
  drivers:
    - "short driver phrase"
  watch_items:
    - "thing to watch"
  invalidation_summary: "What would make this wrong"
  evidence_pack_id: "ep_YYYYwWW_sig_XX"
  disclosures:
    - "disclosure shown after signal"
```

**Signal Count Limits:** 3-7 signals per edition (hard-coded)

**Confidence Policy:**
- If `confidence < 0.55`: Mandatory "Higher uncertainty" caveat in Layer A
- High severity MAY require stricter confidence floors (configurable)

### 4.5 Gate 4: Compliance Firewall (Detailed)

#### 7 Rule Groups

| Group | Purpose | Failure Mode |
|-------|---------|--------------|
| **A** | Prohibited phrases (blocklist) | Hard FAIL |
| **B** | Recommendation-likeness (classifier) | Score-based |
| **C** | Backtest/performance framing | Channel-specific |
| **D** | Disclosures (triggered + placement) | Missing = FAIL |
| **E** | Personalization (hard ban) | Hard FAIL |
| **F** | False precision/overconfidence | Hard FAIL |
| **G** | Overrides and break-glass | Logged + restricted |

#### Rule Group A: Prohibited Phrases (Always FAIL)

```yaml
# A1: Direct transaction directives
prohibited:
  - "buy"
  - "sell"
  - "long"
  - "short"
  - "ape in"
  - "load up"
  - "take profit"
  - "exit now"
  - "rotate into"
  - "allocate X% to"
  - "this is a great entry"

# A2: Suitability/personalization
prohibited:
  - "for your portfolio"
  - "you should"
  - "if you have $X"
  - "best for you"
  - "your retirement"

# A3: Guaranteed outcomes
prohibited:
  - "guaranteed"
  - "risk-free"
  - "sure thing"
  - "can't lose"
  - "no downside"
  - "almost certain"
  - "highly likely to outperform"

# A4: Regulatory red flags
prohibited:
  - "insider"
  - "guaranteed edge"
  - "we found a loophole"
  - "front-run"
```

#### Rule Group B: Recommendation-Likeness Classifier

```yaml
classifier:
  model: "recommendation_likeness_v1"
  thresholds:
    pass: 0.30
    pass_with_flags: 0.45
    fail: 0.45
  
  # Features that increase score:
  features:
    - imperative_verbs      # "do this", "move into"
    - second_person         # "you", "your"
    - certainty_language    # "will", "surely"
    - action_framing        # "best move is"
    - numeric_prescriptions # "put 20% into"

# Output must be explainable
output:
  offending_sentences: []
  score: 0.22
  top_contributing_features: []
```

#### Rule Group C: Backtest/Performance Framing

**Layer A + Telegram (Strict):**
```yaml
forbidden:
  - "would have made X%"
  - "if you followed this"
  - "expected return of"
  - "win rate"
  - "92% success rate"

allowed:
  - "In similar past setups, outcomes varied widely."
  - "Historical reference, not a prediction."
  - "Illustrative scenario based on assumptions."
```

**Layer B (More Permissive):**
```yaml
allowed:
  - scenario ranges with assumptions
required:
  - "hypothetical" label
  - methodology reference
  - limitations/caveats
forbidden:
  - certainty claims
  - individualized expectations
```

#### Rule Group D: Disclosure Triggers

```yaml
disclosure_triggers:
  - condition: "cadence_lag exists"
    disclosure_type: "cadence_lag"
  - condition: "forward_fill_policy.allowed == true AND applied == true"
    disclosure_type: "forward_fill"
  - condition: "sources.canonical.tier >= 2"
    disclosure_type: "proxy"
  - condition: "derivations.is_derived == true"
    disclosure_type: "derivation"
  - condition: "validation_status == PASS_WITH_FLAGS"
    disclosure_type: "pass_with_flags"

# Placement rules
placement:
  web_email_substack: "immediately after signal block"
  telegram: "link to canonical + minimal short reminder"

# Required suffix
required_suffix: "This does not change the educational nature of this commentary."
```

#### Rule Group F: False Precision

```yaml
forbidden:
  - "95% accuracy"
  - "92% historical success"
  - "high probability"  # without caveats
  - precise_forecasts_without_uncertainty

allowed:
  - broad_probability_ranges: ["low", "medium", "high"]
  - "possible outcomes include..."
```

### 4.6 Gate 4 Output Format

```yaml
gate4_result:
  status: "PASS | PASS_WITH_FLAGS | FAIL"
  ruleset_id: "gate4_compliance_ruleset_v1"
  classifier:
    max_score: 0.22
    threshold_profile: "classifier_v1_thresholds"
  findings:
    - rule_id: "A1"
      severity: "FAIL"
      location: "Layer A Signal 2"
      snippet: "You should buy ETH here"
      reason: "Direct transaction directive / personalization"
```

---

## 5. Truth Contract System ("The Contract")

### 5.1 Purpose

Truth Contracts define **how a metric is sourced, refreshed, validated, reconciled, transformed, and governed**. They are the enforceable specification for each data feed.

**Rule:** No contract = no ingest.

### 5.2 Truth Contract YAML Template (v4.1)

```yaml
# ===== IDENTITY & GOVERNANCE =====
contract_id: "rates_us10y_yield_v1"
version: "1.0.0"
domain: "rates | macro | tradfi | crypto | stablecoin | defi | rwa"
risk_tier: "critical | high | medium | low"

owner:
  board: "Rakia"
  steward: "name_or_role"

last_reviewed: "YYYY-MM-DD"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "Human description of the metric."

# ===== CADENCE & SLAs =====
cadence:
  expected_update: "eod | hourly | 15m | weekly | monthly"
  timezone: "UTC"

freshness_sla:
  internal_sla: "PT60M"          # ISO 8601 duration
  publication_sla: "PT12H"       # ISO 8601 duration

collector_policy:
  collector_group: "hourly | daily_00utc | weekly | monthly"
  heartbeat_tick: "PT1H"
  pre_publish_refresh: true
  final_truth_snapshot_role: "depends_on_edition_snapshot"

# ===== HISTORY POLICY =====
history_policy:
  backtest_depth_required: "MAX_AVAILABLE | P15Y | P10Y | P6Y | P3Y"
  min_start_date: null  # e.g., "2010-01-01"
  reason: "macro regime coverage"
  known_coverage_limits: "e.g., perps history starts ~2019"

# ===== UNITS & SCHEMA =====
units:
  standard_unit: "percent"       # conceptual unit
  clean_unit: "decimal"          # stored unit
  decimals: 6
  conversion:
    required: true
    formula: "clean = standard / 100"

storage:
  raw_table: "raw.<table>"
  clean_table: "clean.<table>"
  primary_key: ["asof_ts"]

schema:
  fields:
    - name: "asof_ts"
      type: "timestamp"
      required: true
    - name: "value"
      type: "number"
      required: true
    - name: "retrieved_at_ts"
      type: "timestamp"
      required: true
    - name: "source_name"
      type: "string"
      required: true
    - name: "source_tier"
      type: "number"
      required: true

# ===== SOURCES & METHODOLOGY DRIFT =====
sources:
  canonical:
    name: "FRED"
    tier: 1
    uri: "fred:DGS10"
    method:
      source_methodology_version: "provider_version_or_internal_tag"
      methodology_notes: "EOD close from Federal Reserve."
  fallback:
    - name: "TradingEconomics"
      tier: 2
      uri: "te:us_10y"
      method:
        source_methodology_version: "v1"
        methodology_notes: "Fallback source."

methodology_drift_policy:
  enabled: true
  on_detected_change: "set_pass_with_flags_and_create_task"
  detection_signals:
    - "provider_version_changed"
    - "parser_transform_hash_changed"
    - "schema_changed"
  required_disclosure_label: "methodology_change"

# ===== FORWARD FILL POLICY =====
forward_fill_policy:
  allowed: false  # true for TradFi
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "Crypto must be false."

# ===== DERIVATIONS =====
derivations:
  is_derived: false
  inputs: []
  formula: null
  methodology_version: "1.0.0"

# ===== RECONCILIATION =====
reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 0.0005
    relative: 0.01
  on_breach: "block_clean_promote_and_create_task"

# ===== GATE VALIDATIONS =====
gate_validations:
  gate1_raw:
    - id: "G1-SCHEMA-001"
    - id: "G1-FRESH-001"
    - id: "G1-SANITY-001"

  gate2_clean:
    - id: "G2-UNIT-001"
    - id: "G2-RECON-001"
    - id: "G2-DERIVE-001"
    - id: "G2-STALE-VALUE-001"
      stale_value_check:
        enabled: true
        window_n_updates: 4
        rule: "if value unchanged for N consecutive expected updates"
        severity_by_risk_tier:
          critical: "FAIL"
          high: "PASS_WITH_FLAGS"
    - id: "G2-NULL-ZERO-FLOOR-001"
      null_zero_floor_check:
        enabled: true
        field: "value"
        null_is_fail: true
        zero_is_fail: false

  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If forward_fill_policy.allowed AND applied -> disclosure required"
      - "If derivations.is_derived -> derivation disclosure required"
      - "If validation_status == PASS_WITH_FLAGS -> flags disclosure required"

# ===== ALERTING =====
alerting:
  on_internal_sla_breach:
    board: "CTO Board"
    priority: "high"
  on_publication_sla_breach:
    board: "CTO Board"
    priority: "critical"
  on_reconciliation_breach:
    board: "QR Board"
    priority: "high"
  on_methodology_drift:
    board: "QR Board"
    priority: "high"
  on_zombie_api_detected:
    board: "CTO Board"
    priority: "high"
```

### 5.3 Truth Contract Examples

#### Example A: US 10Y Yield (TradFi, Forward-Fill Allowed)

```yaml
contract_id: "rates_us10y_yield_v1"
version: "1.0.0"
domain: "rates"
risk_tier: "critical"

cadence:
  expected_update: "eod"
  timezone: "UTC"

freshness_sla:
  internal_sla: "P1D"
  publication_sla: "P2D"

forward_fill_policy:
  allowed: true
  max_window: "P1D"
  disclosure_label: "forward_fill_applied"
  notes: "Allowed for weekends/holidays. Disclosure required."

sources:
  canonical:
    name: "FRED"
    tier: 1
    uri: "fred:DGS10"
```

#### Example B: 2s10s Spread (Derived)

```yaml
contract_id: "rates_2s10s_spread_v1"
version: "1.0.0"
domain: "rates"
risk_tier: "high"

derivations:
  is_derived: true
  inputs: ["rates_us10y_yield_v1", "rates_us2y_yield_v1"]
  formula: "clean.rates_us10y_yield_v1.value - clean.rates_us2y_yield_v1.value"
  methodology_version: "1.0.0"

forward_fill_policy:
  allowed: true
  max_window: "P1D"
  notes: "If either input is forward-filled, this inherits disclosure."

reconciliation:
  required: false  # Derived metrics don't reconcile
```

#### Example C: BTC Perps Funding (Crypto, No Forward-Fill)

```yaml
contract_id: "crypto_btc_perps_funding_v1"
version: "1.0.0"
domain: "crypto"
risk_tier: "high"

cadence:
  expected_update: "hourly"
  timezone: "UTC"

freshness_sla:
  internal_sla: "PT60M"
  publication_sla: "PT12H"

forward_fill_policy:
  allowed: false
  max_window: "P0D"
  notes: "Crypto is 24/7. Forward-fill creates ghost data. Forbidden."

derivations:
  is_derived: true
  inputs: ["raw.crypto_perps.*"]
  formula: "weighted_median_by_oi(value) across venues"

sources:
  canonical:
    name: "ExchangeAggregate"
    tier: 2
    uri: "agg:funding_rate_btc_perps"
```

---

## 6. Evidence Pack System ("The Receipt")

### 6.1 Purpose

Evidence Packs are **cryptographic receipts** connecting any published signal to:
- Exact data used (contract IDs + timestamps)
- Validation statuses
- Pipeline version + hashes (reproducibility)
- Invalidation rules
- Approvals + overrides

**Rule:** No evidence pack = no publish.

### 6.2 Evidence Pack Schema

```yaml
# ===== IDENTITY =====
evidence_pack_id: "ep_YYYYwWW_sig_XX"
signal_id: "sig_some_signal_v1"
edition_id: "adelaide_weekly_YYYYwWW"
created_at: "2026-02-01T04:30:00Z"

# ===== CLAIM =====
claim:
  headline: "Human headline"
  summary: "Human summary"
  horizon: "1-8 weeks | 1-3 months | 3-12 months"
  severity: "low | medium | high"
  confidence: 0.72

override:
  edition_confidence_override: false
  override_reason: null

# ===== DISCLOSURES =====
disclosures:
  - type: "cadence_lag | forward_fill | proxy | derivation | methodology | data_quality | pass_with_flags | none_required"
    message: "Disclosure message. This does not change the educational nature of this commentary."

# ===== DRIVERS (What caused the signal) =====
drivers:
  - contract_id: "some_contract_v1"
    feature: "delta_5d_bps"
    value: -10
    direction: "down"

# ===== DATA REFERENCES (Exact data used) =====
data_refs:
  - contract_id: "some_contract_v1"
    asof_ts: "2026-01-25T21:00:00Z"
    validation_status: "PASS | PASS_WITH_FLAGS | FAIL"
    raw_hash: "sha256:..."
    clean_hash: "sha256:..."
    raw_to_clean_transform_hash: "sha256:..."
    pipeline_version: "v4.0.3"

# ===== CONFIDENCE MODEL =====
methods:
  confidence_model: "weighted_evidence_v1"
  components:
    data_quality: 0.85
    cross_confirmation: 0.60
    historical_stability: 0.65
    model_agreement: 0.70

# ===== INVALIDATION =====
invalidation_state:
  current_status: "valid | flagged | invalid"
  last_checked_at: "2026-02-01T05:30:00Z"

invalidation_conditions:
  - condition: "rates_us10y_real_yield_v1.delta_5d > 0.25"
    action: "flag_signal_invalid | block_publication | require_correction"
    severity: "low | medium | high"

# ===== AUDIT TRAIL =====
audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_YYYYwWW_0001"
  approvals:
    - board: "QR"
      status: "DATA_VALIDATED"
      at: "2026-02-01T05:10:00Z"
    - board: "Strategy"
      status: "SIGNAL_APPROVED"
      at: "2026-02-01T05:20:00Z"
    - board: "Compliance"
      status: "DISCLAIMER_VERIFIED"
      at: "2026-02-01T05:35:00Z"
  edition_id_reference: "adelaide_weekly_YYYYwWW"
```

### 6.3 Evidence Pack Example

```yaml
evidence_pack_id: "ep_2026w05_sig_01"
signal_id: "sig_real_rates_eased_v1"
edition_id: "adelaide_weekly_2026w05"
created_at: "2026-02-01T04:30:00Z"

claim:
  headline: "Inflation-adjusted rates eased"
  summary: "Real-rate pressure softened vs last week."
  horizon: "1-8 weeks"
  severity: "medium"
  confidence: 0.72

disclosures:
  - type: "none_required"
    message: "No lag/proxy/derivation disclosures required. This does not change the educational nature of this commentary."

drivers:
  - contract_id: "rates_us10y_real_yield_v1"
    feature: "delta_5d_bps"
    value: -10
    direction: "down"

data_refs:
  - contract_id: "rates_us10y_real_yield_v1"
    asof_ts: "2026-01-25T21:00:00Z"
    validation_status: "PASS"
    raw_hash: "sha256:abc123..."
    clean_hash: "sha256:def456..."
    raw_to_clean_transform_hash: "sha256:ghi789..."
    pipeline_version: "v4.0.3"

methods:
  confidence_model: "weighted_evidence_v1"
  components:
    data_quality: 0.90
    cross_confirmation: 0.65
    historical_stability: 0.62
    model_agreement: 0.70

invalidation_state:
  current_status: "valid"
  last_checked_at: "2026-02-01T05:30:00Z"

invalidation_conditions:
  - condition: "rates_us10y_real_yield_v1.delta_5d > 0.25"
    action: "flag_signal_invalid"
    severity: "high"

audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_2026w05_0001"
  approvals:
    - {board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z"}
    - {board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z"}
    - {board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z"}
```

---

## 7. Data Storage & Transformation

### 7.1 Storage Architecture

| Layer | Storage | Format | Location |
|-------|---------|--------|----------|
| **Specs** | Markdown | .md | `/docs/v4/` |
| **Truth Contracts** | YAML | .yaml | `/contracts/truth_contracts/` |
| **Evidence Packs** | YAML | .yaml | `/samples/adelaide/weekly/*/evidence_packs/` |
| **Config** | YAML | .yaml | `/config/` |
| **Schemas** | JSON Schema | .json | `/schema/` |
| **Governance** | Markdown | .md | `/governance/` |
| **Raw Data** | Tables | raw.* | Database/files |
| **Clean Data** | Tables | clean.* | Database/files |

### 7.2 Data Transformation Pipeline

```
┌──────────────────────────────────────┐
│         TRUTH CONTRACTS              │ (Defines what/how to collect)
│    /contracts/truth_contracts/*.yaml │
└──────────────────┬───────────────────┘
                   │ Contract rules
                   ▼
┌──────────────────────────────────────┐
│          LAYER 0: INGESTION          │
│     Heartbeat Collector + APIs       │
│     "No contract = no ingest"        │
└──────────────────┬───────────────────┘
                   │ Raw data
                   ▼
┌──────────────────────────────────────┐
│       LAYER 1: RAW VALIDATION        │
│            Gate 1 checks             │
│  Schema, freshness, basic sanity     │
└──────────────────┬───────────────────┘
                   │ Validated raw
                   ▼
┌──────────────────────────────────────┐
│      LAYER 2: CLEAN CANONICAL        │
│    Unit conversion, derivations      │
│    Forward-fill (TradFi only)        │
└──────────────────┬───────────────────┘
                   │ Clean data
                   ▼
┌──────────────────────────────────────┐
│      LAYER 3: CLEAN VALIDATION       │
│            Gate 2 checks             │
│  Reconciliation, stale, zombie       │
└──────────────────┬───────────────────┘
                   │ Validated clean
                   ▼
┌──────────────────────────────────────┐
│     LAYER 4: INTELLIGENCE ENGINE     │
│            Gate 3 checks             │
│  Signals + Event Classes + Evidence  │
└──────────────────┬───────────────────┘
                   │ Signals + Evidence Packs
                   ▼
┌──────────────────────────────────────┐
│    LAYER 5: RENDERING & DISTRIBUTION │
│            Gate 4 checks             │
│  Layer A (B2C) + Layer B (B2B)       │
└──────────────────┬───────────────────┘
                   │ Published edition
                   ▼
┌──────────────────────────────────────┐
│     LAYER 6: TELEMETRY & TASKS       │
│  Publication eligibility (arbiter)   │
│  Dashboards, alerts, MTTR tracking   │
└──────────────────────────────────────┘
```

### 7.3 Timestamp Requirements

**Every stored observation must include:**
```yaml
asof_ts: "2026-01-25T21:00:00Z"       # When observation refers to
retrieved_at_ts: "2026-01-26T04:00:00Z"  # When we fetched it
```

**Why both?**
- `asof_ts` = economic period (what the data represents)
- `retrieved_at_ts` = reproducibility (what the system saw at publish time)

**Vintage/Revision Handling (Tier 1 Macro):**
- If source supports revisions, store revision window fields
- Evidence Packs preserve what was seen at `retrieved_at_ts`
- Even if upstream revises later, the receipt is immutable

---

## 8. Event Class System (Triggers)

### 8.1 Event States

| State | Meaning | Eligibility |
|-------|---------|-------------|
| **WATCH** | Conditions forming; not confirmed | Internal triage only |
| **TRIGGERED** | Conditions met with persistence | Internal + sometimes public |
| **RESOLVED** | Conditions reverted | Important to communicate |

### 8.2 Global Rules

**Persistence Rule (Anti-Noise):**
```yaml
# Event becomes TRIGGERED only if condition met in 2 consecutive checks
persistence_checks: 2
```

**Minimum Resolution Requirement:**
```yaml
# Cannot TRIGGER from monthly data alone
minimum_resolution_requirement:
  requires_at_least_one_daily_witness: true
```

**Confidence Input:**
- Event confidence informed by `trust_score_v1` for referenced contracts
- Low trust_score → cap event confidence → stronger caveats in Layer A

### 8.3 Event Schema

```yaml
event:
  id: "EC-07"
  name: "Japan Carry Stress"
  state: "WATCH | TRIGGERED | RESOLVED"
  severity: "low | medium | high | critical"
  horizon: "hours-days | 1-8 weeks | 1-3 months"
  confidence:
    score: 0.72
    label: "low | medium | high"
  
  required_contracts:
    - "fx_usdjpy_spot_v1"
    - "rates_jp10y_yield_proxy_daily_v1"
  
  minimum_resolution_requirement:
    requires_at_least_one_daily_witness: true
  
  trigger:
    description: "Sharp USD/JPY move AND Japan yield proxy rises"
    rule: "fx_usdjpy_spot_v1.delta_5d_pct > 3 AND rates_jp10y_yield_proxy_daily_v1.delta_5d > 0.10"
    persistence_checks: 2
  
  invalidation:
    - rule: "fx_usdjpy_spot_v1.delta_5d_pct < 1 AND rates_jp10y_yield_proxy_daily_v1.delta_5d < 0.05"
      action: "set_resolved"
  
  disclosures:
    - "proxy"
  
  routing:
    internal: ["CTO Board", "QR Board", "Strategy Board"]
    public_allowed: true
  
  layer_a_phrasing:
    watch: "Yen-related indicators are moving more than usual."
    triggered: "Yen and Japan yield indicators moved sharply together."
    resolved: "Japan-related stress indicators have stabilized."
```

### 8.4 The 11 Event Classes

| EC | Name | Severity | Horizon | Required Contracts | Public |
|----|------|----------|---------|-------------------|--------|
| **EC-01** | Liquidity Tightening | High | 1-8w | USD, rates, credit | No |
| **EC-02** | Risk-Off Cascade | High | hours-8w | VIX, credit | **Yes** |
| **EC-03** | Liquidity Easing | Medium | 1-8w | rates, stress | No |
| **EC-04** | Stablecoin Depeg | **Critical** | hours-days | depeg_events | **Yes** |
| **EC-05** | Crypto Leverage Unwind | High | hours-8w | funding, OI | No |
| **EC-06** | Capital Rotation | Medium | 1-3m | sector witnesses | No |
| **EC-07** | Japan Carry Stress | High | hours-8w | USD/JPY, JGB10 (Phase 0.5) | No |
| **EC-08** | Credit Stress Widening | High | 1-8w to 1-3m | credit spreads | No |
| **EC-09** | DeFi Baseline Deterioration | Medium | 1-3m | TVL, yield benchmark | No |
| **EC-10** | RWA Flow Shock | Medium | 1-8w | RWA TVL/flows | No |
| **EC-11** | Commodity Inflation Pulse | Medium | 1-3m | WTI, copper (Phase 0.5) | No |

### 8.5 Event Class Details

#### EC-01: Liquidity Tightening (Macro Gravity Up)
```yaml
trigger:
  rule: "rates_rising_2w AND usd_up_2w AND credit_widening > threshold"
invalidation:
  rule: "credit_spreads < threshold OR rates_revert"
layer_a_phrasing:
  triggered: "Borrowing pressure and stress indicators strengthened together; historically this can coincide with reduced risk appetite, but conditions can change quickly."
```

#### EC-04: Stablecoin Depeg Event (Critical)
```yaml
severity: "critical"
required_contracts: ["stablecoin_depeg_events_v1"]
trigger:
  rule: "confirmed depeg event per contract rules"
layer_a_phrasing:
  triggered: "A stablecoin stress event was detected. These can spread quickly through crypto liquidity."
public_alerts: "Allowed (rare) under Doc 17 policy"
```

#### EC-07: Japan Carry Stress (Phase 0.5 Required)
```yaml
required_contracts:
  - "fx_usdjpy_spot_v1" (daily)
  - "rates_jp10y_yield_proxy_daily_v1" (daily proxy)
minimum_resolution_requirement:
  requires_at_least_one_daily_witness: true
  # If only monthly JGB exists → WATCH only, cannot TRIGGER
trigger:
  rule: "sharp USD/JPY move AND Japan yield proxy rises (persisted)"
layer_a_phrasing:
  watch: "Yen-related indicators are moving more than usual."
  triggered: "Yen and Japan yield indicators moved sharply together. Historically, this has sometimes coincided with broader liquidity stress."
```

### 8.6 Routing Policy

**Internal Routing:** Always allowed (tasks/triage)

**Public Alerts:** Only for high/critical safety classes under strict limits:
- EC-04 (Stablecoin Depeg)
- EC-02 (Risk-Off Cascade)

**Public Alert Limits:**
```yaml
max_per_month: 2
default_channel: "web canonical first, then Telegram/email with link"
```

---

## 9. Telemetry Dashboard & Publication Eligibility

### 9.1 Publication Eligibility States

| State | Color | Meaning | Action |
|-------|-------|---------|--------|
| **Eligible** | GREEN | Publish permitted | Proceed |
| **Eligible with flags** | YELLOW | Requires audited override | Default blocked |
| **Not eligible** | RED | Publish blocked | **No exceptions** (unless break-glass) |

### 9.2 GREEN Eligibility Requirements

An edition is **GREEN** only if **ALL** are true:

1. Gate 4 for the edition == **PASS**
2. 3-7 signals selected
3. All signals have Evidence Packs (schema-valid)
4. Evidence Packs all have `invalidation_state.current_status == valid`
5. All referenced contracts meet **publication SLA** at last check
6. No referenced contracts are FAIL at Gate 1/2
7. No unresolved **high or critical reconciliation diffs** on referenced contracts (last 7 days)
8. No open **critical/high tasks** affecting referenced contracts
9. All mandatory disclaimers present for the channel + jurisdiction(s)

**If ANY fail → RED.**

**If only PASS_WITH_FLAGS issues exist but fully disclosed → YELLOW.**

### 9.3 Dashboard Views

#### View A: Trust Spine Freshness (Per Contract)

| contract_id | risk_tier | last_update_utc | age | internal_sla_status | publication_sla_status | time_to_breach | validation_status | reconciliation_status |
|-------------|-----------|-----------------|-----|---------------------|------------------------|----------------|-------------------|----------------------|
| rates_us10y_real_yield_v1 | critical | 2026-01-25T21:00Z | 8h | ✅ | ✅ | T-40h | PASS | PASS |
| stablecoin_depeg_events_v1 | critical | 2026-01-26T11:45Z | 15m | ✅ | ✅ | T-3h45m | PASS | n/a |

**Color Rules:**
- Green: within SLA
- Yellow: between SLA and 2×SLA (or time_to_breach < 6h)
- Red: > 2×SLA or publication SLA breached

#### View B: Gate Health Overview (Last 7d & 30d)

| gate | total_runs | PASS % | PASS_WITH_FLAGS % | FAIL % | top_failure_reason | MTTR | trend |
|------|------------|--------|-------------------|--------|-------------------|------|-------|
| Gate 1 | 1,234 | 98.5% | 1.2% | 0.3% | Schema mismatch | 2.1h | → |
| Gate 2 | 1,200 | 97.2% | 2.5% | 0.3% | Reconciliation breach | 4.2h | ↗ |
| Gate 3 | 45 | 95.6% | 4.4% | 0.0% | - | - | → |
| Gate 4 | 40 | 100% | 0.0% | 0.0% | - | - | → |

#### View C: Reconciliation Diffs (Vendor Drift Monitor)

| contract_id | risk_tier | canonical_vs_fallback_diff | tolerance | status | resolved | qr_override |
|-------------|-----------|---------------------------|-----------|--------|----------|-------------|
| credit_hy_ig_spread_proxy_v1 | high | 0.03 | 0.01 | BREACH | No | Pending |

**Rule:** Any high/critical diff unresolved for referenced contracts → blocks eligibility.

#### View D: Evidence Pack Monitor

| evidence_pack_id | signal_id | edition_id | invalidation_status | last_checked | triggered_conditions |
|------------------|-----------|------------|---------------------|--------------|---------------------|
| ep_2026w05_sig_01 | sig_real_rates_eased_v1 | adelaide_weekly_2026w05 | valid | 2026-02-01T05:30Z | None |

#### View E: Edition Readiness (Pre-flight Checklist)

```yaml
edition_id: "adelaide_weekly_2026w05"
eligibility: "GREEN"
blocking_issues: []

proposed_signals:
  - signal_id: "sig_real_rates_eased_v1"
    headline: "Inflation-adjusted rates eased"
    evidence_pack_id: "ep_2026w05_sig_01"
    invalidation_status: "valid"
    freshness_ok: true

dependency_map:
  sig_real_rates_eased_v1:
    - contract_id: "rates_us10y_real_yield_v1"
      status: "PASS"
      sla_ok: true
```

### 9.4 Alerting & Task Creation

**Severity Routing:**
| Severity | Response | Routing |
|----------|----------|---------|
| Critical | Immediate task | CTO Board (priority=critical) |
| High | Business-day response | Owning board (priority=high) |
| Medium/Low | Batched daily summary | Owning board |

**Alert Triggers:**
- Publication SLA breach on any critical contract
- Gate 1/2 FAIL spike (PASS < 95% in last 24h for critical)
- Reconciliation breach on high/critical contracts
- Evidence pack invalidation for signal in next edition
- Eligibility changes from GREEN → YELLOW/RED

---

## 10. Trust Score v1

### 10.1 Purpose

Trust Score is a **single versioned KPI** that summarizes Trust Spine health **without replacing hard blockers**.

**Critical Rule:** If you try to use Trust Score to "greenwash" a RED system, the correct response is: **No.**

### 10.2 Components

| Component | Code | Weight | What It Measures |
|-----------|------|--------|------------------|
| Data Quality | DQ | 0.30 | Gate PASS rates, validation status |
| Cross-Confirmation | CC | 0.25 | Multi-source agreement |
| Reconciliation/SLA | RS | 0.25 | Freshness vs SLA, reconciliation status |
| Operational Health | OPS | 0.20 | Open tasks, pending Gate 4 findings |

### 10.3 Formula

```
trust_score = (0.30 × DQ) + (0.25 × CC) + (0.25 × RS) + (0.20 × OPS) - Σ(penalties)
```

### 10.4 Penalty Table

| Penalty | Amount | Trigger |
|---------|--------|---------|
| `open_critical_task` | -0.15 | Any critical task open |
| `open_high_task` | -0.07 | Any high task open |
| `freshness_near_breach` | -0.05 | Contract < 6h to publication SLA |
| `reconciliation_breach_high` | -0.10 | High/critical recon breach |
| `pending_gate4_findings` | -0.08 | Gate 4 has PASS_WITH_FLAGS |

### 10.5 Trust Score Output

```json
{
  "trust_score_v1": {
    "scope": "signal",
    "aggregate": 0.72,
    "components": {
      "dq": 0.85,
      "cc": 0.60,
      "rs": 0.80,
      "ops": 0.65
    },
    "penalties": [
      {
        "type": "freshness_near_breach",
        "target": "credit_hy_ig_spread_proxy_v1",
        "amount": 0.05,
        "explanation": "Contract is within 6h of publication SLA breach."
      }
    ],
    "version": "1.0.0",
    "calculated_at": "2026-02-01T05:30:00Z"
  }
}
```

### 10.6 Policy Hooks (Optional)

```yaml
# If trust_score < 0.60, add mandatory caveat
if trust_score < 0.60:
  layer_a_caveat: "This insight has lower overall system confidence due to [top_penalty]."
  layer_b_flag: "QR review required"
```

---

## 11. Adelaide Weekly Output Contract

### 11.1 Edition Structure

**Schedule:**
- Cadence: Weekly (Sunday 06:00 UTC default)
- Edition ID format: `adelaide_weekly_YYYYwWW`
- Version format: `major.minor.patch`

### 11.2 Hard Publication Blockers

An edition may be published **only if ALL** are true:

1. Gate 4 status == **PASS**
2. Signal count is **3-7**
3. Every signal has a valid **Evidence Pack**
4. Every Evidence Pack has `invalidation_state.current_status == "valid"`
5. Every referenced contract satisfies **publication_sla**
6. No referenced contract has `validation_status == FAIL`
7. No unresolved **high or critical reconciliation diffs** (last 7d)
8. No prohibited language or recommendation-likeness classifier FAIL
9. Mandatory disclaimers present per channel + jurisdiction

**If ANY fail → BLOCK PUBLICATION.**

### 11.3 Layer A vs Layer B

#### Layer A (B2C) — 500-900 words

**Goal:** Calm, plain-language, educational commentary.

**Must Include:**
- What Changed (short narrative)
- Market Snapshot (plain-language table)
- 3-7 Signals (≤120 words each)
- What to Watch Next (short bullets)
- Top-level Disclosures (if any)
- General Caveats
- Short disclaimer (always)

**Style:** "Explain like a smart grandmother." No jargon, no tickers, no trading talk.

#### Layer B (B2B Appendix) — Full Audit

**Must Include:**
- Signal Index table (severity/horizon/confidence/evidence_pack_id/invalidation_status)
- Contract Freshness table (contract_id, asof_ts, SLA compliance, gate statuses)
- Methodology Notes (confidence model, key rules)
- Overrides & Approvals Summary
- Evidence Packs (full YAML or canonical links)
- Long disclaimer (web canonical)

### 11.4 Multi-Channel Formatting

| Channel | Layer A | Layer B | Disclaimer |
|---------|---------|---------|------------|
| **Web (Canonical)** | Full | Full | Long |
| **Email/Substack** | Full | Link to web | Short + link |
| **Telegram** | Summary | Link to web | Minimal + pinned |

### 11.5 Disclaimers

**Short (All Channels):**
> Educational market commentary. Not financial, legal, or tax advice. No recommendation to buy or sell any asset. Investing involves risk.

**Long (Web + Layer B):**
> diBoaS provides educational market intelligence and commentary for general informational purposes only. This is not personalized financial advice and is not a recommendation to buy, sell, or hold any asset. Investing involves risk, including loss of principal. Cryptoassets and DeFi carry additional risks (volatility, liquidity, smart contract risk, and counterparty risk). Any scenarios or historical references are hypothetical, based on assumptions, and not guarantees. Past performance is not indicative of future results.

---

## 12. Break-Glass Protocol

### 12.1 When Allowed

Break-glass **MAY** be used only if:
1. Edition is RED due to SLA breach or reconciliation delay
2. AND there are no Gate 4 prohibited language violations
3. AND compliance approves disclosure language

### 12.2 When Forbidden

Break-glass is **FORBIDDEN** if:
1. Gate 4 has **any Rule Group A** prohibited phrase violations (no exceptions)
2. OR recommendation-likeness classifier **FAIL**

### 12.3 Requirements

```yaml
break_glass:
  sign_off:
    - "CTO"
    - "Compliance"
  forced_actions:
    - edition_version_bump: true
    - public_note_in_header: true
  postmortem_required_within: "72h"
```

---

## 13. Key Formulas & Calculations

### 13.1 Trust Score

```
trust_score = (0.30 × DQ) + (0.25 × CC) + (0.25 × RS) + (0.20 × OPS) - Σ(penalties)
```

### 13.2 Confidence Components

```python
# Data Quality (DQ)
dq = gate_pass_rate * validation_status_weight

# Cross-Confirmation (CC)
cc = correlation_with_fallback * source_agreement_factor

# Reconciliation/SLA (RS)
rs = (1 - sla_breach_proximity) * reconciliation_pass_rate

# Operational Health (OPS)
ops = 1 - (critical_tasks * 0.15 + high_tasks * 0.07)
```

### 13.3 Publication Eligibility

```python
def is_eligible(edition):
    checks = [
        edition.gate4_status == "PASS",
        3 <= len(edition.signals) <= 7,
        all(s.evidence_pack.is_valid() for s in edition.signals),
        all(s.evidence_pack.invalidation_state == "valid" for s in edition.signals),
        all(c.meets_publication_sla() for c in edition.referenced_contracts),
        all(c.validation_status != "FAIL" for c in edition.referenced_contracts),
        not any(c.has_unresolved_high_critical_recon_diff() for c in edition.referenced_contracts),
        not any(t.is_critical_or_high() for t in edition.open_tasks),
        edition.has_all_disclaimers(),
    ]
    return all(checks)
```

### 13.4 Event Trigger Evaluation

```python
def evaluate_event(event_class, data):
    # Check minimum resolution requirement
    if not event_class.has_required_witnesses(data):
        return EventState.WATCH
    
    # Evaluate trigger condition
    if not event_class.trigger_condition(data):
        return EventState.WATCH
    
    # Check persistence (2 consecutive checks)
    if not persistence_manager.is_persisted(event_class.id):
        persistence_manager.record(event_class.id)
        return EventState.WATCH
    
    # Trigger confirmed
    return EventState.TRIGGERED
```

### 13.5 Classifier Score

```python
def recommendation_likeness_score(text):
    features = {
        'imperative_verbs': count_imperative_verbs(text) * 0.15,
        'second_person': count_second_person(text) * 0.12,
        'certainty_language': count_certainty_words(text) * 0.18,
        'action_framing': count_action_phrases(text) * 0.14,
        'numeric_prescriptions': count_allocations(text) * 0.20,
    }
    return sum(features.values())

# Thresholds
if score < 0.30:
    return "PASS"
elif score < 0.45:
    return "PASS_WITH_FLAGS"
else:
    return "FAIL"
```

---

## 14. v3 vs v4 Comparison

| Aspect | v3 | v4 |
|--------|----|----|
| **Core Philosophy** | Smart analytics | Provable intelligence |
| **Publication Control** | Manual pipeline execution | Telemetry-governed (GREEN/YELLOW/RED) |
| **Data Contracts** | Implicit schemas | Explicit Truth Contracts (YAML) |
| **Audit Trail** | Limited logging | Full Evidence Packs with hashes |
| **Forward-Fill** | Used with proxies | Crypto: BANNED; TradFi: allowed with disclosure |
| **Compliance Gate** | Gate 4 exists | Gate 4 is deterministic + classifier |
| **Signal Limits** | Free-form | 3-7 max, each needs Evidence Pack |
| **Invalidation** | Ad-hoc | Machine-readable conditions per signal |
| **Regime Detection** | 6 implicit regimes | 11 explicit Event Classes with triggers |
| **User Output** | Adelaide personas | Layer A (B2C) + Layer B (B2B) split |
| **System Health** | Advisory | **Arbiter** (RED = blocked) |
| **Stale Detection** | Basic freshness | Ghost feed + zombie API detection |
| **Global Coverage** | US-centric | Phase 0.5 adds Japan, commodities, Brazil |
| **Trust Metric** | None | Trust Score v1 (informational, not override) |

---

## 15. Implementation Checklist

### Phase 0 Exit Criteria

Phase 0 is complete when:

- [ ] 100% Phase 0 contracts have Truth Contracts in repo
- [ ] CI validates all contracts against JSON Schema
- [ ] Telemetry shows:
  - [ ] Gate PASS ≥ 95% for last 7 days
  - [ ] Zero open critical tasks older than 24h
  - [ ] Zero unresolved high/critical reconciliation diffs older than 24h
- [ ] One full weekly edition produced end-to-end with:
  - [ ] GREEN eligibility at send time
  - [ ] Valid Evidence Packs for every signal
  - [ ] Gate 4 PASS

### Minimal "Starter Commit" Checklist

- [ ] `/docs/v4/00_INDEX.md` fully current
- [ ] `/docs/v4/spec/` containing enforceable spec set
- [ ] `/docs/v4/contracts/` containing Phase 0 registries
- [ ] Phase 0 Truth Contracts in `/contracts/truth_contracts/phase0/`
- [ ] Gate 4 configs in `/config/gate4/`
- [ ] Trust Score configs in `/config/trust_score/`
- [ ] Telemetry configs in `/config/telemetry/`
- [ ] At least one sample weekly edition with:
  - [ ] Edition markdown
  - [ ] Complete Evidence Packs
  - [ ] Telemetry snapshot
  - [ ] Gate 4 findings

---

## 16. Summary

diBoaS Analytics v4 represents a fundamental shift from **"analytics that work"** to **"intelligence with receipts."**

### Key Innovations

1. **Truth Contracts:** Every data feed has a formal specification before ingestion
2. **Evidence Packs:** Every published signal has a cryptographic receipt
3. **Dual-SLA System:** Separates pipeline health from publication readiness
4. **11 Event Classes:** Deterministic regime detection with persistence rules
5. **Gate 4 Firewall:** Deterministic blocklist + ML classifier for compliance
6. **Telemetry Arbiter:** RED = blocked, no exceptions (unless break-glass)
7. **Trust Score:** Informational KPI that never overrides hard blockers
8. **Layer A/B Split:** Same truth, different packaging for B2C vs B2B
9. **Phase 0.5:** Global macro extension without breaking Phase 0

### The Product Promise

diBoaS delivers **"economic weather"** and **regime awareness** with **receipts**:
- **What changed**
- **Why it matters** (in plain language)
- **What to watch next**
- **What would invalidate this**
- **How confident the system is, and why**

Same truth spine, different packaging for different audiences.

### Non-Negotiable Rules

1. **No contract = no ingest**
2. **No evidence pack = no publish**
3. **Gate 4 is mandatory**
4. **Telemetry is the arbiter**

If the system is unhealthy, publication is blocked. Full stop.

---

*Document Version: 1.0.0*
*Last Updated: 2026-01-30*
*Status: Complete Technical Specification*
