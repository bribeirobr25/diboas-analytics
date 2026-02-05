# 05 â€” Institutional Flows

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 3.0  
**Last Updated:** January 24, 2026  
**Owner:** Rakia (Investment Analyst) + CTO Board
**Change Log:**
- v3: Added `automation_status` flags; marked 13F and corporate holdings as MANUAL_ONLY (GAP-008 fix)

---

## Overview

Institutional flow data tracks where large capital is moving:
- **ETF Flows** â€” BTC, ETH, Gold ETF inflows/outflows
- **13F Holdings** â€” Quarterly filings from large investors
- **Corporate Treasury** â€” Public company crypto holdings
- **Gold Flows** â€” Central bank and ETF gold buying

**Key Insight:** Institutions move markets. Following institutional flows provides leading indicators.

---

## âš ï¸ Automation Status Legend

Each data source is marked with its automation status:

| Status | Meaning | CTO Board Action |
|--------|---------|------------------|
| ðŸŸ¢ `AUTOMATABLE` | Can be automated with APIs | Build collection job |
| ðŸŸ¡ `SEMI_AUTO` | Partially automatable, needs review | Build with human check |
| ðŸ”´ `MANUAL_ONLY` | Requires human research | Add to analyst task list |

---

## 1. ETF Flows (BTC & ETH)

### Automation Status: ðŸŸ¢ AUTOMATABLE

ETF flow data can be collected automatically from aggregator sites.

### What We Track

**Bitcoin ETFs:**

| ETF | Ticker | Issuer | Why Track | Automation Status |
|-----|--------|--------|-----------|-------------------|
| iShares Bitcoin Trust | IBIT | BlackRock | Largest, most liquid | ðŸŸ¢ AUTOMATABLE |
| Fidelity Wise Origin | FBTC | Fidelity | Second largest | ðŸŸ¢ AUTOMATABLE |
| Grayscale Bitcoin Trust | GBTC | Grayscale | Oldest, outflows matter | ðŸŸ¢ AUTOMATABLE |
| ARK 21Shares | ARKB | ARK/21Shares | Cathie Wood sentiment | ðŸŸ¢ AUTOMATABLE |
| Bitwise | BITB | Bitwise | Crypto-native | ðŸŸ¢ AUTOMATABLE |

**Ethereum ETFs:**

| ETF | Ticker | Issuer | Automation Status |
|-----|--------|--------|-------------------|
| iShares Ethereum Trust | ETHA | BlackRock | ðŸŸ¢ AUTOMATABLE |
| Fidelity Ethereum Fund | FETH | Fidelity | ðŸŸ¢ AUTOMATABLE |
| Grayscale Ethereum Trust | ETHE | Grayscale | ðŸŸ¢ AUTOMATABLE |

### Why It Matters

| Flow Direction | Interpretation |
|----------------|----------------|
| **Net inflows >$500M/day** | Strong institutional buying |
| **Sustained inflows (5+ days)** | Institutional accumulation |
| **Net outflows >$500M/day** | Institutional selling |
| **GBTC outflows specifically** | Legacy holders exiting |

**Impact:** ETF flows are the primary driver of BTC price since Jan 2024 launch.

### How to Check

**Frequency:** Daily

**Data Sources (FREE):**

| Source | URL | Data | Automation Status |
|--------|-----|------|-------------------|
| Farside Investors | farside.co.uk/btc | Daily ETF flows | ðŸŸ¢ AUTOMATABLE |
| SoSoValue | sosovalue.xyz | ETF dashboard | ðŸŸ¢ AUTOMATABLE |
| The Block | theblock.co/data | ETF data | ðŸŸ¢ AUTOMATABLE |
| BitMEX Research | Twitter @BitMEXResearch | Daily summary | ðŸŸ¡ SEMI_AUTO |

**Collection:**

```python
# Farside Investors scraping (check ToS)
# Automation Status: AUTOMATABLE
import requests
from bs4 import BeautifulSoup

def get_btc_etf_flows():
    """
    Scrape BTC ETF flows from Farside
    Note: Check website ToS before automated scraping
    """
    url = "https://farside.co.uk/btc/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse table data
    # Return daily flows by ETF
    
    return flows

# Alternative: Manual daily collection
def record_etf_flows(date, flows_dict):
    """
    Manual recording of ETF flows
    Called daily by analyst
    """
    record = {
        'date': date,
        'ibit': flows_dict.get('IBIT', 0),
        'fbtc': flows_dict.get('FBTC', 0),
        'gbtc': flows_dict.get('GBTC', 0),
        'arkb': flows_dict.get('ARKB', 0),
        'total': sum(flows_dict.values())
    }
    
    # Append to CSV
    return record
```

**Alert Thresholds:**

| Event | Threshold | Alert Level |
|-------|-----------|-------------|
| Daily inflow | >$500M | ðŸŸ  High (bullish) |
| Daily outflow | >$500M | ðŸŸ  High (bearish) |
| Weekly inflow | >$2B | ðŸ”´ Critical (strong demand) |
| Weekly outflow | >$2B | ðŸ”´ Critical (heavy selling) |
| GBTC outflow | >$300M/day | ðŸŸ¡ Medium (legacy exit) |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| ETF flow tracking | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |
| Data source integration | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | Farside/SoSoValue |
| Alert system | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |

---

## 2. 13F Institutional Holdings

### âš ï¸ Automation Status: ðŸ”´ MANUAL_ONLY

**Why Manual:** While SEC EDGAR provides raw XML data, parsing 13F filings correctly requires:
- Handling multiple filing formats
- Identifying crypto-related securities among thousands of holdings
- Interpreting position changes in context
- Tracking CIK changes and fund reorganizations

**Recommendation:** Analyst reviews quarterly filings manually. CTO Board can build alerting for new filings only.

### What We Track

**Tier 1 (Always Track):**

| Institution | CIK | AUM | Why Track | Automation Status |
|-------------|-----|-----|-----------|-------------------|
| BlackRock | 0001364742 | $10T+ | Largest asset manager | ðŸ”´ MANUAL_ONLY |
| Vanguard | 0000102909 | $8T+ | Index giant | ðŸ”´ MANUAL_ONLY |
| Fidelity | 0000315066 | $4T+ | BTC ETF issuer | ðŸ”´ MANUAL_ONLY |
| Berkshire Hathaway | 0001067983 | $900B+ | Buffett indicator | ðŸ”´ MANUAL_ONLY |
| Bridgewater | 0001350694 | $150B+ | Macro king | ðŸ”´ MANUAL_ONLY |

**Tier 2 (High Interest):**

| Institution | CIK | Focus | Automation Status |
|-------------|-----|-------|-------------------|
| ARK Invest | 0001569391 | Disruptive tech, crypto | ðŸ”´ MANUAL_ONLY |
| Pershing Square | 0001336528 | Activist, macro | ðŸ”´ MANUAL_ONLY |
| Soros Fund | 0001029160 | Macro, crypto exposure | ðŸ”´ MANUAL_ONLY |
| Point72 | 0001603466 | Quant, diversified | ðŸ”´ MANUAL_ONLY |
| Millennium | 0001015780 | Multi-strategy | ðŸ”´ MANUAL_ONLY |

**Tier 3 (Regional Giants):**

| Institution | Region | Why Track | Automation Status |
|-------------|--------|-----------|-------------------|
| ItaÃºsa | Brazil | Brazil smart money | ðŸ”´ MANUAL_ONLY |
| 3G Capital | Brazil/Global | Lemann empire | ðŸ”´ MANUAL_ONLY |
| Softbank | Japan | Tech/crypto exposure | ðŸ”´ MANUAL_ONLY |
| GIC (Singapore) | Asia | Sovereign wealth | ðŸ”´ MANUAL_ONLY |

### Why It Matters

| Signal | Interpretation |
|--------|----------------|
| **New crypto position** | Institutional adoption |
| **Position increase** | Conviction growing |
| **Position decrease** | Taking profits or reducing risk |
| **Complete exit** | Bearish signal |
| **Multiple funds same stock** | Crowded trade |

### How to Check

**Frequency:** Quarterly (13F due 45 days after quarter end)

**Filing Dates:**

| Quarter End | 13F Deadline |
|-------------|--------------|
| March 31 | May 15 |
| June 30 | August 14 |
| September 30 | November 14 |
| December 31 | February 14 |

**Data Source:** SEC EDGAR (FREE)

```python
import requests

def get_13f_holdings(cik: str) -> dict:
    """
    Get latest 13F holdings from SEC EDGAR
    
    âš ï¸ Automation Status: SEMI_AUTO
    - Can fetch raw filings automatically
    - Parsing requires manual review for accuracy
    """
    # Pad CIK to 10 digits
    cik_padded = cik.zfill(10)
    
    # Get company filings
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    headers = {'User-Agent': 'diBoaS Research team@diboas.com'}
    
    response = requests.get(url, headers=headers)
    filings = response.json()
    
    # Find latest 13F-HR
    recent_filings = filings['filings']['recent']
    for i, form in enumerate(recent_filings['form']):
        if form == '13F-HR':
            accession = recent_filings['accessionNumber'][i]
            filing_date = recent_filings['filingDate'][i]
            
            # Get the actual holdings from XML
            # âš ï¸ MANUAL REVIEW REQUIRED - parsing is complex
            
            return {
                'cik': cik,
                'filing_date': filing_date,
                'holdings': holdings
            }
    
    return None

def track_crypto_exposure():
    """
    Track crypto-related holdings across institutions
    
    âš ï¸ Automation Status: MANUAL_ONLY
    - Requires analyst judgment on what counts as "crypto exposure"
    """
    crypto_securities = [
        'IBIT',   # BlackRock BTC ETF
        'FBTC',   # Fidelity BTC ETF
        'GBTC',   # Grayscale BTC
        'COIN',   # Coinbase
        'MSTR',   # MicroStrategy
        'MARA',   # Marathon Digital
        'RIOT',   # Riot Platforms
    ]
    
    # Check each institution's holdings for these securities
    pass
```

**What to Track:**

| Position | Alert Level | Interpretation |
|----------|-------------|----------------|
| Berkshire enters crypto | ðŸ”´ Critical | Major validation |
| BlackRock increases IBIT | ðŸŸ  High | Institutional demand |
| ARK sells COIN/GBTC | ðŸŸ¡ Medium | Cathie rotating |
| Bridgewater adds gold | ðŸŸ¡ Medium | Macro hedging |
| Multiple funds exit same | ðŸŸ  High | Crowded trade unwinding |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| 13F tracking | ðŸ”´ Not built | ðŸ”´ MANUAL_ONLY | Quarterly task |
| SEC EDGAR integration | ðŸ”´ Not built | ðŸŸ¡ SEMI_AUTO | Alert on new filings only |
| Crypto exposure alerts | ðŸ”´ Not built | ðŸ”´ MANUAL_ONLY | Analyst review |

### Research Task

| Task | Description | Output | Automation Status |
|------|-------------|--------|-------------------|
| **R11** | Review 13F filings for top 20 institutions quarterly | `institutional_13f.csv` | ðŸ”´ MANUAL_ONLY |

---

## 3. Corporate Treasury Holdings

### âš ï¸ Automation Status: ðŸ”´ MANUAL_ONLY

**Why Manual:** Corporate BTC holdings require:
- Monitoring 8-K filings for purchase announcements
- Reading 10-Q/10-K for balance sheet updates
- Verifying against company press releases
- Tracking acquisitions and changes in methodology

**Recommendation:** Analyst updates quarterly; BitcoinTreasuries.net provides baseline.

### What We Track

Public companies holding BTC/crypto on balance sheet.

**Top Holdings:**

| Company | Ticker | BTC Holdings | Est. Value | Automation Status |
|---------|--------|--------------|------------|-------------------|
| Strategy (MicroStrategy) | MSTR | 660,000+ | $66B+ | ðŸ”´ MANUAL_ONLY |
| MARA Holdings | MARA | 46,000+ | $4.6B | ðŸ”´ MANUAL_ONLY |
| Riot Platforms | RIOT | 15,000+ | $1.5B | ðŸ”´ MANUAL_ONLY |
| Coinbase | COIN | 10,000+ | $1B | ðŸ”´ MANUAL_ONLY |
| Tesla | TSLA | 10,000+ | $1B | ðŸ”´ MANUAL_ONLY |
| Block (Square) | SQ | 8,000+ | $800M | ðŸ”´ MANUAL_ONLY |
| Galaxy Digital | GLXY | 8,000+ | $800M | ðŸ”´ MANUAL_ONLY |

### Why It Matters

| Event | Interpretation |
|-------|----------------|
| **MSTR buys** | Saylor accumulating, bullish signal |
| **Public company sells BTC** | Bearish, loss of conviction |
| **New company announces BTC** | Adoption expanding |
| **Miner selling pressure** | MARA/RIOT selling to fund operations |

### How to Check

**Frequency:** Event-driven (8-K filings), quarterly (10-Q)

**Data Sources:**

| Source | Data | Access | Automation Status |
|--------|------|--------|-------------------|
| BitcoinTreasuries.net | Comprehensive list | FREE | ðŸŸ¡ SEMI_AUTO |
| SEC EDGAR | Official filings | FREE | ðŸ”´ MANUAL_ONLY |
| Company press releases | Announcements | FREE | ðŸ”´ MANUAL_ONLY |

```python
def get_corporate_btc_holdings():
    """
    Scrape BitcoinTreasuries.net for holdings
    
    âš ï¸ Automation Status: SEMI_AUTO
    - Can scrape baseline data
    - Should verify against official filings
    """
    url = "https://bitcointreasuries.net/"
    # Parse table
    # Return structured data
    pass

def monitor_mstr_filings():
    """
    Monitor MSTR 8-K filings for BTC purchases
    
    âš ï¸ Automation Status: SEMI_AUTO
    - Can alert on new 8-K filings
    - Requires manual parsing for BTC amounts
    """
    cik = "0001050446"  # MicroStrategy CIK
    # Check for new 8-K filings
    # Alert on BTC purchase announcements
    pass
```

**Alert Triggers:**

| Event | Alert Level | Automation Status |
|-------|-------------|-------------------|
| MSTR buys >10K BTC | ðŸ”´ Critical | ðŸ”´ MANUAL_ONLY |
| Public company announces BTC treasury | ðŸŸ  High | ðŸ”´ MANUAL_ONLY |
| Company sells BTC | ðŸŸ  High | ðŸ”´ MANUAL_ONLY |
| Miner sells >1K BTC | ðŸŸ¡ Medium | ðŸ”´ MANUAL_ONLY |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `corporate_btc_holdings.csv` | âœ… Good (30 records) | ðŸ”´ MANUAL_ONLY | Keep |
| Automated updates | ðŸ”´ Not built | ðŸŸ¡ SEMI_AUTO | BitcoinTreasuries scrape |
| Filing monitoring | ðŸ”´ Not built | ðŸŸ¡ SEMI_AUTO | Alert on 8-K only |

---

## 4. Gold Flows

### Automation Status: ðŸŸ¡ SEMI_AUTO

### What We Track

| Category | What | Why | Automation Status |
|----------|------|-----|-------------------|
| **Gold ETF Flows** | GLD, IAU inflows/outflows | Institutional gold demand | ðŸŸ¢ AUTOMATABLE |
| **Central Bank Buying** | Sovereign gold purchases | Dedollarization signal | ðŸ”´ MANUAL_ONLY |
| **Gold vs BTC Ratio** | GC=F / BTC-USD | "Digital gold" narrative | ðŸŸ¢ AUTOMATABLE |

### Why It Matters

| Signal | Interpretation |
|--------|----------------|
| **Heavy gold ETF inflows** | Flight to safety, risk-off |
| **Central banks buying gold** | Dedollarization, currency concerns |
| **Gold/BTC ratio falling** | BTC outperforming, risk-on |
| **Gold/BTC ratio rising** | Gold outperforming, risk-off |

### How to Check

**Frequency:** Weekly for ETFs, Monthly for CB buying

**Data Sources:**

| Source | Data | Access | Automation Status |
|--------|------|--------|-------------------|
| ETF.com | GLD/IAU flows | FREE | ðŸŸ¢ AUTOMATABLE |
| World Gold Council | CB buying data | FREE | ðŸ”´ MANUAL_ONLY |
| Yahoo Finance | GLD/IAU prices | FREE | ðŸŸ¢ AUTOMATABLE |

```python
def calculate_gold_btc_ratio():
    """
    Gold/BTC ratio for regime detection
    
    Automation Status: AUTOMATABLE
    """
    gold_price = yf.Ticker('GC=F').history(period='1d')['Close'].iloc[-1]
    btc_price = yf.Ticker('BTC-USD').history(period='1d')['Close'].iloc[-1]
    
    ratio = gold_price / btc_price
    
    # Historical context
    # Ratio ~0.02-0.03 during 2021 bull
    # Ratio ~0.04-0.05 during 2022 bear
    
    return {
        'ratio': ratio,
        'regime': 'RISK_ON' if ratio < 0.025 else 'RISK_OFF'
    }
```

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| Gold price | âœ… Have | ðŸŸ¢ AUTOMATABLE | In tradfi_benchmark |
| Gold ETF flows | ðŸ”´ Missing | ðŸŸ¢ AUTOMATABLE | Add |
| CB gold buying | ðŸ”´ Missing | ðŸ”´ MANUAL_ONLY | Nice to have |
| Gold/BTC ratio | ðŸ”´ Not calculated | ðŸŸ¢ AUTOMATABLE | Add to rotation |

### Research Task

| Task | Description | Output | Automation Status |
|------|-------------|--------|-------------------|
| **R9** | Gold ETF flows, CB buying data | `gold_flows.csv` | ðŸŸ¡ SEMI_AUTO |

---

## 5. Notable Investors to Track

### Methodology

Don't invite them â€” **track what they DO** via public data.

| Investor | Track Via | Signal Value | Automation Status |
|----------|-----------|--------------|-------------------|
| **Warren Buffett** | Berkshire 13F, annual letter, cash levels | Risk appetite, value | ðŸ”´ MANUAL_ONLY |
| **Stanley Druckenmiller** | 13F, rare interviews | Macro thesis | ðŸ”´ MANUAL_ONLY |
| **Michael Saylor** | MSTR filings, Twitter | BTC conviction | ðŸŸ¡ SEMI_AUTO |
| **Cathie Wood** | ARK daily trades (public) | Disruptive tech sentiment | ðŸŸ¢ AUTOMATABLE |
| **Ray Dalio** | Bridgewater 13F, LinkedIn | Macro allocation | ðŸ”´ MANUAL_ONLY |
| **Howard Marks** | Oaktree memos | Credit cycles | ðŸ”´ MANUAL_ONLY |
| **Larry Fink** | BlackRock 13F, interviews | Institutional adoption | ðŸ”´ MANUAL_ONLY |

### Special: ARK Daily Trades (AUTOMATABLE)

ARK publishes daily trades (FREE):

```python
def get_ark_daily_trades():
    """
    ARK publishes daily trade data
    URL: https://ark-funds.com/trade-notifications
    
    Automation Status: AUTOMATABLE
    """
    # Parse daily trade notifications
    # Track COIN, GBTC, BITO positions
    pass
```

### Special: Berkshire Cash Levels (MANUAL)

```python
def get_berkshire_cash():
    """
    Berkshire's cash pile is a sentiment indicator
    High cash = Buffett cautious = risk-off
    Deploying cash = Buffett bullish = risk-on
    
    Automation Status: MANUAL_ONLY
    Requires reading 10-Q filings
    """
    # From latest 10-Q
    # Track cash & equivalents, short-term treasuries
    pass
```

---

## File Inventory

### âœ… Keep As-Is

| File | Records | Automation Status | Notes |
|------|---------|-------------------|-------|
| `corporate_btc_holdings.csv` | 30 | ðŸ”´ MANUAL_ONLY | Keep, update quarterly |

### âž• Create New

| File | Contents | Priority | Automation Status |
|------|----------|----------|-------------------|
| `etf_flows.csv` | Daily BTC/ETH ETF flows | ðŸŸ  High | ðŸŸ¢ AUTOMATABLE |
| `institutional_13f.csv` | Quarterly holdings | ðŸŸ  High | ðŸ”´ MANUAL_ONLY |
| `gold_flows.csv` | Gold ETF flows, CB buying | ðŸŸ¡ Medium | ðŸŸ¡ SEMI_AUTO |
| `ark_daily_trades.csv` | ARK trade notifications | ðŸŸ¡ Medium | ðŸŸ¢ AUTOMATABLE |

---

## CTO Board Implementation

### Priority 1: ETF Flow Tracker (AUTOMATABLE)

```yaml
service: etf_flow_tracker
frequency: "0 22 * * 1-5"  # Daily after US market close
sources:
  - farside.co.uk/btc
  - sosovalue.xyz
data_points:
  - ibit_flow
  - fbtc_flow
  - gbtc_flow
  - total_btc_flow
  - total_eth_flow
output: etf_flows.csv
alerts:
  - daily_inflow_large: >$500M
  - daily_outflow_large: <-$500M
  - weekly_trend: 5+ days same direction
automation_status: AUTOMATABLE
```

### Priority 2: ARK Trades Tracker (AUTOMATABLE)

```yaml
service: ark_trades_tracker
frequency: "0 23 * * 1-5"  # Daily after ARK publishes
source: ark-funds.com/trade-notifications
focus_tickers: [COIN, GBTC, BITO, MSTR]
output: ark_daily_trades.csv
alerts:
  - large_buy: >$10M
  - large_sell: >$10M
  - position_exit: Full exit from any crypto-related
automation_status: AUTOMATABLE
```

### Priority 3: 13F Filing Alert (SEMI_AUTO)

```yaml
service: 13f_filing_alert
frequency: "0 */4 * * *"  # Every 4 hours during filing seasons
source: SEC EDGAR
institutions:
  - BlackRock: "0001364742"
  - Berkshire: "0001067983"
  - Bridgewater: "0001350694"
  - ARK: "0001569391"
action: Alert analyst when new 13F filed
output: 13f_filing_alerts.json
automation_status: SEMI_AUTO
note: "Parsing and analysis is MANUAL_ONLY"
```

### Manual Task List (Analyst)

```yaml
manual_tasks:
  quarterly:
    - name: 13F Analysis
      timing: Feb 15, May 15, Aug 14, Nov 14 (+1 week)
      institutions: Top 20 (see Tier 1-3 lists)
      output: institutional_13f.csv
      
    - name: Corporate Holdings Update
      timing: After quarterly earnings
      sources: [10-Q, 8-K, BitcoinTreasuries.net]
      output: corporate_btc_holdings.csv
      
  monthly:
    - name: World Gold Council Data
      timing: 1st week of month
      source: gold.org/goldhub
      output: Update gold_flows.csv
      
  event_driven:
    - name: MSTR Purchase Verification
      trigger: 8-K filing or press release
      action: Verify BTC amount, update holdings
```

---

## Adelaide Integration

### ETF Flow Section (Daily)

```markdown
## ðŸ“Š Institutional Flows

**BTC ETF Flows Today:**
- IBIT: +$245M
- FBTC: +$89M
- GBTC: -$42M
- **Total: +$312M** (5th consecutive inflow day)

**Interpretation:** Sustained institutional buying. Accumulation pattern continues.
```

### 13F Summary (Quarterly)

```markdown
## ðŸ›ï¸ Q4 Institutional Update

**Notable Changes:**
- BlackRock: IBIT position +15% to 520M shares
- Berkshire: Cash at $168B (record high â€” cautious)
- ARK: Reduced COIN position by 8%
- Bridgewater: Added gold miners, reduced tech

**Crypto Exposure Trend:** Increasing among asset managers, flat/declining among macro funds.
```

---

## Automation Summary by Data Type

| Data Type | Automation Status | Frequency | Notes |
|-----------|-------------------|-----------|-------|
| **ETF Flows** | ðŸŸ¢ AUTOMATABLE | Daily | Build collector |
| **13F Holdings** | ðŸ”´ MANUAL_ONLY | Quarterly | Analyst task |
| **Corporate Holdings** | ðŸ”´ MANUAL_ONLY | Quarterly | Analyst task |
| **ARK Trades** | ðŸŸ¢ AUTOMATABLE | Daily | Build collector |
| **Gold ETF Flows** | ðŸŸ¢ AUTOMATABLE | Weekly | Build collector |
| **CB Gold Buying** | ðŸ”´ MANUAL_ONLY | Monthly | World Gold Council |
| **Notable Investor Tracking** | ðŸ”´ MANUAL_ONLY | Quarterly | 13F + public statements |

---

**Next Document:** [06_CAPITAL_ROTATION.md](./06_CAPITAL_ROTATION.md)
