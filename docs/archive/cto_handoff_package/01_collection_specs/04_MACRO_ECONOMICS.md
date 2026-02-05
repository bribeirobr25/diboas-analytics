# 04 â€” Macro Economics

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 2.0  
**Last Updated:** January 20, 2026  
**Owner:** Rakia (Investment Analyst) + CTO Board

---

## Overview

Macro economic data provides the fundamental backdrop for all markets:
- **Global Liquidity** â€” M2 money supply (#1 crypto driver)
- **Central Bank Policy** â€” Interest rates, QE/QT
- **Inflation** â€” CPI, real returns
- **Real Yields** â€” Opportunity cost of holding crypto
- **Credit Conditions** â€” Risk appetite

**Critical Insight:** Global M2 liquidity is the single most important macro indicator for crypto. When liquidity expands, risk assets (including crypto) rise. When it contracts, they fall.

---

## 1. Global Liquidity (M2)

### What We Track

| Central Bank | Currency | FRED Series | Why Track |
|--------------|----------|-------------|-----------|
| Federal Reserve | USD | M2SL | Dominant global liquidity |
| ECB | EUR | MYAGM2EZM196N | EU liquidity |
| Bank of Japan | JPY | MYAGM2JPM189N | Japan liquidity, carry trade |
| PBOC | CNY | Manual | China liquidity |

### Why It Matters

**THIS IS THE #1 MACRO INDICATOR FOR CRYPTO**

| M2 Trend | Historical Crypto Response |
|----------|---------------------------|
| M2 YoY growth >5% | Bullish â€” risk assets rise |
| M2 YoY growth 0-5% | Neutral |
| M2 YoY growth <0% | Bearish â€” risk assets fall |

**Correlation:** BTC has ~0.85 correlation with Global M2 on a lagged basis (2-3 months).

**Mechanism:**
1. Central banks print money â†’ M2 increases
2. New money seeks returns â†’ flows into risk assets
3. Crypto benefits as high-beta risk asset
4. Reverse is true during QT

### How to Check

**Frequency:** Weekly (data released monthly, but important to track)

**Data Sources (FREE):**

| Source | Data | Access |
|--------|------|--------|
| FRED | US M2, Japan M2 proxy | API (free key) |
| ECB SDW | Euro Area M2 | API (free) |
| PBOC | China M2 | Manual/news |

**Collection:**

```python
import requests
import pandas as pd

FRED_API_KEY = "your_free_api_key"

def get_global_m2():
    """
    Collect M2 from major central banks
    """
    series = {
        'US_M2': 'M2SL',              # Fed M2 (billions USD)
        'EU_M2': 'MYAGM2EZM196N',     # Euro Area M2
        'JAPAN_M2': 'MYAGM2JPM189N',  # Japan M2
    }
    
    all_data = {}
    
    for name, series_id in series.items():
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'observation_start': '2020-01-01',
            'frequency': 'm'  # Monthly
        }
        response = requests.get(url, params=params)
        data = response.json()['observations']
        all_data[name] = {
            obs['date']: float(obs['value']) 
            for obs in data 
            if obs['value'] != '.'
        }
    
    df = pd.DataFrame(all_data)
    
    # Calculate YoY change
    df['US_M2_YoY'] = df['US_M2'].pct_change(periods=12) * 100
    
    # Global M2 approximation (USD-weighted)
    # Full calculation requires currency conversion
    df['Global_M2_Approx'] = df['US_M2']  # Simplified
    
    return df

def analyze_liquidity_regime():
    """Classify current liquidity regime"""
    df = get_global_m2()
    latest_yoy = df['US_M2_YoY'].iloc[-1]
    
    if latest_yoy > 5:
        return {
            'regime': 'EXPANSION',
            'signal': 'BULLISH',
            'interpretation': 'Liquidity expanding â€” supportive for risk assets'
        }
    elif latest_yoy > 0:
        return {
            'regime': 'SLOW_GROWTH',
            'signal': 'NEUTRAL',
            'interpretation': 'Modest liquidity growth â€” mixed environment'
        }
    else:
        return {
            'regime': 'CONTRACTION',
            'signal': 'BEARISH',
            'interpretation': 'Liquidity contracting â€” headwind for risk assets'
        }
```

**Alert Thresholds:**

| Metric | Threshold | Alert Level | Action |
|--------|-----------|-------------|--------|
| M2 YoY turns positive | From negative | ðŸ”´ Critical | Major bullish signal |
| M2 YoY turns negative | From positive | ðŸ”´ Critical | Major bearish signal |
| M2 MoM >1% | Single month | ðŸŸ  High | Liquidity injection |
| M2 MoM <-1% | Single month | ðŸŸ  High | Liquidity drain |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Global M2 data | ðŸ”´ Missing | **CRITICAL GAP** |
| FRED API integration | ðŸ”´ Not built | CTO Board priority |
| Liquidity regime indicator | ðŸ”´ Not built | CTO Board priority |
| BTC/M2 correlation tracking | ðŸ”´ Not built | Nice to have |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R5** | Collect M2 data from FRED, ECB, BOJ | `global_liquidity.csv` |

---

## 2. Central Bank Policy

### What We Track

| Central Bank | Key Rate | Current | Why Track |
|--------------|----------|---------|-----------|
| Federal Reserve | Fed Funds | ~5.25% | Global benchmark |
| ECB | Main Refi | ~4.00% | EU rates |
| Bank of England | Bank Rate | ~5.00% | UK rates |
| BCB (Brazil) | Selic | ~11.5% | Brazil target market |
| BOJ | Policy Rate | ~0.25% | Japan, carry trade |

### Why It Matters

| Policy Direction | Impact |
|------------------|--------|
| **Cutting rates** | Bullish â€” cheaper money, risk-on |
| **Holding rates** | Neutral â€” stability |
| **Hiking rates** | Bearish â€” tighter money, risk-off |

**Fed Dominance:** The Fed sets the tone for global policy. Other central banks largely follow.

### How to Check

**Frequency:** Event-driven (meetings ~8x/year per central bank)

**Key Dates:**

| Central Bank | Meeting Frequency | Announcement Time |
|--------------|-------------------|-------------------|
| Fed (FOMC) | 8x/year | Wed 14:00 ET |
| ECB | 6x/year | Thu 14:15 CET |
| BoE | 8x/year | Thu 12:00 GMT |
| BCB (Copom) | 8x/year | Wed 18:30 BRT |
| BOJ | 8x/year | Various |

**Data Sources:**

| Source | Data | Access |
|--------|------|--------|
| FRED | Fed Funds effective rate (DFF) | API |
| ECB | ECB rates | Website/API |
| BCB | Selic rate | Website |

```python
def get_fed_funds_rate():
    """Current Fed Funds rate from FRED"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'DFF',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1
    }
    response = requests.get(url, params=params)
    return float(response.json()['observations'][0]['value'])
```

**Alert Triggers:**

| Event | Alert Level | Action |
|-------|-------------|--------|
| Fed rate decision (any) | ðŸ”´ Critical | Adelaide immediate |
| Unexpected cut/hike | ðŸ”´ Critical | Major market event |
| Dot plot shift | ðŸŸ  High | Forward guidance change |
| ECB/BOJ decision | ðŸŸ  High | Regional impact |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| `inflation_savings_analysis_2015_2025.csv` | âœ… Has central bank rates | Keep |
| Fed Funds tracking | âš ï¸ Partial | In existing file |
| Rate decision calendar | ðŸ”´ Not built | Nice to have |
| Automated alerts | ðŸ”´ Not built | CTO Board |

---

## 3. Inflation Data

### What We Track

| Country | Measure | FRED/Source | Why Track |
|---------|---------|-------------|-----------|
| USA | CPI YoY | CPIAUCSL | Fed target, global benchmark |
| Germany | HICP | ECB | EU benchmark |
| Brazil | IPCA | IBGE | Target market |
| UK | CPI | ONS | BoE target |
| Eurozone | HICP | ECB | ECB target |

### Why It Matters

| Inflation Level | Impact |
|-----------------|--------|
| >Target (2%) | Central banks tighten â€” bearish |
| At target | Goldilocks â€” neutral/bullish |
| <Target | Central banks ease â€” bullish |
| Deflation | Crisis mode â€” extreme easing |

**Crypto Narrative:** "Inflation hedge" â€” high inflation can be bullish if seen as fiat debasement.

### How to Check

**Frequency:** Monthly (CPI released monthly)

**US CPI Release:** Usually 2nd week of month, 08:30 ET

```python
def get_us_cpi():
    """US CPI from FRED"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'CPIAUCSL',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': '2020-01-01'
    }
    response = requests.get(url, params=params)
    data = response.json()['observations']
    
    # Calculate YoY inflation
    df = pd.DataFrame(data)
    df['value'] = df['value'].astype(float)
    df['cpi_yoy'] = df['value'].pct_change(periods=12) * 100
    
    return df
```

**Alert Thresholds:**

| CPI YoY | Alert Level | Interpretation |
|---------|-------------|----------------|
| >4% | ðŸŸ  High | Inflation elevated, Fed hawkish |
| >5% | ðŸ”´ Critical | Inflation hot, aggressive tightening |
| <2% | ðŸŸ¡ Medium | Below target, potential easing |
| Surprise >0.3% | ðŸ”´ Critical | Market-moving event |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| `inflation_savings_analysis_2015_2025.csv` | âœ… Good (793 records) | Keep |
| Countries covered | âœ… 6 countries | Germany, Brazil, Spain, UK, USA, France |
| Real-time CPI alerts | ðŸ”´ Not built | Nice to have |

---

## 4. Real Yields

### What We Track

| Metric | Calculation | Source |
|--------|-------------|--------|
| **10Y Real Yield** | 10Y TIPS yield | FRED (DFII10) |
| **10Y Breakeven Inflation** | 10Y Nominal - 10Y Real | FRED (T10YIE) |
| **Calculated Real Yield** | 10Y Nominal - CPI YoY | Derived |

### Why It Matters

**CRITICAL:** Crypto has strong INVERSE correlation with real yields.

| Real Yield | Crypto Impact |
|------------|---------------|
| **Negative** | Bullish â€” holding cash loses value |
| **Near zero** | Neutral |
| **Positive >1%** | Bearish â€” opportunity cost of holding crypto |
| **Positive >2%** | Strongly bearish â€” significant competition |

**Mechanism:**
1. Real yields rise â†’ Risk-free return attractive
2. Investors shift from risk assets to bonds
3. Crypto as zero-yield asset suffers
4. Reverse is true when real yields negative

### How to Check

**Frequency:** Daily

**Data Source:** FRED (FREE)

```python
def get_real_yields():
    """
    Real yields from TIPS
    """
    series = {
        'TIPS_10Y': 'DFII10',        # 10-Year TIPS real yield
        'BREAKEVEN_10Y': 'T10YIE',   # 10-Year breakeven inflation
        'NOMINAL_10Y': 'DGS10',      # 10-Year nominal yield
    }
    
    all_data = {}
    
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
        all_data[name] = {
            obs['date']: float(obs['value']) 
            for obs in data 
            if obs['value'] != '.'
        }
    
    df = pd.DataFrame(all_data)
    
    # Verify: Nominal â‰ˆ Real + Breakeven
    df['Calculated_Real'] = df['NOMINAL_10Y'] - df['BREAKEVEN_10Y']
    
    return df

def analyze_real_yield_regime():
    """Classify real yield environment"""
    df = get_real_yields()
    real_yield = df['TIPS_10Y'].iloc[-1]
    
    if real_yield < -0.5:
        return {
            'regime': 'DEEPLY_NEGATIVE',
            'signal': 'STRONGLY_BULLISH',
            'interpretation': 'Cash losing value â€” strong tailwind for crypto'
        }
    elif real_yield < 0:
        return {
            'regime': 'NEGATIVE',
            'signal': 'BULLISH',
            'interpretation': 'Real yields negative â€” supportive for crypto'
        }
    elif real_yield < 1:
        return {
            'regime': 'LOW_POSITIVE',
            'signal': 'NEUTRAL',
            'interpretation': 'Modest positive real yields â€” mixed'
        }
    elif real_yield < 2:
        return {
            'regime': 'POSITIVE',
            'signal': 'BEARISH',
            'interpretation': 'Real yields positive â€” headwind for crypto'
        }
    else:
        return {
            'regime': 'HIGH_POSITIVE',
            'signal': 'STRONGLY_BEARISH',
            'interpretation': 'High real yields â€” significant crypto headwind'
        }
```

**Alert Thresholds:**

| Real Yield | Alert Level | Crypto Impact |
|------------|-------------|---------------|
| <0% | ðŸŸ¢ Bullish | Tailwind |
| Crosses 0% (either direction) | ðŸ”´ Critical | Regime change |
| >1.5% | ðŸŸ  High | Headwind increasing |
| >2.0% | ðŸ”´ Critical | Significant headwind |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Real yield data | ðŸ”´ Missing | **CRITICAL GAP** |
| TIPS yields | ðŸ”´ Missing | Add |
| Breakeven inflation | ðŸ”´ Missing | Add |
| Regime indicator | ðŸ”´ Not built | CTO Board |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R6** | Real yields from FRED (TIPS) | Include in `treasury_yields.csv` |

---

## 5. Credit Conditions

### What We Track

| Metric | FRED Series | What It Measures |
|--------|-------------|------------------|
| **HY Spread** | BAMLH0A0HYM2 | High-yield bond spread over Treasuries |
| **IG Spread** | BAMLC0A4CBBB | Investment-grade spread |
| **HY-IG Differential** | Calculated | Credit risk appetite |
| **TED Spread** | Calculated | Short-term funding stress |

### Why It Matters

| Spread Direction | Interpretation |
|------------------|----------------|
| **Spreads tightening** | Risk-on â€” credit markets healthy |
| **Spreads widening** | Risk-off â€” credit stress, flight to quality |
| **Spreads blowing out** | Crisis â€” all risk assets suffer |

**Correlation:** Credit spreads and crypto correlate negatively (wider spreads = lower crypto).

### How to Check

**Frequency:** Daily

**Data Source:** FRED (FREE)

```python
def get_credit_spreads():
    """
    Credit spread data from FRED
    """
    series = {
        'HY_Spread': 'BAMLH0A0HYM2',    # ICE BofA High Yield spread
        'IG_Spread': 'BAMLC0A4CBBB',    # ICE BofA BBB spread
    }
    
    all_data = {}
    
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
        all_data[name] = {
            obs['date']: float(obs['value']) 
            for obs in data 
            if obs['value'] != '.'
        }
    
    df = pd.DataFrame(all_data)
    df['HY_IG_Diff'] = df['HY_Spread'] - df['IG_Spread']
    
    return df

def analyze_credit_conditions():
    """Classify credit market conditions"""
    df = get_credit_spreads()
    hy_spread = df['HY_Spread'].iloc[-1]
    
    if hy_spread < 300:  # basis points
        return {
            'regime': 'TIGHT',
            'signal': 'RISK_ON',
            'interpretation': 'Credit markets healthy â€” bullish risk assets'
        }
    elif hy_spread < 500:
        return {
            'regime': 'NORMAL',
            'signal': 'NEUTRAL',
            'interpretation': 'Credit spreads normal â€” mixed'
        }
    elif hy_spread < 700:
        return {
            'regime': 'ELEVATED',
            'signal': 'CAUTION',
            'interpretation': 'Credit stress building â€” risk-off'
        }
    else:
        return {
            'regime': 'CRISIS',
            'signal': 'RISK_OFF',
            'interpretation': 'Credit crisis â€” flight to quality'
        }
```

**Alert Thresholds:**

| HY Spread | Alert Level | Interpretation |
|-----------|-------------|----------------|
| <300bps | ðŸŸ¢ Bullish | Tight spreads, risk-on |
| >400bps | ðŸŸ¡ Medium | Elevated |
| >500bps | ðŸŸ  High | Credit stress |
| >700bps | ðŸ”´ Critical | Crisis levels |
| Daily change >50bps | ðŸ”´ Critical | Rapid widening |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| Credit spread data | ðŸ”´ Missing | Add |
| HY spread tracking | ðŸ”´ Missing | Add |
| Credit regime indicator | ðŸ”´ Not built | CTO Board |

### Research Task

| Task | Description | Output |
|------|-------------|--------|
| **R7** | Credit spreads from FRED | `credit_spreads.csv` |

---

## 6. Economic Indicators (Context)

### What We Track (Lower Priority)

| Indicator | Frequency | Source | Why Track |
|-----------|-----------|--------|-----------|
| GDP Growth | Quarterly | BEA/Eurostat | Economic backdrop |
| Unemployment | Monthly | BLS/Eurostat | Labor market |
| PMI (Manufacturing) | Monthly | ISM/Markit | Leading indicator |
| Consumer Confidence | Monthly | Conference Board | Sentiment |

### Why It Matters

These are **context** indicators â€” they explain the macro backdrop but don't directly drive crypto prices.

### Current Status

| Item | Status | Priority |
|------|--------|----------|
| GDP data | ðŸ”´ Missing | ðŸŸ¢ Low |
| Unemployment | ðŸ”´ Missing | ðŸŸ¢ Low |
| PMI | ðŸ”´ Missing | ðŸŸ¡ Medium |
| Consumer Confidence | ðŸ”´ Missing | ðŸŸ¢ Low |

**Recommendation:** Add PMI as it's a leading indicator. Others are nice-to-have.

---

## File Inventory

### âœ… Keep As-Is

| File | Contents | Records |
|------|----------|---------|
| `inflation_savings_analysis_2015_2025.csv` | Inflation, savings rates, CB rates | 793 |

### âž• Create New (Critical)

| File | Contents | Priority |
|------|----------|----------|
| `global_liquidity.csv` | M2 from Fed, ECB, BOJ | ðŸ”´ Critical |
| `real_yields.csv` | TIPS yields, breakevens | ðŸ”´ Critical |
| `credit_spreads.csv` | HY spread, IG spread | ðŸŸ  High |

---

## CTO Board Implementation

### Priority 1: Global Liquidity (CRITICAL)

```yaml
service: liquidity_monitor
frequency: "0 6 * * 1"  # Weekly Monday (data is monthly)
source: FRED API
series:
  - M2SL: "US M2"
  - MYAGM2EZM196N: "EU M2"
  - MYAGM2JPM189N: "Japan M2"
output: global_liquidity.csv
calculations:
  - yoy_change: Year-over-year percentage
  - regime: EXPANSION / NEUTRAL / CONTRACTION
alerts:
  - regime_change: When YoY crosses 0%
```

### Priority 2: Real Yields (CRITICAL)

```yaml
service: real_yield_monitor
frequency: "0 18 * * 1-5"  # Daily after market close
source: FRED API
series:
  - DFII10: "10Y TIPS Real Yield"
  - T10YIE: "10Y Breakeven Inflation"
output: real_yields.csv
calculations:
  - regime: NEGATIVE / NEUTRAL / POSITIVE
alerts:
  - zero_crossing: When real yield crosses 0%
  - threshold: When real yield > 1.5%
```

### Priority 3: Credit Spreads

```yaml
service: credit_monitor
frequency: "0 18 * * 1-5"  # Daily
source: FRED API
series:
  - BAMLH0A0HYM2: "HY Spread"
  - BAMLC0A4CBBB: "IG Spread"
output: credit_spreads.csv
calculations:
  - hy_ig_diff: HY - IG
  - regime: TIGHT / NORMAL / ELEVATED / CRISIS
alerts:
  - widening: Daily change > 50bps
  - crisis: HY spread > 700bps
```

---

## Adelaide Integration

### Weekly Macro Section

```markdown
## ðŸŒ Macro Environment

**Global Liquidity:** M2 YoY +3.2% (Expanding)
â†’ Tailwind for risk assets

**Real Yields:** -0.3% (Negative)
â†’ Holding cash loses value â€” bullish crypto

**Fed Policy:** Holding at 5.25%, next meeting Feb 5
â†’ No change expected

**Credit Markets:** HY spread 320bps (Tight)
â†’ Risk appetite healthy

**Inflation:** US CPI 2.9% YoY (Elevated but cooling)
â†’ Fed on hold for now

**Bottom Line:** Macro backdrop supportive. Liquidity expanding and real yields negative favor risk assets including crypto.
```

---

## Summary: Priority Ranking

| Metric | Status | Priority | Crypto Impact |
|--------|--------|----------|---------------|
| **Global M2 Liquidity** | ðŸ”´ Missing | ðŸ”´ Critical | #1 driver |
| **Real Yields (TIPS)** | ðŸ”´ Missing | ðŸ”´ Critical | Strong inverse |
| **Credit Spreads** | ðŸ”´ Missing | ðŸŸ  High | Risk sentiment |
| **Fed Funds Rate** | âš ï¸ Partial | ðŸŸ  High | Policy direction |
| **CPI Inflation** | âœ… Have | ðŸŸ¡ Medium | Context |
| **GDP/Unemployment** | ðŸ”´ Missing | ðŸŸ¢ Low | Background |
| **PMI** | ðŸ”´ Missing | ðŸŸ¡ Medium | Leading indicator |

---

**Next Document:** [05_INSTITUTIONAL_FLOWS.md](./05_INSTITUTIONAL_FLOWS.md)
