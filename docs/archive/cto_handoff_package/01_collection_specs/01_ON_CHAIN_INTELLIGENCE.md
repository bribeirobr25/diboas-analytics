# 01 â€” On-Chain Intelligence

**Parent:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)  
**Version:** 3.0  
**Last Updated:** January 24, 2026  
**Owner:** Rakia (Investment Analyst) + CTO Board
**Change Log:**
- v3: Added `automation_status` flags to identify manual-only data sources (GAP-008 fix)

---

## Overview

On-chain intelligence monitors blockchain activity for:
- **Liquidation Risk** â€” Estate wallets, government seizures
- **Market Maker Activity** â€” Accumulation/distribution patterns
- **Protocol Health** â€” Treasury movements, governance
- **Smart Money Signals** â€” Early depositors, MEV operators

**Unique Edge:** Estate wallet tracking is diBoaS's competitive moat â€” no other consumer platform does this.

---

## âš ï¸ Automation Status Legend

Each data source is marked with its automation status:

| Status | Meaning | CTO Board Action |
|--------|---------|------------------|
| ðŸŸ¢ `AUTOMATABLE` | Can be automated with APIs | Build collection job |
| ðŸŸ¡ `SEMI_AUTO` | Partially automatable, needs review | Build with human check |
| ðŸ”´ `MANUAL_ONLY` | Requires human research | Add to analyst task list |

---

## 1. Estate Wallet Tracking

### What We Track

Bankruptcy estates, government seizures, and liquidation trustees that hold significant crypto and may distribute/sell.

| Entity | Est. Holdings | Status | Risk Level | Automation Status |
|--------|---------------|--------|------------|-------------------|
| Mt. Gox Trustee | ~47,000 BTC (~$4.7B) | Distribution ongoing | ðŸ”´ Critical | ðŸŸ¢ AUTOMATABLE |
| FTX Estate | $5-7B mixed assets | Liquidating | ðŸ”´ Critical | ðŸŸ¢ AUTOMATABLE |
| Genesis (DCG) | $1-2B | Bankruptcy | ðŸ”´ Critical | ðŸŸ¢ AUTOMATABLE |
| Celsius Estate | $2-3B | Distributed 2024 | ðŸŸ¢ Complete | ðŸŸ¢ AUTOMATABLE |
| BlockFi Estate | $500M+ | Liquidating | ðŸŸ  High | ðŸŸ¢ AUTOMATABLE |
| Voyager Estate | $200M+ | Distributed | ðŸŸ¢ Complete | ðŸŸ¢ AUTOMATABLE |
| 3AC Liquidation | Ongoing recovery | Active | ðŸŸ¡ Medium | ðŸŸ¢ AUTOMATABLE |
| UK Government | ~61,000 BTC (~$6.1B) | Seized, timing unknown | ðŸ”´ Critical | ðŸ”´ MANUAL_ONLY |
| US DOJ Seized | Various | Multiple cases | ðŸŸ  High | ðŸ”´ MANUAL_ONLY |
| German Govt (Saxony) | Sold July 2024 | Complete | âœ… Closed | âœ… No tracking needed |

**Automation Notes:**
- ðŸŸ¢ Estate wallets with known addresses can be monitored via blockchain APIs
- ðŸ”´ Government seizures require manual research (PACER, court filings, press releases)

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Supply Shock** | Large distributions = selling pressure |
| **Price Impact** | Mt. Gox 2014 distribution crashed BTC 50%+ |
| **Predictability** | Court dates known in advance |
| **Unique Signal** | No other consumer platform tracks this |

### How to Check

**Frequency:** Every 15 minutes for active estates

**Alert Thresholds:**

| Movement | Alert Level | Action |
|----------|-------------|--------|
| ANY outflow | ðŸ”´ Critical | Immediate Adelaide alert |
| >$10M movement | ðŸ”´ Critical | Push notification |
| Court filing update | ðŸŸ  High | Same-day digest |
| New wallet labeled | ðŸŸ¡ Medium | Add to tracking |

**Data Collection:**

```python
class EstateWalletMonitor:
    """
    Monitor bankruptcy estate wallets for any movement.
    
    Automation Status: AUTOMATABLE for wallet monitoring
    Manual Required: Court schedule updates
    """
    
    ESTATES = {
        'mt_gox': {
            'wallets': ['1234...', '5678...'],  # From court docs
            'chain': 'bitcoin',
            'threshold': 0.01,  # 1% = any movement
            'priority': 'critical',
            'automation_status': 'AUTOMATABLE'
        },
        'ftx': {
            'wallets': ['0x123...', '0x456...'],
            'chain': 'ethereum',
            'threshold': 0.01,
            'priority': 'critical',
            'automation_status': 'AUTOMATABLE'
        },
        'uk_government': {
            'wallets': [],  # Unknown - requires manual research
            'chain': 'bitcoin',
            'priority': 'critical',
            'automation_status': 'MANUAL_ONLY',
            'manual_source': 'UK court filings, press releases'
        },
        'us_doj': {
            'wallets': [],  # Multiple cases, requires PACER research
            'chain': 'multi',
            'priority': 'high',
            'automation_status': 'MANUAL_ONLY',
            'manual_source': 'PACER, DOJ press releases'
        }
    }
    
    def check_wallet(self, address: str, chain: str) -> dict:
        """Check wallet balance via free APIs"""
        if chain == 'bitcoin':
            # Blockchain.com API (FREE)
            url = f"https://blockchain.info/rawaddr/{address}"
        elif chain == 'ethereum':
            # Etherscan API (FREE with key)
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}"
        
        # Return balance + recent transactions
        
    def generate_alert(self, estate: str, movement: dict) -> dict:
        return {
            'type': 'ESTATE_MOVEMENT',
            'priority': 'CRITICAL',
            'entity': estate,
            'amount_usd': movement['amount'],
            'direction': 'OUTFLOW',
            'destination': movement.get('to_address', 'Unknown'),
            'recommended_action': 'Monitor exchange deposits next 24-48h',
            'historical_context': self.get_historical_impact(estate)
        }
```

**Sources (FREE):**

| Source | Data | URL | Automation Status |
|--------|------|-----|-------------------|
| Blockchain.com | BTC balances | blockchain.info/rawaddr/{addr} | ðŸŸ¢ AUTOMATABLE |
| Etherscan | ETH balances | api.etherscan.io | ðŸŸ¢ AUTOMATABLE |
| Arkham Intelligence | Labeled wallets | intel.arkm.com (free tier) | ðŸŸ¢ AUTOMATABLE |
| PACER | Court filings | pacer.uscourts.gov | ðŸ”´ MANUAL_ONLY |
| UK Courts | UK filings | courtserve.net | ðŸ”´ MANUAL_ONLY |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `estate_wallet_tracker.csv` | âœ… Good (51 records) | ðŸŸ¢ AUTOMATABLE | Wallet monitoring |
| Court schedule tracking | ðŸ”´ Not built | ðŸ”´ MANUAL_ONLY | Research task R3 |
| Automated monitoring | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board priority |
| Alert system | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board priority |

### Research Tasks

| Task | Description | Output | Automation Status |
|------|-------------|--------|-------------------|
| **R3** | Document all court case numbers, hearing dates, distribution timelines | `estate_court_schedule.csv` | ðŸ”´ MANUAL_ONLY |

---

## 2. Market Maker Monitoring

### What We Track

Major crypto market makers and their wallet activity for accumulation/distribution signals.

**Tier 1 (Always Track):**

| Firm | Region | Chains | Known Wallets | Automation Status |
|------|--------|--------|---------------|-------------------|
| Wintermute | EU | ETH, Arbitrum, Solana | 5+ verified | ðŸŸ¢ AUTOMATABLE |
| Jump Trading | US | Multi-chain | 3+ verified | ðŸŸ¢ AUTOMATABLE |
| Cumberland (DRW) | US | ETH, BTC | 2+ verified | ðŸŸ¢ AUTOMATABLE |
| GSR | Global | Multi-chain | 3+ verified | ðŸŸ¢ AUTOMATABLE |
| Amber Group | Asia | Multi-chain | 2+ verified | ðŸŸ¢ AUTOMATABLE |

**Tier 2-4:** See `market_maker_wallet_tracker.csv` for full list (35 entries)

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Directional Signal** | MMs accumulating = bullish |
| **Liquidity Indicator** | MM activity = market health |
| **Size Matters** | $50M+ moves are meaningful |
| **Pattern Recognition** | Distribution before dumps |

### How to Check

**Frequency:** Daily balance check, hourly for Tier 1

**Alert Thresholds:**

| Change | Timeframe | Alert Level |
|--------|-----------|-------------|
| >$50M accumulation | 7 days | ðŸŸ  High (bullish) |
| >$50M distribution | 7 days | ðŸŸ  High (bearish) |
| >$100M single move | 24 hours | ðŸ”´ Critical |
| New token >$10M | Any | ðŸŸ¡ Medium |

**Behavior Classification:**

```python
def classify_mm_behavior(wallet_history: list) -> str:
    """
    Classify market maker behavior over 7-day window
    
    Automation Status: AUTOMATABLE
    """
    net_flow = sum([tx['amount'] for tx in wallet_history])
    
    if net_flow > 10_000_000:  # $10M+ net inflow
        return 'ACCUMULATING'
    elif net_flow < -10_000_000:  # $10M+ net outflow
        return 'DISTRIBUTING'
    else:
        return 'NEUTRAL'
```

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `market_maker_wallet_tracker.csv` | âœ… Good (35 records, 27 real) | ðŸŸ¢ AUTOMATABLE | Keep as-is |
| Automated monitoring | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |
| Behavior classification | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |
| TradFi MM placeholders | âœ… Good (8 placeholders) | ðŸ”´ MANUAL_ONLY | Research quarterly |

---

## 3. Protocol Treasury Tracking

### What We Track

DeFi protocol treasuries for health monitoring and risk assessment.

**Priority Protocols (diBoaS Strategy Relevant):**

| Protocol | diBoaS Strategies | Treasury Size | Why Track | Automation Status |
|----------|-------------------|---------------|-----------|-------------------|
| Sky/Maker | 1-5, 7-9 | $1.5B+ | Core stablecoin | ðŸŸ¢ AUTOMATABLE |
| Aave | 4-6 | $500M+ | Lending protocol | ðŸŸ¢ AUTOMATABLE |
| Compound | 4-6 | $400M+ | Lending protocol | ðŸŸ¢ AUTOMATABLE |
| Lido | 7 | $200M+ | LST backing | ðŸŸ¢ AUTOMATABLE |
| Jito | 7, 9 | $200M+ | Solana LST | ðŸŸ¢ AUTOMATABLE |
| Jupiter | 9-10 | $500M+ | Solana DeFi | ðŸŸ¢ AUTOMATABLE |
| Arbitrum DAO | Multi | $3B+ | L2 ecosystem | ðŸŸ¢ AUTOMATABLE |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Protocol Health** | Shrinking treasury = risk |
| **Token Pressure** | Treasury sales = selling pressure |
| **Diversification** | Treasury into stables = defensive |
| **Grant Activity** | Expansion = ecosystem growth |

### How to Check

**Frequency:** Daily via DeFiLlama API

**Automation Status:** ðŸŸ¢ AUTOMATABLE â€” DeFiLlama provides free API

**Alert Thresholds:**

| Change | Alert Level | Interpretation |
|--------|-------------|----------------|
| Treasury drops >10% | ðŸ”´ Critical | Review diBoaS exposure |
| Large token sale | ðŸŸ  High | Selling pressure |
| Diversification to stables | ðŸŸ¡ Medium | Generally positive |
| Grant program expansion | ðŸŸ¢ Low | Ecosystem growth |

**Data Collection:**

```python
import requests

def get_protocol_treasuries():
    """
    DeFiLlama Treasury API (FREE)
    
    Automation Status: AUTOMATABLE
    """
    response = requests.get("https://api.llama.fi/treasuries")
    treasuries = response.json()
    
    # Filter to diBoaS-relevant protocols
    relevant = [
        t for t in treasuries 
        if t['name'] in DIBOAS_PROTOCOLS
    ]
    
    return relevant

def monitor_treasury_changes():
    """Daily treasury check"""
    for protocol in get_protocol_treasuries():
        current = protocol['tvl']
        previous = get_previous_value(protocol['name'])
        
        change_pct = (current - previous) / previous
        
        if abs(change_pct) > 0.05:  # 5% change
            generate_alert(protocol, change_pct)
```

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `protocol_treasury_tracker.csv` | âœ… Good (35 records) | ðŸŸ¢ AUTOMATABLE | Keep as-is |
| Automated API collection | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |
| Alert thresholds | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |

---

## 4. Whale Wallet Monitoring

### What We Track

Known large holders (whales) for accumulation/distribution signals.

**Categories:**

| Category | Count | Purpose | Automation Status |
|----------|-------|---------|-------------------|
| Exchange whales | ~15 | Exchange hot/cold wallets | ðŸŸ¢ AUTOMATABLE |
| DeFi whales | ~20 | Large DeFi participants | ðŸŸ¢ AUTOMATABLE |
| Early adopters | ~10 | Genesis-era wallets | ðŸŸ¢ AUTOMATABLE |
| VC wallets | ~8 | Verified fund wallets | ðŸŸ¡ SEMI_AUTO |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Supply Dynamics** | Whale accumulation = bullish |
| **Dormant Awakening** | Old wallets moving = significant |
| **Exchange Flows** | Whale â†’ exchange = selling |

### How to Check

**Frequency:** Daily

**Alert Thresholds:**

| Event | Alert Level |
|-------|-------------|
| Dormant wallet (>1 year) moves | ðŸ”´ Critical |
| >$100M to exchange | ðŸŸ  High |
| >$100M from exchange | ðŸŸ  High (bullish) |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `whale_wallet_master_list.csv` | âœ… Good (50 records) | ðŸŸ¢ AUTOMATABLE | Keep as-is |
| Dormancy tracking | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |

---

## 5. Smart Money Patterns

### What We Track

Behavioral patterns indicating sophisticated market participants.

**Pattern Types:**

| Pattern | Description | Signal | Automation Status |
|---------|-------------|--------|-------------------|
| **Token Unlock Recipients** | Wallets receiving vested tokens | Potential selling | ðŸŸ¡ SEMI_AUTO |
| **Early Depositors** | First 1000 in new protocols | Airdrop hunters, informed | ðŸŸ¢ AUTOMATABLE |
| **"Cursed" Wallets** | Suspiciously good timing | Potential insiders | ðŸ”´ MANUAL_ONLY |
| **MEV Searchers** | Profitable MEV operations | Sophisticated actors | ðŸŸ¢ AUTOMATABLE |

### Why It Matters

| Impact | Description |
|--------|-------------|
| **Leading Indicator** | Smart money moves first |
| **Risk Assessment** | Insider selling = warning |
| **Methodology Value** | Patterns > specific wallets |

### How to Check (FREE Methods)

**Token Unlocks:**

```sql
-- Dune Analytics (FREE)
-- Find vesting contract recipients
-- Automation Status: SEMI_AUTO (requires Dune query setup)

SELECT 
    evt_tx_hash,
    "to" AS recipient,
    value/1e18 AS tokens,
    evt_block_time
FROM erc20_ethereum.evt_Transfer
WHERE contract_address = 0x[TOKEN_ADDRESS]
    AND "from" = 0x[VESTING_CONTRACT]
ORDER BY evt_block_time DESC
LIMIT 100
```

**Early Depositors:**

```sql
-- Find first 1000 depositors to a protocol
-- Automation Status: AUTOMATABLE via Dune

SELECT 
    "from" AS depositor,
    value AS deposit_amount,
    block_time,
    ROW_NUMBER() OVER (ORDER BY block_time) AS rank
FROM [protocol]_ethereum.deposits
ORDER BY block_time ASC
LIMIT 1000
```

**MEV Searchers (Ethereum):**

| Source | URL | Data | Automation Status |
|--------|-----|------|-------------------|
| Flashbots Dashboard | transparency.flashbots.net | Top searchers | ðŸŸ¢ AUTOMATABLE |
| MEV-Boost | mevboost.pics | Builder stats | ðŸŸ¢ AUTOMATABLE |

**MEV Searchers (Solana):**

| Source | URL | Data | Automation Status |
|--------|-----|------|-------------------|
| Jito Explorer | explorer.jito.wtf | Tips leaderboard | ðŸŸ¢ AUTOMATABLE |
| Dune | dune.com | Jito dashboards | ðŸŸ¢ AUTOMATABLE |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| `expert_watchlist_defi_alpha_corrected.csv` | âœ… Good (8 records) | ðŸŸ¢ AUTOMATABLE | Keep - real VC wallets |
| `expert_watchlist_solana_corrected.csv` | âœ… Good (5 records) | ðŸŸ¢ AUTOMATABLE | Keep |
| `expert_watchlist_mechanism_corrected.csv` | âœ… Good (3 records) | ðŸŸ¢ AUTOMATABLE | Keep |
| Token unlock tracking | ðŸ”´ Not built | ðŸŸ¡ SEMI_AUTO | Research task R1 |
| MEV searcher database | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | Research task R2 |

### âŒ Deprecated

| Item | Reason | Replacement |
|------|--------|-------------|
| `expert_watchlist_asymmetric.csv` | Fake addresses | Macro flow indicators |
| `expert_watchlist_macro.csv` | Fake addresses | Macro flow indicators |

---

## 6. Exchange Hot Wallet Tracking

### What We Track

Major exchange deposit/withdrawal wallets for flow analysis.

**Target Exchanges:**

| Exchange | Priority | Chains | Automation Status |
|----------|----------|--------|-------------------|
| Binance | ðŸ”´ Critical | ETH, BSC, BTC | ðŸŸ¢ AUTOMATABLE |
| Coinbase | ðŸ”´ Critical | ETH, BTC | ðŸŸ¢ AUTOMATABLE |
| Kraken | ðŸŸ  High | ETH, BTC | ðŸŸ¢ AUTOMATABLE |
| OKX | ðŸŸ  High | Multi-chain | ðŸŸ¢ AUTOMATABLE |
| Bybit | ðŸŸ¡ Medium | Multi-chain | ðŸŸ¢ AUTOMATABLE |

### Why It Matters

| Flow Direction | Interpretation |
|----------------|----------------|
| Large inflows | Potential selling |
| Large outflows | Accumulation/custody |
| Net exchange reserves | Macro sentiment |

### How to Check

**Frequency:** Hourly

**Sources (FREE):**

| Source | Data | Automation Status |
|--------|------|-------------------|
| Arkham Intelligence | Labeled exchange wallets | ðŸŸ¢ AUTOMATABLE |
| Etherscan Labels | Exchange tags | ðŸŸ¢ AUTOMATABLE |
| Dune Analytics | Exchange reserve dashboards | ðŸŸ¢ AUTOMATABLE |

### Current Status

| Item | Status | Automation Status | Notes |
|------|--------|-------------------|-------|
| Exchange wallet database | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | Research task R4 |
| Reserve tracking | ðŸ”´ Not built | ðŸŸ¢ AUTOMATABLE | CTO Board |

---

## Research Task Summary

| ID | Task | Priority | Output | Automation Status |
|----|------|----------|--------|-------------------|
| R1 | Token Unlock Schedule Database | ðŸŸ  High | `token_unlock_schedule.csv` | ðŸŸ¡ SEMI_AUTO |
| R2 | MEV Searcher Identification | ðŸŸ¡ Medium | `mev_searcher_tracker.csv` | ðŸŸ¢ AUTOMATABLE |
| R3 | Court Filing Monitor Setup | ðŸ”´ Critical | `estate_court_schedule.csv` | ðŸ”´ MANUAL_ONLY |
| R4 | Exchange Hot Wallet Database | ðŸŸ  High | `exchange_hot_wallets.csv` | ðŸŸ¢ AUTOMATABLE |

---

## CTO Board Implementation

### Priority 1: Estate Wallet Alerts

```yaml
service: estate_wallet_monitor
frequency: "*/15 * * * *"  # Every 15 minutes
chains: [bitcoin, ethereum, solana]
alert_threshold: 0.01  # 1% = any movement
priority: critical
output: alerts_pending.json
automation_status: AUTOMATABLE
```

### Priority 2: Daily Wallet Scans

```yaml
service: wallet_scanner
frequency: "0 6 * * *"  # Daily 06:00 UTC
categories: [market_makers, whales, treasuries]
output: daily_wallet_report.json
automation_status: AUTOMATABLE
```

### Priority 3: Pattern Detection

```yaml
service: pattern_detector
frequency: "0 * * * *"  # Hourly
patterns: [dormant_awakening, large_exchange_flow, accumulation]
output: pattern_alerts.json
automation_status: AUTOMATABLE
```

### Manual Task List (Analyst)

```yaml
manual_tasks:
  - name: Court Schedule Updates
    frequency: Weekly
    sources: [PACER, UK Courts, Kroll]
    output: estate_court_schedule.csv
    
  - name: Government Seizure Research
    frequency: Monthly
    sources: [DOJ press releases, UK courts, German BKA]
    output: Update estate_wallet_tracker.csv
    
  - name: VC Wallet Identification
    frequency: Quarterly
    sources: [13F filings, Crunchbase, news]
    output: Update expert_watchlist files
```

---

## File Inventory

| File | Records | Status | Automation Status | Action |
|------|---------|--------|-------------------|--------|
| `estate_wallet_tracker.csv` | 51 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `market_maker_wallet_tracker.csv` | 35 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `protocol_treasury_tracker.csv` | 35 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `whale_wallet_master_list.csv` | 50 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `expert_watchlist_defi_alpha_corrected.csv` | 8 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `expert_watchlist_solana_corrected.csv` | 5 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `expert_watchlist_mechanism_corrected.csv` | 3 | âœ… Good | ðŸŸ¢ AUTOMATABLE | Keep |
| `master_wallet_tracker.csv` | 180 | âš ï¸ Update | ðŸŸ¢ AUTOMATABLE | Merge corrected files |
| `expert_watchlist_asymmetric.csv` | 2 | âŒ Deprecate | N/A | Replace with flow indicators |
| `expert_watchlist_macro.csv` | 2 | âŒ Deprecate | N/A | Replace with flow indicators |

---

**Next Document:** [02_CRYPTO_MARKETS.md](./02_CRYPTO_MARKETS.md)
