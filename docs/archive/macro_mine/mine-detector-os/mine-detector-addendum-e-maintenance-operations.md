# Mine Detector OS -- Addendum E: Maintenance & Operations

> Data refresh schedules, staleness thresholds, retraining triggers, calibration procedures, and operational checklists.

**Version:** 2026-01-30-r9

**Cross-References:**
- Core OS: mine-detector-os.md (version control, staleness thresholds table)
- Addendum A: mine-detector-addendum-a-ml-classification.md (model retraining)
- Addendum B: mine-detector-addendum-b-social-sentiment.md (API rate limits)
- Addendum D: mine-detector-addendum-d-adr-smallcap.md (token unlock tracking)

---

## Overview

This addendum provides operational guidance for:

1. **Data Refresh Schedules** - How often to update each data source
2. **Staleness Thresholds** - When data is too old to use
3. **Retraining Triggers** - When to retrain ML models
4. **Calibration Tracking** - Measuring system accuracy
5. **Operational Checklists** - Daily/weekly/monthly procedures

---

## Imports and Dependencies

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timezone, timedelta
import math

# Import from shared module (Core OS)
from mine_detector_shared import utc_now, to_utc, format_timestamp, RiskCategory
```

---

## Data Source Registry

```python
class DataSource(Enum):
    """All data sources used by Mine Detector."""
    
    # Price data
    PRICE_DATA = "price_data"
    CRYPTO_PRICE = "crypto_price"  # Separate for tighter thresholds
    
    # Options & derivatives
    OPTIONS_CHAIN = "options_chain"
    PERP_FUNDING = "perp_funding"
    
    # Positioning
    SHORT_INTEREST = "short_interest"
    INSTITUTIONAL_13F = "institutional_13f"
    
    # Credit
    CREDIT_SPREADS = "credit_spreads"
    
    # Social
    TWITTER_SENTIMENT = "twitter_sentiment"
    REDDIT_SENTIMENT = "reddit_sentiment"
    STOCKTWITS_SENTIMENT = "stocktwits_sentiment"
    DISCORD_SENTIMENT = "discord_sentiment"    # r6: Added to match Addendum B
    TELEGRAM_SENTIMENT = "telegram_sentiment"  # r6: Added to match Addendum B
    
    # Web3
    TOKEN_UNLOCKS = "token_unlocks"
    PROTOCOL_TVL = "protocol_tvl"
    CEX_FLOWS = "cex_flows"
    
    # Calendar
    EARNINGS_CALENDAR = "earnings_calendar"
    
    # Governance
    INSIDER_TRANSACTIONS = "insider_transactions"
    SEC_FILINGS = "sec_filings"


@dataclass
class RefreshConfig:
    """Configuration for a data source refresh schedule."""
    source: DataSource
    refresh_interval_minutes: float  # Float to support sub-minute intervals (e.g., 0.25 = 15 sec)
    staleness_threshold_minutes: float
    staleness_penalty_points: float  # Added to composite score when stale
    is_critical: bool  # If true, block scoring when stale
    
    @property
    def refresh_interval(self) -> timedelta:
        return timedelta(minutes=self.refresh_interval_minutes)
    
    @property
    def staleness_threshold(self) -> timedelta:
        return timedelta(minutes=self.staleness_threshold_minutes)


# Data refresh configuration
REFRESH_CONFIGS: Dict[DataSource, RefreshConfig] = {
    # Price data - most time-sensitive
    DataSource.PRICE_DATA: RefreshConfig(
        source=DataSource.PRICE_DATA,
        refresh_interval_minutes=1,
        staleness_threshold_minutes=5,
        staleness_penalty_points=10.0,
        is_critical=True
    ),
    DataSource.CRYPTO_PRICE: RefreshConfig(
        source=DataSource.CRYPTO_PRICE,
        refresh_interval_minutes=0.25,  # 15 seconds
        staleness_threshold_minutes=1,
        staleness_penalty_points=15.0,
        is_critical=True
    ),
    
    # Options & derivatives
    DataSource.OPTIONS_CHAIN: RefreshConfig(
        source=DataSource.OPTIONS_CHAIN,
        refresh_interval_minutes=15,
        staleness_threshold_minutes=60,
        staleness_penalty_points=5.0,
        is_critical=False
    ),
    DataSource.PERP_FUNDING: RefreshConfig(
        source=DataSource.PERP_FUNDING,
        refresh_interval_minutes=60,
        staleness_threshold_minutes=180,
        staleness_penalty_points=5.0,
        is_critical=False
    ),
    
    # Positioning - daily/weekly data
    DataSource.SHORT_INTEREST: RefreshConfig(
        source=DataSource.SHORT_INTEREST,
        refresh_interval_minutes=1440,  # Daily
        staleness_threshold_minutes=2880,  # 2 days
        staleness_penalty_points=3.0,
        is_critical=False
    ),
    DataSource.INSTITUTIONAL_13F: RefreshConfig(
        source=DataSource.INSTITUTIONAL_13F,
        refresh_interval_minutes=10080,  # Weekly
        staleness_threshold_minutes=20160,  # 2 weeks
        staleness_penalty_points=2.0,
        is_critical=False
    ),
    
    # Credit
    DataSource.CREDIT_SPREADS: RefreshConfig(
        source=DataSource.CREDIT_SPREADS,
        refresh_interval_minutes=60,
        staleness_threshold_minutes=240,
        staleness_penalty_points=4.0,
        is_critical=False
    ),
    
    # Social sentiment
    DataSource.TWITTER_SENTIMENT: RefreshConfig(
        source=DataSource.TWITTER_SENTIMENT,
        refresh_interval_minutes=30,
        staleness_threshold_minutes=120,
        staleness_penalty_points=2.0,
        is_critical=False
    ),
    DataSource.REDDIT_SENTIMENT: RefreshConfig(
        source=DataSource.REDDIT_SENTIMENT,
        refresh_interval_minutes=60,
        staleness_threshold_minutes=180,
        staleness_penalty_points=2.0,
        is_critical=False
    ),
    
    # Web3
    DataSource.TOKEN_UNLOCKS: RefreshConfig(
        source=DataSource.TOKEN_UNLOCKS,
        refresh_interval_minutes=360,  # 6 hours
        staleness_threshold_minutes=1440,  # 24 hours
        staleness_penalty_points=8.0,
        is_critical=True  # Critical for crypto
    ),
    DataSource.PROTOCOL_TVL: RefreshConfig(
        source=DataSource.PROTOCOL_TVL,
        refresh_interval_minutes=60,
        staleness_threshold_minutes=360,
        staleness_penalty_points=5.0,
        is_critical=False
    ),
    
    # Calendar
    DataSource.EARNINGS_CALENDAR: RefreshConfig(
        source=DataSource.EARNINGS_CALENDAR,
        refresh_interval_minutes=1440,
        staleness_threshold_minutes=2880,
        staleness_penalty_points=3.0,
        is_critical=False
    ),
    
    # Social - StockTwits
    DataSource.STOCKTWITS_SENTIMENT: RefreshConfig(
        source=DataSource.STOCKTWITS_SENTIMENT,
        refresh_interval_minutes=30,
        staleness_threshold_minutes=120,
        staleness_penalty_points=2.0,
        is_critical=False
    ),
    
    # Social - Discord (r6: Added to match Addendum B)
    DataSource.DISCORD_SENTIMENT: RefreshConfig(
        source=DataSource.DISCORD_SENTIMENT,
        refresh_interval_minutes=15,
        staleness_threshold_minutes=60,
        staleness_penalty_points=1.0,
        is_critical=False
    ),
    
    # Social - Telegram (r6: Added to match Addendum B)
    DataSource.TELEGRAM_SENTIMENT: RefreshConfig(
        source=DataSource.TELEGRAM_SENTIMENT,
        refresh_interval_minutes=15,
        staleness_threshold_minutes=60,
        staleness_penalty_points=1.0,
        is_critical=False
    ),
    
    # Web3 - CEX flows
    DataSource.CEX_FLOWS: RefreshConfig(
        source=DataSource.CEX_FLOWS,
        refresh_interval_minutes=60,
        staleness_threshold_minutes=240,
        staleness_penalty_points=4.0,
        is_critical=False
    ),
    
    # Governance
    DataSource.INSIDER_TRANSACTIONS: RefreshConfig(
        source=DataSource.INSIDER_TRANSACTIONS,
        refresh_interval_minutes=1440,  # Daily
        staleness_threshold_minutes=4320,  # 3 days
        staleness_penalty_points=2.0,
        is_critical=False
    ),
    DataSource.SEC_FILINGS: RefreshConfig(
        source=DataSource.SEC_FILINGS,
        refresh_interval_minutes=1440,  # Daily
        staleness_threshold_minutes=2880,  # 2 days
        staleness_penalty_points=3.0,
        is_critical=False
    ),
}
```

---

## Staleness Detection

```python
@dataclass
class DataFreshness:
    """Freshness status of a data source."""
    source: DataSource
    last_update: Optional[datetime]
    age_seconds: float
    is_stale: bool
    staleness_penalty: float
    is_critical: bool
    status: str  # 'fresh', 'warning', 'stale', 'missing'


class StalenessChecker:
    """
    Check and track data freshness across all sources.
    
    NOTE: This is different from DataSynchronizer in Core OS.
    - StalenessChecker: Tracks age of data sources over time
    - DataSynchronizer: Ensures snapshot consistency for a single scoring run
    """
    
    def __init__(self):
        self.last_updates: Dict[DataSource, datetime] = {}
        self.update_history: Dict[DataSource, List[datetime]] = {}
    
    def record_update(self, source: DataSource, timestamp: datetime = None):
        """Record a data update."""
        ts = timestamp or utc_now()
        ts = to_utc(ts)
        
        self.last_updates[source] = ts
        
        if source not in self.update_history:
            self.update_history[source] = []
        self.update_history[source].append(ts)
        
        # Keep last 100 updates for metrics
        self.update_history[source] = self.update_history[source][-100:]
    
    def check_freshness(self, source: DataSource) -> DataFreshness:
        """Check freshness of a single data source."""
        config = REFRESH_CONFIGS.get(source)
        
        if config is None:
            return DataFreshness(
                source=source,
                last_update=None,
                age_seconds=float('inf'),
                is_stale=True,
                staleness_penalty=5.0,
                is_critical=False,
                status='unknown'
            )
        
        last_update = self.last_updates.get(source)
        
        if last_update is None:
            return DataFreshness(
                source=source,
                last_update=None,
                age_seconds=float('inf'),
                is_stale=True,
                staleness_penalty=config.staleness_penalty_points,
                is_critical=config.is_critical,
                status='missing'
            )
        
        age_seconds = (utc_now() - last_update).total_seconds()
        threshold_seconds = config.staleness_threshold_minutes * 60
        warning_seconds = config.refresh_interval_minutes * 60 * 2  # 2x refresh interval
        
        is_stale = age_seconds > threshold_seconds
        
        if is_stale:
            status = 'stale'
            penalty = config.staleness_penalty_points
        elif age_seconds > warning_seconds:
            status = 'warning'
            penalty = config.staleness_penalty_points * 0.5
        else:
            status = 'fresh'
            penalty = 0.0
        
        return DataFreshness(
            source=source,
            last_update=last_update,
            age_seconds=age_seconds,
            is_stale=is_stale,
            staleness_penalty=penalty,
            is_critical=config.is_critical,
            status=status
        )
    
    def check_all(self) -> Dict[DataSource, DataFreshness]:
        """Check freshness of all data sources."""
        return {source: self.check_freshness(source) for source in DataSource}
    
    def get_critical_stale(self) -> List[DataSource]:
        """Get list of critical data sources that are stale."""
        return [
            source for source, freshness in self.check_all().items()
            if freshness.is_stale and freshness.is_critical
        ]
    
    def get_total_staleness_penalty(self) -> float:
        """Get total penalty from all stale sources."""
        return sum(f.staleness_penalty for f in self.check_all().values())
    
    def can_score(self) -> Dict:
        """Check if scoring is allowed given data freshness."""
        critical_stale = self.get_critical_stale()
        total_penalty = self.get_total_staleness_penalty()
        
        return {
            'can_score': len(critical_stale) == 0,
            'critical_stale': [s.value for s in critical_stale],
            'total_penalty': round(total_penalty, 1),
            'recommendation': 'OK' if len(critical_stale) == 0 else f'Refresh: {", ".join(s.value for s in critical_stale)}'
        }
```

---

## Token Unlock Tracking

```python
@dataclass
class TokenUnlock:
    """A scheduled token unlock event."""
    token: str
    unlock_date: datetime
    amount: float
    pct_of_supply: float
    unlock_type: str  # 'team', 'investor', 'ecosystem', 'foundation'
    recipient: str
    cliff_end: bool = False
    
    @property
    def days_until(self) -> int:
        return (self.unlock_date - utc_now()).days


class TokenUnlockTracker:
    """
    Track upcoming token unlocks for crypto assets.
    
    Critical for catalyst_risk in Web3 assets.
    """
    
    def __init__(self):
        self.unlocks: Dict[str, List[TokenUnlock]] = {}  # token -> unlocks
    
    def add_unlock(self, unlock: TokenUnlock):
        """Add an unlock to tracking."""
        token = unlock.token.upper()
        if token not in self.unlocks:
            self.unlocks[token] = []
        self.unlocks[token].append(unlock)
        self.unlocks[token].sort(key=lambda u: u.unlock_date)
    
    def get_upcoming(self, token: str, days: int = 30) -> List[TokenUnlock]:
        """Get upcoming unlocks for a token within N days."""
        token = token.upper()
        if token not in self.unlocks:
            return []
        
        cutoff = utc_now() + timedelta(days=days)
        return [u for u in self.unlocks[token] 
                if utc_now() <= u.unlock_date <= cutoff]
    
    def get_next_unlock(self, token: str) -> Optional[TokenUnlock]:
        """Get the next upcoming unlock for a token."""
        upcoming = self.get_upcoming(token, days=365)
        return upcoming[0] if upcoming else None
    
    def get_alerts(self, days_warning: int = 7, min_pct: float = 2.0) -> List[Dict]:
        """Get alerts for significant upcoming unlocks."""
        alerts = []
        cutoff = utc_now() + timedelta(days=days_warning)
        
        for token, unlocks in self.unlocks.items():
            for unlock in unlocks:
                if utc_now() <= unlock.unlock_date <= cutoff:
                    if unlock.pct_of_supply >= min_pct:
                        severity = 'CRITICAL' if unlock.pct_of_supply >= 5 else 'HIGH' if unlock.pct_of_supply >= 3 else 'MEDIUM'
                        alerts.append({
                            'token': token,
                            'date': format_timestamp(unlock.unlock_date),
                            'days_until': unlock.days_until,
                            'pct_of_supply': unlock.pct_of_supply,
                            'unlock_type': unlock.unlock_type,
                            'severity': severity,
                            'message': f'{token}: {unlock.pct_of_supply:.1f}% unlock in {unlock.days_until} days ({unlock.unlock_type})'
                        })
        
        return sorted(alerts, key=lambda a: a['days_until'])
```

---

## Retraining Triggers

```python
@dataclass
class RetrainingTrigger:
    """A condition that triggers model retraining."""
    name: str
    threshold: float
    current_value: float
    triggered: bool
    description: str


class RetrainingManager:
    """
    Manage ML model retraining schedules.
    
    Coordinates with Addendum A (ML Classification) for regime model retraining.
    
    IMPORTANT (r8): These retraining triggers are designed for a FUTURE trained ML model.
    The current implementation in Addendum A uses a heuristic expert system (threshold-based
    rules), not a trained model. Therefore:
    
    - The triggers below will become relevant when the system is upgraded to use
      a trained classifier (Random Forest, XGBoost, etc.)
    - Until then, these metrics still provide useful monitoring signals about regime
      volatility and system accuracy, even if actual retraining is not performed
    - When a trained model is deployed, these triggers should gate the retraining pipeline
    """
    
    # Trigger thresholds
    ACCURACY_THRESHOLD = 0.85
    MAX_DAYS_SINCE_TRAINING = 90
    NEW_SAMPLES_THRESHOLD = 500
    REGIME_CHANGE_COUNT_THRESHOLD = 10  # Regime changes in last 30 days
    
    def __init__(self):
        self.last_training_date: Optional[datetime] = None
        self.new_samples_since_training: int = 0
        self.current_accuracy: float = 1.0
        self.regime_change_count_30d: int = 0
        self.training_history: List[Dict] = []
    
    def record_sample(self):
        """Record a new training sample."""
        self.new_samples_since_training += 1
    
    def record_regime_change(self):
        """Record a regime change event."""
        self.regime_change_count_30d += 1
    
    def update_accuracy(self, accuracy: float):
        """Update current model accuracy."""
        self.current_accuracy = accuracy
    
    def check_triggers(self) -> List[RetrainingTrigger]:
        """Check all retraining triggers."""
        triggers = []
        
        # Trigger 1: Accuracy drop
        triggers.append(RetrainingTrigger(
            name='accuracy_drop',
            threshold=self.ACCURACY_THRESHOLD,
            current_value=self.current_accuracy,
            triggered=self.current_accuracy < self.ACCURACY_THRESHOLD,
            description=f'Accuracy {self.current_accuracy:.1%} below {self.ACCURACY_THRESHOLD:.1%} threshold'
        ))
        
        # Trigger 2: Time elapsed
        if self.last_training_date:
            days_since = (utc_now() - self.last_training_date).days
        else:
            days_since = 999
        
        triggers.append(RetrainingTrigger(
            name='time_elapsed',
            threshold=self.MAX_DAYS_SINCE_TRAINING,
            current_value=days_since,
            triggered=days_since > self.MAX_DAYS_SINCE_TRAINING,
            description=f'{days_since} days since last training (max: {self.MAX_DAYS_SINCE_TRAINING})'
        ))
        
        # Trigger 3: New samples accumulated
        triggers.append(RetrainingTrigger(
            name='new_samples',
            threshold=self.NEW_SAMPLES_THRESHOLD,
            current_value=self.new_samples_since_training,
            triggered=self.new_samples_since_training >= self.NEW_SAMPLES_THRESHOLD,
            description=f'{self.new_samples_since_training} new samples (threshold: {self.NEW_SAMPLES_THRESHOLD})'
        ))
        
        # Trigger 4: High regime volatility
        triggers.append(RetrainingTrigger(
            name='regime_volatility',
            threshold=self.REGIME_CHANGE_COUNT_THRESHOLD,
            current_value=self.regime_change_count_30d,
            triggered=self.regime_change_count_30d >= self.REGIME_CHANGE_COUNT_THRESHOLD,
            description=f'{self.regime_change_count_30d} regime changes in 30 days'
        ))
        
        return triggers
    
    def should_retrain(self) -> Dict:
        """Determine if retraining is needed."""
        triggers = self.check_triggers()
        triggered = [t for t in triggers if t.triggered]
        
        return {
            'should_retrain': len(triggered) > 0,
            'triggered_reasons': [t.name for t in triggered],
            'triggers': [
                {'name': t.name, 'triggered': t.triggered, 'description': t.description}
                for t in triggers
            ]
        }
    
    def record_training(self, model_version: str, metrics: Dict):
        """Record a completed training run."""
        self.last_training_date = utc_now()
        self.new_samples_since_training = 0
        self.regime_change_count_30d = 0
        
        self.training_history.append({
            'timestamp': format_timestamp(utc_now()),
            'model_version': model_version,
            'metrics': metrics
        })
        
        # Keep last 50 training records
        self.training_history = self.training_history[-50:]
```

---

## Calibration Tracking

Uses the `BlowupDefinition` and `CalibrationOutcome` from Core OS:

```python
@dataclass
class CalibrationConfig:
    """Configuration for calibration tracking."""
    lookback_days: int = 30
    high_score_threshold: float = 70.0
    
    # Blowup definitions (from Core OS)
    blowup_vol_ratio: float = 2.0        # Realized vol >= 2x historical
    blowup_single_day_loss: float = 5.0  # >= 5% single day loss
    blowup_gap_down: float = 15.0        # >= 15% gap down


@dataclass
class CalibrationOutcome:
    """
    Outcome tracking for a flagged security.
    
    SCHEMA NOTE (r6): Field names MUST match Core OS CalibrationOutcome exactly.
    Core OS uses: max_drawdown, max_single_day_loss, max_gap_down (no _pct suffix)
    This ensures interoperability between Core OS and this operations module.
    """
    ticker: str
    flag_date: datetime
    flag_score: float
    
    # Observed outcomes (within lookback period)
    # NOTE: Field names match Core OS exactly (no _pct suffix)
    max_drawdown: float = 0.0
    max_single_day_loss: float = 0.0
    max_gap_down: float = 0.0
    realized_vol_ratio: float = 1.0
    had_trading_halt: bool = False
    had_credit_event: bool = False
    
    def is_blowup(self, config: CalibrationConfig) -> bool:
        """Determine if this qualifies as a blowup."""
        return (
            self.realized_vol_ratio >= config.blowup_vol_ratio or
            self.max_single_day_loss >= config.blowup_single_day_loss or
            self.max_gap_down >= config.blowup_gap_down or
            self.had_trading_halt or
            self.had_credit_event
        )
    
    def get_label(self, config: CalibrationConfig) -> str:
        """
        Get calibration label.
        
        TRUE_POSITIVE: Flagged HIGH and blew up
        FALSE_POSITIVE: Flagged HIGH and did NOT blow up
        TRUE_NEGATIVE: NOT flagged HIGH and did NOT blow up
        FALSE_NEGATIVE: NOT flagged HIGH and DID blow up
        """
        was_flagged_high = self.flag_score >= config.high_score_threshold
        blew_up = self.is_blowup(config)
        
        if was_flagged_high and blew_up:
            return "TRUE_POSITIVE"
        elif was_flagged_high and not blew_up:
            return "FALSE_POSITIVE"
        elif not was_flagged_high and not blew_up:
            return "TRUE_NEGATIVE"
        else:
            return "FALSE_NEGATIVE"


class CalibrationTracker:
    """
    Track system calibration and accuracy over time.
    """
    
    def __init__(self, config: CalibrationConfig = None):
        self.config = config or CalibrationConfig()
        self.outcomes: List[CalibrationOutcome] = []
        self.bootstrap_data: List[CalibrationOutcome] = []  # Historical priors
    
    def add_bootstrap_data(self, outcomes: List[CalibrationOutcome]):
        """
        Add historical "known blowup" data to bootstrap calibration.
        
        Prevents cold-start problem on Day 1.
        """
        self.bootstrap_data.extend(outcomes)
    
    def add_outcome(self, outcome: CalibrationOutcome):
        """Add a new calibration outcome."""
        self.outcomes.append(outcome)
    
    def get_all_outcomes(self) -> List[CalibrationOutcome]:
        """Get all outcomes including bootstrap data."""
        return self.bootstrap_data + self.outcomes
    
    def compute_metrics(self) -> Dict:
        """Compute calibration metrics."""
        all_outcomes = self.get_all_outcomes()
        
        if len(all_outcomes) < 10:
            return {
                'status': 'insufficient_data',
                'message': f'Need at least 10 outcomes, have {len(all_outcomes)}',
                'outcomes_count': len(all_outcomes)
            }
        
        labels = [o.get_label(self.config) for o in all_outcomes]
        
        tp = labels.count('TRUE_POSITIVE')
        fp = labels.count('FALSE_POSITIVE')
        tn = labels.count('TRUE_NEGATIVE')
        fn = labels.count('FALSE_NEGATIVE')
        
        total = len(labels)
        
        # Metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        accuracy = (tp + tn) / total if total > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # False positive rate (what % of safe stocks we flag)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        
        return {
            'status': 'ok',
            'total_outcomes': total,
            'live_outcomes': len(self.outcomes),
            'bootstrap_outcomes': len(self.bootstrap_data),
            'confusion_matrix': {
                'true_positives': tp,
                'false_positives': fp,
                'true_negatives': tn,
                'false_negatives': fn
            },
            'metrics': {
                'precision': round(precision, 3),
                'recall': round(recall, 3),
                'accuracy': round(accuracy, 3),
                'f1_score': round(f1, 3),
                'false_positive_rate': round(fpr, 3)
            },
            'interpretation': {
                'precision': f'{precision:.1%} of HIGH flags were actual blowups',
                'recall': f'{recall:.1%} of blowups were flagged HIGH',
                'false_positive_rate': f'{fpr:.1%} of safe stocks were incorrectly flagged'
            }
        }
```

---

## System Health Monitor

```python
class SystemHealthMonitor:
    """Monitor overall system health."""
    
    def __init__(self):
        self.staleness_checker = StalenessChecker()
        self.retraining_manager = RetrainingManager()
        self.calibration_tracker = CalibrationTracker()
        self.error_log: List[Dict] = []
    
    def log_error(self, component: str, error: str, severity: str = 'ERROR'):
        """Log an error."""
        self.error_log.append({
            'timestamp': format_timestamp(utc_now()),
            'component': component,
            'error': error,
            'severity': severity
        })
        self.error_log = self.error_log[-500:]  # Keep last 500
    
    def get_health_report(self) -> Dict:
        """Generate comprehensive health report."""
        # Data freshness
        freshness = self.staleness_checker.check_all()
        stale_sources = [s.value for s, f in freshness.items() if f.is_stale]
        critical_stale = self.staleness_checker.get_critical_stale()
        
        # Retraining status
        retrain = self.retraining_manager.should_retrain()
        
        # Calibration
        calibration = self.calibration_tracker.compute_metrics()
        
        # Recent errors
        recent_errors = [e for e in self.error_log 
                        if e['severity'] in ['ERROR', 'CRITICAL']][-10:]
        
        # Overall status
        if critical_stale:
            overall = 'CRITICAL'
        elif stale_sources or retrain['should_retrain']:
            overall = 'WARNING'
        elif recent_errors:
            overall = 'DEGRADED'
        else:
            overall = 'HEALTHY'
        
        return {
            'overall_status': overall,
            'timestamp': format_timestamp(utc_now()),
            'data_freshness': {
                'stale_sources': stale_sources,
                'critical_stale': [s.value for s in critical_stale],
                'total_penalty': self.staleness_checker.get_total_staleness_penalty()
            },
            'retraining': retrain,
            'calibration': calibration,
            'recent_errors': recent_errors
        }
```

---

## Bundle Version Management

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
    """
    Verify all bundle files exist and have matching versions.
    """
    import os
    import hashlib
    
    results = {
        'valid': True,
        'bundle_version': BUNDLE_VERSION,
        'files': {},
        'errors': []
    }
    
    for filename in BUNDLE_FILES:
        filepath = os.path.join(bundle_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
                # Check version
                if f'**Version:** {BUNDLE_VERSION}' in content:
                    version_ok = True
                else:
                    version_ok = False
                    results['valid'] = False
                    results['errors'].append(f'{filename}: version mismatch')
                
                # Compute hash
                file_hash = hashlib.md5(content.encode()).hexdigest()[:8]
                
                results['files'][filename] = {
                    'exists': True,
                    'version_ok': version_ok,
                    'hash': file_hash,
                    'size_bytes': len(content.encode())
                }
                
        except FileNotFoundError:
            results['files'][filename] = {
                'exists': False,
                'version_ok': False,
                'hash': None,
                'size_bytes': 0
            }
            results['valid'] = False
            results['errors'].append(f'{filename}: file not found')
    
    return results
```

---

## Operational Checklists

### Daily Checklist

```
DAILY OPERATIONS CHECKLIST - Mine Detector OS
=============================================

PRE-MARKET (06:00 UTC / 01:00 ET)
---------------------------------
[ ] Verify all data feeds are live
    - Price feeds: streaming
    - Options chain: last update <15 min
    - Credit spreads: last update <4 hours
    
[ ] Check overnight batch jobs completed
    - Short interest update
    - 13F processing (if filing date)
    - Token unlock calendar sync
    
[ ] Review triggered alerts from overnight
    - Any new HIGH/CRITICAL scores?
    - Any earnings surprises?
    - Any token unlock alerts?

[ ] Verify ML model health
    - Regime classification working
    - No imputation warnings

MARKET OPEN (09:30 ET)
----------------------
[ ] Confirm real-time streaming active
[ ] Monitor first 30 minutes for anomalies
[ ] Check API rate limits not exceeded

MARKET CLOSE (16:00 ET)  
-----------------------
[ ] Archive daily scores for calibration
[ ] Run calibration update batch
[ ] Generate daily summary report
[ ] Review any new flagged positions

POST-MARKET
-----------
[ ] Process any after-hours news events
[ ] Update earnings calendar for tomorrow
[ ] Check data freshness for all sources
[ ] Clear any resolved alerts
```

### Weekly Checklist

```
WEEKLY OPERATIONS CHECKLIST
===========================

MONDAY
------
[ ] Review prior week calibration metrics
    - Precision target: >75%
    - Recall target: >70%
    
[ ] Update short interest data
[ ] Review any 13F filings from prior week
[ ] Check token unlock calendar for week ahead

WEDNESDAY
---------
[ ] Mid-week accuracy check
[ ] Review sentiment trend changes
[ ] Verify all API connections healthy

FRIDAY
------
[ ] Generate weekly calibration report
[ ] Archive weekly data
[ ] Review retraining triggers
[ ] Plan any weekend maintenance
```

### Monthly Checklist

```
MONTHLY OPERATIONS CHECKLIST
============================

FIRST WEEK
----------
[ ] Full calibration review
    - Analyze false positives/negatives
    - Adjust thresholds if needed
    
[ ] Evaluate retraining need
[ ] Review API cost/usage
[ ] Check data source reliability

MID-MONTH
---------
[ ] Performance benchmarking
[ ] Documentation updates
[ ] User feedback review

END OF MONTH
------------
[ ] Full system audit
[ ] Backup verification
[ ] Security review
[ ] Capacity planning
```

---

## Dashboard Output

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

ALERTS
--------------------------------------------------------------------------------
[INFO] Next token unlock: ARB 2.1% in 5 days
[INFO] Earnings week: 127 S&P 500 companies reporting

================================================================================
```

---

---

## Future Enhancements to be Evaluated

The following topics have been identified for potential future development:

- **Dynamic blowup thresholds:** Make BlowupDefinition asset-class specific. Current thresholds (e.g., 15% gap-down) are calibrated for US large-cap equities. Crypto assets routinely experience 15-20% swings that don't constitute "blowups." Consider:
  - US Large Cap: 15% gap-down threshold
  - US Small Cap: 20% gap-down threshold  
  - Crypto/DeFi: 30% gap-down threshold
  - ADR Emerging: 20% gap-down threshold

- **Backtesting framework:** Add ability to run historical simulations against past data. Current calibration tracking is forward-looking only. A backtesting module would enable:
  - Walk-forward optimization of weights and thresholds
  - Historical precision/recall analysis by market regime
  - Strategy validation before deployment
  - Integration with Addendum A's regime classification for regime-conditional backtests

---

*Addendum E - Mine Detector OS v2026-01-30-r9*
