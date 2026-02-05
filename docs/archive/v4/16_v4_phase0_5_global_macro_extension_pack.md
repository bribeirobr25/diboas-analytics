# FILE: 16_v4_phase0_5_global_macro_extension_pack.md

# diBoaS v4 — Phase 0.5 Global Macro Extension Pack

**Document ID:** V4-P0-5-GLOBAL-001  
**Status:** Enforceable (add-on pack; fail-closed)  
**Last updated:** 2026-01-26  
**Purpose:** Add high-signal non-US/global anchors without bloating Phase 0 or breaking $0 reliability.

This document addresses the “US-centric blind spot” risk by adding **high ROI** global macro sensors that materially improve regime detection, especially for crypto liquidity spillovers.

**Important constraint:** This is **Phase 0.5**, not Phase 0.
- These contracts **must not** block Phase 0 weekly publication unless they are **explicitly referenced** in a published edition.
- If referenced, they are subject to the same rules: **publication SLA**, gate status, reconciliation policy, and Evidence Pack receipts.

---

## 0) So What (why this exists)
Phase 0 is enough for a credible weekly edition. Phase 0.5 makes it smarter and less US-myopic by adding:
- **Japan liquidity/carry sensors** (global funding regime)
- **Financial stress “adult supervision”** beyond just VIX/credit
- **Commodity pulse** (inflation/growth pressure)
- **Brazil context** (local relevance + EM pulse) without pretending EM drives global BTC

You get better macro framing with minimal extra surface area.

---

## 1) Source tiering (repeated because people forget)
- **Tier 1:** Official / institutional (e.g., FRED, central bank)
- **Tier 2:** Reputable aggregators (stable schemas but can change methodology)
- **Tier 3:** Exchange/public endpoints, scraped series (fragile, rate-limited, “zombie API” risk)

Phase 0.5 should be **Tier 1-first** where possible.

---

## 2) Start date policy (reality-based)
- **TradFi / macro (Tier 1):** Pull **MAX AVAILABLE** (ideally 2010+; earlier if available)
- **Crypto/DeFi:** Keep reality constraints (2018+/2020+ depending on series)
- Evidence Packs must disclose limited history when it matters.

---

## 3) Phase 0.5 Contract Adds

### 3.1 Japan Exception (HIGH ROI for global liquidity)
Japan is not “just another country.” It’s global funding plumbing.

**Add contracts:**
1. `fx_usdjpy_spot_v1`  
   - **Priority:** CRITICAL  
   - **Cadence:** Daily (or more frequent if safely available via Tier 1)  
   - **Why:** USD/JPY shocks often coincide with risk regime shifts.

2. `rates_jp10y_yield_proxy_daily_v1`  
   - **Priority:** CRITICAL  
   - **Cadence:** Daily  
   - **Why:** Event class EC-07 (Japan Carry Unwind) requires at least one daily Japan yield witness.
   - **Note:** This is a **proxy** if it’s not Tier 1. Must be marked Tier 3 and treated accordingly.

3. `rates_jp10y_yield_oecd_monthly_v1` (context series)
   - **Priority:** Medium (context-only)  
   - **Cadence:** Monthly  
   - **Why:** Long-history reference series; **not sufficient** alone for EC-07 triggering.

4. `rates_jp_policy_rate_v1`
   - **Priority:** High (context + confirmation)  
   - **Cadence:** Monthly / as available  
   - **Why:** Confirms policy regime but lags.

**So What:** Adds a global funding “storm sensor” that often matters more than another US equity proxy.

---

### 3.2 Financial Stress Anchor
5. `macro_us_nfci_v1`  
   - **Priority:** High  
   - **Cadence:** Weekly (released Fridays)  
   - **Why:** Broad financial conditions index. Useful for weekend crypto session framing.

**So What:** If this shifts sharply, your “calm narrative” should become “watch stress.”

---

### 3.3 Commodities Pulse (Inflation/Growth Pressure)
6. `commod_wti_spot_v1`  
   - **Priority:** Medium  
   - **Cadence:** Daily  
   - **Why:** Energy shocks feed inflation pressure and risk regime shifts.

7. `commod_copper_spot_v1`  
   - **Priority:** Medium  
   - **Cadence:** Daily (preferred)  
   - **Why:** Industrial demand proxy; helps separate growth vs inflation pulses.

**So What:** Adds a simple macro pulse that local businesses and SMBs can actually understand (“input costs”).

---

### 3.4 Brazil Pack (regional context; do not pretend it drives global markets)
8. `rates_br_selic_v1`  
   - **Priority:** Medium  
   - **Cadence:** Daily (business days)  
   - **Why:** Local borrowing/inflation pressure context for Brazil users.

9. `equity_br_ibovespa_proxy_v1` (optional)
   - **Priority:** Low (defer unless Brazil users are a major share)  
   - **Cadence:** Daily  
   - **Why:** Useful context, but often Tier 3 fragile at $0.

**So What:** Makes the product feel relevant in Brazil without polluting the global regime engine.

---

## 4) Recommended free endpoints (probable)

### 4.1 FRED (Tier 1)
- Base: `https://api.stlouisfed.org/fred/series/observations`
- Example (USD/JPY):
  - `?series_id=DEXJPUS&api_key=YOUR_KEY&file_type=json&observation_start=2010-01-01`
- Example (NFCI):
  - `?series_id=NFCI&api_key=YOUR_KEY&file_type=json&observation_start=2010-01-01`
- Example (WTI):
  - `?series_id=DCOILWTICO&api_key=YOUR_KEY&file_type=json&observation_start=2010-01-01`

### 4.2 Brazil Central Bank SGS (Tier 1)
- Base: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{SERIE}/dados`
- Example (SELIC, SGS series commonly used = 11):
  - `?formato=json&dataInicial=01/01/2010&dataFinal=31/12/2026`

### 4.3 Copper proxy (Tier 1 or Tier 2 depending on series)
- If using FRED copper series (varies by availability), use FRED observations endpoint.
- If not available, use a Tier 2 source and treat as such (reconciliation + stale checks required).

### 4.4 Japan 10Y daily proxy (Tier 3 if needed)
- If a daily JGB10 series is not available via Tier 1 in your stack:
  - Add a Tier 3 proxy endpoint (source will vary by availability).
  - Mark as Tier 3 and apply stricter zombie/null/stale validation.

---

## 5) SLAs (default targets)

| Contract group | internal_sla | publication_sla | Notes |
|---|---:|---:|---|
| USD/JPY (daily) | <24h | <48h | CRITICAL for EC-07 context/trigger |
| JGB 10Y daily proxy | <24h | <48h | CRITICAL for EC-07 trigger |
| JGB 10Y monthly (OECD) | <45d | <60d | Context-only; lag disclosure required if referenced |
| Japan policy rate | <45d | <60d | Context; lag disclosure |
| NFCI (weekly) | <7d | <14d | Released weekly; lag disclosure if referenced |
| WTI/Copper (daily) | <24h | <48h | Commod pulse; proxy disclosures if needed |
| SELIC (business days) | <48h | <72h | Holiday-aware handling |

---

## 6) Holiday awareness (Brazil SGS)
BCB SGS can fail or return maintenance notices during Brazilian holidays.

**Rule:** If SGS fails on a known Brazil holiday window:
- set `PASS_WITH_FLAGS` (not FAIL) if last known value is still within publication SLA
- attach disclosure when referenced: cadence/holiday lag
- create a **low-priority** task unless staleness breaches publication SLA

This avoids “the system is dying” alerts when the country is just… not working today.

---

## 7) Integration rules (fail-closed without breaking Phase 0)
- Phase 0.5 contracts live under Truth Contracts like any other contract.
- If a Phase 0.5 contract is referenced in an edition:
  - it must satisfy **publication SLA**
  - it must not be FAIL
  - evidence pack must include required disclosures (proxy/lag/pass_with_flags)
- If not referenced:
  - it must not affect edition eligibility.

---

## 8) What to defer (to avoid scope creep)
Defer unless/until user demand is clear:
- Broad EM equities (fragile + low incremental signal at $0)
- Full G10 yield curve set (nice-to-have, low ROI initially)
- China “credit impulse” composites (doable later, but adds complexity and lag)

---