# diBoaS Analytics v3 - Complete Technical Deep Dive

## Executive Summary

diBoaS Analytics v3 is a **production-grade Python CLI application** that provides institutional-quality financial intelligence for a retail fintech platform. It performs historical backtesting, forward-looking risk simulations, real-time protocol monitoring, anomaly detection, and generates personalized newsletters through a deterministic (non-LLM) template system.

---

## 1. Technology Stack & Architecture

### 1.1 Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Language** | Python 3.10+ | Core application |
| **Data Processing** | pandas 2.0+, numpy 1.24+ | Time series manipulation |
| **Statistical Analysis** | scipy 1.10+ | Distributions, statistics |
| **Machine Learning** | scikit-learn 1.3+ | Anomaly detection (Isolation Forest) |
| **API Clients** | requests 2.28+, yfinance 0.2+ | External data fetching |
| **Configuration** | python-dotenv, JSON, YAML | Multi-format configs |
| **Testing** | pytest 7.0+, pytest-cov | Unit and integration testing |

### 1.2 Architectural Pattern: 5-Layer Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LAYER 1: RESEARCHER                          │
│  Data Collection (FileLoader, FRED, Yahoo, DeFiLlama, CoinGecko)   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Raw CSV/JSON Data
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        LAYER 2: VALIDATOR                           │
│           Gate 1 (Schema) + Gate 2 (Analytics Quality)             │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Validated Data
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         LAYER 3: ANALYST                            │
│     Battle Test, Monte Carlo, Monitoring, Anomaly Detection        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Analytics Results
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        LAYER 4: OPERATOR                            │
│         Intelligence Triggers, Cooldowns, Alert Consolidation      │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Triggered Actions
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        LAYER 5: PRESENTER                           │
│    Adelaide Newsletter (Regime → Template → Persona → Locale)      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 Project Structure

```
diboas-analytics/
├── main.py                     # CLI entry point (argparse)
├── config/
│   ├── strategies.json         # 10 strategies (NEVER hardcode!)
│   ├── protocols.py            # 6 DeFi protocol definitions
│   ├── thresholds.py           # Alert thresholds
│   ├── dream_mode.py           # Consumer path mappings
│   ├── triggers.yaml           # Intelligence trigger thresholds
│   ├── clo_compliance.yaml     # Legal compliance settings
│   └── tenants/diboas.yaml     # Multi-tenant configuration
├── src/
│   ├── collectors/             # Data collection layer
│   ├── engines/                # Core computation engines
│   ├── validators/             # 4 validation gates
│   ├── adelaide/               # Newsletter generation
│   ├── triggers/               # Intelligence layer
│   ├── crisis/                 # Human approval workflows
│   ├── registries/             # Plugin system
│   ├── domain/                 # Business models
│   ├── policies/               # Access control
│   └── utils/                  # Shared utilities
├── data/                       # Bundled historical CSVs
├── outputs/                    # Generated results (git-ignored)
└── tests/                      # pytest test suite
```

### 1.4 Code Standards & Practices

**Design Patterns:**
- **Registry Pattern**: All major components (collectors, engines, validators, triggers, personas, outputs) use decorator-based registration for dynamic loading
- **Strategy Pattern**: Multiple interchangeable algorithms for anomaly detection, regime classification
- **Template Method**: Base classes define workflow, subclasses implement specifics
- **Facade Pattern**: `AdelaideGenerator` orchestrates complex multi-step generation

**Coding Standards:**
- Type hints throughout (Python 3.10+ syntax)
- Dataclasses for immutable value objects
- Enums for fixed sets (severity levels, regimes, statuses)
- Logging at all levels with structured context
- Comprehensive docstrings (Google style)
- Exception hierarchy with custom `DiBoaSError` base class

**Configuration Philosophy:**
- **NEVER hardcode strategies** - always load from `config/strategies.json`
- All thresholds externalized to config files
- Multi-tenant support via per-tenant YAML configs
- Environment variables for API keys via `.env`

---

## 2. Data Collection & Monitoring

### 2.1 Data Sources Overview

| Source | Type | Data Collected | Update Frequency |
|--------|------|----------------|------------------|
| **FRED** | Live API | Treasury yields, real yields, credit spreads, M2 money supply | Daily |
| **Yahoo Finance** | Live API | S&P 500, NASDAQ, VIX, crypto prices (BTC/ETH/SOL), commodities | Real-time available, daily historical |
| **DeFiLlama** | Live API | Protocol APYs, TVL, pool data | Real-time available, daily historical |
| **CoinGecko** | Live API | Crypto prices, market caps, volumes (backup) | Real-time |
| **Alternative.me** | Live API | Fear & Greed Index | Daily |
| **Bundled CSVs** | File | Historical backfill (May 2022 - Dec 2025) | Static |

### 2.2 Collector Architecture

```python
# Base class pattern
class DataProvider(ABC):
    @abstractmethod
    def fetch_historical(self, start_date, end_date) -> pd.DataFrame
    
    @abstractmethod
    def fetch_current(self) -> dict
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool
```

**FileLoader** - Loads bundled historical CSVs:
```python
FILES = {
    'defillama': 'defillama_historical_apy.csv',
    'yahoo': 'crypto_prices.csv',  # Wide format: btc_close, eth_close, sol_close
    'jupiter': 'jupiter_jlp_historical_apy.csv',
    'treasury_yields': 'treasury_yields.csv',
    'sentiment': 'sentiment_indicators.csv',
    'tradfi': 'tradfi_benchmark_data.csv',
}
```

**Live API Collectors** with rate limiting:
- `FREDCollector`: 120 requests/minute
- `YahooCollector`: yfinance library (no explicit limit)
- `DeFiLlamaCollector`: 60 requests/minute
- `CoinGeckoCollector`: 30 requests/minute (no API key needed)
- `AlternativeCollector`: Fear & Greed Index

### 2.3 Data Schemas

**DeFiLlama APY Data (defillama_historical_apy.csv):**
```
date,protocol,chain,pool,apy,tvl_usd
2024-01-15,aave-v3,ethereum,USDC,4.52,1500000000
```

**Crypto Prices (crypto_prices.csv) - V3 Wide Format:**
```
date,btc_close,eth_close,sol_close
2024-01-15,42500.00,2350.00,95.50
```

**Treasury Yields (treasury_yields.csv):**
```
date,yield_2y,yield_5y,yield_10y,yield_30y
2024-01-15,4.35,4.12,4.05,4.25
```

**Sentiment Indicators (sentiment_indicators.csv):**
```
date,fear_greed_index,fear_greed_label
2024-01-15,65,Greed
```

### 2.4 Update Frequency Guidance

| Data Type | Recommended Update | Rationale |
|-----------|-------------------|-----------|
| **Adelaide Pulse (daily)** | Every 4 hours | Near-real-time market awareness |
| **Adelaide Weekly** | Every 24 hours | Comprehensive analysis |
| **Protocol Health** | Every 15 minutes | TVL/APY monitoring |
| **Trigger Evaluation** | Every 5 minutes | Crisis detection |
| **Battle Test** | On-demand | Historical, static data |
| **Monte Carlo** | Daily or on-demand | Forward projections |

---

## 3. Market Indicators & User Value

### 3.1 Tracked Indicators

**Macro Economics:**
| Indicator | Source | Thresholds | User Value |
|-----------|--------|------------|------------|
| VIX (Volatility Index) | Yahoo | L2: >30, L3: >40 | Market fear gauge |
| 10Y Treasury Yield | FRED | N/A | Risk-free rate benchmark |
| Real Yields (TIPS) | FRED | N/A | Inflation-adjusted returns |
| HY Credit Spread | FRED | Warning: >150bp | Credit market stress |
| M2 Money Supply | FRED | N/A | Liquidity conditions |

**Crypto Markets:**
| Indicator | Source | Thresholds | User Value |
|-----------|--------|------------|------------|
| BTC Price | Yahoo/CoinGecko | L3: -10%, L4: -20% | Market leader |
| ETH Price | Yahoo/CoinGecko | L3: -15% | DeFi benchmark |
| SOL Price | Yahoo/CoinGecko | L3: -20%, L4: -30% | Solana ecosystem |
| Fear & Greed Index | Alternative.me | <25: Extreme Fear | Sentiment gauge |

**DeFi Protocol Health:**
| Indicator | Source | Thresholds | User Value |
|-----------|--------|------------|------------|
| Protocol TVL | DeFiLlama | Warning: -15%, Critical: -30% | Capital flight detection |
| Protocol APY | DeFiLlama | Warning: ±50%, Critical: ±100% | Yield anomalies |
| Utilization Rate | DeFiLlama | Warning: 85%, Critical: 95% | Liquidity stress |
| Sky Depeg | Custom | L2: 1%, L3: 2%, L4: 5% | Stablecoin risk |

### 3.2 Value to Users

1. **Risk-Appropriate Recommendations**: Match user risk tolerance to strategy
2. **Early Warning System**: Detect protocol issues before major losses
3. **Educational Context**: Explain market movements in accessible terms
4. **Historical Perspective**: Show how current events compare to past
5. **Emotional Guardrails**: Prevent panic selling during downturns

---

## 4. Layer-by-Layer Technical Deep Dive

### 4.1 Layer 1: Researcher (Data Collection)

**Purpose:** Gather raw data from multiple sources with graceful degradation.

**Key Components:**
- `FileLoader`: Loads bundled CSVs with date filtering and validation
- `DataAggregator`: Combines data from multiple sources
- Live collectors for each API with rate limiting

**Data Flow:**
```
API Request → Rate Limiter → HTTP Client → JSON/CSV Response
     → Data Validation → DataFrame → Cache (optional) → Output
```

### 4.2 Layer 2: Validator (Data Quality Gates)

**Gate 1 - Schema Validation:**
```python
# Validates raw CSV data against schemas
Checks:
- Required columns present
- Data types correct
- Value bounds (e.g., APY not negative, drawdown 0-100%)
- Data freshness (not stale)
- Minimum row count

Issue Codes:
- G1-COL-001: Missing required column
- G1-TYP-001: Type mismatch
- G1-BND-001: Value out of bounds
```

**Gate 2 - Analytics Validation (QR Board Rules CV-01 to CV-07):**
```python
CV-01: Portfolio value never negative (Critical)
CV-02: Drawdown between 0% and 100% (Critical)
CV-03: Stable strategies (0% crypto) must have 0% drawdown (Warning)
CV-04: Final value >= deposited for stable strategies (Warning)
CV-05: Return % matches calculation (Critical)
CV-06: Net return > 0 after gas costs (Critical)
CV-07: Initial deposit >= per-strategy minimum (Warning)
```

### 4.3 Layer 3: Analyst (Core Engines)

#### 4.3.1 Battle Test Engine (Historical Backtesting)

**Methodology:** Dollar-Cost Averaging (DCA) simulation through historical market conditions.

**Time Period:** May 2022 - December 2025 (bundled data)

**Scenarios:**
| Scenario | Name | Initial | Monthly DCA |
|----------|------|---------|-------------|
| A | Felipe (Sophisticated) | $10,000 | $200/month |
| B | Ana (Minimum) | $5 | $5/month |
| C | Per-Strategy Minimum | Varies | Varies |

**Daily Return Calculation:**
```python
def _calculate_daily_return(strategy, current_date):
    total_return = 0.0
    
    # Stable allocations (no price exposure)
    for protocol, weight in strategy.stable_allocations.items():
        apy = get_protocol_apy(protocol, current_date)
        daily_return = apy / 365 / 100
        total_return += weight * daily_return
    
    # Crypto allocations (with price exposure)
    for protocol, weight in strategy.crypto_allocations.items():
        if protocol == 'jlp':
            # JLP = basket return + fee APY
            daily_return = get_jlp_return(current_date)
        else:
            # Sanctum/Jito = SOL return + staking APY
            sol_return = get_price_return('SOL', current_date)
            staking_apy = get_protocol_apy(protocol, current_date)
            daily_return = sol_return + (staking_apy / 365 / 100)
        
        total_return += weight * daily_return
    
    return total_return
```

**JLP Return Formula (QR Board Validated):**
```python
def calculate_jlp_daily_return(sol_return, eth_return, btc_return, jlp_apy):
    """
    JLP basket: 45% SOL, 27% ETH, 27% BTC
    """
    price_return = (0.45 * sol_return) + (0.27 * eth_return) + (0.27 * btc_return)
    fee_return = jlp_apy / 365 / 100  # Daily APY as decimal
    return price_return + fee_return
```

**Proxy Formulas (When Historical Data Unavailable):**
| Protocol | Formula | Confidence |
|----------|---------|------------|
| Sanctum | `Lido_ETH_APY × 2.0 + 0.5%` | Medium |
| Jito | `Lido_ETH_APY × 2.0 + 1.0%` | Medium |
| JLP (pre-Jan 2024) | Fixed 25% APY | Low |
| Compound V3 | `Aave_APY × 1.1` | High |

**Output:** `BattleTestResult` with daily values, final value, profit, return %, max drawdown.

#### 4.3.2 Monte Carlo Engine (Forward-Looking Risk)

**Methodology:** Regime-switching Monte Carlo with fat-tailed distributions.

**Parameters:**
- 5,000 simulations per strategy
- 48-month horizon (4 years)
- Random seed for reproducibility (default: 42)

**4 Market Regimes with Markov Transitions:**
```python
REGIMES = {
    'bull': {
        'mean_mult': 1.5,    # Higher returns
        'vol_mult': 0.8,     # Lower volatility
        'duration': 180,     # ~6 months
    },
    'bear': {
        'mean_mult': 0.3,    # Lower returns
        'vol_mult': 1.5,     # Higher volatility
        'duration': 120,     # ~4 months
    },
    'crash': {
        'mean_mult': -2.0,   # Negative returns
        'vol_mult': 3.0,     # Very high volatility
        'duration': 30,      # ~1 month
    },
    'recovery': {
        'mean_mult': 2.0,    # High returns
        'vol_mult': 1.2,     # Moderate volatility
        'duration': 90,      # ~3 months
    }
}

# Transition probabilities (Markov matrix)
TRANSITIONS = {
    'bull': {'bull': 0.85, 'bear': 0.10, 'crash': 0.03, 'recovery': 0.02},
    'bear': {'bull': 0.05, 'bear': 0.80, 'crash': 0.10, 'recovery': 0.05},
    'crash': {'bull': 0.00, 'bear': 0.20, 'crash': 0.30, 'recovery': 0.50},
    'recovery': {'bull': 0.40, 'bear': 0.10, 'crash': 0.05, 'recovery': 0.45}
}
```

**Fat-Tailed Returns (Student-t Distribution):**
```python
# Use Student-t with df=4 for fat tails
crypto_return = stats.t.rvs(df=4, loc=crypto_mean, scale=crypto_std)
```

**Crypto Correlation Matrix:**
| Pair | Correlation |
|------|-------------|
| SOL/ETH | 0.75 |
| SOL/BTC | 0.70 |
| ETH/BTC | 0.85 |

**Output Metrics:**
- Mean/Median final value
- VaR (Value at Risk) at 95% and 99%
- CVaR (Conditional VaR) at 95% and 99%
- Probability of loss (any, 10%, 20%, 50%)
- Mean and P95 max drawdown
- Percentiles: P5, P10, P25, P75, P90, P95

#### 4.3.3 Monitoring Engine (Protocol Health)

**Purpose:** Real-time health checks with alerting.

**Checks:**
```python
TVL_THRESHOLDS = {
    'drop_warning': -0.15,   # -15% in 24h
    'drop_critical': -0.30,  # -30% in 24h
    'minimum_usd': 1_000_000
}

UTILIZATION_THRESHOLDS = {
    'warning': 0.85,         # 85%
    'critical': 0.95         # 95%
}

APY_THRESHOLDS = {
    'deviation_warning': 0.50,   # 50% change
    'deviation_critical': 1.00,  # 100% change
    'minimum': 0.0,              # Not negative
    'maximum': 500.0             # Suspicious if above
}
```

**Output:** `ProtocolHealth` with health score (0-100), list of `Alert` objects.

#### 4.3.4 Anomaly Engine (ML-Based Detection)

**3 Detection Methods:**

1. **Z-Score Detector:**
```python
class ZScoreDetector:
    window = 30  # Rolling window
    threshold = 3.0  # Standard deviations
    
    # Detects values > 3 std devs from rolling mean
```

2. **Isolation Forest Detector:**
```python
from sklearn.ensemble import IsolationForest

contamination = 0.05  # 5% expected outliers
n_estimators = 100
random_state = 42
```

3. **Correlation Monitor:**
```python
# Checks if crypto correlations deviate from expected
EXPECTED_CORRELATIONS = {
    ('SOL', 'ETH'): 0.75,
    ('SOL', 'BTC'): 0.70,
    ('ETH', 'BTC'): 0.85
}
deviation_threshold = 0.20  # 20% deviation warning
```

### 4.4 Layer 4: Operator (Intelligence Triggers)

**Trigger Categories:**
| Category | Examples |
|----------|----------|
| Protocol | Sky depeg, TVL drops, utilization spikes |
| Market | BTC/ETH/SOL drops, volatility spikes |
| Wallet | Estate movements ($10M+), whale activity ($25M+) |
| Macro | VIX spikes, yield curve inversion, credit spread widening |

**Trigger Evaluation Flow:**
```python
def evaluate_all(data, correlation_id):
    results = []
    
    for trigger_name in registry.list_available():
        trigger = registry.get(trigger_name)
        
        # Check if enabled
        if not trigger.enabled:
            continue
            
        # Evaluate
        result = trigger.evaluate(data)
        
        if not result.fired:
            continue
            
        # Check cooldown (prevent spam)
        if cooldown_manager.is_on_cooldown(result.trigger_id):
            continue
            
        # Set cooldown
        cooldown_manager.set_cooldown(result.trigger_id)
        
        results.append(result)
    
    # Consolidate related alerts
    return consolidator.consolidate(results)
```

**Cooldown Management:**
- Default: 60 minutes between same trigger firing
- File-based storage (`data/trigger_cooldowns.json`)
- Prevents alert fatigue

**Priority Levels:**
| Level | Name | Response |
|-------|------|----------|
| P0 | Critical | Immediate action |
| P1 | High | Same-day response |
| P2 | Medium | Monitor closely |
| P3 | Info | Awareness only |

### 4.5 Layer 5: Presenter (Adelaide Newsletter)

**Generation Pipeline:**
```
Market Data → Regime Classification → Template Selection
     → Persona Adaptation → Localization → Multi-Channel Formatting
```

**6 Market Regimes:**
```python
class MarketRegime(Enum):
    RISK_ON_BULL = "risk_on_bull"      # Markets up, risk appetite high
    RISK_ON_BEAR = "risk_on_bear"      # Markets down but resilient
    RISK_OFF_BULL = "risk_off_bull"    # Markets up but cautious
    RISK_OFF_BEAR = "risk_off_bear"    # Markets down, defensive
    TRANSITION = "transition"           # Mixed signals
    CRISIS = "crisis"                   # Emergency
```

**Regime Classification Thresholds:**
```python
BULL_THRESHOLD = 2.0    # +2% = bullish
BEAR_THRESHOLD = -2.0   # -2% = bearish
VIX_LOW = 20
VIX_HIGH = 25
VIX_CRISIS = 30
FG_GREED = 60
FG_FEAR = 40
FG_EXTREME_FEAR = 25

# Crisis triggers
CRISIS_BTC_DROP = -20.0               # -20% BTC drop
CRISIS_EXPLOIT_THRESHOLD = 10_000_000  # $10M exploit
```

**3 Personas:**
| Persona | Voice | Target User |
|---------|-------|-------------|
| Ana | Warm, reassuring, grandmother-like | Conservative, financially inexperienced |
| Maria | Professional, data-driven, analytical | Balanced, moderate sophistication |
| Felipe | Direct, sophisticated, action-oriented | Aggressive, high financial literacy |

**5 Output Formats:**
| Format | Purpose | Character Limit |
|--------|---------|-----------------|
| newsletter_md | Full Markdown newsletter | None |
| twitter_thread | Social media | 280 per tweet |
| linkedin_post | Professional network | ~3000 |
| website_teaser | Homepage preview | ~200 |
| substack | Email newsletter | None |

**2 Locales:**
- `en`: English
- `pt-br`: Portuguese (Brazilian)

---

## 5. Data Storage & Transformation

### 5.1 Storage Architecture

| Layer | Storage | Format | Location |
|-------|---------|--------|----------|
| Raw Data | Bundled CSVs | CSV | `data/*.csv` |
| Config | JSON/YAML/Python | Multiple | `config/` |
| Outputs | JSON/CSV/Markdown | Multiple | `outputs/` |
| Cooldowns | JSON | File-based | `data/trigger_cooldowns.json` |
| Audit Trails | JSON | File-based | `outputs/audit/` |

### 5.2 Data Transformation Pipeline

```
┌──────────────────┐
│   Raw CSV Files  │ (Historical data, May 2022 - Dec 2025)
└────────┬─────────┘
         │ FileLoader.load()
         ▼
┌──────────────────┐
│  pandas DataFrame │ (Parsed, date-indexed)
└────────┬─────────┘
         │ Gate 1 Validation (Schema)
         ▼
┌──────────────────┐
│  Validated Data   │ (Type-checked, bounds-checked)
└────────┬─────────┘
         │ DataAggregator.get_*_series()
         ▼
┌──────────────────┐
│  Time Series      │ (Protocol APY, prices, returns)
└────────┬─────────┘
         │ BattleTestEngine / MonteCarloEngine
         ▼
┌──────────────────┐
│  Simulation       │ (Daily values, statistics)
│  Results          │
└────────┬─────────┘
         │ Gate 2 Validation (CV-01 to CV-07)
         ▼
┌──────────────────┐
│  Validated        │ (QR Board approved)
│  Analytics        │
└────────┬─────────┘
         │ Trigger Evaluation
         ▼
┌──────────────────┐
│  Triggered        │ (Alerts, crisis levels)
│  Actions          │
└────────┬─────────┘
         │ Gate 3 Validation (Triggers)
         ▼
┌──────────────────┐
│  Adelaide         │ (Regime, template, persona)
│  Content          │
└────────┬─────────┘
         │ Gate 4 Validation (CLO Compliance)
         ▼
┌──────────────────┐
│  Published        │ (Multi-channel output)
│  Newsletter       │
└──────────────────┘
```

### 5.3 Key Data Structures

**BattleTestResult:**
```python
@dataclass
class BattleTestResult:
    strategy_id: int
    strategy_name: str
    scenario: str
    period_start: date
    period_end: date
    days: int
    deposited: float
    final_value: float
    profit: float
    return_pct: float
    max_drawdown_pct: float
    daily_values: list[float]  # For charting
```

**MonteCarloResult:**
```python
@dataclass
class MonteCarloResult:
    strategy_id: int
    simulations: int
    horizon_months: int
    total_deposited: float
    
    mean_final: float
    median_final: float
    mean_return: float
    median_return: float
    
    prob_any_loss: float
    prob_loss_10pct: float
    prob_loss_20pct: float
    prob_loss_50pct: float
    
    var_95: float
    cvar_95: float
    var_99: float
    cvar_99: float
    
    p5_final: float
    p95_final: float
    
    mean_max_drawdown: float
    p95_max_drawdown: float
    
    final_values: np.ndarray  # Full distribution
```

---

## 6. Trigger System Deep Dive

### 6.1 Trigger Configuration (triggers.yaml)

```yaml
protocol:
  sky:
    depeg_l2:
      threshold_pct: 1.0
    depeg_l3:
      threshold_pct: 2.0
    depeg_l4:
      threshold_pct: 5.0
    tvl_l2:
      threshold_pct: -10
    tvl_l3:
      threshold_pct: -25

market:
  btc:
    drop_l3:
      threshold_pct: -10
    drop_l4:
      threshold_pct: -20
  volatility:
    crypto_spike:
      threshold_std: 2.0

wallet:
  estate:
    l2:
      threshold_usd: 50000000
    l3:
      threshold_usd: 100000000
  whale:
    movement:
      threshold_usd: 25000000

macro:
  vix:
    l2:
      threshold: 30
    l3:
      threshold: 40
```

### 6.2 Trigger Evaluation

```python
class IntelligenceTriggerEvaluator:
    def evaluate_all(self, data, correlation_id=None):
        """
        1. Get all registered triggers
        2. For each trigger:
           a. Check if enabled
           b. Check cooldown
           c. Evaluate against data
           d. Set cooldown if fired
        3. Consolidate related alerts
        4. Return fired triggers only
        """
```

### 6.3 Cooldown Management

```python
class IntelligenceCooldownManager:
    default_cooldown_minutes = 60
    
    # File-based storage (JSON)
    state_file = "data/trigger_cooldowns.json"
    
    def is_on_cooldown(self, trigger_id: str) -> bool
    def set_cooldown(self, trigger_id: str, minutes: int = None)
    def clear_cooldown(self, trigger_id: str) -> bool
    def get_remaining_minutes(self, trigger_id: str) -> int
```

---

## 7. Strategy Configuration

### 7.1 The 10 Official Strategies

| ID | Name | Crypto % | Risk | Allocation |
|----|------|----------|------|------------|
| 1 | Safe Harbor | 0% | Minimal | 50% Sky + 30% Aave + 20% Compound |
| 2 | Stable Growth | 30% | Low | 70% Sky + 30% Sanctum |
| 3 | Goal Keeper | 0% | Minimal | 60% Sky + 25% Aave + 15% Compound |
| 4 | Steady Progress | 35% | Low-Medium | 65% Sky + 35% Sanctum |
| 5 | Patient Builder | 0% | Minimal | 50% Sky + 30% Aave + 20% Compound |
| 6 | Balanced Builder | 40% | Medium | 60% Sky + 25% Sanctum + 15% JLP |
| 7 | Steady Compounder | 0% | Minimal | 55% Sky + 30% Aave + 15% Compound |
| 8 | Wealth Accelerator | 70% | High | 30% Sky + 35% Sanctum + 35% JLP |
| 9 | Yield Maximizer | 0% | Minimal | 45% Sky + 35% Aave + 20% Compound |
| 10 | Full Throttle | 85% | Very High | 15% Sky + 30% Sanctum + 35% JLP + 20% Jito |

### 7.2 Critical Rules

1. **NEVER hardcode strategies** - Always load from `config/strategies.json`
2. **JLP basket weights**: 45% SOL, 27% ETH, 27% BTC (not 50/25/25)
3. **Jito ONLY in Strategy 10** (Full Throttle)
4. **No Huma** in any strategy (removed in v2.0)
5. **Stable strategies (0% crypto) must have 0% drawdown** (CV-03)

### 7.3 Dream Mode Paths (Consumer Simplification)

```python
DREAM_MODE_PATHS = {
    'safety': {
        'strategies': [1, 3, 5, 7, 9],  # 0% crypto
        'label': 'Safety First',
        'color': '#2563EB',  # Blue
    },
    'balance': {
        'strategies': [2, 4, 6],  # 30-40% crypto
        'label': 'Balanced Growth',
        'color': '#7C3AED',  # Purple
    },
    'growth': {
        'strategies': [8, 10],  # 70-85% crypto
        'label': 'Maximum Growth',
        'color': '#DC2626',  # Red
    }
}
```

---

## 8. Compliance & Validation

### 8.1 4 Validation Gates

| Gate | Purpose | Owner |
|------|---------|-------|
| Gate 1 | Schema validation of raw data | QR Board |
| Gate 2 | Analytics quality (CV-01 to CV-07) | QR Board |
| Gate 3 | Trigger validity | QR Board |
| Gate 4 | Legal compliance | CLO Board |

### 8.2 Gate 4 CLO Compliance

**Routing Decisions:**
```yaml
auto_approve: [level_0, level_1, level_2]
require_human: [level_3, level_4, level_5]
```

**Approval Chains:**
| Level | Approvers |
|-------|-----------|
| 3 | CLO Board, CEO |
| 4 | CLO Board, CEO, External Counsel |
| 5 | CLO Board, CEO, Board, External Counsel |

**SLA Times:**
- Level 3: 60 minutes
- Level 4: 75 minutes
- Level 5: 90 minutes
- Spot-check (first 20 editions): 8 hours

**Geo-Blocked:** UK (FSMA Section 21)

**Prohibited Terms:**
- Universal: "guaranteed", "risk-free", "cannot lose", "100% safe"
- US: "you should invest", "I recommend", "buy now"
- BR: "lucro garantido", "sem risco"
- EU: "guaranteed returns", "capital protection guarantee"

---

## 9. Multi-Tenant Support

### 9.1 Tenant Tiers

| Tier | Estate Tracking | Whale Alerts | API Calls/Month |
|------|-----------------|--------------|-----------------|
| diBoaS User | ✅ | ✅ | Unlimited |
| B2B Standard | ❌ | ❌ | 1,000 |
| B2B Premium | ❌ | ❌ | 10,000 |

### 9.2 Feature Flags

```yaml
# config/tenants/diboas.yaml
features:
  estate_wallet_tracking: true
  whale_alerts: true
  real_time_data: true
  custom_strategies: true
  advanced_analytics: true

collectors:
  - fred
  - yahoo_live
  - defillama_live
  - coingecko
  - alternative
```

---

## 10. CLI Commands

```bash
# Data Collection
python main.py collect --offline           # Load bundled data
python main.py collect --source all        # Fetch live data

# Simulations
python main.py battle-test                 # All strategies, Scenario A
python main.py battle-test --strategy 1 --scenario B
python main.py monte-carlo --simulations 5000

# Monitoring
python main.py monitor                     # Check protocol health
python main.py anomaly                     # Run anomaly detection

# Triggers
python main.py triggers                    # Evaluate all triggers
python main.py triggers --dry-run          # Don't record cooldowns

# Validation
python main.py validate-gate1              # Schema validation
python main.py validate-gate2              # Analytics validation
python main.py validate-clo --jurisdiction US

# Adelaide
python main.py adelaide --persona ana --locale en
python main.py adelaide --persona all --format newsletter_md,twitter_thread

# Full Pipeline
python main.py all --offline               # Run everything

# Registry
python main.py registry --type all         # List all registered components
```

---

## 11. Key Formulas & Calculations Summary

### Portfolio Return
```
Daily Return = Σ(weight × protocol_daily_return)
              = Σ(stable_weight × APY/365) + Σ(crypto_weight × (price_return + staking_APY/365))
```

### JLP Return
```
JLP_daily = (0.45 × SOL_return) + (0.27 × ETH_return) + (0.27 × BTC_return) + (JLP_APY/365)
```

### Max Drawdown
```
Drawdown_t = (Peak_t - Value_t) / Peak_t
Max_Drawdown = max(Drawdown_t) for all t
```

### VaR (Value at Risk)
```
VaR_95 = Percentile(final_values, 5)  # 95% confidence
VaR_99 = Percentile(final_values, 1)  # 99% confidence
```

### CVaR (Conditional VaR / Expected Shortfall)
```
CVaR_95 = Mean(final_values where final_values ≤ VaR_95)
```

### Z-Score Anomaly
```
Z = (value - rolling_mean) / rolling_std
Anomaly if |Z| > 3.0
```

### Proxy APY
```
Sanctum_APY = Lido_ETH_APY × 2.0 + 0.5%
Jito_APY = Lido_ETH_APY × 2.0 + 1.0%
JLP_APY = 25% (fixed, pre-Jan 2024)
Compound_APY = Aave_APY × 1.1
```

---

## 12. Summary

diBoaS Analytics v3 is a **complete, production-ready system** that:

1. **Collects data** from 6+ sources with graceful degradation
2. **Validates** through 4 gates ensuring data quality and legal compliance
3. **Analyzes** using historical backtesting and Monte Carlo simulations
4. **Monitors** protocol health and detects anomalies in real-time
5. **Triggers** intelligent alerts with cooldown management
6. **Generates** personalized newsletters without LLM dependency
7. **Supports** multi-tenant B2B deployment

**Key differentiators:**
- Zero LLM dependency (deterministic, auditable)
- 5-layer architecture with clear separation of concerns
- Comprehensive validation gates
- Multi-persona, multi-locale content generation
- Institutional-grade risk metrics for retail users
- $0 operational cost design (file-based, free-tier APIs)
