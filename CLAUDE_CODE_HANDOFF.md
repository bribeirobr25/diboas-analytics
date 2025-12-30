# diBoaS Analytics Application — Claude Code Handoff

**Document Purpose:** Complete specification for Claude Code to build the diBoaS Analytics application
**Created:** December 29, 2025
**Updated:** December 30, 2025 (Added Section 13: Dream Mode Export)
**Created By:** CTO Board (Claude Web Interface)
**For:** Claude Code Implementation

---

## EXECUTIVE SUMMARY

Build a Python CLI application called `diboas-analytics` that performs:
1. **Data Collection** — Fetch historical APY and price data from APIs
2. **Battle Test** — Historical backtesting of 10 investment strategies
3. **Monte Carlo Simulation** — Forward-looking risk analysis with 5,000+ simulations
4. **Protocol Monitoring** — Real-time health checks with alerting
5. **Anomaly Detection** — ML-based unusual behavior detection
6. **Dream Mode Export** — Consumer-ready JSON for frontend features (NEW)

The application should be production-grade, extensible, and follow clean architecture principles.

---

## TABLE OF CONTENTS

1. [Project Structure](#1-project-structure)
2. [Strategy Definitions](#2-strategy-definitions)
3. [Data Collection Module](#3-data-collection-module)
4. [Battle Test Module](#4-battle-test-module)
5. [Monte Carlo Module](#5-monte-carlo-module)
6. [Protocol Monitoring Module](#6-protocol-monitoring-module)
7. [Anomaly Detection Module](#7-anomaly-detection-module)
8. [Validation Rules](#8-validation-rules)
9. [CLI Interface](#9-cli-interface)
10. [Configuration Files](#10-configuration-files)
11. [Testing Requirements](#11-testing-requirements)
12. [Data Files](#12-data-files)
13. [Dream Mode Export Module](#13-dream-mode-export-module) (NEW)

---

# 1. PROJECT STRUCTURE

```
diboas-analytics/
│
├── main.py                          # CLI entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Documentation
├── .env.example                     # Environment variables template
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── strategies.json              # 10 official strategies (v2.0)
│   ├── protocols.py                 # Protocol registry
│   ├── chains.py                    # Chain configurations
│   ├── thresholds.py                # Alert thresholds
│   ├── dream_mode.py                # Dream Mode path mappings (NEW)
│   └── settings.py                  # Application settings
│
├── src/
│   ├── __init__.py
│   │
│   ├── domain/                      # Domain models
│   │   ├── __init__.py
│   │   ├── strategy.py              # Strategy dataclass
│   │   ├── protocol.py              # Protocol dataclass
│   │   ├── simulation.py            # Simulation result models
│   │   ├── alert.py                 # Alert models
│   │   └── dream_mode.py            # Dream Mode models (NEW)
│   │
│   ├── collectors/                  # Data collection
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract DataProvider
│   │   ├── defillama.py             # DeFiLlama API
│   │   ├── yahoo.py                 # Yahoo Finance API
│   │   ├── jupiter.py               # Jupiter API
│   │   └── file_loader.py           # Load bundled CSV files
│   │
│   ├── engines/                     # Core computation
│   │   ├── __init__.py
│   │   ├── battle_test.py           # Historical backtesting
│   │   ├── monte_carlo.py           # Monte Carlo simulation
│   │   ├── monitoring.py            # Protocol health checks
│   │   ├── anomaly.py               # Anomaly detection
│   │   └── dream_mode_export.py     # Dream Mode data export (NEW)
│   │
│   ├── models/                      # ML models for anomaly detection
│   │   ├── __init__.py
│   │   ├── zscore.py                # Z-score detector
│   │   ├── isolation_forest.py      # Isolation Forest
│   │   ├── correlation.py           # Correlation monitor
│   │   └── change_point.py          # Change point detection
│   │
│   ├── validators/                  # Validation rules
│   │   ├── __init__.py
│   │   ├── data_validator.py        # Input data validation
│   │   ├── result_validator.py      # CV-01 through CV-07
│   │   └── config_validator.py      # Strategy config validation
│   │
│   ├── reporters/                   # Output generation
│   │   ├── __init__.py
│   │   ├── csv_reporter.py          # CSV output
│   │   ├── json_reporter.py         # JSON output
│   │   └── markdown_reporter.py     # Markdown reports
│   │
│   ├── notifiers/                   # Alert notifications
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract Notifier
│   │   ├── console.py               # Console output
│   │   ├── slack.py                 # Slack webhook
│   │   └── email.py                 # Email (Phase 2)
│   │
│   └── utils/                       # Utilities
│       ├── __init__.py
│       ├── dates.py                 # Date utilities
│       ├── proxies.py               # APY proxy calculations
│       ├── logging.py               # Logging setup
│       └── hashing.py               # Config hashing for audit
│
├── data/                            # Bundled historical data
│   ├── defillama_historical_apy.csv
│   ├── yahoo_historical_prices.csv
│   ├── jupiter_jlp_historical_apy.csv
│   └── perps_lp_combined_apy.csv
│
├── outputs/                         # Generated results (gitignored)
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── test_battle_test.py
│   ├── test_monte_carlo.py
│   ├── test_validators.py
│   ├── test_collectors.py
│   └── test_dream_mode.py           # Dream Mode tests (NEW)
│
└── storage/                         # SQLite database (gitignored)
    └── .gitkeep
```

---

# 2. STRATEGY DEFINITIONS

## 2.1 Official v2.0 Strategies

**CRITICAL: Never hardcode these. Always load from `config/strategies.json`**

```json
{
  "version": "2.0",
  "strategies": [
    {
      "id": 1,
      "name": "Safe Harbor",
      "goal": "Emergency Fund",
      "crypto_pct": 0,
      "allocations": {
        "stable": { "sky": 0.50, "aave": 0.30, "compound": 0.20 },
        "crypto": {}
      }
    },
    {
      "id": 2,
      "name": "Stable Growth",
      "goal": "Emergency Fund",
      "crypto_pct": 30,
      "allocations": {
        "stable": { "sky": 0.70 },
        "crypto": { "sanctum": 0.30 }
      }
    },
    {
      "id": 3,
      "name": "Goal Keeper",
      "goal": "Short-Term",
      "crypto_pct": 0,
      "allocations": {
        "stable": { "sky": 0.60, "aave": 0.25, "compound": 0.15 },
        "crypto": {}
      }
    },
    {
      "id": 4,
      "name": "Steady Progress",
      "goal": "Short-Term",
      "crypto_pct": 35,
      "allocations": {
        "stable": { "sky": 0.65 },
        "crypto": { "sanctum": 0.35 }
      }
    },
    {
      "id": 5,
      "name": "Patient Builder",
      "goal": "Medium-Term",
      "crypto_pct": 0,
      "allocations": {
        "stable": { "sky": 0.50, "aave": 0.30, "compound": 0.20 },
        "crypto": {}
      }
    },
    {
      "id": 6,
      "name": "Balanced Builder",
      "goal": "Medium-Term",
      "crypto_pct": 40,
      "allocations": {
        "stable": { "sky": 0.60 },
        "crypto": { "sanctum": 0.25, "jlp": 0.15 }
      }
    },
    {
      "id": 7,
      "name": "Steady Compounder",
      "goal": "Long-Term",
      "crypto_pct": 0,
      "allocations": {
        "stable": { "sky": 0.55, "aave": 0.30, "compound": 0.15 },
        "crypto": {}
      }
    },
    {
      "id": 8,
      "name": "Wealth Accelerator",
      "goal": "Long-Term",
      "crypto_pct": 70,
      "allocations": {
        "stable": { "sky": 0.30 },
        "crypto": { "sanctum": 0.35, "jlp": 0.35 }
      }
    },
    {
      "id": 9,
      "name": "Yield Maximizer",
      "goal": "Wealth Building",
      "crypto_pct": 0,
      "allocations": {
        "stable": { "sky": 0.45, "aave": 0.35, "compound": 0.20 },
        "crypto": {}
      }
    },
    {
      "id": 10,
      "name": "Full Throttle",
      "goal": "Wealth Building",
      "crypto_pct": 85,
      "allocations": {
        "stable": { "sky": 0.15 },
        "crypto": { "sanctum": 0.30, "jlp": 0.35, "jito": 0.20 }
      }
    }
  ]
}
```

## 2.2 Protocol Definitions

```python
# config/protocols.py

PROTOCOLS = {
    # Stablecoin Yield (No Crypto Exposure)
    'sky': {
        'name': 'Sky SSR',
        'chain': 'arbitrum',
        'asset': 'USDS',
        'type': 'stablecoin_yield',
        'defillama_project': 'sky-lending',
        'crypto_exposure': False
    },
    'aave': {
        'name': 'Aave V3',
        'chain': 'arbitrum',
        'asset': 'USDC',
        'type': 'lending',
        'defillama_project': 'aave-v3',
        'crypto_exposure': False
    },
    'compound': {
        'name': 'Compound V3',
        'chain': 'arbitrum',
        'asset': 'USDC',
        'type': 'lending',
        'defillama_project': 'compound-v3',
        'crypto_exposure': False
    },
    
    # Crypto Exposure
    'sanctum': {
        'name': 'Sanctum INF',
        'chain': 'solana',
        'asset': 'SOL LST Basket',
        'type': 'liquid_staking',
        'crypto_exposure': True,
        'price_exposure': 'SOL'
    },
    'jito': {
        'name': 'Jito',
        'chain': 'solana',
        'asset': 'JitoSOL',
        'type': 'liquid_staking_mev',
        'crypto_exposure': True,
        'price_exposure': 'SOL'
    },
    'jlp': {
        'name': 'Jupiter JLP',
        'chain': 'solana',
        'asset': 'Perps LP',
        'type': 'perps_lp',
        'crypto_exposure': True,
        'basket_composition': {
            'SOL': 0.45,
            'ETH': 0.27,
            'BTC': 0.27,
            'other': 0.01
        }
    },
    
    # For Proxy Calculations Only
    'lido': {
        'name': 'Lido',
        'chain': 'ethereum',
        'asset': 'stETH',
        'type': 'liquid_staking',
        'defillama_project': 'lido',
        'used_for': 'proxy_calculations_only'
    }
}
```

## 2.3 Proxy Formulas

When historical data is unavailable, use these formulas:

```python
# src/utils/proxies.py

def get_sanctum_apy(lido_apy: float) -> float:
    """Sanctum INF proxy: SOL staking ≈ 2× ETH staking + basket premium"""
    return lido_apy * 2.0 + 0.5

def get_jito_apy(lido_apy: float) -> float:
    """Jito proxy: SOL staking + MEV premium"""
    return lido_apy * 2.0 + 1.0

def get_jlp_apy() -> float:
    """JLP proxy (pre-Jan 2024): Based on GMX GLP historical average"""
    return 25.0  # Fixed 25% APY

def get_compound_apy(aave_apy: float) -> float:
    """Compound V3 proxy (pre-Oct 2022): ~10% higher than Aave"""
    return aave_apy * 1.1

def get_sky_apy(aave_apy: float) -> float:
    """Sky SSR proxy (pre-Oct 2022): ~10% lower than Aave"""
    return aave_apy * 0.9
```

## 2.4 JLP Return Calculation

```python
def calculate_jlp_daily_return(
    sol_return: float,
    eth_return: float,
    btc_return: float,
    jlp_apy: float
) -> float:
    """
    JLP return = weighted basket price change + daily fee income
    
    Basket weights: 45% SOL, 27% ETH, 27% BTC
    """
    price_return = (
        0.45 * sol_return +
        0.27 * eth_return +
        0.27 * btc_return
    )
    fee_return = jlp_apy / 365 / 100  # Daily APY as decimal
    return price_return + fee_return
```

---

# 3. DATA COLLECTION MODULE

## 3.1 Abstract Interface

```python
# src/collectors/base.py

from abc import ABC, abstractmethod
from datetime import date
import pandas as pd

class DataProvider(ABC):
    """Abstract base class for all data providers."""
    
    @abstractmethod
    def fetch_historical(
        self, 
        start_date: date, 
        end_date: date
    ) -> pd.DataFrame:
        """Fetch historical data for the given period."""
        pass
    
    @abstractmethod
    def fetch_current(self) -> dict:
        """Fetch current/live data."""
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """Validate data quality."""
        pass
```

## 3.2 DeFiLlama Collector

```python
# src/collectors/defillama.py

import requests
import pandas as pd
from .base import DataProvider

class DeFiLlamaProvider(DataProvider):
    """
    Fetch APY data from DeFiLlama API.
    
    Endpoint: https://yields.llama.fi/pools
    """
    
    BASE_URL = "https://yields.llama.fi"
    
    def __init__(self, projects: list[str], chain: str = None):
        self.projects = projects
        self.chain = chain
    
    def fetch_historical(self, start_date, end_date) -> pd.DataFrame:
        """
        DeFiLlama doesn't have a historical endpoint.
        Use bundled CSV for historical data.
        This method fetches current snapshot only.
        """
        response = requests.get(f"{self.BASE_URL}/pools")
        response.raise_for_status()
        
        pools = response.json()['data']
        
        # Filter to relevant pools
        filtered = [
            p for p in pools
            if p.get('project') in self.projects
            and (self.chain is None or p.get('chain') == self.chain)
        ]
        
        return pd.DataFrame(filtered)
    
    def fetch_current(self) -> dict:
        """Fetch current APY for monitored protocols."""
        df = self.fetch_historical(None, None)
        return df.to_dict('records')
    
    def validate(self, data: pd.DataFrame) -> bool:
        required_cols = ['project', 'chain', 'symbol', 'apy', 'tvlUsd']
        return all(col in data.columns for col in required_cols)
```

## 3.3 Yahoo Finance Collector

```python
# src/collectors/yahoo.py

import requests
import pandas as pd
from datetime import datetime, timedelta
from .base import DataProvider

class YahooFinanceProvider(DataProvider):
    """
    Fetch crypto price data from Yahoo Finance.
    
    Symbols: BTC-USD, ETH-USD, SOL-USD
    """
    
    SYMBOLS = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD',
        'SOL': 'SOL-USD'
    }
    
    def fetch_historical(self, start_date, end_date) -> pd.DataFrame:
        """Fetch OHLCV data for all crypto assets."""
        all_data = []
        
        for asset, symbol in self.SYMBOLS.items():
            # Yahoo Finance API (or use yfinance library)
            # Implementation depends on chosen approach
            pass
        
        return pd.concat(all_data, ignore_index=True)
    
    def fetch_current(self) -> dict:
        """Fetch current prices."""
        # Implementation
        pass
    
    def validate(self, data: pd.DataFrame) -> bool:
        required_cols = ['date', 'symbol', 'close']
        return all(col in data.columns for col in required_cols)
```

## 3.4 File Loader (Bundled Data)

```python
# src/collectors/file_loader.py

import pandas as pd
from pathlib import Path

class FileLoader:
    """Load bundled historical data from CSV files."""
    
    DATA_DIR = Path(__file__).parent.parent.parent / 'data'
    
    FILES = {
        'defillama': 'defillama_historical_apy.csv',
        'yahoo': 'yahoo_historical_prices.csv',
        'jupiter': 'jupiter_jlp_historical_apy.csv',
        'perps': 'perps_lp_combined_apy.csv'
    }
    
    @classmethod
    def load(cls, source: str) -> pd.DataFrame:
        """Load data from bundled CSV file."""
        filepath = cls.DATA_DIR / cls.FILES[source]
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        df = pd.read_csv(filepath, parse_dates=['date'])
        return df
    
    @classmethod
    def load_all(cls) -> dict[str, pd.DataFrame]:
        """Load all bundled data files."""
        return {
            name: cls.load(name)
            for name in cls.FILES.keys()
        }
```

---

# 4. BATTLE TEST MODULE

## 4.1 Core Algorithm

```python
# src/engines/battle_test.py

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional
from datetime import date

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
    
class BattleTestEngine:
    """
    Historical backtesting engine.
    
    Simulates DCA investing through historical market conditions.
    """
    
    def __init__(
        self,
        strategies: list[dict],
        apy_data: pd.DataFrame,
        price_data: pd.DataFrame,
        jlp_data: pd.DataFrame
    ):
        self.strategies = strategies
        self.apy_data = apy_data
        self.price_data = price_data
        self.jlp_data = jlp_data
    
    def run(
        self,
        strategy_id: int,
        initial_deposit: float,
        monthly_dca: float,
        start_date: date,
        end_date: date
    ) -> BattleTestResult:
        """
        Run battle test for a single strategy.
        """
        strategy = next(s for s in self.strategies if s['id'] == strategy_id)
        
        # Get date range
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Initialize tracking
        portfolio_value = initial_deposit
        peak_value = initial_deposit
        max_drawdown = 0.0
        total_deposited = initial_deposit
        last_dca_month = start_date.month
        
        # Daily simulation
        for current_date in dates[1:]:
            # Monthly DCA
            if current_date.month != last_dca_month:
                portfolio_value += monthly_dca
                total_deposited += monthly_dca
                last_dca_month = current_date.month
            
            # Calculate daily return
            daily_return = self._calculate_daily_return(
                strategy, current_date
            )
            
            # Apply return
            portfolio_value *= (1 + daily_return)
            
            # Track drawdown
            if portfolio_value > peak_value:
                peak_value = portfolio_value
            
            drawdown = (peak_value - portfolio_value) / peak_value
            max_drawdown = max(max_drawdown, drawdown)
        
        return BattleTestResult(
            strategy_id=strategy_id,
            strategy_name=strategy['name'],
            scenario=f"${initial_deposit:,.0f} + ${monthly_dca}/mo",
            period_start=start_date,
            period_end=end_date,
            days=len(dates),
            deposited=total_deposited,
            final_value=portfolio_value,
            profit=portfolio_value - total_deposited,
            return_pct=(portfolio_value - total_deposited) / total_deposited * 100,
            max_drawdown_pct=max_drawdown * 100
        )
    
    def _calculate_daily_return(
        self, 
        strategy: dict, 
        current_date: date
    ) -> float:
        """
        Calculate weighted daily return based on strategy allocations.
        """
        total_return = 0.0
        
        # Stable allocations
        for protocol, weight in strategy['allocations']['stable'].items():
            apy = self._get_protocol_apy(protocol, current_date)
            daily_return = apy / 365 / 100
            total_return += weight * daily_return
        
        # Crypto allocations
        for protocol, weight in strategy['allocations']['crypto'].items():
            if protocol == 'jlp':
                # JLP = basket return + fee APY
                daily_return = self._get_jlp_return(current_date)
            else:
                # Sanctum/Jito = SOL return + staking APY
                sol_return = self._get_price_return('SOL', current_date)
                staking_apy = self._get_protocol_apy(protocol, current_date)
                daily_return = sol_return + (staking_apy / 365 / 100)
            
            total_return += weight * daily_return
        
        return total_return
    
    def _get_protocol_apy(self, protocol: str, current_date: date) -> float:
        """Get APY for protocol on given date, with proxy fallback."""
        # Implementation with proxy logic
        pass
    
    def _get_price_return(self, symbol: str, current_date: date) -> float:
        """Get daily price return for crypto asset."""
        # Implementation
        pass
    
    def _get_jlp_return(self, current_date: date) -> float:
        """Get JLP daily return (basket + fees)."""
        sol_return = self._get_price_return('SOL', current_date)
        eth_return = self._get_price_return('ETH', current_date)
        btc_return = self._get_price_return('BTC', current_date)
        
        jlp_apy = self._get_protocol_apy('jlp', current_date)
        
        basket_return = (
            0.45 * sol_return +
            0.27 * eth_return +
            0.27 * btc_return
        )
        fee_return = jlp_apy / 365 / 100
        
        return basket_return + fee_return
```

## 4.2 Test Scenarios

```python
SCENARIOS = {
    'A': {
        'name': 'Felipe (Sophisticated)',
        'initial_deposit': 10000,
        'monthly_dca': 200
    },
    'B': {
        'name': 'Ana (Minimum)',
        'initial_deposit': 5,
        'monthly_dca': 5
    },
    'C': {
        'name': 'Per-Strategy Minimum',
        'minimums': {
            1: {'initial': 50, 'monthly': 10},
            2: {'initial': 20, 'monthly': 5},
            3: {'initial': 50, 'monthly': 10},
            4: {'initial': 20, 'monthly': 5},
            5: {'initial': 50, 'monthly': 10},
            6: {'initial': 30, 'monthly': 5},
            7: {'initial': 50, 'monthly': 10},
            8: {'initial': 100, 'monthly': 20},
            9: {'initial': 50, 'monthly': 10},
            10: {'initial': 200, 'monthly': 40}
        }
    }
}
```

---

# 5. MONTE CARLO MODULE

## 5.1 Core Algorithm

```python
# src/engines/monte_carlo.py

import numpy as np
import pandas as pd
from dataclasses import dataclass
from scipy import stats

@dataclass
class MonteCarloResult:
    strategy_id: int
    strategy_name: str
    simulations: int
    horizon_months: int
    total_deposited: float
    
    # Distribution metrics
    mean_final: float
    median_final: float
    std_final: float
    
    # Return metrics
    mean_return: float
    median_return: float
    
    # Risk metrics
    prob_any_loss: float
    prob_loss_10pct: float
    prob_loss_20pct: float
    prob_loss_50pct: float
    
    var_95: float
    cvar_95: float
    var_99: float
    cvar_99: float
    
    # Percentiles
    p5_final: float
    p95_final: float
    
    # Drawdown
    mean_max_drawdown: float
    p95_max_drawdown: float

class MonteCarloEngine:
    """
    Monte Carlo simulation engine with regime switching.
    
    Methodology:
    - 5,000+ simulations per strategy
    - Block bootstrap (21-day blocks)
    - 4 regimes: Bull, Bear, Crash, Recovery
    - Fat-tailed distributions (Student-t, df=4)
    """
    
    REGIMES = {
        'bull': {'mean_mult': 1.5, 'vol_mult': 0.8, 'duration': 180},
        'bear': {'mean_mult': 0.3, 'vol_mult': 1.5, 'duration': 120},
        'crash': {'mean_mult': -2.0, 'vol_mult': 3.0, 'duration': 30},
        'recovery': {'mean_mult': 2.0, 'vol_mult': 1.2, 'duration': 90}
    }
    
    # Markov transition matrix
    TRANSITIONS = {
        'bull': {'bull': 0.85, 'bear': 0.10, 'crash': 0.03, 'recovery': 0.02},
        'bear': {'bull': 0.05, 'bear': 0.80, 'crash': 0.10, 'recovery': 0.05},
        'crash': {'bull': 0.00, 'bear': 0.20, 'crash': 0.30, 'recovery': 0.50},
        'recovery': {'bull': 0.40, 'bear': 0.10, 'crash': 0.05, 'recovery': 0.45}
    }
    
    def __init__(
        self,
        strategies: list[dict],
        historical_returns: pd.DataFrame,
        n_simulations: int = 5000,
        horizon_months: int = 48,
        random_seed: int = 42
    ):
        self.strategies = strategies
        self.historical_returns = historical_returns
        self.n_simulations = n_simulations
        self.horizon_months = horizon_months
        np.random.seed(random_seed)
    
    def run(
        self,
        strategy_id: int,
        initial_deposit: float = 10000,
        monthly_dca: float = 200
    ) -> MonteCarloResult:
        """Run Monte Carlo simulation for a single strategy."""
        
        strategy = next(s for s in self.strategies if s['id'] == strategy_id)
        
        # Calculate total deposits
        total_deposited = initial_deposit + (monthly_dca * self.horizon_months)
        
        # Generate simulated paths
        final_values = []
        max_drawdowns = []
        
        for _ in range(self.n_simulations):
            path = self._simulate_path(
                strategy, initial_deposit, monthly_dca
            )
            final_values.append(path[-1])
            max_drawdowns.append(self._calculate_max_drawdown(path))
        
        final_values = np.array(final_values)
        max_drawdowns = np.array(max_drawdowns)
        
        # Calculate metrics
        returns = (final_values - total_deposited) / total_deposited
        
        return MonteCarloResult(
            strategy_id=strategy_id,
            strategy_name=strategy['name'],
            simulations=self.n_simulations,
            horizon_months=self.horizon_months,
            total_deposited=total_deposited,
            
            mean_final=np.mean(final_values),
            median_final=np.median(final_values),
            std_final=np.std(final_values),
            
            mean_return=np.mean(returns) * 100,
            median_return=np.median(returns) * 100,
            
            prob_any_loss=np.mean(final_values < total_deposited) * 100,
            prob_loss_10pct=np.mean(returns < -0.10) * 100,
            prob_loss_20pct=np.mean(returns < -0.20) * 100,
            prob_loss_50pct=np.mean(returns < -0.50) * 100,
            
            var_95=np.percentile(final_values, 5),
            cvar_95=np.mean(final_values[final_values <= np.percentile(final_values, 5)]),
            var_99=np.percentile(final_values, 1),
            cvar_99=np.mean(final_values[final_values <= np.percentile(final_values, 1)]),
            
            p5_final=np.percentile(final_values, 5),
            p95_final=np.percentile(final_values, 95),
            
            mean_max_drawdown=np.mean(max_drawdowns) * 100,
            p95_max_drawdown=np.percentile(max_drawdowns, 95) * 100
        )
    
    def _simulate_path(
        self,
        strategy: dict,
        initial_deposit: float,
        monthly_dca: float
    ) -> np.ndarray:
        """Simulate a single price path with regime switching."""
        
        days = self.horizon_months * 21  # Trading days
        values = np.zeros(days)
        values[0] = initial_deposit
        
        current_regime = 'bull'
        regime_day = 0
        
        for day in range(1, days):
            # Monthly DCA
            if day % 21 == 0:
                values[day-1] += monthly_dca
            
            # Regime transition
            regime_day += 1
            if regime_day >= self.REGIMES[current_regime]['duration']:
                current_regime = self._transition_regime(current_regime)
                regime_day = 0
            
            # Generate daily return
            daily_return = self._generate_return(strategy, current_regime)
            values[day] = values[day-1] * (1 + daily_return)
        
        return values
    
    def _generate_return(self, strategy: dict, regime: str) -> float:
        """Generate daily return with fat tails."""
        
        # Base parameters (from historical data)
        base_mean = 0.0003  # ~10% annual
        base_std = 0.02     # ~30% annual vol
        
        # Adjust for regime
        regime_params = self.REGIMES[regime]
        mean = base_mean * regime_params['mean_mult']
        std = base_std * regime_params['vol_mult']
        
        # Adjust for crypto exposure
        crypto_pct = strategy['crypto_pct'] / 100
        std = std * (1 + crypto_pct * 2)  # Higher vol for crypto
        
        # Fat-tailed distribution
        return stats.t.rvs(df=4, loc=mean, scale=std)
    
    def _transition_regime(self, current: str) -> str:
        """Transition to new regime based on Markov matrix."""
        probs = self.TRANSITIONS[current]
        regimes = list(probs.keys())
        weights = list(probs.values())
        return np.random.choice(regimes, p=weights)
    
    def _calculate_max_drawdown(self, path: np.ndarray) -> float:
        """Calculate maximum drawdown from price path."""
        peak = np.maximum.accumulate(path)
        drawdown = (peak - path) / peak
        return np.max(drawdown)
```

---

# 6. PROTOCOL MONITORING MODULE

## 6.1 Health Check Engine

```python
# src/engines/monitoring.py

from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

class AlertSeverity(Enum):
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'
    EMERGENCY = 'emergency'

@dataclass
class ProtocolHealth:
    protocol: str
    timestamp: datetime
    
    # Metrics
    tvl: float
    tvl_change_24h: float
    apy: float
    apy_change_24h: float
    utilization: Optional[float]
    
    # Status
    is_healthy: bool
    alerts: list['Alert']

@dataclass
class Alert:
    protocol: str
    severity: AlertSeverity
    metric: str
    message: str
    value: float
    threshold: float
    timestamp: datetime

class MonitoringEngine:
    """Protocol health monitoring with alerting."""
    
    THRESHOLDS = {
        'tvl_drop_warning': -0.15,      # -15% TVL drop
        'tvl_drop_critical': -0.30,     # -30% TVL drop
        'utilization_warning': 0.85,     # 85% utilization
        'utilization_critical': 0.95,    # 95% utilization
        'apy_deviation_warning': 0.50,   # 50% APY change
        'apy_deviation_critical': 1.00,  # 100% APY change
    }
    
    def check_protocol(self, protocol: str, current: dict, previous: dict) -> ProtocolHealth:
        """Check health of a single protocol."""
        
        alerts = []
        
        # TVL check
        tvl_change = (current['tvl'] - previous['tvl']) / previous['tvl']
        if tvl_change < self.THRESHOLDS['tvl_drop_critical']:
            alerts.append(Alert(
                protocol=protocol,
                severity=AlertSeverity.CRITICAL,
                metric='tvl_change_24h',
                message=f"TVL dropped {tvl_change*100:.1f}% in 24h",
                value=tvl_change,
                threshold=self.THRESHOLDS['tvl_drop_critical'],
                timestamp=datetime.utcnow()
            ))
        elif tvl_change < self.THRESHOLDS['tvl_drop_warning']:
            alerts.append(Alert(
                protocol=protocol,
                severity=AlertSeverity.WARNING,
                metric='tvl_change_24h',
                message=f"TVL dropped {tvl_change*100:.1f}% in 24h",
                value=tvl_change,
                threshold=self.THRESHOLDS['tvl_drop_warning'],
                timestamp=datetime.utcnow()
            ))
        
        # Utilization check (if applicable)
        if current.get('utilization'):
            if current['utilization'] > self.THRESHOLDS['utilization_critical']:
                alerts.append(Alert(
                    protocol=protocol,
                    severity=AlertSeverity.CRITICAL,
                    metric='utilization',
                    message=f"Utilization at {current['utilization']*100:.1f}%",
                    value=current['utilization'],
                    threshold=self.THRESHOLDS['utilization_critical'],
                    timestamp=datetime.utcnow()
                ))
        
        return ProtocolHealth(
            protocol=protocol,
            timestamp=datetime.utcnow(),
            tvl=current['tvl'],
            tvl_change_24h=tvl_change,
            apy=current['apy'],
            apy_change_24h=(current['apy'] - previous['apy']) / previous['apy'],
            utilization=current.get('utilization'),
            is_healthy=len([a for a in alerts if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]]) == 0,
            alerts=alerts
        )
```

---

# 7. ANOMALY DETECTION MODULE

## 7.1 Z-Score Detector

```python
# src/models/zscore.py

import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class AnomalyResult:
    protocol: str
    metric: str
    value: float
    z_score: float
    is_anomaly: bool
    threshold: float

class ZScoreDetector:
    """
    Statistical anomaly detection using Z-scores.
    
    Flags values that deviate significantly from rolling mean.
    """
    
    def __init__(self, window: int = 30, threshold: float = 3.0):
        self.window = window
        self.threshold = threshold
    
    def detect(self, series: pd.Series) -> list[AnomalyResult]:
        """Detect anomalies in time series."""
        
        rolling_mean = series.rolling(window=self.window).mean()
        rolling_std = series.rolling(window=self.window).std()
        
        z_scores = (series - rolling_mean) / rolling_std
        
        anomalies = []
        for idx, (value, z) in enumerate(zip(series, z_scores)):
            if pd.notna(z) and abs(z) > self.threshold:
                anomalies.append(AnomalyResult(
                    protocol='',  # Set by caller
                    metric=series.name,
                    value=value,
                    z_score=z,
                    is_anomaly=True,
                    threshold=self.threshold
                ))
        
        return anomalies
```

## 7.2 Isolation Forest

```python
# src/models/isolation_forest.py

from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

class IsolationForestDetector:
    """
    ML-based anomaly detection using Isolation Forest.
    
    Detects unusual transactions and behavior patterns.
    """
    
    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_fitted = False
    
    def fit(self, data: pd.DataFrame):
        """Fit model on historical data."""
        self.model.fit(data)
        self.is_fitted = True
    
    def detect(self, data: pd.DataFrame) -> np.ndarray:
        """
        Detect anomalies.
        
        Returns: -1 for anomalies, 1 for normal
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before detection")
        
        return self.model.predict(data)
    
    def score(self, data: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores.
        
        Lower (more negative) = more anomalous
        """
        return self.model.decision_function(data)
```

---

# 8. VALIDATION RULES

## 8.1 Validation Rule Definitions

```python
# src/validators/result_validator.py

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Severity(Enum):
    CRITICAL = 'critical'
    WARNING = 'warning'
    INFO = 'info'

@dataclass
class ValidationResult:
    rule_id: str
    passed: bool
    severity: Severity
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None

class ResultValidator:
    """
    Validate Battle Test and Monte Carlo results.
    
    Rules CV-01 through CV-07.
    """
    
    GAS_COSTS = {
        'arbitrum': 0.30,
        'solana': 0.005
    }
    
    MINIMUM_DEPOSITS = {
        1: 50, 2: 20, 3: 50, 4: 20, 5: 50,
        6: 30, 7: 50, 8: 100, 9: 50, 10: 200
    }
    
    def validate_cv01(self, portfolio_values: list[float]) -> ValidationResult:
        """CV-01: Portfolio value never negative."""
        min_value = min(portfolio_values)
        passed = min_value >= 0
        
        return ValidationResult(
            rule_id='CV-01',
            passed=passed,
            severity=Severity.CRITICAL,
            message='Portfolio value went negative' if not passed else 'OK',
            value=min_value,
            threshold=0
        )
    
    def validate_cv02(self, max_drawdown: float) -> ValidationResult:
        """CV-02: Drawdown between 0% and 100%."""
        passed = 0 <= max_drawdown <= 100
        
        return ValidationResult(
            rule_id='CV-02',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Invalid drawdown: {max_drawdown}%' if not passed else 'OK',
            value=max_drawdown,
            threshold=100
        )
    
    def validate_cv03(self, strategy_id: int, max_drawdown: float) -> ValidationResult:
        """CV-03: Stable strategies (0% crypto) have 0% max drawdown."""
        stable_strategies = [1, 3, 5, 7, 9]
        
        if strategy_id not in stable_strategies:
            return ValidationResult(
                rule_id='CV-03',
                passed=True,
                severity=Severity.INFO,
                message='Not a stable strategy, rule not applicable'
            )
        
        passed = max_drawdown == 0
        
        return ValidationResult(
            rule_id='CV-03',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Stable strategy has {max_drawdown}% drawdown' if not passed else 'OK',
            value=max_drawdown,
            threshold=0
        )
    
    def validate_cv04(
        self, 
        strategy_id: int, 
        deposited: float, 
        final_value: float
    ) -> ValidationResult:
        """CV-04: Final value >= deposited for stable strategies."""
        stable_strategies = [1, 3, 5, 7, 9]
        
        if strategy_id not in stable_strategies:
            return ValidationResult(
                rule_id='CV-04',
                passed=True,
                severity=Severity.INFO,
                message='Not a stable strategy, rule not applicable'
            )
        
        passed = final_value >= deposited
        
        return ValidationResult(
            rule_id='CV-04',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Stable strategy lost money' if not passed else 'OK',
            value=final_value,
            threshold=deposited
        )
    
    def validate_cv05(
        self, 
        deposited: float, 
        final_value: float, 
        reported_return: float
    ) -> ValidationResult:
        """CV-05: Return % matches calculation."""
        calculated_return = (final_value - deposited) / deposited * 100
        diff = abs(calculated_return - reported_return)
        passed = diff < 0.01  # 0.01% tolerance
        
        return ValidationResult(
            rule_id='CV-05',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Return mismatch: {calculated_return:.2f}% vs {reported_return:.2f}%' if not passed else 'OK',
            value=diff,
            threshold=0.01
        )
    
    def validate_cv06(
        self,
        gross_return: float,
        tx_count: int,
        chain: str
    ) -> ValidationResult:
        """CV-06: Net return > 0 after gas costs."""
        gas_per_tx = self.GAS_COSTS.get(chain, 0.30)
        total_gas = tx_count * gas_per_tx
        net_return = gross_return - total_gas
        passed = net_return > 0
        
        return ValidationResult(
            rule_id='CV-06',
            passed=passed,
            severity=Severity.CRITICAL,
            message=f'Negative net return after ${total_gas:.2f} gas' if not passed else 'OK',
            value=net_return,
            threshold=0
        )
    
    def validate_cv07(
        self,
        strategy_id: int,
        initial_deposit: float
    ) -> ValidationResult:
        """CV-07: Initial deposit >= per-strategy minimum."""
        min_required = self.MINIMUM_DEPOSITS[strategy_id]
        passed = initial_deposit >= min_required
        
        return ValidationResult(
            rule_id='CV-07',
            passed=passed,
            severity=Severity.WARNING,
            message=f'Deposit ${initial_deposit} below minimum ${min_required}' if not passed else 'OK',
            value=initial_deposit,
            threshold=min_required
        )
```

---

# 9. CLI INTERFACE

## 9.1 Main Entry Point

```python
# main.py

import argparse
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description='diBoaS Analytics - Investment Strategy Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py collect --all           Fetch all data from APIs
  python main.py collect --offline       Use bundled data only
  python main.py battle-test             Run full battle test
  python main.py battle-test --strategy 1  Test only Safe Harbor
  python main.py monte-carlo             Run Monte Carlo simulation
  python main.py monitor                 Check protocol health
  python main.py anomaly                 Run anomaly detection
  python main.py dream-mode-export       Generate Dream Mode data (NEW)
  python main.py all                     Run full pipeline
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect data from APIs')
    collect_parser.add_argument('--all', action='store_true', help='Fetch from all sources')
    collect_parser.add_argument('--offline', action='store_true', help='Use bundled data only')
    collect_parser.add_argument('--source', choices=['defillama', 'yahoo', 'jupiter'], help='Specific source')
    
    # Battle Test command
    bt_parser = subparsers.add_parser('battle-test', help='Run historical backtesting')
    bt_parser.add_argument('--strategy', type=int, help='Specific strategy ID (1-10)')
    bt_parser.add_argument('--scenario', choices=['A', 'B', 'C'], help='Test scenario')
    bt_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    bt_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    
    # Monte Carlo command
    mc_parser = subparsers.add_parser('monte-carlo', help='Run Monte Carlo simulation')
    mc_parser.add_argument('--strategy', type=int, help='Specific strategy ID (1-10)')
    mc_parser.add_argument('--simulations', type=int, default=5000, help='Number of simulations')
    mc_parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    # Monitor command
    mon_parser = subparsers.add_parser('monitor', help='Check protocol health')
    mon_parser.add_argument('--protocol', help='Specific protocol')
    mon_parser.add_argument('--alerts-only', action='store_true', help='Show only active alerts')
    
    # Anomaly command
    anom_parser = subparsers.add_parser('anomaly', help='Run anomaly detection')
    anom_parser.add_argument('--model', choices=['zscore', 'isolation', 'correlation'], help='Specific model')
    anom_parser.add_argument('--protocol', help='Specific protocol')
    
    # Dream Mode Export command (NEW)
    dm_parser = subparsers.add_parser('dream-mode-export', help='Generate Dream Mode data for frontend')
    dm_parser.add_argument('--output', default='./outputs/dream_mode_data.json', help='Output file path')
    
    # All command
    all_parser = subparsers.add_parser('all', help='Run full pipeline')
    all_parser.add_argument('--offline', action='store_true', help='Use bundled data')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate summary report')
    report_parser.add_argument('--format', choices=['csv', 'json', 'markdown'], default='markdown')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Route to appropriate handler
    if args.command == 'collect':
        from src.commands.collect import run_collect
        run_collect(args)
    elif args.command == 'battle-test':
        from src.commands.battle_test import run_battle_test
        run_battle_test(args)
    elif args.command == 'monte-carlo':
        from src.commands.monte_carlo import run_monte_carlo
        run_monte_carlo(args)
    elif args.command == 'monitor':
        from src.commands.monitor import run_monitor
        run_monitor(args)
    elif args.command == 'anomaly':
        from src.commands.anomaly import run_anomaly
        run_anomaly(args)
    elif args.command == 'dream-mode-export':
        from src.commands.dream_mode_export import run_dream_mode_export
        run_dream_mode_export(args)
    elif args.command == 'all':
        from src.commands.full_pipeline import run_all
        run_all(args)
    elif args.command == 'report':
        from src.commands.report import run_report
        run_report(args)

if __name__ == '__main__':
    main()
```

---

# 10. CONFIGURATION FILES

## 10.1 Requirements

```
# requirements.txt

# Core
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0

# API clients
requests>=2.28.0
yfinance>=0.2.0

# ML
scikit-learn>=1.3.0
statsmodels>=0.14.0

# Database
sqlalchemy>=2.0.0

# CLI
python-dotenv>=1.0.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0

# Development
black>=23.0.0
ruff>=0.1.0
mypy>=1.0.0
```

## 10.2 Environment Variables

```bash
# .env.example

# API Keys (optional - for live data)
DEFILLAMA_API_KEY=
YAHOO_API_KEY=

# Notifications
SLACK_WEBHOOK_URL=
PAGERDUTY_API_KEY=

# Settings
LOG_LEVEL=INFO
OUTPUT_DIR=./outputs
DATA_DIR=./data
```

## 10.3 Settings

```python
# config/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', BASE_DIR / 'outputs'))
STORAGE_DIR = BASE_DIR / 'storage'

# Simulation defaults
DEFAULT_SIMULATIONS = 5000
DEFAULT_HORIZON_MONTHS = 48
DEFAULT_START_DATE = '2022-05-01'
DEFAULT_END_DATE = '2025-12-31'

# Validation
VALIDATION_TOLERANCE = 0.01  # 0.01% for return matching

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Dream Mode
BANK_COMPARISON_APY = 0.5  # 0.5% EU average
BANK_COMPARISON_SOURCE = "ECB Statistics, December 2024"
```

---

# 11. TESTING REQUIREMENTS

## 11.1 Unit Tests

```python
# tests/test_battle_test.py

import pytest
from src.engines.battle_test import BattleTestEngine

class TestBattleTest:
    
    def test_stable_strategy_zero_drawdown(self):
        """Stable strategies (0% crypto) should have 0% drawdown."""
        # Test implementation
        pass
    
    def test_dca_contribution(self):
        """Monthly DCA should be added correctly."""
        pass
    
    def test_return_calculation(self):
        """Return % should match deposited vs final value."""
        pass


# tests/test_validators.py

import pytest
from src.validators.result_validator import ResultValidator

class TestValidators:
    
    def test_cv01_negative_portfolio(self):
        """CV-01 should fail on negative portfolio value."""
        validator = ResultValidator()
        result = validator.validate_cv01([-100, 50, 100])
        assert not result.passed
        assert result.severity.value == 'critical'
    
    def test_cv03_stable_with_drawdown(self):
        """CV-03 should warn if stable strategy has drawdown."""
        validator = ResultValidator()
        result = validator.validate_cv03(strategy_id=1, max_drawdown=5.0)
        assert not result.passed
    
    def test_cv07_minimum_deposit(self):
        """CV-07 should warn if deposit below minimum."""
        validator = ResultValidator()
        result = validator.validate_cv07(strategy_id=10, initial_deposit=50)
        assert not result.passed  # Full Throttle requires $200
```

---

# 12. DATA FILES

The following CSV files should be placed in the `data/` directory:

| File | Description | Source |
|------|-------------|--------|
| `defillama_historical_apy.csv` | Historical APY data (47,496 rows) | DeFiLlama |
| `yahoo_historical_prices.csv` | BTC/ETH/SOL prices (4,380 rows) | Yahoo Finance |
| `jupiter_jlp_historical_apy.csv` | JLP APY data (697 rows) | Jupiter |
| `perps_lp_combined_apy.csv` | Perps LP data | Various |

**Schema for `defillama_historical_apy.csv`:**
```
date,project,chain,symbol,tvlUsd,apy,apyBase,apyReward
2022-05-01,aave-v3,arbitrum,USDC,1500000000,4.5,3.2,1.3
```

**Schema for `yahoo_historical_prices.csv`:**
```
date,symbol,open,high,low,close,volume
2022-05-01,BTC,38000,39000,37500,38500,12345678
2022-05-01,ETH,2800,2900,2750,2850,23456789
2022-05-01,SOL,95,98,92,96,34567890
```

---

# 13. DREAM MODE EXPORT MODULE (NEW)

## 13.1 Purpose

Dream Mode is a pre-launch feature that lets waitlist users simulate what their money could become. The analytics application must export consumer-ready data for the frontend.

## 13.2 Configuration

```python
# config/dream_mode.py

"""
Dream Mode configuration.

Maps the 10 internal strategies to 3 simplified consumer paths.
"""

# Path definitions for Dream Mode UI
DREAM_MODE_PATHS = {
    'safety': {
        'strategies': [1, 3, 5, 7, 9],  # All 0% crypto strategies
        'label': 'Safety First',
        'description': 'Stable yield, no crypto exposure',
        'color': '#2563EB',  # Blue
        'risk_level': 'Minimal'
    },
    'balance': {
        'strategies': [2, 4, 6],  # 30-40% crypto strategies
        'label': 'Balanced Growth',
        'description': 'Moderate crypto exposure (30-40%)',
        'color': '#7C3AED',  # Purple
        'risk_level': 'Low-Medium'
    },
    'growth': {
        'strategies': [8, 10],  # 70-85% crypto strategies
        'label': 'Maximum Growth',
        'description': 'High crypto exposure (70-85%)',
        'color': '#DC2626',  # Red
        'risk_level': 'High'
    }
}

# Bank comparison baseline (CLO-approved)
BANK_COMPARISON = {
    'apy': 0.5,  # 0.5% APY
    'source': 'ECB Statistics',
    'date': 'December 2024',
    'note': 'Average EU savings account rate. Rates may vary.'
}

# CLO-mandated disclaimers
DISCLAIMERS = {
    'simulation': "This is a simulation based on historical data from May 2022 to December 2025. Past performance does not guarantee future returns.",
    'risk': "Capital is at risk. Actual results may differ significantly.",
    'not_advice': "This is for educational purposes only and does not constitute investment advice.",
    'card_watermark': "⚠️ SIMULATION — Based on historical data. Not a guarantee. diboas.com",
    'bank_comparison': f"Bank comparison based on average EU savings account rate of 0.5% APY. Source: ECB Statistics, December 2024. Rates may vary."
}

# Enhanced disclaimers for specific regions
REGIONAL_DISCLAIMERS = {
    'pt-BR': "⚠️ SIMULAÇÃO EDUCACIONAL — Este recurso utiliza dados históricos apenas para fins ilustrativos. Não constitui oferta de investimento, promessa de retorno ou aconselhamento financeiro. Resultados reais podem diferir significativamente.",
    'en-US': "⚠️ EDUCATIONAL SIMULATION — This feature uses historical data for illustrative purposes only. It does not constitute an offer of investment, promise of returns, or financial advice. Actual results may differ significantly."
}
```

## 13.3 Domain Model

```python
# src/domain/dream_mode.py

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class PathProjection:
    """Projection for a specific time period."""
    period: str  # '1_week', '1_month', '1_year', '5_years'
    multiplier: float  # e.g., 1.095 for +9.5%
    bank_multiplier: float  # e.g., 1.005 for +0.5%
    
@dataclass
class PathMetrics:
    """Aggregated metrics for a Dream Mode path."""
    path_id: str  # 'safety', 'balance', 'growth'
    label: str
    description: str
    color: str
    risk_level: str
    
    # Aggregated from underlying strategies
    avg_apy: float
    max_drawdown: float
    probability_of_loss: float
    
    # Pre-calculated projections
    projections: Dict[str, PathProjection]
    
    # Warning for high-risk paths
    warning: Optional[str] = None

@dataclass
class DreamModeData:
    """Complete export for Dream Mode frontend."""
    version: str
    generated_at: datetime
    
    # Data sources for CLO compliance
    data_sources: Dict[str, dict]
    
    # The 3 paths
    paths: Dict[str, PathMetrics]
    
    # Bank comparison
    bank_comparison: dict
    
    # CLO-mandated disclaimers
    disclaimers: dict
    regional_disclaimers: dict
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            'version': self.version,
            'generated_at': self.generated_at.isoformat(),
            'data_sources': self.data_sources,
            'paths': {k: asdict(v) for k, v in self.paths.items()},
            'bank_comparison': self.bank_comparison,
            'disclaimers': self.disclaimers,
            'regional_disclaimers': self.regional_disclaimers
        }
```

## 13.4 Export Engine

```python
# src/engines/dream_mode_export.py

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from config.dream_mode import DREAM_MODE_PATHS, BANK_COMPARISON, DISCLAIMERS, REGIONAL_DISCLAIMERS
from src.domain.dream_mode import DreamModeData, PathMetrics, PathProjection

class DreamModeExporter:
    """
    Generate consumer-ready Dream Mode data from Battle Test and Monte Carlo results.
    
    This bridges internal analytics to the frontend feature.
    """
    
    def __init__(
        self,
        battle_test_results: List[dict],
        monte_carlo_results: List[dict],
        strategies: List[dict]
    ):
        self.battle_test_results = battle_test_results
        self.monte_carlo_results = monte_carlo_results
        self.strategies = strategies
    
    def export(self, output_path: str = './outputs/dream_mode_data.json') -> DreamModeData:
        """Generate and save Dream Mode data."""
        
        # Build data sources metadata
        data_sources = self._build_data_sources()
        
        # Aggregate metrics for each path
        paths = {}
        for path_id, path_config in DREAM_MODE_PATHS.items():
            paths[path_id] = self._aggregate_path_metrics(path_id, path_config)
        
        # Build complete export
        dream_mode_data = DreamModeData(
            version='1.0',
            generated_at=datetime.utcnow(),
            data_sources=data_sources,
            paths=paths,
            bank_comparison=BANK_COMPARISON,
            disclaimers=DISCLAIMERS,
            regional_disclaimers=REGIONAL_DISCLAIMERS
        )
        
        # Save to file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(dream_mode_data.to_dict(), f, indent=2)
        
        return dream_mode_data
    
    def _build_data_sources(self) -> dict:
        """Build data sources metadata for CLO compliance."""
        return {
            'apy_data': {
                'source': 'DeFiLlama',
                'period': '2022-05-01 to 2025-12-31',
                'last_updated': datetime.utcnow().strftime('%Y-%m-%d')
            },
            'price_data': {
                'source': 'Yahoo Finance',
                'period': '2022-05-01 to 2025-12-31'
            },
            'battle_test': {
                'methodology': 'Historical backtesting with DCA',
                'period': '1,334 days (May 2022 - Dec 2025)',
                'events_captured': ['Terra/Luna collapse', 'FTX crash', 'USDC depeg']
            },
            'monte_carlo': {
                'methodology': 'Regime-switching simulation with fat tails',
                'simulations': 5000,
                'horizon': '48 months'
            }
        }
    
    def _aggregate_path_metrics(self, path_id: str, path_config: dict) -> PathMetrics:
        """Aggregate metrics across strategies in a path."""
        
        strategy_ids = path_config['strategies']
        
        # Filter results for this path's strategies
        bt_results = [r for r in self.battle_test_results if r['strategy_id'] in strategy_ids]
        mc_results = [r for r in self.monte_carlo_results if r['strategy_id'] in strategy_ids]
        
        # Calculate averages across strategies in path
        avg_return = np.mean([r['return_pct'] for r in bt_results]) if bt_results else 0
        max_drawdown = max([r['max_drawdown_pct'] for r in bt_results]) if bt_results else 0
        prob_loss = np.mean([r['prob_any_loss'] for r in mc_results]) if mc_results else 0
        
        # Convert return to APY (approximate)
        # Battle test is ~3.65 years, so annualize
        annual_return = avg_return / 3.65
        
        # Pre-calculate projections
        projections = self._calculate_projections(annual_return)
        
        # Add warning for high-risk paths
        warning = None
        if path_id == 'growth':
            warning = f"High volatility — up to {max_drawdown:.0f}% drawdown observed in historical testing"
        
        return PathMetrics(
            path_id=path_id,
            label=path_config['label'],
            description=path_config['description'],
            color=path_config['color'],
            risk_level=path_config['risk_level'],
            avg_apy=round(annual_return, 1),
            max_drawdown=round(max_drawdown, 1),
            probability_of_loss=round(prob_loss, 1),
            projections=projections,
            warning=warning
        )
    
    def _calculate_projections(self, annual_return: float) -> Dict[str, PathProjection]:
        """Calculate projections for different time horizons."""
        
        # Convert annual return to decimal
        r = annual_return / 100
        bank_r = BANK_COMPARISON['apy'] / 100
        
        periods = {
            '1_week': 7 / 365,
            '1_month': 30 / 365,
            '1_year': 1,
            '5_years': 5
        }
        
        projections = {}
        for period_name, years in periods.items():
            multiplier = (1 + r) ** years
            bank_multiplier = (1 + bank_r) ** years
            
            projections[period_name] = PathProjection(
                period=period_name,
                multiplier=round(multiplier, 4),
                bank_multiplier=round(bank_multiplier, 4)
            )
        
        return projections
```

## 13.5 CLI Command

```python
# src/commands/dream_mode_export.py

import json
from pathlib import Path

from src.engines.dream_mode_export import DreamModeExporter
from src.collectors.file_loader import FileLoader
from config.settings import OUTPUT_DIR

def run_dream_mode_export(args):
    """Generate Dream Mode data for frontend."""
    
    print("🌙 Generating Dream Mode data...")
    
    # Load existing results
    bt_results_path = OUTPUT_DIR / 'battle_test_results.csv'
    mc_results_path = OUTPUT_DIR / 'monte_carlo_results.csv'
    
    if not bt_results_path.exists() or not mc_results_path.exists():
        print("❌ Error: Run battle-test and monte-carlo first")
        print("   python main.py battle-test")
        print("   python main.py monte-carlo")
        return
    
    import pandas as pd
    bt_results = pd.read_csv(bt_results_path).to_dict('records')
    mc_results = pd.read_csv(mc_results_path).to_dict('records')
    
    # Load strategies
    strategies_path = Path(__file__).parent.parent.parent / 'config' / 'strategies.json'
    with open(strategies_path) as f:
        strategies = json.load(f)['strategies']
    
    # Export
    exporter = DreamModeExporter(bt_results, mc_results, strategies)
    result = exporter.export(args.output)
    
    print(f"✅ Dream Mode data exported to: {args.output}")
    print(f"   Version: {result.version}")
    print(f"   Paths: {', '.join(result.paths.keys())}")
    print(f"   Generated: {result.generated_at.isoformat()}")
```

## 13.6 Expected Output

```json
{
  "version": "1.0",
  "generated_at": "2025-12-30T12:00:00Z",
  "data_sources": {
    "apy_data": {
      "source": "DeFiLlama",
      "period": "2022-05-01 to 2025-12-31",
      "last_updated": "2025-12-30"
    },
    "price_data": {
      "source": "Yahoo Finance",
      "period": "2022-05-01 to 2025-12-31"
    },
    "battle_test": {
      "methodology": "Historical backtesting with DCA",
      "period": "1,334 days (May 2022 - Dec 2025)",
      "events_captured": ["Terra/Luna collapse", "FTX crash", "USDC depeg"]
    },
    "monte_carlo": {
      "methodology": "Regime-switching simulation with fat tails",
      "simulations": 5000,
      "horizon": "48 months"
    }
  },
  "paths": {
    "safety": {
      "path_id": "safety",
      "label": "Safety First",
      "description": "Stable yield, no crypto exposure",
      "color": "#2563EB",
      "risk_level": "Minimal",
      "avg_apy": 9.5,
      "max_drawdown": 0.0,
      "probability_of_loss": 0.0,
      "projections": {
        "1_week": { "period": "1_week", "multiplier": 1.0018, "bank_multiplier": 1.0001 },
        "1_month": { "period": "1_month", "multiplier": 1.0079, "bank_multiplier": 1.0004 },
        "1_year": { "period": "1_year", "multiplier": 1.095, "bank_multiplier": 1.005 },
        "5_years": { "period": "5_years", "multiplier": 1.574, "bank_multiplier": 1.025 }
      },
      "warning": null
    },
    "balance": {
      "path_id": "balance",
      "label": "Balanced Growth",
      "description": "Moderate crypto exposure (30-40%)",
      "color": "#7C3AED",
      "risk_level": "Low-Medium",
      "avg_apy": 29.4,
      "max_drawdown": 13.0,
      "probability_of_loss": 18.7,
      "projections": {
        "1_week": { "period": "1_week", "multiplier": 1.0055, "bank_multiplier": 1.0001 },
        "1_month": { "period": "1_month", "multiplier": 1.024, "bank_multiplier": 1.0004 },
        "1_year": { "period": "1_year", "multiplier": 1.294, "bank_multiplier": 1.005 },
        "5_years": { "period": "5_years", "multiplier": 3.62, "bank_multiplier": 1.025 }
      },
      "warning": null
    },
    "growth": {
      "path_id": "growth",
      "label": "Maximum Growth",
      "description": "High crypto exposure (70-85%)",
      "color": "#DC2626",
      "risk_level": "High",
      "avg_apy": 184.0,
      "max_drawdown": 66.1,
      "probability_of_loss": 25.5,
      "projections": {
        "1_week": { "period": "1_week", "multiplier": 1.027, "bank_multiplier": 1.0001 },
        "1_month": { "period": "1_month", "multiplier": 1.12, "bank_multiplier": 1.0004 },
        "1_year": { "period": "1_year", "multiplier": 2.84, "bank_multiplier": 1.005 },
        "5_years": { "period": "5_years", "multiplier": 18.4, "bank_multiplier": 1.025 }
      },
      "warning": "High volatility — up to 66% drawdown observed in historical testing"
    }
  },
  "bank_comparison": {
    "apy": 0.5,
    "source": "ECB Statistics",
    "date": "December 2024",
    "note": "Average EU savings account rate. Rates may vary."
  },
  "disclaimers": {
    "simulation": "This is a simulation based on historical data from May 2022 to December 2025. Past performance does not guarantee future returns.",
    "risk": "Capital is at risk. Actual results may differ significantly.",
    "not_advice": "This is for educational purposes only and does not constitute investment advice.",
    "card_watermark": "⚠️ SIMULATION — Based on historical data. Not a guarantee. diboas.com",
    "bank_comparison": "Bank comparison based on average EU savings account rate of 0.5% APY. Source: ECB Statistics, December 2024. Rates may vary."
  },
  "regional_disclaimers": {
    "pt-BR": "⚠️ SIMULAÇÃO EDUCACIONAL — Este recurso utiliza dados históricos apenas para fins ilustrativos. Não constitui oferta de investimento, promessa de retorno ou aconselhamento financeiro. Resultados reais podem diferir significativamente.",
    "en-US": "⚠️ EDUCATIONAL SIMULATION — This feature uses historical data for illustrative purposes only. It does not constitute an offer of investment, promise of returns, or financial advice. Actual results may differ significantly."
  }
}
```

## 13.7 Tests

```python
# tests/test_dream_mode.py

import pytest
from src.engines.dream_mode_export import DreamModeExporter
from config.dream_mode import DREAM_MODE_PATHS, DISCLAIMERS

class TestDreamModeExport:
    
    def test_path_mapping_covers_all_strategies(self):
        """All 10 strategies should be mapped to exactly one path."""
        all_strategies = set()
        for path in DREAM_MODE_PATHS.values():
            all_strategies.update(path['strategies'])
        
        assert all_strategies == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    
    def test_safety_path_only_stable_strategies(self):
        """Safety path should only include 0% crypto strategies."""
        safety_strategies = DREAM_MODE_PATHS['safety']['strategies']
        assert safety_strategies == [1, 3, 5, 7, 9]
    
    def test_disclaimers_present(self):
        """All required disclaimers should be present."""
        required = ['simulation', 'risk', 'not_advice', 'card_watermark', 'bank_comparison']
        for key in required:
            assert key in DISCLAIMERS
            assert len(DISCLAIMERS[key]) > 0
    
    def test_projections_increase_over_time(self):
        """Multipliers should increase for longer time periods."""
        # Mock test - actual implementation would use real data
        pass
    
    def test_growth_path_has_warning(self):
        """Growth path should have volatility warning."""
        # The export should add a warning for high-risk paths
        pass
```

---

# IMPLEMENTATION NOTES

## Priority Order (Updated)

1. **Config loading** — Ensure strategies load from JSON
2. **Data loading** — File loader for bundled CSVs
3. **Battle Test** — Core backtesting with validation
4. **Monte Carlo** — Risk simulation
5. **Monitoring** — Health checks
6. **Anomaly Detection** — ML models
7. **CLI** — User interface
8. **Reports** — Output generation
9. **Dream Mode Export** — Consumer data (NEW)
10. **Tests** — Validation

## Key Principles

1. **Never hardcode strategies** — Always load from `config/strategies.json`
2. **Abstract data providers** — Easy to add new sources
3. **Validate everything** — CV-01 through CV-07 on every run
4. **Log extensively** — Audit trail for all operations
5. **Fail gracefully** — Handle API failures, missing data
6. **Dream Mode uses validated data only** — Export only what Battle Test and Monte Carlo produce

## Expected Outputs

After running `python main.py all`:

```
outputs/
├── battle_test_results.csv
├── battle_test_report.md
├── monte_carlo_results.csv
├── monte_carlo_report.md
├── protocol_health.json
├── anomaly_scores.json
├── validation_report.json
├── dream_mode_data.json          # NEW - for frontend
└── execution_metadata.json
```

---

**END OF HANDOFF DOCUMENT**
