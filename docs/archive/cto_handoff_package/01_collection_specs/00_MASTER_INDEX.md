# diBoaS Market Intelligence System — Master Index

**Version:** 2.0  
**Date:** January 20, 2026  
**Status:** APPROVED  
**Owner:** Strategy Board + CTO Board

---

## Executive Summary

The diBoaS Market Intelligence System provides comprehensive monitoring across on-chain crypto, traditional finance, and macroeconomic indicators. This intelligence feeds into:

1. **Adelaide Newsletter** — Daily/weekly market intelligence for users
2. **Risk Monitoring** — Protocol health, estate wallets, liquidation risk
3. **Strategy Optimization** — Yield opportunities, rotation signals
4. **User Alerts** — Significant market movements

---

## Documentation Structure

```
📁 diBoaS Market Intelligence System
│
├── 📄 00_MASTER_INDEX.md (this document)
│
├── 📄 01_ON_CHAIN_INTELLIGENCE.md
│   ├── Estate Wallet Tracking
│   ├── Market Maker Monitoring
│   ├── Protocol Treasury Tracking
│   ├── Whale Wallet Monitoring
│   └── Smart Money Patterns
│
├── 📄 02_CRYPTO_MARKETS.md
│   ├── Price Data (BTC, ETH, SOL, etc.)
│   ├── DeFi Protocol Yields
│   ├── Stablecoin Supply & Flows
│   └── Exchange Reserves
│
├── 📄 03_TRADFI_MARKETS.md
│   ├── Equity Indices (Global + Regional)
│   ├── Fixed Income (Yields, Spreads)
│   ├── Commodities (Gold, Oil, Metals)
│   ├── Currencies (DXY, Major Pairs)
│   └── Volatility (VIX)
│
├── 📄 04_MACRO_ECONOMICS.md
│   ├── Global Liquidity (M2)
│   ├── Central Bank Policy
│   ├── Inflation Data
│   ├── Real Yields
│   └── Credit Conditions
│
├── 📄 05_INSTITUTIONAL_FLOWS.md
│   ├── ETF Flows (BTC, ETH, Gold)
│   ├── 13F Institutional Holdings
│   ├── Corporate Treasury Holdings
│   └── Fund Positioning
│
├── 📄 06_CAPITAL_ROTATION.md
│   ├── Rotation Ratios
│   ├── Cycle Indicators
│   ├── Intermarket Analysis
│   └── Regime Detection
│
├── 📄 07_NEWS_AND_SENTIMENT.md
│   ├── Data Sources
│   ├── News Monitoring
│   ├── Sentiment Indicators
│   └── Alert Keywords
│
└── 📄 08_ADELAIDE_INTEGRATION.md
    ├── Daily Digest Format
    ├── Weekly Report Format
    ├── Alert Templates
    └── Priority Routing
```

---

## Quick Reference: Data Inventory

### Current Status Overview

| Category | Documents | Status | Records | Priority |
|----------|-----------|--------|---------|----------|
| **On-Chain** | 01 | ✅ Good | 220+ wallets | 🔴 Critical |
| **Crypto Markets** | 02 | ✅ Good | 50,000+ | 🔴 Critical |
| **TradFi Markets** | 03 | ⚠️ Gaps | 36,000+ | 🔴 Critical |
| **Macro Economics** | 04 | 🔴 Missing | ~800 | 🔴 Critical |
| **Institutional Flows** | 05 | ⚠️ Partial | 30+ | 🟠 High |
| **Capital Rotation** | 06 | 🔴 Missing | 0 | 🟠 High |
| **News & Sentiment** | 07 | 🔴 Missing | 0 | 🟡 Medium |
| **Adelaide Integration** | 08 | 📋 Spec Only | — | 🟠 High |

### Action Summary

| Action | Files Affected | Priority |
|--------|----------------|----------|
| ✅ **Keep as-is** | 15 files | — |
| 🔄 **Update/Extend** | 3 files | 🟠 High |
| ➕ **Create new** | 8+ files | 🔴 Critical |
| ❌ **Deprecate** | 2 files | 🟢 Low |

---

## Priority Matrix

### 🔴 Critical (Build This Week)

| Data | Document | Why Critical |
|------|----------|--------------|
| Global M2 Liquidity | 04_MACRO | #1 crypto driver |
| Real Yields (TIPS) | 04_MACRO | Inverse crypto correlation |
| Treasury Yields | 03_TRADFI | Rate environment |
| Estate Wallet Alerts | 01_ON_CHAIN | Unique moat |
| Adelaide Daily Digest | 08_ADELAIDE | User-facing deliverable |

### 🟠 High (Build This Month)

| Data | Document | Why Important |
|------|----------|---------------|
| Asia Indices | 03_TRADFI | Regional coverage |
| Credit Spreads | 04_MACRO | Risk appetite |
| ETF Flows | 05_INSTITUTIONAL | Institutional sentiment |
| Rotation Ratios | 06_ROTATION | Cycle positioning |
| 13F Tracking | 05_INSTITUTIONAL | Smart money |

### 🟡 Medium (Build Q1)

| Data | Document | Why Useful |
|------|----------|------------|
| Sentiment Indicators | 07_NEWS | Contrarian signals |
| Gold Flows | 05_INSTITUTIONAL | Hard asset demand |
| Regional Giants | 05_INSTITUTIONAL | Target market insight |
| News Monitoring | 07_NEWS | Breaking events |

### 🟢 Low (Backlog)

| Data | Document | Why Later |
|------|----------|-----------|
| Individual Country Data | Various | Regional aggregates sufficient |
| Altcoin-specific | — | Not relevant to strategies |
| Social Sentiment | 07_NEWS | Lagging, noisy |

---

## Existing Data Files

### ✅ Keep As-Is (No Changes)

| File | Category | Records | Quality |
|------|----------|---------|---------|
| `defillama_historical_apy.csv` | Crypto | 47,497 | ✅ Excellent |
| `sky_ssr_historical_apy.csv` | Crypto | 334 | ✅ Excellent |
| `compound_v3_arbitrum_usdc_apy.csv` | Crypto | 840 | ✅ Excellent |
| `sanctum_inf_historical_apy.csv` | Crypto | 667 | ✅ Excellent |
| `jito_extended_apy.csv` | Crypto | 301 | ✅ Excellent |
| `jupiter_jlp_historical_apy.csv` | Crypto | 698 | ✅ Good |
| `perps_lp_combined_apy.csv` | Crypto | 12,986 | ✅ Good |
| `estate_wallet_tracker.csv` | On-Chain | 51 | ✅ Excellent |
| `whale_wallet_master_list.csv` | On-Chain | 50 | ✅ Good |
| `market_maker_wallet_tracker.csv` | On-Chain | 35 | ✅ Good |
| `protocol_treasury_tracker.csv` | On-Chain | 35 | ✅ Good |
| `corporate_btc_holdings.csv` | Institutional | 30 | ✅ Good |
| `expert_watchlist_defi_alpha_corrected.csv` | On-Chain | 8 | ✅ Good |
| `inflation_savings_analysis_2015_2025.csv` | Macro | 793 | ✅ Good |
| `rwa_protocol_comparison.csv` | Crypto | 10 | ✅ Good |

### 🔄 Update/Extend (Add Data)

| File | What to Add | Priority |
|------|-------------|----------|
| `tradfi_benchmark_data_2020_2025.csv` | Nikkei, Hang Seng, JPY, CNY | 🟠 High |
| `yahoo_historical_prices.csv` | More granular crypto data | 🟡 Medium |
| `master_wallet_tracker.csv` | Merge corrected watchlists | 🟠 High |

### ➕ Create New

| File | Category | Priority |
|------|----------|----------|
| `global_liquidity.csv` | Macro | 🔴 Critical |
| `treasury_yields.csv` | TradFi | 🔴 Critical |
| `real_yields.csv` | Macro | 🔴 Critical |
| `credit_spreads.csv` | Macro | 🟠 High |
| `etf_flows.csv` | Institutional | 🟠 High |
| `rotation_indicators.csv` | Rotation | 🟠 High |
| `institutional_13f.csv` | Institutional | 🟠 High |
| `sentiment_indicators.csv` | Sentiment | 🟡 Medium |
| `gold_flows.csv` | Institutional | 🟡 Medium |

### ❌ Deprecate (Replace)

| File | Reason | Replacement |
|------|--------|-------------|
| `expert_watchlist_asymmetric.csv` | Fake addresses | Flow indicators |
| `expert_watchlist_macro.csv` | Fake addresses | Macro dashboard |

---

## CTO Board Implementation Guide

### Phase 1: Foundation (Week 1-2)

```yaml
priority: critical
tasks:
  - name: "Global M2 Liquidity Collection"
    source: "FRED API"
    frequency: "Daily"
    output: "global_liquidity.csv"
    
  - name: "Treasury Yields Collection"
    source: "FRED API"
    frequency: "Daily"
    output: "treasury_yields.csv"
    
  - name: "Estate Wallet Alert System"
    source: "On-chain APIs"
    frequency: "Every 15 minutes"
    output: "alerts_pending.json"
    
  - name: "Adelaide Daily Digest Generator"
    source: "All data sources"
    frequency: "Daily 06:00 UTC"
    output: "daily_digest.md"
```

### Phase 2: Expansion (Week 3-4)

```yaml
priority: high
tasks:
  - name: "Asia Indices Addition"
    source: "Yahoo Finance"
    frequency: "Daily"
    output: "Update tradfi_benchmark.csv"
    
  - name: "ETF Flow Tracker"
    source: "Farside, SoSoValue"
    frequency: "Daily"
    output: "etf_flows.csv"
    
  - name: "Rotation Ratio Calculator"
    source: "Derived from existing data"
    frequency: "Daily"
    output: "rotation_indicators.csv"
    
  - name: "Credit Spreads Collection"
    source: "FRED API"
    frequency: "Daily"
    output: "credit_spreads.csv"
```

### Phase 3: Enhancement (Week 5-8)

```yaml
priority: medium
tasks:
  - name: "13F Quarterly Parser"
    source: "SEC EDGAR"
    frequency: "Quarterly"
    output: "institutional_13f.csv"
    
  - name: "Sentiment Aggregator"
    source: "Multiple"
    frequency: "Daily"
    output: "sentiment_indicators.csv"
    
  - name: "Weekly Report Generator"
    source: "All data sources"
    frequency: "Weekly Sunday 06:00 UTC"
    output: "weekly_report.md"
```

---

## Rakia Researcher Task Index

| Task ID | Description | Document | Output File | Priority |
|---------|-------------|----------|-------------|----------|
| R1 | Token Unlock Schedule | 01_ON_CHAIN | `token_unlock_schedule.csv` | 🟠 High |
| R2 | MEV Searcher Identification | 01_ON_CHAIN | `mev_searcher_tracker.csv` | 🟡 Medium |
| R3 | Court Filing Monitor | 01_ON_CHAIN | `estate_court_schedule.csv` | 🔴 Critical |
| R4 | Exchange Hot Wallets | 01_ON_CHAIN | `exchange_hot_wallets.csv` | 🟠 High |
| R5 | Global M2 Data Collection | 04_MACRO | `global_liquidity.csv` | 🔴 Critical |
| R6 | Treasury Yields + Real Yields | 03_TRADFI / 04_MACRO | `treasury_yields.csv` | 🔴 Critical |
| R7 | Credit Spreads | 04_MACRO | `credit_spreads.csv` | 🟠 High |
| R8 | Asia Market Indices | 03_TRADFI | Update `tradfi_benchmark.csv` | 🟠 High |
| R9 | Gold Flow Tracking | 05_INSTITUTIONAL | `gold_flows.csv` | 🟡 Medium |
| R10 | Capital Rotation Ratios | 06_ROTATION | `rotation_indicators.csv` | 🟠 High |
| R11 | 13F Institutional Tracker | 05_INSTITUTIONAL | `institutional_13f.csv` | 🟠 High |
| R12 | Sentiment Indicators | 07_NEWS | `sentiment_indicators.csv` | 🟡 Medium |

---

## Document Links

| Doc ID | Title | Status |
|--------|-------|--------|
| 01 | [On-Chain Intelligence](./01_ON_CHAIN_INTELLIGENCE.md) | ✅ Ready |
| 02 | [Crypto Markets](./02_CRYPTO_MARKETS.md) | ✅ Ready |
| 03 | [TradFi Markets](./03_TRADFI_MARKETS.md) | ✅ Ready |
| 04 | [Macro Economics](./04_MACRO_ECONOMICS.md) | ✅ Ready |
| 05 | [Institutional Flows](./05_INSTITUTIONAL_FLOWS.md) | ✅ Ready |
| 06 | [Capital Rotation](./06_CAPITAL_ROTATION.md) | ✅ Ready |
| 07 | [News & Sentiment](./07_NEWS_AND_SENTIMENT.md) | ✅ Ready |
| 08 | [Adelaide Integration](./08_ADELAIDE_INTEGRATION.md) | ✅ Ready |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-20 | Initial on-chain specification |
| 1.1 | 2026-01-20 | Added TradFi/Macro addendum |
| 2.0 | 2026-01-20 | Complete restructure into modular documentation |

---

**Next Step:** Review each sub-document for detailed specifications.
