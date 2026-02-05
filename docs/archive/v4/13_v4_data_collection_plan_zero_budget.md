# FILE: 13_v4_data_collection_plan_zero_budget.md

# diBoaS v4 — Data Collection Plan (Phase 0, $0 Budget)

**Document ID:** V4-DATA-PLAN-001  
**Status:** Enforceable (Phase 0)  
**Revision:** v1.1  
**Last updated:** 2026-01-26  
**Constraint:** $0 external data spend  
**Rule:** No contract = no ingest (see `03_v4_truth_contract_spec.md`)

This document defines **what data we collect**, **where we collect it**, **how far back**, **how frequently**, and **how we keep it auditable and resilient** under a $0 budget.

Phase 0 is designed to power the v4 “Truth Spine” and weekly Adelaide output without overpromising, without HFT cosplay, and without fragile pipelines.

---

## 1) Objectives (Phase 0)

Phase 0 data collection must enable:

1) A reproducible weekly Adelaide edition (3–7 signals) with Evidence Packs  
2) Strong regime visibility across macro/TradFi/crypto/DeFi/RWA  
3) System health that fails closed: stale/blocked inputs => **no publish**  
4) Auditability: every claim ties to exact inputs, retrieval times, and validation status  
5) Survivability under free-tier constraints (rate limits, schema drift, outages)

---

## 2) What we collect (Phase 0 domains)

Phase 0 focuses on high-signal, low-cost metrics. The goal is regime clarity, not coverage vanity.

### A) Rates & Inflation (macro gravity)
- US 2Y / 10Y / 30Y yields  
- 2s10s spread (derived)  
- 10Y real yield (proxy acceptable; disclose)  
- 10Y breakeven inflation  

**Why:** Rates shape cross-asset risk appetite and “price of money” regimes.

### B) Broad Risk & Stress Proxies (cross-asset scoreboard)
- S&P 500 proxy  
- VIX proxy  
- Broad USD index proxy  
- Credit stress proxy (HY OAS and/or IG proxy)  

**Why:** Fast read on risk-on/off and stress regimes with interpretable drivers.

### C) Crypto Spot & Structure (risk temperature inside crypto)
- BTC spot, ETH spot  
- BTC/ETH perpetuals funding (standardized)  
- BTC/ETH open interest  

**Why:** Spot shows direction; funding + OI reveal leverage and crowding.

### D) Stablecoins (plumbing + smoke alarms)
- Total stablecoin supply  
- Depeg events (near-real-time monitoring)  

**Why:** Stablecoins are crypto liquidity plumbing; depegs are early warning.

### E) DeFi Baseline (onchain risk appetite)
- Blue-chip TVL proxy  
- Benchmark DeFi yield proxy (composite; methodology-sensitive)  

**Why:** Tracks onchain expansion/contraction; must be disclosure-heavy.

### F) RWA Tokenized Treasuries (bridge narrative + flows)
- Tokenized treasury TVL/NAV proxy  
- Net flows (derived)  

**Why:** Bridge between TradFi and onchain demand; issuer lag is normal and must be disclosed.

### Optional (Phase 0 extension, low cost)
- **US M2 money supply (monthly):** `macro_us_m2_money_supply_v1`  
  - Mandatory `cadence_lag` disclosure if referenced.

This aligns with `02_v4_phase0_core_contracts.md`.

---

## 3) Source policy ($0 reality, tiering, fallbacks)

Each Truth Contract MUST declare:
- canonical source (required)
- 0–2 fallbacks (recommended)
- `source_tier` (enforced in Trust Score / confidence)
- methodology metadata (see §3.3)

### 3.1 Source tiers (required)

| Tier | Examples | Trust level | Common failure modes | Policy |
|---|---|---:|---|---|
| Tier 1 | Official/public institutions | High | Revisions / vintages | Store `retrieved_at_ts` + vintage fields when available |
| Tier 2 | Reputable aggregators | Medium | Schema changes, throttling, methodology drift | Add fallbacks + drift tracking + reconciliation |
| Tier 3 | Public exchange APIs | Lower | Rate limits, outages, ghost values | Aggregate across venues + stale checks mandatory |

Tier affects:
- confidence/trust_score penalties
- redundancy requirements
- SLA strictness and alerting
- stale-value and zombie/null checks enforcement

### 3.2 Fallback + reconciliation expectations
For Tier 2/3 contracts, the contract should ideally have:
- at least one fallback source
- reconciliation enabled where feasible (tolerance bands)
- “on breach” behavior that creates tasks and blocks clean promotion for high/critical inputs

### 3.3 Methodology drift tracking (required)
Tier 2/3 providers can change the meaning of a metric without changing the endpoint. Phase 0 treats this as a first-class risk.

Each contract MUST declare:
- `source_methodology_version` (provider-defined if available, otherwise an internal tag)
- `methodology_notes` (plain-language explanation)
- a drift policy: if detected => `PASS_WITH_FLAGS` + QR task + disclosure if referenced

Minimum drift detection signals:
- provider/version metadata changed
- schema changed
- parsing/transformation hash changed

---

## 4) Endpoints (recommended patterns)

This is a practical “where we pull it from” list. Exact contract YAML must store canonical + fallback URIs.

### 4.1 FRED (TradFi/macro backbone)
**Pattern:**
- `https://api.stlouisfed.org/fred/series/observations?series_id={SERIES}&api_key={KEY}&file_type=json&observation_start={YYYY-MM-DD}`

Recommended series IDs (Phase 0 core):
- Yields: `DGS2`, `DGS10`, `DGS30`
- Real yield: `DFII10`
- Breakeven: `T10YIE`
- VIX proxy: `VIXCLS`
- SPX proxy: `SP500`
- Broad USD: `DTWEXBGS`
- HY OAS proxy: `BAMLH0A0HYM2`
- IG proxy (optional): `BAMLCC0A0CMTRIV`
- Optional M2: `M2SL` (monthly)

**Revision / vintage policy:** store both `asof_ts` and `retrieved_at_ts`, and include vintage fields when available (see §8).

### 4.2 DefiLlama (stablecoins / DeFi / RWA baselines)
Use DefiLlama endpoints for:
- stablecoin supply aggregates
- TVL baselines
- selected RWA aggregates when available

**Policy:** Tier 2. Expect throttling and occasional schema/methodology changes.

### 4.3 Crypto spot (aggregator and/or exchange spot endpoints)
Use a Tier 2 aggregator for spot if stable under $0 constraints.
Fallback: exchange spot endpoints.

**Policy:** caching required; fallbacks recommended.

### 4.4 Perps funding & open interest (exchange public APIs)
Use Tier 3 exchange endpoints with multi-venue aggregation.

**Policy:** do not rely on a single exchange; aggregate across ≥3 venues where feasible.

---

## 5) History policy (how far back)

Each contract MUST include a `history_policy`:
- `backtest_depth_required` (MAX_AVAILABLE / P15Y / P10Y / P6Y / P3Y)
- `min_start_date` (optional)
- a reason and known coverage limits

### 5.1 Recommended defaults

| Domain | Recommended history | Rationale |
|---|---|---|
| Rates / VIX / Credit / USD | MAX_AVAILABLE (min 2010) | multiple macro regimes |
| BTC/ETH spot | earliest reliable | multi-cycle crypto context |
| Perps funding/OI | reality-based (often 2018/2019+) | product availability |
| DeFi TVL/yield | reality-based (often 2020+) | DeFi era |
| RWA tokenized treasuries | reality-based (often 2021+) | issuer/product era |
| M2 (optional) | MAX_AVAILABLE | long-run context; lagged |

**Disclosure rule:** Evidence Packs must disclose limited history where relevant (DeFi/RWA/perps).

---

## 6) Granularity policy (how “fast” data needs to be)

$0 does not support high-frequency pulls everywhere. Granularity is chosen by usefulness and survivability.

### 6.1 Recommended granularity (Phase 0)

| Contract group | Granularity | Notes |
|---|---|---|
| FRED TradFi proxies (rates, VIX, SPX, USD, credit) | Daily | pull once/day + pre-publish refresh |
| Crypto spot | Hourly (or 4h) | enough for weekly signals |
| Perps funding/OI | Hourly (or 4h) | aggregate across venues |
| Stablecoin supply | Daily | |
| Depeg detection | 15–60m checks | top stablecoins only; alert-focused |
| DeFi TVL/yields | Daily | methodology-sensitive; expect flags |
| RWA | Daily or slower | issuer lag normal; disclosure mandatory |
| M2 (optional) | Monthly | lag disclosure mandatory |

---

## 7) Update cadence + the “Heartbeat Collector”

To avoid rate-limit chaos and inconsistent snapshots, Phase 0 uses a **single orchestrated collector**.

### 7.1 Collector tick schedule (recommended)
- Runs every hour (UTC)
- On every tick:
  - crypto spot (hourly or 4h bucket)
  - perps funding/OI
  - depeg checks (if enabled)
- On `hour == 00` tick:
  - FRED / macro / TradFi daily pulls
  - DeFi TVL/yields daily pulls
  - RWA daily pulls

### 7.2 Pre-publication refresh (required)
Before the weekly eligibility check, run a “final refresh” to minimize stale blocks.

Default:
- Run at `Sunday 04:00 UTC` (configurable)
- Pull/re-check:
  - crypto/perps/stables high-frequency inputs
  - any near-breach SLAs
  - any Tier 2/3 endpoints that have been flaky in the last 24h

### 7.3 Final Truth Snapshot (Edition Snapshot Semantics) — REQUIRED
`final_truth_snapshot_ts` is the **single timestamp** used to determine edition eligibility.

Rules:
- Default `final_truth_snapshot_ts = Sunday 04:00 UTC` (configurable).
- For each referenced contract, select latest observation where:
  - `asof_ts <= final_truth_snapshot_ts`
- If any referenced contract is:
  - missing
  - stale beyond `publication_sla`
  - `FAIL` at Gate 1/2
  - or has unresolved high/critical reconciliation diffs in the last 7d  
  then:
  - Telemetry => **RED**
  - Publication => **BLOCKED**
  - Task(s) => created with severity by risk tier

**Ragged edge note:** If a source updates later in the day (macro/TradFi timing), missing data at the snapshot time is treated as a real readiness failure (alerts/tasks). Do not “wait and hope.”

---

## 8) Auditability rules (vintages, timestamps, receipts)

### 8.1 Required timestamps for every observation
Store:
- `asof_ts` (when observation refers to)
- `retrieved_at_ts` (when we fetched it)

`retrieved_at_ts` is **mandatory** for:
- reproducibility
- revision awareness
- Evidence Pack receipts

### 8.2 Revision/vintage handling (Tier 1 macro especially)
If the source supports vintages/revisions, store:
- the source’s revision window fields when available (e.g., real-time period)
- and always preserve the retrieved observation as-of `retrieved_at_ts`

**Reason:** Evidence Packs must prove what the system saw at publication time, even if the upstream revises later.

---

## 9) Weekend/holiday alignment (5-day TradFi vs 7-day crypto)

Cross-asset features must define a consistent as-of policy.

### 9.1 Canonical rule
For any feature mixing 5-day and 7-day assets:
- Use `final_truth_snapshot_ts`
- Use latest observation `<= final_truth_snapshot_ts` per contract
- Do not force synchrony by inventing data

### 9.2 Forward-fill policy (strict)
- Crypto: forward-fill forbidden
- TradFi: forward-fill allowed only within contract policy (e.g., weekends/holidays), tracked and disclosed if applied

### 9.3 Required disclosure pattern (example)
If a weekly feature mixes:
- TradFi data as of Friday close
- Crypto data as of Sunday snapshot  
Evidence Pack must include a note like:
- “TradFi inputs reflect last available market close before snapshot; crypto inputs reflect 24/7 data as of snapshot. This does not change the educational nature of this commentary.”

---

## 10) $0 failure modes and required mitigations

### 10.1 Rate limits & throttling
Mitigations:
- single heartbeat collector
- caching of identical requests
- exponential backoff
- automatic downshift (reduce low-risk polling under quota pressure)
- prioritize critical contracts in pre-publish refresh

### 10.2 Ghost updates (timestamps move, values freeze)
Mitigation:
- **stale_value_check** (mandatory for Tier 2/3 sources)

Recommended config:
```yaml
stale_value_check:
  enabled: true
  window_n_updates: 4
  rule: "if value unchanged for N consecutive expected updates"
  severity_by_risk_tier:
    critical: "FAIL"
    high: "PASS_WITH_FLAGS"
    medium: "PASS_WITH_FLAGS"
    low: "FLAG_ONLY"