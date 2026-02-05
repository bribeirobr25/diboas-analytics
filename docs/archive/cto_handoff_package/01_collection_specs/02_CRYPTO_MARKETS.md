# 02 â€” Crypto Markets

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 2.0  
**Last Updated:** January 20, 2026  
**Owner:** Rakia (Investment Analyst) + CTO Board

---

## Overview

Crypto market data covers:
- **Price Data** â€” BTC, ETH, SOL, stablecoins
- **DeFi Yields** â€” Protocol APYs for diBoaS strategies
- **Stablecoin Flows** â€” Supply changes, minting/burning
- **Exchange Data** â€” Volume, reserves, dominance

**Primary Use:** Strategy optimization, yield tracking, risk monitoring

---

## 1. Price Data

### What We Track

| Asset | Symbol | Why Track | diBoaS Relevance |
|-------|--------|-----------|------------------|
| Bitcoin | BTC | Market leader, macro asset | Strategy benchmarks |
| Ethereum | ETH | DeFi backbone | Strategy 4-6 underlying |
| Solana | SOL | Solana strategies | Strategy 7-10 underlying |
| USDC | USDC | Primary stablecoin | All strategies |
| USDT | USDT | Largest stablecoin | TRON focus |
| DAI/USDS | DAI | Sky protocol | Strategy 1-5 |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Strategy Performance** | Crypto exposure affects returns |
| **Correlation Analysis** | BTC leads altcoins |
| **Volatility Assessment** | Risk management |
| **User Context** | Adelaide market updates |

### How to Check

**Frequency:** Real-time for alerts, daily for historical

**Data Sources (FREE):**

| Source | Data | API |
|--------|------|-----|
| CoinGecko | Prices, market cap | api.coingecko.com |
| Yahoo Finance | Historical OHLCV | yfinance Python |
| DeFiLlama | DeFi-specific | api.llama.fi |

**Collection:**

```python
import yfinance as yf

def get_crypto_prices():
    """Daily crypto price collection"""
    tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    data = yf.download(tickers, period='1d')
    return data

# CoinGecko for additional data
import requests

def get_coingecko_data(coin_id):
    """Get detailed coin data"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    return requests.get(url).json()
```

**Key Metrics:**

| Metric | Threshold | Alert |
|--------|-----------|-------|
| BTC 24h change | >Â±5% | ðŸŸ  High |
| BTC 24h change | >Â±10% | ðŸ”´ Critical |
| ETH/BTC ratio | Major shift | ðŸŸ¡ Medium |
| SOL/ETH ratio | Major shift | ðŸŸ¡ Medium |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| `yahoo_historical_prices.csv` | âœ… Good (4,381 records) | Keep, update daily |
| Real-time price feeds | ðŸ”´ Not built | CTO Board |
| Price alert system | ðŸ”´ Not built | CTO Board |

---

## 2. DeFi Protocol Yields

### What We Track

APY data for all protocols used in diBoaS strategies.

**Protocol Coverage:**

| Protocol | Chain | Strategies | Pool ID |
|----------|-------|------------|---------|
| Sky Savings Rate (SSR) | Ethereum | 1-9 | `d8c4eff5-c8a9-46fc-a888-057c4c668e72` |
| Compound V3 USDC | Arbitrum | 1,3,5,7,9 | `d9c395b9-00d0-4426-a6b3-572a6dd68e54` |
| Aave V3 USDC | Arbitrum | 4-6 | Various |
| Jito (JitoSOL) | Solana | 7,9 | `0e7d0722-9054-4907-8593-567b353c0900` |
| Sanctum Infinity (INF) | Solana | 2,4,6,8,10 | Custom calculation |
| Jupiter JLP | Solana | 9-10 | Custom |
| GMX V2 | Arbitrum | 9-10 | Custom |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Strategy Returns** | APY directly affects user returns |
| **Allocation Decisions** | Higher APY = potential reallocation |
| **Risk Assessment** | APY spikes may indicate risk |
| **Historical Analysis** | Backtest validation |

### How to Check

**Frequency:** Daily

**Data Sources (FREE):**

| Protocol | Source | Method |
|----------|--------|--------|
| Most DeFi | DeFiLlama Yields API | Direct API |
| Sanctum | DeFiLlama Protocol + Fees | Calculated |
| Jupiter JLP | Jupiter API | Direct API |
| GMX V2 | GMX Subgraph | GraphQL |

**Collection Methods:**

```python
# DeFiLlama Yields API (most protocols)
def get_defillama_pool(pool_id):
    url = f"https://yields.llama.fi/chart/{pool_id}"
    response = requests.get(url)
    return response.json()['data']

# Sky SSR
sky_data = get_defillama_pool('d8c4eff5-c8a9-46fc-a888-057c4c668e72')

# Compound V3 Arbitrum
compound_data = get_defillama_pool('d9c395b9-00d0-4426-a6b3-572a6dd68e54')

# Jito
jito_data = get_defillama_pool('0e7d0722-9054-4907-8593-567b353c0900')
```

**Sanctum INF Special Handling:**

```python
def calculate_sanctum_apy():
    """
    Sanctum INF requires calculated APY:
    Total APY = Base Staking APY (~7.5%) + Trading Fee APY
    Trading Fee APY = (Daily Fees Ã— 365) / TVL Ã— 100
    """
    # Get TVL history
    tvl = requests.get("https://api.llama.fi/protocol/sanctum-infinity").json()
    
    # Get fees history
    fees = requests.get("https://api.llama.fi/summary/fees/sanctum-infinity").json()
    
    # Calculate APY
    # ... calculation logic
```

**Alert Thresholds:**

| Change | Alert Level | Action |
|--------|-------------|--------|
| APY drops >50% | ðŸ”´ Critical | Review strategy allocation |
| APY spikes >3x | ðŸŸ  High | May indicate risk/opportunity |
| TVL drops >30% | ðŸ”´ Critical | Protocol risk assessment |
| New pool >10% APY | ðŸŸ¡ Medium | Research opportunity |

### Current Status

| File | Records | Status | Notes |
|------|---------|--------|-------|
| `defillama_historical_apy.csv` | 47,497 | âœ… Excellent | Keep, update daily |
| `sky_ssr_historical_apy.csv` | 334 | âœ… Excellent | Keep, update daily |
| `compound_v3_arbitrum_usdc_apy.csv` | 840 | âœ… Excellent | Keep, update daily |
| `sanctum_inf_historical_apy.csv` | 667 | âœ… Excellent | Keep, update daily |
| `jito_extended_apy.csv` | 301 | âœ… Excellent | Keep, update daily |
| `jupiter_jlp_historical_apy.csv` | 698 | âœ… Good | Keep, update daily |
| `perps_lp_combined_apy.csv` | 12,986 | âœ… Good | Keep |
| `gmx_v2_current_apy.csv` | 355 | âœ… Good | Keep, update daily |
| `sanctum_tvl_history.csv` | 668 | âœ… Good | Keep |
| Automated daily collection | ðŸ”´ Not built | CTO Board priority |

---

## 3. Stablecoin Supply & Flows

### What We Track

| Stablecoin | Market Cap | Primary Chain | Why Track |
|------------|------------|---------------|-----------|
| USDT | $140B+ | Tron, Ethereum | Largest, EM demand |
| USDC | $45B+ | Ethereum, Solana | Primary diBoaS stable |
| DAI/USDS | $5B+ | Ethereum | Sky protocol |
| EURC | $100M+ | Ethereum | EU users |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Liquidity Indicator** | Stablecoin growth = dry powder |
| **Institutional Signal** | Large mints precede buying |
| **Regional Demand** | USDT growth = EM adoption |
| **Risk Monitoring** | Depeg risk assessment |

### How to Check

**Frequency:** Daily

**Data Source:** DeFiLlama Stablecoins API (FREE)

```python
def get_stablecoin_supply():
    """
    DeFiLlama Stablecoins API
    """
    # USDC (id=1)
    usdc = requests.get("https://stablecoins.llama.fi/stablecoin/1").json()
    
    # USDT (id=2)
    usdt = requests.get("https://stablecoins.llama.fi/stablecoin/2").json()
    
    # DAI (id=3)
    dai = requests.get("https://stablecoins.llama.fi/stablecoin/3").json()
    
    return {
        'usdc': usdc['currentChainCirculating'],
        'usdt': usdt['currentChainCirculating'],
        'dai': dai['currentChainCirculating']
    }

def detect_large_mints():
    """Alert on large stablecoin mints"""
    current = get_stablecoin_supply()
    previous = get_previous_supply()
    
    for stable, supply in current.items():
        change = supply - previous[stable]
        if change > 500_000_000:  # $500M
            generate_alert('STABLECOIN_MINT', stable, change)
```

**Alert Thresholds:**

| Event | Threshold | Alert Level | Interpretation |
|-------|-----------|-------------|----------------|
| USDC mint | >$500M/day | ðŸŸ  High | Institutional buying coming |
| USDT mint | >$500M/day | ðŸŸ¡ Medium | EM demand |
| Stablecoin burn | >$500M/day | ðŸŸ  High | Redemptions |
| USDC depeg | >0.5% | ðŸ”´ Critical | Risk event |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Stablecoin supply tracking | ðŸ”´ Not built | CTO Board |
| Mint/burn alerts | ðŸ”´ Not built | CTO Board |
| Chain breakdown | ðŸ”´ Not built | Nice to have |

---

## 4. Exchange Reserves

### What We Track

Total crypto held on exchanges â€” a proxy for selling pressure.

### Why It Matters

| Trend | Interpretation |
|-------|----------------|
| Reserves decreasing | Accumulation (bullish) |
| Reserves increasing | Potential selling (bearish) |
| Sudden spike | Large deposit = imminent sale |

### How to Check

**Frequency:** Daily

**Data Sources:**

| Source | Access | Data |
|--------|--------|------|
| CryptoQuant | Free tier (limited) | BTC reserves |
| Glassnode | Free tier (limited) | Exchange balances |
| Dune Analytics | FREE | Community dashboards |

**Dune Query Example:**

```sql
-- Exchange reserves proxy (labeled addresses)
SELECT 
    date_trunc('day', block_time) AS date,
    SUM(value/1e18) AS total_eth
FROM ethereum.traces
WHERE to IN (SELECT address FROM labels.exchange_addresses)
GROUP BY 1
ORDER BY 1 DESC
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Exchange reserve tracking | ðŸ”´ Not built | Phase 2 |
| Dune integration | ðŸ”´ Not built | CTO Board |

---

## 5. Market Dominance & Ratios

### What We Track

| Ratio | Formula | Signal |
|-------|---------|--------|
| BTC Dominance | BTC Market Cap / Total Market Cap | Risk appetite |
| ETH/BTC | ETH price / BTC price | Altcoin sentiment |
| SOL/ETH | SOL price / ETH price | L1 rotation |
| Stablecoin Ratio | Stablecoin MC / Total MC | Dry powder |

### Why It Matters

| Ratio Movement | Interpretation |
|----------------|----------------|
| BTC dominance rising | Flight to quality, risk-off |
| BTC dominance falling | Altcoin season, risk-on |
| ETH/BTC rising | ETH outperforming, DeFi sentiment |
| Stablecoin ratio rising | Cautious, waiting |

### How to Check

**Frequency:** Daily

**Calculation:**

```python
def get_market_ratios():
    """Calculate key market ratios"""
    
    # CoinGecko global data
    global_data = requests.get(
        "https://api.coingecko.com/api/v3/global"
    ).json()['data']
    
    btc_dominance = global_data['market_cap_percentage']['btc']
    eth_dominance = global_data['market_cap_percentage']['eth']
    
    # Price ratios from existing data
    btc_price = get_price('BTC')
    eth_price = get_price('ETH')
    sol_price = get_price('SOL')
    
    return {
        'btc_dominance': btc_dominance,
        'eth_btc_ratio': eth_price / btc_price,
        'sol_eth_ratio': sol_price / eth_price,
    }
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Dominance tracking | ðŸ”´ Not built | Easy to add |
| Ratio calculations | ðŸ”´ Not built | CTO Board |

---

## 6. RWA Protocol Data

### What We Track

Real World Asset tokenization protocols for potential future integration.

| Protocol | TVL | APY Range | Status |
|----------|-----|-----------|--------|
| Ondo USDY | $700M | 4.25-5.3% | Research |
| OpenEden TBILL | $286M | 4.5-5.3% | Research |
| Maple Finance | $4B | 8-20% | Research |
| Centrifuge | $650M | 3-8% | Research |

### Why It Matters

RWA protocols offer:
- T-Bill exposure on-chain
- Potentially lower smart contract risk
- Regulatory clarity (some)

### Current Status

| File | Records | Status | Notes |
|------|---------|--------|-------|
| `rwa_protocol_comparison.csv` | 10 | âœ… Good | Keep for research |
| `rwa_historical_defaults.csv` | 9 | âœ… Good | Risk documentation |

**Not in current strategies** â€” research for Phase 2.

---

## File Inventory

### âœ… Keep As-Is

| File | Records | Update Frequency |
|------|---------|------------------|
| `defillama_historical_apy.csv` | 47,497 | Daily |
| `sky_ssr_historical_apy.csv` | 334 | Daily |
| `compound_v3_arbitrum_usdc_apy.csv` | 840 | Daily |
| `sanctum_inf_historical_apy.csv` | 667 | Daily |
| `jito_extended_apy.csv` | 301 | Daily |
| `sanctum_tvl_history.csv` | 668 | Daily |
| `defillama_target_pools.csv` | 777 | Weekly |
| `jupiter_jlp_historical_apy.csv` | 698 | Daily |
| `perps_lp_combined_apy.csv` | 12,986 | Weekly |
| `gmx_v2_current_apy.csv` | 355 | Daily |
| `perps_lp_final_summary.csv` | 8 | Monthly |
| `defillama_protocol_summary.csv` | 10 | Weekly |
| `yahoo_historical_prices.csv` | 4,381 | Daily |
| `rwa_protocol_comparison.csv` | 10 | Quarterly |
| `rwa_historical_defaults.csv` | 9 | Event-based |

### âž• Create New

| File | Priority | Description |
|------|----------|-------------|
| `stablecoin_supply.csv` | ðŸŸ  High | Daily supply tracking |
| `market_ratios.csv` | ðŸŸ¡ Medium | Dominance, ratios |
| `exchange_reserves.csv` | ðŸŸ¡ Medium | Reserve tracking |

---

## CTO Board Implementation

### Priority 1: Automated Yield Collection

```yaml
service: yield_collector
frequency: "0 6 * * *"  # Daily 06:00 UTC
pools:
  - sky_ssr: "d8c4eff5-c8a9-46fc-a888-057c4c668e72"
  - compound_arb: "d9c395b9-00d0-4426-a6b3-572a6dd68e54"
  - jito: "0e7d0722-9054-4907-8593-567b353c0900"
output: Append to respective CSV files
```

### Priority 2: Stablecoin Monitor

```yaml
service: stablecoin_monitor
frequency: "0 * * * *"  # Hourly
stablecoins: [usdc, usdt, dai]
alert_threshold: 500_000_000  # $500M
output: stablecoin_supply.csv, alerts
```

### Priority 3: Price Alerts

```yaml
service: price_alerts
frequency: "*/5 * * * *"  # Every 5 minutes
assets: [BTC, ETH, SOL]
thresholds:
  daily_change_warning: 5%
  daily_change_critical: 10%
output: price_alerts.json
```

---

**Next Document:** [03_TRADFI_MARKETS.md](./03_TRADFI_MARKETS.md)
