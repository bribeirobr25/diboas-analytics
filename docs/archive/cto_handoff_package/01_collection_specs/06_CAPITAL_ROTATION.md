# 06 Ã¢â‚¬â€ Capital Rotation & Cycles

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 2.1  
**Last Updated:** January 24, 2026  
**Change:** GAP-012 fix â€” Added XLF/XLU and IWM/SPY to priority table with Phase annotations  
**Owner:** Rakia (Investment Analyst) + CTO Board  
**Contributors:** Kevin Wadsworth (@NorthstarCharts), Patrick Karim (@badcharts1)

---

## Overview

Capital rotation analysis tracks how money flows between asset classes:
- **Intermarket Ratios** Ã¢â‚¬â€ Stocks vs Bonds, Gold vs Stocks, BTC vs Gold
- **Cycle Analysis** Ã¢â‚¬â€ Commodity supercycle, dollar cycle, rate cycle
- **Regime Detection** Ã¢â‚¬â€ Risk-on vs Risk-off environments

**Key Insight:** Markets move in cycles. Understanding where we are in the cycle helps position portfolios.

---

## 1. Intermarket Rotation Ratios

### What We Track

| Ratio | Formula | What It Measures |
|-------|---------|------------------|
| **Stocks/Bonds** | SPY/TLT | Risk appetite |
| **Commodities/Stocks** | DJP/SPY | Inflation expectations |
| **Gold/Stocks** | GLD/SPY | Fear vs greed |
| **Gold/BTC** | GC=F / BTC-USD | Hard asset preference |
| **BTC/NASDAQ** | BTC-USD / QQQ | Tech correlation |
| **Copper/Gold** | HG=F / GC=F | Economic optimism |
| **Oil/Gold** | CL=F / GC=F | Inflation vs deflation |

### Why It Matters

**The Capital Rotation Cycle:**

```
BONDS Ã¢â€ â€™ STOCKS Ã¢â€ â€™ COMMODITIES Ã¢â€ â€™ HARD ASSETS Ã¢â€ â€™ CASH Ã¢â€ â€™ Repeat

Early Cycle:    Bonds outperform (rates falling, recovery beginning)
Mid Cycle:      Stocks outperform (growth accelerating)
Late Cycle:     Commodities outperform (inflation rising)
End Cycle:      Hard assets outperform (currency debasement fears)
Recession:      Cash outperforms (deflation, deleveraging)
```

**Ratio Interpretations:**

| Ratio | Rising Means | Falling Means |
|-------|--------------|---------------|
| SPY/TLT | Risk-on, stocks preferred | Risk-off, bonds preferred |
| GLD/SPY | Defensive, fear | Aggressive, greed |
| Gold/BTC | Traditional safe haven preferred | "Digital gold" preferred |
| Copper/Gold | Economic optimism | Economic pessimism |

### How to Check

**Frequency:** Daily

**Calculation:**

```python
import yfinance as yf
import pandas as pd

def calculate_rotation_ratios():
    """
    Calculate all intermarket rotation ratios
    """
    # Download price data
    tickers = ['SPY', 'TLT', 'GLD', 'DJP', 'QQQ', 'BTC-USD', 'GC=F', 'HG=F', 'CL=F']
    data = yf.download(tickers, period='5y')['Adj Close']
    
    # Calculate ratios
    ratios = pd.DataFrame()
    ratios['Stocks_Bonds'] = data['SPY'] / data['TLT']
    ratios['Commodities_Stocks'] = data['DJP'] / data['SPY']
    ratios['Gold_Stocks'] = data['GLD'] / data['SPY']
    ratios['Gold_BTC'] = data['GC=F'] / data['BTC-USD']
    ratios['BTC_NASDAQ'] = data['BTC-USD'] / data['QQQ']
    ratios['Copper_Gold'] = data['HG=F'] / data['GC=F']
    ratios['Oil_Gold'] = data['CL=F'] / data['GC=F']
    
    return ratios

def interpret_ratios(ratios: pd.DataFrame) -> dict:
    """
    Interpret current ratio readings
    """
    latest = ratios.iloc[-1]
    ma_50 = ratios.rolling(50).mean().iloc[-1]
    
    signals = {}
    
    # Stocks/Bonds
    if latest['Stocks_Bonds'] > ma_50['Stocks_Bonds']:
        signals['risk_appetite'] = 'RISK_ON'
    else:
        signals['risk_appetite'] = 'RISK_OFF'
    
    # Gold/BTC
    if latest['Gold_BTC'] > ma_50['Gold_BTC']:
        signals['hard_asset_preference'] = 'TRADITIONAL'
    else:
        signals['hard_asset_preference'] = 'DIGITAL'
    
    # Copper/Gold
    if latest['Copper_Gold'] > ma_50['Copper_Gold']:
        signals['economic_outlook'] = 'OPTIMISTIC'
    else:
        signals['economic_outlook'] = 'PESSIMISTIC'
    
    return signals
```

**Alert Thresholds:**

| Ratio | Signal | Alert Level |
|-------|--------|-------------|
| SPY/TLT breaks 50-day MA | Trend change | Ã°Å¸Å¸Â  High |
| Gold/BTC > 0.04 | Gold outperforming | Ã°Å¸Å¸Â¡ Medium |
| Gold/BTC < 0.02 | BTC outperforming | Ã°Å¸Å¸Â¡ Medium |
| Copper/Gold rising strongly | Economic recovery | Ã°Å¸Å¸Â¡ Medium |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Rotation ratio calculations | Ã°Å¸â€Â´ Not built | CTO Board |
| Historical ratio data | Ã°Å¸â€Â´ Not collected | Research task R10 |
| Regime detection | Ã°Å¸â€Â´ Not built | CTO Board |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R10** | Calculate historical rotation ratios | `rotation_indicators.csv` |

---

## 2. Cycle Analysis

### Major Cycles

**1. Commodity Supercycle (Multi-decade)**

| Phase | Period | Characteristics |
|-------|--------|-----------------|
| Last Bottom | ~2020 | COVID crash, peak pessimism |
| Current Phase | Early-Mid Cycle | Commodities outperforming stocks |
| Expected Peak | ~2030-2035 | Based on historical patterns |

**Implication:** Bullish for hard assets (gold, BTC) through this decade.

**2. Dollar Cycle (8-12 years)**

| Phase | Indicator | Crypto Impact |
|-------|-----------|---------------|
| Dollar Bull | DXY rising | Bearish crypto |
| Dollar Bear | DXY falling | Bullish crypto |

| Recent History | |
|----------------|--|
| DXY Peak | September 2022 (~114) |
| Current | ~104 |
| Thesis | Secular decline ahead |

**Implication:** If dollar enters secular decline, tailwind for crypto.

**3. Interest Rate Cycle (40+ years)**

| Phase | Period | Rates |
|-------|--------|-------|
| Bond Bull Market | 1981-2020 | Rates falling for 40 years |
| Current | Normalization | Rates volatile, higher |
| Next Phase | TBD | Eventually lower |

**4. Equity Valuation Cycle (Buffett Indicator)**

```
Buffett Indicator = Total Market Cap / GDP

Levels:
<80%   = Undervalued
80-100% = Fair value
100-150% = Overvalued
>150% = Extremely overvalued

Current: ~180% (historically elevated)
```

### How to Check

**Frequency:** Monthly (cycles are long-term)

**Data Sources:**

| Indicator | Source | Access |
|-----------|--------|--------|
| DXY | Yahoo Finance | FREE |
| Commodity Index | DJP, GSG | FREE |
| Buffett Indicator | FRED (WILL5000/GDP) | FREE |
| Historical cycles | Manual analysis | Ã¢â‚¬â€ |

```python
def get_buffett_indicator():
    """
    Buffett Indicator = Wilshire 5000 / GDP
    """
    # Wilshire 5000 total market cap
    wilshire = get_fred_series('WILL5000IND')
    
    # Nominal GDP
    gdp = get_fred_series('GDP')
    
    # Calculate ratio
    buffett = (wilshire / gdp) * 100
    
    return {
        'value': buffett.iloc[-1],
        'valuation': classify_valuation(buffett.iloc[-1])
    }

def classify_valuation(buffett_value):
    if buffett_value < 80:
        return 'UNDERVALUED'
    elif buffett_value < 100:
        return 'FAIR_VALUE'
    elif buffett_value < 150:
        return 'OVERVALUED'
    else:
        return 'EXTREMELY_OVERVALUED'
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Cycle tracking | Ã°Å¸â€Â´ Not built | Manual analysis |
| Buffett indicator | Ã°Å¸â€Â´ Not calculated | Add |
| Dollar cycle position | Ã°Å¸â€Â´ Not tracked | Add |

---

## 3. Regime Detection

### Risk Regimes

| Regime | Characteristics | Crypto Response |
|--------|-----------------|-----------------|
| **Risk-On** | VIX <20, SPY/TLT rising, spreads tight | Bullish |
| **Risk-Off** | VIX >25, SPY/TLT falling, spreads widening | Bearish |
| **Euphoria** | VIX <15, extreme greed | Caution (top forming) |
| **Panic** | VIX >35, extreme fear | Potential bottom |

### Regime Detection Algorithm

```python
def detect_market_regime():
    """
    Multi-factor regime detection
    """
    # Factor 1: VIX Level
    vix = get_current_vix()
    
    # Factor 2: SPY/TLT ratio vs 50-day MA
    spy_tlt = calculate_ratio('SPY', 'TLT')
    spy_tlt_ma = spy_tlt.rolling(50).mean().iloc[-1]
    
    # Factor 3: Credit spreads
    hy_spread = get_hy_spread()
    
    # Factor 4: Stablecoin supply trend
    stablecoin_growth = get_stablecoin_mom()
    
    # Scoring
    score = 0
    
    if vix < 20:
        score += 1
    elif vix > 30:
        score -= 2
    
    if spy_tlt.iloc[-1] > spy_tlt_ma:
        score += 1
    else:
        score -= 1
    
    if hy_spread < 400:
        score += 1
    elif hy_spread > 600:
        score -= 2
    
    if stablecoin_growth > 0:
        score += 1
    
    # Classify regime
    if score >= 3:
        return 'STRONG_RISK_ON'
    elif score >= 1:
        return 'RISK_ON'
    elif score >= -1:
        return 'NEUTRAL'
    elif score >= -3:
        return 'RISK_OFF'
    else:
        return 'STRONG_RISK_OFF'
```

### BTC-Specific Regime

| Regime | BTC Dominance | ETH/BTC | Signal |
|--------|---------------|---------|--------|
| **BTC Season** | Rising (>50%) | Falling | Flight to quality in crypto |
| **Alt Season** | Falling (<45%) | Rising | Risk-on, speculation |
| **Stablecoin Season** | Ã¢â‚¬â€ | Ã¢â‚¬â€ | Crypto-wide risk-off |

```python
def detect_crypto_regime():
    """
    Crypto-specific regime detection
    """
    btc_dom = get_btc_dominance()
    eth_btc = get_ratio('ETH', 'BTC')
    stablecoin_ratio = get_stablecoin_ratio()
    
    if btc_dom > 55:
        return 'BTC_SEASON'
    elif btc_dom < 42 and eth_btc > eth_btc_ma:
        return 'ALT_SEASON'
    elif stablecoin_ratio > 0.15:
        return 'STABLECOIN_SEASON'
    else:
        return 'MIXED'
```

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Regime detection | Ã°Å¸â€Â´ Not built | CTO Board |
| Multi-factor model | Ã°Å¸â€Â´ Not built | CTO Board |
| Crypto regime | Ã°Å¸â€Â´ Not built | CTO Board |

---

## 4. Kevin Wadsworth / Patrick Karim Methodology

### Capital Rotation Framework

From NorthstarBadCharts methodology:

**Key Principles:**

1. **Track ratios, not just prices** Ã¢â‚¬â€ SPY/TLT tells more than SPY alone
2. **Long-term cycles matter** Ã¢â‚¬â€ Commodity supercycle, dollar cycle
3. **Mean reversion on extreme readings** Ã¢â‚¬â€ Extremes don't last
4. **Sector rotation leads macro** Ã¢â‚¬â€ Sectors rotate before indices

**Their Key Ratios:**

| Ratio | What Kevin/Patrick Track |
|-------|--------------------------|
| Gold/Silver | Risk appetite in metals |
| Copper/Gold | Economic vs defensive |
| XLE/SPY | Energy rotation |
| XLF/SPY | Financials rotation |
| TLT/IEF | Duration preference |

### Sector Rotation (Advanced)

```
Recession Ã¢â€ â€™ Recovery Ã¢â€ â€™ Expansion Ã¢â€ â€™ Late Cycle Ã¢â€ â€™ Recession

Recession:       Consumer Staples, Utilities outperform
Recovery:        Financials, Consumer Discretionary outperform
Expansion:       Technology, Industrials outperform
Late Cycle:      Energy, Materials outperform
```

### Implementation for diBoaS

Focus on the **key ratios that matter for crypto**:

| Priority | Ratio | Why | Phase |
|----------|-------|-----|-------|
| ðŸ”´ Critical | SPY/TLT | Risk appetite | Phase 1 |
| ðŸ”´ Critical | Gold/BTC | Hard asset preference | Phase 2 |
| ðŸŸ  High | Copper/Gold | Economic outlook | Phase 1 |
| ðŸŸ  High | XLF/XLU | Cyclical vs Defensive (Financials/Utilities) | Phase 1 |
| ðŸŸ  High | IWM/SPY | Risk appetite (Small Cap/Large Cap) | Phase 1 |
| ðŸŸ  High | DXY trend | Dollar cycle | Phase 2 |
| ðŸŸ¡ Medium | Sector rotations | Advanced context | Phase 2 |

**Phase Notes:**
- **Phase 1 ratios** are collected in Task 1.7 of the manual pipeline and included in `rotation_indicators.csv`
- **Phase 2 ratios** require additional data sources and will be added in future iterations

---

## File Inventory

### Ã¢Å¾â€¢ Create New

| File | Contents | Priority |
|------|----------|----------|
| `rotation_indicators.csv` | All rotation ratios, daily | Ã°Å¸Å¸Â  High |
| `cycle_positions.csv` | Current cycle phase estimates | Ã°Å¸Å¸Â¡ Medium |
| `regime_history.csv` | Historical regime classifications | Ã°Å¸Å¸Â¡ Medium |

---

## CTO Board Implementation

### Priority 1: Rotation Ratio Calculator

```yaml
service: rotation_calculator
frequency: "0 22 * * 1-5"  # Daily after market close
inputs:
  - SPY, TLT, GLD, DJP, QQQ, BTC-USD, GC=F, HG=F, CL=F
calculations:
  - stocks_bonds: SPY / TLT
  - gold_stocks: GLD / SPY
  - gold_btc: GC=F / BTC-USD
  - copper_gold: HG=F / GC=F
  - btc_nasdaq: BTC-USD / QQQ
outputs:
  - rotation_indicators.csv
  - 50-day MA for each ratio
  - Ratio vs MA signal
alerts:
  - ma_crossover: Ratio crosses 50-day MA
```

### Priority 2: Regime Detector

```yaml
service: regime_detector
frequency: "0 22 * * 1-5"  # Daily
inputs:
  - VIX level
  - SPY/TLT vs MA
  - Credit spreads
  - Stablecoin growth
  - BTC dominance
outputs:
  - Current regime (RISK_ON / RISK_OFF / etc.)
  - Regime change alerts
```

---

## Adelaide Integration

### Weekly Rotation Section

```markdown
## Ã°Å¸â€â€ž Capital Rotation

**Risk Appetite (SPY/TLT):** Above 50-day MA Ã¢â€ â€™ Risk-On
**Gold vs BTC:** Ratio at 0.023 Ã¢â€ â€™ BTC outperforming Ã¢â€ â€™ Risk-On
**Economic Outlook (Cu/Au):** Rising Ã¢â€ â€™ Economic optimism
**Dollar (DXY):** 104.2, below 2022 highs Ã¢â€ â€™ Supportive for crypto

**Cycle Position:**
- Commodity Supercycle: Early-Mid (bullish hard assets)
- Dollar Cycle: Potential secular decline (bullish crypto)
- Rate Cycle: Normalization (volatile)

**Current Regime:** RISK-ON
- VIX low (15)
- Spreads tight (320bps)
- Equities outperforming bonds
- Crypto dominance shifting to alts

**Implication:** Environment favors risk assets including crypto. Continue strategic accumulation.
```

---

**Next Document:** [07_NEWS_AND_SENTIMENT.md](./07_NEWS_AND_SENTIMENT.md)
