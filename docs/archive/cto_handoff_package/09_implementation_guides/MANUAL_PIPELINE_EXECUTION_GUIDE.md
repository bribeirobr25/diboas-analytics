# diBoaS Analytics â€” Manual Pipeline Execution Guide

**Purpose:** First-time manual run of the complete data pipeline  
**Created:** January 23, 2026  
**Updated:** January 24, 2026 (v3 â€” GAP-001, GAP-002, GAP-003, GAP-011, GAP-012 fixes)  
**Prepared by:** Rakia  
**For:** Bar to coordinate across boards  
**Change Log:**
- v3: Added SPY, TLT, XLF, XLU, IWM to Task 1.2 (GAP-001)
- v3: Updated tradfi_benchmark_data.csv schema to wide format (GAP-002)
- v3: Changed `entity_name` to `entity` in Task 1.4 (GAP-003)
- v3: Added year currency check to validation criteria (GAP-011)
- v2: Added Phase 1 vs Phase 2 note to Task 1.7 (GAP-012)

---

## Pipeline Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                                                                             â”‚
â”‚  LAYER 1         LAYER 2         LAYER 3         LAYER 4         LAYER 5   â”‚
â”‚  COLLECTION  â†’   VALIDATION  â†’   ANALYTICS  â†’   INTELLIGENCE â†’  PRESENT   â”‚
â”‚                                                                             â”‚
â”‚  Rakia           Rakia           QR              Strategy        CMO       â”‚
â”‚  Researcher      Validator       Board           Board           Board     â”‚
â”‚                                                                             â”‚
â”‚     â†“               â†“               â†“               â†“              â†“       â”‚
â”‚  Gate 1          Gate 2          Gate 3          Gate 4         OUTPUT     â”‚
â”‚  (Schema)        (Quality)       (Stats)         (Legal+Tone)   (User)     â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

# LAYER 1: DATA COLLECTION

**Owner:** Rakia Researcher  
**Input:** Data specification documents (00-08)  
**Output:** Raw CSV files  
**Gate:** Gate 1 (Schema Validation)

---

## Task 1.1: Macro Economics Data

**Specification:** `04_MACRO_ECONOMICS.md`

**Request to Rakia Researcher:**

> Please collect the following macro economics data as the first task in our manual pipeline run. This is a fresh start - do not reference any previous data collection.
>
> **Data Required:**
>
> | Data Point | Source | Frequency | Date Range |
> |------------|--------|-----------|------------|
> | US Treasury Yields (2Y, 5Y, 10Y, 30Y) | FRED (DGS2, DGS5, DGS10, DGS30) | Daily | 2020-01-01 to today |
> | US M2 Money Supply | FRED (M2SL) | Monthly | 2020-01 to latest |
> | Real Yields (10Y TIPS) | FRED (DFII10) | Daily | 2020-01-01 to today |
> | Fed Funds Rate | FRED (FEDFUNDS) | Monthly | 2020-01 to latest |
>
> **Deliverables:**
> 1. `treasury_yields.csv` â€” columns: date, yield_2y, yield_5y, yield_10y, yield_30y
> 2. `global_liquidity.csv` â€” columns: date, us_m2_bn, us_m2_yoy
> 3. `real_yields.csv` â€” columns: date, real_yield_10y
>
> **Validation Criteria:**
> - All dates are parseable (YYYY-MM-DD format)
> - All dates contain year 2020 or later (no year currency errors like 202X becoming 20X)
> - No missing values in required columns
> - Values are within expected ranges (yields 0-10%, M2 $15-25 trillion)
> - Latest date within 7 days of today (accounting for weekends/holidays)

---

## Task 1.2: TradFi Market Data

**Specification:** `03_TRADFI_MARKETS.md`

**Request to Rakia Researcher:**

> Please collect TradFi market data as the second collection task.
>
> **Data Required:**
>
> | Data Point | Source | Ticker | Date Range | Required For |
> |------------|--------|--------|------------|--------------|
> | S&P 500 | Yahoo Finance | ^GSPC | 2020-01-01 to today | Benchmark |
> | NASDAQ | Yahoo Finance | ^IXIC | 2020-01-01 to today | Benchmark |
> | Gold | Yahoo Finance | GC=F | 2020-01-01 to today | Commodities |
> | Copper | Yahoo Finance | HG=F | 2020-01-01 to today | Commodities |
> | VIX | Yahoo Finance | ^VIX | 2020-01-01 to today | Volatility |
> | Credit Spreads (HY OAS) | FRED | BAMLH0A0HYM2 | 2020-01-01 to today | Credit |
> | **SPY ETF** | **Yahoo Finance** | **SPY** | **2020-01-01 to today** | **Rotation (Required)** |
> | **TLT ETF (20+ Yr Treasury)** | **Yahoo Finance** | **TLT** | **2020-01-01 to today** | **Rotation (Required)** |
> | **XLF ETF (Financials)** | **Yahoo Finance** | **XLF** | **2020-01-01 to today** | **Rotation (Required)** |
> | **XLU ETF (Utilities)** | **Yahoo Finance** | **XLU** | **2020-01-01 to today** | **Rotation (Required)** |
> | **IWM ETF (Russell 2000)** | **Yahoo Finance** | **IWM** | **2020-01-01 to today** | **Rotation (Required)** |
>
> **CRITICAL:** SPY, TLT, XLF, XLU, IWM are **REQUIRED** for Task 1.7 (Rotation Indicators). Do not skip these.
>
> **Deliverables:**
> 1. `tradfi_benchmark_data.csv` â€” **WIDE FORMAT** with columns:
>    - date, spy_close, tlt_close, xlf_close, xlu_close, iwm_close, gspc_close, ixic_close, vix_close
>    - (One row per date, one column per ticker)
> 2. `credit_spreads.csv` â€” columns: date, hy_oas_spread, ig_spread
> 3. `commodities.csv` â€” columns: date, gold_close, copper_close
>
> **Schema Note:** The `tradfi_benchmark_data.csv` should be in **WIDE format** (tickers as columns), NOT long format (tickers as rows). This enables direct ratio calculations in Task 1.7.
>
> **Validation Criteria:**
> - Trading days only (no weekends except for 24/7 markets)
> - OHLC relationship: Low â‰¤ Open,Close â‰¤ High
> - No negative prices
> - Volume â‰¥ 0
> - All dates contain year 2020 or later

---

## Task 1.3: Crypto & DeFi Data

**Specification:** `02_CRYPTO_MARKETS.md`

**Request to Rakia Researcher:**

> Please collect crypto and DeFi yield data.
>
> **Data Required:**
>
> | Data Point | Source | Date Range |
> |------------|--------|------------|
> | BTC/USD Price | Yahoo Finance (BTC-USD) | 2020-01-01 to today |
> | ETH/USD Price | Yahoo Finance (ETH-USD) | 2020-01-01 to today |
> | SOL/USD Price | Yahoo Finance (SOL-USD) | 2020-01-01 to today |
> | DeFi Protocol APYs | DeFiLlama API | Last 2 years |
>
> **Target Protocols for APY:**
> - Compound V3 (Arbitrum USDC)
> - Aave V3 (Ethereum USDC)
> - Sky Savings Rate (formerly MakerDAO DSR)
> - Jupiter JLP (Solana)
> - Jito (Solana staking)
>
> **Deliverables:**
> 1. `crypto_prices.csv` â€” columns: date, btc_close, eth_close, sol_close
> 2. `defillama_historical_apy.csv` â€” columns: date, protocol, chain, pool, apy, tvl_usd
> 3. `jupiter_jlp_historical_apy.csv` â€” columns: date, apy, tvl_usd
> 4. `jito_historical_apy.csv` â€” columns: date, apy, tvl_usd
>
> **Validation Criteria:**
> - APY values 0-100% (flag anything >50% for review)
> - TVL values positive
> - No future dates
> - All dates contain year 2020 or later

---

## Task 1.4: On-Chain Intelligence

**Specification:** `01_ON_CHAIN_INTELLIGENCE.md`

**Request to Rakia Researcher:**

> Please collect on-chain intelligence data focusing on estate wallets and exchange flows.
>
> **Data Required:**
>
> | Data Point | Source | Notes |
> |------------|--------|-------|
> | Estate Wallet Addresses | Arkham Intelligence, court docs | FTX, Mt. Gox, Genesis, Celsius, 3AC |
> | Estate Court Schedule | Kroll, PACER, court websites | Next hearing dates, distribution timelines |
> | Exchange Hot Wallets | Etherscan labels, Arkham | Top 10 exchanges by volume |
> | Token Unlock Schedule | Tokenomist, TokenUnlocks | Major protocols next 90 days |
>
> **Deliverables:**
> 1. `estate_wallet_tracker.csv` â€” columns: **entity**, wallet_address, chain, last_known_balance, estimated_usd_value, risk_tier
>    - **NOTE:** Column is `entity`, NOT `entity_name`
> 2. `estate_court_schedule.csv` â€” columns: entity, next_hearing_date, case_status, distribution_timeline, case_number
> 3. `exchange_hot_wallets.csv` â€” columns: exchange, wallet_address, chain, label
> 4. `token_unlock_schedule.csv` â€” columns: protocol, unlock_date, token_amount, usd_value, unlock_type
>
> **Validation Criteria:**
> - Wallet addresses match chain format (0x... for ETH, bc1/3... for BTC)
> - Court dates are in the future or marked as "complete"
> - No duplicate wallet addresses

---

## Task 1.5: Institutional Flows

**Specification:** `05_INSTITUTIONAL_FLOWS.md`

**Request to Rakia Researcher:**

> Please collect institutional flow data.
>
> **Data Required:**
>
> | Data Point | Source | Notes | Automation Status |
> |------------|--------|-------|-------------------|
> | 13F Filings (Crypto exposure) | SEC EDGAR | Strategy, Tesla, major funds | **MANUAL ONLY** |
> | BTC ETF Holdings | Fund websites, SEC | IBIT, FBTC, GBTC, ARKB | Automatable |
> | Corporate BTC Holdings | Company filings, BitcoinTreasuries | Public companies | **MANUAL ONLY** |
>
> **Note:** 13F filings and corporate holdings require manual research and cannot be fully automated.
>
> **Deliverables:**
> 1. `institutional_13f.csv` â€” columns: entity_name, filing_date, btc_shares, btc_value_usd, change_from_prior
> 2. `btc_etf_holdings.csv` â€” columns: date, fund_ticker, btc_holdings, aum_usd
> 3. `corporate_btc_holdings.csv` â€” columns: company, btc_holdings, avg_cost_basis, market_value
>
> **Validation Criteria:**
> - Filing dates are valid quarters
> - Holdings values are positive
> - Known entities match expected names

---

## Task 1.6: Sentiment Indicators

**Specification:** `07_NEWS_AND_SENTIMENT.md`

**Request to Rakia Researcher:**

> Please collect sentiment indicator data.
>
> **Data Required:**
>
> | Data Point | Source | Frequency | API Endpoint |
> |------------|--------|-----------|--------------|
> | Crypto Fear & Greed Index | Alternative.me | Daily | `https://api.alternative.me/fng/` |
> | AAII Investor Sentiment | AAII.com | Weekly (Thursdays) | Manual scrape |
> | VIX (already collected) | Yahoo Finance | Daily | Already in Task 1.2 |
>
> **Deliverables:**
> 1. `sentiment_indicators.csv` â€” columns: date, fear_greed_index, fear_greed_label
> 2. `aaii_sentiment.csv` â€” columns: date, bullish_pct, bearish_pct, neutral_pct
>
> **Validation Criteria:**
> - Fear/Greed index 0-100
> - AAII percentages sum to 100% (Â±1% tolerance for rounding)
> - Weekly data has ~52 rows per year
> - All dates contain year 2020 or later

---

## Task 1.7: Capital Rotation Indicators

**Specification:** `06_CAPITAL_ROTATION.md`

**Request to Rakia Researcher:**

> Please calculate capital rotation indicators from the price data already collected in Task 1.2.
>
> **Calculations Required:**
>
> | Ratio | Formula | Interpretation | Source Columns |
> |-------|---------|----------------|----------------|
> | SPY/TLT | spy_close / tlt_close | Risk-on vs Risk-off | tradfi_benchmark_data.csv |
> | Copper/Gold | copper_close / gold_close | Economic growth expectations | commodities.csv |
> | XLF/XLU | xlf_close / xlu_close | Cyclical vs Defensive | tradfi_benchmark_data.csv |
> | IWM/SPY | iwm_close / spy_close | Risk appetite (small vs large cap) | tradfi_benchmark_data.csv |
>
> **Copper/Gold Formula Note:** 
> - Copper is in cents/lb (~$4.50 = 450 cents), Gold is in $/oz (~$2,700)
> - Raw ratio will be very small (e.g., 0.0017)
> - This is correct â€” do NOT normalize. The ratio's trend matters, not absolute value.
>
> **Deliverables:**
> 1. `rotation_indicators.csv` â€” columns: date, spy_tlt_ratio, copper_gold_ratio, xlf_xlu_ratio, iwm_spy_ratio, spy_tlt_ma50, spy_tlt_signal
>
> **Validation Criteria:**
> - All ratios positive
> - MA50 calculated correctly (50-day rolling average)
> - Signal = "ABOVE_MA" if ratio > MA50, else "BELOW_MA"
>
> **Phase 1 vs Phase 2 Note:**
> These four ratios (SPY/TLT, Copper/Gold, XLF/XLU, IWM/SPY) are the **Phase 1** rotation indicators.
> Phase 2 will add: Gold/BTC, DXY trend, and additional sector rotations.
> See `06_CAPITAL_ROTATION.md` for the complete priority table with phase annotations.

---

# LAYER 2: DATA VALIDATION

**Owner:** Rakia Data Validator  
**Input:** Raw CSV files from Layer 1  
**Output:** Validated CSV files + Validation Report  
**Gate:** Gate 2 (Data Quality)

---

## Task 2.1: Tier 1 Structural Validation

**Request to Rakia Data Validator:**

> Please perform Tier 1 (Structural) validation on all CSV files received from Rakia Researcher.
>
> **Checks Required:**
>
> | Check | Pass Criteria |
> |-------|---------------|
> | Schema | All required columns present |
> | Data Types | Dates parseable, numbers numeric |
> | Completeness | <5% null values in required fields |
> | Format | Consistent date format (YYYY-MM-DD) |
> | Year Check | All years are 2020-2026 (no truncated years like 202 or 20) |
> | Duplicates | No duplicate rows |
>
> **Deliverable:**
> - `tier1_validation_report.json` with pass/fail for each file and check
>
> **Blocker Conditions (Auto-FAIL):**
> - Missing required columns
> - >5% unparseable dates
> - Empty file
> - Year values outside 2020-2026 range

---

## Task 2.2: Tier 2 Cross-Reference Validation

**Request to Rakia Data Validator:**

> Please perform Tier 2 (Cross-Reference) validation.
>
> **Checks Required:**
>
> | Check | Method |
> |-------|--------|
> | Known Events | COVID crash (Mar 2020), FTX collapse (Nov 2022), Fed hikes (2022-2023) visible in data |
> | Calculation Verification | Recalculate 5 random MA50 values, verify within 0.5% |
> | Outlier Detection | Flag values >3 standard deviations from mean |
> | Trend Consistency | VIX should spike when equities drop |
> | Date Range | Data covers 2020-01-01 to present |
>
> **Deliverable:**
> - `tier2_validation_report.json` with findings for each check
> - List of flagged outliers for review

---

## Task 2.3: Tier 3 Source Verification

**Request to Rakia Data Validator:**

> Please perform Tier 3 (Source Verification) validation by spot-checking against live sources.
>
> **Checks Required:**
>
> | Data | Source to Verify Against |
> |------|--------------------------|
> | Treasury Yields (latest 3 days) | Treasury.gov or FRED |
> | BTC Price (latest) | CoinGecko or Yahoo Finance |
> | FTX Court Date | Kroll restructuring portal |
> | Mt. Gox Deadline | Official trustee website |
> | 3 random wallet addresses | Etherscan/Solscan |
>
> **Weekend/Holiday Consideration:**
> - Treasury yields are only published on business days
> - "Latest 3 days" means latest 3 business days
> - A file dated Friday is still fresh on Sunday
>
> **Deliverable:**
> - `tier3_verification_report.md` with comparison tables
> - Discrepancy analysis (acceptable if <5% difference for prices)

---

## Task 2.4: Consolidated Validation Report

**Request to Rakia Data Validator:**

> Please create a consolidated validation report.
>
> **Deliverables:**
> 1. `complete_validation_report.md` â€” Human-readable summary
> 2. `validation_report.json` â€” Machine-readable results
>
> **Required Sections:**
> - Executive Summary (pass rate by tier)
> - Per-file pass/fail status
> - Issues found and severity
> - Recommendations for fixes
> - Overall verdict: PASS / CONDITIONAL PASS / FAIL

---

# LAYER 3: ANALYTICS

**Owner:** QR Board  
**Input:** Validated CSV files from Layer 2  
**Output:** Analytics results, risk metrics, simulations  
**Gate:** Gate 3 (Statistical Validation)

---

## Task 3.1: Battle Test Analysis

**Request to QR Board:**

> Please run Battle Test analysis on the 10 diBoaS strategies using the validated historical data.
>
> **Analysis Required:**
>
> | Scenario | Date Range | What to Measure |
> |----------|------------|-----------------|
> | COVID Crash | Feb 19 - Mar 23, 2020 | Max drawdown, recovery time |
> | FTX Collapse | Nov 1 - Nov 30, 2022 | Strategy exposure, losses |
> | Terra/Luna | May 1 - May 15, 2022 | UST depeg impact |
> | 2022 Bear Market | Jan 1 - Dec 31, 2022 | Full year performance |
> | 2023 Recovery | Jan 1 - Dec 31, 2023 | Upside capture |
>
> **Deliverables:**
> 1. `battle_test_results.json` â€” Per-strategy performance in each scenario
> 2. `battle_test_summary.md` â€” Human-readable analysis
>
> **Validation Criteria (CV-01 to CV-07):**
> - CV-01: Sharpe ratio calculation verified
> - CV-02: Drawdown calculation verified
> - CV-03: Recovery time calculation verified
> - CV-04: No look-ahead bias
> - CV-05: Transaction costs included
> - CV-06: Slippage assumptions documented
> - CV-07: Statistical significance noted

---

## Task 3.2: Monte Carlo Simulation

**Request to QR Board:**

> Please run Monte Carlo simulation for each strategy.
>
> **Parameters:**
>
> | Parameter | Value |
> |-----------|-------|
> | Simulations | 10,000 |
> | Time Horizon | 1 year |
> | Confidence Levels | 95%, 99% |
> | Regime Model | 3-state (Bull/Bear/Neutral) |
> | Correlation Matrix | Dynamic (regime-dependent) |
>
> **Deliverables:**
> 1. `monte_carlo_results.json` â€” Per-strategy distribution of outcomes
> 2. For each strategy:
>    - VaR (95%, 99%)
>    - CVaR (Expected Shortfall)
>    - Probability of loss
>    - Expected return range (10th-90th percentile)
>
> **Validation Criteria:**
> - Simulations converge (variance of last 1,000 < 0.1%)
> - Results plausible given historical data
> - Regime transitions follow Markov assumptions

---

## Task 3.3: Risk Metrics Calculation

**Request to QR Board:**

> Please calculate standard risk metrics for each strategy.
>
> **Metrics Required:**
>
> | Metric | Formula | Period |
> |--------|---------|--------|
> | Sharpe Ratio | (Return - RFR) / StdDev | 1Y, 3Y, All-time |
> | Sortino Ratio | (Return - RFR) / DownsideStdDev | 1Y, 3Y |
> | Max Drawdown | Peak-to-trough decline | All-time |
> | Calmar Ratio | CAGR / Max Drawdown | 3Y |
> | Beta to BTC | Covariance / Variance(BTC) | 1Y |
>
> **Deliverables:**
> 1. `risk_metrics.json` â€” All metrics per strategy
> 2. `risk_metrics_summary.md` â€” Comparison table

---

## Task 3.4: Anomaly Detection

**Request to QR Board:**

> Please run anomaly detection on the collected data.
>
> **Methods:**
>
> | Method | Apply To |
> |--------|----------|
> | Z-Score (>3Ïƒ) | Price changes, yield changes |
> | Isolation Forest | Multi-dimensional market data |
> | CUSUM | Detecting regime changes |
>
> **Deliverables:**
> 1. `anomalies_detected.json` â€” List of detected anomalies with timestamps
> 2. `anomaly_report.md` â€” Human-readable analysis with context
>
> **Alert Categories:**
> - Price Anomaly: >5% single-day move in major asset
> - Yield Anomaly: >50bps single-day change in treasury
> - Correlation Anomaly: Major change in BTC/equity correlation

---

# LAYER 4: INTELLIGENCE

**Owner:** Strategy Board  
**Input:** Analytics results from Layer 3  
**Output:** Triggered actions, alerts, regime classification  
**Gate:** Gate 3 (Strategy Validation)

---

## Task 4.1: Trigger Evaluation

**Request to Strategy Board:**

> Please evaluate all 28 defined triggers against current market data.
>
> **Input Files:**
> - `battle_test_results.json`
> - `monte_carlo_results.json`
> - `risk_metrics.json`
> - `anomalies_detected.json`
>
> **Deliverable:**
> - `triggered_actions.json` with:
>   - trigger_id
>   - fired: true/false
>   - priority: P0/P1/P2/P3
>   - recommended_action
>   - supporting_data

---

## Task 4.2: Alert Consolidation

**Request to Strategy Board:**

> Please consolidate all fired triggers into a prioritized alert list.
>
> **Consolidation Rules:**
> - De-duplicate related triggers
> - Preserve highest priority
> - Add human-readable context
>
> **Deliverable:**
> - `consolidated_alerts.json` ordered by priority

---

## Task 4.3: Regime Classification

**Request to Strategy Board:**

> Please classify current market regime based on all inputs.
>
> **Regime Categories:**
>
> | Regime | Indicators |
> |--------|------------|
> | Risk-On Bull | SPY/TLT high, VIX low, BTC strong |
> | Risk-Off Bear | SPY/TLT low, VIX high, BTC weak |
> | Neutral/Transition | Mixed signals |
> | Crisis | VIX >35, correlations spike to 1 |
>
> **Deliverable:**
> - `regime_classification.json` with confidence scores

---

# LAYER 5: PRESENTATION

**Owner:** CMO Board + CLO Board  
**Input:** Intelligence outputs from Layer 4  
**Output:** Adelaide content ready for distribution  
**Gate:** Gate 4 (Legal + Tone Approval)

---

## Task 5.1: Content Assembly

**Request to CMO Board:**

> Please assemble Adelaide Daily content from the intelligence outputs.
>
> **Sections Required:**
>
> | Section | Length | Content |
> |---------|--------|---------|
> | Market Snapshot | 150 words | Key numbers, regime, trend |
> | Whale Watch | 100 words | Estate activity, MM signals |
> | Your Strategies | 200 words | Performance, recommendations |
> | Adelaide's Insight | 100 words | Human-readable analysis |
>
> **Deliverables:**
> - `adelaide_daily_draft.md` â€” Full newsletter content
> - `adelaide_daily_data.json` â€” Structured data for templates

---

## Task 5.2: Persona Adaptation

**Request to CMO Board:**

> Please create persona-specific versions of the Adelaide Daily.
>
> **Personas:**
>
> | Persona | Style | Focus |
> |---------|-------|-------|
> | Ana (Conservative) | Simple, reassuring | Stability, safety |
> | Maria (Balanced) | Friendly, educational | Growth potential |
> | Felipe (Sophisticated) | Technical, data-rich | Risk/reward analysis |
>
> **Deliverables:**
> - `adelaide_daily_ana_en.md`
> - `adelaide_daily_maria_en.md`
> - `adelaide_daily_felipe_en.md`

---

## Task 5.3: Legal Compliance Review

**Request to CLO Board:**

> Please review Adelaide content for legal compliance.
>
> **Checks Required:**
>
> | Check | Requirement |
> |-------|-------------|
> | Disclaimers | Present for EU, US, BR |
> | Investment Advice | No recommendations language |
> | Statistics | From QR-approved list only |
> | Risk Warnings | Before any yield mention |
> | Fee Disclosure | Accurate and visible |
>
> **Deliverable:**
> - `clo_review_result.json` with pass/fail and required edits

---

## Task 5.4: Localization

**Request to CMO Board:**

> Please localize approved content to Portuguese (Brazil).
>
> **Deliverables:**
> - `adelaide_daily_ana_ptbr.md`
> - `adelaide_daily_maria_ptbr.md`
> - `adelaide_daily_felipe_ptbr.md`
>
> **Localization Notes:**
> - Cultural adaptation, not literal translation
> - Dollar protection messaging for Brazil
> - Use "Seu EU do futuro" style expressions

---

## Task 5.5: Final Approval

**Request to CLO + CMO Boards:**

> Please provide final approval for distribution.
>
> **Deliverables:**
> - `gate4_cmo_validation.json`
> - `gate4_clo_validation.json`
>
> **Approval Criteria:**
> - All legal checks passed
> - Tone appropriate for persona
> - No conflicting recommendations
> - Data matches source files

---

# RECOMMENDED EXECUTION SCHEDULE

## Day 1: Layer 1 (Collection)

| Order | Task | Chat | Est. Time |
|-------|------|------|-----------|
| 1 | Task 1.1: Macro Economics | Rakia Researcher | 1 hour |
| 2 | Task 1.2: TradFi Markets | Rakia Researcher | 1.5 hours |
| 3 | Task 1.3: Crypto & DeFi | Rakia Researcher | 1.5 hours |
| 4 | Task 1.4: On-Chain Intelligence | Rakia Researcher | 2 hours |
| 5 | Task 1.5: Institutional Flows | Rakia Researcher | 1 hour |
| 6 | Task 1.6: Sentiment Indicators | Rakia Researcher | 30 min |
| 7 | Task 1.7: Capital Rotation | Rakia Researcher | 30 min |

**Day 1 Total:** ~7-8 hours

---

## Day 2: Layer 2 (Validation)

| Order | Task | Chat | Est. Time |
|-------|------|------|-----------|
| 8 | Task 2.1: Tier 1 Structural | Rakia Data Validator | 1 hour |
| 9 | Task 2.2: Tier 2 Cross-Reference | Rakia Data Validator | 1.5 hours |
| 10 | Task 2.3: Tier 3 Source Verification | Rakia Data Validator | 1 hour |
| 11 | Task 2.4: Consolidated Report | Rakia Data Validator | 30 min |

**Day 2 Total:** ~4 hours

---

## Day 3: Layer 3 (Analytics)

| Order | Task | Chat | Est. Time |
|-------|------|------|-----------|
| 12 | Task 3.1: Battle Test | QR Board | 2 hours |
| 13 | Task 3.2: Monte Carlo | QR Board | 2 hours |
| 14 | Task 3.3: Risk Metrics | QR Board | 1 hour |
| 15 | Task 3.4: Anomaly Detection | QR Board | 1 hour |

**Day 3 Total:** ~6 hours

---

## Day 4: Layer 4 (Intelligence)

| Order | Task | Chat | Est. Time |
|-------|------|------|-----------|
| 16 | Task 4.1: Trigger Evaluation | Strategy Board | 1.5 hours |
| 17 | Task 4.2: Alert Consolidation | Strategy Board | 1 hour |
| 18 | Task 4.3: Regime Classification | Strategy Board | 1 hour |

**Day 4 Total:** ~3.5 hours

---

## Day 5: Layer 5 (Presentation)

| Order | Task | Chat | Est. Time |
|-------|------|------|-----------|
| 19 | Task 5.1: Content Assembly | CMO Board | 1.5 hours |
| 20 | Task 5.2: Persona Adaptation | CMO Board | 1 hour |
| 21 | Task 5.3: Legal Compliance | CLO Board | 1 hour |
| 22 | Task 5.4: Localization | CMO Board | 1 hour |
| 23 | Task 5.5: Final Approval | CLO + CMO | 30 min |

**Day 5 Total:** ~5 hours

---

## Total Estimated Time

| Day | Layer | Hours |
|-----|-------|-------|
| Day 1 | Collection | 7-8 |
| Day 2 | Validation | 4 |
| Day 3 | Analytics | 6 |
| Day 4 | Intelligence | 3.5 |
| Day 5 | Presentation | 5 |
| **Total** | | **25-27 hours** |

---

# HANDOFF CHECKLIST

After each layer, verify handoff before proceeding:

## Layer 1 â†’ Layer 2 Handoff
- [ ] All 7 collection tasks complete
- [ ] CSV files delivered to project
- [ ] File naming follows convention
- [ ] No obvious errors (can open in Excel)
- [ ] Rotation ETFs (SPY, TLT, XLF, XLU, IWM) included in tradfi_benchmark_data.csv

## Layer 2 â†’ Layer 3 Handoff
- [ ] Validation report complete
- [ ] Overall verdict: PASS or CONDITIONAL PASS
- [ ] Any issues documented
- [ ] Validated files clearly marked

## Layer 3 â†’ Layer 4 Handoff
- [ ] Battle Test results complete
- [ ] Monte Carlo results complete
- [ ] Risk metrics calculated
- [ ] Anomalies flagged

## Layer 4 â†’ Layer 5 Handoff
- [ ] Triggers evaluated
- [ ] Alerts consolidated
- [ ] Regime classified
- [ ] Strategy recommendations ready

## Layer 5 â†’ Output
- [ ] Content assembled
- [ ] Personas adapted
- [ ] Legal review passed
- [ ] Localization complete
- [ ] Gate 4 approved

---

# COPY-PASTE PROMPTS

Below are ready-to-use prompts for each chat.

---

## Prompt for Rakia Researcher (Layer 1)

```
Hi Rakia Researcher,

We are doing a manual dry run of the complete data pipeline. This is a fresh start - treat this as the first time collecting data.

Please start with Task 1.1: Macro Economics Data

**Data Required:**
- US Treasury Yields (2Y, 5Y, 10Y, 30Y) from FRED â€” 2020-01-01 to today
- US M2 Money Supply from FRED â€” 2020-01 to latest
- Real Yields (10Y TIPS) from FRED â€” 2020-01-01 to today

**Deliverables:**
1. treasury_yields.csv â€” columns: date, yield_2y, yield_5y, yield_10y, yield_30y
2. global_liquidity.csv â€” columns: date, us_m2_bn, us_m2_yoy
3. real_yields.csv â€” columns: date, real_yield_10y

Please confirm when complete, then we'll proceed to Task 1.2.
```

---

## Prompt for Rakia Data Validator (Layer 2)

```
Hi Rakia Data Validator,

Rakia Researcher has completed Layer 1 data collection. Please perform validation.

Start with Task 2.1: Tier 1 Structural Validation

**Files to Validate:** [list files from Layer 1]

**Checks Required:**
- Schema: All required columns present
- Data Types: Dates parseable, numbers numeric
- Completeness: <5% null values
- Format: Consistent YYYY-MM-DD dates
- Year Check: All years are 2020-2026 (no truncated years)
- Duplicates: No duplicate rows

Please provide tier1_validation_report.json with pass/fail for each file.
```

---

## Prompt for QR Board (Layer 3)

```
Hi QR Board,

Validated data is ready from Layer 2. Please perform analytics.

Start with Task 3.1: Battle Test Analysis

**Scenarios to Test:**
- COVID Crash: Feb 19 - Mar 23, 2020
- FTX Collapse: Nov 1 - Nov 30, 2022
- Terra/Luna: May 1 - May 15, 2022
- 2022 Bear Market: Full year
- 2023 Recovery: Full year

**Deliverables:**
- battle_test_results.json
- battle_test_summary.md

Please apply validation criteria CV-01 through CV-07.
```

---

## Prompt for Strategy Board (Layer 4)

```
Hi Strategy Board,

Analytics are complete from Layer 3. Please perform intelligence processing.

Start with Task 4.1: Trigger Evaluation

**Input:** Battle Test results, Monte Carlo results, Risk Metrics, Anomalies

**Evaluate triggers for:**
- Rebalancing needs
- Risk alerts
- Opportunities
- Crisis indicators

**Deliverable:** triggered_actions.json with priority and recommended actions
```

---

## Prompt for CMO Board (Layer 5)

```
Hi CMO Board,

Intelligence outputs are ready from Layer 4. Please assemble Adelaide content.

Start with Task 5.1: Content Assembly

**Sections needed:**
- Market Snapshot (150 words)
- Whale Watch (100 words)
- Your Strategies (200 words)
- Adelaide's Insight (100 words)

**Deliverables:**
- adelaide_daily_draft.md
- adelaide_daily_data.json

Content budget: Max 100KB
```

---

## Prompt for CLO Board (Layer 5 - Legal)

```
Hi CLO Board,

CMO Board has drafted Adelaide content. Please perform legal review.

Task 5.3: Legal Compliance Review

**Checks Required:**
- Disclaimers present for EU, US, BR
- No investment advice language
- All statistics from QR-approved list
- Risk warnings before yield mentions
- Fee disclosure accurate

**Deliverable:** clo_review_result.json with pass/fail and required edits
```

---

*End of Manual Pipeline Execution Guide v3*
