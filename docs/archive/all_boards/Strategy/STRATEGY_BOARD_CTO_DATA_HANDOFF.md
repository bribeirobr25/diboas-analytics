# Strategy Board → CTO Board: Data Files Handoff

**Date:** February 4, 2026  
**From:** Strategy Board  
**To:** CTO Board  
**Priority:** P1 (Pre-Launch)  
**Blocking:** Partial — Core analytics work, some triggers disabled

---

## Executive Summary

The Strategy Board has completed a full review of the diboas-analytics v3 implementation following the February 3, 2026 full run. The implementation is **substantially complete** for launch, with one critical gap: **12 data files are missing** from the `data/` directory, which disables several trigger categories.

---

## Missing Data Files

### Current State

| Category | Expected Files | Found | Missing |
|----------|----------------|-------|---------|
| Core Market Data | 8 | 8 | 0 |
| Wallet Trackers | 4 | 0 | 4 |
| Institutional Flows | 3 | 0 | 3 |
| Macro Indicators | 5 | 0 | 5 |

### Files Present ✅

```
data/
├── commodities.csv              ✅ 41 KB
├── crypto_prices.csv            ✅ 132 KB
├── defillama_historical_apy.csv ✅ 139 KB
├── jito_historical_apy.csv      ✅ 8 KB
├── jupiter_jlp_historical_apy.csv ✅ 2 KB
├── rotation_indicators.csv      ✅ 105 KB
├── sentiment_indicators.csv     ✅ 8 KB
└── tradfi_benchmark_data.csv    ✅ 139 KB
```

### Files Missing ❌

#### Wallet Trackers (4 files)

| File | Source | Impact if Missing |
|------|--------|-------------------|
| `estate_wallet_tracker.csv` | Manual curation | Estate wallet triggers disabled |
| `whale_wallet_master_list.csv` | Manual curation | Whale movement triggers disabled |
| `market_maker_wallet_tracker.csv` | Manual curation | Market maker alerts disabled |
| `protocol_treasury_tracker.csv` | Manual curation | Protocol treasury monitoring disabled |

**Schema Required:**
```csv
# estate_wallet_tracker.csv
wallet_address,entity,chain,last_known_balance_usd,last_updated,notes

# whale_wallet_master_list.csv
wallet_address,label,chain,category,first_seen,notes

# market_maker_wallet_tracker.csv
wallet_address,entity,chain,role,last_updated

# protocol_treasury_tracker.csv
protocol,wallet_address,chain,treasury_type,last_balance_usd,last_updated
```

#### Institutional Flows (3 files)

| File | Source | Impact if Missing |
|------|--------|-------------------|
| `btc_etf_holdings.csv` | CoinGlass / ETF filings | ETF flow triggers disabled |
| `corporate_btc_holdings.csv` | BitcoinTreasuries.net | Corporate treasury triggers disabled |
| `institutional_13f.csv` | SEC EDGAR | Institutional position triggers disabled |

**Schema Required:**
```csv
# btc_etf_holdings.csv
date,ticker,etf_name,btc_holdings,aum_usd,daily_flow_btc

# corporate_btc_holdings.csv
date,company,ticker,btc_holdings,cost_basis_usd,market_value_usd

# institutional_13f.csv
filing_date,institution,ticker,shares,value_usd,change_pct
```

#### Macro Indicators (5 files)

| File | Source | Impact if Missing |
|------|--------|-------------------|
| `aaii_sentiment.csv` | AAII website | Retail sentiment triggers disabled |
| `credit_spreads.csv` | FRED | Credit stress triggers disabled |
| `global_liquidity.csv` | FRED / Central banks | Liquidity regime triggers disabled |
| `treasury_yields.csv` | FRED | Yield curve triggers disabled |
| `real_yields.csv` | FRED | Real yield triggers disabled |

**Schema Required:**
```csv
# aaii_sentiment.csv
date,bullish_pct,bearish_pct,neutral_pct,bull_bear_spread

# credit_spreads.csv
date,hy_spread_bps,ig_spread_bps,ted_spread_bps

# global_liquidity.csv
date,fed_balance_sheet_b,ecb_balance_sheet_b,boj_balance_sheet_b,m2_yoy_pct

# treasury_yields.csv
date,us_2y,us_10y,us_30y,spread_10y_2y

# real_yields.csv
date,tips_5y,tips_10y,breakeven_5y,breakeven_10y
```

---

## Triggers Affected

### Currently Disabled (Missing Data)

| Trigger Category | Trigger Count | Status |
|------------------|---------------|--------|
| `wallet/estate_wallet_triggers.py` | 3 | ❌ Disabled |
| `wallet/whale_wallet_triggers.py` | 3 | ❌ Disabled |
| `macro/liquidity_triggers.py` | 2 | ❌ Disabled |
| `macro/yield_curve_triggers.py` | 3 | ❌ Disabled |

### Currently Active (Data Present)

| Trigger Category | Trigger Count | Status |
|------------------|---------------|--------|
| `protocol/sky_protocol_triggers.py` | 4 | ✅ Active |
| `protocol/sanctum_protocol_triggers.py` | 4 | ✅ Active |
| `protocol/jlp_protocol_triggers.py` | 4 | ✅ Active |
| `protocol/aave_protocol_triggers.py` | 2 | ✅ Active |
| `protocol/stablecoin_depeg_triggers.py` | 6 | ✅ Active |
| `market/price_movement_triggers.py` | 5 | ✅ Active |
| `market/volatility_triggers.py` | 2 | ✅ Active |

---

## Recommended Actions

### Option A: Full Data Population (Recommended)

1. **Wallet Trackers:** Use addresses from project files:
   - `/mnt/project/estate_wallet_tracker.csv`
   - `/mnt/project/whale_wallet_master_list.csv`
   - `/mnt/project/market_maker_wallet_tracker.csv`
   - `/mnt/project/protocol_treasury_tracker.csv`

2. **Institutional Flows:** Implement collectors or use project files:
   - `/mnt/project/btc_etf_holdings.csv`
   - `/mnt/project/corporate_btc_holdings.csv`
   - `/mnt/project/institutional_13f.csv`

3. **Macro Indicators:** Use FRED collector + project files:
   - `/mnt/project/aaii_sentiment.csv`
   - `/mnt/project/credit_spreads.csv`
   - `/mnt/project/global_liquidity.csv`
   - `/mnt/project/treasury_yields.csv`
   - `/mnt/project/real_yields.csv`

### Option B: Minimal Launch (Acceptable)

Copy only the files that enable P0/P1 triggers:
- `treasury_yields.csv` (yield curve inversion detection)
- `credit_spreads.csv` (credit stress detection)
- `estate_wallet_tracker.csv` (bankruptcy estate monitoring)

### Option C: Launch Without (Not Recommended)

Proceed with current 8 files. Impact:
- Wallet triggers: 6 disabled
- Macro triggers: 5 disabled
- Adelaide content less comprehensive

---

## Timeline Request

| Action | Effort | Deadline |
|--------|--------|----------|
| Copy project files to data/ | 30 min | Feb 5 |
| Verify schemas match | 1 hour | Feb 5 |
| Run full pipeline test | 2 hours | Feb 6 |
| Confirm triggers fire correctly | 1 hour | Feb 6 |

**Total Estimated Effort:** 4-5 hours

---

## Acceptance Criteria

Strategy Board will consider this handoff complete when:

1. ✅ All 20 CSV files present in `data/` directory
2. ✅ Schemas match specifications above
3. ✅ Full pipeline run completes without data errors
4. ✅ At least one trigger from each category fires in test

---

## Contact

For questions about trigger specifications or strategy impact:
- **Strategy Board** — This chat
- **Reference:** `cto_handoff_package/03_layer4_intelligence/STRATEGY_BOARD_CTO_HANDOFF.md`

---

*Document generated by Strategy Board — February 4, 2026*
