# Macro Operating System

> A coherent, actionable framework for market monitoring and diagnosis. Not a list of data points—a transmission map of how markets actually move.

---

## How to Use This System

**Core principle:** Core tells you *what's happening*. The numbered categories tell you *why* and *whether it's real*. The Regime Filter tells you *where to look first*.

**Daily workflow:**
1. Scan Core Dashboard (Category 0) — vital signs only, 30 seconds
2. Change Detection — what moved, what's accelerating, what's diverging
3. Identify which of the 7 Canonical Patterns is active
4. Follow the routing logic to the relevant categories
5. Use Linkage Maps to trace causation, not just correlation
6. Apply Validation Rules to avoid misdiagnosis

**Design rules:**
- Core is vital signs, not the entire blood panel
- Every indicator earns its place with a "So What"
- Track trend breaks and acceleration, not magic thresholds
- Levels lie; changes tell the truth

**Four-Quadrant Mental Model:**

```
         FRONTLINE MONITORING              DEEP DIAGNOSTICS
       ┌─────────────────────────┐     ┌─────────────────────────┐
       │ 0) Core Dashboard       │     │ 5) Credit               │
       │ 1) Equities             │     │ 9) Funding Stress       │
 LIVE  │ 2) Equity Internals     │     │ 14) Options Micro       │
       │ 3) Rates                │     │ 17) Market Functioning  │
       │ 8) Volatility           │     │ 19) Systematic Flows    │
       │ 12) Flows               │     │ 22) Crypto Satellite    │
       └─────────────────────────┘     └─────────────────────────┘
                    │                              │
                    ▼                              ▼
         FUNDAMENTAL DRIVERS               STRUCTURAL FORCES
       ┌─────────────────────────┐     ┌─────────────────────────┐
       │ 4) Real Rates/Inflation │     │ 10) Global Liquidity    │
       │ 26) Labor & Wages       │     │ 11) Global Anchors      │
 SLOW  │ 27) Growth & GDP        │     │ 21) Housing & MBS       │
       │ 28) Inflation Prints    │     │ 23) Geopolitics         │
       │ 29) Profits & Margins   │     │ 30) Fiscal & Debt       │
       └─────────────────────────┘     └─────────────────────────┘
```

**Quadrant logic:**
- **Frontline:** What's happening now? Check daily.
- **Diagnostics:** Is something breaking? Check when Frontline signals stress.
- **Fundamental:** Why is this happening? Check to validate or reject hypotheses.
- **Structural:** What slow forces matter? Check weekly or when regimes shift.

**Flow between quadrants:**
- Frontline stress → Check Diagnostics for confirmation
- Diagnostics confirm → Check Fundamentals for "why"
- Fundamentals unclear → Check Structural forces for regime context

---

## Default Data Transforms

Raw levels often mislead. Apply these transforms by default:

| Transform | Use Case | Example |
|-----------|----------|---------|
| **Δ1d / Δ1w / Δ1m** | Detect momentum shifts | HY spread +25bps in 3 days matters more than level |
| **% change** | Normalize across series | 10Y yield +5% vs gold -2% |
| **Rolling percentile (1–5y)** | Context for "extreme" readings | VIX at 95th percentile vs history |
| **Z-score** | Cross-series comparison | Funding stress z-score vs credit z-score |

**Rule of thumb:** When in doubt, look at the 1-week change and the 1-year percentile rank.

**Primary alert logic:** Use z-score > 2 or percentile > 95% as the primary trigger, with fixed levels as intuition checks only.

---

## 0) Core Dashboard (Always-On Vital Signs)

*Target: 12–14 lines maximum. Glanceable in 30 seconds.*

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `sp500_close` | Broad US risk-on/off baseline | Daily |
| `qqq_close` | Growth/duration regime barometer | Daily |
| `iwm_close` | Cyclical risk appetite confirmation | Daily |
| `vix_close` | Equity stress price | Daily |
| `move_index` | Rates volatility — often the real troublemaker | Daily |
| `ust_3m_yield` | Cash hurdle rate for everything | Daily |
| `ust_2y_yield` | Policy expectations + recession odds | Daily |
| `ust_10y_yield` | Global discount rate | Daily |
| `curve_10y_minus_2y` | Curve regime (growth/recession signal) | Daily |
| `tips_10y_real_yield` | Valuation gravity for duration assets | Daily |
| `hy_oas_spread` | First "credit is cracking" alarm | Daily |
| `dxy_index` | USD strength (fixed-basket index) | Daily |
| `wti_close` | Energy/inflation/geopolitical shock barometer | Daily |

**Conditional promotions to Core** (based on active regime):
- `gold_close` — promote during real-rate stress or geopolitical regimes
- `global_pmi_flash` — promote when growth regime is in question (monthly, step-function update)

---

## 1) Equities (Direction + Leadership)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `sp500_close` | Broad trend | Daily |
| `qqq_close` | Growth leadership | Daily |
| `iwm_close` | Cyclical confirmation | Daily |
| `acwi_close` | Global breadth (US-only vs global move) | Daily |
| `xlf_close` | Curve/credit-cycle thermometer | Daily |
| `xlu_close` | Defensive "bond proxy" leadership | Daily |
| `xlre_close` | Real-estate transmission of rates/credit | Daily |
| `xhb_close` | Housing sensitivity to rates (soft vs hard landing tell) | Daily |
| `soxx_close` | Capex cycle proxy (modern "transports") | Daily |
| `xlk_close` | Tech sector leadership (granular vs QQQ) | Daily |

---

## 2) Equity Internals (Move Quality, Not Just Direction)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `breadth_pct_above_50dma` | Short-term participation | Daily |
| `breadth_pct_above_200dma` | Long-trend health | Daily |
| `nyse_advance_decline_line` | Participation divergence warning | Daily |
| `rsp_close` | "Real market" vs mega-cap concentration (equal-weight S&P) | Daily |
| `iwm_spy_ratio` | Risk appetite / cyclicality gauge *(see Derived Series)* | Daily |
| `mgk_spy_ratio` | Mega-cap dominance — instant concentration risk read *(see Derived Series)* | Daily |
| `mag7_market_cap_pct` | Mag7 as % of S&P 500 market cap *(see Data Dictionary)* | Daily |

---

## 3) Rates (Treasury Curve + Duration Proxies)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `ust_3m_yield` | Cash return baseline | Daily |
| `ust_2y_yield` | Front-end policy pricing | Daily |
| `ust_5y_yield` | Belly of the curve | Daily |
| `ust_10y_yield` | Global discount rate benchmark | Daily |
| `ust_30y_yield` | Long duration + term premium | Daily |
| `curve_10y_minus_2y` | Primary curve regime signal *(see Derived Series)* | Daily |
| `curve_30y_minus_10y` | Long-end steepness *(see Derived Series)* | Daily |
| `curve_5y_minus_2y` | Near-term policy path *(see Derived Series)* | Daily |
| `shy_close` | Tradable short duration | Daily |
| `ief_close` | Tradable intermediate duration | Daily |
| `tlt_close` | Tradable long duration | Daily |

---

## 4) Real Rates & Inflation Expectations (Why Yields Moved)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `tips_5y_real_yield` | Real discount rate, medium-term | Daily |
| `tips_10y_real_yield` | Real discount rate, benchmark | Daily |
| `tips_30y_real_yield` | Real discount rate, long-term | Daily |
| `breakeven_10y` | Market inflation expectations (10Y nominal minus TIPS) *(see Derived Series)* | Daily |
| `breakeven_5y5y` | Forward inflation expectations (strips out near-term noise) | Daily |
| `trimmed_mean_pce` | "True" inflation trend, Dallas Fed (less noise) | Monthly |
| `median_cpi` | "True" inflation trend, Cleveland Fed | Monthly |
| `cleveland_fed_inflation_nowcast` | Live inflation estimate | Daily |

---

## 5) Credit (Spreads + Diagnostics)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `hy_oas_spread` | Weakest borrowers' stress gauge | Daily |
| `ig_oas_spread` | Broad investment-grade funding conditions | Daily |
| `hy_ccc_minus_bb_spread` | Where the rot concentrates first (CCC widens before BB) *(see Derived Series)* | Daily |
| `leveraged_loan_spread` | Floating-rate junk stress | Daily |
| `cdx_ig` | Institutional IG credit stress (derivatives) | Daily |
| `cdx_hy` | Institutional HY credit stress (derivatives) | Daily |
| `bank_cds_index` | Plumbing/financial system risk | Daily |
| `embi_spread` | EM sovereign stress canary | Daily |
| `hy_default_rate` | Validates whether spreads reflect real solvency risk | Monthly |
| `hy_distress_ratio` | % of HY trading at distressed levels | Weekly |

---

## 6) FX (Global Financial Conditions)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `dxy_index` | USD strength — ICE US Dollar Index, fixed-basket (EUR 57.6%, JPY 13.6%, GBP 11.9%, CAD 9.1%, SEK 4.2%, CHF 3.6%) | Daily |
| `eurusd` | US vs Europe macro divergence | Daily |
| `usdjpy` | Carry trade + Japan flow stress signal | Daily |
| `usdcny` | China policy + trade tension barometer | Daily |
| `em_fx_index` | Broad EM currency stress (risk-off shows here first) | Daily |
| `audusd` | Commodity-currency proxy (China/resources exposure) | Daily |

**Note on DXY vs Trade-Weighted:** DXY is a fixed-basket index dominated by EUR (not trade-weighted). For true trade-weighted USD conditions, use Fed's TWEXB (Broad) or TWEXM (Major Currencies) series from FRED.

---

## 7) Commodities (Inflation Impulse + Cycle)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `wti_close` | US oil benchmark, macro shock barometer | Daily |
| `brent_close` | Global oil benchmark | Daily |
| `gold_close` | Hedge demand + real-rate sensitivity | Daily |
| `copper_close` | Industrial cycle / China sensitivity | Daily |
| `bcom_index` | Broad commodity inflation impulse | Daily |
| `natgas_close` | Regional energy stress | Daily |
| `wheat_close` | Food inflation/supply shocks | Daily |
| `corn_close` | Food inflation/supply shocks | Daily |
| `soy_close` | Food inflation/supply shocks | Daily |

---

## 8) Volatility (Equity + Rates)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `vix_close` | Headline equity stress | Daily |
| `vix_term_structure` | Front vs back months — stress-now vs calm-carry regime *(see Derived Series)* | Daily |
| `vvix` | Volatility of volatility — fear acceleration | Daily |
| `skew_index` | Tail-risk pricing (OTM puts vs calls) | Daily |
| `move_index` | Rates volatility stress channel | Daily |
| `spx_realized_vol_20d` | What actually happened (vs implied) *(see Derived Series)* | Daily |
| `vol_risk_premium` | Implied minus realized — carry regime vs hidden danger *(see Derived Series)* | Daily |

---

## 9) Funding Stress (Money-Market Plumbing)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `sofr_ff_spread` | SOFR minus Fed Funds effective — secured vs unsecured funding gap | Daily |
| `fra_ois_spread` | Forward rate agreement stress *(subscription required; see Proxy Ladder)* | Daily |
| `repo_gc_rate` | General collateral repo rate (use SOFR as proxy if direct unavailable) | Daily |
| `cross_currency_basis_eurusd` | Global USD scarcity (Europe) | Daily |
| `cross_currency_basis_usdjpy` | Global USD scarcity (Japan) | Daily |
| `cp_spread` | Commercial paper funding stress | Daily |

**Note on SOFR:** SOFR is a secured overnight rate that serves as proxy for GC repo. The `sofr_ff_spread` measures the gap between secured funding (SOFR) and the unsecured policy rate (Fed Funds effective). This is NOT an OIS spread — it's a funding/policy gap indicator.

**Note on FRA-OIS:** The `fra_ois_spread` requires Bloomberg or similar subscription. If unavailable, rely on `sofr_ff_spread` + `repo_gc_rate` + `cp_spread` + cross-currency basis, which together capture funding stress adequately. See Proxy Ladder for alternatives.

---

## 10) Global Liquidity (Slow + Policy Liquidity)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `us_m2_level` | US broad money supply | Monthly |
| `us_m2_yoy` | US money supply acceleration *(see Derived Series)* | Monthly |
| `china_m2_yoy` | Global marginal liquidity driver | Monthly |
| `ecb_m3_yoy` | Europe liquidity pulse | Monthly |
| `fed_balance_sheet` | Fed QE/QT impulse | Weekly |
| `ecb_balance_sheet` | ECB QE/QT impulse | Weekly |
| `boj_balance_sheet` | BOJ policy stance | Weekly |
| `pboc_balance_sheet` | PBOC liquidity injections | Monthly |
| `global_m2_yoy_weighted` | Clean "global liquidity" summary *(see Derived Series)* | Monthly |

---

## 11) Global Macro Anchors (Non-US Gravity)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `germany_10y_bund_yield` | Europe discount rate anchor | Daily |
| `france_oat_minus_bund` | Eurozone stress detector (primary signal for EU fiscal risk) *(see Derived Series)* | Daily |
| `italy_btp_minus_bund` | Eurozone periphery stress *(see Derived Series)* | Daily |
| `japan_10y_jgb_yield` | Carry/flow rerouting risk | Daily |
| `eem_close` | EM equity stress amplifier | Daily |
| `china_tsf_yoy` | China total social financing growth | Monthly |
| `china_credit_impulse` | China cycle driver (leading indicator) | Monthly |

---

## 12) Flows (Literal Money In/Out)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `etf_flow_spy` | S&P 500 allocation shifts | Daily |
| `etf_flow_qqq` | Growth/tech allocation shifts | Daily |
| `etf_flow_iwm` | Small-cap allocation shifts | Daily |
| `etf_flow_tlt` | Long duration demand | Daily |
| `etf_flow_ief` | Intermediate duration demand | Daily |
| `etf_flow_shy` | Cash proxy demand | Daily |
| `etf_flow_hyg` | HY credit risk appetite in dollars | Daily |
| `etf_flow_lqd` | IG credit demand | Daily |
| `etf_flow_gld` | Hedge demand in dollars | Daily |
| `money_market_fund_assets` | "Cash on the sidelines" actually measurable | Weekly |

---

## 13) Positioning (Who's Offsides)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `cftc_net_sp500` | Equity futures positioning — squeeze/air-pocket risk | Weekly (Fri release) |
| `cftc_net_nasdaq` | Tech futures positioning | Weekly (Fri release) |
| `cftc_net_ust_2y` | 2Y Treasury positioning — crowded trades = violent moves | Weekly (Fri release) |
| `cftc_net_ust_10y` | 10Y Treasury positioning | Weekly (Fri release) |
| `cftc_net_usd` | Dollar positioning — crowding = global tightening risk | Weekly (Fri release) |
| `cftc_net_gold` | Gold positioning vs fundamentals | Weekly (Fri release) |
| `cftc_net_wti` | Oil positioning vs fundamentals | Weekly (Fri release) |

---

## 14) Options Microstructure (Why Price Action Gets Weird)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `put_call_ratio_10d` | Hedging vs speculation regime *(see Derived Series)* | Daily |
| `spx_oi_by_strike` | Pin/risk "magnet" zones | Daily |
| `dealer_gamma_exposure` | Chop vs trend/air pockets (positive = damping, negative = amplifying) | Daily |
| `charm_vanna_proxy` | Dealer hedging flow accelerants | Daily |
| `zero_dte_volume_share` | Intraday fragility from 0DTE options *(see Derived Series)* | Daily |

---

## 15) Treasury Supply & Auctions (Rates Move for Boring Reasons)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `treasury_net_issuance` | Supply pressure on yields | Monthly |
| `issuance_mix_bills_vs_coupons` | Duration supply vs liquidity effect | Monthly |
| `auction_tail` | Demand weakness (higher = worse demand) | Per auction |
| `auction_bid_to_cover` | Demand strength | Per auction |
| `auction_dealer_takedown_pct` | Forced dealer absorption (higher = weaker real demand) | Per auction |

---

## 16) Swaps & Inflation Swaps (Rates Plumbing)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `sofr_swap_2y` | Clean 2Y policy/term pricing | Daily |
| `sofr_swap_5y` | Clean 5Y pricing | Daily |
| `sofr_swap_10y` | Clean 10Y pricing | Daily |
| `swap_spread_10y` | Hedging/stress between swaps and cash Treasuries *(see Derived Series)* | Daily |
| `inflation_swap_5y` | Inflation expectations (cleaner than breakevens) | Daily |
| `inflation_swap_10y` | Long-term inflation pricing | Daily |

---

## 17) Market Functioning & Liquidity (Can You Even Trade It)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `spy_bid_ask_spread` | Equity market liquidity | Daily |
| `es_market_depth` | S&P futures depth — thin markets gap harder | Daily |
| `ust_market_depth` | Treasury liquidity stress | Daily |
| `hyg_bid_ask_spread` | HY credit tradability | Daily |
| `lqd_bid_ask_spread` | IG credit tradability | Daily |
| `trace_credit_volume` | Credit market activity | Daily |

---

## 18) Correlation & Regime (When Diversification Dies)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `equity_bond_corr_60d` | Bonds hedging stocks vs "everything sells off" *(see Derived Series)* | Daily |
| `cross_asset_corr_index` | "One trade" market risk *(see Derived Series)* | Daily |
| `spx_dispersion` | Concentrated index vs stock-pickers' market | Daily |

---

## 19) Systematic Flows (Robots)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `cta_trend_signal` | Persistent forced buying/selling from trend followers | Daily |
| `vol_target_exposure_proxy` | Deleveraging risk when vol rises | Daily |
| `risk_parity_stress_proxy` | Cross-asset forced selling risk | Daily |

---

## 20) Event Risk Calendar (Scheduled Ambushes)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `fed_meeting_dates` | Volatility clustering around FOMC | Calendar |
| `fed_dotplot_dates` | Policy projection updates | Calendar |
| `cpi_release_dates` | High-impact inflation prints | Calendar |
| `pce_release_dates` | Fed's preferred inflation measure | Calendar |
| `nfp_release_dates` | Labor market prints | Calendar |
| `ism_release_dates` | PMI releases | Calendar |
| `cpi_surprise` | Actual minus consensus *(see Derived Series)* | Per release |
| `nfp_surprise` | Actual minus consensus *(see Derived Series)* | Per release |
| `pmi_surprise` | Actual minus consensus *(see Derived Series)* | Per release |

---

## 21) Housing & MBS Transmission (The Missing Bridge)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `mortgage_rate_30y` | Real household hurdle rate | Weekly (Freddie Mac PMMS, Thursday) |
| `mortgage_spread_vs_10y` | "Is transmission broken?" — wide spread = broken *(see Derived Series)* | Weekly |
| `mbs_oas` | MBS credit/liquidity filter | Daily |
| `mortgage_apps_purchase` | Real-time housing demand | Weekly |
| `mortgage_apps_refi` | Rate sensitivity response | Weekly |
| `cmbs_spread` | Commercial real estate stress channel | Daily |
| `mortgage_delinquency_rate` | Slow validation of housing stress | Quarterly |

---

## 22) Crypto Satellite (Fringe Liquidity Thermometer)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `btc_close` | Risk appetite at the edges | Daily |
| `eth_close` | Alt-crypto risk appetite | Daily |
| `stablecoin_market_cap` | "Shadow dry powder" proxy | Daily |
| `btc_funding_rate` | Leverage temperature in crypto | Daily |
| `btc_basis` | Futures vs spot — leverage indicator *(see Derived Series)* | Daily |
| `btc_realized_vol` | Crypto stress impulse *(see Derived Series)* | Daily |

---

## 23) Geopolitics & Supply Chain Proxies (Market-Based)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `ovx` | Oil implied volatility — geopolitical smoke detector | Daily |
| `bdi_index` | Baltic Dry Index — global trade cycle pulse | Daily |
| `scfi_index` | Shanghai container freight — supply-chain inflation risk | Weekly |
| `defense_etf_close` | ITA/XAR — geopolitical risk bid | Daily |
| `rare_earth_price_index` | Strategic mineral/tech supply chain stress | Weekly |

---

## 24) Sentiment, Leverage & Fragility

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `margin_debt_level` | Leverage in the system | Monthly |
| `margin_debt_yoy` | Leverage acceleration — drawdown amplifier when turns down *(see Derived Series)* | Monthly |
| `naaim_exposure_index` | Active manager risk posture | Weekly |
| `aaii_bull_bear_spread` | Retail extremes (contrarian signal) *(see Derived Series)* | Weekly |

---

## 25) Tech / Capex Cycle (AI-Era Growth Engine Proxy)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `soxx_close` | Semiconductor/hardware capex cycle lead | Daily |
| `soxx_qqq_ratio` | Hardware reality vs software narrative *(see Derived Series)* | Daily |
| `global_semi_sales_yoy` | Real demand confirmation beyond stock prices | Monthly |

---

## 26) Labor & Wages (Fed Constraint + Recession Triggers)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `initial_claims_4wk_avg` | Fastest labor inflection signal | Weekly |
| `continuing_claims` | Confirms persistence of layoffs | Weekly |
| `unemployment_rate_u3` | Headline unemployment (lagging but important) | Monthly |
| `unemployment_rate_u6` | Broader slack measure | Monthly |
| `sahm_rule_indicator` | Recession trigger framework | Monthly |
| `jolts_job_openings` | Labor demand | Monthly |
| `jolts_quits_rate` | Worker confidence | Monthly |
| `eci_yoy` | Employment Cost Index — wage inflation persistence | Quarterly |
| `avg_hourly_earnings_yoy` | Monthly wage proxy *(see Derived Series)* | Monthly |
| `atlanta_fed_wage_tracker` | Cleanest wage inflation for marginal worker | Monthly |
| `prime_age_lfpr` | Labor supply signal (cleaner than headline LFPR) | Monthly |

---

## 27) Growth & GDP (Leading Activity + Nowcasts)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `gdp_nowcast_atlanta` | Atlanta Fed GDPNow — live growth estimate | Weekly |
| `gdp_nowcast_ny` | NY Fed nowcast | Weekly |
| `ism_pmi_mfg` | Manufacturing cycle direction | Monthly |
| `ism_pmi_services` | Services cycle direction | Monthly |
| `pmi_new_orders` | Leading edge of demand | Monthly |
| `industrial_production_yoy` | Real output pulse *(see Derived Series)* | Monthly |
| `retail_sales_control_yoy` | Consumer engine health (ex-autos, gas, building) *(see Derived Series)* | Monthly |
| `housing_starts` | Rate-sensitive growth channel | Monthly |
| `building_permits` | Forward housing activity | Monthly |

---

## 28) Inflation Prints (What Drives the Reaction Function)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `cpi_core_mom_sa` | Trend signal markets actually trade *(see Derived Series)* | Monthly |
| `core_pce_mom_sa` | Fed's preferred trend measure *(see Derived Series)* | Monthly |
| `cpi_shelter_mom` | Sticky inflation block | Monthly |
| `owners_equivalent_rent_mom` | Housing inflation component | Monthly |
| `import_price_ex_petro_yoy` | Tariff/imported inflation early warning *(see Derived Series)* | Monthly |
| `atlanta_fed_wage_tracker` | Wage-price spiral monitor | Monthly |

---

## 29) Profits, Margins & Earnings Reality

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `forward_eps_sp500` | Profit baseline for valuation | Weekly |
| `earnings_revision_breadth` | Upstream profit cycle signal (positive = upgrades > downgrades) | Weekly |
| `equity_risk_premium` | Earnings yield minus real yield — valuation pressure *(see Derived Series)* | Daily |
| `unit_labor_costs_yoy` | Wage pressure hitting margins *(see Derived Series)* | Quarterly |
| `productivity_growth_yoy` | Growth-without-inflation possibility *(see Derived Series)* | Quarterly |

---

## 30) Fiscal & Debt Sustainability (Macro Gravity)

| Indicator | So What | Frequency |
|-----------|---------|-----------|
| `debt_to_gdp` | Long-run constraint, term premium risk | Quarterly |
| `budget_deficit_12m` | Rolling deficit — fiscal thrust | Monthly |
| `deficit_to_gdp` | Fiscal stance relative to economy | Quarterly |
| `primary_deficit` | Deficit ex-interest — underlying fiscal stance | Quarterly |
| `net_interest_outlays` | Servicing drag and political constraint | Monthly |
| `interest_to_revenue_ratio` | Live fiscal stress (more responsive than debt/GDP) | Monthly |
| `term_premium_acm` | "Yields up because compensation" detector | Daily |

---

## 31) Regime Filter & Linkage Engine (Prioritization Layer)

> **This is not more data. This is instructions.**

### The 7 Canonical Patterns

Use these to diagnose *what kind of move* you're seeing before asking *what it means*.

---

### Pattern 0: Goldilocks / Liquidity-Driven Rally

**Signature:** Falling vol, narrowing spreads, steepening curve, positive flows, improving breadth

**Detection signals:**
- `vix_close` < 15 and declining
- `hy_oas_spread` < 350bps and narrowing
- `curve_10y_minus_2y` steepening (growth optimism)
- `global_m2_yoy_weighted` improving or QT slowing
- `etf_flow_spy` positive
- `money_market_fund_assets` declining (cash moving to risk)
- `breadth_pct_above_50dma` > 60% and rising

**First check:** 10) Global Liquidity → 12) Flows → 5) Credit (spreads narrowing)

**Then check:** 3) Rates (curve shape) → 19) Systematic (CTA buying) → 2) Internals (breadth)

**Key insight:** This is the "everything works" regime. Focus on growth sectors and duration assets. Watch for late-cycle exuberance: margin debt spikes, retail FOMO (AAII bulls extreme), concentration risk (Mag7 cap % rising).

**Most likely transitions:**
- → Pattern 2 (Growth Scare): PMI misses, earnings revisions turn negative
- → Pattern 3 (Inflation Shock): Commodities spike, breakevens surge unexpectedly

---

### Pattern 1: Liquidity Crisis

**Signature:** Funding stress leads → credit follows → equities last

**Detection signals:**
- `sofr_ff_spread` spiking above 15bps
- `repo_gc_rate` elevated vs policy rate
- `cross_currency_basis_eurusd` or `_usdjpy` widening beyond -30bps
- `dxy_index` surging
- Credit spreads widening but equities still holding

**First check:** 9) Funding Stress → 17) Market Functioning → 6) FX

**Then check:** 5) Credit → 12) Flows → 8) Volatility

**Most likely transitions:**
- → Pattern 6 (Credit Event): Funding stress persists, weakest borrowers crack
- → Pattern 0 (Goldilocks): Central bank intervention, liquidity restored

---

### Pattern 2: Growth Scare

**Signature:** PMIs roll over → earnings revisions turn negative → credit widens → equities follow

**Detection signals:**
- `ism_pmi_mfg` or `pmi_new_orders` declining below 50
- `earnings_revision_breadth` turning negative
- `iwm_spy_ratio` declining (cyclicals underperforming)
- `curve_10y_minus_2y` flattening or inverting
- `initial_claims_4wk_avg` rising

**First check:** 27) Growth/GDP → 29) Profits/Revisions → 5) Credit

**Then check:** 1) Equities leadership → 2) Internals → 3) Rates (curve)

**Most likely transitions:**
- → Pattern 6 (Credit Event): Growth scare becomes solvency scare
- → Pattern 0 (Goldilocks): Data stabilizes, Fed pivots dovish

---

### Pattern 3: Inflation Shock

**Signature:** Breakevens spike → rates reprice → duration assets sell → everything follows

**Detection signals:**
- `breakeven_10y` surging
- `cpi_core_mom_sa` surprising to upside
- `import_price_ex_petro_yoy` accelerating
- Commodities (especially `wti_close`, `bcom_index`) spiking
- `atlanta_fed_wage_tracker` reaccelerating

**First check:** 28) Inflation prints → 4) Real rates/breakevens → 7) Commodities

**Then check:** 3) Rates (curve) → 16) Inflation swaps → 1) Equity sector rotation

**Note:** Promote `wti_close` and `gold_close` to Core during this regime.

**Most likely transitions:**
- → Pattern 5 (Fiscal Tantrum): Inflation forces higher-for-longer, fiscal concerns mount
- → Pattern 2 (Growth Scare): Fed overtightens, demand collapses

---

### Pattern 4: Positioning Unwind

**Signature:** Vol spikes, spreads calm, breadth collapses — technical, not fundamental

**Detection signals:**
- `vix_close` spiking but `hy_oas_spread` flat
- `dealer_gamma_exposure` flipping negative
- `cta_trend_signal` reversing
- `zero_dte_volume_share` elevated
- `spx_dispersion` spiking

**First check:** 14) Options microstructure → 13) Positioning → 19) Systematic flows

**Then check:** 17) Market Functioning → 8) Volatility → 12) Flows

**Key insight:** This is NOT a fundamental credit event. Don't panic-sell at the lows. Wait for positioning to clear.

**Most likely transitions:**
- → Pattern 0 (Goldilocks): Positioning clears, liquidity takes over
- → Pattern 2 or 6: If fundamental weakness was masked, it emerges

---

### Pattern 5: Fiscal / Supply Tantrum

**Signature:** Auction tails → term premium rises → curve steepens — yields up for "boring" reasons

**Detection signals:**
- `auction_tail` widening, `auction_bid_to_cover` declining
- `term_premium_acm` rising
- `ust_10y_yield` rising while `ust_2y_yield` stable or down
- `deficit_to_gdp` elevated, `treasury_net_issuance` heavy
- `interest_to_revenue_ratio` rising

**First check:** 15) Treasury Supply/Auctions → 30) Fiscal/Debt → 3) Rates (term premium/curve)

**Then check:** 16) Swaps → 6) FX → 10) Global Liquidity

**Most likely transitions:**
- → Pattern 3 (Inflation Shock): Fiscal expansion stokes inflation
- → Pattern 2 (Growth Scare): Higher rates choke growth

---

### Pattern 6: Credit Event (The Silent Leak)

**Signature:** HY/IG widening, bank CDS up, funding spreads widening — equities not reacting yet

**Detection signals:**
- `hy_oas_spread` and `ig_oas_spread` widening
- `bank_cds_index` creeping up
- `hy_ccc_minus_bb_spread` blowing out (stress concentrated in weakest names)
- `vix_close` relatively calm
- `sp500_close` still green

**First check:** 5) Credit → 9) Funding Stress → 17) Market Functioning

**Then check:** 12) Flows → 11) Global Anchors → 8) Volatility

**Key insight:** Equities are the last to admit it. Credit is the first to price it. This regime hurts people who only watch SPY and VIX.

**Most likely transitions:**
- → Pattern 1 (Liquidity Crisis): Credit event metastasizes to funding markets
- → Pattern 0 (Goldilocks): Central bank backstop, spreads compress

---

### Regime Transition Matrix

Markets don't jump randomly between patterns. Use this to anticipate what comes next:

| Current Pattern | Most Likely Next | Trigger to Watch |
|-----------------|------------------|------------------|
| 0 (Goldilocks) | 2 (Growth Scare) | PMI misses, earnings revisions turn negative |
| 0 (Goldilocks) | 3 (Inflation Shock) | Commodity spike, breakevens surge |
| 1 (Liquidity Crisis) | 6 (Credit Event) | Funding stress persists > 1 week |
| 1 (Liquidity Crisis) | 0 (Goldilocks) | Central bank intervention |
| 2 (Growth Scare) | 6 (Credit Event) | HY spreads break 500bps, defaults rise |
| 2 (Growth Scare) | 0 (Goldilocks) | Data stabilizes, Fed pivots |
| 3 (Inflation Shock) | 5 (Fiscal Tantrum) | Higher-for-longer narrative takes hold |
| 3 (Inflation Shock) | 2 (Growth Scare) | Fed overtightens |
| 4 (Positioning Unwind) | 0 (Goldilocks) | Positioning clears (usually 3-5 days) |
| 4 (Positioning Unwind) | 2 or 6 | Fundamental weakness was masked |
| 5 (Fiscal Tantrum) | 3 (Inflation Shock) | Fiscal expansion stokes demand |
| 5 (Fiscal Tantrum) | 2 (Growth Scare) | Higher rates choke activity |
| 6 (Credit Event) | 1 (Liquidity Crisis) | Contagion to funding markets |
| 6 (Credit Event) | 0 (Goldilocks) | Central bank backstop |

---

### Validation Rules (Avoiding Misdiagnosis)

Apply these sanity checks when patterns seem unclear or contradictory.

---

#### Validation Rule: Inflation Shock vs. Growth Scare

**If** `breakeven_10y` ↑ **AND** `pmi_new_orders` ↓ → **Contradiction!**

This is **stagflation worry**, not a clean inflation or growth pattern.

**Resolution:**
- Check 29) Profits → Are margins getting crushed?
- Key indicators: `unit_labor_costs_yoy` ↑ + `productivity_growth_yoy` ↓
- This regime is harder to trade — bonds won't hedge equities

---

#### Validation Rule: USD Strength Diagnosis

**If** `dxy_index` ↑ **AND** `ust_2y_yield` ↓ → **Abnormal!**

Not rate differentials driving USD — must be safe-haven flows.

**Resolution:**
- Check `cross_currency_basis` for USD scarcity
- Check `embi_spread` for EM stress
- Check `france_oat_minus_bund` or `italy_btp_minus_bund` for Europe stress
- This is **global risk-off**, not US strength

---

#### Validation Rule: Credit-Equity Divergence Time Limit

**If** `hy_oas_spread` widening >50bps **AND** `sp500_close` unchanged for >5 days → **High alert**

One market is wrong. Historically, equities converge to credit within 1–2 weeks.

**Resolution:**
- Check 12) Flows — who's selling credit?
- Check 13) Positioning — who's trapped?
- Prepare for equity catch-down or credit snapback

---

#### Validation Rule: Fiscal vs. Growth Contradiction

**If** `deficit_to_gdp` ↑ **AND** `gdp_nowcast_atlanta` ↓ → **Warning!**

Fiscal expansion isn't translating to growth. Possible causes:
- Crowding out (rates too high)
- Spending on transfer payments, not productive investment
- External drag (trade deficit widening)

**Resolution:**
- Check 30) Fiscal → Is interest burden consuming the expansion?
- Check 27) Growth → Where is the weakness concentrated?
- Check 28) Inflation → Is fiscal stoking prices without output?

---

### Linkage Maps (Tracing Causation)

Use these when a key indicator moves to understand *why* and *what else should move*.

---

#### `tips_10y_real_yield` ↑

**Immediate check:**
- `gold_close` ↓ ?
- `qqq_close` ↓ ?
- `equity_risk_premium` ↓ ?

**Then ask: WHY did it rise?**
- `breakeven_10y` ↓ → real rates up because inflation expectations fell
- `ust_10y_yield` (nominal) ↑ → real rates up because nominals rose

**If nominal yield ↑, check:**
- `auction_tail` ↑ ? → supply/demand issue (Pattern 5)
- `deficit_to_gdp` ↑ ? → fiscal pressure
- Fed speak hawkish? → policy repricing (check 20)

---

#### `hy_oas_spread` ↑

**Immediate check:**
- `ig_oas_spread` also ↑ ? → broad credit stress
- `bank_cds_index` ↑ ? → plumbing risk
- `sp500_close` / `iwm_close` ↓ ? → equity confirmation

**Then ask: WHERE is the stress?**
- `hy_ccc_minus_bb_spread` blowing out → stress in weakest names
- `leveraged_loan_spread` ↑ → floating-rate stress (rate-sensitive)
- `embi_spread` ↑ → EM contagion channel

**If credit widening but equities calm:** Check Pattern 6 — equities may be late

---

#### `dxy_index` ↑

**Immediate check:**
- `em_fx_index` ↓ ? → EM stress
- `cross_currency_basis` widening? → USD funding scarcity
- `usdjpy` ↑ ? → carry unwind risk

**Then ask: WHY is USD strong?**
- `ust_2y_yield` (US) ↑ vs foreign yields → rate differential
- `vix_close` ↑, `hy_oas_spread` ↑ → flight to safety
- Foreign stress? Check `france_oat_minus_bund`, `japan_10y_jgb_yield`

---

#### `vix_close` ↑

**First question: Is credit confirming?**
- `hy_oas_spread` ↑ → fundamental stress, take seriously
- `hy_oas_spread` flat → likely technical/positioning (Pattern 4)

**If technical, check:**
- `dealer_gamma_exposure` → flipped negative?
- `cta_trend_signal` → reversing?
- `zero_dte_volume_share` → elevated intraday fragility?

**If fundamental, check:** Pattern 2 (Growth Scare) or Pattern 6 (Credit Event)

---

#### `curve_10y_minus_2y` steepening with `ust_10y_yield` ↑

**This is unusual. Ask why:**
- `auction_tail` ↑, `treasury_net_issuance` heavy → supply tantrum (Pattern 5)
- `term_premium_acm` ↑ → investors demanding compensation
- `dxy_index` ↑, `usdjpy` moving → foreign selling (check Japan, China flows)

**Check:** 15) Treasury Supply → 30) Fiscal → 11) Global Anchors

---

## Quick Reference: Morning Triage Checklist

### Step 1: Scan Core Dashboard (30 seconds)
- Any major moves overnight?
- VIX/MOVE elevated?
- Curve shape changed?
- DXY moved significantly?
- HY spread moved?

### Step 2: Change Detection (60 seconds)

For each Core indicator that moved, compute:

| Indicator | Today | Δ1d | Δ5d | Δ20d | Acceleration? | Divergence? |
|-----------|-------|-----|-----|------|---------------|-------------|
| `sp500_close` | — | — | — | — | Δ5d vs Δ20d | vs VIX, HY |
| `vix_close` | — | — | — | — | Δ5d vs Δ20d | vs HY spread |
| `hy_oas_spread` | — | — | — | — | Δ5d vs Δ20d | vs equities |
| `dxy_index` | — | — | — | — | Δ5d vs Δ20d | vs 2Y yield |
| `curve_10y_minus_2y` | — | — | — | — | Δ5d vs Δ20d | vs term premium |

**Key questions:**
1. **What moved?** (Δ1d significant?)
2. **Is it accelerating?** (Δ5d > Δ20d in same direction?)
3. **Are related indicators confirming?** (VIX up but HY flat = warning)

**Example Change Matrix:**
```
              Today    Δ1d    Δ5d   Δ20d  Acceleration?  Divergence?
SP500       5892     +0.3%  +1.2%  +3.4%  No (slowing)   None
VIX         18.2     +13%   +22%   +15%   Yes            HY only +2% → VIX overshoot?
10Y-2Y      42bps    +2bps  +8bps  +15bps No (slowing)   Normal
HY Spread   385bps   +5bps  +32bps +45bps Yes            **Equities not reacting**
```

This 60-second scan tells you **what's new** before you diagnose **what it means**.

### Step 3: Pattern Recognition (1 minute)

| If you see... | Likely Pattern | First Check |
|---------------|----------------|-------------|
| Low vol, tight spreads, flows positive | 0 — Goldilocks | 10, 12, 5 |
| Funding spreads spiking, DXY up | 1 — Liquidity Crisis | 9, 17, 6 |
| PMIs down, revisions negative | 2 — Growth Scare | 27, 29, 5 |
| Breakevens up, commodities up | 3 — Inflation Shock | 28, 4, 7 |
| VIX up but HY flat, gamma negative | 4 — Positioning Unwind | 14, 13, 19 |
| Auction tails, term premium up | 5 — Fiscal Tantrum | 15, 30, 3 |
| Credit wide, equities calm | 6 — Credit Event | 5, 9, 17 |

### Step 4: Validate or Reject (2–3 minutes)
- Check the "first check" categories for that pattern
- If confirmed, check the "then check" categories
- Apply Validation Rules if signals are mixed
- If not confirmed, reassess — may be noise or a hybrid

### Step 5: Linkage Check (as needed)
- If a key indicator moved, trace the linkage map
- Ask "why did this move?" before "what does it mean?"

### Step 6: Check Transition Matrix
- What pattern could this become?
- What would trigger the transition?

---

## Example Triage: Putting It All Together

*Scenario: Monday morning, screens show mixed signals*

### Initial Core Scan (30 seconds)

| Indicator | Reading | Δ1w | Signal |
|-----------|---------|-----|--------|
| `sp500_close` | 5,892 | +0.3% | Calm |
| `vix_close` | 18.2 | +2.1 | Slightly elevated |
| `hy_oas_spread` | 385bps | +32bps | **Widening** |
| `dxy_index` | 104.2 | +0.8% | Firming |
| `curve_10y_minus_2y` | +42bps | +5bps | Steepening |
| `move_index` | 98 | +8 | Elevated |

**Initial read:** Credit stress without equity confirmation. VIX mildly elevated but not panicking.

### Change Detection (60 seconds)

| Indicator | Δ1d | Δ5d | Δ20d | Acceleration? | Divergence? |
|-----------|-----|-----|------|---------------|-------------|
| `sp500_close` | +0.1% | +0.3% | +2.1% | No (slowing) | — |
| `vix_close` | +8% | +13% | +22% | Yes (still rising) | HY confirming |
| `hy_oas_spread` | +8bps | +32bps | +45bps | **Yes (accelerating)** | **Equities not reacting** |
| `dxy_index` | +0.2% | +0.8% | +1.5% | No | Normal |

**Key finding:** HY spread acceleration + equity divergence = high alert signal.

### Pattern Recognition (1 minute)

Checking against the 7 patterns:
- Pattern 0 (Goldilocks)? No — HY widening, VIX rising
- Pattern 4 (Positioning Unwind)? Possible — VIX up but equities calm
- **Pattern 6 (Credit Event)?** Most likely — HY widening, equities ignoring it

### First Check: Categories 5, 9, 17 (2 minutes)

**5) Credit:**
- `hy_ccc_minus_bb_spread`: +48bps in 1 week → Stress concentrated in weakest names
- `bank_cds_index`: +12bps → Financial stress emerging
- `leveraged_loan_spread`: +25bps → Floating-rate pain

**9) Funding:**
- `sofr_ff_spread`: 8bps → Within normal range
- `cross_currency_basis_eurusd`: -18bps → Mild USD demand, not crisis

**17) Market Functioning:**
- `hyg_bid_ask_spread`: +40% vs last week → Credit liquidity deteriorating

**Diagnosis confirmed:** Pattern 6 (Credit Event) — silent leak. Funding is okay (not Pattern 1), but credit is pricing something equities haven't acknowledged.

### Validation Check

Applying Credit-Equity Divergence rule:
- HY widening >50bps? Yes (32bps in 1 week, accelerating)
- Equities unchanged? Yes (SPY +0.3%)
- Duration: 5+ days? Just starting

**High alert.** Historical precedent: equities converge to credit within 1-2 weeks.

### Then Check: Categories 12, 11 (1 minute)

**12) Flows:**
- `etf_flow_hyg`: -$1.2B last week → Credit outflows accelerating
- `etf_flow_spy`: +$0.4B → Equity flows still positive (divergence!)

**11) Global Anchors:**
- `france_oat_minus_bund`: +8bps → Mild Europe stress
- `embi_spread`: +22bps → EM also widening

### Conclusion & Action Framework

**Diagnosis:** Pattern 6 (Credit Event) in early stages. Equities haven't priced it yet.

**What to watch:**
- If `hy_oas_spread` breaks 400bps → Likely equity catch-down coming
- If `bank_cds_index` accelerates → Could transition to Pattern 1 (Liquidity Crisis)
- If spreads stabilize at current levels → Possible false alarm

**Regime transition probability:**
- → Pattern 1 (Liquidity Crisis): 25% if funding stress emerges
- → Pattern 0 (Goldilocks): 40% if this is a brief scare
- → Equity catch-down within Pattern 6: 35%

**Time spent:** ~5 minutes total

---

## Alert Thresholds with Contextual Triggers

**Primary rule:** Use z-score > 2 or percentile > 95% as the primary trigger. Fixed levels are intuition checks only — they drift over time.

### Single-Indicator Thresholds

| Indicator | Yellow Flag (Level) | Red Flag (Level) | Or Use |
|-----------|---------------------|------------------|--------|
| `vix_close` | > 20 | > 30 | > 90th %ile (5y) |
| `hy_oas_spread` | > 400bps | > 500bps | > 90th %ile (5y) |
| `sofr_ff_spread` | > 10bps | > 20bps | > 95th %ile (2y) |
| `initial_claims_4wk_avg` | > 250k | > 300k | > 90th %ile (5y) |
| `equity_bond_corr_60d` | > 0.3 | > 0.5 | > 90th %ile (5y) |
| `dealer_gamma_exposure` | Negative | Deeply negative | < 10th %ile |
| `auction_tail` | > 2bps | > 4bps | > 90th %ile (2y) |

### Contextual Triggers (Paired Conditions)

| Single Indicator | Yellow Flag | RED FLAG if ALSO... |
|------------------|-------------|---------------------|
| `vix_close` > 20 | Normal stress | `dealer_gamma_exposure` negative → air pocket risk |
| `hy_oas_spread` > 400bps | Expensive | `hy_ccc_minus_bb_spread` > 200bps → rot concentrated in weakest |
| `sofr_ff_spread` > 10bps | Some stress | `cross_currency_basis` < -30bps → global USD shortage |
| `initial_claims` > 250k | Labor softening | `continuing_claims` also rising → persistent, not one-off |
| `vix_close` > 25 | Elevated fear | `hy_oas_spread` flat → likely positioning, not fundamental |
| `ust_10y_yield` +20bps | Rates moving | `auction_tail` > 3bps → supply-driven, not growth optimism |
| `dxy_index` > 105 | USD strong | `ust_2y_yield` down → safe-haven flow, not rate differential |

---

## Data Dictionary (Exact Series Definitions)

Precision prevents silent errors. Use these specific series or document substitutions.

### Core & Rates

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `sp500_close` | S&P 500 Index closing price | Yahoo Finance | ^GSPC |
| `qqq_close` | Invesco QQQ ETF closing price | Yahoo Finance | QQQ |
| `iwm_close` | iShares Russell 2000 ETF closing price | Yahoo Finance | IWM |
| `vix_close` | CBOE Volatility Index | Yahoo Finance | ^VIX |
| `move_index` | ICE BofA MOVE Index (Treasury vol) | Bloomberg, ICE | — |
| `ust_3m_yield` | 3-Month Treasury Bill yield | FRED | DGS3MO |
| `ust_2y_yield` | 2-Year Treasury yield | FRED | DGS2 |
| `ust_5y_yield` | 5-Year Treasury yield | FRED | DGS5 |
| `ust_10y_yield` | 10-Year Treasury yield | FRED | DGS10 |
| `ust_30y_yield` | 30-Year Treasury yield | FRED | DGS30 |
| `tips_10y_real_yield` | 10-Year TIPS real yield | FRED | DFII10 |
| `dxy_index` | ICE US Dollar Index — **fixed-basket** (EUR 57.6%, JPY 13.6%, GBP 11.9%, CAD 9.1%, SEK 4.2%, CHF 3.6%). NOT trade-weighted. | Yahoo Finance | DX-Y.NYB |

### Credit

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `hy_oas_spread` | ICE BofA US High Yield OAS (bps) | FRED | BAMLH0A0HYM2 |
| `ig_oas_spread` | ICE BofA US Corporate IG OAS (bps) | FRED | BAMLC0A0CM |
| `hy_ccc_minus_bb_spread` | ICE BofA CCC OAS minus ICE BofA BB OAS. Positive = stress in weakest names. | FRED | BAMLH0A3HYC minus BAMLH0A1HYBB |
| `cdx_ig` | Markit CDX NA IG 5Y spread | Bloomberg, Markit | — |
| `cdx_hy` | Markit CDX NA HY 5Y spread | Bloomberg, Markit | — |
| `bank_cds_index` | Average 5Y CDS of major US banks (JPM, BAC, C, WFC, GS, MS) | Bloomberg | — |
| `embi_spread` | JPMorgan EMBI+ spread | Bloomberg | — |

### Equity Internals

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `mag7_market_cap_pct` | Sum of market caps of AAPL, MSFT, AMZN, NVDA, GOOGL, META, TSLA divided by S&P 500 total market cap, expressed as percentage. | Preferred: Index provider or Bloomberg. Fallback: Compute from individual market caps (Yahoo Finance) + S&P 500 total market cap proxy (SPY shares outstanding × price × IVV adjustment factor, or use ^GSPC constituents). | Calculate |

### Inflation & Real Rates

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `breakeven_10y` | 10Y nominal yield minus 10Y TIPS yield | FRED | T10YIE |
| `breakeven_5y5y` | 5Y5Y forward inflation expectation | FRED | T5YIFR |
| `trimmed_mean_pce` | Dallas Fed Trimmed Mean PCE (12-month) | FRED | PCETRIM12M159SFRBDAL |
| `median_cpi` | Cleveland Fed Median CPI | Cleveland Fed | — |
| `cpi_core_mom_sa` | Core CPI MoM, seasonally adjusted | FRED | CPILFESL (calculate MoM) |
| `core_pce_mom_sa` | Core PCE MoM, seasonally adjusted | FRED | PCEPILFE (calculate MoM) |

### Funding & Liquidity

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `sofr_ff_spread` | SOFR minus Fed Funds Effective Rate. This is a secured/unsecured funding gap, NOT an OIS spread. | FRED | SOFR minus FEDFUNDS |
| `fra_ois_spread` | 3-month FRA minus OIS rate. Measures forward funding stress expectations. **Requires Bloomberg/Reuters subscription.** If unavailable, rely on `sofr_ff_spread` + `repo_gc_rate` + `cp_spread` + cross-currency basis for funding stress assessment. | Bloomberg | — |
| `repo_gc_rate` | General collateral repo rate. Use SOFR as proxy if direct series unavailable. | FRED | SOFR |
| `cross_currency_basis_eurusd` | EUR/USD 3M cross-currency basis swap | Bloomberg | — |
| `fed_balance_sheet` | Federal Reserve total assets | FRED | WALCL |
| `us_m2_yoy` | M2 money supply YoY change | FRED | M2SL (calculate YoY) |

### Labor & Growth

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `initial_claims_4wk_avg` | Initial jobless claims 4-week average | FRED | IC4WSA |
| `continuing_claims` | Continued claims (insured unemployed) | FRED | CCSA |
| `unemployment_rate_u3` | Civilian unemployment rate | FRED | UNRATE |
| `sahm_rule_indicator` | Sahm Rule recession indicator. Uses SAHMCURRENT (current published value). Note: SAHMREALTIME exists for real-time research vintages. | FRED | SAHMCURRENT |
| `atlanta_fed_wage_tracker` | Atlanta Fed Wage Growth Tracker (3-month MA) | Atlanta Fed | — |
| `gdp_nowcast_atlanta` | Atlanta Fed GDPNow | Atlanta Fed | — |
| `ism_pmi_mfg` | ISM Manufacturing PMI | ISM | — |

### Fiscal

| Indicator | Definition | Source | Code/Ticker |
|-----------|------------|--------|-------------|
| `term_premium_acm` | Adrian-Crump-Moench 10Y term premium | NY Fed | — |
| `debt_to_gdp` | Federal debt held by public / GDP | FRED | GFDEGDQ188S |
| `net_interest_outlays` | Federal interest payments (monthly) | Treasury Monthly Statement | — |
| `interest_to_revenue_ratio` | Federal interest payments / Federal revenue | Treasury Monthly Statement | Calculate |

### Positioning & Options

| Indicator | Definition | Source |
|-----------|------------|--------|
| `cftc_net_sp500` | CFTC COT, E-mini S&P 500 net non-commercial | CFTC (Fri release, Tue data) |
| `dealer_gamma_exposure` | Model-based estimate of dealer gamma | SpotGamma, SqueezeMetrics, or DIY |
| `put_call_ratio_10d` | 10-day average equity put/call ratio | CBOE |

### Housing (Weekly frequency)

| Indicator | Definition | Source | Frequency |
|-----------|------------|--------|-----------|
| `mortgage_rate_30y` | Freddie Mac PMMS 30-year fixed rate | FRED | Weekly (Thursday) |
| `mortgage_apps_purchase` | MBA Purchase Applications Index | MBA | Weekly |
| `mortgage_apps_refi` | MBA Refinance Applications Index | MBA | Weekly |

---

## Derived Series Formulas

These indicators require calculation. Document your exact methodology to prevent "same label, different calculation" errors.

### Derived Series Registry

| Indicator | Formula | Inputs | Update | Unit |
|-----------|---------|--------|--------|------|
| `iwm_spy_ratio` | IWM / SPY | IWM close, SPY close | Daily | Ratio |
| `mgk_spy_ratio` | MGK / SPY | MGK close, SPY close | Daily | Ratio |
| `soxx_qqq_ratio` | SOXX / QQQ | SOXX close, QQQ close | Daily | Ratio |
| `curve_10y_minus_2y` | DGS10 - DGS2 | 10Y yield, 2Y yield | Daily | bps |
| `curve_30y_minus_10y` | DGS30 - DGS10 | 30Y yield, 10Y yield | Daily | bps |
| `curve_5y_minus_2y` | DGS5 - DGS2 | 5Y yield, 2Y yield | Daily | bps |
| `breakeven_10y` | DGS10 - DFII10 | 10Y nominal, 10Y TIPS | Daily | % |
| `mortgage_spread_vs_10y` | MORTGAGE30US - DGS10 | 30Y mortgage, 10Y yield | Weekly | bps |
| `hy_ccc_minus_bb_spread` | BAMLH0A3HYC - BAMLH0A1HYBB | ICE BofA CCC OAS, BB OAS | Daily | bps |
| `france_oat_minus_bund` | France 10Y - Germany 10Y | Sovereign yields | Daily | bps |
| `italy_btp_minus_bund` | Italy 10Y - Germany 10Y | Sovereign yields | Daily | bps |
| `swap_spread_10y` | 10Y SOFR swap - UST 10Y | Swap rate, Treasury | Daily | bps |
| `sofr_ff_spread` | SOFR - Fed Funds Effective | SOFR, FEDFUNDS | Daily | bps |
| `vix_term_structure` | VX1 / VX4 (or VIX / VIX3M) | VIX futures or spot | Daily | Ratio |
| `spx_realized_vol_20d` | StdDev(20d returns) × √252 | SPX daily returns | Daily | % |
| `vol_risk_premium` | VIX - spx_realized_vol_20d | VIX, realized vol | Daily | pts |
| `equity_risk_premium` | (1 / Fwd P/E) × 100 - DFII10 | Forward P/E, real yield | Daily | % |
| `global_m2_yoy_weighted` | 0.5×US + 0.25×China + 0.25×EU | M2 YoY series | Monthly | % |
| `equity_bond_corr_60d` | Corr(SPY, TLT, 60d) | Daily returns | Daily | Corr |
| `cross_asset_corr_index` | Avg pairwise corr (SPY, TLT, GLD, DXY) | Daily returns | Daily | Corr |
| `put_call_ratio_10d` | 10d SMA of CBOE P/C ratio | CBOE data | Daily | Ratio |
| `zero_dte_volume_share` | 0DTE vol / Total SPX vol | Options volume | Daily | % |
| `us_m2_yoy` | (M2 current / M2 12m ago) - 1 | M2SL | Monthly | % |
| `margin_debt_yoy` | (Margin current / 12m ago) - 1 | FINRA margin | Monthly | % |
| `avg_hourly_earnings_yoy` | (AHE current / 12m ago) - 1 | BLS AHE | Monthly | % |
| `industrial_production_yoy` | (INDPRO current / 12m ago) - 1 | INDPRO | Monthly | % |
| `retail_sales_control_yoy` | (Control current / 12m ago) - 1 | Census control group | Monthly | % |
| `import_price_ex_petro_yoy` | YoY import prices ex-petroleum | BLS | Monthly | % |
| `unit_labor_costs_yoy` | YoY unit labor costs | BLS | Quarterly | % |
| `productivity_growth_yoy` | YoY output per hour | BLS | Quarterly | % |
| `cpi_surprise` | Actual CPI - Consensus | Release data | Per release | % |
| `nfp_surprise` | Actual NFP - Consensus | Release data | Per release | k jobs |
| `pmi_surprise` | Actual PMI - Consensus | Release data | Per release | pts |
| `aaii_bull_bear_spread` | AAII Bulls% - Bears% | AAII survey | Weekly | % |
| `btc_basis` | (BTC futures / spot) - 1, annualized | CME, spot | Daily | % |
| `btc_realized_vol` | StdDev(20d returns) × √365 | BTC returns | Daily | % |
| `mag7_market_cap_pct` | (AAPL + MSFT + AMZN + NVDA + GOOGL + META + TSLA mkt cap) / SPX total mkt cap × 100 | Individual mkt caps, index total | Daily | % |

---

## Proxy Ladder (Hard-to-Source Metrics)

For each difficult series, here's a fallback chain:

### MOVE Index (Rates Volatility)

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | ICE BofA MOVE Index via Bloomberg | Bloomberg terminal |
| **Public proxy** | TYVIX (Treasury VIX) if available, or implied vol on TLT options | CBOE, options data |
| **DIY approximation** | 20-day realized vol of TLT × 1.2 adjustment factor | Calculate yourself |

### CDX Credit Indices

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | Markit CDX NA IG/HY via Bloomberg | Bloomberg terminal |
| **Public proxy** | HYG/LQD ETF option-implied spreads | Options data |
| **DIY approximation** | Track HYG price; 1% drop ≈ 15-20bps spread widening | Yahoo Finance |

### Cross-Currency Basis

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | Bloomberg 3M EUR/USD or USD/JPY basis swap | Bloomberg terminal |
| **Public proxy** | Watch for "dollar shortage" headlines; check TED spread as rough proxy | FRED (TEDRATE) |
| **DIY approximation** | Compare covered interest parity; deviation = basis | Requires FX forward data |

### FRA-OIS Spread

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | Bloomberg 3M FRA-OIS | Bloomberg terminal |
| **Public proxy** | Not directly available publicly. Use `sofr_ff_spread` as primary funding stress indicator instead. | FRED (calculate) |
| **DIY approximation** | Combine `sofr_ff_spread` + `cp_spread` + cross-currency basis for composite funding stress read. If all three are elevated, funding stress is confirmed even without FRA-OIS. | Multiple sources |

### Dealer Gamma Exposure

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | SpotGamma, SqueezeMetrics, or GEX from options analytics providers | Subscription |
| **Public proxy** | Large put OI at round strikes + falling prices = likely negative gamma | CBOE options data |
| **DIY approximation** | See code appendix for basic calculation using yfinance | Python + options data |

### CTA Trend Signal

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | SocGen CTA Index positioning estimates | Research subscription |
| **Public proxy** | CFTC COT positioning trends in major futures | CFTC (free, delayed) |
| **DIY approximation** | 50/200 DMA crossover direction on ES, ZN, ZB, GC, CL | Calculate yourself |

### Private Credit Spreads *(if tracking)*

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | Cliffwater Direct Lending Index | Subscription |
| **Public proxy** | Leveraged loan spreads (S&P LSTA Index) | Bloomberg, some FRED |
| **DIY approximation** | BDC NAV discounts (ARCC, MAIN, etc.) | Yahoo Finance |

### Mag7 Market Cap Percentage

| Tier | Source | Access |
|------|--------|--------|
| **Preferred** | Index provider or Bloomberg terminal | Subscription |
| **Public proxy** | Compare MGK (Vanguard Mega Cap Growth) to SPY as rough proxy for concentration | Yahoo Finance |
| **DIY approximation** | Sum individual market caps from Yahoo Finance (AAPL, MSFT, AMZN, NVDA, GOOGL, META, TSLA) and divide by S&P 500 total market cap estimate | Calculate yourself |

---

## Data Maintenance Notes

### Update Frequency Summary

| Frequency | What to Check |
|-----------|---------------|
| **Daily** | Core Dashboard, Equities, Rates, Credit spreads, FX, Commodities, Volatility, Market functioning, ETF prices |
| **Weekly** | Flows (ETF), Positioning (CFTC Fridays), Claims, Money market assets, Nowcasts, Mortgage rates/apps |
| **Monthly** | M2/liquidity, PMIs, Inflation prints, Labor (NFP, JOLTS), Housing starts, Earnings revisions |
| **Quarterly** | GDP, ECI, Productivity, Unit labor costs, Fiscal aggregates, Delinquencies |
| **Per Event** | Auctions (check day of), Fed meetings, CPI/PCE releases |

### Source Tiers

**Free / FRED / Public:**
- Treasury yields, most spreads, M2, labor data, GDP nowcasts, CPI/PCE, CFTC positioning (delayed)
- Yahoo Finance for equity/ETF prices
- CBOE for basic options data

**Requires Bloomberg / Reuters / Subscription:**
- MOVE Index, CDX indices, cross-currency basis, FRA-OIS, dealer gamma, real-time flows, some global liquidity
- Real-time CFTC positioning
- Bank CDS, detailed credit indices

**Build Yourself / Proxy:**
- Dealer gamma exposure (requires options data + model)
- CTA trend signals (proxy with moving averages on futures)
- Vol target exposure (estimate from VIX level vs trailing average)
- Mag7 market cap percentage (from individual tickers)
- Many derived series (see Derived Series Formulas section)

---

## Appendix A: What This System Won't Tell You

1. **Timing** — It tells you the regime, not when the regime ends
2. **Magnitude** — It tells you direction of stress, not how far it goes
3. **Trades** — It's a diagnostic tool, not a signal generator
4. **The future** — It maps the current machine; it doesn't predict mutations
5. **Single-name risk** — Company-specific blowups aren't captured until they hit indices
6. **Pure geopolitics** — Wars and elections are inputs, not outputs of this system

### Known Blind Spots

- **Private markets opacity:** Private credit, venture capital, real estate direct holdings aren't captured
- **Political tail risks:** Election surprises, regulatory shifts not yet priced
- **Cross-border capital controls:** Sudden imposition of controls
- **Market microstructure breaks:** Flash crashes from algorithmic interaction
- **Single counterparty failure:** A specific bank/fund blowing up before systemic indicators show it

Use this to understand *what kind of market you're in* and *where to focus attention*. The actual decisions are still yours.

---

## Appendix B: Customization Tips

**For EM-focused users:**
- Promote `embi_spread`, `em_fx_index`, `china_credit_impulse` to Core
- Add EM-specific credit indices if available
- Watch `usdcny` and `audusd` more closely

**For volatility traders:**
- Emphasize Categories 8, 14, 19
- Add VIX futures term structure details
- Track gamma exposure more granularly
- Consider adding VVIX/VIX ratio

**For fixed income focus:**
- Emphasize Categories 3, 4, 15, 16
- Add swap spread curve details
- Track auction calendar religiously
- Add Treasury repo specials if available

**For macro tourists / generalists:**
- Stick to Core + Pattern recognition
- Check Categories 26–28 monthly
- Don't get lost in microstructure unless vol spikes

---

## Appendix C: Current Regime Considerations (Optional)

*This section captures themes that may be relevant to the current macro environment but may not age well. Review periodically and update or remove as conditions change.*

### Theme: AI Infrastructure Bottleneck

The AI buildout may be constrained by physical infrastructure (power, cooling, specialized labor) rather than just chips.

**Potential additions to Category 25:**
- Electricity PPI / Industrial power rates
- Utility capex indices
- Data center REIT performance (EQIX, DLR)

**So what:** Distinguishes between AI "bubble" (capex only) and AI "revolution" (productivity gains materialize).

### Theme: Private Credit Shadow Cycle

With more lending moving to private markets, public HY spreads may not capture the full credit cycle.

**Potential additions:**
- Private credit fund NAVs
- BDC discount/premium to NAV
- PE secondary market discounts

**So what:** The "invisible" credit cycle. Stress may emerge in private markets before public spreads widen.

### Theme: Fiscal Dominance / Sovereign Fragmentation

Developed market sovereign risk is diverging, with fiscal concerns affecting even "safe" countries.

**Already captured:**
- `france_oat_minus_bund` (primary EU stress signal)
- `interest_to_revenue_ratio` (live fiscal stress)
- `term_premium_acm` (compensation for duration risk)

**Potential additions:**
- Fed independence risk premium (5Y/10Y inflation swap spread)
- Debt ceiling / fiscal cliff calendar events

### Theme: Pattern 7 Consideration — Productivity Surge (Experimental)

*Not yet validated in practice. Monitor for emergence. Do not force-fit.*

**Hypothetical signature:**
- `productivity_growth_yoy` ↑ sustained
- `unit_labor_costs_yoy` ↓ or flat
- `soxx_close` surging (AI/automation investment)
- Wages stable while profits expand
- Inflation falling without growth slowing

**Hypothetical first check:** 29) Profits → 25) Tech/Capex → 28) Inflation

**So what:** Would distinguish "good" disinflation from growth scares. The "rising tide lifts all boats" regime. Currently theoretical — add to main patterns only if observed in practice.

---

## Appendix D: Implementation Code Snippets (Optional)

*For users building automated dashboards. These are starting points, not production code.*

### Basic Data Pull (Python + yfinance + FRED)

```python
import yfinance as yf
import pandas_datareader as pdr
from datetime import datetime, timedelta

# Equity prices
tickers = ['SPY', 'QQQ', 'IWM', 'TLT', 'HYG', 'GLD']
data = yf.download(tickers, period='1y')['Adj Close']

# FRED series
fred_series = {
    'ust_10y': 'DGS10',
    'ust_2y': 'DGS2',
    'tips_10y': 'DFII10',
    'hy_spread': 'BAMLH0A0HYM2',
    'hy_ccc': 'BAMLH0A3HYC',
    'hy_bb': 'BAMLH0A1HYBB',
    'vix': 'VIXCLS',
    'sofr': 'SOFR',
    'ff_effective': 'FEDFUNDS',
    'initial_claims': 'IC4WSA',
    'sahm_rule': 'SAHMCURRENT',  # Use SAHMCURRENT for current published value
}

start = datetime.now() - timedelta(days=365)
fred_data = {name: pdr.get_data_fred(code, start) 
             for name, code in fred_series.items()}

# Calculate derived series
fred_data['sofr_ff_spread'] = fred_data['sofr'] - fred_data['ff_effective']
fred_data['hy_ccc_minus_bb_spread'] = fred_data['hy_ccc'] - fred_data['hy_bb']
```

### Mag7 Market Cap Percentage

```python
def calculate_mag7_pct():
    """
    Calculate Mag7 as percentage of S&P 500 market cap.
    """
    mag7_tickers = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'META', 'TSLA']
    
    mag7_market_cap = 0
    for ticker in mag7_tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        if 'marketCap' in info:
            mag7_market_cap += info['marketCap']
    
    # S&P 500 total market cap approximation
    # Use SPY AUM * (1/0.10) as rough proxy, or fetch from index provider
    spy = yf.Ticker('SPY')
    spy_price = spy.history(period='1d')['Close'].iloc[-1]
    # SPY has ~900M shares outstanding, tracks ~10% of SPX by design
    # Better: use actual S&P 500 total market cap from index provider
    spx_market_cap_estimate = spy_price * 900e6 * 10  # Very rough estimate
    
    mag7_pct = (mag7_market_cap / spx_market_cap_estimate) * 100
    
    return {
        'mag7_market_cap': mag7_market_cap,
        'spx_market_cap_estimate': spx_market_cap_estimate,
        'mag7_pct': mag7_pct
    }
```

### Basic Gamma Estimation (Conceptual)

```python
import yfinance as yf
import numpy as np

def estimate_dealer_gamma(ticker='^GSPC'):
    """
    Rough gamma estimate from put/call OI at nearby strikes.
    This is a simplification - real gamma requires full options chain
    and assumptions about dealer positioning.
    """
    spx = yf.Ticker(ticker)
    
    # Get nearest expiry options
    expirations = spx.options[:3]  # Next 3 expirations
    
    total_call_oi = 0
    total_put_oi = 0
    
    for exp in expirations:
        chain = spx.option_chain(exp)
        
        # Get ATM strikes (within 2% of spot)
        spot = spx.history(period='1d')['Close'].iloc[-1]
        atm_calls = chain.calls[
            (chain.calls['strike'] > spot * 0.98) & 
            (chain.calls['strike'] < spot * 1.02)
        ]
        atm_puts = chain.puts[
            (chain.puts['strike'] > spot * 0.98) & 
            (chain.puts['strike'] < spot * 1.02)
        ]
        
        total_call_oi += atm_calls['openInterest'].sum()
        total_put_oi += atm_puts['openInterest'].sum()
    
    # Rough proxy: more puts = more negative gamma (dealers short puts)
    gamma_proxy = (total_call_oi - total_put_oi) / (total_call_oi + total_put_oi)
    
    return {
        'gamma_proxy': gamma_proxy,  # Positive = supportive, Negative = amplifying
        'call_oi': total_call_oi,
        'put_oi': total_put_oi,
        'interpretation': 'Likely positive gamma' if gamma_proxy > 0.1 
                         else 'Likely negative gamma' if gamma_proxy < -0.1 
                         else 'Neutral gamma'
    }
```

### CTA Trend Signal Proxy

```python
def cta_trend_proxy(prices, short_window=50, long_window=200):
    """
    Simple trend-following signal proxy.
    Assumes CTAs are net long when price > both MAs, net short when below both.
    """
    ma_short = prices.rolling(short_window).mean()
    ma_long = prices.rolling(long_window).mean()
    
    signal = np.where(
        (prices > ma_short) & (prices > ma_long), 1,  # Strong uptrend
        np.where(
            (prices < ma_short) & (prices < ma_long), -1,  # Strong downtrend
            0  # Mixed/neutral
        )
    )
    
    return signal

# Apply to major futures proxies
es_signal = cta_trend_proxy(spy_prices)  # Equity
zn_signal = cta_trend_proxy(ief_prices)  # Rates
gc_signal = cta_trend_proxy(gld_prices)  # Gold
```

### Z-Score Alert Generator

```python
def generate_alerts(current_values, historical_data, threshold=2.0):
    """
    Generate alerts when current values exceed z-score threshold.
    """
    alerts = []
    
    for indicator, current in current_values.items():
        if indicator in historical_data.columns:
            hist = historical_data[indicator].dropna()
            mean = hist.mean()
            std = hist.std()
            
            if std > 0:
                z_score = (current - mean) / std
                percentile = (hist < current).mean() * 100
                
                if abs(z_score) > threshold:
                    alerts.append({
                        'indicator': indicator,
                        'current': current,
                        'z_score': z_score,
                        'percentile': percentile,
                        'direction': 'HIGH' if z_score > 0 else 'LOW',
                        'severity': 'RED' if abs(z_score) > 2.5 else 'YELLOW'
                    })
    
    return sorted(alerts, key=lambda x: abs(x['z_score']), reverse=True)
```

### Change Detection Matrix

```python
def compute_change_matrix(data, indicators):
    """
    Compute the Change Detection Matrix for morning triage.
    """
    results = []
    
    for ind in indicators:
        if ind not in data.columns:
            continue
            
        series = data[ind].dropna()
        if len(series) < 21:
            continue
            
        current = series.iloc[-1]
        d1 = (current / series.iloc[-2] - 1) * 100 if series.iloc[-2] != 0 else 0
        d5 = (current / series.iloc[-6] - 1) * 100 if len(series) > 5 else 0
        d20 = (current / series.iloc[-21] - 1) * 100 if len(series) > 20 else 0
        
        # Acceleration: is Δ5d > Δ20d in same direction?
        same_direction = (d5 > 0 and d20 > 0) or (d5 < 0 and d20 < 0)
        accelerating = same_direction and abs(d5) > abs(d20) * 0.25  # 5d pace > 25% of 20d
        
        results.append({
            'indicator': ind,
            'current': current,
            'd1_pct': d1,
            'd5_pct': d5,
            'd20_pct': d20,
            'accelerating': accelerating
        })
    
    return pd.DataFrame(results)
```

---

*Built for navigating markets as they actually work, not as textbooks describe them.*
