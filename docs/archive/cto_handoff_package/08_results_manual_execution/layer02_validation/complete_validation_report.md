# diBoaS Analytics â€” Complete Validation Report

**Layer 2: Data Validation**  
**Date:** January 24, 2026  
**Validator:** Claude (Rakia Data Validator)  
**Pipeline Run:** Manual Dry Run #1

---

## OVERALL VERDICT

# âš ï¸ CONDITIONAL PASS

**Rationale:** All 20 CSV files are structurally sound and contain valid data. However, 3 critical data freshness/accuracy issues were identified that require correction before production use.

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Files Validated | 20 |
| Tier 1 (Structural) | âœ… 20/20 passed |
| Tier 2 (Cross-Reference) | âœ… 5/6 event checks passed |
| Tier 3 (Source Verification) | âš ï¸ 3 discrepancies found |
| Blocking Errors | 0 |
| Warnings | 6 |
| Specification Gaps Found | 5 |

---

## Tier 1: Structural Validation Results

### All Files Passed Basic Structural Checks

| File | Rows | Cols | Nulls | Duplicates | Date Range |
|------|------|------|-------|------------|------------|
| treasury_yields.csv | 1,514 | 5 | 0% | 0 | 2020-01-02 to 2026-01-22 |
| global_liquidity.csv | 70 | 3 | 0% | 0 | 2020-01-01 to 2025-10-01 |
| real_yields.csv | 1,514 | 2 | 0% | 0 | 2020-01-02 to 2026-01-22 |
| tradfi_benchmark_data.csv | 1,582 | 9 | 0% | 0 | 2020-01-02 to 2026-01-23 |
| commodities.csv | 93 | 5 | 0% | 0 | 2020-01-02 to 2026-01-23 |
| credit_spreads.csv | 83 | 3 | 0% | 0 | 2020-01-02 to 2026-01-23 |
| crypto_prices.csv | 96 | 4 | 0% | 0 | 2020-01-01 to 2026-01-23 |
| defillama_historical_apy.csv | 96 | 6 | 0% | 0 | 2024-01-01 to 2026-01-22 |
| jupiter_jlp_historical_apy.csv | 56 | 3 | 0% | 0 | 2023-10-01 to 2026-01-22 |
| jito_historical_apy.csv | 54 | 3 | 0% | 0 | 2024-01-01 to 2026-01-22 |
| estate_wallet_tracker.csv | 13 | 9 | 0% | 0 | â€” |
| market_maker_wallet_tracker.csv | 15 | 7 | 0% | 0 | â€” |
| protocol_treasury_tracker.csv | 15 | 8 | 0% | 0 | â€” |
| whale_wallet_master_list.csv | 30 | 7 | 0% | 0 | â€” |
| btc_etf_holdings.csv | 22 | 8 | 0% | 0 | 2024-01-11 to 2026-01-22 |
| corporate_btc_holdings.csv | 12 | 8 | 0% | 0 | â€” |
| institutional_13f.csv | 18 | 8 | 0% | 0 | 2025-02-12 to 2025-11-14 |
| sentiment_indicators.csv | 107 | 3 | 0% | 0 | 2020-01-02 to 2026-01-23 |
| aaii_sentiment.csv | 170 | 5 | 0% | 0 | 2020-01-02 to 2026-01-16 |
| rotation_indicators.csv | 1,582 | 7 | 0% | 0 | 2020-01-02 to 2026-01-23 |

### Schema Validation Issues

| File | Issue | Severity |
|------|-------|----------|
| estate_wallet_tracker.csv | Column named `entity` instead of spec's `entity_name` | âš ï¸ Warning |
| tradfi_benchmark_data.csv | Wide format delivered vs spec's long format | âš ï¸ Warning (already noted in Layer 1 gap analysis) |
| commodities.csv | Extra columns (silver, oil_wti) beyond spec | â„¹ï¸ Info |

---

## Tier 2: Cross-Reference Validation Results

### Known Event Checks

| Event | Date Range | File | Result |
|-------|------------|------|--------|
| COVID Crash | 2020-03-09 to 2020-03-23 | treasury_yields.csv | âœ… 43.8% drop visible |
| COVID Crash | 2020-03-09 to 2020-03-23 | tradfi_benchmark_data.csv | âœ… 22.8% drop visible |
| COVID Crash | 2020-03-09 to 2020-03-23 | crypto_prices.csv | âš ï¸ Insufficient pre-event data |
| FTX Collapse | 2022-11-06 to 2022-11-14 | crypto_prices.csv | âœ… 18.2% drop visible |
| 2022 Rate Hikes | 2022-03 to 2022-12 | treasury_yields.csv | âœ… 2.16% rise visible |
| 2024 BTC ATH | 2024-03-01 to 2024-03-31 | crypto_prices.csv | âœ… $73,000 peak visible |

**Result:** 5/6 passed (1 insufficient data due to monthly aggregation)

### Calculation Verification

| Calculation | File | Result |
|-------------|------|--------|
| SPY/TLT Ratio | rotation_indicators.csv | âœ… Verified (max diff: 0.00005) |
| MA50 | rotation_indicators.csv | âœ… Verified (max diff: 0.00005) |
| M2 YoY % | global_liquidity.csv | âœ… Verified (max diff: 0.05%) |
| AAII Sum to 100% | aaii_sentiment.csv | âœ… Verified (100.0% exactly) |
| Copper/Gold Ratio | rotation_indicators.csv | âš ï¸ Different scale than commodities.csv |

---

## Tier 3: Source Verification Results

### Verified Against Live Sources (January 23-24, 2026)

| Data Point | Stored Value | Live Value | Source | Status |
|------------|--------------|------------|--------|--------|
| 10Y Treasury | ~4.6% | **4.26%** | FRED DGS10 | ðŸ”´ DISCREPANCY |
| 2Y Treasury | ~4.3% | **3.61%** | FRED DGS2 | ðŸ”´ DISCREPANCY |
| 30Y Treasury | ~4.8% | 4.84% | FRED DGS30 | âœ… Match |
| BTC Price | â€” | $90,630 | CoinMarketCap | âœ… Verified |
| ETH Price | â€” | $3,168 | CoinMarketCap | âœ… Verified |
| SOL Price | â€” | $121-$142 | Mixed sources | âš ï¸ 17% variance |
| M2 Latest Month | Oct 2025 | **Nov 2025** | FRED M2SL | ðŸ”´ STALE |
| M2 Value | â€” | $22,322.4B | FRED M2SL | âœ… Verified |
| AAII Bullish | â€” | 43.2% | AAII.com | âœ… Verified |
| Fear & Greed | â€” | 20 (Extreme Fear) | Alternative.me | âœ… Verified |
| IBIT Holdings | â€” | 779,977 BTC | BlackRock | âœ… Verified |
| FBTC Holdings | â€” | 194,498 BTC | Fidelity | âœ… Verified |

---

## Issues Summary

### ðŸ”´ Critical Issues (Require Correction)

| Code | File | Issue | Remediation |
|------|------|-------|-------------|
| T3-TRS-001 | treasury_yields.csv | 10Y yield may be stale (~4.6% vs live 4.26%) | Re-fetch from FRED DGS10 |
| T3-TRS-002 | treasury_yields.csv | 2Y yield may be stale (~4.3% vs live 3.61%) | Re-fetch from FRED DGS2 |
| T3-M2-001 | global_liquidity.csv | Data ends Oct 2025; Nov 2025 now available | Update to include Nov 2025 |

### âš ï¸ Warnings (Non-Blocking)

| Code | File | Issue | Remediation |
|------|------|-------|-------------|
| T1-SCH-001 | estate_wallet_tracker.csv | Column `entity` doesn't match spec `entity_name` | Update spec or rename column |
| T2-DAT-001 | crypto_prices.csv | Insufficient pre-COVID data for drop calculation | Backfill Jan-Feb 2020 daily data |
| T2-CAL-001 | rotation_indicators.csv | Copper/Gold ratio scale differs from commodities.csv | Document calculation formula |

### â„¹ï¸ Informational

| Code | File | Issue |
|------|------|-------|
| T1-SCH-002 | commodities.csv | Extra columns (silver, oil_wti) beyond minimum spec |
| T1-SCH-003 | tradfi_benchmark_data.csv | Wide format vs spec's long format (already in Layer 1 gaps) |

---

## Verdict Criteria

| Criteria | Threshold | Actual | Pass? |
|----------|-----------|--------|-------|
| Tier 1 structural pass rate | â‰¥95% | 100% | âœ… |
| Tier 2 event visibility | â‰¥80% | 83% | âœ… |
| Tier 3 critical discrepancies | 0 | 3 | âš ï¸ |
| Blocking errors | 0 | 0 | âœ… |

**Verdict Logic:**
- PASS: 0 errors, 0 critical discrepancies
- CONDITIONAL PASS: 0 errors, but warnings or discrepancies exist
- FAIL: 1+ blocking errors

**Result: CONDITIONAL PASS** â€” Data is usable but corrections recommended before Adelaide newsletter launch.

---

## Recommendations

### Before Production Use

1. **Re-fetch Treasury Yields** â€” Current data may be showing cached/stale values
2. **Update M2 Data** â€” Pull November 2025 data from FRED M2SL
3. **Verify Researcher Data Source** â€” Confirm Treasury yield API is configured correctly

### Before CTO Automation

1. **Fix 5 specification gaps** â€” See `LAYER2_SPEC_GAP_ANALYSIS.md`
2. **Add schema definitions** â€” 10 files have no validation schema in CTO specs
3. **Document calculation formulas** â€” Copper/Gold ratio methodology unclear

---

## Gate 1 Verdict

| Gate | Status | Can Proceed? |
|------|--------|--------------|
| Gate 1: Raw Data Validation | âš ï¸ CONDITIONAL PASS | âœ… Yes, with noted caveats |

**Handoff to Layer 3 (QR Board Analytics):** APPROVED with recommendations

---

*Validation Report prepared by Claude (Rakia Data Validator)*
*January 24, 2026*
