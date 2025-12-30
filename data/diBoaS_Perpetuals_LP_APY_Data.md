# diBoaS Perpetuals LP Historical APY Data

**Version:** 1.0  
**Date:** December 27, 2025  
**Prepared By:** Rakia (Investment/DeFi Opportunities Analyst)  
**For:** QR Board, Strategy Board, CTO Board

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Data Collection Methods](#2-data-collection-methods)
3. [GMX V2 Data](#3-gmx-v2-data)
4. [Jupiter JLP Data](#4-jupiter-jlp-data)
5. [Drift Protocol Status](#5-drift-protocol-status)
6. [Data Files Reference](#6-data-files-reference)
7. [Integration Guide](#7-integration-guide)

---

# 1. Executive Summary

## Data Collected

| Protocol | Records | Date Range | Avg APY | Source |
|----------|---------|------------|---------|--------|
| **GMX V2** | 9,633 | Oct 2023 - Dec 2025 | 17.58% | DeFiLlama |
| **Jupiter JLP** | 697 | Jan 2024 - Dec 2025 | 44.60% | Calculated from fees |
| **JLP-related pools** | 2,655 | Nov 2023 - Dec 2025 | Variable | DeFiLlama |
| **Total** | **12,985** | — | — | — |

## Key Findings

### GMX V2 (Arbitrum)

- **19 pools tracked** with >$1M TVL
- **Top pools by TVL**: ETH-USDC ($89.8M), WBTC-USDC ($83.3M)
- **Current APY range**: 1-26% (30-day average)
- **Historical max**: 2,692% (extreme volatility events)
- **Typical range**: 5-20% APY

### Jupiter JLP (Solana)

- **~$1.1B TVL** (largest perps LP on Solana)
- **30-day average APY**: 30.62%
- **Historical average APY**: 44.60%
- **APY volatility**: High (0-212% range, correlated with trading volume)
- **Fee share**: 75% to JLP holders

### Drift Protocol (Solana)

- **API Access**: Restricted (requires authentication)
- **Alternative**: DeFiLlama does not track Drift Insurance Fund APY
- **Recommendation**: Use Drift SDK for direct integration

---

# 2. Data Collection Methods

## 2.1 GMX V2 Data Sources

### DeFiLlama Yields API (Historical)

```
Base URL: https://yields.llama.fi
Endpoint: /chart/{pool_id}
```

Used for historical daily APY data back to October 2023.

### GMX Native API (Current)

```
Base URL: https://arbitrum-api.gmxinfra.io
Endpoints:
  /apy?period={period}         # Pre-calculated APY
  /markets/info                 # Market metadata
  /performance/annualized      # Annualized returns
```

Periods available: `1d`, `7d`, `30d`, `90d`, `180d`, `1y`, `total`

**No authentication required** for GMX API.

## 2.2 Jupiter JLP Calculation Method

JLP APY is not directly provided by any API. Calculated from:

### Formula

```
Daily APY = (Daily Fees × 0.75 × 365 / TVL) × 100
```

- **0.75**: JLP holders receive 75% of protocol fees
- **25%**: Goes to Jupiter protocol

### Data Sources

| Data | Source | Endpoint |
|------|--------|----------|
| Daily Fees | DeFiLlama Fees API | `/summary/fees/jupiter-perpetual-exchange` |
| TVL | DeFiLlama Protocol API | `/protocol/jupiter-perpetual-exchange` |

### Fee Components

| Fee Type | Rate |
|----------|------|
| Position Open/Close | 6 bps (0.06%) |
| Borrow Fee | Variable (hourly) |
| Swap Fee | Variable by asset |
| Liquidation Fee | Variable |

## 2.3 Drift Protocol

Drift's Data API requires authentication. Historical data available via:

- **S3 Archives** (deprecated Jan 2025): Historical insurance fund records
- **DriftPy SDK**: Python SDK for programmatic access

```bash
pip install driftpy  # Python 3.10+
```

---

# 3. GMX V2 Data

## 3.1 Pool Coverage

| Pool | Chain | TVL | Avg APY |
|------|-------|-----|---------|
| ETH-USDC | Arbitrum | $89.8M | ~6.4% |
| WBTC-USDC | Arbitrum | $83.3M | ~4.3% |
| WBTC-WBTC | Arbitrum | $41.9M | ~1.1% |
| ETH-ETH | Arbitrum | $19.6M | ~3.1% |
| SOL-USDC | Arbitrum | $11.0M | ~2.2% |
| LINK-USDC | Arbitrum | $10.5M | Variable |

## 3.2 APY Composition

GM pool yields come from:

1. **Trading Fees** (63% of protocol fees to GM holders)
   - Open/close: 0.05-0.07%
   - Variable per trade

2. **Borrowing Fees**
   - Hourly compounding
   - Based on utilization

3. **Funding Fees**
   - Balance payments between longs/shorts
   - Can be positive or negative

4. **Swap Fees**: 5-7 bps

## 3.3 Historical APY Statistics

| Metric | Value |
|--------|-------|
| Total Records | 9,633 |
| Date Range | Oct 2023 - Dec 2025 |
| Average APY | 17.58% |
| Median APY | ~8% |
| Max APY | 2,692% (extreme event) |
| Min APY | 0.01% |

---

# 4. Jupiter JLP Data

## 4.1 Pool Composition

JLP is a basket of 5 assets:

| Asset | Target Weight |
|-------|--------------|
| SOL | 45% |
| ETH | 10% |
| WBTC | 10% |
| USDC | 24.5% |
| USDT | 10.5% |

## 4.2 Historical APY Statistics

| Metric | Value |
|--------|-------|
| Total Records | 697 days |
| Date Range | Jan 2024 - Dec 2025 |
| Average APY | 44.60% |
| 30-day Average | 30.62% |
| Max APY | 212.83% |
| Min APY | 0.00% |

## 4.3 Recent Performance (Last 10 Days)

| Date | Daily Fees | TVL | APY |
|------|------------|-----|-----|
| Dec 17 | $2.66M | $1,220M | 59.60% |
| Dec 18 | $3.43M | $1,175M | 79.95% |
| Dec 19 | $1.36M | $1,138M | 32.64% |
| Dec 20 | $0.23M | $1,159M | 5.39% |
| Dec 21 | $0.62M | $1,154M | 14.68% |
| Dec 22 | $1.58M | $1,150M | 37.62% |
| Dec 23 | $1.27M | $1,134M | 30.56% |
| Dec 24 | $0.95M | $1,117M | 23.25% |
| Dec 25 | $0.42M | $1,105M | 10.49% |
| Dec 26 | $1.13M | $1,093M | 28.22% |

## 4.4 APY Volatility Analysis

JLP APY is highly volatile due to:

1. **Trading Volume Correlation**: High volume = high fees = high APY
2. **Market Conditions**: Bull markets generate more trading activity
3. **Weekend Effect**: Lower volume on weekends
4. **Major Events**: News/volatility spikes create fee spikes

**Standard Deviation**: ~35% (daily APY varies significantly)

---

# 5. Drift Protocol Status

## 5.1 Data Access Limitations

| Method | Status | Notes |
|--------|--------|-------|
| Data API | 🔒 Restricted | Returns "Access denied" |
| S3 Archives | ⚠️ Deprecated | Jan 2025 deprecation |
| DeFiLlama | ❌ Not tracked | Insurance Fund APY not available |
| SDK | ✅ Available | Requires Solana RPC |

## 5.2 Recommended Approach

For Drift Insurance Fund and lending APY:

```python
from driftpy.drift_client import DriftClient
from solana.rpc.async_api import AsyncClient

# Connect to Solana
connection = AsyncClient("https://api.mainnet-beta.solana.com")

# Initialize Drift client
drift_client = DriftClient(connection)

# Get spot market info (includes lending rates)
spot_market = await drift_client.get_spot_market_account(0)  # USDC
lending_rate = spot_market.deposit_rate
```

## 5.3 Future Integration

When Drift API access is resolved:

1. Use `/rateHistory?marketIndex={index}` for lending rates
2. Use `/fundingRates?marketName={market}` for perp funding
3. Calculate IF APY from vault amount changes

---

# 6. Data Files Reference

## 6.1 Output Files

| File | Records | Description |
|------|---------|-------------|
| `perps_lp_combined_apy.csv` | 12,985 | All perpetuals LP APY data |
| `perps_lp_final_summary.csv` | 7 | Summary by project |
| `gmx_v2_current_apy.csv` | 354 | GMX V2 current APY (all periods) |
| `jupiter_jlp_historical_apy.csv` | 697 | JLP calculated APY |
| `perps_lp_historical_apy.csv` | 12,288 | DeFiLlama historical data |

## 6.2 Schema: perps_lp_combined_apy.csv

| Column | Type | Description |
|--------|------|-------------|
| date | string | Date (YYYY-MM-DD) |
| pool_id | string | Pool identifier |
| symbol | string | Asset symbol (e.g., "GM:ETH-USDC", "JLP") |
| project | string | Protocol name |
| chain | string | Blockchain |
| tvl_usd | float | Total Value Locked |
| apy | float | Total APY (%) |
| apy_base | float | Base APY component |
| apy_reward | float | Reward APY component |

## 6.3 Schema: jupiter_jlp_historical_apy.csv

| Column | Type | Description |
|--------|------|-------------|
| date | string | Date (YYYY-MM-DD) |
| pool_id | string | Always "jupiter-jlp" |
| symbol | string | Always "JLP" |
| project | string | "jupiter-perpetual-exchange" |
| chain | string | "Solana" |
| tvl_usd | float | JLP pool TVL |
| daily_fees | float | Total daily fees (USD) |
| jlp_fees | float | JLP holder share (75%) |
| apy | float | Annualized APY (%) |

---

# 7. Integration Guide

## 7.1 Loading Data

```python
import pandas as pd

# Load combined perpetuals data
perps_df = pd.read_csv('perps_lp_combined_apy.csv', parse_dates=['date'])

# Filter by protocol
gmx_data = perps_df[perps_df['project'] == 'gmx-v2-perps']
jlp_data = perps_df[perps_df['project'] == 'jupiter-perpetual-exchange']

# Get daily APY for backtesting
jlp_daily = jlp_data[['date', 'apy']].set_index('date')
```

## 7.2 Calculating Strategy Returns

```python
# JLP Strategy (Strategy 2 in diBoaS)
def calculate_jlp_returns(deposit, jlp_data):
    """Calculate compounded returns from JLP APY data"""
    balance = deposit
    
    for _, row in jlp_data.iterrows():
        daily_rate = row['apy'] / 365 / 100
        balance *= (1 + daily_rate)
    
    return balance

# Example: $10,000 invested for 1 year
final_balance = calculate_jlp_returns(10000, jlp_daily.last('365D'))
```

## 7.3 Combining with Price Data

```python
# Merge with asset prices for impermanent loss calculation
prices_df = pd.read_csv('yahoo_historical_prices.csv', parse_dates=['date'])
sol_prices = prices_df[prices_df['symbol'] == 'SOL'][['date', 'close']]

# JLP value = TVL, but composition changes
merged = jlp_data.merge(sol_prices, on='date', how='left')
merged['sol_pct_change'] = merged['close'].pct_change()
```

## 7.4 GMX V2 Current APY Refresh

```python
import requests

def get_gmx_current_apy(period='30d'):
    """Fetch current GMX V2 APY from native API"""
    url = f"https://arbitrum-api.gmxinfra.io/apy?period={period}"
    response = requests.get(url)
    data = response.json()
    
    return {
        addr: info['apy'] * 100  # Convert to percentage
        for addr, info in data.get('markets', {}).items()
    }
```

---

# Appendix: API Reference

## GMX V2 API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/apy` | GET | Current APY for all markets |
| `/markets/info` | GET | Market metadata |
| `/performance/annualized` | GET | Annualized performance |

**Base URL**: `https://arbitrum-api.gmxinfra.io`

## DeFiLlama Fees API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/summary/fees/{protocol}` | GET | Daily fees data |
| `/protocol/{protocol}` | GET | TVL and protocol info |

**Base URL**: `https://api.llama.fi`

## Jupiter (Limited Access)

| Endpoint | Status |
|----------|--------|
| `/v1/info` | ❌ Requires API key |
| Stats page | ✅ Web UI only |

---

*Document compiled December 27, 2025*

*Data should be refreshed daily for production use*
