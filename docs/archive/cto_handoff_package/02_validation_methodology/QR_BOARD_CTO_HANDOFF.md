# QR Board CTO Handoff
## Layer 3: Analytics Engine & Validation Specifications

**Document Version:** 2.0  
**Date:** January 24, 2026  
**Prepared by:** QR Board (Quantitative Research Board)  
**Updated by:** QR Board (Gap Analysis Fixes)  
**For:** CTO Board â€” diboas-analytics Implementation  
**Status:** Ready for Implementation

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | QR Board | Initial release |
| 2.0 | 2026-01-24 | QR Board | Added negative Sharpe ratio explanation (GAP-013), Added proxy data disclaimer (GAP-014) |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Battle Test Engine](#2-battle-test-engine)
3. [Monte Carlo Simulation](#3-monte-carlo-simulation)
4. [Risk Metrics Calculations](#4-risk-metrics-calculations)
5. [Data Quality Assurance](#5-data-quality-assurance)
6. [Auto-Validation Framework](#6-auto-validation-framework)
7. [Adelaide Claims Validation](#7-adelaide-claims-validation)
8. [Anomaly Detection](#8-anomaly-detection)
9. [Proxy Data Methodology](#9-proxy-data-methodology)
10. [Output Schemas](#10-output-schemas)
11. [Configuration Templates](#11-configuration-templates)
12. [Implementation Checklist](#12-implementation-checklist)
13. [Appendices](#13-appendices)

---

## 1. Executive Summary

### 1.1 Document Purpose

This document specifies **Layer 3: Analytics** of the diboas-analytics data pipeline. The Analytics Engine transforms validated raw data into quantitative insights, risk metrics, and validated projections.

### 1.2 QR Board Scope

| In Scope | Out of Scope |
|----------|--------------|
| Battle Test backtesting engine | Data collection (Rakia) |
| Monte Carlo forward simulation | Raw data validation (Gate 1) |
| Risk metrics calculation | Trigger logic (Strategy Board) |
| Data quality scoring | Alert routing (Strategy Board) |
| Analytics validation (Gate 2) | Message templates (CMO Board) |
| Adelaide claims validation | Legal compliance (CLO Board) |
| Anomaly detection models | User interface design |

### 1.3 Position in Pipeline

```
Layer 1 â†’ Layer 2 â†’ [LAYER 3] â†’ Layer 4 â†’ Layer 5
Collection  Validation  ANALYTICS  Intelligence  Presentation
 (Rakia)     (Rakia)    (QR BOARD)  (Strategy)   (CMO/CLO)
```

### 1.4 Related Documents

| Document | Location | Relationship |
|----------|----------|--------------|
| STRATEGY_BOARD_CTO_HANDOFF.md | /mnt/project/ | Layer 4 triggers consume our outputs |
| VALIDATION_GATES_CTO_HANDOFF.md | /mnt/project/ | Gate 2 uses our validation rules |
| strategies_v2_1.json | /mnt/project/ | Canonical strategy definitions |
| diboas-analytics-v3-qr-board-specs.md | /mnt/project/ | Extended QR specifications |
| data_validation_handoff_package.md | /mnt/project/ | Rakia's data validation methodology |

### 1.5 Key Parameters Summary

| Parameter | Confirmed Value | Owner |
|-----------|-----------------|-------|
| Battle Test Period | 2022-01-01 to 2025-12-31 (48 months) | QR Board |
| Monte Carlo Simulations | 5,000 minimum (10,000 production) | QR Board |
| Distribution | Student-t (df=4) | QR Board |
| Regime States | 4 (Bull, Bear, Crash, Recovery) | QR Board |
| Confidence Interval | 90% (P5 to P95) | QR Board |
| Data Quality Threshold | â‰¥80 for Adelaide claims | QR Board |
| Random Seed | 42 (reproducibility) | QR Board |

---

## 2. Battle Test Engine

### 2.1 Purpose

The Battle Test Engine performs historical backtesting of all 10 investment strategies against actual market data. It answers: **"How would this strategy have performed over the past 4 years?"**

### 2.2 Execution Triggers

| Trigger | Frequency | Initiated By |
|---------|-----------|--------------|
| Scheduled run | Weekly (Sunday 3 AM UTC) | GitHub Actions |
| Strategy allocation change | On event | Strategy Board |
| New protocol added | On event | Strategy Board |
| Protocol removed (emergency) | Immediate | Strategy Board |
| Manual validation request | On demand | Any Board |
| Major market event | Within 24 hours | Protocol Monitoring |

### 2.3 Scenario Definitions

```python
# Battle Test Scenarios (QR Board Approved)

BATTLE_TEST_SCENARIOS = {
    'A': {
        'name': 'Established Investor',
        'description': 'Typical user with meaningful initial capital',
        'initial_investment': 10000,  # EUR/USD
        'monthly_dca': 200,
        'currency': 'EUR',
        'purpose': 'Validate strategy performance for standard users'
    },
    'B': {
        'name': 'Ana Persona (Minimum Viable)',
        'description': 'Conservative user with minimal capital - tests â‚¬5 minimum claim',
        'initial_investment': 5,
        'monthly_dca': 5,
        'currency': 'EUR',
        'purpose': 'Validate minimum viable investment claim for Ana persona'
    }
}

BATTLE_TEST_CONFIG = {
    'time_period': {
        'start_date': '2022-01-01',
        'end_date': '2025-12-31',
        'total_days': 1461,  # Including leap year
        'total_months': 48
    },
    'methodology': {
        'return_calculation': 'daily_compounding',
        'drawdown_calculation': 'peak_to_trough',
        'dca_timing': 'first_day_of_month',
        'rebalancing': 'none',  # Buy-and-hold for test
        'fee_modeling': 'excluded',  # Gross returns
        'gas_costs': 'excluded'  # Validated separately via CV-06/CV-07
    },
    'data_requirements': {
        'apy_frequency': 'daily',
        'price_frequency': 'daily',
        'min_data_completeness': 0.95  # 95% required
    }
}
```

### 2.4 Calculation Methodology

```python
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class BattleTestResult:
    strategy_id: int
    strategy_name: str
    scenario: str
    initial_investment: float
    monthly_dca: float
    total_invested: float
    final_value: float
    total_return_pct: float
    annualized_return_pct: float
    max_drawdown_pct: float
    max_drawdown_date: str
    recovery_days: int
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    winning_months: int
    losing_months: int
    test_start_date: str
    test_end_date: str
    days_tested: int
    data_quality_score: float
    config_hash: str
    run_timestamp: str


def run_battle_test(
    strategy: dict,
    scenario: dict,
    apy_data: pd.DataFrame,
    price_data: pd.DataFrame
) -> BattleTestResult:
    """
    Execute Battle Test for a single strategy/scenario combination.
    
    Methodology:
    1. Initialize portfolio with initial investment
    2. Calculate daily returns based on strategy allocations
    3. Apply monthly DCA on first of each month
    4. Track drawdowns and recovery
    5. Calculate final risk metrics
    """
    
    # Extract parameters
    initial = scenario['initial_investment']
    monthly_dca = scenario['monthly_dca']
    start_date = BATTLE_TEST_CONFIG['time_period']['start_date']
    end_date = BATTLE_TEST_CONFIG['time_period']['end_date']
    
    # Initialize tracking
    portfolio_value = initial
    total_invested = initial
    daily_values = []
    daily_returns = []
    
    # Get strategy allocations
    allocations = strategy['allocations']
    
    # Process each day
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    for date in date_range:
        # Check for DCA (first of month)
        if date.day == 1 and date != date_range[0]:
            portfolio_value += monthly_dca
            total_invested += monthly_dca
        
        # Calculate daily return based on allocations
        daily_return = calculate_portfolio_return(
            allocations, 
            apy_data.loc[date],
            price_data.loc[date]
        )
        
        # Apply return
        portfolio_value *= (1 + daily_return)
        
        # Track
        daily_values.append(portfolio_value)
        if len(daily_values) > 1:
            daily_returns.append(
                (daily_values[-1] - daily_values[-2]) / daily_values[-2]
            )
    
    # Calculate metrics
    daily_returns = np.array(daily_returns)
    final_value = portfolio_value
    total_return = (final_value - total_invested) / total_invested
    
    # Annualized return
    years = len(date_range) / 365
    annualized_return = (1 + total_return) ** (1 / years) - 1
    
    # Risk metrics
    sharpe = calculate_sharpe_ratio(daily_returns)
    sortino = calculate_sortino_ratio(daily_returns)
    max_dd, dd_date, recovery = calculate_max_drawdown(daily_values)
    calmar = calculate_calmar_ratio(annualized_return, max_dd)
    
    return BattleTestResult(
        strategy_id=strategy['id'],
        strategy_name=strategy['name'],
        scenario=scenario['name'],
        initial_investment=initial,
        monthly_dca=monthly_dca,
        total_invested=total_invested,
        final_value=round(final_value, 2),
        total_return_pct=round(total_return * 100, 2),
        annualized_return_pct=round(annualized_return * 100, 2),
        max_drawdown_pct=round(max_dd * 100, 2),
        max_drawdown_date=dd_date.isoformat() if dd_date else None,
        recovery_days=recovery,
        sharpe_ratio=round(sharpe, 3),
        sortino_ratio=round(sortino, 3),
        calmar_ratio=round(calmar, 3),
        winning_months=count_winning_months(daily_values),
        losing_months=count_losing_months(daily_values),
        test_start_date=start_date,
        test_end_date=end_date,
        days_tested=len(date_range),
        data_quality_score=calculate_data_quality_score(apy_data, price_data),
        config_hash=hash_config(BATTLE_TEST_CONFIG),
        run_timestamp=datetime.datetime.utcnow().isoformat()
    )
```

### 2.5 Output Format

```csv
strategy_id,strategy_name,scenario,initial_investment,monthly_dca,total_invested,final_value,total_return_pct,annualized_return_pct,max_drawdown_pct,max_drawdown_date,recovery_days,sharpe_ratio,sortino_ratio,calmar_ratio,winning_months,losing_months,test_start_date,test_end_date,days_tested,data_quality_score,config_hash,run_timestamp
1,Safe Harbor,Scenario A,10000,200,19600,21344.56,8.9,2.15,1.2,2022-06-15,45,1.85,2.45,1.79,42,6,2022-01-01,2025-12-31,1461,98.5,abc123,2026-01-23T14:30:00Z
```

---

## 3. Monte Carlo Simulation

### 3.1 Purpose

Monte Carlo simulation generates forward-looking projections by running thousands of possible market paths. It answers: **"What are the probable outcomes if I invest in this strategy for the next 4 years?"**

### 3.2 Configuration

```python
MONTE_CARLO_CONFIG = {
    'num_simulations': {
        'development': 1000,
        'staging': 5000,
        'production': 10000
    },
    'projection_period': {
        'years': 4,
        'days': 1461
    },
    'distribution': {
        'type': 'student_t',
        'degrees_of_freedom': 4,  # Fat tails
        'rationale': 'Better captures crypto tail risk than normal distribution'
    },
    'random_seed': 42,  # Reproducibility
    'confidence_interval': {
        'level': 0.90,
        'lower_percentile': 5,
        'upper_percentile': 95
    }
}
```

### 3.3 Regime-Based Model

```python
REGIME_MODEL = {
    'states': {
        'bull': {
            'stable_return_multiplier': 1.0,
            'crypto_return_multiplier': 1.5,
            'volatility_multiplier': 0.8,
            'base_probability': 0.40
        },
        'bear': {
            'stable_return_multiplier': 0.9,
            'crypto_return_multiplier': 0.5,
            'volatility_multiplier': 1.2,
            'base_probability': 0.30
        },
        'crash': {
            'stable_return_multiplier': 0.7,
            'crypto_return_multiplier': -0.5,
            'volatility_multiplier': 2.5,
            'base_probability': 0.10
        },
        'recovery': {
            'stable_return_multiplier': 1.1,
            'crypto_return_multiplier': 2.0,
            'volatility_multiplier': 1.5,
            'base_probability': 0.20
        }
    },
    'transition_matrix': {
        # Probability of moving from row state to column state
        # Order: bull, bear, crash, recovery
        'bull':     [0.70, 0.20, 0.05, 0.05],
        'bear':     [0.15, 0.60, 0.20, 0.05],
        'crash':    [0.05, 0.30, 0.35, 0.30],
        'recovery': [0.40, 0.10, 0.05, 0.45]
    }
}
```

### 3.4 Simulation Engine

```python
def run_monte_carlo(
    strategy: dict,
    initial_investment: float,
    monthly_dca: float,
    num_simulations: int = 10000,
    seed: int = 42
) -> MonteCarloResult:
    """
    Run Monte Carlo simulation for a strategy.
    
    Uses:
    - Regime-switching model for market states
    - Student-t distribution for fat tails
    - Correlation matrix for asset dependencies
    """
    
    np.random.seed(seed)
    
    final_values = []
    all_paths = []
    
    for sim in range(num_simulations):
        # Initialize
        portfolio_value = initial_investment
        current_regime = 'bull'  # Start assumption
        
        path = [portfolio_value]
        
        for day in range(MONTE_CARLO_CONFIG['projection_period']['days']):
            # Monthly DCA
            if day > 0 and day % 30 == 0:
                portfolio_value += monthly_dca
            
            # Regime transition
            current_regime = sample_next_regime(current_regime)
            
            # Sample return from regime-adjusted distribution
            daily_return = sample_regime_return(
                strategy['allocations'],
                current_regime,
                MONTE_CARLO_CONFIG['distribution']
            )
            
            portfolio_value *= (1 + daily_return)
            path.append(portfolio_value)
        
        final_values.append(portfolio_value)
        all_paths.append(path)
    
    return MonteCarloResult(
        final_values=np.array(final_values),
        paths=np.array(all_paths),
        config=MONTE_CARLO_CONFIG
    )
```

### 3.5 Correlation Matrices by Regime

```python
CORRELATION_MATRICES = {
    'bull': np.array([
        # BTC    ETH    SOL   Stable
        [1.00,  0.85,  0.80,  0.10],  # BTC
        [0.85,  1.00,  0.88,  0.08],  # ETH
        [0.80,  0.88,  1.00,  0.05],  # SOL
        [0.10,  0.08,  0.05,  1.00],  # Stable
    ]),
    'bear': np.array([
        [1.00,  0.90,  0.85,  0.15],
        [0.90,  1.00,  0.92,  0.12],
        [0.85,  0.92,  1.00,  0.10],
        [0.15,  0.12,  0.10,  1.00],
    ]),
    'crash': np.array([
        [1.00,  0.95,  0.95,  0.30],
        [0.95,  1.00,  0.97,  0.25],
        [0.95,  0.97,  1.00,  0.20],
        [0.30,  0.25,  0.20,  1.00],
    ]),
    'recovery': np.array([
        [1.00,  0.80,  0.75,  0.05],
        [0.80,  1.00,  0.85,  0.03],
        [0.75,  0.85,  1.00,  0.02],
        [0.05,  0.03,  0.02,  1.00],
    ])
}
```

---

## 4. Risk Metrics Calculations

### 4.1 Sharpe Ratio

```python
def calculate_sharpe_ratio(
    returns: np.ndarray,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 365
) -> float:
    """
    Calculate annualized Sharpe Ratio.
    
    Sharpe = (Portfolio Return - Risk Free Rate) / Portfolio Volatility
    
    Args:
        returns: Array of period returns (daily)
        risk_free_rate: Annual risk-free rate (default 4%)
        periods_per_year: 365 for daily, 12 for monthly
    
    Returns:
        Annualized Sharpe Ratio (can be negative - see Section 4.1.1)
    """
    if len(returns) < 2:
        return 0.0
    
    # Annualize returns and volatility
    mean_return = np.mean(returns) * periods_per_year
    volatility = np.std(returns, ddof=1) * np.sqrt(periods_per_year)
    
    if volatility == 0:
        return 0.0
    
    sharpe = (mean_return - risk_free_rate) / volatility
    return sharpe
```

### 4.1.1 Understanding Negative Sharpe Ratios

**[NEW in v2.0 - GAP-013 FIX]**

A **negative Sharpe ratio** is mathematically valid and can occur in real-world scenarios. Understanding when and why this happens is critical for proper interpretation.

#### When Negative Sharpe Ratios Occur

A negative Sharpe ratio indicates the strategy's return was **below the risk-free rate**. This means the investor would have been better off holding Treasury bills.

```python
# Example: Negative Sharpe Calculation
# 
# Scenario: 2022 Bear Market
# Strategy annual return: 2%
# Risk-free rate (Treasury): 4%
# Strategy volatility: 15%
#
# Sharpe = (0.02 - 0.04) / 0.15 = -0.133

def example_negative_sharpe():
    strategy_return = 0.02   # 2% annual return
    risk_free_rate = 0.04    # 4% Treasury rate
    volatility = 0.15        # 15% annual volatility
    
    sharpe = (strategy_return - risk_free_rate) / volatility
    # Result: -0.133 (negative)
    return sharpe
```

#### Valid Scenarios for Negative Sharpe

| Scenario | Explanation | Example |
|----------|-------------|---------|
| Bear Markets | Crypto assets decline while rates rise | 2022 crypto winter |
| Rising Rate Environment | Risk-free rate exceeds strategy returns | 2023 Fed hikes |
| High-Volatility Strategies | Volatile strategies during drawdowns | Strategy 10 in crashes |
| Protocol Failures | Strategies with exposure to failed protocols | UST/LUNA exposure |

#### Interpretation Guidelines

| Sharpe Range | Interpretation | Action |
|--------------|----------------|--------|
| > 2.0 | Excellent risk-adjusted returns | Monitor for sustainability |
| 1.0 - 2.0 | Good risk-adjusted returns | Standard operating range |
| 0.0 - 1.0 | Acceptable but not optimal | Review allocations |
| -0.5 - 0.0 | Underperforming risk-free rate | Investigate causes |
| < -0.5 | Significant underperformance | Crisis review required |

#### Validation Approach

```python
# In Gate 2 validation, we:
# 1. DO NOT flag negative Sharpe as an error (it's mathematically valid)
# 2. Set bounds at -5 to +10 (extremely negative would indicate calculation error)
# 3. Cross-check with other metrics for consistency

SHARPE_BOUNDS = {
    'min': -5.0,   # Below this indicates calculation error
    'max': 10.0,   # Above this indicates calculation error
    'warning_threshold': -1.0  # Log warning if below this
}

def validate_sharpe_ratio(sharpe: float, strategy_id: int) -> ValidationResult:
    """
    Validate Sharpe ratio is within mathematically valid bounds.
    
    NOTE: Negative values ARE valid. They indicate underperformance
    relative to risk-free rate, which can happen in bear markets.
    """
    issues = []
    
    if sharpe < SHARPE_BOUNDS['min']:
        issues.append(ValidationIssue(
            code="G2-SHP-001",
            severity="ERROR",
            message=f"Sharpe ratio {sharpe} below calculation error threshold",
            remediation="Check return/volatility calculation for errors"
        ))
    
    elif sharpe < SHARPE_BOUNDS['warning_threshold']:
        issues.append(ValidationIssue(
            code="G2-SHP-002",
            severity="WARNING",
            message=f"Sharpe ratio {sharpe} significantly negative",
            remediation="Expected in bear markets - verify market conditions"
        ))
    
    return ValidationResult(issues=issues)
```

#### Cross-Metric Validation

When Sharpe is negative, other metrics should be consistent:

```python
def validate_sharpe_consistency(metrics: dict) -> List[ValidationIssue]:
    """
    Validate negative Sharpe is consistent with other metrics.
    """
    issues = []
    sharpe = metrics.get('sharpe_ratio')
    prob_loss = metrics.get('probability_of_loss')
    median_return = metrics.get('median_return')
    
    if sharpe < 0:
        # Negative Sharpe should correlate with:
        
        # 1. Higher probability of loss
        if prob_loss < 0.3:
            issues.append(ValidationIssue(
                code="G2-COH-003",
                severity="WARNING",
                message="Negative Sharpe with low P(loss) - unusual",
                remediation="Verify both calculations"
            ))
        
        # 2. Lower or negative median returns expected
        if median_return > 0.10:  # 10%
            issues.append(ValidationIssue(
                code="G2-COH-004",
                severity="WARNING",
                message="Negative Sharpe with high median return - check volatility",
                remediation="High volatility may be causing negative Sharpe"
            ))
    
    return issues
```

### 4.2 Sortino Ratio

```python
def calculate_sortino_ratio(
    returns: np.ndarray,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 365
) -> float:
    """
    Calculate annualized Sortino Ratio.
    
    Sortino = (Portfolio Return - Risk Free Rate) / Downside Deviation
    
    Unlike Sharpe, only penalizes downside volatility.
    
    Args:
        returns: Array of period returns (daily)
        risk_free_rate: Annual risk-free rate
        periods_per_year: 365 for daily
    
    Returns:
        Annualized Sortino Ratio
    """
    if len(returns) < 2:
        return 0.0
    
    # Calculate downside returns (below 0)
    downside_returns = returns[returns < 0]
    
    if len(downside_returns) == 0:
        return float('inf')  # No downside = perfect
    
    # Downside deviation (semi-deviation)
    downside_std = np.std(downside_returns, ddof=1) * np.sqrt(periods_per_year)
    
    if downside_std == 0:
        return float('inf')
    
    # Annualized return
    mean_return = np.mean(returns) * periods_per_year
    
    sortino = (mean_return - risk_free_rate) / downside_std
    return sortino
```

### 4.3 Maximum Drawdown

```python
def calculate_max_drawdown(values: np.ndarray) -> Tuple[float, int, int]:
    """
    Calculate Maximum Drawdown and its timing.
    
    Max DD = (Peak - Trough) / Peak
    
    Args:
        values: Array of portfolio values over time
    
    Returns:
        Tuple of (max_drawdown_pct, peak_index, trough_index)
    """
    if len(values) < 2:
        return 0.0, 0, 0
    
    # Track running maximum
    running_max = np.maximum.accumulate(values)
    
    # Calculate drawdown at each point
    drawdowns = (running_max - values) / running_max
    
    # Find maximum drawdown
    max_dd = np.max(drawdowns)
    trough_idx = np.argmax(drawdowns)
    
    # Find the peak before the trough
    peak_idx = np.argmax(values[:trough_idx + 1])
    
    return max_dd, peak_idx, trough_idx


def calculate_recovery_days(
    values: List[float],
    trough_date: pd.Timestamp,
    dates: pd.DatetimeIndex
) -> int:
    """Calculate days from trough to recover to previous peak."""
    if trough_date is None:
        return 0
    
    trough_idx = dates.get_loc(trough_date)
    peak_value = max(values[:trough_idx + 1])
    
    # Find when we recover to peak
    for i in range(trough_idx, len(values)):
        if values[i] >= peak_value:
            return i - trough_idx
    
    # Never recovered
    return len(values) - trough_idx
```

### 4.4 Value at Risk (VaR)

```python
def calculate_var(
    returns: np.ndarray,
    confidence_level: float = 0.95,
    method: str = 'historical'
) -> float:
    """
    Calculate Value at Risk.
    
    VaR = Maximum expected loss at given confidence level
    
    Args:
        returns: Array of returns
        confidence_level: 0.95 for 95% VaR, 0.99 for 99% VaR
        method: 'historical' or 'parametric'
    
    Returns:
        VaR as a positive number (loss)
    """
    if method == 'historical':
        # Historical VaR: actual percentile of returns
        percentile = (1 - confidence_level) * 100
        var = -np.percentile(returns, percentile)
    
    elif method == 'parametric':
        # Parametric VaR: assumes normal distribution
        from scipy import stats
        mean = np.mean(returns)
        std = np.std(returns, ddof=1)
        z_score = stats.norm.ppf(1 - confidence_level)
        var = -(mean + z_score * std)
    
    return max(0, var)  # VaR is a loss, so return positive


def calculate_var_95(returns: np.ndarray) -> float:
    """95% VaR - loss exceeded 5% of the time."""
    return calculate_var(returns, confidence_level=0.95)


def calculate_var_99(returns: np.ndarray) -> float:
    """99% VaR - loss exceeded 1% of the time."""
    return calculate_var(returns, confidence_level=0.99)
```

### 4.5 Conditional VaR (Expected Shortfall)

```python
def calculate_cvar(
    returns: np.ndarray,
    confidence_level: float = 0.95
) -> float:
    """
    Calculate Conditional VaR (Expected Shortfall).
    
    CVaR = Expected loss given that loss exceeds VaR
    Also known as Expected Shortfall (ES) or Average VaR
    
    More conservative than VaR - considers severity of tail losses.
    
    Args:
        returns: Array of returns
        confidence_level: 0.95 for 95% CVaR
    
    Returns:
        CVaR as a positive number
    """
    var = calculate_var(returns, confidence_level)
    
    # Get returns worse than VaR
    tail_returns = returns[returns <= -var]
    
    if len(tail_returns) == 0:
        return var  # No tail losses
    
    # Average of tail losses
    cvar = -np.mean(tail_returns)
    return cvar


def calculate_cvar_95(returns: np.ndarray) -> float:
    """95% CVaR - average loss in worst 5% of cases."""
    return calculate_cvar(returns, confidence_level=0.95)
```

### 4.6 Calmar Ratio

```python
def calculate_calmar_ratio(
    annualized_return: float,
    max_drawdown: float
) -> float:
    """
    Calculate Calmar Ratio.
    
    Calmar = Annualized Return / Maximum Drawdown
    
    Measures return per unit of drawdown risk.
    
    Args:
        annualized_return: Annual return (decimal, e.g., 0.15 for 15%)
        max_drawdown: Maximum drawdown (decimal, e.g., 0.20 for 20%)
    
    Returns:
        Calmar Ratio
    """
    if max_drawdown == 0:
        return float('inf') if annualized_return > 0 else 0.0
    
    return annualized_return / max_drawdown
```

### 4.7 Confidence Interval Calculation

```python
def calculate_confidence_interval(
    values: np.ndarray,
    confidence: float = 0.90
) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for a set of values.
    
    Args:
        values: Array of values (e.g., simulation results)
        confidence: Confidence level (0.90 for 90%)
    
    Returns:
        Tuple of (lower_bound, median, upper_bound)
    """
    lower_pct = (1 - confidence) / 2 * 100
    upper_pct = (1 + confidence) / 2 * 100
    
    lower = np.percentile(values, lower_pct)
    median = np.median(values)
    upper = np.percentile(values, upper_pct)
    
    return lower, median, upper


def format_confidence_interval(
    lower: float,
    median: float,
    upper: float,
    confidence: float = 0.90
) -> str:
    """Format CI for display."""
    return f"{lower:.1f}% to {upper:.1f}% ({int(confidence*100)}% CI, median {median:.1f}%)"
```

---

## 5. Data Quality Assurance

### 5.1 Data Quality Score Calculation

```python
def calculate_data_quality_score(
    apy_data: pd.DataFrame,
    price_data: pd.DataFrame,
    source_info: dict = None
) -> float:
    """
    Calculate overall data quality score (0-100).
    
    QR Board threshold: â‰¥80 for Adelaide claims
    
    Weights:
    - Completeness: 30% (no missing values)
    - Consistency: 25% (no outliers beyond 3 std)
    - Timeliness: 25% (data freshness)
    - Accuracy: 20% (source reliability)
    
    Args:
        apy_data: DataFrame with APY data
        price_data: DataFrame with price data
        source_info: Dict with source metadata
    
    Returns:
        Data quality score (0-100)
    """
    from scipy import stats
    
    # Combine data for completeness check
    combined = pd.concat([apy_data, price_data], axis=1)
    
    # 1. Completeness (30%)
    total_cells = combined.size
    missing_cells = combined.isnull().sum().sum()
    completeness = (1 - missing_cells / total_cells) * 100
    
    # 2. Consistency (25%)
    numeric_cols = combined.select_dtypes(include=[np.number])
    z_scores = np.abs(stats.zscore(numeric_cols, nan_policy='omit'))
    outlier_pct = (z_scores > 3).sum().sum() / z_scores.size
    consistency = (1 - outlier_pct) * 100
    
    # 3. Timeliness (25%)
    if hasattr(combined.index, 'max'):
        latest_date = combined.index.max()
        hours_old = (pd.Timestamp.now() - latest_date).total_seconds() / 3600
        timeliness = max(0, 100 - (hours_old / 168 * 100))
    else:
        timeliness = 50
    
    # 4. Accuracy (20%)
    source_scores = {
        'DeFiLlama': 95,
        'FRED': 98,
        'Yahoo Finance': 90,
        'CoinGecko': 92,
        'Jupiter API': 93,
        'Etherscan': 96,
        'Manual': 70,
        'Proxy': 60
    }
    if source_info:
        accuracy_scores = [source_scores.get(s, 75) for s in source_info.get('sources', [])]
        accuracy = np.mean(accuracy_scores) if accuracy_scores else 75
    else:
        accuracy = 75
    
    # Weighted total
    total = (
        completeness * 0.30 +
        consistency * 0.25 +
        timeliness * 0.25 +
        accuracy * 0.20
    )
    
    return round(total, 1)


def assess_data_quality(score: float) -> Tuple[str, bool]:
    """
    Assess data quality score.
    
    Returns:
        Tuple of (grade, approved_for_adelaide)
    """
    if score >= 90:
        return 'A', True
    elif score >= 80:
        return 'B', True
    elif score >= 70:
        return 'C', False  # Needs review
    elif score >= 60:
        return 'D', False
    else:
        return 'F', False
```

### 5.2 Source Reliability Scoring

```python
SOURCE_RELIABILITY = {
    # Tier 1: Official/Primary Sources (95-100)
    'FRED': {'score': 98, 'tier': 1, 'description': 'Federal Reserve Economic Data'},
    'Treasury.gov': {'score': 99, 'tier': 1, 'description': 'US Treasury Official'},
    'SEC EDGAR': {'score': 98, 'tier': 1, 'description': 'SEC Official Filings'},
    'Etherscan': {'score': 96, 'tier': 1, 'description': 'On-chain verified'},
    'Solscan': {'score': 95, 'tier': 1, 'description': 'On-chain verified'},
    
    # Tier 2: Established Data Providers (85-94)
    'DeFiLlama': {'score': 94, 'tier': 2, 'description': 'DeFi aggregator'},
    'CoinGecko': {'score': 92, 'tier': 2, 'description': 'Crypto price aggregator'},
    'Yahoo Finance': {'score': 90, 'tier': 2, 'description': 'TradFi data provider'},
    'Jupiter API': {'score': 93, 'tier': 2, 'description': 'Protocol official'},
    
    # Tier 3: Secondary Sources (70-84)
    'News Articles': {'score': 75, 'tier': 3, 'description': 'Journalistic sources'},
    'Social Media': {'score': 65, 'tier': 3, 'description': 'Unverified'},
    
    # Tier 4: Derived/Proxy (50-69)
    'Proxy Formula': {'score': 60, 'tier': 4, 'description': 'QR Board estimated'},
    'Manual Entry': {'score': 70, 'tier': 4, 'description': 'Human entered'}
}
```

### 5.3 Timeliness Requirements

```python
TIMELINESS_REQUIREMENTS = {
    'price_data': {
        'max_age_hours': 1,
        'critical_threshold': 6,
        'stale_threshold': 24
    },
    'apy_data': {
        'max_age_hours': 24,
        'critical_threshold': 48,
        'stale_threshold': 168  # 1 week
    },
    'tvl_data': {
        'max_age_hours': 6,
        'critical_threshold': 24,
        'stale_threshold': 72
    },
    'macro_data': {
        'max_age_hours': 24,
        'critical_threshold': 72,
        'stale_threshold': 168
    },
    'estate_wallet': {
        'max_age_hours': 1,
        'critical_threshold': 6,
        'stale_threshold': 24
    }
}


def check_timeliness(data_type: str, last_updated: pd.Timestamp) -> dict:
    """Check if data meets timeliness requirements."""
    req = TIMELINESS_REQUIREMENTS.get(data_type, TIMELINESS_REQUIREMENTS['apy_data'])
    hours_old = (pd.Timestamp.now() - last_updated).total_seconds() / 3600
    
    return {
        'hours_old': round(hours_old, 1),
        'status': (
            'fresh' if hours_old <= req['max_age_hours']
            else 'acceptable' if hours_old <= req['critical_threshold']
            else 'stale' if hours_old <= req['stale_threshold']
            else 'expired'
        ),
        'approved': hours_old <= req['critical_threshold']
    }
```

---

## 6. Auto-Validation Framework

### 6.1 CTO Auto-Approve Criteria

```python
AUTO_APPROVE_CRITERIA = {
    'performance_claim': {
        'description': 'Historical return statements',
        'conditions': [
            'value_within_90_ci',
            'data_quality_score >= 80',
            'no_regime_change_24h',
            'strategy_has_30d_data',
            'not_highest_return_claim',
            'past_performance_disclaimer'
        ],
        'example': '"Strategy 1 returned 8.2% over 12 months"'
    },
    'probability_claim': {
        'description': 'Forward-looking probability statements',
        'conditions': [
            'monte_carlo_n >= 5000',
            'confidence_interval_stated',
            'methodology_disclosed',
            'not_guaranteed_language'
        ],
        'example': '"0.8% probability of loss over 4 years"'
    },
    'comparison_claim': {
        'description': 'Comparing to benchmarks',
        'conditions': [
            'benchmark_source_documented',
            'same_time_period',
            'methodology_disclosed',
            'not_superlative_language'
        ],
        'example': '"Outperformed average savings account by 3.2%"'
    }
}
```

### 6.2 Escalation Rules

```python
ESCALATION_RULES = {
    'auto_approve': {
        'conditions': 'All AUTO_APPROVE_CRITERIA met',
        'action': 'CTO Board can approve without QR review',
        'sla': 'Immediate'
    },
    'qr_review_required': {
        'conditions': 'Any AUTO_APPROVE_CRITERIA not met',
        'action': 'Route to QR Board for manual review',
        'sla': '24 hours for non-critical, 4 hours for critical'
    },
    'ceo_escalation': {
        'conditions': [
            'Claim involves superlatives (best, highest, only)',
            'Claim contradicts previous statements',
            'Legal concerns raised by CLO'
        ],
        'action': 'Route to CEO Board',
        'sla': '48 hours'
    }
}
```

### 6.3 Statistical Thresholds

```python
STATISTICAL_THRESHOLDS = {
    'return_deviation': {
        'warning': 2.0,    # 2 std dev from expected
        'escalate': 3.0,
        'critical': 4.0
    },
    'volatility_spike': {
        'warning': 1.5,    # 50% above normal
        'escalate': 2.0,
        'critical': 2.5
    },
    'correlation_change': {
        'warning': 0.15,
        'escalate': 0.25,
        'critical': 0.35
    },
    'drawdown_deviation': {
        'warning': 1.2,    # 20% worse than Monte Carlo p95
        'escalate': 1.5,
        'critical': 2.0
    }
}


def check_statistical_deviation(
    metric: str,
    actual: float,
    expected: float,
    std: float
) -> Tuple[str, bool]:
    """
    Check if a metric deviates significantly from expected.
    
    Returns:
        Tuple of (status, needs_escalation)
    """
    thresholds = STATISTICAL_THRESHOLDS.get(metric, STATISTICAL_THRESHOLDS['return_deviation'])
    
    if std == 0:
        return 'normal', False
    
    z_score = abs(actual - expected) / std
    
    if z_score >= thresholds['critical']:
        return 'critical', True
    elif z_score >= thresholds['escalate']:
        return 'escalate', True
    elif z_score >= thresholds['warning']:
        return 'warning', False
    else:
        return 'normal', False
```

### 6.4 SLA for QR Board Response

```python
QR_BOARD_SLA = {
    'CRITICAL': {
        'initial_response_hours': 2,
        'resolution_hours': 8,
        'escalation_path': ['QR Board Lead', 'Strategy Board', 'CEO']
    },
    'HIGH': {
        'initial_response_hours': 8,
        'resolution_hours': 24,
        'escalation_path': ['QR Board Lead', 'Strategy Board']
    },
    'MEDIUM': {
        'initial_response_hours': 24,
        'resolution_hours': 48,
        'escalation_path': ['QR Board']
    },
    'LOW': {
        'initial_response_hours': 48,
        'resolution_hours': 168,  # 1 week
        'escalation_path': ['QR Board']
    }
}
```

---

## 7. Adelaide Claims Validation

### 7.1 Claim Types and Validation Rules

```python
ADELAIDE_CLAIM_VALIDATION = {
    'performance_claim': {
        'type': 'HISTORICAL',
        'description': 'Statements about past returns',
        'required_checks': [
            'value_matches_battle_test',
            'time_period_clearly_stated',
            'no_cherry_picking_period',
            'data_quality_score >= 80',
            'disclaimer_present'
        ],
        'required_disclaimer': 'Past performance does not guarantee future results.',
        'prohibited_phrases': ['guaranteed', 'risk-free', 'always'],
        'example_valid': '"Strategy 1 returned 8.2% over the 12 months ending December 2025"',
        'example_invalid': '"Strategy 1 always returns 8%"'
    },
    
    'comparison_claim': {
        'type': 'COMPARATIVE',
        'description': 'Comparing to benchmarks or alternatives',
        'required_checks': [
            'benchmark_source_documented',
            'time_periods_identical',
            'methodology_apples_to_apples',
            'benchmark_data_verified'
        ],
        'required_disclaimer': 'Comparison methodology: [specify]',
        'prohibited_phrases': ['beat', 'crush', 'destroy'],
        'allowed_phrases': ['outperformed', 'exceeded', 'generated more than'],
        'example_valid': '"Strategy 1 exceeded average savings account returns by 3.2% (comparison period: 2024)"',
        'example_invalid': '"We crush traditional banks"'
    },
    
    'probability_claim': {
        'type': 'FORWARD_LOOKING',
        'description': 'Statements about likelihood of outcomes',
        'required_checks': [
            'monte_carlo_n >= 5000',
            'confidence_interval_stated',
            'methodology_disclosed',
            'limitations_acknowledged'
        ],
        'required_disclaimer': 'Based on [N] simulations using historical data patterns. Actual results may differ.',
        'prohibited_phrases': ['will', 'certain', 'guaranteed'],
        'allowed_phrases': ['may', 'could', 'probability', 'based on simulations'],
        'example_valid': '"Based on 10,000 simulations, Strategy 1 has a 0.8% probability of loss over 4 years"',
        'example_invalid': '"You will definitely make money"'
    },
    
    'whale_tracking_claim': {
        'type': 'MARKET_INSIGHT',
        'description': 'Reporting large wallet movements',
        'required_checks': [
            'no_wallet_owner_identification',
            'no_specific_firm_names_unless_public',
            'aggregate_language_used',
            'not_investment_advice'
        ],
        'prohibited_phrases': ['you should', 'buy now', 'sell immediately'],
        'prohibited_entities': ['Jump Trading', 'Wintermute', 'Alameda', 'specific person names'],
        'allowed_phrases': ['large wallet', 'smart money', 'institutional flows', 'significant movement'],
        'example_valid': '"A large wallet moved $45M ETH to exchanges over the past 24 hours"',
        'example_invalid': '"Jump Trading is dumping - you should sell"'
    },
    
    'apy_claim': {
        'type': 'CURRENT_STATE',
        'description': 'Current or recent yield information',
        'required_checks': [
            'apy_from_verified_source',
            'time_period_specified',
            'range_not_single_point',
            'variability_acknowledged'
        ],
        'required_disclaimer': 'APY is variable and may change.',
        'prohibited_phrases': ['locked in', 'guaranteed yield', 'fixed rate'],
        'example_valid': '"Current APY range: 6-10% (7-day average)"',
        'example_invalid': '"Earn a guaranteed 8% APY"'
    }
}


def validate_adelaide_claim(
    claim_text: str,
    claim_type: str,
    supporting_data: dict
) -> dict:
    """
    Validate an Adelaide newsletter claim.
    
    Args:
        claim_text: The actual claim text
        claim_type: One of the ADELAIDE_CLAIM_VALIDATION keys
        supporting_data: Dict with relevant metrics, sources, etc.
    
    Returns:
        Validation result dict
    """
    rules = ADELAIDE_CLAIM_VALIDATION.get(claim_type)
    if not rules:
        return {'valid': False, 'reason': f'Unknown claim type: {claim_type}'}
    
    issues = []
    
    # Check prohibited phrases
    for phrase in rules.get('prohibited_phrases', []):
        if phrase.lower() in claim_text.lower():
            issues.append(f"Prohibited phrase: '{phrase}'")
    
    # Check required disclaimer
    required_disclaimer = rules.get('required_disclaimer', '')
    if required_disclaimer and required_disclaimer not in claim_text:
        issues.append(f"Missing disclaimer: '{required_disclaimer[:50]}...'")
    
    # Check prohibited entities (for whale tracking)
    for entity in rules.get('prohibited_entities', []):
        if entity.lower() in claim_text.lower():
            issues.append(f"Prohibited entity reference: '{entity}'")
    
    # Check required data quality
    if 'data_quality_score >= 80' in rules.get('required_checks', []):
        dq_score = supporting_data.get('data_quality_score', 0)
        if dq_score < 80:
            issues.append(f"Data quality {dq_score} below threshold (80)")
    
    return {
        'valid': len(issues) == 0,
        'claim_type': claim_type,
        'issues': issues,
        'disclaimer_required': rules.get('required_disclaimer'),
        'auto_approve_eligible': len(issues) == 0 and claim_type in ['performance_claim', 'apy_claim']
    }
```

### 7.2 Regional Compliance Notes

```python
REGIONAL_COMPLIANCE = {
    'EU': {
        'regulator': 'ESMA / MiCA',
        'additional_requirements': [
            'No personalized investment advice',
            'Risk warnings in local language',
            'Cooling-off period disclosures',
            'GDPR-compliant data handling'
        ],
        'prohibited_terms': ['guaranteed returns', 'no risk'],
        'required_warnings': [
            'Capital at risk',
            'Past performance is not indicative of future results'
        ]
    },
    'US': {
        'regulator': 'SEC / CFTC',
        'additional_requirements': [
            'No investment advice without registration',
            'Accredited investor disclosures where applicable',
            'Anti-fraud provisions apply'
        ],
        'prohibited_terms': ['guaranteed', 'risk-free', 'insured'],
        'required_warnings': [
            'Not FDIC insured',
            'May lose value',
            'Not a bank deposit'
        ]
    },
    'Brazil': {
        'regulator': 'CVM / Banco Central',
        'additional_requirements': [
            'Portuguese language required',
            'Local tax implications disclosed',
            'Registration requirements noted'
        ],
        'prohibited_terms': ['garantido', 'sem risco'],
        'required_warnings': [
            'Rentabilidade passada nÃ£o Ã© garantia de rentabilidade futura',
            'Investimentos envolvem riscos'
        ]
    }
}
```

---

## 8. Anomaly Detection

### 8.1 Statistical Methods

```python
def detect_z_score_anomaly(
    values: np.ndarray,
    threshold: float = 3.0
) -> List[int]:
    """
    Detect anomalies using Z-score method.
    
    Args:
        values: Array of values to check
        threshold: Z-score threshold (default 3.0 = 99.7% confidence)
    
    Returns:
        List of indices where anomalies detected
    """
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    
    if std == 0:
        return []
    
    z_scores = np.abs((values - mean) / std)
    anomaly_indices = np.where(z_scores > threshold)[0]
    
    return list(anomaly_indices)


def detect_change_points(
    values: np.ndarray,
    window: int = 30,
    threshold: float = 2.0
) -> List[int]:
    """
    Detect change points in time series.
    
    Uses rolling mean comparison to detect regime shifts.
    
    Returns:
        List of indices where change points detected
    """
    change_points = []
    
    for i in range(window, len(values) - window):
        before = values[i-window:i]
        after = values[i:i+window]
        
        mean_diff = abs(np.mean(after) - np.mean(before))
        pooled_std = np.sqrt((np.var(before) + np.var(after)) / 2)
        
        if pooled_std > 0 and mean_diff / pooled_std > threshold:
            change_points.append(i)
    
    return change_points


def detect_spc_violation(
    values: np.ndarray,
    control_limits: Tuple[float, float] = None
) -> dict:
    """
    Statistical Process Control violation detection.
    
    Checks for:
    - Values outside control limits (Â±3Ïƒ)
    - Runs of 7+ consecutive values above/below mean
    - Trends of 7+ consecutive increasing/decreasing values
    """
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    
    if control_limits is None:
        ucl = mean + 3 * std  # Upper Control Limit
        lcl = mean - 3 * std  # Lower Control Limit
    else:
        lcl, ucl = control_limits
    
    violations = {
        'outside_limits': [],
        'runs': [],
        'trends': []
    }
    
    # Check control limits
    for i, v in enumerate(values):
        if v > ucl or v < lcl:
            violations['outside_limits'].append(i)
    
    # Check runs (7+ consecutive above/below mean)
    run_count = 0
    run_sign = 0
    for i, v in enumerate(values):
        current_sign = 1 if v > mean else -1
        if current_sign == run_sign:
            run_count += 1
        else:
            run_count = 1
            run_sign = current_sign
        
        if run_count >= 7:
            violations['runs'].append(i)
    
    # Check trends (7+ consecutive increasing/decreasing)
    trend_count = 0
    for i in range(1, len(values)):
        if values[i] > values[i-1]:
            if trend_count >= 0:
                trend_count += 1
            else:
                trend_count = 1
        elif values[i] < values[i-1]:
            if trend_count <= 0:
                trend_count -= 1
            else:
                trend_count = -1
        
        if abs(trend_count) >= 7:
            violations['trends'].append(i)
    
    return violations
```

### 8.2 ML Methods

```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_isolation_forest(
    training_data: np.ndarray,
    contamination: float = 0.05
) -> IsolationForest:
    """
    Train Isolation Forest for anomaly detection.
    
    Args:
        training_data: Historical data (n_samples, n_features)
        contamination: Expected proportion of anomalies
    
    Returns:
        Trained IsolationForest model
    """
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    model.fit(training_data)
    return model


def detect_isolation_forest_anomaly(
    model: IsolationForest,
    current_data: np.ndarray
) -> Tuple[bool, float]:
    """
    Detect anomaly using trained Isolation Forest.
    
    Returns:
        Tuple of (is_anomaly, anomaly_score)
    """
    prediction = model.predict(current_data.reshape(1, -1))
    score = model.decision_function(current_data.reshape(1, -1))[0]
    
    is_anomaly = prediction[0] == -1
    return is_anomaly, score


def detect_correlation_breakdown(
    current_correlations: np.ndarray,
    expected_correlations: np.ndarray,
    threshold: float = 0.25
) -> List[Tuple[str, str, float]]:
    """
    Detect when asset correlations deviate from expected.
    
    Returns:
        List of (asset1, asset2, deviation) tuples for breakdowns
    """
    assets = ['BTC', 'ETH', 'SOL', 'stable_yield']
    breakdowns = []
    
    for i, asset1 in enumerate(assets):
        for j, asset2 in enumerate(assets):
            if i < j:  # Upper triangle only
                expected = expected_correlations[i, j]
                actual = current_correlations[i, j]
                deviation = abs(actual - expected)
                
                if deviation > threshold:
                    breakdowns.append((asset1, asset2, deviation))
    
    return breakdowns
```

### 8.3 Anomaly Thresholds Table

```python
ANOMALY_THRESHOLDS = {
    'apy_deviation': {
        'metric': 'Protocol APY deviation from 30-day mean',
        'warning': {'threshold': 2.0, 'unit': 'std dev'},
        'critical': {'threshold': 3.0, 'unit': 'std dev'},
        'severe': {'threshold': 4.0, 'unit': 'std dev'},
        'action_warning': 'Log and monitor',
        'action_critical': 'Alert Strategy Board',
        'action_severe': 'Trigger Battle Test regression'
    },
    'tvl_drop': {
        'metric': 'Protocol TVL 24h change',
        'warning': {'threshold': 10, 'unit': '%'},
        'critical': {'threshold': 20, 'unit': '%'},
        'severe': {'threshold': 30, 'unit': '%'},
        'action_warning': 'Log and monitor',
        'action_critical': 'Alert Strategy Board + investigate',
        'action_severe': 'Consider protocol suspension'
    },
    'price_drop': {
        'metric': 'Crypto asset 24h price change',
        'warning': {'threshold': 10, 'unit': '%'},
        'critical': {'threshold': 20, 'unit': '%'},
        'severe': {'threshold': 30, 'unit': '%'},
        'action_warning': 'Monitor affected strategies',
        'action_critical': 'Crisis template consideration',
        'action_severe': 'Activate crisis communication'
    },
    'correlation_breakdown': {
        'metric': 'Correlation deviation from expected',
        'warning': {'threshold': 0.15, 'unit': 'absolute'},
        'critical': {'threshold': 0.25, 'unit': 'absolute'},
        'severe': {'threshold': 0.35, 'unit': 'absolute'},
        'action_warning': 'Log for Monte Carlo review',
        'action_critical': 'Recalibrate Monte Carlo',
        'action_severe': 'Full simulation re-run'
    },
    'estate_wallet_movement': {
        'metric': 'Estate wallet transfer amount',
        'warning': {'threshold': 1_000_000, 'unit': 'USD'},
        'critical': {'threshold': 10_000_000, 'unit': 'USD'},
        'severe': {'threshold': 50_000_000, 'unit': 'USD'},
        'action_warning': 'Log movement',
        'action_critical': 'Alert Strategy Board',
        'action_severe': 'P0 crisis alert'
    }
}
```

---

## 9. Proxy Data Methodology

### 9.1 Proxy Data Policy v1.0

```python
# Approved by Strategy Board Session 006

PROXY_DATA_POLICY = {
    'version': '1.0',
    'approved_date': '2026-01-19',
    'approved_by': 'Strategy Board',
    
    'principles': [
        'Real data collection is always preferred over proxy',
        'Proxy data used only when real data unavailable',
        'All proxy formulas documented with rationale',
        'Proxy data clearly labeled in all outputs',
        'Users informed when strategies use >20% proxy data'
    ],
    
    'separation_requirement': {
        'description': 'Real and proxy data in separate columns',
        'real_column_suffix': '',
        'proxy_column_suffix': '_proxy',
        'combined_column_suffix': '_combined'
    },
    
    'user_communication': {
        'threshold_for_disclosure': 0.20,  # 20%
        'display_indicator': '~',
        'display_text': '(partially estimated)',
        'tooltip': 'Some data in this calculation is estimated based on similar protocols'
    }
}
```

### 9.2 Proxy Data Disclaimer and Limitations

**[NEW in v2.0 - GAP-014 FIX]**

#### Official Disclaimer

> **PROXY DATA DISCLAIMER**
> 
> Some historical data used in Battle Test calculations is estimated using proxy formulas 
> when actual protocol data is unavailable (typically for periods before protocol launch). 
> Proxy data is derived from similar protocols or economic models and may not accurately 
> reflect actual returns that would have occurred.
> 
> **Key Limitations:**
> - Proxy formulas are estimates, not verified historical data
> - Confidence levels for proxy data range from 60-80% (lower than real data at 95%+)
> - Strategies with >20% proxy data are flagged with a "~" indicator
> - Proxy methodology documented in Section 9.3
> 
> Users should consider proxy data limitations when evaluating strategy performance, 
> particularly for strategies with high proxy percentages.

```python
PROXY_DATA_DISCLAIMER = {
    'short_version': 'Some data estimated. See methodology.',
    
    'medium_version': (
        'Historical returns for periods before protocol launch are estimated '
        'using proxy formulas. Actual results may have differed.'
    ),
    
    'full_version': '''
    PROXY DATA DISCLOSURE
    
    This analysis includes estimated data for periods when certain DeFi protocols 
    were not yet launched. Proxy formulas are used based on similar protocols:
    
    - Sanctum (pre-March 2024): Estimated from SOL staking + LST premium
    - Jito (pre-March 2023): Estimated from SOL staking + MEV premium  
    - Jupiter JLP (pre-Sept 2023): Estimated from GMX GLP + Solana premium
    
    Confidence levels for proxy data: 60-80%
    Confidence levels for real data: 95%+
    
    Users should weigh this uncertainty when evaluating strategy performance.
    ''',
    
    'required_on': [
        'Adelaide newsletter (any strategy with >20% proxy)',
        'Battle Test reports',
        'Strategy comparison pages',
        'Performance claim validation'
    ],
    
    'not_required_on': [
        'Real-time APY displays (current data only)',
        'Strategies with 0% proxy (pure stable strategies)',
        'General educational content'
    ]
}


def generate_proxy_disclosure(strategy_id: int) -> str:
    """
    Generate appropriate proxy disclosure for a strategy.
    
    Returns the disclosure text or empty string if not needed.
    """
    breakdown = STRATEGY_PROXY_BREAKDOWN.get(strategy_id, {})
    
    if not breakdown.get('disclosure', False):
        return ''  # No disclosure needed
    
    proxy_pct = breakdown.get('proxy_pct', 0)
    
    return f'''
    Note: {proxy_pct}% of historical data for this strategy is estimated 
    using proxy formulas for periods before certain protocols launched. 
    {PROXY_DATA_DISCLAIMER['medium_version']}
    '''
```

#### Proxy Data Quality Impact on Claims

```python
PROXY_IMPACT_ON_CLAIMS = {
    'auto_approval': {
        'allowed': 'Strategies with â‰¤20% proxy data',
        'requires_review': 'Strategies with >20% proxy data',
        'blocked': 'Strategies with >50% proxy data cannot make specific return claims'
    },
    
    'claim_modifications': {
        'high_proxy': {
            'threshold': 0.50,  # 50%
            'required_language': 'estimated',
            'example': '"Strategy 8 generated an estimated 25% return (70% of data estimated)"'
        },
        'medium_proxy': {
            'threshold': 0.20,  # 20%
            'required_language': 'partially estimated',
            'example': '"Strategy 4 returned 15% (45% estimated)"'
        },
        'low_proxy': {
            'threshold': 0.0,
            'required_language': None,  # Standard disclosure sufficient
            'example': '"Strategy 1 returned 5.2% over 4 years"'
        }
    },
    
    'confidence_interval_widening': {
        'description': 'CI should be wider for high-proxy strategies',
        'formula': 'CI_width = base_ci_width * (1 + proxy_pct * 0.5)',
        'example': '90% CI for 50% proxy strategy: Â±50% wider than pure real data'
    }
}


def validate_claim_with_proxy_consideration(
    claim: str,
    strategy_id: int,
    claim_value: float
) -> dict:
    """
    Validate a claim considering proxy data impact.
    """
    breakdown = STRATEGY_PROXY_BREAKDOWN.get(strategy_id, {})
    proxy_pct = breakdown.get('proxy_pct', 0) / 100
    
    issues = []
    modifications = []
    
    # High proxy - specific return claims blocked
    if proxy_pct > 0.50:
        if 'returned' in claim.lower() and '%' in claim:
            issues.append('Specific return claims not allowed for >50% proxy strategies')
            modifications.append('Use range or "estimated" language')
    
    # Medium proxy - must include "estimated" or "partially estimated"
    elif proxy_pct > 0.20:
        if 'estimated' not in claim.lower() and 'approximate' not in claim.lower():
            issues.append('Claims for >20% proxy strategies must include estimation disclosure')
            modifications.append('Add "partially estimated" to claim')
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'suggested_modifications': modifications,
        'proxy_percentage': proxy_pct * 100,
        'requires_disclosure': proxy_pct > 0.20
    }
```

### 9.3 Proxy Formulas by Protocol

```python
PROXY_FORMULAS = {
    'sanctum_pre_2024': {
        'protocol': 'Sanctum INF',
        'period': 'Before March 2024',
        'formula': 'SOL_staking_apy * 0.95 + 0.02',
        'rationale': 'LST aggregator typically slightly below direct staking plus diversification premium',
        'confidence': 0.75,
        'code': '''
def proxy_sanctum_apy(sol_staking_apy: float) -> float:
    """Estimate Sanctum APY before launch."""
    return sol_staking_apy * 0.95 + 0.02
'''
    },
    
    'jito_pre_march_2023': {
        'protocol': 'Jito',
        'period': 'Before March 2023',
        'formula': 'SOL_staking_apy + MEV_premium',
        'mev_premium': 0.015,  # 1.5% historical average
        'rationale': 'JitoSOL = SOL staking + MEV rewards (~1-2% historically)',
        'confidence': 0.80,
        'code': '''
def proxy_jito_apy(sol_staking_apy: float, mev_premium: float = 0.015) -> float:
    """Estimate Jito APY before launch."""
    return sol_staking_apy + mev_premium
'''
    },
    
    'jlp_pre_sept_2023': {
        'protocol': 'Jupiter JLP',
        'period': 'Before September 2023',
        'formula': 'perps_market_maker_avg_apy',
        'reference_protocol': 'GMX GLP',
        'rationale': 'JLP similar to GLP - perps LP with protocol fees',
        'confidence': 0.70,
        'code': '''
def proxy_jlp_apy(gmx_glp_apy: float) -> float:
    """Estimate JLP APY before launch using GLP as proxy."""
    # JLP typically higher volume but similar mechanism
    return gmx_glp_apy * 1.1  # 10% premium for Solana activity
'''
    }
}
```

### 9.4 Real vs Proxy Breakdown by Strategy

```python
# Calculated based on data availability

STRATEGY_PROXY_BREAKDOWN = {
    1: {'name': 'Safe Harbor', 'real_pct': 100, 'proxy_pct': 0, 'disclosure': False},
    2: {'name': 'Beat Inflation', 'real_pct': 60, 'proxy_pct': 40, 'disclosure': True},
    3: {'name': 'Goal Keeper', 'real_pct': 100, 'proxy_pct': 0, 'disclosure': False},
    4: {'name': 'Steady Progress', 'real_pct': 55, 'proxy_pct': 45, 'disclosure': True},
    5: {'name': 'Patient Builder', 'real_pct': 100, 'proxy_pct': 0, 'disclosure': False},
    6: {'name': 'Balanced Builder', 'real_pct': 45, 'proxy_pct': 55, 'disclosure': True},
    7: {'name': 'Steady Compounder', 'real_pct': 100, 'proxy_pct': 0, 'disclosure': False},
    8: {'name': 'Wealth Accelerator', 'real_pct': 30, 'proxy_pct': 70, 'disclosure': True},
    9: {'name': 'Yield Maximizer', 'real_pct': 100, 'proxy_pct': 0, 'disclosure': False},
    10: {'name': 'Full Throttle', 'real_pct': 15, 'proxy_pct': 85, 'disclosure': True}
}

# Note: Stable-only strategies (1,3,5,7,9) = 100% real
# Crypto strategies use proxy for pre-launch protocol periods
```

---

## 10. Output Schemas

### 10.1 Battle Test Results Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BattleTestResults",
  "type": "object",
  "required": ["version", "run_timestamp", "config_hash", "strategies"],
  "properties": {
    "version": {"type": "string"},
    "run_timestamp": {"type": "string", "format": "date-time"},
    "config_hash": {"type": "string"},
    "data_quality_score": {"type": "number"},
    "validation_status": {"type": "string", "enum": ["pass", "warn", "fail"]},
    "strategies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["strategy_id", "scenario", "results"],
        "properties": {
          "strategy_id": {"type": "integer"},
          "strategy_name": {"type": "string"},
          "scenario": {"type": "string"},
          "results": {
            "type": "object",
            "properties": {
              "initial_investment": {"type": "number"},
              "total_invested": {"type": "number"},
              "final_value": {"type": "number"},
              "total_return_pct": {"type": "number"},
              "annualized_return_pct": {"type": "number"},
              "max_drawdown_pct": {"type": "number"},
              "sharpe_ratio": {"type": "number"},
              "sortino_ratio": {"type": "number"},
              "calmar_ratio": {"type": "number"}
            }
          }
        }
      }
    }
  }
}
```

### 10.2 Monte Carlo Results Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MonteCarloResults",
  "type": "object",
  "required": ["version", "run_timestamp", "config", "strategies"],
  "properties": {
    "version": {"type": "string"},
    "run_timestamp": {"type": "string", "format": "date-time"},
    "config": {
      "type": "object",
      "properties": {
        "num_simulations": {"type": "integer"},
        "projection_years": {"type": "integer"},
        "random_seed": {"type": "integer"},
        "distribution": {"type": "string"}
      }
    },
    "strategies": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "strategy_id": {"type": "integer"},
          "ci_lower": {"type": "number"},
          "ci_median": {"type": "number"},
          "ci_upper": {"type": "number"},
          "probability_of_loss": {"type": "number"},
          "var_95": {"type": "number"},
          "cvar_99": {"type": "number"}
        }
      }
    }
  }
}
```

---

## 11. Configuration Templates

### 11.1 Battle Test Config

```yaml
# config/battle_test.yaml

version: "1.0"
last_updated: "2026-01-23"

scenarios:
  A:
    name: "Established Investor"
    initial_investment: 10000
    monthly_dca: 200
    currency: "EUR"
    
  B:
    name: "Ana Persona"
    initial_investment: 5
    monthly_dca: 5
    currency: "EUR"

time_period:
  start_date: "2022-01-01"
  end_date: "2025-12-31"

methodology:
  return_calculation: "daily_compounding"
  dca_timing: "first_day_of_month"
  rebalancing: "none"
  fee_modeling: "excluded"

data_requirements:
  min_completeness: 0.95
  apy_frequency: "daily"
  price_frequency: "daily"
```

### 11.2 Monte Carlo Config

```yaml
# config/monte_carlo.yaml

version: "1.0"
last_updated: "2026-01-23"

simulation:
  num_paths:
    development: 1000
    staging: 5000
    production: 10000
  random_seed: 42
  
projection:
  years: 4
  
distribution:
  type: "student_t"
  degrees_of_freedom: 4

confidence_interval:
  level: 0.90
  lower_percentile: 5
  upper_percentile: 95
```

### 11.3 Regime Model Config

```yaml
# config/regime_model.yaml

version: "1.0"
last_updated: "2026-01-23"

regimes:
  bull:
    name: "Bull Market"
    stable_return_mult: 1.0
    crypto_return_mult: 1.5
    volatility_mult: 0.8
    base_probability: 0.40
    
  bear:
    name: "Bear Market"
    stable_return_mult: 0.9
    crypto_return_mult: 0.5
    volatility_mult: 1.2
    base_probability: 0.30
    
  crash:
    name: "Market Crash"
    stable_return_mult: 0.7
    crypto_return_mult: -0.5
    volatility_mult: 2.5
    base_probability: 0.10
    
  recovery:
    name: "Recovery"
    stable_return_mult: 1.1
    crypto_return_mult: 2.0
    volatility_mult: 1.5
    base_probability: 0.20

transition_matrix:
  bull:     [0.70, 0.20, 0.05, 0.05]
  bear:     [0.15, 0.60, 0.20, 0.05]
  crash:    [0.05, 0.30, 0.35, 0.30]
  recovery: [0.40, 0.10, 0.05, 0.45]
```

---

## 12. Implementation Checklist

### 12.1 Phase 1: Data Validation (Week 1)

- [ ] Implement CV-01 through CV-07 validators
- [ ] Create data quality score calculator
- [ ] Set up timeliness checks
- [ ] Implement source reliability scoring
- [ ] Create validation result logger
- [ ] Test with sample data

### 12.2 Phase 2: Battle Test Engine (Week 1-2)

- [ ] Implement daily return calculator
- [ ] Implement DCA logic
- [ ] Implement drawdown tracking
- [ ] Calculate risk metrics (Sharpe, Sortino, Calmar)
- [ ] Implement scenario A and B
- [ ] Create output CSV writer
- [ ] Validate against historical results
- [ ] Test edge cases (missing data, extreme values)

### 12.3 Phase 3: Monte Carlo Engine (Week 2)

- [ ] Implement regime model
- [ ] Implement transition matrix sampling
- [ ] Implement correlation matrix handling
- [ ] Implement Student-t sampling
- [ ] Calculate VaR and CVaR
- [ ] Calculate probability metrics
- [ ] Set up reproducible random seed
- [ ] Validate against expected distributions

### 12.4 Phase 4: Anomaly Detection (Week 3 / Q2)

- [ ] Implement Z-score detection
- [ ] Implement change point detection
- [ ] Implement SPC violation detection
- [ ] (Q2) Implement Isolation Forest
- [ ] (Q2) Implement correlation monitoring
- [ ] Create anomaly alert generator

### 12.5 Phase 5: Integration Tests

- [ ] Test Battle Test â†’ Monte Carlo data flow
- [ ] Test anomaly detection â†’ alert generation
- [ ] Test auto-validation â†’ QR escalation
- [ ] Test Adelaide claims validation
- [ ] End-to-end pipeline test
- [ ] Performance benchmarking

---

## 13. Appendices

### Appendix A: Complete Correlation Matrix Tables

See Section 3.5 for full matrices by regime.

### Appendix B: Validation Rules Summary

| Rule | Description | Threshold | Action on Fail |
|------|-------------|-----------|----------------|
| CV-01 | Data completeness | â‰¥95% | Block pipeline |
| CV-02 | APY range | -100% to 500% | Block pipeline |
| CV-03 | Price change | â‰¤50% daily | Block pipeline |
| CV-04 | Date continuity | â‰¤3 day gap | Block pipeline |
| CV-05 | Allocation sum | = 100% | Block pipeline |
| CV-06 | Gas floor | â‰¥$0.01 | Block pipeline |
| CV-07 | Gas ceiling | â‰¤$50 | Block pipeline |

### Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Battle Test** | Historical backtesting of strategies against actual market data |
| **Monte Carlo** | Forward simulation using thousands of random paths |
| **VaR** | Value at Risk - maximum expected loss at confidence level |
| **CVaR** | Conditional VaR - average loss when VaR is exceeded |
| **Sharpe Ratio** | Risk-adjusted return (can be negative - see Section 4.1.1) |
| **Sortino Ratio** | Downside risk-adjusted return |
| **Calmar Ratio** | Return / Maximum Drawdown |
| **Regime** | Market state (Bull, Bear, Crash, Recovery) |
| **Proxy Data** | Estimated data when real data unavailable (see Section 9.2) |
| **Adelaide** | User-facing newsletter system |

### Appendix D: v2.0 Changes Summary

| Gap ID | Description | Section Updated |
|--------|-------------|-----------------|
| GAP-013 | Negative Sharpe ratio explanation | Section 4.1.1 (NEW) |
| GAP-014 | Proxy data disclaimer and limitations | Section 9.2 (NEW) |

---

**Document End**

*Prepared by QR Board â€” Quantitative Research Board*  
*Jim Simons (Chair), Marcos LÃ³pez de Prado, Nassim Taleb, Andrew Ng, Cathy O'Neil, Emanuel Derman, Yann LeCun, Andrej Karpathy, Anatoly Yakovenko, Claudia Perlich, Hilary Mason*
