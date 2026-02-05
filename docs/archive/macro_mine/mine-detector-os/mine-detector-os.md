# Mine Detector Operating System

> A single-name idiosyncratic risk scanner that complements the Macro Operating System. This is a landmine detection framework, not a watchlist.

**Version:** 2026-01-30-r9

**Bundle Files:**
- Core OS: mine-detector-os.md (this document)
- Addendum A: mine-detector-addendum-a-ml-classification.md
- Addendum B: mine-detector-addendum-b-social-sentiment.md
- Addendum C: mine-detector-addendum-c-brokerage.md
- Addendum D: mine-detector-addendum-d-adr-smallcap.md
- Addendum E: mine-detector-addendum-e-maintenance-operations.md

---

## Purpose

The Mine Detector scans individual securities for idiosyncratic risk -- company-specific landmines that can blow up a position regardless of macro conditions. While the Macro OS tells you whether to be in risk assets, the Mine Detector tells you whether a specific name is safe to own.

**Core Insight:** Most equity blowups are predictable in hindsight. The patterns exist in options markets, credit spreads, insider behavior, and positioning data weeks before the event. This system codifies those patterns.

**Output:** A composite risk score (0-100) for each security, with category breakdowns and actionable thresholds.

---

## The 9 Canonical Risk Categories

Every idiosyncratic risk maps to one of these categories:

```python
from enum import Enum

class RiskCategory(Enum):
    """
    Canonical risk categories for Mine Detector OS.
    Use this enum throughout all modules for consistency.
    """
    CATALYST_RISK = "catalyst_risk"
    SOLVENCY_RISK = "solvency_risk"
    CROWDING_RISK = "crowding_risk"
    LIQUIDITY_FLOW_RISK = "liquidity_flow_risk"
    MOMENTUM_RISK = "momentum_risk"
    GOVERNANCE_RISK = "governance_risk"
    REFINANCING_RISK = "refinancing_risk"
    DILUTION_RISK = "dilution_risk"
    EVENT_RISK = "event_risk"
```

| # | Category | What It Detects | Key Data Sources |
|---|----------|-----------------|------------------|
| 1 | Catalyst Risk | Earnings, FDA dates, legal rulings approaching | Corporate calendars, court dockets |
| 2 | Solvency Risk | Bankruptcy probability, covenant breach | Credit spreads, Altman-Z, debt schedules |
| 3 | Crowding Risk | Positioning extremes, squeeze/collapse setups | Short interest, borrow rates, 13F concentration |
| 4 | Liquidity Flow Risk | Forced selling pressure | ETF rebalance, index changes, margin calls |
| 5 | Momentum Risk | Technical breakdowns | Price vs MA, RSI extremes, volume patterns |
| 6 | Governance Risk | Management red flags | Insider sales, auditor changes, restatements |
| 7 | Refinancing Risk | Debt maturity walls | Bond schedules, revolver availability |
| 8 | Dilution Risk | Equity overhang | Shelf registrations, warrant exercises, ATM programs |
| 9 | Event Risk | Binary outcomes, social anomalies | M&A spreads, litigation, social sentiment spikes |

---

## Shared Utilities Module

All addendums import from this shared module for consistency:

```python
"""
mine_detector_shared.py
Shared utilities for Mine Detector OS.
All addendums must import from here for consistency.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import math


# =============================================================================
# TIME UTILITIES (UTC ONLY)
# =============================================================================

def utc_now() -> datetime:
    """Get current time in UTC. Use this throughout the system."""
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """Convert any datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO string with UTC indicator."""
    utc_dt = to_utc(dt)
    return utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ')


# =============================================================================
# RISK CATEGORIES (CANONICAL)
# =============================================================================

class RiskCategory(Enum):
    """Canonical risk categories. Use this enum everywhere."""
    CATALYST_RISK = "catalyst_risk"
    SOLVENCY_RISK = "solvency_risk"
    CROWDING_RISK = "crowding_risk"
    LIQUIDITY_FLOW_RISK = "liquidity_flow_risk"
    MOMENTUM_RISK = "momentum_risk"
    GOVERNANCE_RISK = "governance_risk"
    REFINANCING_RISK = "refinancing_risk"
    DILUTION_RISK = "dilution_risk"
    EVENT_RISK = "event_risk"


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


# =============================================================================
# SCORE UTILITIES
# =============================================================================

def verify_and_cap_score(score: float, source: str = "unknown") -> float:
    """
    Verify score is in valid range [0, 100] and cap if necessary.
    Logs warning if capping was required.
    """
    if score < 0:
        print(f"WARNING: Negative score {score} from {source}, capping to 0")
        return 0.0
    if score > 100:
        print(f"WARNING: Score {score} from {source} exceeds 100, capping to 100")
        return 100.0
    return float(score)


def combine_penalties(penalties: List[float], 
                      method: str = "max_plus_sqrt") -> float:
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
    if not penalties:
        return 0.0
    
    if method == 'sum':
        return min(100.0, sum(penalties))
    
    if method == 'max':
        return max(penalties)
    
    if method == 'max_plus_sqrt':
        sorted_p = sorted(penalties, reverse=True)
        max_penalty = sorted_p[0]
        others_sum = sum(sorted_p[1:])
        return min(100.0, max_penalty + math.sqrt(others_sum))
    
    return max(penalties)
```

---

## Interface Contracts

Each addendum implements a specific interface. These contracts ensure consistent integration:

### ML Classification Interface (Addendum A)

```python
def classify_regime(features: Dict[str, float], 
                    classifier_state: 'RegimeClassifierState') -> Dict:
    """
    Classify current market regime.
    
    Args:
        features: Dict of feature name to value
        classifier_state: Persistent state object (MUST be reused across calls)
    
    Returns:
        {
            'regime': str,           # RISK_ON, RISK_OFF, TRANSITION
            'confidence': float,     # 0.0 to 1.0
            'probabilities': Dict,   # Per-regime probs (MUST sum to 1.0)
            'features_used': List,   # Features that drove classification
            'regime_tenure_days': int
        }
    """
```

### Social Sentiment Interface (Addendum B)

```python
def compute_social_sentiment(ticker: str, 
                              time_window_hours: int = 24) -> Dict:
    """
    Compute social sentiment score for a ticker.
    
    Returns:
        {
            'score': float,              # -100 to +100 (raw sentiment)
            'event_risk_contribution': float,  # 0 to 100 (mapped to Event Risk)
            'confidence': str,           # HIGH, MEDIUM, LOW, VERY_LOW
            'volume': int,               # Posts analyzed
            'sources': Dict,             # By platform
            'alerts': List[str]
        }
    """
```

### Brokerage Integration Interface (Addendum C)

```python
def get_portfolio_positions() -> List[Dict]:
    """
    Retrieve current portfolio positions.
    
    Returns list of:
        {
            'ticker': str,
            'quantity': float,
            'avg_cost': float,
            'current_price': float,
            'market_value': float,
            'unrealized_pnl': float,
            'asset_class': str,
            'contract_multiplier': float
        }
    """
```

### ADR/Small-Cap/Web3 Interface (Addendum D)

```python
def compute_structural_overlay(security_type: str,
                                geopolitical: Dict,
                                liquidity: Dict,
                                data_gaps: List[str]) -> Dict:
    """
    Compute structural risk overlay.
    
    Returns:
        {
            'overlay_notches': float,    # 0.0 to 2.5 (raw measure)
            'overlay_points': float,     # 0 to 25 (notches * 10)
            'confidence': str,
            'reasons': List[str],
            'security_type': str
        }
    
    UNIT CONVERSION:
        overlay_points = overlay_notches * 10
        
        Example: 1.5 notches = 15 points added to composite score
    """
```

---

## Composite Score Calculation

```python
def compute_composite_score(category_scores: Dict[RiskCategory, float],
                            weights: Dict[RiskCategory, float] = None,
                            overlay_notches: float = 0.0,
                            staleness_penalty: float = 0.0) -> Dict:
    """
    Compute weighted composite risk score.
    
    Args:
        category_scores: Dict mapping RiskCategory to score (0-100 each)
        weights: Optional custom weights (default: DEFAULT_WEIGHTS)
        overlay_notches: Structural overlay from Addendum D (0.0 to 2.5)
        staleness_penalty: Penalty from stale data sources (see Addendum E)
                           Obtained from StalenessChecker.get_total_staleness_penalty()
    
    Returns:
        {
            'composite_score': float,       # 0-100 (before adjustments)
            'adjusted_score': float,        # After overlay + staleness (capped at 100)
            'overlay_notches': float,       # Raw overlay (0.0-2.5)
            'overlay_points': float,        # Points added (0-25)
            'staleness_penalty': float,     # Points added from stale data
            'category_contributions': Dict,
            'dominant_risks': List[str]
        }
    
    OVERLAY UNIT CONVERSION:
        The structural overlay from Addendum D is in "notches" (0.0 to 2.5).
        Convert to points: overlay_points = overlay_notches * 10
        
        - 0.0 notches = 0 points (US large-cap baseline)
        - 1.0 notches = 10 points
        - 2.5 notches = 25 points (maximum structural penalty)
    
    STALENESS PENALTY:
        Added to the score when data sources are stale. Obtained from
        Addendum E's StalenessChecker.get_total_staleness_penalty().
        This ensures the system penalizes uncertainty from outdated data.
    """
    weights = weights or DEFAULT_WEIGHTS
    
    # ==========================================================================
    # MISSING CATEGORY HANDLING (r6 fix)
    # ==========================================================================
    # If fewer than 9 categories are provided, we must handle this explicitly.
    # Options:
    #   1. STRICT: Require all 9 categories (raise error if missing)
    #   2. RENORMALIZE: Redistribute weights across provided categories only
    #   3. PENALIZE: Add a "data gap" penalty for missing categories
    #
    # We use RENORMALIZE + WARNING approach:
    # - Renormalize weights over only the categories that ARE provided
    # - Log a warning listing which categories are missing
    # - This prevents silently understated scores (the original bug)
    # ==========================================================================
    
    # r7 fix: Build set from non-None values only
    # This prevents weight leakage when Web3 translation returns None for unmapped categories
    provided_categories = set(k for k, v in category_scores.items() if v is not None)
    all_categories = set(RiskCategory)
    missing_categories = all_categories - provided_categories
    
    if missing_categories:
        missing_names = [cat.value for cat in missing_categories]
        print(f"WARNING: Missing {len(missing_categories)} categories: {missing_names}. "
              f"Weights will be renormalized over {len(provided_categories)} provided categories.")
    
    # Filter weights to only include provided categories
    active_weights = {k: v for k, v in weights.items() if k in provided_categories}
    
    # ==========================================================================
    # MINIMUM WEIGHT COVERAGE CHECK (r8 fix)
    # ==========================================================================
    # If too few categories are provided, the renormalized weights can cause
    # misleading scores. For example, if only CATALYST_RISK (15% weight) is
    # provided, it renormalizes to 100%, potentially creating false CRITICAL.
    # Require at least 40% of total weight coverage for a valid score.
    # ==========================================================================
    MIN_WEIGHT_COVERAGE = 0.4  # 40% of total weight required
    
    total_provided_weight = sum(weights.get(cat, 0) for cat in provided_categories)
    if total_provided_weight < MIN_WEIGHT_COVERAGE:
        return {
            'composite_score': 0.0,
            'adjusted_score': 0.0,
            'overlay_notches': round(overlay_notches, 2),
            'overlay_points': round(overlay_notches * 10.0, 1),
            'staleness_penalty': round(staleness_penalty, 1),
            'category_contributions': {},
            'dominant_risks': [],
            'missing_categories': [cat.value for cat in missing_categories],
            'warning': f'Insufficient category coverage: {total_provided_weight:.0%} < {MIN_WEIGHT_COVERAGE:.0%} minimum',
            'weight_coverage': round(total_provided_weight, 2)
        }
    
    if not active_weights:
        # No valid categories provided at all
        return {
            'composite_score': 0.0,
            'adjusted_score': 0.0,
            'overlay_notches': round(overlay_notches, 2),
            'overlay_points': round(overlay_notches * 10.0, 1),
            'staleness_penalty': round(staleness_penalty, 1),
            'category_contributions': {},
            'dominant_risks': [],
            'missing_categories': [cat.value for cat in missing_categories],
            'warning': 'No valid category scores provided'
        }
    
    # Normalize weights to sum to 1.0 (over provided categories only)
    total_weight = sum(active_weights.values())
    normalized_weights = {k: v/total_weight for k, v in active_weights.items()}
    
    # Calculate weighted contributions
    contributions = {}
    for category, score in category_scores.items():
        if score is None:
            # Skip None values (Web3 translation returns None for unmapped categories)
            continue
        
        # r8 fix: Validate numeric type before processing
        if not isinstance(score, (int, float)):
            raise TypeError(
                f"Score for {category.value} must be numeric (int or float), "
                f"got {type(score).__name__}: {score}"
            )
        
        capped_score = verify_and_cap_score(score, f"category_{category.value}")
        weight = normalized_weights.get(category, 0)
        contributions[category] = capped_score * weight
    
    # Base composite (0-100)
    composite = sum(contributions.values())
    composite = verify_and_cap_score(composite, "composite_base")
    
    # Apply structural overlay (notches -> points)
    overlay_points = overlay_notches * 10.0
    
    # Apply staleness penalty (from Addendum E)
    # Staleness penalty is already in points, no conversion needed
    
    adjusted = composite + overlay_points + staleness_penalty
    adjusted = verify_and_cap_score(adjusted, "composite_adjusted")
    
    # Identify dominant risks (top 3)
    sorted_contrib = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    dominant = [cat.value for cat, _ in sorted_contrib[:3]]
    
    result = {
        'composite_score': round(composite, 1),
        'adjusted_score': round(adjusted, 1),
        'overlay_notches': round(overlay_notches, 2),
        'overlay_points': round(overlay_points, 1),
        'staleness_penalty': round(staleness_penalty, 1),
        'category_contributions': {k.value: round(v, 2) for k, v in contributions.items()},
        'dominant_risks': dominant
    }
    
    # Include missing categories info if any were missing
    if missing_categories:
        result['missing_categories'] = [cat.value for cat in missing_categories]
        result['categories_provided'] = len(provided_categories)
        result['categories_expected'] = len(all_categories)
    
    return result
```

---

## Score Interpretation and Actions

| Score Range | Risk Level | Recommended Action |
|-------------|------------|-------------------|
| 0-25 | LOW | Normal position sizing allowed |
| 26-50 | MODERATE | Tighten stops, reduce if scaling in |
| 51-70 | ELEVATED | Reduce position by 50%, set hard stops |
| 71-85 | HIGH | Exit or hedge immediately |
| 86-100 | CRITICAL | Avoid entirely, close existing positions |

**Threshold Clarification (r7):**

The system uses three related but distinct threshold concepts:

1. **Static Score Table (above):** Baseline interpretation for all regimes. Used for display, reporting, and human decision-making.

2. **Regime-Adjusted Thresholds (MacroOSIntegration):** Dynamic thresholds that shift based on current market regime. For example, in RISK_OFF, the "critical" warning may trigger at 75 instead of 86. These are used for alerts and recommendations.

3. **Execution Hard Blocks (Addendum C):** The brokerage layer uses the static CRITICAL threshold (86) as the hard block for automated execution, regardless of regime. This ensures consistent safety behavior.

The regime-adjusted thresholds provide earlier warnings in stressed markets, while the static 86 threshold remains the universal "do not pass" line for automated systems.

---

## Data Quality: Staleness vs Synchronization

The system distinguishes between two data quality concepts:

**Timestamp Clarification (r8):**

These two systems use DIFFERENT timestamp concepts:

| System | Timestamp Used | Purpose | Example |
|--------|---------------|---------|--------|
| **StalenessChecker** (Addendum E) | `data_origin_timestamp` | Is the data itself too old? | Short Interest published 2 days ago is OK (threshold: 48h) |
| **DataSynchronizer** (below) | `fetch_timestamp` | Are all data points from the same moment? | All data fetched within 5 minutes of each other |

A data point can be:
- **Fresh for staleness** (origin: 2 days ago, within 48h threshold) AND
- **Valid for synchronization** (fetched: 30 seconds ago, within 5 min spread)

When calling `DataSynchronizer.add_data()`, pass the **fetch timestamp** (when you retrieved it), NOT the data origin date. The staleness check happens separately via `StalenessChecker`.

### 1. Staleness Thresholds

How old can data be before we penalize or alert? Different sources have different tolerances:

| Data Source | Normal Refresh | Staleness Threshold | Penalty |
|-------------|----------------|---------------------|---------|
| Price (equities) | 1 min | 5 min | +10 pts |
| Price (crypto) | 15 sec | 1 min | +15 pts |
| Options Chain | 15 min | 60 min | +5 pts |
| Short Interest | Daily | 48 hours | +3 pts |
| Token Unlocks | 6 hours | 24 hours | +8 pts |

See Addendum E for complete schedules.

### 2. Snapshot Synchronization

When computing a composite score, all data must be from approximately the same moment. This prevents mixing Monday's price with Friday's short interest.

```python
from threading import Lock
from dataclasses import dataclass
from typing import Any

@dataclass
class DataPoint:
    """A timestamped data point."""
    source: str
    value: Any
    timestamp: datetime
    
    @property
    def age_seconds(self) -> float:
        return (utc_now() - self.timestamp).total_seconds()


class DataSynchronizer:
    """
    Ensures all data sources are temporally aligned before scoring.
    
    IMPORTANT: This is DIFFERENT from staleness thresholds.
    - Staleness: How old can data be before penalty?
    - Synchronization: Are all data points from the same moment?
    
    Data can be "fresh" (within staleness threshold) but still rejected
    by the synchronizer if it's too far from other data in the snapshot.
    """
    
    MAX_SNAPSHOT_SPREAD_SECONDS = 300  # 5 minutes max spread within snapshot
    
    def __init__(self):
        self._lock = Lock()
        self._snapshot_time: Optional[datetime] = None
        self._data_cache: Dict[str, DataPoint] = {}
    
    def begin_snapshot(self) -> datetime:
        """Begin a synchronized snapshot. Returns reference time."""
        with self._lock:
            self._snapshot_time = utc_now()
            self._data_cache = {}
            return self._snapshot_time
    
    def add_data(self, source: str, value: Any, 
                 data_timestamp: datetime) -> Dict:
        """
        Add data to current snapshot.
        
        Returns:
            {'accepted': bool, 'reason': str or None, 'lag_seconds': float}
        """
        with self._lock:
            if self._snapshot_time is None:
                raise RuntimeError("Call begin_snapshot() first")
            
            data_timestamp = to_utc(data_timestamp)
            lag = (self._snapshot_time - data_timestamp).total_seconds()
            
            # Reject if too old relative to snapshot time
            if lag > self.MAX_SNAPSHOT_SPREAD_SECONDS:
                return {
                    'accepted': False,
                    'reason': f'Data too old: {lag:.0f}s lag > {self.MAX_SNAPSHOT_SPREAD_SECONDS}s max',
                    'lag_seconds': lag
                }
            
            # Reject future data (clock skew protection)
            if lag < -60:
                return {
                    'accepted': False,
                    'reason': f'Data from future: {-lag:.0f}s ahead',
                    'lag_seconds': lag
                }
            
            self._data_cache[source] = DataPoint(
                source=source,
                value=value,
                timestamp=data_timestamp
            )
            
            return {'accepted': True, 'reason': None, 'lag_seconds': lag}
    
    def get_snapshot(self) -> Dict:
        """Return the synchronized snapshot."""
        with self._lock:
            if not self._data_cache:
                return {
                    'snapshot_time': self._snapshot_time,
                    'sources': {},
                    'spread_seconds': 0
                }
            
            timestamps = [dp.timestamp for dp in self._data_cache.values()]
            spread = (max(timestamps) - min(timestamps)).total_seconds()
            
            return {
                'snapshot_time': self._snapshot_time,
                'sources': {
                    src: {'value': dp.value, 'timestamp': dp.timestamp}
                    for src, dp in self._data_cache.items()
                },
                'spread_seconds': spread
            }
```

---

## API Fallbacks and Manual Mode

When APIs are unavailable, the system degrades gracefully:

```python
class ManualModeManager:
    """Manages fallback to manual data entry when APIs fail."""
    
    REQUIRED_MANUAL_FIELDS = {
        RiskCategory.CATALYST_RISK: ['next_earnings_date', 'days_to_catalyst'],
        RiskCategory.SOLVENCY_RISK: ['current_ratio', 'debt_to_equity'],
        RiskCategory.CROWDING_RISK: ['short_interest_pct'],
        RiskCategory.MOMENTUM_RISK: ['price_vs_50dma_pct'],
    }
    
    def __init__(self):
        self.api_status: Dict[str, bool] = {}
        self.manual_overrides: Dict[str, Any] = {}
    
    def check_api_health(self, api_name: str) -> bool:
        return self.api_status.get(api_name, True)
    
    def require_manual_entry(self, category: RiskCategory) -> List[str]:
        """Fields requiring manual entry when APIs down."""
        return self.REQUIRED_MANUAL_FIELDS.get(category, [])
    
    def set_manual_override(self, field: str, value: Any, source: str = "manual"):
        """Record manual override with audit trail."""
        self.manual_overrides[field] = {
            'value': value,
            'source': source,
            'timestamp': utc_now(),
            'is_manual': True
        }
    
    def get_data_with_fallback(self, field: str, api_func, manual_value=None):
        """Try API first, fall back to manual if provided."""
        try:
            return api_func()
        except Exception as e:
            if manual_value is not None:
                self.set_manual_override(field, manual_value)
                return manual_value
            raise RuntimeError(f"API failed, no manual fallback for {field}: {e}")
```

---

## Macro OS Integration

Integration with the Macro Operating System for regime-aware scoring:

```python
class MacroOSIntegration:
    """
    Integrates Mine Detector with Macro OS regime signals.
    
    Regime affects:
    1. Category weight adjustments
    2. Score thresholds for actions
    3. Alert sensitivity
    """
    
    REGIME_WEIGHT_ADJUSTMENTS = {
        'RISK_OFF': {
            RiskCategory.SOLVENCY_RISK: 1.3,
            RiskCategory.REFINANCING_RISK: 1.3,
            RiskCategory.LIQUIDITY_FLOW_RISK: 1.2,
            RiskCategory.MOMENTUM_RISK: 0.8,
        },
        'RISK_ON': {
            RiskCategory.CROWDING_RISK: 1.2,
            RiskCategory.MOMENTUM_RISK: 1.1,
            RiskCategory.SOLVENCY_RISK: 0.9,
        },
        'TRANSITION': {}
    }
    
    REGIME_THRESHOLDS = {
        'RISK_OFF': {'elevated': 40, 'high': 60, 'critical': 75},
        'RISK_ON': {'elevated': 55, 'high': 75, 'critical': 90},
        'TRANSITION': {'elevated': 50, 'high': 70, 'critical': 85}
    }
    
    def __init__(self):
        self._current_regime = 'TRANSITION'
    
    def get_adjusted_weights(self, 
                              base_weights: Dict[RiskCategory, float]) -> Dict[RiskCategory, float]:
        """Adjust weights based on current regime."""
        adjustments = self.REGIME_WEIGHT_ADJUSTMENTS.get(self._current_regime, {})
        
        adjusted = {}
        for category, weight in base_weights.items():
            multiplier = adjustments.get(category, 1.0)
            adjusted[category] = weight * multiplier
        
        # Renormalize
        total = sum(adjusted.values())
        return {k: v/total for k, v in adjusted.items()}
    
    def get_thresholds(self) -> Dict[str, int]:
        """Get score thresholds for current regime."""
        return self.REGIME_THRESHOLDS.get(
            self._current_regime, 
            self.REGIME_THRESHOLDS['TRANSITION']
        )
    
    def update_regime(self, regime: str):
        """Update from Macro OS."""
        if regime in self.REGIME_WEIGHT_ADJUSTMENTS:
            self._current_regime = regime
```

---

## Calibration and Outcome Tracking

Formal definitions for measuring system accuracy:

```python
@dataclass
class BlowupDefinition:
    """
    What constitutes a "blowup" for calibration.
    
    A security "blew up" if ANY of these occur within 30 days of HIGH/CRITICAL score:
    1. Realized vol >= 2x the 20-day historical vol at flag time
    2. Single-session loss >= 5%
    3. Gap down >= 15%
    4. Trading halt for fundamental reasons
    5. Credit event (default, covenant breach, restructuring)
    """
    vol_ratio_threshold: float = 2.0
    single_day_loss_threshold: float = 5.0
    gap_down_threshold: float = 15.0
    lookback_days: int = 30
    high_score_threshold: float = 70.0


@dataclass
class CalibrationOutcome:
    """Tracks outcome for calibration."""
    ticker: str
    flag_date: datetime
    flag_score: float
    
    # Outcomes within lookback
    max_drawdown: float = 0.0
    max_single_day_loss: float = 0.0
    max_gap_down: float = 0.0
    realized_vol_ratio: float = 1.0
    had_trading_halt: bool = False
    had_credit_event: bool = False
    
    def is_blowup(self, definition: BlowupDefinition = None) -> bool:
        """Did this qualify as a blowup?"""
        d = definition or BlowupDefinition()
        return (
            self.realized_vol_ratio >= d.vol_ratio_threshold or
            self.max_single_day_loss >= d.single_day_loss_threshold or
            self.max_gap_down >= d.gap_down_threshold or
            self.had_trading_halt or
            self.had_credit_event
        )
    
    def get_label(self, definition: BlowupDefinition = None) -> str:
        """
        Calibration label:
        - TRUE_POSITIVE: Flagged high AND blew up
        - FALSE_POSITIVE: Flagged high but did NOT blow up
        - TRUE_NEGATIVE: NOT flagged AND did NOT blow up
        - FALSE_NEGATIVE: NOT flagged but DID blow up
        """
        d = definition or BlowupDefinition()
        flagged_high = self.flag_score >= d.high_score_threshold
        blew_up = self.is_blowup(d)
        
        if flagged_high and blew_up:
            return "TRUE_POSITIVE"
        elif flagged_high and not blew_up:
            return "FALSE_POSITIVE"
        elif not flagged_high and not blew_up:
            return "TRUE_NEGATIVE"
        else:
            return "FALSE_NEGATIVE"
```

---

## Dashboard Output

```
================================================================================
                     MINE DETECTOR RISK ASSESSMENT
                     Ticker: XYZ Corp | 2026-01-30 10:00 UTC
================================================================================

COMPOSITE SCORE: 67/100 [ELEVATED]
Structural Overlay: +0.0 notches (+0 points) - US Large Cap
Macro Regime: RISK_ON (thresholds adjusted)

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
Action: REDUCE POSITION BY 50%
Reason: Elevated score (67) with multiple concurrent risks
Stop:   Hard stop at -8% from current

================================================================================
```

---

## Version Control

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
    import os
    
    results = {'valid': True, 'files': {}, 'errors': []}
    
    for filename in BUNDLE_FILES:
        filepath = os.path.join(bundle_dir, filename)
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                if f'**Version:** {BUNDLE_VERSION}' in content:
                    results['files'][filename] = 'OK'
                else:
                    results['files'][filename] = 'VERSION_MISMATCH'
                    results['valid'] = False
                    results['errors'].append(f"{filename}: version mismatch")
        except FileNotFoundError:
            results['files'][filename] = 'MISSING'
            results['valid'] = False
            results['errors'].append(f"{filename}: not found")
    
    return results
```

---

## Cross-References

- **Addendum A:** Regime classification, feature engineering, model calibration
- **Addendum B:** Social sentiment, bot detection, Event Risk mapping
- **Addendum C:** Portfolio sync, brokerage integration, execution
- **Addendum D:** ADR/small-cap/Web3 overlays, structural risk
- **Addendum E:** Data schedules, staleness, retraining, operations

---

---

## Future Enhancements to be Evaluated

The following topics have been identified for potential future development:

- **Thread safety concerns:** Add locking mechanisms or thread-local storage for stateful components (RegimeClassifierState, StalenessChecker) to support concurrent scoring requests in production environments.

- **Structured logging (r8):** Replace `print()` statements with Python's `logging` module for production deployments. This enables log levels, structured output (JSON), and integration with log aggregation systems (ELK, Datadog, etc.). Current `print()` calls in `verify_and_cap_score()` and `compute_composite_score()` should become `logger.warning()` calls.

---

## Design Notes

**Intentional Double-Penalization of Structural Overlay (r8):**

The structural overlay from Addendum D intentionally affects BOTH:
1. The `adjusted_score` (overlay_points added to composite)
2. Position sizing limits (via `get_position_size_limit()` in Addendum D)

This is **by design** for conservative risk management. A China ADR with 1.5 notches overlay will:
- Have 15 points added to its score (potentially pushing it from HIGH to CRITICAL)
- AND have position sizing capped at 50% of normal

This dual penalization reflects the compounding nature of structural risks—they affect both the probability of adverse events AND the ability to exit positions when those events occur.

---

*Mine Detector OS v2026-01-30-r9*
