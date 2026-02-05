# Macro Operating System & Mine Detector OS - Complete Technical Deep Dive

## Executive Summary

The Macro Operating System and Mine Detector OS represent a **dual-layer market intelligence framework** designed to answer two fundamental questions:

1. **Macro OS:** "What market regime are we in? Is it safe to be in risk assets?"
2. **Mine Detector OS:** "Is this specific security safe to own?"

Together, they form a **comprehensive risk surveillance system** that monitors macro conditions globally while scanning individual securities for idiosyncratic landmines. The Macro OS provides the **weather report** (regime context), while Mine Detector provides the **terrain analysis** (single-name risk scoring).

**Design Philosophy:**
- **Macro OS:** "Levels lie; changes tell the truth" - Focus on regime detection through pattern recognition
- **Mine Detector:** "If you can't see the landmine, you ARE the landmine" - Proactive risk identification

**Bundle Version:** `2026-01-30-r9` (unified versioning across all Mine Detector documents)

---

## 1. Technology Stack & Architecture

### 1.1 Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Language** | Python 3.10+ | Core implementation |
| **Data Structures** | dataclasses, Enum | Immutable value objects, type-safe enums |
| **Type Safety** | Type hints (full coverage) | Compile-time checking |
| **Time Handling** | datetime (UTC-only) | Consistent timezone management |
| **Math** | math (stdlib) | Score normalization (softmax, sqrt) |
| **Concurrency** | threading.Lock | State isolation (planned) |
| **Configuration** | Dict-based configs | Weights, thresholds, platform settings |

### 1.2 Architectural Pattern: Dual-System Design

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MACRO OPERATING SYSTEM                          │
│   "What regime are we in? Is it safe to be in risk assets?"        │
│                                                                     │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│   │ Frontline │  │   Deep    │  │Fundamental│  │Structural │      │
│   │Monitoring │  │Diagnostics│  │  Drivers  │  │  Forces   │      │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘      │
│         │              │              │              │              │
│         └──────────────┴──────────────┴──────────────┘              │
│                              │                                       │
│                    ┌─────────▼─────────┐                            │
│                    │  7 CANONICAL      │                            │
│                    │  PATTERNS         │                            │
│                    │  (Regime Types)   │                            │
│                    └─────────┬─────────┘                            │
└──────────────────────────────┼──────────────────────────────────────┘
                               │ Regime Signal
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       MINE DETECTOR OS                               │
│      "Is this specific security safe to own?"                        │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                    9 RISK CATEGORIES                          │  │
│   │  Catalyst │ Solvency │ Crowding │ Liquidity │ Momentum       │  │
│   │  Governance │ Refinancing │ Dilution │ Event                 │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│   ┌────────────────┐  ┌──────▼──────┐  ┌────────────────┐          │
│   │  Addendum A    │  │ COMPOSITE   │  │  Addendum D    │          │
│   │  ML Regime     │──│   SCORE     │──│  Structural    │          │
│   │  Classification│  │  (0-100)    │  │  Overlay       │          │
│   └────────────────┘  └──────┬──────┘  └────────────────┘          │
│                              │                                       │
│   ┌────────────────┐  ┌──────▼──────┐  ┌────────────────┐          │
│   │  Addendum B    │  │   RISK      │  │  Addendum E    │          │
│   │  Social        │──│   LEVEL     │──│  Maintenance   │          │
│   │  Sentiment     │  │  (Action)   │  │  & Operations  │          │
│   └────────────────┘  └──────┬──────┘  └────────────────┘          │
│                              │                                       │
│                       ┌──────▼──────┐                               │
│                       │ Addendum C  │                               │
│                       │ Brokerage   │                               │
│                       │ Integration │                               │
│                       └─────────────┘                               │
└──────────────────────────────────────────────────────────────────────┘
```

### 1.3 Project Structure

```
new/
├── macro-operating-system.md           # Macro regime detection (single doc)
│
└── mine-detector-os/                   # Single-name risk scanner (bundle)
    ├── mine-detector-os.md             # Core OS: 9 categories, scoring, interfaces
    ├── mine-detector-addendum-a-ml-classification.md    # Regime classification
    ├── mine-detector-addendum-b-social-sentiment.md     # Social media analysis
    ├── mine-detector-addendum-c-brokerage.md            # Portfolio sync, execution
    ├── mine-detector-addendum-d-adr-smallcap.md         # Structural overlay
    ├── mine-detector-addendum-e-maintenance-operations.md # Data ops, calibration
    └── feedback/
        ├── feedback01.md               # External audit 1
        ├── feedback02.md               # External audit 2
        ├── feedback03.md               # External audit 3
        └── feedback04.md               # External audit 4
```

### 1.4 Code Standards & Practices

**Design Patterns:**

| Pattern | Location | Purpose |
|---------|----------|---------|
| **State Pattern** | Addendum A (`RegimeClassifierState`) | Regime persistence, hysteresis |
| **Strategy Pattern** | Addendum D (Assessors) | Different risk assessment algorithms |
| **Observer Pattern** | Addendum E (`SystemHealthMonitor`) | Health monitoring |
| **Factory Pattern** | Addendum C (`BrokerAdapter`) | Pluggable broker connectors |
| **Registry Pattern** | Core OS (`REFRESH_CONFIGS`) | Configuration-driven data sources |
| **Decorator Pattern** | Addendum B (`@with_retry`) | Retry logic for API calls |

**Coding Standards:**

```python
# 1. UTC-ONLY time handling
def utc_now() -> datetime:
    """Get current time in UTC. Use this throughout the system."""
    return datetime.now(timezone.utc)

# 2. Enum-based categorization
class RiskCategory(Enum):
    CATALYST_RISK = "catalyst_risk"
    SOLVENCY_RISK = "solvency_risk"
    # ... all 9 categories

# 3. Dataclass for value objects
@dataclass
class Position:
    ticker: str
    quantity: float
    avg_cost: float
    # ... with computed properties

# 4. Type hints throughout
def compute_composite_score(
    category_scores: Dict[RiskCategory, float],
    weights: Dict[RiskCategory, float] = None,
    overlay_notches: float = 0.0
) -> Dict:

# 5. Defensive score capping
def verify_and_cap_score(score: float, source: str = "unknown") -> float:
    if score < 0:
        print(f"WARNING: Negative score {score} from {source}, capping to 0")
        return 0.0
    if score > 100:
        print(f"WARNING: Score {score} from {source} exceeds 100, capping to 100")
        return 100.0
    return float(score)
```

**Configuration Philosophy:**

1. **Weights externalized:** `DEFAULT_WEIGHTS` dict for risk category weights
2. **Thresholds in configs:** `REFRESH_CONFIGS`, `REGIME_THRESHOLDS`
3. **Platform settings:** `PLATFORM_CONFIGS` for social media sources
4. **Staleness rules:** Per-source refresh intervals and penalties

**Golden Rules (Non-Negotiable):**

```python
# From Mine Detector OS

GOLDEN_RULES = {
    1: "Composite score MUST include adjusted_score (with overlay + staleness)",
    2: "Score >= 86 is a HARD BLOCK for execution (CRITICAL threshold)",
    3: "RegimeClassifierState MUST be persistent across calls",
    4: "staleness_penalty comes from Addendum E's StalenessChecker",
    5: "overlay_points = overlay_notches * 10 (ALWAYS)"
}
```

### 1.5 Bundle Integrity Verification

```python
BUNDLE_VERSION = "2026-01-30-r9"

BUNDLE_FILES = [
    "mine-detector-os.md",
    "mine-detector-addendum-a-ml-classification.md",
    "mine-detector-addendum-b-social-sentiment.md",
    "mine-detector-addendum-c-brokerage.md",
    "mine-detector-addendum-d-adr-smallcap.md",
    "mine-detector-addendum-e-maintenance-operations.md"
]

def verify_bundle_integrity(bundle_dir: str) -> Dict:
    """Verify all files exist with matching versions."""
    # Checks each file for version string and computes hash
```

---

## 2. Data Collection & Monitoring

### 2.1 Macro Operating System Data Sources

The Macro OS organizes 150+ indicators across 31 categories (0-30) in a four-quadrant model:

#### Quadrant Structure

| Quadrant | Update Frequency | Purpose | Categories |
|----------|------------------|---------|------------|
| **Frontline Monitoring** | Daily/Real-time | Live risk sensing | 0-10: Core, Equities, Internals, Rates, Volatility, Credit, FX, Commodities, Flows, Positioning, Options Micro |
| **Deep Diagnostics** | Daily | Stress detection | 11-17: Funding Stress, Liquidity, Treasury Supply, Swaps, Functioning, Correlation, Systematic |
| **Fundamental Drivers** | Weekly/Monthly | "Why" context | 18-24: Event Risk, Real Estate, Crypto, Geopolitical, Sentiment, Tech/Capex, Labor |
| **Structural Forces** | Monthly/Quarterly | Regime backdrop | 25-30: Growth, Inflation, Profits, Fiscal, Global Anchors |

#### Category 0: Core Dashboard (14 Vital Signs)

| Indicator | Source | Frequency | Purpose |
|-----------|--------|-----------|---------|
| `sp500_close` | Yahoo Finance | Daily | US large-cap health |
| `qqq_close` | Yahoo Finance | Daily | Tech/growth proxy |
| `iwm_close` | Yahoo Finance | Daily | Small-cap/domestic |
| `vix_close` | Yahoo Finance | Daily | Implied volatility |
| `move_index` | ICE/Proxy | Daily | Bond volatility |
| `ust_3m_yield` | FRED | Daily | Short-term rates |
| `ust_2y_yield` | FRED | Daily | Fed expectations |
| `ust_10y_yield` | FRED | Daily | Long-term rates |
| `curve_10y_minus_2y` | Derived | Daily | Yield curve shape |
| `tips_10y_real_yield` | FRED | Daily | Inflation-adjusted rates |
| `hy_oas_spread` | FRED | Daily | Credit stress |
| `dxy_index` | Yahoo Finance | Daily | Dollar strength |
| `wti_close` | Yahoo Finance | Daily | Energy/inflation |

#### Data Source Registry

| Source | Data Types | API/Method | Rate Limit |
|--------|------------|------------|------------|
| **FRED** | Treasury yields, credit spreads, M2, real yields | REST API | 120/min |
| **Yahoo Finance** | Equities, VIX, DXY, commodities, ETFs | yfinance library | Generous |
| **ICE/Bloomberg** | MOVE Index, CDX indices | Terminal/Proxy | N/A |
| **CME** | Futures positioning (COT) | Weekly file | N/A |
| **AAII** | Sentiment survey | Weekly | N/A |
| **DeFiLlama** | Protocol TVL, yields | REST API | 60/min |
| **Glassnode** | On-chain metrics | REST API | Tier-based |

### 2.2 Mine Detector Data Sources

Mine Detector tracks 17+ data source types across TradFi and Web3:

#### Price & Derivatives Data

| Source | Refresh | Staleness Threshold | Penalty | Critical? |
|--------|---------|---------------------|---------|-----------|
| `PRICE_DATA` (equities) | 1 min | 5 min | +10 pts | ✅ Yes |
| `CRYPTO_PRICE` | 15 sec | 1 min | +15 pts | ✅ Yes |
| `OPTIONS_CHAIN` | 15 min | 60 min | +5 pts | No |
| `PERP_FUNDING` | 60 min | 180 min | +5 pts | No |

#### Positioning Data

| Source | Refresh | Staleness Threshold | Penalty | Critical? |
|--------|---------|---------------------|---------|-----------|
| `SHORT_INTEREST` | Daily | 48 hours | +3 pts | No |
| `INSTITUTIONAL_13F` | Weekly | 2 weeks | +2 pts | No |
| `CREDIT_SPREADS` | 60 min | 240 min | +4 pts | No |

#### Social Sentiment Data

| Source | Refresh | Staleness Threshold | Penalty | Critical? |
|--------|---------|---------------------|---------|-----------|
| `TWITTER_SENTIMENT` | 30 min | 120 min | +2 pts | No |
| `REDDIT_SENTIMENT` | 60 min | 180 min | +2 pts | No |
| `STOCKTWITS_SENTIMENT` | 30 min | 120 min | +2 pts | No |
| `DISCORD_SENTIMENT` | 15 min | 60 min | +1 pt | No |
| `TELEGRAM_SENTIMENT` | 15 min | 60 min | +1 pt | No |

#### Web3 Data

| Source | Refresh | Staleness Threshold | Penalty | Critical? |
|--------|---------|---------------------|---------|-----------|
| `TOKEN_UNLOCKS` | 6 hours | 24 hours | +8 pts | ✅ Yes |
| `PROTOCOL_TVL` | 60 min | 360 min | +5 pts | No |
| `CEX_FLOWS` | 60 min | 240 min | +4 pts | No |

#### Calendar & Governance

| Source | Refresh | Staleness Threshold | Penalty | Critical? |
|--------|---------|---------------------|---------|-----------|
| `EARNINGS_CALENDAR` | Daily | 48 hours | +3 pts | No |
| `INSIDER_TRANSACTIONS` | Daily | 72 hours | +2 pts | No |
| `SEC_FILINGS` | Daily | 48 hours | +3 pts | No |

### 2.3 Update Frequency Guidance

#### Macro OS Recommended Schedule

| Data Type | Update Frequency | Rationale |
|-----------|------------------|-----------|
| **Core Dashboard (Category 0)** | Every 30 seconds scan | Vital signs monitoring |
| **Frontline Monitoring** | Every 60 seconds | Live risk detection |
| **Deep Diagnostics** | Every 5 minutes | Stress confirmation |
| **Fundamental Drivers** | Daily/Weekly | Slow-moving context |
| **Structural Forces** | Weekly/Monthly | Regime backdrop |

#### Mine Detector Recommended Schedule

| Operation | Frequency | Notes |
|-----------|-----------|-------|
| **Composite Score Calculation** | On-demand or every 5 min | Per security |
| **Social Sentiment Refresh** | Every 30 min | Rate limits apply |
| **Portfolio Risk Scan** | Every 5 min during market hours | All positions |
| **Token Unlock Alerts** | Every 6 hours | Calendar-based |
| **Regime Classification** | Every 15 min | Via Addendum A |
| **Staleness Check** | Before every score | Penalty calculation |
| **Calibration Update** | Daily (post-market) | Outcome tracking |

---

## 3. Market Indicators & User Value

### 3.1 Macro OS: The 7 Canonical Patterns

The Macro OS reduces the complexity of global markets into 7 recognizable regimes:

| Pattern | Name | Signature | First Check | User Value |
|---------|------|-----------|-------------|------------|
| **0** | Goldilocks | Low VIX (<15), tight HY spreads, positive flows | Liquidity → Flows → Credit | "Green light for risk" |
| **1** | Liquidity Crisis | FRA-OIS spike, DXY surge, funding stress | Funding → Market Functioning → FX | "Cash is king - de-risk NOW" |
| **2** | Growth Scare | PMIs roll, earnings revisions negative | Growth → Profits → Credit | "Rotate to defensives" |
| **3** | Inflation Shock | Breakevens spike, commodities up | Inflation → Real Rates → Commodities | "Duration is toxic" |
| **4** | Positioning Unwind | VIX spike but HY flat, gamma negative | Options Micro → Positioning → Systematic | "Technical, not fundamental" |
| **5** | Fiscal Tantrum | Auction tails, term premium rises | Treasury Supply → Fiscal → Rates | "Long-end pressure building" |
| **6** | Credit Event | HY/IG widening, bank CDS up, equities calm | Credit → Funding → Market Functioning | "Silent leak - front-run before panic" |

#### Pattern Validation Matrix

```
                    INFLATION   GROWTH    CREDIT    FX STRENGTH
PATTERN 0 (Gold)    Stable      Positive  Tight     Neutral
PATTERN 1 (Liq)     N/A         Mixed     Widening  USD Strong++
PATTERN 2 (Growth)  Falling     Negative  Widening  USD Weak
PATTERN 3 (Infl)    Spiking     Mixed     Widening  USD Strong
PATTERN 4 (Pos)     N/A         N/A       Stable    N/A
PATTERN 5 (Fiscal)  Rising      Mixed     Widening  Mixed
PATTERN 6 (Credit)  N/A         Negative  Widening  USD Strong
```

### 3.2 Mine Detector: The 9 Risk Categories

| # | Category | What It Detects | Key Indicators | User Value |
|---|----------|-----------------|----------------|------------|
| 1 | **Catalyst Risk** | Upcoming binary events | Earnings dates, FDA rulings, legal cases | "Know your calendar" |
| 2 | **Solvency Risk** | Bankruptcy probability | Altman-Z, debt ratios, covenant status | "Avoid blow-ups" |
| 3 | **Crowding Risk** | Positioning extremes | Short interest, borrow rates, 13F concentration | "Don't be the last one out" |
| 4 | **Liquidity Flow Risk** | Forced selling | ETF rebalance, index changes, margin calls | "Anticipate mechanical selling" |
| 5 | **Momentum Risk** | Technical breakdowns | Price vs MA, RSI extremes, volume | "Trend is your friend (until it isn't)" |
| 6 | **Governance Risk** | Management red flags | Insider sales, auditor changes, restatements | "Follow the smart money" |
| 7 | **Refinancing Risk** | Debt maturity walls | Bond schedules, revolver availability | "Maturity walls kill" |
| 8 | **Dilution Risk** | Equity overhang | Shelf registrations, ATM programs, warrants | "Know your share count" |
| 9 | **Event Risk** | Binary outcomes + social anomalies | M&A spreads, litigation, sentiment spikes | "Unknown unknowns" |

### 3.3 Score Interpretation & Actionable Guidance

| Score Range | Risk Level | Recommended Action | Position Limit |
|-------------|------------|--------------------|----------------|
| **0-25** | LOW | Normal sizing allowed | 100% |
| **26-50** | MODERATE | Tighten stops, reduce if scaling | 100% |
| **51-70** | ELEVATED | Reduce position by 50%, set hard stops | 75% |
| **71-85** | HIGH | Exit or hedge immediately | 50% |
| **86-100** | **CRITICAL** | **AVOID ENTIRELY - HARD BLOCK** | 0% |

### 3.4 Structural Overlay Impact (ADR/Small-Cap/Web3)

| Security Type | Overlay Notches | Overlay Points | Position Limit |
|---------------|-----------------|----------------|----------------|
| US Large/Mid-Cap | 0.0 | 0 | 100% normal |
| US Small-Cap | 0.3-0.8 | 3-8 | 100% normal |
| ADR Developed | 0.2-0.5 | 2-5 | 100% normal |
| ADR Emerging | 0.5-1.0 | 5-10 | 75% normal |
| **ADR China** | 0.8-2.0 | 8-20 | 25-50% normal |
| ADR Russia | 2.5 | 25 | **AVOID** |
| Web3 Tokenized | 0.5-2.5 | 5-25 | Variable |

---

## 4. How Each Layer Works

### 4.1 Macro Operating System Layers

#### Layer 1: Data Ingestion & Normalization

**Input:** Raw market data from FRED, Yahoo, Bloomberg terminals
**Process:**
1. Fetch current values for all 150+ indicators
2. Calculate standard transforms:
   - **Δ1d, Δ5d, Δ20d** (absolute changes)
   - **% change** (relative changes)
   - **Rolling percentile** (1-year and 5-year lookbacks)
   - **Z-score** (standardized deviation from mean)

**Output:** Normalized indicator matrix with transforms

```python
DEFAULT_TRANSFORMS = ['delta_1d', 'delta_1w', 'delta_1m', 'pct_change', 
                      'percentile_1y', 'percentile_5y', 'z_score']
```

#### Layer 2: Change Detection Matrix

**Input:** Normalized indicator matrix
**Process:**
1. For each indicator, compute multi-horizon changes:
   - **Acceleration:** Is Δ1d > Δ5d? (momentum building)
   - **Divergence:** Is Δ1d opposite to Δ20d? (potential reversal)
   - **Extreme:** Is z-score > 2 or percentile > 95%?

**Output:** Change detection flags per indicator

```
CHANGE DETECTION MATRIX (Example)
---------------------------------
Indicator       Δ1d    Δ5d    Δ20d   Accel?  Diverge?  Extreme?
vix_close       +2.5   +1.8   -0.5   YES     YES       NO
hy_oas_spread   +15    +10    +25    YES     NO        YES
dxy_index       +0.3   +0.8   +1.2   NO      NO        NO
```

#### Layer 3: Pattern Recognition

**Input:** Change detection flags + current levels
**Process:**
1. Check signature conditions for each of 7 patterns
2. Calculate pattern confidence (0-100%)
3. Validate against contradictory signals

**Pattern 1 (Liquidity Crisis) Detection Logic:**
```python
def detect_liquidity_crisis(data: Dict) -> Dict:
    signals = []
    confidence = 0
    
    # Funding stress leads
    if data['fra_ois_spread_z_score'] > 2:
        signals.append('FRA-OIS elevated')
        confidence += 25
    
    # DXY strength
    if data['dxy_percentile_1y'] > 90:
        signals.append('USD strength extreme')
        confidence += 20
    
    # Cross-currency basis
    if data['eurusd_xccy_basis'] < -50:
        signals.append('Cross-currency stress')
        confidence += 20
    
    # Credit widening (lagging confirmation)
    if data['hy_oas_spread_z_score'] > 1.5:
        signals.append('Credit confirming')
        confidence += 15
    
    return {
        'pattern': 'LIQUIDITY_CRISIS',
        'confidence': min(100, confidence),
        'signals': signals,
        'first_check': ['funding_stress', 'market_functioning', 'fx']
    }
```

#### Layer 4: Validation & Cross-Check

**Input:** Pattern detection results
**Process:**
1. Apply validation rules to prevent misdiagnosis
2. Check for contradictory patterns

**Validation Rules:**

| Rule | Check | Action |
|------|-------|--------|
| Inflation vs Growth | Breakevens up + PMIs down | Flag "Stagflation" |
| USD Strength Diagnosis | DXY up + Why? | Check funding (Pattern 1) vs carry (Pattern 3) |
| Credit-Equity Divergence | HY wide + SPX flat > 5 days | Escalate (Pattern 6 likely) |
| Fiscal vs Growth | Yields up + PMIs up | Distinguish Pattern 5 vs Pattern 3 |

#### Layer 5: Regime Output & Transition Matrix

**Input:** Validated pattern with confidence
**Process:**
1. Output current regime classification
2. Check transition probability matrix
3. Identify leading indicators for regime shift

**Transition Matrix (Simplified):**
```
FROM \ TO          Pattern 0  Pattern 1  Pattern 2  Pattern 3
Pattern 0 (Gold)   -          Watch HY   Watch PMI  Watch BEI
Pattern 1 (Liq)    VIX<20     -          PMI<48     BEI>2.8%
Pattern 2 (Growth) VIX<15     FRA-OIS    -          CPI>0.3%
Pattern 3 (Infl)   CPI<0.2%   FRA-OIS    PMI<48     -
```

### 4.2 Mine Detector OS Layers

#### Core OS Layer: 9-Category Risk Assessment

**Input:** Security identifier (ticker) + market data
**Process:**
1. For each of 9 risk categories, compute score (0-100)
2. Apply category weights
3. Aggregate into composite score

**Default Weights:**
```python
DEFAULT_WEIGHTS = {
    RiskCategory.CATALYST_RISK: 0.15,
    RiskCategory.SOLVENCY_RISK: 0.15,
    RiskCategory.CROWDING_RISK: 0.12,
    RiskCategory.LIQUIDITY_FLOW_RISK: 0.10,
    RiskCategory.MOMENTUM_RISK: 0.10,
    RiskCategory.GOVERNANCE_RISK: 0.12,
    RiskCategory.REFINANCING_RISK: 0.10,
    RiskCategory.DILUTION_RISK: 0.08,
    RiskCategory.EVENT_RISK: 0.08
}
# Weights sum to 1.00
```

**Penalty Combination Method:**
```python
def combine_penalties(penalties: List[float], method: str = "max_plus_sqrt") -> float:
    """
    Combine multiple penalties for the same category.
    
    Methods:
        - 'sum': Simple sum (can exceed 100, requires capping)
        - 'max': Take maximum only (ignores smaller penalties)
        - 'max_plus_sqrt': Max + sqrt(sum of others) -- RECOMMENDED
    
    Example with penalties [30, 20, 10]:
        - sum: 60
        - max: 30
        - max_plus_sqrt: 30 + sqrt(20+10) = 30 + 5.48 = 35.48
    """
```

#### Addendum A: ML Classification Layer

**Input:** Feature vector (VIX, credit spreads, SPX vs 200-DMA, flows, sentiment)
**Process:**
1. Impute missing values using regime-conditional medians
2. Compute raw scores for each regime (RISK_ON, RISK_OFF, TRANSITION)
3. Normalize via softmax to get probabilities (sum = 1.0)
4. Apply regime bias (tenure-based hysteresis)
5. Select regime with confidence threshold

**Feature Ranges:**
```python
FEATURE_RANGES = {
    'vix_level': (10, 80),
    'vix_percentile_1y': (0, 100),
    'hy_spread': (250, 1500),
    'spx_vs_200dma': (-30, 30),
    'equity_fund_flows_4w': (-50, 50),
    'put_call_ratio': (0.5, 1.5),
    'aaii_bull_bear_spread': (-40, 40)
}
```

**Regime Bias (Hysteresis):**
```python
def get_regime_bias(tenure_days: int) -> float:
    if tenure_days < 3:
        return 0.0
    elif tenure_days < 7:
        return 0.05
    elif tenure_days < 14:
        return 0.10
    elif tenure_days < 30:
        return 0.12
    else:
        return 0.15  # Maximum bias toward current regime
```

**Regime-Adjusted Thresholds:**
```python
REGIME_THRESHOLDS = {
    'RISK_OFF': {'elevated': 40, 'high': 60, 'critical': 75},
    'RISK_ON': {'elevated': 55, 'high': 75, 'critical': 90},
    'TRANSITION': {'elevated': 50, 'high': 70, 'critical': 85}
}
```

#### Addendum B: Social Sentiment Layer

**Input:** Ticker symbol + time window
**Process:**
1. Fetch posts from 5 platforms (Twitter, Reddit, StockTwits, Discord, Telegram)
2. Filter bot accounts (probability > 0.7 = filtered)
3. Analyze sentiment per post (-1 to +1)
4. Weight by platform importance
5. Map to Event Risk contribution

**Bot Detection Signals:**
```python
BOT_SIGNALS = {
    'new_account': {'threshold_days': 30, 'weight': 0.15},
    'high_frequency': {'threshold_posts_per_day': 50, 'weight': 0.20},
    'low_engagement_ratio': {'threshold': 0.01, 'weight': 0.15},
    'repetitive_content': {'threshold_similarity': 0.8, 'weight': 0.20},
    'suspicious_timing': {'threshold_variance': 0.1, 'weight': 0.15},
    'coordinated_behavior': {'threshold_correlation': 0.9, 'weight': 0.15}
}
```

**Platform Weights:**
```python
PLATFORM_WEIGHTS = {
    Platform.TWITTER: 0.35,
    Platform.REDDIT: 0.30,
    Platform.STOCKTWITS: 0.25,
    Platform.DISCORD: 0.05,
    Platform.TELEGRAM: 0.05
}
```

**Sentiment to Event Risk Mapping:**
```python
def map_sentiment_to_event_risk(sentiment_score: float,  # -100 to +100
                                 confidence: str,
                                 volume: int,
                                 volume_change_pct: float) -> Dict:
    # Extreme bullishness (>70) = elevated risk (crowded trade)
    # Extreme bearishness (<-70) = elevated risk (information leakage)
    # Volume spike (>200%) = elevated risk (unusual activity)
```

#### Addendum C: Brokerage Integration Layer

**Input:** Portfolio positions + Mine Detector scores
**Process:**
1. Sync positions across brokers (normalize to Position dataclass)
2. Check market halt status before orders
3. Enforce confirmation requirements
4. Apply hard block at score >= 86

**Contract Multipliers:**
```python
CONTRACT_MULTIPLIERS = {
    'equity': 1.0,
    'option': 100.0,
    'mini_option': 10.0,
    'es_future': 50.0,    # E-mini S&P 500
    'mes_future': 5.0,    # Micro E-mini
    'btc_future': 5.0,    # CME BTC
    'crypto': 1.0,
}
```

**Confirmation Enforcement:**
```python
SCORE_THRESHOLDS = {
    'warn': 50,      # Log warning
    'confirm': 70,   # Require user confirmation
    'block': 86,     # HARD BLOCK (CRITICAL threshold)
}

ALWAYS_CONFIRM = [
    'close_all_positions',
    'liquidate_portfolio',
    'increase_position_high_risk',
    'new_position_critical_risk',
]
```

#### Addendum D: Structural Overlay Layer

**Input:** Security classification + geopolitical/liquidity factors
**Process:**
1. Classify security type (US Large-Cap, ADR China, Web3, etc.)
2. Compute base overlay notches
3. Add stacking adjustments (VIE, HFCAA, sector, geopolitical)
4. Convert notches to points (×10)

**China ADR Stacking Example:**
```python
def assess_china_adr(risk: ChinaADRRisk) -> Dict:
    base = 0.8  # Base notches for ADR_CHINA
    additional = 0.0
    
    if risk.has_vie_structure:
        additional += 0.3  # No direct ownership
    
    if risk.hfcaa_status == 'non_compliant':
        additional += 0.5  # Delisting risk
    elif risk.hfcaa_status == 'at_risk':
        additional += 0.25
    
    if risk.sector in SENSITIVE_SECTORS:
        additional += 0.2  # Tech, semis, AI, etc.
    
    additional += TENSION_ADJUSTMENTS.get(risk.geopolitical_tension, 0.1)
    
    total = base + min(1.2, additional)  # Cap additional at 1.2
    return {
        'total_notches': total,  # Max 2.0
        'total_points': total * 10  # Max 20
    }
```

**Web3 Risk Assessment:**
```python
CHAIN_RISK_NOTCHES = {
    'ethereum': 0.0,
    'arbitrum': 0.05,
    'optimism': 0.05,
    'base': 0.08,
    'polygon': 0.1,
    'solana': 0.15,
    'bsc': 0.2,
}
```

**Web3 Metric Translation to TradFi Categories:**
```python
WEB3_TO_TRADFI = {
    'token_unlocks': RiskCategory.CATALYST_RISK,
    'protocol_tvl': RiskCategory.SOLVENCY_RISK,
    'perp_funding': RiskCategory.CROWDING_RISK,
    'cex_flows': RiskCategory.LIQUIDITY_FLOW_RISK,
    'multisig_config': RiskCategory.GOVERNANCE_RISK,
    'emission_schedule': RiskCategory.DILUTION_RISK,
    'hack_history': RiskCategory.EVENT_RISK,
}
```

#### Addendum E: Maintenance & Operations Layer

**Input:** System state + data freshness timestamps
**Process:**
1. Check staleness of all data sources
2. Calculate total staleness penalty
3. Track calibration outcomes
4. Evaluate retraining triggers

**Staleness Penalty Calculation:**
```python
def get_total_staleness_penalty(self) -> float:
    """Sum of penalties from all stale sources."""
    return sum(f.staleness_penalty for f in self.check_all().values())
```

**Retraining Triggers:**
```python
RETRAINING_TRIGGERS = {
    'accuracy_drop': {'threshold': 0.85, 'triggered_when': 'accuracy < 85%'},
    'time_elapsed': {'threshold': 90, 'triggered_when': 'days since training > 90'},
    'new_samples': {'threshold': 500, 'triggered_when': 'samples accumulated >= 500'},
    'regime_volatility': {'threshold': 10, 'triggered_when': 'regime changes in 30d >= 10'}
}
```

---

## 5. How Mine Detector Works End-to-End

### 5.1 Complete Scoring Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT: Ticker "XYZ"                          │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Data Collection                                             │
│ • Price data (1-min staleness check)                               │
│ • Options chain (15-min staleness)                                 │
│ • Short interest (daily)                                           │
│ • Social sentiment (30-min)                                        │
│ • Earnings calendar (daily)                                        │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Staleness Check (Addendum E)                               │
│ • Check each source against threshold                              │
│ • Calculate staleness_penalty = Σ(stale_source_penalties)          │
│ • If CRITICAL source stale → Block scoring                         │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Regime Classification (Addendum A)                         │
│ • Get current regime (RISK_ON, RISK_OFF, TRANSITION)               │
│ • Adjust category weights based on regime                          │
│ • Get regime-adjusted thresholds                                   │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: Category Scoring (Core OS)                                 │
│ • Catalyst Risk: Days to earnings, FDA date, legal ruling          │
│ • Solvency Risk: Altman-Z, debt ratios, covenant proximity         │
│ • Crowding Risk: Short interest %, borrow rate, 13F concentration  │
│ • Liquidity Flow: ETF rebalance impact, index membership           │
│ • Momentum Risk: Price vs 50/200 DMA, RSI, volume trend            │
│ • Governance Risk: Insider selling, auditor changes, restatements  │
│ • Refinancing Risk: Debt maturity schedule, revolver availability  │
│ • Dilution Risk: Shelf registration, ATM program, warrant overhang │
│ • Event Risk: M&A spread, litigation, social sentiment (Addendum B)│
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 5: Security Classification (Addendum D)                       │
│ • Classify: US Large-Cap, ADR China, Web3, etc.                    │
│ • Calculate overlay_notches (0.0 - 2.5)                            │
│ • Convert: overlay_points = overlay_notches × 10                   │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 6: Composite Score Calculation (Core OS)                      │
│                                                                     │
│   composite_score = Σ(category_score × adjusted_weight)            │
│                                                                     │
│   adjusted_score = composite_score                                 │
│                  + overlay_points (0-25)                           │
│                  + staleness_penalty (0-50+)                       │
│                                                                     │
│   adjusted_score = min(100, max(0, adjusted_score))                │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 7: Risk Level Assignment                                      │
│                                                                     │
│   if adjusted_score >= 86:  → CRITICAL (HARD BLOCK)                │
│   if adjusted_score >= 71:  → HIGH (Exit/Hedge)                    │
│   if adjusted_score >= 51:  → ELEVATED (Reduce 50%)                │
│   if adjusted_score >= 26:  → MODERATE (Tighten stops)             │
│   else:                     → LOW (Normal sizing)                  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ OUTPUT: Risk Assessment                                             │
│ {                                                                   │
│   'composite_score': 67,                                           │
│   'adjusted_score': 72,                                            │
│   'overlay_notches': 0.5,                                          │
│   'overlay_points': 5,                                             │
│   'staleness_penalty': 0,                                          │
│   'risk_level': 'HIGH',                                            │
│   'dominant_risks': ['crowding_risk', 'catalyst_risk', 'event_risk']│
│   'recommendation': 'Exit or hedge immediately'                    │
│ }                                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Example Calculation: China ADR Tech Stock

**Security:** BABA (Alibaba - China ADR, Technology Sector)

**Step 1: Category Scores**
```
Catalyst Risk:      45 (no earnings for 6 weeks)
Solvency Risk:      35 (reasonable balance sheet)
Crowding Risk:      55 (moderate short interest)
Liquidity Flow:     40 (no imminent ETF rebalance)
Momentum Risk:      60 (below 200-DMA)
Governance Risk:    50 (state influence concerns)
Refinancing Risk:   30 (manageable debt)
Dilution Risk:      25 (no ATM program)
Event Risk:         65 (regulatory uncertainty)
```

**Step 2: Regime-Adjusted Weights (Regime = RISK_OFF)**
```
RISK_OFF multipliers:
  Solvency:    1.3× (more important in stress)
  Refinancing: 1.3× (more important in stress)
  Liquidity:   1.2× (more important in stress)
  Momentum:    0.8× (less important in stress)

After renormalization, weights shift toward credit/liquidity risks
```

**Step 3: Weighted Composite**
```
composite_score = (45 × 0.14) + (35 × 0.18) + (55 × 0.11) + ...
                = 46.5 (rounded)
```

**Step 4: Structural Overlay (China ADR)**
```
Base (ADR_CHINA):           +0.80 notches
VIE structure:              +0.30 notches
HFCAA at-risk:             +0.25 notches
Sensitive sector (Tech):    +0.20 notches
Geopolitical (moderate):    +0.10 notches
                            ---------------
Total overlay:              1.65 notches → 16.5 points
```

**Step 5: Adjusted Score**
```
adjusted_score = 46.5 + 16.5 + 0 (no staleness penalty)
               = 63.0

Risk Level: ELEVATED
Recommendation: Reduce position by 50%, set hard stops
Position Limit: 50% of normal (due to 1.65 notches overlay)
```

---

## 6. Data Storage & Transformation

### 6.1 Raw Data → Useful Information Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                      RAW DATA LAYER                                 │
│                                                                     │
│  • API responses (JSON)                                            │
│  • CSV files (historical)                                          │
│  • Real-time feeds (websockets)                                    │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               NORMALIZATION & VALIDATION LAYER                      │
│                                                                     │
│  • Timestamp → UTC conversion                                      │
│  • Schema validation                                               │
│  • Missing data detection                                          │
│  • Staleness flagging                                              │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               SYNCHRONIZATION LAYER                                 │
│                                                                     │
│  DataSynchronizer ensures all data in a scoring run                │
│  is from the same 5-minute window (MAX_SNAPSHOT_SPREAD)            │
│                                                                     │
│  • begin_snapshot() → sets reference time                          │
│  • add_data(source, value, timestamp) → accepts or rejects         │
│  • get_snapshot() → returns synchronized data bundle               │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               TRANSFORMATION LAYER                                  │
│                                                                     │
│  Macro OS Transforms:                                              │
│  • delta_1d = value_today - value_yesterday                        │
│  • pct_change = (delta_1d / value_yesterday) × 100                 │
│  • percentile_1y = rank / count × 100                              │
│  • z_score = (value - mean_1y) / std_1y                            │
│                                                                     │
│  Mine Detector Transforms:                                         │
│  • category_score = category_specific_formula(inputs)              │
│  • overlay_points = overlay_notches × 10                           │
│  • adjusted_score = composite + overlay + staleness                │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               STATE MANAGEMENT LAYER                                │
│                                                                     │
│  Persistent State Objects:                                         │
│  • RegimeClassifierState (regime, tenure, history)                 │
│  • StalenessChecker (last_updates per source)                      │
│  • CalibrationTracker (outcomes, metrics)                          │
│  • TokenUnlockTracker (upcoming unlocks)                           │
│                                                                     │
│  CRITICAL: These MUST persist across calls                         │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               OUTPUT LAYER                                          │
│                                                                     │
│  • Risk assessments (JSON/Dict)                                    │
│  • Dashboard outputs (formatted text)                              │
│  • Alerts (priority-ordered)                                       │
│  • Calibration records (for accuracy tracking)                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Data Freshness Tracking

**Two Timestamp Concepts:**

| Concept | Definition | Used By | Example |
|---------|------------|---------|---------|
| **data_origin_timestamp** | When the underlying data was created | StalenessChecker | Short interest published 2 days ago |
| **fetch_timestamp** | When we retrieved the data | DataSynchronizer | Fetched 30 seconds ago |

**A data point can be:**
- Fresh for staleness (origin: 2 days ago, within 48h threshold) AND
- Valid for synchronization (fetched: 30 seconds ago, within 5-min spread)

### 6.3 Historical Data for Calibration

**Blowup Definition:**
```python
@dataclass
class BlowupDefinition:
    vol_ratio_threshold: float = 2.0      # Realized vol >= 2× historical
    single_day_loss_threshold: float = 5.0 # Single-session loss >= 5%
    gap_down_threshold: float = 15.0       # Gap down >= 15%
    lookback_days: int = 30                # Within 30 days of HIGH score
```

**Calibration Outcome Tracking:**
```python
@dataclass
class CalibrationOutcome:
    ticker: str
    flag_date: datetime
    flag_score: float
    
    max_drawdown: float
    max_single_day_loss: float
    max_gap_down: float
    realized_vol_ratio: float
    had_trading_halt: bool
    had_credit_event: bool
    
    def get_label(self) -> str:
        # Returns: TRUE_POSITIVE, FALSE_POSITIVE, TRUE_NEGATIVE, FALSE_NEGATIVE
```

---

## 7. Triggers & Alert System

### 7.1 Macro OS Triggers

#### Primary Triggers (z-score > 2 or percentile > 95%)

| Indicator | Trigger Condition | Pattern Implication |
|-----------|-------------------|---------------------|
| VIX | z-score > 2 | Pattern 1 or 4 |
| HY OAS Spread | percentile > 95% | Pattern 1, 2, or 6 |
| FRA-OIS Spread | > 30 bps | Pattern 1 (Liquidity Crisis) |
| 10Y-2Y Curve | Inversion deepens | Pattern 2 or 5 |
| DXY | z-score > 2 | Pattern 1 or 3 |
| Breakeven Inflation | > 3% | Pattern 3 (Inflation Shock) |

#### RED FLAG Paired Conditions

| Condition 1 | Condition 2 | Alert Level | Action |
|-------------|-------------|-------------|--------|
| VIX > 25 | HY spread widening > 50 bps/week | RED FLAG | De-risk immediately |
| FRA-OIS > 50 bps | DXY > 2 z-score | RED FLAG | Liquidity crisis confirmed |
| PMI < 48 | Earnings revisions < -10% | RED FLAG | Growth scare confirmed |
| Auction tail > 3 bps | 30Y yield up > 20 bps/week | RED FLAG | Fiscal tantrum building |

### 7.2 Mine Detector Triggers

#### Score-Based Triggers

| Trigger | Condition | Action | Can Override? |
|---------|-----------|--------|---------------|
| **Warning** | Score 50-69 | Log warning, continue | Yes |
| **Confirmation Required** | Score 70-85 | Require user confirmation | Yes |
| **Hard Block** | Score >= 86 | Block execution | **NO** |

#### Category-Specific Alerts

| Category | Alert Condition | Severity | Example |
|----------|-----------------|----------|---------|
| Catalyst Risk | Earnings in < 7 days + IV skew elevated | HIGH | "Earnings volatility approaching" |
| Crowding Risk | Short interest > 25% + utilization > 90% | CRITICAL | "Squeeze or collapse setup" |
| Solvency Risk | Altman-Z < 1.8 | HIGH | "Bankruptcy zone" |
| Governance Risk | Insider selling > $10M in 30 days | HIGH | "Smart money exiting" |
| Event Risk | Social volume > 3× normal + sentiment extreme | MEDIUM | "Unusual social activity" |

#### Token Unlock Alerts (Web3)

| Condition | Days Until | % of Supply | Severity |
|-----------|------------|-------------|----------|
| Large unlock approaching | <= 7 | >= 5% | CRITICAL |
| Significant unlock | <= 7 | >= 3% | HIGH |
| Notable unlock | <= 14 | >= 2% | MEDIUM |

### 7.3 System Health Triggers (Addendum E)

| Trigger | Condition | Effect |
|---------|-----------|--------|
| **Critical Data Stale** | PRICE_DATA > 5 min stale | Block scoring |
| **Crypto Price Stale** | CRYPTO_PRICE > 1 min stale | Block crypto scoring |
| **Token Unlocks Stale** | > 24 hours stale | +8 points penalty |
| **All Sources Healthy** | No staleness | Normal operation |

### 7.4 Market Halt Detection

```python
class MarketStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PRE_MARKET = "pre_market"
    AFTER_HOURS = "after_hours"
    HALTED = "halted"       # Trading halt (T1, T2, etc.)
    SUSPENDED = "suspended"  # Longer suspension

HALT_CODES = {
    'T1': 'News pending',
    'T2': 'News released',
    'T5': 'Price movement (10% in 5 min)',
    'T6': 'Extraordinary market activity',
    'T12': 'Additional information requested',
    'LUDP': 'Limit up/down pause',
    'MWCB': 'Market-wide circuit breaker'
}
```

**Pre-Flight Check (Before Order Execution):**
```python
def execute_with_risk_check(order, risk_score, risk_details):
    # CHECK 1: Market halt status
    halt_info = check_trading_status(order.ticker)
    if halt_info.status in [HALTED, SUSPENDED]:
        return {'blocked': True, 'reason': f'Security halted: {halt_info.halt_code}'}
    
    # CHECK 2: Risk score threshold
    if risk_score >= 86:
        return {'blocked': True, 'reason': 'CRITICAL risk score'}
    
    # CHECK 3: Confirmation for high risk
    if risk_score >= 70:
        return {'requires_confirmation': True, 'confirmation_id': generate_id()}
    
    # PROCEED: Execute order
    return adapter.place_order(order)
```

---

## 8. Formulas & Calculations Reference

### 8.1 Macro OS Formulas

#### Standard Transforms

```python
# Absolute change
delta_1d = value_t - value_t_minus_1

# Percentage change
pct_change = (delta_1d / value_t_minus_1) * 100

# Rolling percentile (1-year lookback, ~252 trading days)
percentile_1y = (rank_in_252d_window / 252) * 100

# Z-score (1-year lookback)
z_score = (value - mean_252d) / std_252d
```

#### Derived Indicators

```python
# Yield curve spread
curve_10y_minus_2y = yield_10y - yield_2y

# Real yield (approximation)
real_yield_10y = nominal_yield_10y - breakeven_inflation_10y

# Credit stress ratio
credit_stress_ratio = hy_spread / ig_spread

# VIX term structure (contango/backwardation)
vix_term_structure = vix_spot - vix_3m

# Dollar funding stress
fra_ois_spread = libor_3m - ois_3m
```

#### Mag7 Market Cap Calculation

```python
def calculate_mag7_weight():
    mag7_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    
    mag7_mcap = sum(get_market_cap(t) for t in mag7_tickers)
    spx_mcap = get_index_market_cap('SPX')
    
    return (mag7_mcap / spx_mcap) * 100  # Percentage
```

### 8.2 Mine Detector Formulas

#### Composite Score

```python
def compute_composite_score(category_scores, weights, overlay_notches, staleness_penalty):
    # Step 1: Handle missing categories (renormalize weights)
    provided_categories = {k for k, v in category_scores.items() if v is not None}
    active_weights = {k: v for k, v in weights.items() if k in provided_categories}
    
    # Step 2: Check minimum coverage (40%)
    total_provided_weight = sum(weights.get(cat, 0) for cat in provided_categories)
    if total_provided_weight < 0.4:
        return {'warning': 'Insufficient category coverage'}
    
    # Step 3: Normalize weights
    total_weight = sum(active_weights.values())
    normalized_weights = {k: v/total_weight for k, v in active_weights.items()}
    
    # Step 4: Weighted sum
    contributions = {}
    for category, score in category_scores.items():
        if score is not None:
            capped_score = min(100, max(0, score))
            weight = normalized_weights.get(category, 0)
            contributions[category] = capped_score * weight
    
    composite = sum(contributions.values())
    
    # Step 5: Apply adjustments
    overlay_points = overlay_notches * 10.0
    adjusted = composite + overlay_points + staleness_penalty
    adjusted = min(100, max(0, adjusted))
    
    return {
        'composite_score': round(composite, 1),
        'adjusted_score': round(adjusted, 1),
        'overlay_points': round(overlay_points, 1),
        'staleness_penalty': round(staleness_penalty, 1)
    }
```

#### Softmax Probability Normalization (Regime Classification)

```python
def softmax_normalize(raw_scores, temperature=30.0):
    """
    Convert raw scores to proper probabilities.
    Result guaranteed to sum to 1.0.
    """
    max_score = max(raw_scores.values())
    exp_scores = {}
    
    for regime, score in raw_scores.items():
        exp_scores[regime] = math.exp((score - max_score) / temperature)
    
    total = sum(exp_scores.values())
    return {regime: exp_score / total for regime, exp_score in exp_scores.items()}
```

#### Web3 Funding Rate Annualization

```python
def crowding_risk_from_funding(perp_funding_rate_8h):
    """
    UNIT: perp_funding_rate_8h is in DECIMAL form (0.0001 = 0.01%)
    Annualization: rate × 3 periods/day × 365 days × 100 (to %)
    """
    funding_annual = abs(perp_funding_rate_8h) * 3 * 365 * 100
    
    if funding_annual > 100:  # >100% annualized
        return 90
    if funding_annual > 50:
        return 70
    if funding_annual > 20:
        return 45
    if funding_annual > 10:
        return 25
    return 10
```

#### Penalty Combination (max_plus_sqrt)

```python
def combine_penalties(penalties, method='max_plus_sqrt'):
    """
    Example with penalties [30, 20, 10]:
    - sum: 60
    - max: 30
    - max_plus_sqrt: 30 + sqrt(20+10) = 30 + 5.48 = 35.48
    """
    if method == 'max_plus_sqrt':
        sorted_p = sorted(penalties, reverse=True)
        max_penalty = sorted_p[0]
        others_sum = sum(sorted_p[1:])
        return min(100.0, max_penalty + math.sqrt(others_sum))
```

### 8.3 Calibration Metrics

```python
def compute_calibration_metrics(outcomes):
    labels = [o.get_label() for o in outcomes]
    
    tp = labels.count('TRUE_POSITIVE')
    fp = labels.count('FALSE_POSITIVE')
    tn = labels.count('TRUE_NEGATIVE')
    fn = labels.count('FALSE_NEGATIVE')
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    accuracy = (tp + tn) / len(labels)
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    
    return {
        'precision': precision,   # % of HIGH flags that were actual blowups
        'recall': recall,         # % of blowups that were flagged HIGH
        'accuracy': accuracy,
        'f1_score': f1,
        'false_positive_rate': fpr
    }
```

---

## 9. Dashboard Outputs

### 9.1 Macro OS Dashboard

```
================================================================================
                        MACRO REGIME DASHBOARD
                        2026-01-30 10:00 UTC
================================================================================

CURRENT REGIME: PATTERN 2 (GROWTH SCARE)
Confidence: 68%
Tenure: 8 days
Transition Watch: Pattern 6 (Credit Event) if HY widens +50bps

CORE DASHBOARD (14 Vital Signs)
--------------------------------------------------------------------------------
Indicator           Value      Δ1d     Δ5d     %ile(1Y)  Z-Score   Status
-----------------   --------   ------  ------  --------  --------  ------
S&P 500             4,892      -1.2%   -3.5%   35%       -0.8      [*]
VIX                 22.5       +15%    +25%    78%       +1.2      [!]
10Y Yield           4.15%      -5bp    -15bp   45%       -0.3      OK
2Y Yield            4.45%      -8bp    -20bp   52%       -0.2      OK
10Y-2Y Spread       -30bp      +3bp    +5bp    25%       -0.5      OK
HY OAS Spread       420bp      +25bp   +55bp   72%       +1.1      [!]
DXY                 104.2      +0.3%   +1.2%   65%       +0.6      OK

PATTERN VALIDATION
--------------------------------------------------------------------------------
✓ PMI rolling: 48.2 (below expansion)
✓ Earnings revisions: -8% (negative)
✓ Credit widening: +55bp in 5 days
✗ USD weakening: Not confirmed (DXY stable)

ALERTS
--------------------------------------------------------------------------------
[WARNING] HY spreads approaching 1-year 75th percentile
[WARNING] VIX elevated but not extreme
[INFO]    Watching for Pattern 6 transition (credit-equity divergence)

================================================================================
```

### 9.2 Mine Detector Dashboard

```
================================================================================
                     MINE DETECTOR RISK ASSESSMENT
                     Ticker: XYZ Corp | 2026-01-30 10:00 UTC
================================================================================

COMPOSITE SCORE: 67/100 [ELEVATED]
Structural Overlay: +0.5 notches (+5 points) - US Small-Cap
Staleness Penalty: +0 points
Adjusted Score: 72/100 [HIGH]
Macro Regime: RISK_OFF (thresholds adjusted)

CATEGORY BREAKDOWN
--------------------------------------------------------------------------------
Category               Score    Weight    Contribution    Status
-------------------    -----    ------    ------------    --------
Catalyst Risk            72     0.15         10.8         [!] Earnings in 3d
Solvency Risk            45     0.15          6.8         OK
Crowding Risk            81     0.12          9.7         [!] 28% short
Liquidity Flow Risk      35     0.10          3.5         OK
Momentum Risk            58     0.10          5.8         [*] Below 50-DMA
Governance Risk          42     0.12          5.0         OK
Refinancing Risk         55     0.10          5.5         [*] $2B due 6mo
Dilution Risk            38     0.08          3.0         OK
Event Risk               75     0.08          6.0         [!] Litigation

DOMINANT RISKS: Crowding, Event, Catalyst

ALERTS
--------------------------------------------------------------------------------
[CRITICAL] Short interest 28% with 89% utilization
[WARNING]  Earnings in 3 days with elevated IV skew
[WARNING]  Litigation hearing Feb 15

RECOMMENDATION
--------------------------------------------------------------------------------
Action: EXIT OR HEDGE IMMEDIATELY
Reason: Adjusted score 72 (HIGH) with multiple concurrent risks
Position Limit: 50% of normal (due to RISK_OFF regime)
Stop: Hard stop at -8% from current

================================================================================
```

### 9.3 System Health Dashboard

```
================================================================================
                        SYSTEM HEALTH DASHBOARD
                        2026-01-30 10:00 UTC
================================================================================

OVERALL STATUS: [HEALTHY]

DATA FRESHNESS
--------------------------------------------------------------------------------
Source                Last Update     Age        Status
--------------------  -------------   --------   --------
price_data            10:00:01 UTC    1s         [OK]
crypto_price          10:00:05 UTC    5s         [OK]
options_chain         09:45:00 UTC    15min      [OK]
short_interest        2026-01-29      1d         [OK]
credit_spreads        08:00:00 UTC    2hr        [OK]
token_unlocks         06:00:00 UTC    4hr        [OK]
twitter_sentiment     09:30:00 UTC    30min      [OK]

Total Staleness Penalty: 0.0 points

CALIBRATION (Last 30 Days)
--------------------------------------------------------------------------------
Outcomes: 847 (797 live + 50 bootstrap)

              Predicted HIGH    Predicted OK
Actual Blowup       62 (TP)         8 (FN)
Actual OK           23 (FP)       754 (TN)

Precision: 72.9%  (target: >75%)  [WARNING]
Recall:    88.6%  (target: >70%)  [OK]
Accuracy:  96.3%                  [OK]
F1 Score:  80.0%                  [OK]

RETRAINING STATUS
--------------------------------------------------------------------------------
Last Training:       2025-12-15 (46 days ago)
New Samples:         312 / 500 threshold
Model Accuracy:      89.2%
Regime Changes (30d): 3

Triggers: None active [OK]

================================================================================
```

---

## 10. External Audit Summary

The Mine Detector OS bundle underwent 4 independent external audits (feedback01-04). Key findings:

### 10.1 Strengths Confirmed (Across All Audits)

| Area | Finding | Rating |
|------|---------|--------|
| **Architecture** | Exceptional separation of concerns, modular design | 9/10 |
| **Consistency** | All 6 docs synchronized to same version | ✅ |
| **Interfaces** | Clear Python contracts with proper return types | ✅ |
| **State Management** | Regime hysteresis prevents whipsawing | ✅ |
| **Safety** | Hard block at 86 cannot be bypassed | ✅ |
| **Documentation** | Dashboard outputs, operational checklists | ✅ |

### 10.2 Critical Issues Identified

| Priority | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| 🔴 HIGH | Thread safety gaps | Core OS, Addendum A, E | Add `threading.Lock` to stateful components |
| 🔴 HIGH | API keys in BrokerConfig | Addendum C | Move to environment variables |
| 🔴 MEDIUM | Float precision | Addendum C | Use `Decimal` for financial calculations |
| 🔴 MEDIUM | Timestamp semantics | Core OS, Addendum E | Clearly separate origin_ts vs fetch_ts |
| ⚠️ | "ML" title misleading | Addendum A | Rename to "Expert System" or implement actual ML |
| ⚠️ | Web3 category gaps | Addendum D | Some categories return None |
| ⚠️ | Social sentiment gameable | Addendum B | Move to NLP/embedding-based analysis |

### 10.3 Overall Rating

**Average across 4 audits: 8.5/10**

"Production-ready with the noted fixes. This represents a sophisticated framework that, with the recommended improvements, could serve as the foundation for an institutional-grade risk management system."

---

## 11. Integration with diBoaS Analytics v3/v4

### 11.1 System Relationship

| System | Level | Purpose | Relationship |
|--------|-------|---------|--------------|
| **Macro OS** | Market-wide | Regime detection | Feeds regime into Mine Detector (Addendum A) |
| **Mine Detector** | Single security | Risk scoring | Uses regime for weight adjustments |
| **v3 Pipeline** | Platform | Daily/weekly data | Could feed Macro OS indicators |
| **v4 Architecture** | Platform | Provable intelligence | Could wrap Mine Detector outputs in Evidence Packs |

### 11.2 Potential Integration Points

1. **Macro OS → v3 Layer 3 (Analyst)**
   - Regime classification could inform Monte Carlo scenarios
   - Pattern detection could trigger Adelaide content variations

2. **Mine Detector → v4 Evidence Packs**
   - Each Mine Detector score could generate an Evidence Pack
   - Calibration outcomes could validate Truth Contracts

3. **v4 Gate 4 → Mine Detector Compliance**
   - Mine Detector disclaimers could follow Gate 4 language packs
   - Score communications could require compliance review

### 11.3 Recommended Integration Sequence

1. **Phase 1:** Use Macro OS regime signal in Adelaide weekly commentary
2. **Phase 2:** Add Mine Detector scoring for DeFi protocol health monitoring
3. **Phase 3:** Wrap Mine Detector outputs in v4 Evidence Pack format
4. **Phase 4:** Integrate structural overlay (Addendum D) for crypto positions

---

## 12. Appendix: Glossary

| Term | Definition |
|------|------------|
| **ADR** | American Depositary Receipt - foreign company shares traded on US exchanges |
| **Altman-Z** | Bankruptcy prediction score (Z < 1.8 = distress zone) |
| **FRA-OIS** | Forward Rate Agreement minus Overnight Index Swap - funding stress indicator |
| **HFCAA** | Holding Foreign Companies Accountable Act - US law requiring PCAOB audit access |
| **HY OAS** | High Yield Option-Adjusted Spread - credit stress measure |
| **LUDP** | Limit Up / Limit Down Pause - trading halt for extreme price moves |
| **MOVE Index** | Merrill Lynch Option Volatility Estimate - bond market VIX |
| **Notch** | Structural overlay unit (0.0-2.5), converted to points via ×10 |
| **PCAOB** | Public Company Accounting Oversight Board |
| **Perp Funding** | Perpetual futures funding rate - leverage sentiment indicator |
| **VIE** | Variable Interest Entity - corporate structure for foreign ownership |

---

## 13. Appendix: Operational Checklists

### 13.1 Daily Checklist

```
PRE-MARKET (06:00 UTC)
[ ] Verify all data feeds are live
[ ] Check overnight batch jobs completed
[ ] Review triggered alerts from overnight
[ ] Verify ML model health

MARKET OPEN (09:30 ET)
[ ] Confirm real-time streaming active
[ ] Monitor first 30 minutes for anomalies
[ ] Check API rate limits not exceeded

MARKET CLOSE (16:00 ET)
[ ] Archive daily scores for calibration
[ ] Run calibration update batch
[ ] Generate daily summary report
[ ] Review any new flagged positions
```

### 13.2 Weekly Checklist

```
MONDAY
[ ] Review prior week calibration metrics
[ ] Update short interest data
[ ] Review any 13F filings from prior week
[ ] Check token unlock calendar for week ahead

FRIDAY
[ ] Generate weekly calibration report
[ ] Archive weekly data
[ ] Review retraining triggers
[ ] Plan any weekend maintenance
```

### 13.3 Monthly Checklist

```
FIRST WEEK
[ ] Full calibration review (analyze FP/FN)
[ ] Evaluate retraining need
[ ] Review API cost/usage
[ ] Check data source reliability

END OF MONTH
[ ] Full system audit
[ ] Backup verification
[ ] Security review
[ ] Capacity planning
```

---

*Document Version: 2026-01-30*
*Bundle Version: 2026-01-30-r9*
*Covering: Macro Operating System + Mine Detector OS (Core + Addendums A-E)*
