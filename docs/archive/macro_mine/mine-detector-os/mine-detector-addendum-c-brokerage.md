# Mine Detector OS -- Addendum C: Brokerage Integration

> Real-time portfolio synchronization and risk-aware execution. Connects Mine Detector scores to actual positions.

**Version:** 2026-01-30-r9

**Cross-References:**
- Core OS: mine-detector-os.md (interface contract, position sizing, RiskCategory enum)
- Addendum D: mine-detector-addendum-d-adr-smallcap.md (crypto exchange connectors)
- Addendum E: mine-detector-addendum-e-maintenance-operations.md (API health monitoring)

---

## Overview

This addendum provides:

1. **Portfolio Synchronization** - Real-time position tracking across brokers
2. **Risk-Aware Execution** - Integration with Mine Detector scores
3. **Multi-Asset Support** - Equities, options, crypto, futures
4. **Confirmation Enforcement** - Safety checks before execution
5. **Market Halt Detection** - Pre-flight checks for halted securities

**Web3 Integration Note (r7):** For crypto and tokenized assets, this addendum handles execution and portfolio tracking, while **Addendum D** provides the structural risk overlay (smart contract risk, chain risk, etc.). When processing Web3 positions, the composite score should include the overlay from Addendum D's `compute_structural_overlay()` function.

---

## Interface Contract

Implements the Core OS Brokerage Integration interface:

```python
def get_portfolio_positions() -> List[Dict]:
    """
    Retrieve current portfolio positions.
    
    Returns:
        List of position dicts with:
        {
            'ticker': str,
            'quantity': float,
            'avg_cost': float,
            'current_price': float,
            'market_value': float,
            'unrealized_pnl': float,
            'asset_class': str,          # equity, option, crypto, etc.
            'contract_multiplier': float  # 1.0 for stocks, 100.0 for options
        }
    """
```

---

## Imports and Dependencies

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Import from shared module (Core OS)
from mine_detector_shared import utc_now, to_utc, format_timestamp, RiskCategory
```

---

## Supported Brokers

```python
class Broker(Enum):
    """Supported brokers."""
    INTERACTIVE_BROKERS = "interactive_brokers"
    TD_AMERITRADE = "td_ameritrade"
    SCHWAB = "schwab"
    FIDELITY = "fidelity"
    ROBINHOOD = "robinhood"
    ALPACA = "alpaca"
    TRADIER = "tradier"
    # Crypto
    COINBASE = "coinbase"
    BINANCE = "binance"
    KRAKEN = "kraken"


@dataclass
class BrokerConfig:
    """Configuration for a broker connection."""
    broker: Broker
    api_key: str
    api_secret: str
    account_id: Optional[str] = None
    paper_trading: bool = False
    
    # Capabilities
    supports_equities: bool = True
    supports_options: bool = False
    supports_crypto: bool = False
    supports_futures: bool = False
    
    # Limits
    max_orders_per_minute: int = 60
    max_positions: int = 100


BROKER_CAPABILITIES = {
    Broker.INTERACTIVE_BROKERS: {
        'equities': True, 'options': True, 'crypto': True, 'futures': True,
        'fractional': False, 'extended_hours': True
    },
    Broker.SCHWAB: {
        'equities': True, 'options': True, 'crypto': False, 'futures': True,
        'fractional': True, 'extended_hours': True
    },
    Broker.ALPACA: {
        'equities': True, 'options': False, 'crypto': True, 'futures': False,
        'fractional': True, 'extended_hours': True
    },
    Broker.COINBASE: {
        'equities': False, 'options': False, 'crypto': True, 'futures': False,
        'fractional': True, 'extended_hours': True  # 24/7
    },
    Broker.BINANCE: {
        'equities': False, 'options': False, 'crypto': True, 'futures': True,
        'fractional': True, 'extended_hours': True
    }
}
```

---

## Contract Multipliers

Contract multipliers convert between contract quantities and actual exposure:

```python
# IMPORTANT: All multipliers are floats to handle fractional contracts
CONTRACT_MULTIPLIERS: Dict[str, float] = {
    # Equities
    'equity': 1.0,
    
    # Options
    'option': 100.0,           # Standard equity options = 100 shares
    'mini_option': 10.0,       # Mini options = 10 shares
    'index_option': 100.0,     # Index options (SPX, etc.)
    
    # Futures
    'es_future': 50.0,         # E-mini S&P 500 = $50 x index
    'mes_future': 5.0,         # Micro E-mini S&P = $5 x index
    'nq_future': 20.0,         # E-mini Nasdaq = $20 x index
    'mnq_future': 2.0,         # Micro Nasdaq = $2 x index
    
    # Crypto futures
    'btc_future': 5.0,         # CME BTC futures = 5 BTC
    'eth_future': 50.0,        # CME ETH futures = 50 ETH
    'micro_btc_future': 0.1,   # Micro BTC = 0.1 BTC
    'micro_eth_future': 0.1,   # Micro ETH = 0.1 ETH
    
    # Spot crypto
    'crypto': 1.0,
    'crypto_perp': 1.0,        # Perpetual futures (varies by exchange)
}


def get_contract_multiplier(asset_class: str, 
                             ticker: str = None,
                             exchange: str = None) -> float:
    """
    Get the appropriate contract multiplier for an asset.
    
    Returns:
        Float multiplier (never int to avoid type issues)
    """
    # Check for specific futures contracts
    if asset_class == 'future' and ticker:
        ticker_upper = ticker.upper()
        
        # CME crypto futures
        if 'BTC' in ticker_upper:
            if 'MICRO' in ticker_upper or 'MBT' in ticker_upper:
                return CONTRACT_MULTIPLIERS['micro_btc_future']
            return CONTRACT_MULTIPLIERS['btc_future']
        
        if 'ETH' in ticker_upper:
            if 'MICRO' in ticker_upper or 'MET' in ticker_upper:
                return CONTRACT_MULTIPLIERS['micro_eth_future']
            return CONTRACT_MULTIPLIERS['eth_future']
        
        # E-mini futures
        if ticker_upper in ['ES', '/ES']:
            return CONTRACT_MULTIPLIERS['es_future']
        if ticker_upper in ['MES', '/MES']:
            return CONTRACT_MULTIPLIERS['mes_future']
        if ticker_upper in ['NQ', '/NQ']:
            return CONTRACT_MULTIPLIERS['nq_future']
        if ticker_upper in ['MNQ', '/MNQ']:
            return CONTRACT_MULTIPLIERS['mnq_future']
    
    return CONTRACT_MULTIPLIERS.get(asset_class, 1.0)
```

---

## Position Data Model

```python
@dataclass
class Position:
    """Normalized position across all brokers."""
    ticker: str
    quantity: float  # Number of contracts/shares
    avg_cost: float
    current_price: float
    
    # Classification
    asset_class: str = "equity"
    broker: Optional[Broker] = None
    account_id: Optional[str] = None
    
    # Contract details
    contract_multiplier: float = 1.0
    
    # Options-specific
    option_type: Optional[str] = None  # call, put
    strike: Optional[float] = None
    expiration: Optional[str] = None
    
    # Crypto-specific
    chain: Optional[str] = None
    contract_address: Optional[str] = None
    
    # Risk scores (populated by Mine Detector)
    composite_risk_score: Optional[float] = None
    dominant_risks: List[str] = field(default_factory=list)
    
    @property
    def market_value(self) -> float:
        """Calculate market value including contract multiplier."""
        return self.quantity * self.current_price * self.contract_multiplier
    
    @property
    def unrealized_pnl(self) -> float:
        """Calculate unrealized P&L including contract multiplier."""
        if self.avg_cost <= 0:
            return 0.0
        return (self.current_price - self.avg_cost) * self.quantity * self.contract_multiplier
    
    @property
    def unrealized_pnl_pct(self) -> float:
        """Calculate unrealized P&L percentage."""
        if self.avg_cost <= 0:
            return 0.0
        return ((self.current_price / self.avg_cost) - 1) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dict matching interface contract."""
        return {
            'ticker': self.ticker,
            'quantity': self.quantity,
            'avg_cost': self.avg_cost,
            'current_price': self.current_price,
            'market_value': self.market_value,
            'unrealized_pnl': self.unrealized_pnl,
            'asset_class': self.asset_class,
            'contract_multiplier': self.contract_multiplier,
            'broker': self.broker.value if self.broker else None,
            'composite_risk_score': self.composite_risk_score,
            'dominant_risks': self.dominant_risks
        }
```

---

## Market Status & Halt Detection

```python
class MarketStatus(Enum):
    """Market/security trading status."""
    OPEN = "open"
    CLOSED = "closed"
    PRE_MARKET = "pre_market"
    AFTER_HOURS = "after_hours"
    HALTED = "halted"           # Trading halt (T1, T2, etc.)
    SUSPENDED = "suspended"      # Longer suspension
    UNKNOWN = "unknown"


@dataclass
class HaltInfo:
    """Information about a trading halt."""
    ticker: str
    status: MarketStatus
    halt_code: Optional[str] = None  # T1, T2, T12, LUDP, etc.
    halt_time: Optional[datetime] = None
    expected_resume: Optional[datetime] = None
    reason: Optional[str] = None


class MarketStatusChecker:
    """
    Check market and security trading status.
    
    CRITICAL: Must check halt status before placing orders.
    """
    
    HALT_CODES = {
        'T1': 'News pending',
        'T2': 'News released',
        'T5': 'Price movement (10% in 5 min)',
        'T6': 'Extraordinary market activity',
        'T12': 'Additional information requested',
        'LUDP': 'Limit up/down pause',
        'MWCB': 'Market-wide circuit breaker'
    }
    
    def __init__(self):
        self._halt_cache: Dict[str, HaltInfo] = {}
        self._cache_time: Optional[datetime] = None
        self._cache_ttl_seconds = 30  # Refresh every 30 seconds
    
    def check_trading_status(self, ticker: str, 
                              broker: Broker = None) -> HaltInfo:
        """
        Check if a security is currently halted.
        
        Returns:
            HaltInfo with current status
        """
        # Check cache freshness
        now = utc_now()
        if (self._cache_time is None or 
            (now - self._cache_time).total_seconds() > self._cache_ttl_seconds):
            self._refresh_cache()
        
        # Return cached info or default OPEN
        if ticker.upper() in self._halt_cache:
            return self._halt_cache[ticker.upper()]
        
        return HaltInfo(
            ticker=ticker,
            status=MarketStatus.OPEN
        )
    
    def is_tradeable(self, ticker: str) -> bool:
        """Quick check if a security can be traded."""
        info = self.check_trading_status(ticker)
        return info.status in [MarketStatus.OPEN, MarketStatus.PRE_MARKET, 
                               MarketStatus.AFTER_HOURS]
    
    def _refresh_cache(self):
        """Refresh halt cache from data sources."""
        # In production: query NYSE/NASDAQ halt feeds, broker APIs
        self._cache_time = utc_now()
        # Placeholder - would populate from actual data sources
```

---

## Broker Adapter Base

```python
class BrokerAdapter(ABC):
    """
    Abstract base class for broker adapters.
    Each broker has a concrete implementation.
    """
    
    def __init__(self, config: BrokerConfig):
        self.config = config
        self._authenticated = False
        self.market_status = MarketStatusChecker()
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the broker."""
        pass
    
    @abstractmethod
    def get_positions(self) -> List[Position]:
        """Get all positions."""
        pass
    
    @abstractmethod
    def get_account_balance(self) -> Dict:
        """Get account balance and buying power."""
        pass
    
    @abstractmethod
    def place_order(self, order: 'Order') -> 'OrderResult':
        """Place an order."""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        pass
    
    def is_market_open(self) -> bool:
        """Check if market is open for this broker."""
        # Crypto brokers are 24/7
        if self.config.supports_crypto and not self.config.supports_equities:
            return True
        
        # Check US market hours
        import pytz
        et = pytz.timezone('US/Eastern')
        now = datetime.now(et)
        
        # Skip weekends
        if now.weekday() >= 5:
            return False
        
        # Regular hours: 9:30 AM - 4:00 PM ET
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= now <= market_close


class AlpacaAdapter(BrokerAdapter):
    """Alpaca broker adapter implementation."""
    
    def authenticate(self) -> bool:
        """Authenticate with Alpaca."""
        # Would use alpaca-trade-api
        # from alpaca_trade_api import REST
        # self.api = REST(self.config.api_key, self.config.api_secret)
        self._authenticated = True
        return True
    
    def get_positions(self) -> List[Position]:
        """Get positions from Alpaca."""
        if not self._authenticated:
            raise RuntimeError("Not authenticated")
        
        # Would call: positions = self.api.list_positions()
        # Convert to Position objects
        positions = []
        
        # Placeholder implementation
        return positions
    
    def get_account_balance(self) -> Dict:
        """Get Alpaca account info."""
        # Would call: account = self.api.get_account()
        return {
            'cash': 0.0,
            'buying_power': 0.0,
            'portfolio_value': 0.0
        }
    
    def place_order(self, order: 'Order') -> 'OrderResult':
        """Place order through Alpaca."""
        # Pre-flight halt check
        if not self.market_status.is_tradeable(order.ticker):
            halt_info = self.market_status.check_trading_status(order.ticker)
            return OrderResult(
                success=False,
                order_id=None,
                filled_quantity=0,
                filled_price=None,
                status='blocked',
                error_message=f'Security halted: {halt_info.halt_code or "unknown"}'
            )
        
        # Would call: self.api.submit_order(...)
        return OrderResult(
            success=True,
            order_id='placeholder',
            filled_quantity=0,
            filled_price=None,
            status='submitted'
        )
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel Alpaca order."""
        # Would call: self.api.cancel_order(order_id)
        return True
```

---

## Order Management

```python
class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class TimeInForce(Enum):
    DAY = "day"
    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"


@dataclass
class Order:
    """Order to be placed."""
    ticker: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    
    # Optional fields
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    trail_percent: Optional[float] = None
    
    time_in_force: TimeInForce = TimeInForce.DAY
    extended_hours: bool = False
    
    # Risk integration
    mine_detector_score: Optional[float] = None
    requires_confirmation: bool = False
    confirmation_reason: Optional[str] = None


@dataclass
class OrderResult:
    """Result of order placement."""
    success: bool
    order_id: Optional[str]
    filled_quantity: float
    filled_price: Optional[float]
    status: str
    error_message: Optional[str] = None
```

---

## Confirmation Enforcement

```python
class ConfirmationManager:
    """
    Manages confirmation requirements for high-risk actions.
    """
    
    ALWAYS_CONFIRM = [
        'close_all_positions',
        'liquidate_portfolio',
        'increase_position_high_risk',
        'new_position_critical_risk',
    ]
    
    SCORE_THRESHOLDS = {
        'warn': 50,
        'confirm': 70,
        'block': 86,  # Matches Core OS CRITICAL threshold (86-100)
    }
    
    def __init__(self):
        self.pending_confirmations: Dict[str, Dict] = {}
        self.confirmation_log: List[Dict] = []
    
    def check_action(self, action: str, ticker: str, 
                     risk_score: float, order: Order) -> Dict:
        """
        Check if an action requires confirmation.
        
        IMPORTANT (r8): The risk_score parameter MUST be the `adjusted_score`
        from compute_composite_score(), NOT the base composite_score.
        The adjusted_score includes:
        - Structural overlay points (from Addendum D)
        - Staleness penalty points (from Addendum E)
        
        Using composite_score instead of adjusted_score would bypass
        critical structural risk adjustments.
        """
        # ==========================================================================
        # HARD BLOCK CHECK - MUST BE FIRST (r8 fix)
        # ==========================================================================
        # Score >= 86 is an UNCONDITIONAL hard block. This check MUST happen
        # BEFORE the ALWAYS_CONFIRM check to prevent confirmation from bypassing
        # the safety threshold. A CRITICAL score cannot be overridden by any
        # confirmation mechanism.
        # ==========================================================================
        if risk_score >= self.SCORE_THRESHOLDS['block']:
            return {
                'requires_confirmation': True,
                'confirmation_id': None,
                'reason': f'Risk score {risk_score:.0f} exceeds block threshold (86 = CRITICAL)',
                'can_override': False
            }
        
        # ==========================================================================
        # ALWAYS_CONFIRM CHECK - After hard block (r8 fix)
        # ==========================================================================
        # These actions require confirmation but CAN be overridden (unlike hard block).
        # This check is intentionally AFTER the hard block check.
        # ==========================================================================
        if action in self.ALWAYS_CONFIRM:
            conf_id = self._generate_id()
            self.pending_confirmations[conf_id] = {
                'action': action,
                'ticker': ticker,
                'order': order,
                'risk_score': risk_score,
                'created_at': utc_now()
            }
            return {
                'requires_confirmation': True,
                'confirmation_id': conf_id,
                'reason': f'Action "{action}" always requires confirmation',
                'can_override': True
            }
        
        # Score-based confirmation (below hard block threshold)
        if risk_score >= self.SCORE_THRESHOLDS['confirm']:
            conf_id = self._generate_id()
            self.pending_confirmations[conf_id] = {
                'action': action,
                'ticker': ticker,
                'order': order,
                'risk_score': risk_score,
                'created_at': utc_now()
            }
            return {
                'requires_confirmation': True,
                'confirmation_id': conf_id,
                'reason': f'Risk score {risk_score:.0f} exceeds confirm threshold (70)',
                'can_override': True
            }
        
        if risk_score >= self.SCORE_THRESHOLDS['warn']:
            return {
                'requires_confirmation': False,
                'confirmation_id': None,
                'reason': f'Warning: Risk score {risk_score:.0f} is elevated',
                'can_override': True
            }
        
        return {
            'requires_confirmation': False,
            'confirmation_id': None,
            'reason': None,
            'can_override': True
        }
    
    def confirm(self, confirmation_id: str, confirmed_by: str,
                override_reason: str = None) -> bool:
        """Confirm a pending action."""
        if confirmation_id not in self.pending_confirmations:
            return False
        
        pending = self.pending_confirmations[confirmation_id]
        
        # Check expiration (5 minutes)
        age = (utc_now() - pending['created_at']).total_seconds()
        if age > 300:
            del self.pending_confirmations[confirmation_id]
            return False
        
        # Log
        self.confirmation_log.append({
            'confirmation_id': confirmation_id,
            'action': pending['action'],
            'ticker': pending['ticker'],
            'risk_score': pending['risk_score'],
            'confirmed_by': confirmed_by,
            'override_reason': override_reason,
            'confirmed_at': utc_now()
        })
        
        del self.pending_confirmations[confirmation_id]
        return True
    
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]
```

---

## Risk-Aware Execution

```python
class RiskAwareExecutor:
    """Execute orders with Mine Detector risk integration."""
    
    def __init__(self, broker_adapter: BrokerAdapter):
        self.adapter = broker_adapter
        self.confirmation_manager = ConfirmationManager()
    
    def execute_with_risk_check(self, order: Order, risk_score: float,
                                 risk_details: Dict) -> Dict:
        """
        Execute an order with full risk checks including halt detection.
        
        CRITICAL (r8): The risk_score parameter MUST be the `adjusted_score`
        from compute_composite_score(), which includes:
        - Base weighted composite score
        - Structural overlay points (from Addendum D)
        - Staleness penalty points (from Addendum E)
        
        DO NOT pass composite_score (the unadjusted value). This would bypass
        critical risk adjustments and potentially allow execution on securities
        that should be blocked.
        
        Example:
            result = compute_composite_score(category_scores, overlay_notches=1.5)
            # Use result['adjusted_score'], NOT result['composite_score']
            executor.execute_with_risk_check(order, result['adjusted_score'], result)
        """
        warnings = []
        
        # PRE-FLIGHT CHECK 1: Market halt status
        halt_info = self.adapter.market_status.check_trading_status(order.ticker)
        if halt_info.status in [MarketStatus.HALTED, MarketStatus.SUSPENDED]:
            return {
                'executed': False,
                'order_result': None,
                'confirmation_required': False,
                'blocked': True,
                'block_reason': f'Security is halted: {halt_info.halt_code or "unknown"} - {halt_info.reason or ""}',
                'halt_info': {
                    'status': halt_info.status.value,
                    'code': halt_info.halt_code,
                    'reason': halt_info.reason,
                    'expected_resume': format_timestamp(halt_info.expected_resume) if halt_info.expected_resume else None
                },
                'warnings': []
            }
        
        # Determine action type
        if order.side == OrderSide.BUY:
            # NOTE: >= 86 matches CRITICAL threshold from Core OS and ConfirmationManager
            if risk_score >= 86:
                action = 'new_position_critical_risk'
            elif risk_score > 70:
                action = 'increase_position_high_risk'
            else:
                action = 'buy'
        else:
            action = 'sell'
        
        # Check confirmation requirements
        conf_check = self.confirmation_manager.check_action(
            action=action,
            ticker=order.ticker,
            risk_score=risk_score,
            order=order
        )
        
        # Add warnings
        if risk_details.get('dominant_risks'):
            for risk in risk_details['dominant_risks'][:3]:
                warnings.append(f'Elevated {risk}')
        
        # If blocked (score >= 86, CRITICAL threshold), return immediately
        if conf_check['requires_confirmation'] and not conf_check['can_override']:
            return {
                'executed': False,
                'order_result': None,
                'confirmation_required': True,
                'confirmation_id': None,
                'blocked': True,
                'block_reason': conf_check['reason'],
                'warnings': warnings
            }
        
        # If confirmation required, return pending
        if conf_check['requires_confirmation']:
            return {
                'executed': False,
                'order_result': None,
                'confirmation_required': True,
                'confirmation_id': conf_check['confirmation_id'],
                'blocked': False,
                'warnings': warnings
            }
        
        # Execute
        try:
            result = self.adapter.place_order(order)
            return {
                'executed': result.success,
                'order_result': result,
                'confirmation_required': False,
                'confirmation_id': None,
                'blocked': False,
                'warnings': warnings
            }
        except Exception as e:
            return {
                'executed': False,
                'order_result': OrderResult(
                    success=False,
                    order_id=None,
                    filled_quantity=0,
                    filled_price=None,
                    status='error',
                    error_message=str(e)
                ),
                'confirmation_required': False,
                'confirmation_id': None,
                'blocked': False,
                'warnings': warnings
            }
```

---

## Portfolio Manager

```python
class PortfolioManager:
    """Manages portfolio across multiple brokers."""
    
    def __init__(self, adapters: List[BrokerAdapter] = None):
        self.adapters = adapters or []
    
    def get_all_positions(self) -> List[Position]:
        """Get positions from all brokers."""
        all_positions = []
        
        for adapter in self.adapters:
            try:
                positions = adapter.get_positions()
                all_positions.extend(positions)
            except Exception as e:
                print(f"Error fetching positions from {adapter.config.broker}: {e}")
        
        return all_positions
    
    def get_position_by_ticker(self, ticker: str) -> Optional[Position]:
        """Get position for a specific ticker."""
        all_positions = self.get_all_positions()
        for pos in all_positions:
            if pos.ticker.upper() == ticker.upper():
                return pos
        return None
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary statistics."""
        positions = self.get_all_positions()
        
        if not positions:
            return {
                'total_value': 0.0,
                'total_pnl': 0.0,
                'position_count': 0,
                'by_asset_class': {}
            }
        
        total_value = sum(p.market_value for p in positions)
        total_pnl = sum(p.unrealized_pnl for p in positions)
        
        by_class = {}
        for pos in positions:
            cls = pos.asset_class
            if cls not in by_class:
                by_class[cls] = {'count': 0, 'value': 0.0}
            by_class[cls]['count'] += 1
            by_class[cls]['value'] += pos.market_value
        
        return {
            'total_value': round(total_value, 2),
            'total_pnl': round(total_pnl, 2),
            'position_count': len(positions),
            'by_asset_class': by_class
        }
    
    def enrich_with_risk_scores(self, mine_detector_scores: Dict[str, Dict]) -> List[Position]:
        """Enrich positions with Mine Detector risk scores."""
        positions = self.get_all_positions()
        
        for pos in positions:
            if pos.ticker in mine_detector_scores:
                scores = mine_detector_scores[pos.ticker]
                pos.composite_risk_score = scores.get('adjusted_score')
                pos.dominant_risks = scores.get('dominant_risks', [])
        
        return positions


# Main interface implementation
def get_portfolio_positions(portfolio_manager: PortfolioManager = None) -> List[Dict]:
    """
    Main interface implementation for Core OS.
    
    Returns normalized positions across all connected brokers.
    """
    if portfolio_manager is None:
        portfolio_manager = PortfolioManager()
    
    positions = portfolio_manager.get_all_positions()
    return [pos.to_dict() for pos in positions]
```

---

## API Health Monitoring

```python
class BrokerHealthMonitor:
    """Monitor broker API health and availability."""
    
    def __init__(self, adapters: List[BrokerAdapter] = None):
        self.adapters = adapters or []
        self.health_history: Dict[Broker, List[Dict]] = {}
    
    def check_all(self) -> Dict[Broker, Dict]:
        """Check health of all broker connections."""
        results = {}
        
        for adapter in self.adapters:
            broker = adapter.config.broker
            result = self._check_single(adapter)
            results[broker] = result
            
            if broker not in self.health_history:
                self.health_history[broker] = []
            self.health_history[broker].append({
                'timestamp': utc_now(),
                **result
            })
            self.health_history[broker] = self.health_history[broker][-100:]
        
        return results
    
    def _check_single(self, adapter: BrokerAdapter) -> Dict:
        """Check health of a single broker."""
        start_time = utc_now()
        
        try:
            adapter.get_account_balance()
            latency = (utc_now() - start_time).total_seconds() * 1000
            
            return {
                'healthy': True,
                'latency_ms': round(latency, 1),
                'error': None,
                'market_open': adapter.is_market_open()
            }
        except Exception as e:
            return {
                'healthy': False,
                'latency_ms': None,
                'error': str(e),
                'market_open': None
            }
    
    def get_availability(self, broker: Broker, hours: int = 24) -> float:
        """Get availability percentage over time period."""
        if broker not in self.health_history:
            return 0.0
        
        cutoff = utc_now() - timedelta(hours=hours)
        recent = [h for h in self.health_history[broker] if h['timestamp'] > cutoff]
        
        if not recent:
            return 0.0
        
        healthy_count = sum(1 for h in recent if h['healthy'])
        return round(healthy_count / len(recent) * 100, 1)
```

---

## Dashboard Output

```
================================================================================
                        PORTFOLIO & RISK OVERVIEW
                        2026-01-30 10:00 UTC
================================================================================

PORTFOLIO SUMMARY
--------------------------------------------------------------------------------
Total Value:      $247,832.45
Unrealized P&L:   +$12,456.78 (+5.3%)
Position Count:   15
Cash Available:   $52,167.55

POSITIONS WITH RISK SCORES
--------------------------------------------------------------------------------
Ticker    Qty      Value       P&L      Risk   Dominant Risks
------    -----    --------    ------   ----   --------------------------
AAPL      100      $18,234     +$1,234  32     [OK]
NVDA      50       $24,567     +$4,567  45     Crowding, Momentum
XYZ       200      $8,456      -$234    72     [!] Solvency, Governance
TSLA      25       $12,345     +$567    58     Momentum, Crowding

HIGH RISK POSITIONS (Score > 70)
--------------------------------------------------------------------------------
[!] XYZ:  Score 72 - REDUCE RECOMMENDED
         Dominant: Solvency Risk (85), Governance Risk (72)
         Action: Consider reducing position by 50%

HALTED SECURITIES
--------------------------------------------------------------------------------
None currently halted in portfolio

BROKER STATUS
--------------------------------------------------------------------------------
Broker              Status    Latency    Availability (24h)
------------------  --------  ---------  ------------------
Interactive Brokers  [OK]     45ms       99.8%
Alpaca               [OK]     32ms       99.5%
Coinbase             [OK]     78ms       100.0%

================================================================================
```

---

---

## Future Enhancements to be Evaluated

The following topics have been identified for potential future development:

- **Use Decimal instead of float:** Switch from `float` to Python's `Decimal` class for all financial calculations (prices, quantities, market values) to prevent floating-point precision errors in ledger/accounting scenarios.

- **Currency conversion:** Add currency rate handling to the Position dataclass and PortfolioManager. Currently, market_value calculations assume all prices are in the portfolio's base currency. This matters for ADRs traded in foreign currencies and stablecoins (USDT vs USD).

- **API key storage practices:** Move credential storage from BrokerConfig attributes to environment variables or a secrets manager (e.g., HashiCorp Vault). Add logging redaction to prevent accidental credential exposure in SystemHealthMonitor logs.

---

*Addendum C - Mine Detector OS v2026-01-30-r9*
