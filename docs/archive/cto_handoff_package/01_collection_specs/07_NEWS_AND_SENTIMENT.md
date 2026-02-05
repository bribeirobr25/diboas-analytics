# 07 â€” News & Sentiment

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 3.0  
**Last Updated:** January 24, 2026  
**Owner:** Rakia (Investment Analyst) + CMO Board
**Change Log:**
- v3: Added complete Alternative.me Fear & Greed API documentation (GAP-006 fix)

---

## Overview

News and sentiment monitoring provides:
- **Breaking Events** â€” Market-moving news
- **Sentiment Indicators** â€” Contrarian signals
- **Regulatory Updates** â€” Policy changes
- **Keyword Monitoring** â€” Alert triggers

**Key Insight:** Sentiment indicators are best used as contrarian signals. Extreme fear = potential buying opportunity. Extreme greed = potential selling opportunity.

---

## 1. Data Sources

### Tier 1: Essential (FREE)

| Source | Type | What For | URL |
|--------|------|----------|-----|
| **FRED** | Data | US economic data | fred.stlouisfed.org |
| **ECB SDW** | Data | EU economic data | sdw.ecb.europa.eu |
| **DeFiLlama** | Data | DeFi TVL, yields, stablecoins | defillama.com |
| **CoinGecko** | Data | Crypto prices, dominance | coingecko.com |
| **Alternative.me** | Data | Crypto Fear & Greed Index | api.alternative.me |
| **The Block** | News | Crypto industry news | theblock.co |
| **CoinDesk** | News | Crypto news | coindesk.com |
| **SEC EDGAR** | Filings | 13F, 8-K, 10-Q | sec.gov/edgar |

### Tier 2: Important (FREE/Low Cost)

| Source | Type | What For | Cost |
|--------|------|----------|------|
| **Messari** | Research | Crypto analysis | Free tier |
| **Glassnode** | On-chain | Metrics | Free tier |
| **Dune Analytics** | On-chain | Custom queries | FREE |
| **Trading Economics** | Data | Global economic | Free tier |
| **CME FedWatch** | Data | Rate expectations | FREE |

### Tier 3: Regional (Target Markets)

| Region | Source | What For |
|--------|--------|----------|
| **US** | Fed statements, SEC | Policy, regulatory |
| **EU** | ECB press releases | ECB policy |
| **EU** | MiCA updates | Crypto regulation |
| **Brazil** | BCB (Banco Central) | Selic, policy |
| **Brazil** | CVM | Crypto regulation |
| **Brazil** | Valor EconÃ´mico, InfoMoney | Local news |
| **Asia** | BOJ statements | Japan liquidity |
| **Asia** | Nikkei Asia | Asia macro |

### Tier 4: Premium (If Budget Allows)

| Source | What For | Cost |
|--------|----------|------|
| Bloomberg Terminal | Everything | $$$$ |
| Financial Times | EU analysis | $ |
| Wall Street Journal | US policy | $ |
| Delphi Digital | Crypto research | $$ |
| Nansen | On-chain | $$ |
| Arkham Pro | Wallet tracking | $$ |

---

## 2. Sentiment Indicators

### What We Track

| Indicator | Source | Range | Update |
|-----------|--------|-------|--------|
| **Crypto Fear & Greed** | Alternative.me | 0-100 | Daily |
| **CNN Fear & Greed** | CNN | 0-100 | Daily |
| **AAII Sentiment** | AAII.com | Bull/Bear % | Weekly |
| **Put/Call Ratio** | CBOE | Ratio | Daily |
| **VIX** | CBOE | Index | Real-time |
| **BTC Funding Rates** | Exchanges | Rate | Real-time |

### Why It Matters

**Sentiment as Contrarian Signal:**

| Reading | Interpretation | Action |
|---------|----------------|--------|
| Extreme Fear (<20) | Capitulation, oversold | Potential buy |
| Fear (20-40) | Pessimism | Accumulation zone |
| Neutral (40-60) | Balanced | Hold |
| Greed (60-80) | Optimism | Caution |
| Extreme Greed (>80) | Euphoria, overbought | Potential sell |

**Historical Accuracy:**

- Extreme Fear readings (<15) have historically preceded 20-50% rallies
- Extreme Greed readings (>80) have historically preceded 15-30% corrections
- NOT timing tools â€” confirmation tools

---

## 3. Alternative.me Crypto Fear & Greed Index API

### ðŸ”´ COMPLETE API DOCUMENTATION (GAP-006)

**Base Endpoint:**
```
GET https://api.alternative.me/fng/
```

**Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `limit` | int | No | Number of results (0 = all) | `limit=30` |
| `format` | string | No | Response format | `format=json` (default) or `format=csv` |
| `date_format` | string | No | Date format style | `us`, `cn`, `kr`, `world` |

**Rate Limits:**
- Approximately 30 requests per minute
- No authentication required (FREE API)
- No API key needed

**Response Schema:**

```json
{
  "name": "Fear and Greed Index",
  "data": [
    {
      "value": "20",
      "value_classification": "Extreme Fear",
      "timestamp": "1706140800",
      "time_until_update": "43200"
    },
    {
      "value": "25",
      "value_classification": "Extreme Fear",
      "timestamp": "1706054400",
      "time_until_update": ""
    }
  ],
  "metadata": {
    "error": null
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `value` | string | Fear & Greed score (0-100) |
| `value_classification` | string | Text label for the score |
| `timestamp` | string | Unix timestamp (seconds) |
| `time_until_update` | string | Seconds until next update (only on latest) |

**Value Classifications:**

| Range | Classification |
|-------|----------------|
| 0-24 | Extreme Fear |
| 25-44 | Fear |
| 45-55 | Neutral |
| 56-75 | Greed |
| 76-100 | Extreme Greed |

**Python Implementation:**

```python
import requests
from datetime import datetime

def get_crypto_fear_greed(limit: int = 30) -> dict:
    """
    Crypto Fear & Greed Index from Alternative.me
    FREE API - No authentication required
    
    Args:
        limit: Number of days to retrieve (0 = all historical data)
    
    Returns:
        dict with current value and historical data
    """
    url = "https://api.alternative.me/fng/"
    params = {
        'limit': limit,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Parse response
    records = []
    for item in data['data']:
        records.append({
            'date': datetime.fromtimestamp(int(item['timestamp'])).strftime('%Y-%m-%d'),
            'fear_greed_index': int(item['value']),
            'fear_greed_label': item['value_classification']
        })
    
    return {
        'current': records[0] if records else None,
        'historical': records
    }

def get_fear_greed_historical(days: int = 365) -> list:
    """
    Get historical Fear & Greed data for CSV export
    
    Returns:
        List of dicts ready for CSV: [{'date': '2024-01-01', 'fear_greed_index': 45, 'fear_greed_label': 'Neutral'}, ...]
    """
    result = get_crypto_fear_greed(limit=days)
    return result['historical']

# Example: Get all historical data
def export_fear_greed_to_csv(output_path: str = 'sentiment_indicators.csv'):
    """
    Export Fear & Greed historical data to CSV
    """
    import pandas as pd
    
    # Get all historical data (limit=0)
    url = "https://api.alternative.me/fng/?limit=0&format=json"
    response = requests.get(url)
    data = response.json()
    
    records = []
    for item in data['data']:
        records.append({
            'date': datetime.fromtimestamp(int(item['timestamp'])).strftime('%Y-%m-%d'),
            'fear_greed_index': int(item['value']),
            'fear_greed_label': item['value_classification']
        })
    
    df = pd.DataFrame(records)
    df = df.sort_values('date')  # Oldest first
    df.to_csv(output_path, index=False)
    
    print(f"Exported {len(df)} records to {output_path}")
    return df
```

**cURL Example:**

```bash
# Get last 30 days
curl "https://api.alternative.me/fng/?limit=30"

# Get all historical data
curl "https://api.alternative.me/fng/?limit=0"

# Get CSV format
curl "https://api.alternative.me/fng/?limit=30&format=csv"
```

**Error Handling:**

```python
def get_fear_greed_safe() -> dict:
    """
    Fear & Greed with error handling
    """
    try:
        response = requests.get(
            "https://api.alternative.me/fng/?limit=1",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('metadata', {}).get('error'):
            return {'error': data['metadata']['error']}
        
        if not data.get('data'):
            return {'error': 'No data returned'}
        
        latest = data['data'][0]
        return {
            'value': int(latest['value']),
            'label': latest['value_classification'],
            'timestamp': datetime.fromtimestamp(int(latest['timestamp'])),
            'error': None
        }
        
    except requests.exceptions.Timeout:
        return {'error': 'API timeout'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}
    except (KeyError, ValueError) as e:
        return {'error': f'Parse error: {str(e)}'}
```

---

## 4. Other Sentiment Collection

### AAII Investor Sentiment

```python
def get_aaii_sentiment():
    """
    AAII Investor Sentiment Survey
    Weekly release (Thursday)
    
    Note: AAII does not have a free API.
    Options:
    1. Manual entry from https://www.aaii.com/sentimentsurvey
    2. Web scraping (check ToS)
    3. Third-party data providers
    """
    # Historical average: 38% Bull, 30% Bear, 32% Neutral
    # Data released every Thursday
    pass

def record_aaii_sentiment(date: str, bullish: float, bearish: float, neutral: float):
    """
    Manual recording of AAII sentiment
    Called weekly after Thursday release
    
    Validation: bullish + bearish + neutral should equal ~100% (Â±1% for rounding)
    """
    assert abs(bullish + bearish + neutral - 100) < 2, "Percentages must sum to ~100%"
    
    record = {
        'date': date,
        'bullish_pct': bullish,
        'bearish_pct': bearish,
        'neutral_pct': neutral
    }
    
    # Append to aaii_sentiment.csv
    return record
```

### Put/Call Ratio

```python
def get_put_call_ratio():
    """
    CBOE Put/Call Ratio
    >1.0 = More puts (bearish sentiment, contrarian bullish)
    <0.8 = More calls (bullish sentiment, contrarian bearish)
    
    Note: Historical daily data requires paid data feed.
    Free sources:
    - CBOE website (current day only)
    - Yahoo Finance (delayed)
    """
    pass
```

### BTC Funding Rates

```python
def get_btc_funding_rates():
    """
    BTC Perpetual Funding Rates
    Positive = Longs paying shorts (bullish positioning)
    Negative = Shorts paying longs (bearish positioning)
    Extreme positive (>0.1%) = Overleveraged longs
    
    Sources (FREE APIs):
    - Binance: https://fapi.binance.com/fapi/v1/fundingRate
    - Bybit: https://api.bybit.com/v2/public/funding/prev-funding-rate
    """
    import requests
    
    # Binance example
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {'symbol': 'BTCUSDT', 'limit': 1}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data:
        return {
            'rate': float(data[0]['fundingRate']),
            'time': data[0]['fundingTime']
        }
    return None
```

---

## 5. Alert Thresholds

| Indicator | Level | Alert | Signal |
|-----------|-------|-------|--------|
| Crypto F&G | <15 | ðŸ”´ Critical | Extreme fear = buy signal |
| Crypto F&G | >85 | ðŸ”´ Critical | Extreme greed = sell signal |
| AAII Bulls | >50% | ðŸŸ  High | Contrarian bearish |
| AAII Bears | >50% | ðŸŸ  High | Contrarian bullish |
| Put/Call | >1.2 | ðŸŸ¡ Medium | Fear elevated |
| BTC Funding | >0.1% | ðŸŸ  High | Overleveraged longs |
| BTC Funding | <-0.05% | ðŸŸ¡ Medium | Shorts crowded |

---

## 6. Current Status

| Item | Status | Notes |
|------|--------|-------|
| Sentiment tracking | ðŸ”´ Not built | CTO Board |
| Fear & Greed API | âœ… Documented | See Section 3 |
| AAII data | ðŸ”´ Not collected | Weekly manual |
| Funding rates | ðŸ”´ Not tracked | Add |

---

## 7. News Monitoring

### Critical Keywords

**Regulatory:**
```python
REGULATORY_KEYWORDS = [
    'SEC', 'CFTC', 'MiCA', 'stablecoin regulation',
    'crypto ban', 'Bitcoin ETF', 'securities', 'enforcement',
    'Gensler', 'custody rule', 'broker-dealer'
]
```

**Central Banks:**
```python
CENTRAL_BANK_KEYWORDS = [
    'Fed rate', 'FOMC', 'ECB rate', 'quantitative easing',
    'quantitative tightening', 'balance sheet', 'Powell',
    'Lagarde', 'dot plot', 'rate cut', 'rate hike'
]
```

**Market Events:**
```python
MARKET_EVENT_KEYWORDS = [
    'Mt. Gox', 'FTX', 'Celsius', 'bankruptcy', 'distribution',
    'hack', 'exploit', 'depeg', 'USDC', 'USDT', 'Tether',
    'liquidation', 'whale', 'Saylor', 'MicroStrategy'
]
```

**Macro:**
```python
MACRO_KEYWORDS = [
    'CPI', 'inflation', 'employment', 'GDP', 'recession',
    'yield curve', 'inversion', 'M2', 'liquidity'
]
```

### Monitoring Strategy

```python
class NewsMonitor:
    """
    Monitor news sources for market-moving events
    """
    
    SOURCES = [
        'https://www.theblock.co/rss',
        'https://www.coindesk.com/rss',
        # Add more RSS feeds
    ]
    
    def scan_headlines(self):
        """
        Scan RSS feeds for keyword matches
        """
        alerts = []
        
        for source in self.SOURCES:
            feed = parse_rss(source)
            
            for item in feed:
                headline = item['title'].lower()
                
                # Check against keyword lists
                for keyword in REGULATORY_KEYWORDS:
                    if keyword.lower() in headline:
                        alerts.append({
                            'type': 'REGULATORY',
                            'headline': item['title'],
                            'source': source,
                            'priority': 'HIGH'
                        })
        
        return alerts
    
    def check_fed_calendar(self):
        """
        Check upcoming Fed events
        """
        # FOMC meeting dates
        # CPI release dates
        # Employment report dates
        pass
```

### Event Calendar

| Event | Frequency | Typical Time | Impact |
|-------|-----------|--------------|--------|
| FOMC Decision | 8x/year | Wed 14:00 ET | ðŸ”´ Critical |
| CPI Release | Monthly | 2nd week, 08:30 ET | ðŸ”´ Critical |
| Employment Report | Monthly | 1st Friday, 08:30 ET | ðŸŸ  High |
| ECB Decision | 6x/year | Thu 14:15 CET | ðŸŸ  High |
| Crypto earnings (COIN, MSTR) | Quarterly | Varies | ðŸŸ¡ Medium |

### Current Status

| Item | Status | Notes |
|------|--------|-------|
| News monitoring | ðŸ”´ Not built | CMO/CTO Board |
| RSS integration | ðŸ”´ Not built | CTO Board |
| Event calendar | ðŸ”´ Not built | Manual for now |
| Keyword alerts | ðŸ”´ Not built | CTO Board |

---

## 8. Social Sentiment (Lower Priority)

### What to Track (Cautiously)

| Platform | Signal | Quality |
|----------|--------|---------|
| Twitter/X | Trending topics | Low (noisy) |
| Reddit (r/bitcoin, r/cryptocurrency) | Sentiment | Low-Medium |
| Discord/Telegram | Project chatter | Very Low |

### Why Lower Priority

- **Lagging:** Social sentiment follows price, doesn't lead
- **Manipulable:** Bots, paid shills, coordinated campaigns
- **Noisy:** High volume, low signal
- **Unreliable:** Contrarian indicator at best

**Recommendation:** Focus on quantitative sentiment (Fear & Greed, AAII, funding rates) over social sentiment.

---

## 9. Noise to Ignore

| Category | Examples | Why Ignore |
|----------|----------|------------|
| **Price Predictions** | "$100K by Friday" | No track record |
| **Influencer Calls** | Random CT personalities | Unreliable |
| **Technical Analysis** | "Head and shoulders forming" | Subjective |
| **Altcoin News** | New token launches | Not relevant to strategies |
| **Social Sentiment** | "Everyone is bullish" | Lagging |
| **Political Polls** | Election predictions | Not actionable |
| **Conspiracy Theories** | "Manipulation" claims | Noise |

---

## File Inventory

### âž• Create New

| File | Contents | Priority |
|------|----------|----------|
| `sentiment_indicators.csv` | Fear & Greed, AAII, Put/Call | ðŸŸ¡ Medium |
| `event_calendar.csv` | FOMC, CPI, ECB dates | ðŸŸ¡ Medium |

---

## CTO Board Implementation

### Priority 1: Sentiment Dashboard

```yaml
service: sentiment_collector
frequency: "0 12 * * *"  # Daily at noon UTC
sources:
  - name: "Alternative.me Fear & Greed"
    endpoint: "https://api.alternative.me/fng/"
    params:
      limit: 1
      format: json
    mapping:
      value: data[0].value
      label: data[0].value_classification
  - name: "CNN F&G"
    method: scrape  # Check ToS
  - name: "AAII"
    method: manual_weekly_input
output: sentiment_indicators.csv
alerts:
  - extreme_fear: F&G < 15
  - extreme_greed: F&G > 85
```

### Priority 2: News Keyword Monitor (Phase 2)

```yaml
service: news_monitor
frequency: "*/30 * * * *"  # Every 30 minutes
sources:
  - theblock.co/rss
  - coindesk.com/rss
keywords:
  - regulatory: [SEC, CFTC, MiCA, ban]
  - central_bank: [Fed, FOMC, ECB, rate]
  - market_event: [hack, exploit, bankruptcy]
output: news_alerts.json
priority_routing:
  regulatory: HIGH
  central_bank: HIGH
  market_event: MEDIUM
```

---

## Adelaide Integration

### Sentiment Section

```markdown
## ðŸ˜° Market Sentiment

**Crypto Fear & Greed:** 32 (Fear)
- 30-day average: 45
- Historical context: Readings below 25 have preceded rallies

**AAII Sentiment:** 28% Bulls, 42% Bears
- More bears than usual â†’ contrarian bullish

**BTC Funding:** +0.02% (neutral)
- Not overleveraged in either direction

**Interpretation:** Fear elevated but not extreme. Market positioning suggests room for upside surprise. Accumulation environment.
```

### Breaking News Alert

```markdown
## ðŸš¨ Breaking: Fed Decision

**Event:** FOMC kept rates unchanged at 5.25%

**Key Points:**
- Dot plot suggests 2 cuts in 2025 (vs 3 expected)
- Powell: "Progress on inflation but not confident enough"

**Market Reaction:**
- S&P 500: -0.8%
- BTC: -2.3%
- 10Y Yield: +8bps to 4.33%

**Adelaide Take:** Slightly hawkish surprise. Short-term headwind but path to cuts remains intact. No change to long-term thesis.
```

---

**Next Document:** [08_ADELAIDE_INTEGRATION.md](./08_ADELAIDE_INTEGRATION.md)
