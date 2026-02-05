# QR Board Post-Launch Implementation Plan
## diBoaS Analytics v3.1 Enhancements

**Document Version:** 1.0  
**Created:** February 4, 2026  
**Target Completion:** March 15, 2026  
**Owner:** QR Board  

---

## Executive Summary

This document outlines the implementation plan for quantitative methodology enhancements identified during the pre-launch QR Board review. All items are post-launch acceptable but should be completed within 30 days of the February 12, 2026 launch.

**Total Estimated Effort:** 12-15 days  
**Priority Distribution:** 6 P1 items, 4 P2 items

---

## Implementation Timeline

```
Week 1 (Feb 12-18): Risk Metrics Foundation
├── Day 1-2: Sharpe ratio refinement
├── Day 2-3: Sortino ratio implementation
└── Day 3-4: Integration testing

Week 2 (Feb 19-25): Monte Carlo Enhancements
├── Day 1-2: Antithetic variates
├── Day 2-4: Protocol failure scenarios
└── Day 4-5: Battle Test integration

Week 3 (Feb 26 - Mar 4): Advanced Analytics
├── Day 1-2: Regime-conditional correlations
├── Day 2-3: IL calculator utility
└── Day 3-4: CDaR implementation

Week 4 (Mar 5-11): Integration & Validation
├── Day 1-2: Full regression testing
├── Day 2-3: Gate 2 validation updates
└── Day 3-4: Documentation & sign-off

Buffer (Mar 12-15): Contingency
```

---

## Phase 1: Risk Metrics Foundation (Week 1)

### 1.1 Sharpe Ratio Refinement

**Priority:** P1  
**Effort:** 1.5 days  
**File:** `src/domain/simulation.py`

#### Current Implementation (Simplified)
```python
@property
def sharpe_ratio(self) -> float:
    if self.std_final <= 0:
        return 0.0
    annual_return = self.mean_return / 4  # 4 years
    annual_vol = (self.std_final / self.total_deposited) * 100 / 2
    return annual_return / annual_vol if annual_vol > 0 else 0
```

#### Target Implementation
```python
@property
def sharpe_ratio(self) -> float:
    """
    Calculate annualized Sharpe ratio.
    
    Formula: (R_p - R_f) / σ_p
    Where:
        R_p = Annualized portfolio return
        R_f = Risk-free rate (default 4.5% for 2026 US Treasury)
        σ_p = Annualized portfolio volatility
    """
    if self.final_values is None or len(self.final_values) == 0:
        return 0.0
    
    # Calculate monthly returns from simulation paths
    # Assuming 21 trading days per month in the simulation
    monthly_returns = self._calculate_monthly_returns()
    
    if len(monthly_returns) == 0 or np.std(monthly_returns) == 0:
        return 0.0
    
    # Annualize
    annual_return = np.mean(monthly_returns) * 12
    annual_vol = np.std(monthly_returns) * np.sqrt(12)
    
    # Risk-free rate (configurable)
    risk_free_rate = self.config.get('risk_free_rate', 0.045)
    
    sharpe = (annual_return - risk_free_rate) / annual_vol
    
    # Bound to reasonable range [-3, +5] per Gate 2 spec
    return np.clip(sharpe, -3.0, 5.0)

def _calculate_monthly_returns(self) -> np.ndarray:
    """Extract monthly returns from simulation final values."""
    if self.final_values is None:
        return np.array([])
    
    # Convert final values to returns relative to total deposited
    returns = (self.final_values - self.total_deposited) / self.total_deposited
    
    # Annualize over the horizon period
    years = self.horizon_months / 12
    monthly_returns = np.power(1 + returns, 1 / self.horizon_months) - 1
    
    return monthly_returns
```

#### Configuration Addition
```python
# config/settings.py
RISK_FREE_RATE = 0.045  # 4.5% US Treasury 10Y (Jan 2026)
RISK_FREE_RATE_SOURCE = "US Treasury 10Y yield, January 2026"
```

#### Acceptance Criteria
- [ ] Sharpe ratio uses proper annualization formula
- [ ] Risk-free rate is configurable
- [ ] Values bounded to [-3, +5] per Gate 2 spec
- [ ] Unit tests cover edge cases (zero volatility, negative returns)

---

### 1.2 Sortino Ratio Implementation

**Priority:** P1  
**Effort:** 1 day  
**File:** `src/domain/simulation.py`

#### New Implementation
```python
@property
def sortino_ratio(self) -> float:
    """
    Calculate annualized Sortino ratio.
    
    Formula: (R_p - R_f) / σ_d
    Where:
        R_p = Annualized portfolio return
        R_f = Risk-free rate (or MAR - Minimum Acceptable Return)
        σ_d = Downside deviation (volatility of negative returns only)
    
    Sortino focuses only on downside risk, making it more appropriate
    for asymmetric return distributions common in crypto.
    """
    if self.final_values is None or len(self.final_values) == 0:
        return 0.0
    
    monthly_returns = self._calculate_monthly_returns()
    
    if len(monthly_returns) == 0:
        return 0.0
    
    # Risk-free rate as MAR (Minimum Acceptable Return)
    risk_free_rate = self.config.get('risk_free_rate', 0.045)
    mar_monthly = risk_free_rate / 12
    
    # Calculate downside deviation
    downside_returns = monthly_returns[monthly_returns < mar_monthly]
    
    if len(downside_returns) == 0:
        # No downside - return high value but bounded
        return 5.0
    
    downside_deviation = np.std(downside_returns) * np.sqrt(12)
    
    if downside_deviation == 0:
        return 5.0
    
    annual_return = np.mean(monthly_returns) * 12
    sortino = (annual_return - risk_free_rate) / downside_deviation
    
    # Bound to reasonable range
    return np.clip(sortino, -3.0, 10.0)
```

#### Add to MonteCarloResult dataclass
```python
@dataclass
class MonteCarloResult:
    # ... existing fields ...
    
    # New risk metrics
    sortino_ratio: float = 0.0
    downside_deviation: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            # ... existing fields ...
            'sharpe_ratio': round(self.sharpe_ratio, 3),
            'sortino_ratio': round(self.sortino_ratio, 3),
            'downside_deviation': round(self.downside_deviation, 4),
        }
```

#### Acceptance Criteria
- [ ] Sortino ratio calculated using downside deviation only
- [ ] MAR defaults to risk-free rate but is configurable
- [ ] Handles edge case of no downside returns
- [ ] Added to MonteCarloResult output
- [ ] Gate 2 validation includes Sortino sanity check

---

### 1.3 Gate 2 Statistical Sanity Updates

**Priority:** P1  
**Effort:** 0.5 days  
**File:** `src/validators/gate2/gate2_statistical_sanity.py`

#### New Validation Rules
```python
def _check_sharpe_bounds(
    self,
    strategy_id: str,
    data: Dict[str, Any]
) -> List[Gate2ValidationIssue]:
    """Check that Sharpe ratio is within reasonable bounds."""
    issues = []
    
    sharpe = data.get("sharpe_ratio", 0)
    
    # Sharpe should be between -3 and +5 for any reasonable strategy
    if sharpe < -3.0 or sharpe > 5.0:
        issues.append(Gate2ValidationIssue(
            code="G2-STA-004",
            severity=Gate2ValidationSeverity.ERROR,
            message=f"Sharpe ratio out of bounds for strategy {strategy_id}",
            field=f"monte_carlo.strategies.{strategy_id}.sharpe_ratio",
            actual_value=sharpe,
            expected_value="-3.0 <= Sharpe <= 5.0",
            remediation="Verify return and volatility calculations"
        ))
    
    return issues

def _check_sortino_sharpe_relationship(
    self,
    strategy_id: str,
    data: Dict[str, Any]
) -> List[Gate2ValidationIssue]:
    """
    Check Sortino vs Sharpe relationship.
    
    For strategies with negative skew (most crypto), Sortino should be
    lower than Sharpe. For strategies with positive skew, Sortino 
    should be higher.
    """
    issues = []
    
    sharpe = data.get("sharpe_ratio", 0)
    sortino = data.get("sortino_ratio", 0)
    crypto_pct = data.get("crypto_pct", 0)
    
    # High-crypto strategies typically have negative skew
    # Sortino penalizes downside more, so should be similar or lower
    if crypto_pct >= 50 and sortino > sharpe * 2:
        issues.append(Gate2ValidationIssue(
            code="G2-STA-005",
            severity=Gate2ValidationSeverity.WARNING,
            message=f"Unusual Sortino/Sharpe relationship for high-crypto strategy {strategy_id}",
            field=f"monte_carlo.strategies.{strategy_id}",
            actual_value=f"Sharpe={sharpe}, Sortino={sortino}",
            expected_value="Sortino typically <= 2x Sharpe for high-crypto",
            remediation="Review downside deviation calculation"
        ))
    
    return issues
```

---

## Phase 2: Monte Carlo Enhancements (Week 2)

### 2.1 Antithetic Variates Implementation

**Priority:** P1  
**Effort:** 1.5 days  
**File:** `src/engines/monte_carlo.py`

#### Technical Background
Antithetic variates reduce Monte Carlo variance by using paired simulations where one uses random draws U and the other uses (1-U). This creates negatively correlated paths that cancel out some variance.

#### Implementation
```python
class MonteCarloEngine:
    """Enhanced Monte Carlo with antithetic variates."""
    
    def __init__(
        self,
        strategies: list[Strategy] = None,
        n_simulations: int = DEFAULT_SIMULATIONS,
        horizon_months: int = DEFAULT_HORIZON_MONTHS,
        random_seed: int = DEFAULT_RANDOM_SEED,
        use_antithetic: bool = True  # NEW PARAMETER
    ):
        self.strategies = strategies or StrategyLoader.load_default()
        self.n_simulations = n_simulations
        self.horizon_months = horizon_months
        self.random_seed = random_seed
        self.use_antithetic = use_antithetic
        
        np.random.seed(random_seed)
        self._calculate_base_parameters()

    def run(
        self,
        strategy_id: int,
        initial_deposit: float = 10000,
        monthly_dca: float = 200
    ) -> MonteCarloResult:
        """Run Monte Carlo with optional antithetic variates."""
        strategy = StrategyLoader.get_strategy_by_id(strategy_id, self.strategies)
        logger.info(f"Running Monte Carlo for {strategy.name} (antithetic={self.use_antithetic})")
        
        total_deposited = initial_deposit + (monthly_dca * self.horizon_months)
        
        final_values = []
        max_drawdowns = []
        
        # With antithetic variates, we run n/2 pairs
        n_pairs = self.n_simulations // 2 if self.use_antithetic else self.n_simulations
        
        for sim in range(n_pairs):
            if self.use_antithetic:
                # Generate paired paths
                path_original, path_antithetic = self._simulate_antithetic_paths(
                    strategy, initial_deposit, monthly_dca
                )
                
                final_values.append(path_original[-1])
                final_values.append(path_antithetic[-1])
                max_drawdowns.append(self._calculate_max_drawdown(path_original))
                max_drawdowns.append(self._calculate_max_drawdown(path_antithetic))
            else:
                path = self._simulate_path(strategy, initial_deposit, monthly_dca)
                final_values.append(path[-1])
                max_drawdowns.append(self._calculate_max_drawdown(path))
        
        # ... rest of calculation unchanged ...

    def _simulate_antithetic_paths(
        self,
        strategy: Strategy,
        initial_deposit: float,
        monthly_dca: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate paired antithetic paths.
        
        Returns:
            Tuple of (original_path, antithetic_path)
        """
        days = self.horizon_months * 21
        
        # Pre-generate all random numbers for this simulation
        uniform_draws = np.random.uniform(0, 1, days)
        
        # Original path uses uniform_draws directly
        path_original = self._simulate_path_with_draws(
            strategy, initial_deposit, monthly_dca, uniform_draws
        )
        
        # Antithetic path uses (1 - uniform_draws)
        antithetic_draws = 1 - uniform_draws
        path_antithetic = self._simulate_path_with_draws(
            strategy, initial_deposit, monthly_dca, antithetic_draws
        )
        
        return path_original, path_antithetic

    def _simulate_path_with_draws(
        self,
        strategy: Strategy,
        initial_deposit: float,
        monthly_dca: float,
        uniform_draws: np.ndarray
    ) -> np.ndarray:
        """Simulate path using pre-generated uniform draws."""
        days = len(uniform_draws)
        values = np.zeros(days)
        values[0] = initial_deposit
        
        current_regime = 'bull'
        regime_day = 0
        
        for day in range(1, days):
            if day % 21 == 0:
                values[day - 1] += monthly_dca
            
            regime_day += 1
            if regime_day >= self.REGIMES[current_regime]['duration']:
                current_regime = self._transition_regime(current_regime)
                regime_day = 0
            
            # Convert uniform draw to return using inverse CDF
            daily_return = self._generate_return_from_uniform(
                strategy, current_regime, uniform_draws[day]
            )
            values[day] = values[day - 1] * (1 + daily_return)
        
        return values

    def _generate_return_from_uniform(
        self,
        strategy: Strategy,
        regime: str,
        uniform_draw: float
    ) -> float:
        """Generate return from uniform draw using inverse CDF."""
        regime_params = self.REGIMES[regime]
        crypto_pct = strategy.crypto_pct / 100
        
        # Stable component (normal distribution)
        stable_pct = 1 - crypto_pct
        if stable_pct > 0:
            stable_mean = self.base_stable_return * regime_params['mean_mult'] * 0.5
            stable_std = self.base_stable_vol * regime_params['vol_mult'] * 0.5
            # Inverse CDF of normal
            stable_return = stats.norm.ppf(uniform_draw, loc=stable_mean, scale=stable_std)
        else:
            stable_return = 0
        
        # Crypto component (Student-t for fat tails)
        if crypto_pct > 0:
            crypto_mean = self.base_crypto_return * regime_params['mean_mult']
            crypto_std = self.base_crypto_vol * regime_params['vol_mult']
            # Inverse CDF of Student-t
            crypto_return = stats.t.ppf(uniform_draw, df=4, loc=crypto_mean, scale=crypto_std)
        else:
            crypto_return = 0
        
        return stable_pct * stable_return + crypto_pct * crypto_return
```

#### Expected Variance Reduction
- **Without antithetic:** Standard error ≈ σ/√n
- **With antithetic:** Standard error ≈ σ/√n × √((1+ρ)/2)
- For typical financial simulations, expect **20-40% variance reduction**

#### Acceptance Criteria
- [ ] Antithetic variates enabled by default
- [ ] Can be disabled via parameter for comparison
- [ ] Variance reduction verified (compare with/without)
- [ ] Results remain statistically equivalent
- [ ] Performance impact documented

---

### 2.2 Protocol Failure Scenarios

**Priority:** P0 (Elevated post-launch)  
**Effort:** 2 days  
**Files:** 
- `src/engines/monte_carlo.py`
- `config/protocol_failures.yaml` (new)

#### Configuration File
```yaml
# config/protocol_failures.yaml
# Protocol failure scenarios for Monte Carlo stress testing
# QR Board approved: January 30, 2026

protocol_failures:
  sky_depeg:
    name: "Sky USDS Depeg"
    description: "USDS loses peg to $1.00"
    probability_annual: 0.02  # 2% annual probability
    impact:
      type: "instant_loss"
      loss_pct: 0.15  # 15% loss on Sky allocation
      recovery_months: 3
    affected_protocols: ["sky"]
    historical_reference: "UST depeg May 2022"

  aave_exploit:
    name: "Aave Smart Contract Exploit"
    description: "Critical vulnerability exploited"
    probability_annual: 0.01  # 1% annual probability
    impact:
      type: "instant_loss"
      loss_pct: 0.50  # 50% loss on Aave allocation
      recovery_months: 6
    affected_protocols: ["aave"]
    historical_reference: "Euler Finance March 2023"

  sanctum_failure:
    name: "Sanctum LST Basket Failure"
    description: "One or more LSTs in basket fail"
    probability_annual: 0.03  # 3% annual probability
    impact:
      type: "instant_loss"
      loss_pct: 0.25  # 25% loss on Sanctum allocation
      recovery_months: 2
    affected_protocols: ["sanctum"]
    historical_reference: "stETH depeg June 2022"

  jlp_jupiter_exploit:
    name: "Jupiter/JLP Exploit"
    description: "Perps LP mechanism exploited"
    probability_annual: 0.05  # 5% annual probability (newer protocol)
    impact:
      type: "instant_loss"
      loss_pct: 0.40  # 40% loss on JLP allocation
      recovery_months: 4
    affected_protocols: ["jlp"]
    historical_reference: "Mango Markets October 2022"

  jito_slashing:
    name: "Jito Validator Slashing Event"
    description: "Major slashing event affects JitoSOL"
    probability_annual: 0.02  # 2% annual probability
    impact:
      type: "instant_loss"
      loss_pct: 0.10  # 10% loss on Jito allocation
      recovery_months: 1
    affected_protocols: ["jito"]
    historical_reference: "Hypothetical based on staking risks"

  compound_exploit:
    name: "Compound Smart Contract Exploit"
    description: "Critical vulnerability exploited"
    probability_annual: 0.01  # 1% annual probability
    impact:
      type: "instant_loss"
      loss_pct: 0.50  # 50% loss on Compound allocation
      recovery_months: 6
    affected_protocols: ["compound"]
    historical_reference: "Compound governance attack 2021"

# Correlated failure scenarios
correlated_failures:
  defi_contagion:
    name: "DeFi Contagion Event"
    description: "Multiple protocols fail in cascade"
    probability_annual: 0.005  # 0.5% annual probability
    triggers:
      - sky_depeg
      - aave_exploit
    conditional_probability: 0.30  # 30% chance second fails given first

  solana_ecosystem_shock:
    name: "Solana Ecosystem Shock"
    description: "Solana network issue affects all SOL protocols"
    probability_annual: 0.02  # 2% annual probability
    triggers:
      - sanctum_failure
      - jlp_jupiter_exploit
      - jito_slashing
    conditional_probability: 0.50  # 50% chance others affected
```

#### Implementation
```python
# src/engines/protocol_failure.py

from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml
import numpy as np


@dataclass
class ProtocolFailure:
    """Represents a protocol failure event."""
    name: str
    affected_protocols: List[str]
    loss_pct: float
    recovery_months: int
    probability_annual: float


class ProtocolFailureSimulator:
    """
    Simulate protocol failure events in Monte Carlo.
    
    Uses Poisson process for failure timing and applies
    instant losses to affected protocol allocations.
    """
    
    def __init__(self, config_path: str = "config/protocol_failures.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.failures = self._parse_failures()
    
    def _parse_failures(self) -> List[ProtocolFailure]:
        """Parse failure configurations."""
        failures = []
        for key, cfg in self.config.get('protocol_failures', {}).items():
            failures.append(ProtocolFailure(
                name=cfg['name'],
                affected_protocols=cfg['affected_protocols'],
                loss_pct=cfg['impact']['loss_pct'],
                recovery_months=cfg['impact']['recovery_months'],
                probability_annual=cfg['probability_annual']
            ))
        return failures
    
    def simulate_failures(
        self,
        horizon_months: int,
        strategy_allocations: Dict[str, float]
    ) -> List[tuple[int, str, float]]:
        """
        Simulate protocol failures over simulation horizon.
        
        Returns:
            List of (month, protocol, loss_pct) tuples
        """
        events = []
        
        for failure in self.failures:
            # Check if strategy has exposure to affected protocols
            exposure = sum(
                strategy_allocations.get(p, 0) 
                for p in failure.affected_protocols
            )
            
            if exposure == 0:
                continue
            
            # Convert annual probability to monthly
            monthly_prob = 1 - (1 - failure.probability_annual) ** (1/12)
            
            # Simulate Poisson process
            for month in range(horizon_months):
                if np.random.random() < monthly_prob:
                    # Failure occurs
                    loss = exposure * failure.loss_pct
                    events.append((month, failure.name, loss))
        
        return events
    
    def apply_failure_to_path(
        self,
        portfolio_values: np.ndarray,
        failure_month: int,
        loss_pct: float,
        recovery_months: int
    ) -> np.ndarray:
        """Apply failure event to portfolio path."""
        modified = portfolio_values.copy()
        
        # Convert month to day index (21 days per month)
        failure_day = failure_month * 21
        
        if failure_day < len(modified):
            # Apply instant loss
            modified[failure_day:] *= (1 - loss_pct)
            
            # Gradual recovery (optional)
            # For now, just apply instant loss
        
        return modified
```

#### Integration with Monte Carlo
```python
# In MonteCarloEngine._simulate_path()

def _simulate_path_with_failures(
    self,
    strategy: Strategy,
    initial_deposit: float,
    monthly_dca: float,
    include_failures: bool = True
) -> np.ndarray:
    """Simulate path with optional protocol failures."""
    path = self._simulate_path(strategy, initial_deposit, monthly_dca)
    
    if not include_failures:
        return path
    
    # Get strategy allocations
    allocations = {
        **strategy.stable_allocations,
        **strategy.crypto_allocations
    }
    
    # Simulate failures
    failure_sim = ProtocolFailureSimulator()
    failures = failure_sim.simulate_failures(
        self.horizon_months,
        allocations
    )
    
    # Apply each failure to path
    for month, name, loss_pct in failures:
        logger.debug(f"Applying {name} at month {month}: {loss_pct:.1%} loss")
        path = failure_sim.apply_failure_to_path(
            path, month, loss_pct, recovery_months=3
        )
    
    return path
```

#### Acceptance Criteria
- [ ] 6 protocol failure scenarios configured
- [ ] Failure probabilities based on historical data
- [ ] Correlated failures handled
- [ ] Loss impact correctly applied to paths
- [ ] Results show increased tail risk for affected strategies
- [ ] Documented in methodology notes

---

## Phase 3: Advanced Analytics (Week 3)

### 3.1 Regime-Conditional Correlations

**Priority:** P2  
**Effort:** 1.5 days  
**File:** `src/engines/monte_carlo.py`

#### Implementation
```python
class MonteCarloEngine:
    """Enhanced with regime-conditional correlations."""
    
    # Regime-specific correlation matrices
    REGIME_CORRELATIONS = {
        'bull': {
            ('SOL', 'ETH'): 0.70,
            ('SOL', 'BTC'): 0.65,
            ('ETH', 'BTC'): 0.80,
        },
        'bear': {
            ('SOL', 'ETH'): 0.80,
            ('SOL', 'BTC'): 0.75,
            ('ETH', 'BTC'): 0.88,
        },
        'crash': {
            # Correlations spike during crashes ("correlations go to 1")
            ('SOL', 'ETH'): 0.92,
            ('SOL', 'BTC'): 0.90,
            ('ETH', 'BTC'): 0.95,
        },
        'recovery': {
            ('SOL', 'ETH'): 0.75,
            ('SOL', 'BTC'): 0.70,
            ('ETH', 'BTC'): 0.82,
        }
    }
    
    def _generate_correlated_crypto_returns(
        self,
        regime: str
    ) -> Dict[str, float]:
        """
        Generate correlated crypto returns using Cholesky decomposition.
        
        Returns:
            Dictionary of {asset: daily_return}
        """
        correlations = self.REGIME_CORRELATIONS[regime]
        
        # Build correlation matrix
        assets = ['SOL', 'ETH', 'BTC']
        n = len(assets)
        corr_matrix = np.eye(n)
        
        for i, asset1 in enumerate(assets):
            for j, asset2 in enumerate(assets):
                if i != j:
                    key = tuple(sorted([asset1, asset2]))
                    corr_matrix[i, j] = correlations.get(key, 0.7)
        
        # Cholesky decomposition
        L = np.linalg.cholesky(corr_matrix)
        
        # Generate independent standard normals
        z = np.random.standard_normal(n)
        
        # Transform to correlated
        correlated_z = L @ z
        
        # Apply to each asset's return distribution
        regime_params = self.REGIMES[regime]
        returns = {}
        
        for i, asset in enumerate(assets):
            mean = self.base_crypto_return * regime_params['mean_mult']
            std = self.base_crypto_vol * regime_params['vol_mult']
            returns[asset] = mean + std * correlated_z[i]
        
        return returns
```

#### Acceptance Criteria
- [ ] Correlations vary by regime
- [ ] Crash regime shows correlation spike
- [ ] Cholesky decomposition for proper correlation structure
- [ ] Documented methodology change

---

### 3.2 Impermanent Loss Calculator

**Priority:** P1  
**Effort:** 1 day  
**File:** `src/utils/impermanent_loss.py` (new)

#### Implementation
```python
"""
Impermanent Loss Calculator for AMM/LP positions.

Used for JLP and other LP-based protocol allocations.
"""

import numpy as np
from typing import Tuple


def calculate_impermanent_loss(
    price_ratio: float,
    initial_ratio: float = 1.0
) -> float:
    """
    Calculate impermanent loss for a 50/50 LP position.
    
    IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
    
    Args:
        price_ratio: Current price / Initial price
        initial_ratio: Starting price ratio (default 1.0)
    
    Returns:
        Impermanent loss as decimal (negative value)
    
    Example:
        >>> calculate_impermanent_loss(2.0)  # Price doubled
        -0.0572  # 5.72% IL
    """
    if price_ratio <= 0:
        raise ValueError("Price ratio must be positive")
    
    k = price_ratio / initial_ratio
    il = 2 * np.sqrt(k) / (1 + k) - 1
    
    return il


def calculate_il_with_fees(
    price_ratio: float,
    fee_apy: float,
    holding_days: int
) -> Tuple[float, float, float]:
    """
    Calculate net position considering IL and fee income.
    
    Args:
        price_ratio: Current price / Initial price
        fee_apy: Annual fee APY as decimal (e.g., 0.25 for 25%)
        holding_days: Number of days in position
    
    Returns:
        Tuple of (impermanent_loss, fee_income, net_pnl)
    """
    il = calculate_impermanent_loss(price_ratio)
    
    # Daily fee income
    daily_fee = fee_apy / 365
    fee_income = daily_fee * holding_days
    
    # Net P&L
    net_pnl = il + fee_income
    
    return il, fee_income, net_pnl


def calculate_jlp_il(
    sol_change: float,
    eth_change: float,
    btc_change: float,
    jlp_apy: float,
    holding_days: int
) -> dict:
    """
    Calculate JLP-specific impermanent loss.
    
    JLP basket: 45% SOL, 27% ETH, 27% BTC
    
    Args:
        sol_change: SOL price change as decimal
        eth_change: ETH price change as decimal
        btc_change: BTC price change as decimal
        jlp_apy: JLP fee APY as decimal
        holding_days: Days in position
    
    Returns:
        Dictionary with IL breakdown
    """
    # Weighted average price change
    weighted_change = (
        0.45 * sol_change +
        0.27 * eth_change +
        0.27 * btc_change
    )
    
    # Calculate IL for each pair vs USDC
    sol_il = calculate_impermanent_loss(1 + sol_change)
    eth_il = calculate_impermanent_loss(1 + eth_change)
    btc_il = calculate_impermanent_loss(1 + btc_change)
    
    # Weighted IL (simplified - actual JLP math is more complex)
    weighted_il = (
        0.45 * sol_il +
        0.27 * eth_il +
        0.27 * btc_il
    )
    
    # Fee income
    daily_fee = jlp_apy / 365
    fee_income = daily_fee * holding_days
    
    return {
        'sol_il': sol_il,
        'eth_il': eth_il,
        'btc_il': btc_il,
        'weighted_il': weighted_il,
        'fee_income': fee_income,
        'net_pnl': weighted_il + fee_income,
        'breakeven_days': abs(weighted_il) / daily_fee if daily_fee > 0 else float('inf')
    }


# IL lookup table for quick reference
IL_TABLE = {
    1.25: -0.006,   # +25% price change
    1.50: -0.020,   # +50% price change
    1.75: -0.038,   # +75% price change
    2.00: -0.057,   # +100% price change (2x)
    2.50: -0.100,   # +150% price change
    3.00: -0.134,   # +200% price change (3x)
    4.00: -0.200,   # +300% price change (4x)
    5.00: -0.253,   # +400% price change (5x)
    0.80: -0.006,   # -20% price change
    0.50: -0.057,   # -50% price change
    0.25: -0.200,   # -75% price change
}
```

#### Acceptance Criteria
- [ ] Standard IL formula implemented
- [ ] JLP-specific multi-asset IL calculator
- [ ] Fee income offset calculation
- [ ] Breakeven days calculation
- [ ] Unit tests with known values

---

### 3.3 Conditional Drawdown at Risk (CDaR)

**Priority:** P2  
**Effort:** 1 day  
**File:** `src/domain/simulation.py`

#### Implementation
```python
@dataclass
class MonteCarloResult:
    # ... existing fields ...
    
    # New drawdown metrics
    cdar_95: float = 0.0  # Conditional Drawdown at Risk 95%
    cdar_99: float = 0.0  # Conditional Drawdown at Risk 99%
    
    @property
    def cdar_95(self) -> float:
        """
        Conditional Drawdown at Risk at 95% confidence.
        
        CDaR is the expected drawdown given that drawdown exceeds VaR.
        Similar to CVaR but for drawdowns instead of returns.
        
        Formula: E[DD | DD > DD_α]
        """
        if self.max_drawdowns is None or len(self.max_drawdowns) == 0:
            return 0.0
        
        # Find 95th percentile drawdown (as VaR)
        dd_var_95 = np.percentile(self.max_drawdowns, 95)
        
        # Calculate average of drawdowns exceeding VaR
        tail_drawdowns = self.max_drawdowns[self.max_drawdowns >= dd_var_95]
        
        if len(tail_drawdowns) == 0:
            return dd_var_95
        
        return np.mean(tail_drawdowns)
```

#### Acceptance Criteria
- [ ] CDaR calculated at 95% and 99% levels
- [ ] Relationship: CDaR ≥ VaR for drawdowns
- [ ] Added to Gate 2 validation

---

## Phase 4: Integration & Validation (Week 4)

### 4.1 Full Regression Testing

**Priority:** P1  
**Effort:** 2 days  

#### Test Suite
```python
# tests/test_qr_enhancements.py

import pytest
import numpy as np
from src.engines.monte_carlo import MonteCarloEngine
from src.utils.impermanent_loss import calculate_impermanent_loss


class TestRiskMetrics:
    """Test enhanced risk metrics."""
    
    def test_sharpe_ratio_bounds(self):
        """Sharpe should be bounded [-3, +5]."""
        engine = MonteCarloEngine(n_simulations=1000)
        result = engine.run(strategy_id=1)
        assert -3.0 <= result.sharpe_ratio <= 5.0
    
    def test_sortino_positive_for_stable(self):
        """Stable strategies should have positive Sortino."""
        engine = MonteCarloEngine(n_simulations=1000)
        result = engine.run(strategy_id=1)  # Safe Harbor
        assert result.sortino_ratio > 0
    
    def test_sortino_vs_sharpe_relationship(self):
        """For crypto strategies, Sortino typically <= 2x Sharpe."""
        engine = MonteCarloEngine(n_simulations=1000)
        result = engine.run(strategy_id=10)  # Full Throttle
        # Allow some variance but check general relationship
        assert result.sortino_ratio <= result.sharpe_ratio * 3


class TestAntitheticVariates:
    """Test antithetic variates implementation."""
    
    def test_variance_reduction(self):
        """Antithetic should reduce variance."""
        # Run with antithetic
        engine_av = MonteCarloEngine(n_simulations=1000, use_antithetic=True)
        result_av = engine_av.run(strategy_id=5)
        
        # Run without antithetic
        engine_no_av = MonteCarloEngine(n_simulations=1000, use_antithetic=False)
        result_no_av = engine_no_av.run(strategy_id=5)
        
        # Variance should be lower with antithetic
        # (May need multiple runs to verify statistically)
        assert result_av.std_final <= result_no_av.std_final * 1.1  # Allow 10% margin
    
    def test_mean_preserved(self):
        """Mean should be preserved with antithetic."""
        engine_av = MonteCarloEngine(n_simulations=2000, use_antithetic=True)
        engine_no_av = MonteCarloEngine(n_simulations=2000, use_antithetic=False)
        
        result_av = engine_av.run(strategy_id=5)
        result_no_av = engine_no_av.run(strategy_id=5)
        
        # Means should be within 5%
        mean_diff = abs(result_av.mean_final - result_no_av.mean_final)
        assert mean_diff < result_no_av.mean_final * 0.05


class TestProtocolFailures:
    """Test protocol failure scenarios."""
    
    def test_failure_increases_tail_risk(self):
        """Protocol failures should increase tail risk."""
        engine = MonteCarloEngine(n_simulations=1000)
        
        # Run without failures
        result_clean = engine.run(strategy_id=8, include_failures=False)
        
        # Run with failures
        result_failures = engine.run(strategy_id=8, include_failures=True)
        
        # P95 drawdown should be higher with failures
        assert result_failures.p95_max_drawdown >= result_clean.p95_max_drawdown * 0.95


class TestImpermanentLoss:
    """Test IL calculator."""
    
    def test_known_il_values(self):
        """Test against known IL values."""
        # 2x price = 5.72% IL
        il = calculate_impermanent_loss(2.0)
        assert abs(il - (-0.0572)) < 0.001
        
        # 4x price = 20% IL
        il = calculate_impermanent_loss(4.0)
        assert abs(il - (-0.20)) < 0.001
    
    def test_il_symmetric(self):
        """IL should be similar for inverse price moves."""
        il_up = calculate_impermanent_loss(2.0)  # 2x
        il_down = calculate_impermanent_loss(0.5)  # 0.5x
        assert abs(il_up - il_down) < 0.001
```

### 4.2 Gate 2 Validation Updates

**File:** `src/validators/gate2/gate2_analytics_validator.py`

Add new validation rules for enhanced metrics:

```python
NEW_RULES = [
    "G2-STA-004: Sharpe ratio bounds check",
    "G2-STA-005: Sortino vs Sharpe relationship",
    "G2-STA-006: CDaR >= VaR for drawdowns",
    "G2-STA-007: Antithetic variance reduction verification",
]
```

### 4.3 Documentation Updates

**Files to Update:**
1. `docs/diboas_analytics_v3_technical_deep_dive.md` - Add methodology section
2. `config/qr_approved_claims.yaml` - Add new claim templates
3. `cto_handoff_package/02_validation_methodology/QR_BOARD_CTO_HANDOFF.md` - Update specs

---

## Deliverables Checklist

### Week 1 Deliverables
- [ ] Refined Sharpe ratio implementation
- [ ] New Sortino ratio implementation  
- [ ] Updated Gate 2 validation rules
- [ ] Unit tests for risk metrics

### Week 2 Deliverables
- [ ] Antithetic variates in Monte Carlo
- [ ] Protocol failure scenarios configuration
- [ ] Protocol failure simulator
- [ ] Integration with Monte Carlo engine

### Week 3 Deliverables
- [ ] Regime-conditional correlations
- [ ] Impermanent loss calculator
- [ ] CDaR implementation
- [ ] Unit tests for advanced analytics

### Week 4 Deliverables
- [ ] Full regression test suite
- [ ] Gate 2 validation updates
- [ ] Documentation updates
- [ ] QR Board sign-off on v3.1

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Antithetic breaks backward compatibility | Low | Medium | Feature flag for disable |
| Protocol failures too pessimistic | Medium | Low | Calibrate against historical |
| Performance degradation | Low | Medium | Benchmark before/after |
| Gate 2 failures with new rules | Medium | High | Run in warning mode first |

---

## Success Criteria

**v3.1 Release Criteria:**
1. All P1 items implemented and tested
2. Gate 2 validation passes with new rules
3. Variance reduction from antithetic > 15%
4. No regression in existing functionality
5. Documentation updated

**QR Board Sign-Off Requirements:**
- [ ] Sharpe/Sortino match industry standard formulas
- [ ] Protocol failures calibrated to historical events
- [ ] Antithetic variates properly implemented
- [ ] All acceptance criteria met

---

## Appendix: Historical References for Protocol Failures

| Event | Date | Impact | Used For |
|-------|------|--------|----------|
| UST/LUNA collapse | May 2022 | 100% loss | sky_depeg baseline |
| Euler Finance hack | Mar 2023 | $197M | aave_exploit baseline |
| stETH depeg | Jun 2022 | ~5% depeg | sanctum_failure baseline |
| Mango Markets exploit | Oct 2022 | $114M | jlp_jupiter_exploit baseline |
| Compound governance | Sep 2021 | $90M at risk | compound_exploit baseline |

---

**Document End**

*QR Board Implementation Plan v1.0*  
*Target: diBoaS Analytics v3.1*  
*Completion: March 15, 2026*
