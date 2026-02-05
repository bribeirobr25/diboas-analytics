# diBoaS Analytics - Version Comparison Matrix

## Executive Summary

| Aspect | v3 | v4 | Macro OS + Mine Detector |
|--------|----|----|--------------------------|
| **Core Philosophy** | "Smart Analytics" | "Provable Intelligence" | "Regime + Landmine Detection" |
| **Primary Question** | "How did strategies perform?" | "Can we prove what we publish?" | "Is it safe to invest?" |
| **Target Output** | Adelaide Newsletter | Audit-ready Edition | Risk Scores + Regime |
| **Operational Status** | ✅ Production | 📋 Specification | 📋 Specification |

---

## 1. Technology & Architecture Comparison

### 1.1 Core Technologies

| Component | v3 | v4 | Macro OS + Mine Detector |
|-----------|----|----|--------------------------|
| **Language** | Python 3.10+ | YAML/JSON specs (implementation agnostic) | Python 3.10+ |
| **Data Processing** | pandas 2.0+, numpy 1.24+ | Spec-defined transforms | dataclasses, Enum, typing |
| **Statistical Engine** | scipy 1.10+ (distributions) | Schema-validated | math (stdlib), softmax |
| **ML Components** | scikit-learn (Isolation Forest) | N/A (spec layer) | Heuristic expert system (planned: RF/XGBoost) |
| **Configuration** | JSON, YAML, python-dotenv | YAML contracts + JSON schemas | Dict-based configs |
| **Hashing/Integrity** | N/A | SHA-256 (Evidence Packs) | File hash verification |
| **Time Handling** | datetime | ISO 8601 strict | UTC-only (enforced) |
| **Testing** | pytest 7.0+ | JSON Schema CI validation | Calibration tracking |

### 1.2 Architectural Pattern

| Aspect | v3 | v4 | Macro OS + Mine Detector |
|--------|----|----|--------------------------|
| **Layers** | 5 layers | 6 layers + telemetry | Dual-system (2 independent) |
| **Pattern Name** | Pipeline Architecture | Zero-Trust Architecture | State Machine + Scoring Engine |
| **Data Flow** | Sequential (Researcher → Presenter) | Contract-gated (blocked by default) | Parallel (Macro feeds Mine Detector) |
| **Blocking Behavior** | Advisory (warnings) | Mandatory (RED = blocked) | Hard block at score ≥86 |

### 1.3 Layer Comparison

| Layer | v3 | v4 | Macro OS | Mine Detector |
|-------|----|----|----------|---------------|
| **L0** | - | Ingestion (contract-gated) | - | - |
| **L1** | Researcher (data collection) | Raw Validation (Gate 1) | Data Ingestion | Data Collection |
| **L2** | Validator (Gate 1+2) | Clean Canonical (transforms) | Change Detection | Staleness Check |
| **L3** | Analyst (engines) | Clean Validation (Gate 2) | Pattern Recognition | Category Scoring |
| **L4** | Operator (triggers) | Intelligence (Gate 3) | Validation/Cross-check | Regime Adjustment |
| **L5** | Presenter (Adelaide) | Rendering (Gate 4) | Regime Output | Composite Score |
| **L6** | - | Telemetry (arbiter) | Transition Matrix | Brokerage Integration |

### 1.4 Design Patterns Used

| Pattern | v3 | v4 | Macro OS + Mine Detector |
|---------|----|----|--------------------------|
| **Registry** | ✅ (collectors, engines, triggers) | ✅ (contracts, validators) | ✅ (data sources, platforms) |
| **Strategy** | ✅ (anomaly detectors) | ✅ (validators) | ✅ (risk assessors) |
| **Template Method** | ✅ (base classes) | ✅ (contract templates) | - |
| **Facade** | ✅ (AdelaideGenerator) | - | - |
| **State** | - | - | ✅ (RegimeClassifierState) |
| **Factory** | - | - | ✅ (BrokerAdapter) |
| **Observer** | - | ✅ (telemetry) | ✅ (SystemHealthMonitor) |

---

## 2. Data Collection Comparison

### 2.1 Data Sources Overview

| Source Type | v3 | v4 | Macro OS | Mine Detector |
|-------------|----|----|----------|---------------|
| **FRED (macro)** | ✅ (yields, spreads, M2) | ✅ (7 contracts) | ✅ (multiple categories) | ✅ (credit spreads) |
| **Yahoo Finance** | ✅ (equities, crypto, VIX) | ✅ (proxies) | ✅ (Core Dashboard) | ✅ (price data) |
| **DeFiLlama** | ✅ (APYs, TVL) | ✅ (2 contracts) | - | ✅ (protocol TVL) |
| **CoinGecko** | ✅ (backup prices) | - | - | ✅ (crypto prices) |
| **Bloomberg/ICE** | - | - | ✅ (MOVE Index, CDX) | - |
| **CME** | - | - | ✅ (COT positioning) | - |
| **Social Media** | - | - | - | ✅ (Twitter, Reddit, StockTwits, Discord, Telegram) |
| **Brokerage APIs** | - | - | - | ✅ (IB, TD, Schwab, etc.) |
| **Japan (BoJ, OECD)** | - | ✅ (Phase 0.5) | ✅ (Global Anchors) | - |
| **Brazil (BCB)** | - | ✅ (Phase 0.5) | - | - |

### 2.2 Data Volume

| Metric | v3 | v4 | Macro OS | Mine Detector |
|--------|----|----|----------|---------------|
| **Indicators** | ~30 | 23 core + 9 extension | 150+ across 31 categories | 9 categories × N tickers |
| **Protocols Tracked** | 6 DeFi | 2 DeFi contracts | - | Variable (per position) |
| **Strategies** | 10 | N/A (not strategy-focused) | - | - |
| **Contracts/Sources** | N/A | 32 Truth Contracts | ~50 derived indicators | 17 data source types |

### 2.3 Update Frequency

| Data Type | v3 | v4 | Macro OS | Mine Detector |
|-----------|----|----|----------|---------------|
| **Crypto prices** | Real-time available | Hourly (contract) | Daily (Core Dashboard) | 15 seconds |
| **Macro/rates** | Daily | EOD (contract) | Daily | 60 min |
| **DeFi TVL/APY** | 15 min available | Daily (contract) | - | 60 min |
| **Stablecoin depeg** | - | **15 min (critical)** | - | - |
| **Social sentiment** | - | - | - | 15-60 min (platform-dependent) |
| **Short interest** | - | - | - | Daily |
| **Portfolio sync** | - | - | - | 5 min |

### 2.4 Staleness Handling

| Aspect | v3 | v4 | Macro OS | Mine Detector |
|--------|----|----|----------|---------------|
| **Staleness Policy** | Warning only | Dual SLA (internal + publication) | Change detection flags | Staleness penalty (points) |
| **Forward-Fill** | Allowed | **Crypto: FORBIDDEN** / TradFi: Allowed with disclosure | N/A | N/A |
| **Block on Stale** | No | Yes (publication blocked) | Pattern confidence reduced | Score penalty + critical block |
| **Ghost Detection** | No | G2-STALE-VALUE-001 | Acceleration/divergence checks | fetch_ts vs origin_ts distinction |

---

## 3. Monitoring & Validation Comparison

### 3.1 Validation Gates

| Gate | v3 | v4 | Macro OS | Mine Detector |
|------|----|----|----------|---------------|
| **Schema Validation** | Gate 1 (columns, types) | Gate 1 (JSON Schema) | N/A | DataSynchronizer |
| **Bounds Checking** | Gate 1 (value ranges) | Gate 1 (sanity) | Z-score thresholds | Score capping (0-100) |
| **Analytics Quality** | Gate 2 (CV-01 to CV-07) | Gate 2 (reconciliation, derivation) | Pattern validation rules | Category score validation |
| **Intelligence Quality** | - | Gate 3 (signal schema, confidence) | 7 canonical patterns | 9 risk categories |
| **Compliance** | Gate 4 (CLO rules) | Gate 4 (deterministic firewall) | - | - |

### 3.2 Validation Rules

| Rule Type | v3 | v4 | Macro OS | Mine Detector |
|-----------|----|----|----------|---------------|
| **Portfolio value** | CV-01: Never negative | Gate 1 sanity | - | Score ≥ 0 |
| **Drawdown** | CV-02: 0-100% | Schema validation | - | Score ≤ 100 |
| **Return calculation** | CV-05: Formula match | Gate 2 derivation | - | Weight sum = 1.0 |
| **Cross-validation** | - | Reconciliation (canonical vs fallback) | Contradiction checks | Category coverage ≥ 40% |
| **Freshness** | Warning only | Publication SLA (block) | Δ1d/Δ5d/Δ20d | Staleness threshold per source |

### 3.3 Monitoring Outputs

| Output | v3 | v4 | Macro OS | Mine Detector |
|--------|----|----|----------|---------------|
| **Health Score** | Protocol health (0-100) | Telemetry status (GREEN/YELLOW/RED) | Pattern confidence (0-100%) | Composite score (0-100) |
| **Alerts** | Protocol alerts (L1-L4) | Tasks (priority-based) | RED FLAG escalation | Score-based (warn/confirm/block) |
| **Dashboard** | ProtocolHealth output | Telemetry dashboard | Core Dashboard (14 vitals) | Risk assessment dashboard |
| **Audit Trail** | Logging | Evidence Packs (SHA-256) | - | Calibration tracking |

---

## 4. Frameworks & Methodologies Comparison

### 4.1 Core Methodologies

| Methodology | v3 | v4 | Macro OS | Mine Detector |
|-------------|----|----|----------|---------------|
| **Backtesting** | ✅ Battle Test (DCA simulation) | - | - | - |
| **Forward Simulation** | ✅ Monte Carlo (regime-switching) | - | - | - |
| **Anomaly Detection** | ✅ Z-score + Isolation Forest | - | Z-score + percentile | - |
| **Regime Classification** | Markov transitions | - | 7 canonical patterns | RISK_ON/RISK_OFF/TRANSITION |
| **Risk Scoring** | - | Trust Score v1 | - | 9-category weighted composite |
| **Compliance** | Gate 4 (CLO rules) | Gate 4 (deterministic firewall) | - | - |

### 4.2 Statistical Methods

| Method | v3 | v4 | Macro OS | Mine Detector |
|--------|----|----|----------|---------------|
| **Distributions** | Student-t (df=4) for fat tails | - | - | - |
| **Normalization** | - | - | Z-score, percentile | Softmax (regime probabilities) |
| **Correlation** | Crypto correlation matrix | - | VIX/HY divergence tracking | - |
| **Aggregation** | Weighted returns | Composite derivation | 4-quadrant model | max_plus_sqrt penalty combination |
| **Hysteresis** | Trigger cooldowns | - | Transition matrix | Regime tenure bias (0-15%) |

### 4.3 Key Formulas

| Formula | v3 | v4 | Macro OS | Mine Detector |
|---------|----|----|----------|---------------|
| **Daily Return** | `Σ(weight × (price_return + apy/365))` | Derivation spec | - | - |
| **JLP Return** | `0.45×SOL + 0.27×ETH + 0.27×BTC + fee_apy/365` | - | - | - |
| **Risk Score** | - | Trust Score weighted sum | - | `Σ(category_score × weight) + overlay + staleness` |
| **Percentile** | - | - | `rank_in_window / window_size × 100` | - |
| **Z-score** | `(value - mean) / std` | - | `(value - mean_252d) / std_252d` | - |
| **Overlay Points** | - | - | - | `notches × 10` |
| **Softmax** | - | - | - | `exp(score/T) / Σexp(scores/T)` |

---

## 5. Triggers & Alerts Comparison

### 5.1 Trigger Types

| Trigger Type | v3 | v4 | Macro OS | Mine Detector |
|--------------|----|----|----------|---------------|
| **Protocol health** | ✅ TVL drops, APY spikes | - | - | Protocol TVL for solvency |
| **Market moves** | ✅ BTC/ETH/SOL drops | Event classes | Core Dashboard vitals | Momentum risk category |
| **Macro stress** | ✅ VIX spikes, credit widening | Event classes | RED FLAG pairs | - |
| **Positioning** | - | Event classes | Crowding/systematic flows | Crowding risk category |
| **Social anomalies** | - | - | - | ✅ Sentiment spikes |
| **Calendar events** | - | Event classes | - | ✅ Earnings, FDA, unlocks |
| **Wallet movements** | ✅ Estate ($10M+), whale ($25M+) | Event classes | - | - |

### 5.2 Alert Severity Levels

| Level | v3 | v4 | Macro OS | Mine Detector |
|-------|----|----|----------|---------------|
| **L1/Low** | Info | Info | OK | 0-25 (LOW) |
| **L2/Medium** | Warning | Medium | Watch | 26-50 (MODERATE) |
| **L3/High** | Alert | High | Alert | 51-70 (ELEVATED) |
| **L4/Critical** | Crisis | Critical | RED FLAG | 71-85 (HIGH) |
| **L5/Block** | - | - | - | **86-100 (CRITICAL - HARD BLOCK)** |

### 5.3 Trigger Thresholds Examples

| Indicator | v3 | v4 | Macro OS | Mine Detector |
|-----------|----|----|----------|---------------|
| **VIX** | L2: >30, L3: >40 | Event class threshold | z-score >2, percentile >95% | N/A (uses regime) |
| **BTC drop** | L3: -10%, L4: -20% | Event class | N/A | Momentum risk score |
| **Credit spread** | Warning: >150bp | Event class | Paired with VIX for RED FLAG | Credit spreads for solvency |
| **Short interest** | - | - | - | >25% = CRITICAL |
| **Score threshold** | - | - | - | ≥70 = confirm, ≥86 = block |

---

## 6. User Value & Benefits Comparison

### 6.1 Primary User Benefits

| Benefit | v3 | v4 | Macro OS | Mine Detector |
|---------|----|----|----------|---------------|
| **Risk-appropriate guidance** | ✅ Strategy matching | ✅ Tiered content | ✅ Regime awareness | ✅ Position-level risk |
| **Early warning** | ✅ Protocol alerts | ✅ Event detection | ✅ Pattern recognition | ✅ Landmine detection |
| **Educational value** | ✅ Adelaide templates | ✅ Plain-language signals | ✅ "Why" explanations | ✅ Dominant risk identification |
| **Historical context** | ✅ Battle Test results | ✅ Evidence Packs | ✅ Percentile rankings | ✅ Calibration metrics |
| **Emotional guardrails** | ✅ Persona-adapted messaging | ✅ Confidence levels | - | ✅ Hard blocks prevent panic trades |
| **Audit trail** | Limited logging | ✅ Full cryptographic | - | ✅ Calibration outcomes |
| **Regulatory compliance** | ✅ Gate 4 disclaimers | ✅ Gate 4 firewall | - | - |

### 6.2 User Segments Served

| User Segment | v3 | v4 | Macro OS | Mine Detector |
|--------------|----|----|----------|---------------|
| **Ana (conservative)** | ✅ Persona-adapted | ✅ Tier A | ✅ Weather report | ✅ LOW threshold guidance |
| **Maria (balanced)** | ✅ Persona-adapted | ✅ Tier B | ✅ Driver explanations | ✅ MODERATE/ELEVATED guidance |
| **Felipe (aggressive)** | ✅ Persona-adapted | ✅ Tier C | ✅ Full pattern details | ✅ HIGH threshold guidance |
| **Yield Hunter** | ✅ Strategy comparison | ✅ Evidence Packs | - | ✅ DeFi/Web3 overlay |
| **B2B Client** | ✅ Multi-tenant | ✅ Audit-ready | ✅ Regime classification | ✅ Portfolio risk scans |

### 6.3 Key Value Propositions

| Value Proposition | v3 | v4 | Macro OS | Mine Detector |
|-------------------|----|----|----------|---------------|
| **"How did my strategy do?"** | ✅ Battle Test | - | - | - |
| **"What might happen?"** | ✅ Monte Carlo | - | ✅ Transition matrix | - |
| **"Can I trust this data?"** | - | ✅ Evidence Packs | - | - |
| **"What regime are we in?"** | - | - | ✅ 7 canonical patterns | ✅ RISK_ON/OFF/TRANSITION |
| **"Is this position safe?"** | - | - | - | ✅ Composite score |
| **"What risks should I watch?"** | ✅ Trigger alerts | ✅ Event classes | ✅ RED FLAG alerts | ✅ Dominant risks |
| **"Should I buy/sell now?"** | - | - | ✅ Regime guidance | ✅ Action recommendations |

---

## 7. Golden Rules Comparison

### 7.1 Non-Negotiable Rules

| System | Golden Rules |
|--------|--------------|
| **v3** | 1. NEVER hardcode strategies (load from config) |
|        | 2. All thresholds externalized |
|        | 3. Multi-tenant support required |
| **v4** | 1. No contract = no ingest |
|        | 2. No evidence pack = no publish |
|        | 3. Gate 4 is mandatory |
|        | 4. Telemetry is the arbiter (RED = blocked) |
| **Macro OS** | 1. Levels lie; changes tell the truth |
|              | 2. Core is vital signs, not entire blood panel |
|              | 3. Validate before acting on patterns |
| **Mine Detector** | 1. Composite must include adjusted_score |
|                   | 2. Score ≥86 is HARD BLOCK (cannot override) |
|                   | 3. RegimeClassifierState must persist |
|                   | 4. staleness_penalty from StalenessChecker |
|                   | 5. overlay_points = notches × 10 |

---

## 8. Integration Points

### 8.1 How Systems Connect

```
┌────────────────────────────────────────────────────────────────────────┐
│                           USER REQUEST                                  │
│              "Should I invest in XYZ? Is it safe?"                     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
           ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────────┐
│    MACRO OS      │   │  MINE DETECTOR   │   │     v3 ANALYTICS         │
│                  │   │                  │   │                          │
│ "What regime?"   │   │ "What risks?"    │   │ "How did strategies      │
│ Pattern: RISK_OFF│──▶│ Score: 72 (HIGH) │   │  perform historically?"  │
│                  │   │ Risks: Crowding, │   │                          │
│                  │   │ Event, Catalyst  │   │ Battle Test + Monte Carlo│
└────────┬─────────┘   └────────┬─────────┘   └────────────┬─────────────┘
         │                      │                          │
         │                      │                          │
         └──────────────────────┼──────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          v4 ARCHITECTURE                               │
│                                                                        │
│  Truth Contracts → Evidence Packs → Gate 4 Compliance → Publication   │
│                                                                        │
│  "Can we PROVE what we publish?"                                       │
└────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       ADELAIDE OUTPUT                                  │
│                                                                        │
│  "Here's what's happening, why it matters, and what to watch"         │
│  + Evidence Pack links (v4)                                           │
│  + Regime context (Macro OS)                                          │
│  + Position-level guidance (Mine Detector)                            │
└────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Data Flow Integration

| From | To | Data Passed |
|------|----|----|
| **v3 Researcher** | Macro OS | Raw market data (yields, VIX, crypto prices) |
| **Macro OS** | Mine Detector (Addendum A) | Regime classification (RISK_ON/OFF/TRANSITION) |
| **Mine Detector** | v4 Evidence Packs | Risk scores + category breakdowns |
| **v4 Gate 4** | Adelaide | Compliance-checked content |
| **v4 Telemetry** | All systems | Health status (GREEN/YELLOW/RED) |

---

## 9. Summary: When to Use Each System

| Question | Use This System |
|----------|-----------------|
| "How would a DCA strategy have performed since 2022?" | **v3 Battle Test** |
| "What's the probability of losing 20% over 4 years?" | **v3 Monte Carlo** |
| "Is protocol X healthy right now?" | **v3 Monitoring Engine** |
| "Can we prove this claim with an audit trail?" | **v4 Evidence Packs** |
| "Is our publication compliant with CLO rules?" | **v4 Gate 4** |
| "Should we publish this week or block?" | **v4 Telemetry** |
| "What market regime are we in right now?" | **Macro OS** |
| "Is a liquidity crisis forming?" | **Macro OS** (Pattern 1) |
| "What's the risk score for ticker XYZ?" | **Mine Detector** |
| "Should I hold this China ADR?" | **Mine Detector** (Addendum D) |
| "Is social sentiment on GME extreme?" | **Mine Detector** (Addendum B) |
| "Can I execute this trade automatically?" | **Mine Detector** (Addendum C) |

---

## 10. Evolution Path

```
v3 (Production)          v4 (Specification)         Macro OS + Mine Detector
─────────────────        ──────────────────         ────────────────────────
│                        │                          │
│ "Smart Analytics"      │ "Provable Intelligence" │ "Regime + Landmines"
│                        │                          │
│ • Historical perf      │ • Audit trail           │ • Market-wide regime
│ • Forward simulation   │ • Publication gates     │ • Single-name risk
│ • Protocol health      │ • Compliance firewall   │ • Execution blocks
│ • Adelaide templates   │ • Event routing         │ • Brokerage integration
│                        │                          │
└────────────┬───────────┴────────────┬────────────┴──────────────────────
             │                        │
             │                        │
             ▼                        ▼
     ┌───────────────────────────────────────────────────────────────┐
     │                    UNIFIED PLATFORM                            │
     │                                                                │
     │  1. Macro OS feeds regime into v4 signals                     │
     │  2. Mine Detector scores wrapped in v4 Evidence Packs         │
     │  3. v3 engines continue for historical/simulation             │
     │  4. Gate 4 compliance applies to ALL outputs                  │
     │  5. Adelaide becomes multi-source aggregator                  │
     │                                                                │
     │  Result: Complete financial intelligence platform             │
     └───────────────────────────────────────────────────────────────┘
```

---

*Document Version: 2026-01-30*
*Comparing: v3 (Production) | v4 (Specification) | Macro OS + Mine Detector (Specification)*
