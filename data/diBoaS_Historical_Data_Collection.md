# diBoaS Historical Data Collection Summary

**Version:** 1.0  
**Date:** December 27, 2025  
**Prepared By:** Rakia (Investment/DeFi Opportunities Analyst)  
**For:** QR Board, Strategy Board, CTO Board

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [APY Data Collection](#2-apy-data-collection)
3. [Price Data Collection](#3-price-data-collection)
4. [Data Quality Assessment](#4-data-quality-assessment)
5. [Usage Guide](#5-usage-guide)
6. [Data Sources & API Reference](#6-data-sources--api-reference)

---

# 1. Executive Summary

## Data Collected

| Dataset | Records | Date Range | Sources |
|---------|---------|------------|---------|
| **Historical APY** | 47,496 | Feb 2022 - Dec 2025 | DeFiLlama Yields API |
| **Historical Prices** | 4,380 | Dec 2021 - Dec 2025 | Yahoo Finance |
| **Target Pools** | 776 | Current snapshot | DeFiLlama Yields API |

## Protocols Covered (APY Data)

| Protocol | Records | Date Range | Avg APY |
|----------|---------|------------|---------|
| Aave V3 | 23,435 | Aug 2022 - Dec 2025 | 1.64% |
| Sky Lending | 6,056 | Oct 2022 - Dec 2025 | 1.11% |
| Curve | 5,862 | Feb 2022 - Dec 2025 | 4.71% |
| Kamino Lend | 5,446 | Nov 2023 - Dec 2025 | 2.19% |
| Compound V3 | 4,833 | Oct 2022 - Dec 2025 | Variable |
| Lido | 1,305 | May 2022 - Dec 2025 | 3.64% |
| Jito LST | 277 | Mar 2025 - Dec 2025 | 6.97% |
| Euler V2 | 142 | Sep 2025 - Dec 2025 | 9.90% |
| Pendle | 140 | Nov 2025 - Dec 2025 | 10.17% |

## Price Data Coverage

| Asset | Records | Date Range | Price Range |
|-------|---------|------------|-------------|
| **BTC** | 1,460 | Dec 2021 - Dec 2025 | $15,787 - $124,753 |
| **ETH** | 1,460 | Dec 2021 - Dec 2025 | $994 - $4,831 |
| **SOL** | 1,460 | Dec 2021 - Dec 2025 | $9.65 - $261.87 |

---

# 2. APY Data Collection

## 2.1 Data Source

**DeFiLlama Yields API**
- Base URL: `https://yields.llama.fi`
- Authentication: None required (free tier)
- Rate Limit: 500 requests/minute
- Update Frequency: Hourly snapshots, daily historical

## 2.2 Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `/pools` | Current pool snapshot with APY, TVL, metadata |
| `/chart/{pool_id}` | Historical daily APY/TVL time series |

## 2.3 Output Files

### defillama_target_pools.csv

Current snapshot of all target protocol pools.

| Column | Description |
|--------|-------------|
| pool_id | DeFiLlama UUID for the pool |
| project | Protocol slug (e.g., "aave-v3") |
| project_name | Display name (e.g., "Aave V3") |
| chain | Blockchain (Ethereum, Arbitrum, Solana, Base) |
| symbol | Asset symbol (e.g., "USDC", "WETH") |
| tvl_usd | Total Value Locked in USD |
| current_apy | Current total APY (%) |
| apy_base | Base APY from protocol activity |
| apy_reward | Reward APY from incentives |
| stablecoin | Boolean flag for stablecoins |

### defillama_historical_apy.csv

Historical daily APY data for backtesting.

| Column | Description |
|--------|-------------|
| date | Date in YYYY-MM-DD format |
| pool_id | DeFiLlama UUID |
| project | Protocol slug |
| project_name | Display name |
| chain | Blockchain |
| symbol | Asset symbol |
| tvl_usd | TVL on that date |
| apy | Total APY on that date (%) |
| apy_base | Base APY component |
| apy_reward | Reward APY component |

### defillama_protocol_summary.csv

Aggregated statistics by protocol.

| Column | Description |
|--------|-------------|
| project | Protocol slug |
| project_name | Display name |
| total_records | Number of daily data points |
| pools_count | Number of pools tracked |
| chains | Comma-separated chain list |
| symbols | Comma-separated asset symbols |
| date_start | Earliest data date |
| date_end | Latest data date |
| avg_apy | Average APY across all records |
| min_apy | Minimum observed APY |
| max_apy | Maximum observed APY |

## 2.4 Protocols Included

### Lending Protocols

| Protocol | Slug | Chains | Data Start |
|----------|------|--------|------------|
| Aave V3 | aave-v3 | Ethereum, Arbitrum, Base | Aug 2022 |
| Compound V3 | compound-v3 | Ethereum | Oct 2022 |
| Kamino Lend | kamino-lend | Solana | Nov 2023 |
| Euler V2 | euler-v2 | Ethereum | Sep 2025 |

### Liquid Staking

| Protocol | Slug | Chains | Data Start |
|----------|------|--------|------------|
| Lido | lido | Ethereum | May 2022 |
| Jito | jito-liquid-staking | Solana | Mar 2025 |

### Yield Strategy

| Protocol | Slug | Chains | Data Start |
|----------|------|--------|------------|
| Sky/Spark | sky-lending | Ethereum | Oct 2022 |
| Pendle | pendle | Arbitrum | Nov 2025 |
| Curve | curve-dex | Ethereum | Feb 2022 |

## 2.5 Data Gaps & Limitations

| Protocol | Issue | Mitigation |
|----------|-------|------------|
| **Jito** | Only 277 records (Mar 2025+) | Historical Jito data predates DeFiLlama tracking |
| **Euler V2** | Only 142 records (Sep 2025+) | Protocol relaunched after 2023 exploit |
| **Pendle** | Only 140 records (Nov 2025+) | PT pools are time-limited by design |
| **Jupiter JLP** | Missing from top 80 pools | Separate tracking needed |
| **GMX V2** | Missing from top 80 pools | Separate tracking needed |
| **Drift** | Missing from top 80 pools | Separate tracking needed |

---

# 3. Price Data Collection

## 3.1 Data Source

**Yahoo Finance**
- Package: `yfinance` Python library
- Authentication: None required
- Rate Limit: Reasonable use (no hard limits)
- Coverage: Full 4-year history available

## 3.2 Output File

### yahoo_historical_prices.csv

| Column | Description |
|--------|-------------|
| date | Date in YYYY-MM-DD format |
| symbol | Asset symbol (BTC, ETH, SOL) |
| ticker | Yahoo Finance ticker (e.g., BTC-USD) |
| open | Opening price USD |
| high | High price USD |
| low | Low price USD |
| close | Closing price USD |
| volume | 24h trading volume |

## 3.3 Price Statistics

### Bitcoin (BTC)

| Metric | Value |
|--------|-------|
| Records | 1,460 days |
| Date Range | Dec 28, 2021 - Dec 26, 2025 |
| Min Price | $15,787.28 (Nov 2022) |
| Max Price | $124,752.53 (Dec 2024) |
| 4-Year Return | ~+175% |

### Ethereum (ETH)

| Metric | Value |
|--------|-------|
| Records | 1,460 days |
| Date Range | Dec 28, 2021 - Dec 26, 2025 |
| Min Price | $993.64 (Jun 2022) |
| Max Price | $4,831.35 (Nov 2024) |
| 4-Year Return | ~+30% |

### Solana (SOL)

| Metric | Value |
|--------|-------|
| Records | 1,460 days |
| Date Range | Dec 28, 2021 - Dec 26, 2025 |
| Min Price | $9.65 (Dec 2022) |
| Max Price | $261.87 (Nov 2024) |
| 4-Year Return | ~+50% |

---

# 4. Data Quality Assessment

## 4.1 Completeness Score

| Dataset | Completeness | Notes |
|---------|--------------|-------|
| APY Data | 85% | Missing newer protocols (Jito, Euler V2) historical data |
| Price Data | 100% | Full 4-year coverage for all 3 assets |
| Pool Metadata | 100% | All 776 target pools captured |

## 4.2 Known Issues

### APY Data

1. **Null APY values**: Some records have null apy_base/apy_reward
   - **Mitigation**: Use `apy` field which is always populated

2. **Protocol slug variations**: Some protocols have multiple slugs
   - Example: "morpho" vs "morpho-blue" vs "morpho-v1"
   - **Mitigation**: Included all variations in target list

3. **Stale data**: Some low-TVL pools may have stale APY
   - **Mitigation**: Filtered to pools >$50K TVL

### Price Data

1. **Weekend gaps**: Some weekend data may be interpolated
   - **Impact**: Minimal for daily analysis

2. **Timezone**: Data is in UTC
   - **Impact**: Consistent across all assets

## 4.3 Validation Checks Performed

- [x] No duplicate date/pool combinations
- [x] APY values within reasonable bounds (0-1000%)
- [x] Price values positive and non-null
- [x] Date sequences continuous (no gaps >2 days)
- [x] Pool IDs match between snapshot and historical data

---

# 5. Usage Guide

## 5.1 Loading Data in Python

```python
import pandas as pd

# Load APY data
apy_df = pd.read_csv('defillama_historical_apy.csv', parse_dates=['date'])

# Load price data
price_df = pd.read_csv('yahoo_historical_prices.csv', parse_dates=['date'])

# Load pool metadata
pools_df = pd.read_csv('defillama_target_pools.csv')
```

## 5.2 Common Queries

### Get APY history for specific protocol

```python
aave_data = apy_df[apy_df['project'] == 'aave-v3']
```

### Get USDC pools only

```python
usdc_pools = apy_df[apy_df['symbol'].str.contains('USDC')]
```

### Merge APY with price data

```python
# Add ETH price to Ethereum pools
eth_prices = price_df[price_df['symbol'] == 'ETH'][['date', 'close']]
eth_prices = eth_prices.rename(columns={'close': 'eth_price'})

merged = apy_df.merge(eth_prices, on='date', how='left')
```

### Calculate strategy returns

```python
# Simple yield calculation
apy_df['daily_yield'] = apy_df['apy'] / 365

# Compounded monthly return
monthly = apy_df.groupby(['project', pd.Grouper(key='date', freq='M')])['apy'].mean()
```

## 5.3 Backtesting Integration

The data supports the existing 48-month backtesting framework:

1. **Strategy 1 (Sky SSR)**: Use `sky-lending` + `SUSDS` symbol
2. **Strategy 2 (Aave+JLP)**: Use `aave-v3` + separate JLP data
3. **Strategy 3 (Lido+Aave)**: Use `lido` + `aave-v3`
4. **Strategy 4-10**: Mix relevant protocol data

---

# 6. Data Sources & API Reference

## 6.1 DeFiLlama Yields API

| Property | Value |
|----------|-------|
| Base URL | `https://yields.llama.fi` |
| Documentation | https://defillama.com/docs/api |
| Rate Limit | 500 req/min (free) |
| Authentication | None |

### Key Endpoints

```
GET /pools
Returns: All ~16,000 pools with current APY

GET /chart/{pool_uuid}
Returns: Historical daily APY for specific pool
```

### Pro API ($300/month)

Additional endpoints for:
- Borrow rates: `/yields/poolsBorrow`
- Historical lend/borrow: `/yields/chartLendBorrow/{pool}`
- LSD rates: `/yields/lsdRates`

## 6.2 Yahoo Finance

| Property | Value |
|----------|-------|
| Package | `yfinance` (Python) |
| Documentation | https://pypi.org/project/yfinance/ |
| Rate Limit | Reasonable use |
| Authentication | None |

### Tickers Used

| Asset | Ticker |
|-------|--------|
| Bitcoin | BTC-USD |
| Ethereum | ETH-USD |
| Solana | SOL-USD |

## 6.3 Future Data Collection

### Recommended Additions

| Data Type | Source | Priority |
|-----------|--------|----------|
| Jupiter JLP APY | Jupiter API | High |
| GMX V2 APY | GMX Subgraph | High |
| Drift APY | Drift API | Medium |
| Gas prices | Etherscan/Arbiscan | Medium |
| LST exchange rates | Protocol APIs | Low |

### Automation Recommendations

1. **Daily APY collection**: Cron job at 00:00 UTC
2. **Weekly full refresh**: Sunday 03:00 UTC
3. **Monitoring**: Alert on >20% APY changes

---

# Appendix: File Checksums

| File | Size | Records |
|------|------|---------|
| defillama_target_pools.csv | ~150 KB | 776 |
| defillama_historical_apy.csv | ~5 MB | 47,496 |
| defillama_protocol_summary.csv | ~2 KB | 9 |
| yahoo_historical_prices.csv | ~200 KB | 4,380 |

---

*Document compiled December 27, 2025*

*Data should be refreshed monthly for production use*
