# Mine Detector OS -- Addendum A: ML Classification

> Machine learning regime classification for dynamic risk assessment. Provides probabilistic regime detection with proper state management.

**Version:** 2026-01-30-r9

**Cross-References:**
- Core OS: mine-detector-os.md (interface contract, weight adjustments, RiskCategory enum)
- Addendum E: mine-detector-addendum-e-maintenance-operations.md (retraining schedules)

---

## Overview

This addendum provides ML-based regime classification that:

1. Identifies market regimes (RISK_ON, RISK_OFF, TRANSITION)
2. Returns properly normalized probabilities (sum to 1.0)
3. Maintains persistent state across calls to prevent whipsawing
4. Handles missing data with regime-conditional imputation
5. Adjusts Mine Detector weights based on regime

---

## Interface Contract

Implements the Core OS ML Classification interface:

```python
def classify_regime(features: Dict[str, float], 
                    classifier_state: 'RegimeClassifierState') -> Dict:
    """
    Classify current market regime.
    
    IMPORTANT: The classifier_state parameter MUST be a persistent object
    that is reused across all calls. Creating a new state each call will
    break regime continuity and bias features.
    
    Args:
        features: Dict of feature name to value
        classifier_state: Persistent state object
    
    Returns:
        {
            'regime': str,           # RISK_ON, RISK_OFF, TRANSITION
            'confidence': float,     # 0.0 to 1.0
            'probabilities': Dict,   # Per-regime probs (sum to 1.0)
            'features_used': List,   # Features driving classification
            'regime_tenure_days': int
        }
    """
```

---

## Imports and Dependencies

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timezone, timedelta
import math

# Import from Core OS shared module
from mine_detector_shared import utc_now, to_utc, format_timestamp, RiskCategory
```

---

## Regime Enum

```python
class Regime(Enum):
    """Market regime classifications."""
    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    TRANSITION = "TRANSITION"
```

---

## Feature Engineering

```python
@dataclass
class RegimeFeatures:
    """Features used for regime classification."""
    
    # Volatility
    vix_level: Optional[float] = None
    vix_percentile_1y: Optional[float] = None
    vix_term_structure: Optional[float] = None  # VIX - VIX3M
    realized_vol_20d: Optional[float] = None
    
    # Credit
    hy_spread: Optional[float] = None           # High yield spread (bps)
    ig_spread: Optional[float] = None           # Investment grade (bps)
    credit_spread_change_5d: Optional[float] = None
    
    # Equity
    spx_vs_200dma: Optional[float] = None       # % above/below
    advance_decline_ratio: Optional[float] = None
    new_highs_minus_lows: Optional[float] = None
    
    # Flows
    equity_fund_flows_4w: Optional[float] = None
    bond_fund_flows_4w: Optional[float] = None
    
    # Sentiment
    put_call_ratio: Optional[float] = None
    aaii_bull_bear_spread: Optional[float] = None


class FeatureEngineer:
    """Engineer and normalize features for classification."""
    
    FEATURE_RANGES = {
        'vix_level': (10, 80),
        'vix_percentile_1y': (0, 100),
        'vix_term_structure': (-15, 15),
        'realized_vol_20d': (5, 60),
        'hy_spread': (250, 1500),
        'ig_spread': (50, 400),
        'credit_spread_change_5d': (-100, 100),
        'spx_vs_200dma': (-30, 30),
        'advance_decline_ratio': (0.3, 3.0),
        'new_highs_minus_lows': (-500, 500),
        'equity_fund_flows_4w': (-50, 50),
        'bond_fund_flows_4w': (-50, 50),
        'put_call_ratio': (0.5, 1.5),
        'aaii_bull_bear_spread': (-40, 40)
    }
    
    def normalize_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Normalize features to 0-1 range."""
        normalized = {}
        for name, (min_val, max_val) in self.FEATURE_RANGES.items():
            raw = features.get(name)
            if raw is not None:
                clipped = max(min_val, min(max_val, raw))
                normalized[name] = (clipped - min_val) / (max_val - min_val)
            else:
                normalized[name] = None
        return normalized
    
    def compute_derived_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Compute derived composite features."""
        derived = {}
        
        vix = features.get('vix_level')
        realized = features.get('realized_vol_20d')
        if vix and realized and realized > 0:
            derived['vol_regime'] = vix / realized
        
        hy = features.get('hy_spread')
        ig = features.get('ig_spread')
        if hy and ig and ig > 0:
            derived['credit_stress'] = hy / ig
        
        return derived
```

---

## Regime-Conditional Imputation

When features are missing, impute using regime-specific historical medians:

```python
class RegimeConditionalImputer:
    """
    Impute missing features using regime-conditional distributions.
    
    Different regimes have different typical values. For example,
    VIX is typically higher in RISK_OFF regimes.
    """
    
    REGIME_MEDIANS = {
        Regime.RISK_ON: {
            'vix_level': 14,
            'vix_percentile_1y': 25,
            'hy_spread': 350,
            'ig_spread': 90,
            'spx_vs_200dma': 5.0,
            'put_call_ratio': 0.85,
            'advance_decline_ratio': 1.5,
            'equity_fund_flows_4w': 15,
            'aaii_bull_bear_spread': 10
        },
        Regime.RISK_OFF: {
            'vix_level': 28,
            'vix_percentile_1y': 75,
            'hy_spread': 550,
            'ig_spread': 150,
            'spx_vs_200dma': -3.0,
            'put_call_ratio': 1.1,
            'advance_decline_ratio': 0.7,
            'equity_fund_flows_4w': -20,
            'aaii_bull_bear_spread': -15
        },
        Regime.TRANSITION: {
            'vix_level': 20,
            'vix_percentile_1y': 50,
            'hy_spread': 420,
            'ig_spread': 110,
            'spx_vs_200dma': 1.0,
            'put_call_ratio': 0.95,
            'advance_decline_ratio': 1.0,
            'equity_fund_flows_4w': 0,
            'aaii_bull_bear_spread': 0
        }
    }
    
    def __init__(self):
        self.last_known_values: Dict[str, float] = {}
    
    def impute(self, features: Dict[str, Optional[float]], 
               regime_hint: Regime = Regime.TRANSITION) -> Tuple[Dict[str, float], List[str]]:
        """
        Impute missing values.
        
        Priority:
        1. Last known value (if available)
        2. Regime-conditional median
        3. TRANSITION median as ultimate fallback
        """
        medians = self.REGIME_MEDIANS.get(regime_hint, self.REGIME_MEDIANS[Regime.TRANSITION])
        
        imputed = {}
        log = []
        
        for key, value in features.items():
            if value is not None:
                imputed[key] = value
                self.last_known_values[key] = value
            else:
                # Try last known
                if key in self.last_known_values:
                    imputed[key] = self.last_known_values[key]
                    log.append(f"{key}: last known")
                # Regime-conditional median
                elif key in medians:
                    imputed[key] = medians[key]
                    log.append(f"{key}: {regime_hint.value} median")
                # Ultimate fallback
                else:
                    fallback = self.REGIME_MEDIANS[Regime.TRANSITION].get(key, 0)
                    imputed[key] = fallback
                    log.append(f"{key}: fallback")
        
        return imputed, log
```

---

## Classifier State (Persistent)

```python
@dataclass
class RegimeClassifierState:
    """
    Persistent state for the regime classifier.
    
    CRITICAL: This object MUST be created once and reused across ALL calls.
    Creating a new state each call will:
    - Reset regime tenure (breaking bias calculations)
    - Lose imputation history
    - Cause regime whipsawing
    
    Usage:
        state = RegimeClassifierState()  # Create ONCE
        for _ in trading_days:
            result = classify_regime(features, state)  # Reuse
    """
    current_regime: Regime = Regime.TRANSITION
    regime_start_date: datetime = field(default_factory=utc_now)
    regime_tenure_days: int = 0
    last_classification_date: Optional[datetime] = None
    
    imputer: RegimeConditionalImputer = field(default_factory=RegimeConditionalImputer)
    regime_history: List[Dict] = field(default_factory=list)
    
    def update_regime(self, new_regime: Regime):
        """Update regime and track history."""
        now = utc_now()
        
        if new_regime != self.current_regime:
            # Record change
            self.regime_history.append({
                'from': self.current_regime.value,
                'to': new_regime.value,
                'at': format_timestamp(now),
                'tenure': self.regime_tenure_days
            })
            self.regime_history = self.regime_history[-50:]  # Keep last 50
            
            # Reset
            self.current_regime = new_regime
            self.regime_start_date = now
            self.regime_tenure_days = 0
        else:
            # Increment tenure
            if self.last_classification_date:
                days = (now - self.last_classification_date).days
                self.regime_tenure_days += max(0, days)
        
        self.last_classification_date = now
    
    def get_regime_bias(self) -> float:
        """
        Bias strength toward current regime based on tenure.
        Longer tenure = stronger resistance to regime change.
        """
        if self.regime_tenure_days < 3:
            return 0.0
        elif self.regime_tenure_days < 7:
            return 0.05
        elif self.regime_tenure_days < 14:
            return 0.10
        elif self.regime_tenure_days < 30:
            return 0.12
        else:
            return 0.15
```

---

## Regime Classifier

```python
class RegimeClassifier:
    """
    Heuristic-based regime classifier with proper probability normalization.
    
    IMPLEMENTATION NOTE (r7):
    This is currently an EXPERT SYSTEM using threshold-based heuristics,
    not a trained Machine Learning model. The "ML" in the addendum title
    refers to the intended architecture, not the current implementation.
    
    Current approach:
    - Uses hardcoded if/else rules based on VIX, credit spreads, etc.
    - Applies softmax normalization for proper probability output
    - Includes regime bias/hysteresis to prevent whipsawing
    
    Production upgrade path:
    - Replace _compute_raw_scores() with a trained model (Random Forest, XGBoost)
    - Keep the same interface contract (inputs/outputs unchanged)
    - Retrain using historical regime labels from Addendum E calibration data
    """
    
    REGIME_CHANGE_THRESHOLD = 0.65  # Min confidence to change
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
    
    def classify(self, raw_features: Dict[str, float], 
                 state: RegimeClassifierState) -> Dict:
        """
        Classify current regime.
        
        Args:
            raw_features: Feature dict (some may be None)
            state: Persistent state object
        
        Returns:
            Interface-compliant dict with normalized probabilities.
        """
        # Impute missing data
        imputed, imputation_log = state.imputer.impute(
            raw_features,
            regime_hint=state.current_regime
        )
        
        # Compute raw scores
        raw_scores = self._compute_raw_scores(imputed)
        
        # Normalize to probabilities (sum to 1.0)
        probabilities = self._softmax_normalize(raw_scores)
        
        # Apply regime bias
        biased_probs = self._apply_regime_bias(probabilities, state)
        
        # Select regime
        regime, confidence = self._select_regime(biased_probs, state)
        
        # Update state
        state.update_regime(regime)
        
        # Identify key features
        features_used = self._identify_key_features(imputed, regime)
        
        return {
            'regime': regime.value,
            'confidence': round(confidence, 3),
            'probabilities': {k.value: round(v, 3) for k, v in biased_probs.items()},
            'features_used': features_used,
            'imputation_log': imputation_log,
            'regime_tenure_days': state.regime_tenure_days,
            'bias_applied': state.get_regime_bias()
        }
    
    def _compute_raw_scores(self, features: Dict[str, float]) -> Dict[Regime, float]:
        """
        Compute raw (unnormalized) scores for each regime.
        These are NOT probabilities yet.
        """
        risk_on = 50.0
        risk_off = 50.0
        
        # VIX
        vix = features.get('vix_level', 20)
        if vix < 15:
            risk_on += 20
            risk_off -= 15
        elif vix < 18:
            risk_on += 10
            risk_off -= 5
        elif vix > 30:
            risk_on -= 20
            risk_off += 25
        elif vix > 25:
            risk_on -= 10
            risk_off += 15
        
        # Credit spreads
        hy = features.get('hy_spread', 400)
        if hy < 350:
            risk_on += 15
            risk_off -= 10
        elif hy > 550:
            risk_on -= 15
            risk_off += 20
        elif hy > 450:
            risk_on -= 5
            risk_off += 10
        
        # Price vs 200-DMA
        spx_ma = features.get('spx_vs_200dma', 0)
        if spx_ma > 8:
            risk_on += 15
            risk_off -= 10
        elif spx_ma > 3:
            risk_on += 8
            risk_off -= 5
        elif spx_ma < -8:
            risk_on -= 15
            risk_off += 18
        elif spx_ma < -3:
            risk_on -= 8
            risk_off += 10
        
        # Fund flows
        flows = features.get('equity_fund_flows_4w', 0)
        if flows > 25:
            risk_on += 10
            risk_off -= 8
        elif flows < -25:
            risk_on -= 10
            risk_off += 12
        
        # Ensure positive
        risk_on = max(1, risk_on)
        risk_off = max(1, risk_off)
        
        # Transition based on uncertainty
        diff = abs(risk_on - risk_off)
        transition = max(1, 100 - diff)
        
        return {
            Regime.RISK_ON: risk_on,
            Regime.RISK_OFF: risk_off,
            Regime.TRANSITION: transition
        }
    
    def _softmax_normalize(self, raw_scores: Dict[Regime, float]) -> Dict[Regime, float]:
        """
        Convert raw scores to proper probabilities using softmax.
        Result is guaranteed to sum to 1.0.
        """
        temperature = 30.0  # Higher = more uniform
        
        # For numerical stability, subtract max
        max_score = max(raw_scores.values())
        exp_scores = {}
        for regime, score in raw_scores.items():
            exp_scores[regime] = math.exp((score - max_score) / temperature)
        
        total = sum(exp_scores.values())
        return {regime: exp_score / total for regime, exp_score in exp_scores.items()}
    
    def _apply_regime_bias(self, probs: Dict[Regime, float], 
                           state: RegimeClassifierState) -> Dict[Regime, float]:
        """Apply bias toward current regime to prevent whipsawing."""
        bias = state.get_regime_bias()
        if bias == 0:
            return probs
        
        current = state.current_regime
        biased = dict(probs)
        
        # Add bias to current
        biased[current] = min(0.95, biased[current] + bias)
        
        # Redistribute from others proportionally
        others_total = sum(p for r, p in probs.items() if r != current)
        if others_total > 0:
            for regime in biased:
                if regime != current:
                    reduction = bias * (probs[regime] / others_total)
                    biased[regime] = max(0.01, biased[regime] - reduction)
        
        # Renormalize to sum to 1.0
        total = sum(biased.values())
        return {r: p / total for r, p in biased.items()}
    
    def _select_regime(self, probs: Dict[Regime, float], 
                       state: RegimeClassifierState) -> Tuple[Regime, float]:
        """Select regime with hysteresis."""
        best = max(probs, key=probs.get)
        best_prob = probs[best]
        
        # Require threshold to change regime
        if best != state.current_regime:
            if best_prob < self.REGIME_CHANGE_THRESHOLD:
                return state.current_regime, probs[state.current_regime]
        
        return best, best_prob
    
    def _identify_key_features(self, features: Dict[str, float], 
                               regime: Regime) -> List[str]:
        """Identify features supporting the regime call."""
        key = []
        
        vix = features.get('vix_level', 20)
        hy = features.get('hy_spread', 400)
        spx = features.get('spx_vs_200dma', 0)
        
        if regime == Regime.RISK_ON:
            if vix < 18: key.append(f"vix={vix:.1f} (low)")
            if hy < 380: key.append(f"hy_spread={hy:.0f} (tight)")
            if spx > 3: key.append(f"spx_ma=+{spx:.1f}%")
        elif regime == Regime.RISK_OFF:
            if vix > 25: key.append(f"vix={vix:.1f} (elevated)")
            if hy > 480: key.append(f"hy_spread={hy:.0f} (wide)")
            if spx < -3: key.append(f"spx_ma={spx:.1f}%")
        else:
            key.append("mixed_signals")
        
        return key[:5]
```

---

## Global State Management

```python
# Global instances - create once, reuse always
_classifier_state: Optional[RegimeClassifierState] = None
_classifier: Optional[RegimeClassifier] = None


def get_classifier_state() -> RegimeClassifierState:
    """Get or create global classifier state."""
    global _classifier_state
    if _classifier_state is None:
        _classifier_state = RegimeClassifierState()
    return _classifier_state


def get_classifier() -> RegimeClassifier:
    """Get or create global classifier."""
    global _classifier
    if _classifier is None:
        _classifier = RegimeClassifier()
    return _classifier


def classify_regime(features: Dict[str, float], 
                    classifier_state: RegimeClassifierState = None) -> Dict:
    """
    Main entry point implementing Core OS interface.
    
    If no state provided, uses global singleton state.
    """
    state = classifier_state or get_classifier_state()
    classifier = get_classifier()
    return classifier.classify(features, state)


def reset_classifier_state():
    """Reset global state. Use for testing or reinitialization."""
    global _classifier_state
    _classifier_state = RegimeClassifierState()
```

---

## Integration with Core OS

```python
def get_regime_adjusted_weights(base_weights: Dict[RiskCategory, float],
                                 regime_result: Dict) -> Dict[RiskCategory, float]:
    """
    Adjust category weights based on regime classification.
    """
    from mine_detector_os import MacroOSIntegration
    
    regime = regime_result['regime']
    confidence = regime_result['confidence']
    
    # Scale adjustment by confidence
    blend = confidence if confidence >= 0.5 else confidence / 0.5
    
    integration = MacroOSIntegration()
    integration._current_regime = regime
    
    adjustments = integration.REGIME_WEIGHT_ADJUSTMENTS.get(regime, {})
    
    adjusted = {}
    for category, weight in base_weights.items():
        multiplier = adjustments.get(category, 1.0)
        blended = 1.0 + (multiplier - 1.0) * blend
        adjusted[category] = weight * blended
    
    # Renormalize
    total = sum(adjusted.values())
    return {k: round(v/total, 4) for k, v in adjusted.items()}
```

---

## Model Calibration

```python
@dataclass
class CalibrationMetrics:
    """Metrics for evaluating classifier performance."""
    accuracy: float
    precision_by_regime: Dict[str, float]
    recall_by_regime: Dict[str, float]
    regime_persistence: float
    false_transition_rate: float


class ModelCalibrator:
    """Calibrate and evaluate regime classifier."""
    
    def __init__(self):
        self.predictions: List[Dict] = []
        self.actuals: List[str] = []
    
    def record(self, prediction: Dict, actual: str):
        self.predictions.append(prediction)
        self.actuals.append(actual)
    
    def compute_metrics(self) -> CalibrationMetrics:
        """Compute calibration metrics."""
        if len(self.predictions) < 30:
            raise ValueError("Need >= 30 samples")
        
        correct = sum(1 for p, a in zip(self.predictions, self.actuals) if p['regime'] == a)
        accuracy = correct / len(self.predictions)
        
        regimes = ['RISK_ON', 'RISK_OFF', 'TRANSITION']
        precision = {}
        recall = {}
        
        for r in regimes:
            pred_idx = [i for i, p in enumerate(self.predictions) if p['regime'] == r]
            actual_idx = [i for i, a in enumerate(self.actuals) if a == r]
            tp = len(set(pred_idx) & set(actual_idx))
            precision[r] = tp / len(pred_idx) if pred_idx else 0.0
            recall[r] = tp / len(actual_idx) if actual_idx else 0.0
        
        return CalibrationMetrics(
            accuracy=round(accuracy, 3),
            precision_by_regime=precision,
            recall_by_regime=recall,
            regime_persistence=self._persistence(),
            false_transition_rate=self._false_transitions()
        )
    
    def _persistence(self) -> float:
        if not self.predictions:
            return 0.0
        transitions = sum(
            1 for i in range(1, len(self.predictions))
            if self.predictions[i]['regime'] != self.predictions[i-1]['regime']
        )
        return len(self.predictions) / max(1, transitions)
    
    def _false_transitions(self) -> float:
        if len(self.predictions) < 4:
            return 0.0
        transitions = 0
        reversed_t = 0
        for i in range(1, len(self.predictions) - 3):
            if self.predictions[i]['regime'] != self.predictions[i-1]['regime']:
                transitions += 1
                if self.predictions[i+3]['regime'] == self.predictions[i-1]['regime']:
                    reversed_t += 1
        return round(reversed_t / max(1, transitions), 3)
```

---

## Dashboard Output

```
================================================================================
                        REGIME CLASSIFICATION
                        2026-01-30 10:00 UTC
================================================================================

CURRENT REGIME: RISK_ON
Confidence: 0.72
Tenure: 15 days
Bias Applied: 0.12

PROBABILITIES (sum = 1.00)
--------------------------------------------------------------------------------
RISK_ON:     0.72  ████████████████████░░░░░░░░
RISK_OFF:    0.18  █████░░░░░░░░░░░░░░░░░░░░░░░
TRANSITION:  0.10  ███░░░░░░░░░░░░░░░░░░░░░░░░░

KEY FEATURES
--------------------------------------------------------------------------------
- vix=14.2 (low)
- hy_spread=340 (tight)
- spx_ma=+6.2%

WEIGHT ADJUSTMENTS
--------------------------------------------------------------------------------
Category              Base     Adjusted   Change
------------------    ------   --------   ------
solvency_risk         0.150    0.135      -10%
crowding_risk         0.120    0.144      +20%
momentum_risk         0.100    0.110      +10%

================================================================================
```

---

*Addendum A - Mine Detector OS v2026-01-30-r9*
