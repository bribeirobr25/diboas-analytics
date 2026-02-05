# 03 â€” TradFi Markets

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 3.0  
**Last Updated:** January 24, 2026  
**Owner:** Rakia (Investment Analyst) + CTO Board
**Change Log:**
- v3: Marked rotation ETFs (SPY, TLT, XLF, XLU, IWM) as REQUIRED (GAP-001 fix)

---

## Overview

Traditional finance market data provides:
- **Risk Sentiment** â€” Equity indices, VIX
- **Rate Environment** â€” Treasury yields, spreads
- **Currency Context** â€” Dollar strength, EM currencies
- **Commodity Signals** â€” Gold, oil correlation
- **Capital Rotation** â€” Risk-on/off indicators

**Key Insight:** Crypto is now a macro asset. BTC correlates 0.6-0.8 with NASDAQ in risk-on periods.

---

## 1. Equity Indices

### What We Track

**Global (Required):**

| Index | Symbol | Region | Why Track |
|-------|--------|--------|-----------|
| S&P 500 | ^GSPC | US | Risk sentiment benchmark |
| NASDAQ | ^IXIC | US | Tech/growth correlation |
| VIX | ^VIX | US | Fear gauge |

**Regional (Important):**

| Index | Symbol | Region | Why Track |
|-------|--------|--------|-----------|
| Euro Stoxx 50 | ^STOXX50E | EU | EU sentiment |
| DAX | ^GDAXI | Germany | EU industrial |
| Bovespa | ^BVSP | Brazil | Brazil target market |
| Nikkei 225 | ^N225 | Japan | Asia liquidity |
| Hang Seng | ^HSI | Hong Kong | China proxy |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Risk Correlation** | BTC follows equities in risk-on |
| **Regional Context** | EU/Brazil users need local context |
| **Sentiment Gauge** | VIX >30 = fear = potential crypto selloff |
| **Macro Regime** | Equity performance indicates macro regime |

### How to Check

**Frequency:** Daily (EOD), real-time for alerts

**Data Source:** Yahoo Finance (FREE)

```python
import yfinance as yf

def get_equity_indices():
    """Daily equity index collection"""
    
    # Global indices
    global_indices = ['^GSPC', '^IXIC', '^VIX']
    
    # Regional indices
    regional_indices = ['^STOXX50E', '^GDAXI', '^BVSP', '^N225', '^HSI']
    
    all_tickers = global_indices + regional_indices
    
    data = yf.download(
        all_tickers,
        start='2020-01-01',
        end='today'
    )
    
    return data
```

**Alert Thresholds:**

| Index | Change | Alert Level | Crypto Impact |
|-------|--------|-------------|---------------|
| S&P 500 | >Â±2% daily | ðŸŸ  High | Likely crypto follows |
| S&P 500 | >Â±5% daily | ðŸ”´ Critical | Major risk event |
| VIX | >25 | ðŸŸ  High | Fear elevated |
| VIX | >35 | ðŸ”´ Critical | Panic, potential capitulation |
| NASDAQ | >Â±3% daily | ðŸŸ  High | Tech correlation |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| `tradfi_benchmark_data_2020_2025.csv` | âœ… Good | Has S&P, NASDAQ, DAX, Bovespa, VIX |
| Nikkei 225 | ðŸ”´ Missing | Add to file |
| Hang Seng | ðŸ”´ Missing | Add to file |
| Real-time alerts | ðŸ”´ Not built | CTO Board |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R8** | Add Asia indices to TradFi benchmark | Update `tradfi_benchmark_data_2020_2025.csv` |

---

## 2. Rotation ETFs (REQUIRED)

### What We Track

**ðŸ”´ CRITICAL: These ETFs are REQUIRED for capital rotation calculations in Task 1.7.**

| ETF | Symbol | Tracks | Why REQUIRED |
|-----|--------|--------|--------------|
| **SPY** | SPY | S&P 500 | SPY/TLT ratio (risk-on/off) |
| **TLT** | TLT | 20+ Year Treasuries | SPY/TLT ratio (risk-on/off) |
| **XLF** | XLF | Financial Select Sector | XLF/XLU ratio (cyclical/defensive) |
| **XLU** | XLU | Utilities Select Sector | XLF/XLU ratio (cyclical/defensive) |
| **IWM** | IWM | Russell 2000 Small Cap | IWM/SPY ratio (risk appetite) |

### Why REQUIRED

These ETFs enable the four Phase 1 rotation indicators:

| Ratio | ETFs Used | Interpretation |
|-------|-----------|----------------|
| **SPY/TLT** | SPY Ã· TLT | High = Risk-On, Low = Risk-Off |
| **XLF/XLU** | XLF Ã· XLU | High = Cyclical, Low = Defensive |
| **IWM/SPY** | IWM Ã· SPY | High = Risk appetite, Low = Flight to quality |
| **Copper/Gold** | HG=F Ã· GC=F | Economic growth expectations |

### How to Check

**Frequency:** Daily (EOD)

**Data Source:** Yahoo Finance (FREE)

```python
import yfinance as yf

def get_rotation_etfs():
    """
    Collect rotation ETF data for capital rotation analysis.
    REQUIRED for Task 1.7.
    """
    
    # REQUIRED rotation ETFs
    rotation_etfs = ['SPY', 'TLT', 'XLF', 'XLU', 'IWM']
    
    data = yf.download(
        rotation_etfs,
        start='2020-01-01',
        end='today'
    )
    
    # Return in WIDE format for direct ratio calculation
    return data['Close']  # Returns DataFrame with columns: SPY, TLT, XLF, XLU, IWM
```

**Output Format:**

The `tradfi_benchmark_data.csv` should be in **WIDE format**:

```csv
date,spy_close,tlt_close,xlf_close,xlu_close,iwm_close,...
2020-01-02,323.54,139.23,30.44,67.89,166.32,...
2020-01-03,322.41,140.12,30.21,68.01,165.87,...
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| SPY | âœ… Required | Must be in tradfi_benchmark_data.csv |
| TLT | âœ… Required | Must be in tradfi_benchmark_data.csv |
| XLF | âœ… Required | Must be in tradfi_benchmark_data.csv |
| XLU | âœ… Required | Must be in tradfi_benchmark_data.csv |
| IWM | âœ… Required | Must be in tradfi_benchmark_data.csv |

---

## 3. Fixed Income (Yields & Spreads)

### What We Track

**Treasury Yields (Required):**

| Maturity | FRED Series | Why Track |
|----------|-------------|-----------|
| 2-Year | DGS2 | Short-term rate expectations |
| 5-Year | DGS5 | Medium-term |
| 10-Year | DGS10 | Benchmark rate |
| 30-Year | DGS30 | Long-term expectations |

**Yield Curve (Required):**

| Spread | Formula | Why Track |
|--------|---------|-----------|
| 2s10s Spread | 10Y - 2Y | Recession indicator |
| 2s30s Spread | 30Y - 2Y | Long-term expectations |

**Bond ETFs (Current):**

| ETF | Symbol | Tracks |
|-----|--------|--------|
| TLT | TLT | 20+ Year Treasuries |
| AGG | AGG | Total Bond Market |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Opportunity Cost** | Higher yields = competition for crypto |
| **Recession Signal** | Inverted curve = recession warning |
| **Fed Expectations** | 2Y reflects Fed path |
| **Risk-Free Rate** | Benchmark for all returns |

### How to Check

**Frequency:** Daily

**Data Source:** FRED API (FREE)

```python
import requests

FRED_API_KEY = "your_free_api_key"  # Get at fred.stlouisfed.org

def get_treasury_yields():
    """
    Collect Treasury yields from FRED
    """
    series = {
        '2Y': 'DGS2',
        '5Y': 'DGS5',
        '10Y': 'DGS10',
        '30Y': 'DGS30',
    }
    
    all_data = []
    
    for name, series_id in series.items():
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'observation_start': '2020-01-01'
        }
        response = requests.get(url, params=params)
        data = response.json()['observations']
        
        for obs in data:
            if obs['value'] != '.':
                all_data.append({
                    'date': obs['date'],
                    'maturity': name,
                    'yield': float(obs['value'])
                })
    
    return all_data

def calculate_yield_curve():
    """Calculate yield curve spreads"""
    yields = get_treasury_yields()
    
    # Get latest values
    latest = {}
    for y in yields:
        if y['date'] == max(obs['date'] for obs in yields):
            latest[y['maturity']] = y['yield']
    
    spread_2s10s = latest['10Y'] - latest['2Y']
    spread_2s30s = latest['30Y'] - latest['2Y']
    
    return {
        '2s10s_spread': spread_2s10s,
        '2s30s_spread': spread_2s30s,
        'inverted': spread_2s10s < 0
    }
```

**Alert Thresholds:**

| Metric | Threshold | Alert Level | Interpretation |
|--------|-----------|-------------|----------------|
| 10Y yield | >5% | ðŸŸ  High | Tight financial conditions |
| 10Y yield | Change >20bps/day | ðŸŸ  High | Significant move |
| 2s10s spread | <0 (inverted) | ðŸ”´ Critical | Recession signal |
| 2s10s spread | Uninversion | ðŸŸ  High | Recession imminent (historically) |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| TLT (price only) | âœ… Have | In tradfi_benchmark |
| Actual yields (2Y, 10Y, etc.) | ðŸ”´ Missing | Critical gap |
| Yield curve calculation | ðŸ”´ Not built | CTO Board |
| FRED API integration | ðŸ”´ Not built | CTO Board |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R6** | Collect Treasury yields from FRED | `treasury_yields.csv` |

---

## 4. Commodities

### What We Track

| Commodity | Symbol | Why Track |
|-----------|--------|-----------|
| Gold | GC=F | Safe haven, BTC correlation |
| Silver | SI=F | Industrial + monetary |
| Oil (WTI) | CL=F | Inflation input, geopolitics |
| Copper | HG=F | Economic health indicator |

### Why It Matters

| Commodity | Crypto Relationship |
|-----------|---------------------|
| **Gold** | Both "hard money" â€” positive correlation in debasement scenarios |
| **Oil** | Inflation driver â€” high oil = CPI pressure = Fed hawkish = crypto headwind |
| **Copper** | Economic bellwether â€” strong copper = healthy economy = risk-on |

### How to Check

**Frequency:** Daily

**Data Source:** Yahoo Finance (FREE)

```python
def get_commodities():
    """Commodity price collection"""
    tickers = {
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'Oil_WTI': 'CL=F',
        'Copper': 'HG=F',
    }
    
    data = yf.download(list(tickers.values()), period='5y')
    return data
```

**Key Ratios:**

| Ratio | Formula | Signal |
|-------|---------|--------|
| Gold/BTC | GC=F / BTC-USD | Falling = BTC outperforming = risk-on |
| Copper/Gold | HG=F / GC=F | Rising = economic optimism |
| Gold/Silver | GC=F / SI=F | >80 = fear, <60 = optimism |
| Oil/Gold | CL=F / GC=F | Inflation vs deflation |

**Copper/Gold Ratio Note:**
- Copper is quoted in cents/lb (e.g., $4.50 = 450 cents)
- Gold is quoted in $/oz (e.g., ~$2,700)
- Raw ratio will be very small (e.g., 0.0017)
- This is correct â€” the trend matters, not absolute value

**Alert Thresholds:**

| Commodity | Change | Alert Level |
|-----------|--------|-------------|
| Gold | >Â±3% daily | ðŸŸ  High |
| Oil | >Â±5% daily | ðŸŸ  High |
| Oil | >$100/barrel | ðŸŸ  High (inflation risk) |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Gold (GC=F) | âœ… Have | In tradfi_benchmark |
| Oil (CL=F) | âœ… Have | In tradfi_benchmark |
| Silver (SI=F) | âœ… Have | In tradfi_benchmark |
| Copper (HG=F) | âœ… REQUIRED | For Copper/Gold ratio |
| Commodity ratios | ðŸ”´ Not calculated | Add to rotation doc |

---

## 5. Currencies

### What We Track

**Major (Required):**

| Pair | Symbol | Why Track |
|------|--------|-----------|
| DXY (Dollar Index) | DX-Y.NYB | Global dollar strength |
| EUR/USD | EURUSD=X | EU market context |
| GBP/USD | GBPUSD=X | UK exposure |

**Regional (Important):**

| Pair | Symbol | Why Track |
|------|--------|-----------|
| BRL/USD | BRL=X | Brazil market |
| JPY/USD | JPY=X | Carry trade, BOJ policy |
| CNY/USD | CNY=X | China liquidity |

### Why It Matters

| Currency | Crypto Impact |
|----------|---------------|
| **DXY** | Strong inverse correlation â€” DXY up = BTC down |
| **JPY** | Yen weakness = carry trade = risk-on |
| **BRL** | Brazil users care about BRL purchasing power |
| **CNY** | China policy signal |

### How to Check

**Frequency:** Daily

**DXY Interpretation:**

| DXY Level | Interpretation | Crypto Impact |
|-----------|----------------|---------------|
| <100 | Dollar weak | Bullish crypto |
| 100-105 | Neutral | Mixed |
| >105 | Dollar strong | Bearish crypto |
| >110 | Very strong | Significant headwind |

**Collection:**

```python
def get_currencies():
    """Currency pair collection"""
    pairs = {
        'DXY': 'DX-Y.NYB',
        'EUR_USD': 'EURUSD=X',
        'GBP_USD': 'GBPUSD=X',
        'BRL_USD': 'BRL=X',
        'JPY_USD': 'JPY=X',
        'CNY_USD': 'CNY=X',
    }
    
    data = yf.download(list(pairs.values()), period='5y')
    return data
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| DXY | âœ… Have | In tradfi_benchmark |
| EUR/USD | âœ… Have | In tradfi_benchmark |
| BRL/USD | âœ… Have | In tradfi_benchmark |
| JPY/USD | ðŸ”´ Missing | Add |
| CNY/USD | ðŸ”´ Missing | Add |

---

## 6. Volatility

### What We Track

| Index | Symbol | Measures |
|-------|--------|----------|
| VIX | ^VIX | S&P 500 implied volatility |
| VVIX | ^VVIX | Volatility of VIX |
| MOVE | ^MOVE | Bond market volatility |

### Why It Matters

| VIX Level | Market State | Crypto Impact |
|-----------|--------------|---------------|
| <15 | Complacent | Risk-on, bullish |
| 15-20 | Normal | Neutral |
| 20-30 | Elevated fear | Caution |
| 30-40 | High fear | Potential capitulation |
| >40 | Panic | Crisis, forced selling |

### How to Check

**Frequency:** Daily, real-time for spikes

**VIX Term Structure:**

```python
def analyze_vix():
    """VIX analysis"""
    vix = yf.Ticker('^VIX')
    current_vix = vix.info['regularMarketPrice']
    
    # VIX futures for term structure
    # Contango (futures > spot) = normal, complacent
    # Backwardation (futures < spot) = fear, hedging demand
    
    return {
        'vix_level': current_vix,
        'regime': classify_vix_regime(current_vix)
    }

def classify_vix_regime(vix):
    if vix < 15:
        return 'COMPLACENT'
    elif vix < 20:
        return 'NORMAL'
    elif vix < 30:
        return 'ELEVATED'
    elif vix < 40:
        return 'HIGH_FEAR'
    else:
        return 'PANIC'
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| VIX | âœ… Have | In tradfi_benchmark |
| VIX regime classification | ðŸ”´ Not built | CTO Board |
| Spike alerts | ðŸ”´ Not built | CTO Board |

---

## 7. MAG 7 / Tech Stocks

### What We Track

| Stock | Symbol | Why Track |
|-------|--------|-----------|
| Apple | AAPL | Market cap leader |
| Microsoft | MSFT | Enterprise tech |
| Amazon | AMZN | Consumer + cloud |
| Alphabet | GOOGL | Ad market |
| Meta | META | Social/metaverse |
| Nvidia | NVDA | AI bellwether |
| Tesla | TSLA | Risk sentiment, Elon factor |

### Why It Matters

MAG 7 stocks are:
- Highly correlated with NASDAQ
- Indicators of tech/growth sentiment
- Tesla specifically has BTC treasury exposure

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| MAG 7 prices | âœ… Have | In tradfi_benchmark |
| Individual tracking | ðŸŸ¡ Nice to have | Lower priority |

---

## File Inventory

### âœ… Keep As-Is

| File | Contents | Records |
|------|----------|---------|
| `tradfi_benchmark_data_2020_2025.csv` | Indices, commodities, currencies, MAG 7 | 36,532 |

**Tickers in file:**
- Indices: ^GSPC, ^IXIC, ^VIX, ^STOXX50E, ^GDAXI, ^BVSP
- Commodities: GC=F, CL=F, SI=F
- Currencies: DX-Y.NYB, EURUSD=X, BRL=X
- ETFs: TLT, AGG, EEM, EWZ, VNQ
- Stocks: AAPL, AMZN, GOOGL, META, MSFT, NVDA, TSLA

### ðŸ”´ REQUIRED (Must Have)

| Ticker | Name | Priority | Why Required |
|--------|------|----------|--------------|
| **SPY** | S&P 500 ETF | ðŸ”´ REQUIRED | SPY/TLT rotation ratio |
| **TLT** | 20+ Yr Treasury ETF | ðŸ”´ REQUIRED | SPY/TLT rotation ratio |
| **XLF** | Financials ETF | ðŸ”´ REQUIRED | XLF/XLU rotation ratio |
| **XLU** | Utilities ETF | ðŸ”´ REQUIRED | XLF/XLU rotation ratio |
| **IWM** | Russell 2000 ETF | ðŸ”´ REQUIRED | IWM/SPY rotation ratio |
| **HG=F** | Copper Futures | ðŸ”´ REQUIRED | Copper/Gold ratio |

### ðŸ”„ Update (Add Data)

| Current File | Add | Priority |
|--------------|-----|----------|
| `tradfi_benchmark_data_2020_2025.csv` | ^N225 (Nikkei) | ðŸŸ  High |
| `tradfi_benchmark_data_2020_2025.csv` | ^HSI (Hang Seng) | ðŸŸ  High |
| `tradfi_benchmark_data_2020_2025.csv` | JPY=X | ðŸŸ¡ Medium |
| `tradfi_benchmark_data_2020_2025.csv` | CNY=X | ðŸŸ¡ Medium |

### âž• Create New

| File | Contents | Priority |
|------|----------|----------|
| `treasury_yields.csv` | 2Y, 5Y, 10Y, 30Y actual yields | ðŸ”´ Critical |

---

## CTO Board Implementation

### Priority 1: Treasury Yields

```yaml
service: treasury_yield_collector
frequency: "0 18 * * 1-5"  # Daily 18:00 UTC (after US close)
source: FRED API
series:
  - DGS2: "2Y"
  - DGS5: "5Y"
  - DGS10: "10Y"
  - DGS30: "30Y"
output: treasury_yields.csv
calculations:
  - 2s10s_spread: 10Y - 2Y
  - 2s30s_spread: 30Y - 2Y
alerts:
  - yield_spike: >20bps daily change
  - inversion: 2s10s < 0
```

### Priority 2: Rotation ETF Collection

```yaml
service: rotation_etf_collector
frequency: "0 22 * * 1-5"  # Daily 22:00 UTC (after US close)
source: Yahoo Finance
tickers:
  - SPY: "S&P 500 ETF"
  - TLT: "20+ Yr Treasury ETF"
  - XLF: "Financials ETF"
  - XLU: "Utilities ETF"
  - IWM: "Russell 2000 ETF"
output: Update tradfi_benchmark_data.csv (WIDE format)
format: One column per ticker, one row per date
```

### Priority 3: Add Asia Indices

```yaml
service: tradfi_updater
action: add_tickers
tickers:
  - "^N225": "Nikkei 225"
  - "^HSI": "Hang Seng"
  - "JPY=X": "JPY/USD"
  - "CNY=X": "CNY/USD"
output: Update tradfi_benchmark_data_2020_2025.csv
```

### Priority 4: VIX Alerts

```yaml
service: volatility_monitor
frequency: "*/15 * * * *"  # Every 15 minutes during market hours
thresholds:
  warning: 25
  elevated: 30
  critical: 40
output: vix_alerts.json
```

---

## Adelaide Integration

### Daily Context

```markdown
## ðŸ“ˆ TradFi Snapshot

**Equities:** S&P 500 +0.8% | NASDAQ +1.2% | VIX 15.3
**Rates:** 10Y at 4.25% (+5bps) | 2s10s spread: +42bps
**Dollar:** DXY 104.2 (-0.3%)
**Gold:** $2,450 (+0.5%)

**Rotation Signals:**
- SPY/TLT: 7.86 (ABOVE MA50 â€” Risk-On)
- XLF/XLU: 0.71 (ABOVE MA50 â€” Cyclical)
- IWM/SPY: 0.41 (BELOW MA50 â€” Quality preferred)

**Interpretation:** Risk-on environment continues. Low VIX and weakening dollar supportive for crypto.
```

---

**Next Document:** [04_MACRO_ECONOMICS.md](./04_MACRO_ECONOMICS.md)
