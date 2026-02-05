# Strategy Board CTO Handoff
## Layer 4: Intelligence Engine Specification

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Prepared by:** Strategy Board  
**For:** CTO Board â€” diboas-analytics Implementation  
**Status:** Ready for Implementation

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Pipeline Context](#2-pipeline-context)
3. [Trigger System](#3-trigger-system)
4. [Action Routing](#4-action-routing)
5. [Rebalancing Engine](#5-rebalancing-engine)
6. [Alert Consolidation](#6-alert-consolidation)
7. [Priority & Escalation](#7-priority--escalation)
8. [Cross-Strategy Correlation](#8-cross-strategy-correlation)
9. [Configuration Files](#9-configuration-files)
10. [API Specifications](#10-api-specifications)
11. [Database Schema](#11-database-schema)
12. [Integration Points](#12-integration-points)
13. [Testing Requirements](#13-testing-requirements)

---

## 1. Executive Summary

### 1.1 Purpose

This document specifies **Layer 4: Intelligence** of the diboas-analytics data pipeline. The Intelligence Engine transforms validated analytics data into actionable triggers, alerts, and recommendations.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Trigger detection and classification | Data collection (Rakia) |
| Strategy-to-event mapping | Analytics calculations (QR Board) |
| Rebalancing rule evaluation | Message content/templates (CMO Board) |
| Alert generation and routing | Legal compliance checking (CLO Board) |
| Priority assignment | User interface design |
| Alert consolidation | On-chain execution |

### 1.3 Position in Pipeline

```
Layer 1 â†’ Layer 2 â†’ Layer 3 â†’ [LAYER 4] â†’ Layer 5
Collection  Validation  Analytics  INTELLIGENCE  Presentation
 (Rakia)     (Rakia)    (QR Board)  (Strategy)   (CMO/CLO)
```

### 1.4 Input Sources

| Source | Data Type | Frequency |
|--------|-----------|-----------|
| QR Board Analytics | Risk metrics, Monte Carlo results | On calculation completion |
| Protocol Health | TVL, APY, utilization | Every 15 minutes |
| Price Feeds | BTC, ETH, SOL, stablecoins | Every 5 minutes |
| Estate Wallets | Movement alerts | Every 60 minutes |
| Whale Wallets | Large transactions | Every 60 minutes |
| Macro Indicators | VIX, Treasury yields | Every 15 minutes |

### 1.5 Output Targets

| Target | Output Type | Delivery |
|--------|-------------|----------|
| Adelaide Newsletter | Structured alert objects | Real-time + batched |
| Strategy Board Dashboard | Monitoring data | Real-time |
| User Notifications | Alert payloads | Priority-based |
| Audit Log | Decision records | Every event |

---

## 2. Pipeline Context

### 2.1 What Strategy Board Receives (Inputs)

From **QR Board Analytics Engine**:
```json
{
  "strategy_id": 1,
  "timestamp": "2026-01-23T10:00:00Z",
  "metrics": {
    "current_apy": 4.2,
    "var_95": 2.1,
    "cvar_99": 3.4,
    "sharpe_ratio": 1.8,
    "max_drawdown": 5.2,
    "probability_of_loss": 0.03
  },
  "monte_carlo": {
    "median_return": 4.1,
    "ci_5th": 2.8,
    "ci_95th": 5.9,
    "crash_scenario_loss": -8.2
  }
}
```

From **Protocol Health Monitoring**:
```json
{
  "protocol": "sky_ssr",
  "timestamp": "2026-01-23T10:00:00Z",
  "tvl_usd": 2_850_000_000,
  "tvl_change_24h_pct": -3.2,
  "current_apy": 4.5,
  "apy_7d_avg": 4.8,
  "utilization_pct": 67.3,
  "usds_peg": 0.9985
}
```

From **Price Feeds**:
```json
{
  "timestamp": "2026-01-23T10:00:00Z",
  "prices": {
    "BTC": {"price": 42500, "change_24h_pct": -8.5},
    "ETH": {"price": 2250, "change_24h_pct": -12.3},
    "SOL": {"price": 98, "change_24h_pct": -15.2}
  }
}
```

From **Estate/Whale Monitoring**:
```json
{
  "event_type": "estate_movement",
  "timestamp": "2026-01-23T10:00:00Z",
  "estate": "ftx",
  "wallet": "0x123...",
  "amount_usd": 45_000_000,
  "asset": "ETH",
  "direction": "outflow"
}
```

### 2.2 What Strategy Board Produces (Outputs)

**Alert Object**:
```json
{
  "alert_id": "ALT-2026-01-23-001",
  "timestamp": "2026-01-23T10:00:05Z",
  "event_type": "btc_price_drop",
  "trigger": {
    "condition": "btc_drop_24h > 10%",
    "actual_value": 12.3,
    "threshold": 10
  },
  "classification": {
    "level": 3,
    "level_name": "warning",
    "priority": "P0",
    "category": "market_condition"
  },
  "affected_strategies": [3, 4, 5, 6, 7, 8, 9, 10],
  "action": {
    "type": "crisis_template",
    "template_id": "market_volatility_alert",
    "requires_consolidation": true
  },
  "routing": {
    "channels": ["email", "in_app", "push"],
    "user_segments": ["strategies_3_to_10"],
    "escalation": {
      "if_no_ack_minutes": 30,
      "escalate_to": "ceo_board"
    }
  },
  "metadata": {
    "source_data": {...},
    "validation_gate_passed": true,
    "consolidation_group": "market_crash_2026-01-23"
  }
}
```

**Rebalance Recommendation**:
```json
{
  "recommendation_id": "REB-2026-01-23-001",
  "timestamp": "2026-01-23T10:00:05Z",
  "user_id": "user_123",
  "strategy_id": 6,
  "type": "suggested",
  "reason": "allocation_drift",
  "current_allocations": {
    "stable": {"sky_ssr": 52, "aave_v3": 18},
    "crypto": {"sanctum_inf": 20, "jlp": 10}
  },
  "target_allocations": {
    "stable": {"sky_ssr": 50, "aave_v3": 20},
    "crypto": {"sanctum_inf": 20, "jlp": 10}
  },
  "max_drift_pct": 7.2,
  "threshold_type": "suggest",
  "user_action_required": true
}
```

---

## 3. Trigger System

### 3.1 Trigger Categories

The Intelligence Engine monitors 5 trigger categories:

| Category | Description | Check Frequency |
|----------|-------------|-----------------|
| Protocol Health | TVL, APY, utilization, depeg | 5-15 minutes |
| Market Conditions | BTC, ETH, SOL price movements | 5 minutes |
| Estate & Whale | Large wallet movements | 60 minutes |
| Macro Indicators | VIX, Treasury yields, M2 | 15-60 minutes |
| Strategy Performance | Drift, underperformance | Daily |

### 3.2 Protocol Health Triggers

#### 3.2.1 Sky/USDS Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `SKY-DEP-L1` | USDS depeg | >0.5% off peg | 1 (Watch) | 1, 3, 5, 7, 9 |
| `SKY-DEP-L2` | USDS depeg | >1.0% off peg | 2 (Caution) | 1, 3, 5, 7, 9 |
| `SKY-DEP-L3` | USDS depeg | >2.0% off peg | 3 (Warning) | 1, 3, 5, 7, 9 |
| `SKY-DEP-L4` | USDS depeg | >5.0% off peg | 4 (Critical) | 1, 3, 5, 7, 9 |
| `SKY-TVL-L2` | TVL drop | >10% in 24h | 2 (Caution) | 1, 3, 5, 7, 9 |
| `SKY-TVL-L3` | TVL drop | >25% in 24h | 3 (Warning) | 1, 3, 5, 7, 9 |
| `SKY-BUF-L2` | Surplus buffer | <$50M | 2 (Caution) | 1, 3, 5, 7, 9 |
| `SKY-APY-L2` | APY drop | >30% from 7d avg | 2 (Caution) | 1, 3, 5, 7, 9 |

**USDS Depeg Calculation**:
```python
def calculate_usds_depeg(usds_price: float) -> float:
    """Calculate USDS deviation from $1.00 peg."""
    return abs(1.0 - usds_price) * 100  # Returns percentage

# Example: usds_price = 0.985 â†’ depeg = 1.5%
```

#### 3.2.2 Sanctum Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `SAN-APY-L2` | APY drop | >50% from 7d avg | 2 (Caution) | 2, 4, 6, 8, 10 |
| `SAN-TVL-L3` | TVL drop | >20% in 24h | 3 (Warning) | 2, 4, 6, 8, 10 |
| `SAN-TVL-L4` | TVL drop | >50% in 24h | 4 (Critical) | 2, 4, 6, 8, 10 |

#### 3.2.3 Jupiter JLP Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `JLP-UTL-L2` | Utilization | >90% | 2 (Caution) | 6, 8, 10 |
| `JLP-APY-L2` | APY drop | >40% from 7d avg | 2 (Caution) | 6, 8, 10 |
| `JLP-TVL-L3` | TVL drop | >30% in 24h | 3 (Warning) | 6, 8, 10 |

#### 3.2.4 Fallback Protocol Triggers (Aave, Compound)

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `AAVE-UTL-L2` | Utilization | >85% | 2 (Caution) | Fallback users |
| `COMP-UTL-L2` | Utilization | >85% | 2 (Caution) | Fallback users |

### 3.3 Market Condition Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `MKT-BTC-L3` | BTC drop | >10% in 24h | 3 (Warning) | 3, 4, 5, 6, 7, 8, 9, 10 |
| `MKT-BTC-L4` | BTC drop | >20% in 24h | 4 (Critical) | ALL (1-10) |
| `MKT-ETH-L3` | ETH drop | >15% in 24h | 3 (Warning) | 2, 4, 6, 8, 10 |
| `MKT-SOL-L3` | SOL drop | >20% in 24h | 3 (Warning) | 2, 4, 6, 8, 10 |
| `MKT-SOL-L4` | SOL drop | >30% in 24h | 4 (Critical) | 2, 4, 6, 8, 10 |
| `MKT-BTC-UP` | BTC pump | >15% in 24h | Info | 3, 4, 6, 8, 10 |
| `MKT-CAP-L3` | Total crypto market cap | >15% drop in 24h | 3 (Warning) | 3-10 |

**Price Change Calculation**:
```python
def calculate_price_change_24h(current: float, price_24h_ago: float) -> float:
    """Calculate 24-hour percentage change."""
    if price_24h_ago == 0:
        return 0
    return ((current - price_24h_ago) / price_24h_ago) * 100

# Example: current=42500, price_24h_ago=48000 â†’ change = -11.46%
```

### 3.4 Estate & Whale Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `EST-MOV-INFO` | Estate wallet movement | >$10M | Info | ALL |
| `EST-MOV-L2` | Estate wallet movement | >$50M | 2 (Caution) | ALL |
| `EST-MOV-L3` | Estate wallet movement | >$100M | 3 (Warning) | ALL |
| `EST-MTGOX` | Mt. Gox distribution | Any confirmed | 3 (Warning) | ALL |
| `EST-FTX` | FTX estate movement | Any confirmed | 2 (Caution) | ALL |
| `WHL-ACC-INFO` | Whale accumulation | >$50M in 7d | Info | Related strategies |
| `WHL-DIST-L2` | Whale distribution | >$50M in 7d | 2 (Caution) | Related strategies |

**Estate Wallet List** (from Rakia data):
```python
MONITORED_ESTATES = {
    "mtgox": {
        "wallets": ["1PuQBfbZ3yG4xqz7..."],  # From estate_wallet_tracker.csv
        "total_holdings_btc": 34689,
        "deadline": "2026-10-31"
    },
    "ftx": {
        "wallets": ["0x456...", "So1ana..."],
        "total_holdings_usd": 3_200_000_000,
        "monthly_unlocks": True
    },
    "genesis": {
        "wallets": ["0x789..."],
        "total_holdings_usd": 1_800_000_000,
        "status": "distribution_pending"
    },
    "celsius": {
        "wallets": ["0xabc..."],
        "total_holdings_usd": 850_000_000,
        "status": "bankruptcy_proceedings"
    },
    "uk_gov": {
        "wallets": ["bc1q..."],
        "total_holdings_btc": 61000,
        "status": "civil_proceedings"
    }
}
```

### 3.5 Macro Triggers

| Trigger ID | Event | Threshold | Level | Affected Strategies |
|------------|-------|-----------|-------|---------------------|
| `MAC-VIX-L2` | VIX spike | >30 | 2 (Caution) | ALL |
| `MAC-VIX-L3` | VIX spike | >40 | 3 (Warning) | ALL |
| `MAC-FED-INFO` | Fed rate decision | Any change | Info | ALL |
| `MAC-10Y-INFO` | 10Y Treasury spike | >50bps in 1 week | Info | ALL |
| `MAC-STBL-L2` | Stablecoin supply | >5% drop in 7d | 2 (Caution) | ALL |

### 3.6 Trigger Evaluation Engine

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import datetime

class TriggerLevel(Enum):
    INFO = 0
    WATCH = 1
    CAUTION = 2
    WARNING = 3
    CRITICAL = 4

@dataclass
class TriggerResult:
    trigger_id: str
    triggered: bool
    level: TriggerLevel
    actual_value: float
    threshold: float
    affected_strategies: List[int]
    timestamp: datetime.datetime
    metadata: dict

class TriggerEngine:
    """Evaluates all trigger conditions against incoming data."""
    
    def __init__(self, config: dict):
        self.triggers = self._load_triggers(config)
        self.cooldowns = {}  # Prevent alert spam
    
    def evaluate_all(self, data: dict) -> List[TriggerResult]:
        """Evaluate all triggers against current data."""
        results = []
        
        # Protocol triggers
        if "protocol_health" in data:
            results.extend(self._evaluate_protocol_triggers(data["protocol_health"]))
        
        # Market triggers
        if "prices" in data:
            results.extend(self._evaluate_market_triggers(data["prices"]))
        
        # Estate/whale triggers
        if "wallet_events" in data:
            results.extend(self._evaluate_wallet_triggers(data["wallet_events"]))
        
        # Macro triggers
        if "macro" in data:
            results.extend(self._evaluate_macro_triggers(data["macro"]))
        
        # Filter by cooldown
        results = self._apply_cooldowns(results)
        
        return results
    
    def _evaluate_protocol_triggers(self, health_data: dict) -> List[TriggerResult]:
        """Evaluate protocol health triggers."""
        results = []
        
        # Sky/USDS depeg
        if "sky_ssr" in health_data:
            sky = health_data["sky_ssr"]
            usds_peg = sky.get("usds_peg", 1.0)
            depeg_pct = abs(1.0 - usds_peg) * 100
            
            # Check each depeg level
            depeg_thresholds = [
                ("SKY-DEP-L1", 0.5, TriggerLevel.WATCH),
                ("SKY-DEP-L2", 1.0, TriggerLevel.CAUTION),
                ("SKY-DEP-L3", 2.0, TriggerLevel.WARNING),
                ("SKY-DEP-L4", 5.0, TriggerLevel.CRITICAL),
            ]
            
            for trigger_id, threshold, level in depeg_thresholds:
                if depeg_pct > threshold:
                    results.append(TriggerResult(
                        trigger_id=trigger_id,
                        triggered=True,
                        level=level,
                        actual_value=depeg_pct,
                        threshold=threshold,
                        affected_strategies=[1, 3, 5, 7, 9],
                        timestamp=datetime.datetime.utcnow(),
                        metadata={"protocol": "sky_ssr", "usds_price": usds_peg}
                    ))
                    break  # Only highest triggered level
            
            # Sky TVL drop
            tvl_change = sky.get("tvl_change_24h_pct", 0)
            if tvl_change < -25:
                results.append(TriggerResult(
                    trigger_id="SKY-TVL-L3",
                    triggered=True,
                    level=TriggerLevel.WARNING,
                    actual_value=abs(tvl_change),
                    threshold=25,
                    affected_strategies=[1, 3, 5, 7, 9],
                    timestamp=datetime.datetime.utcnow(),
                    metadata={"protocol": "sky_ssr"}
                ))
            elif tvl_change < -10:
                results.append(TriggerResult(
                    trigger_id="SKY-TVL-L2",
                    triggered=True,
                    level=TriggerLevel.CAUTION,
                    actual_value=abs(tvl_change),
                    threshold=10,
                    affected_strategies=[1, 3, 5, 7, 9],
                    timestamp=datetime.datetime.utcnow(),
                    metadata={"protocol": "sky_ssr"}
                ))
        
        return results
    
    def _evaluate_market_triggers(self, price_data: dict) -> List[TriggerResult]:
        """Evaluate market condition triggers."""
        results = []
        
        # BTC drop
        if "BTC" in price_data:
            btc_change = price_data["BTC"].get("change_24h_pct", 0)
            
            if btc_change < -20:
                results.append(TriggerResult(
                    trigger_id="MKT-BTC-L4",
                    triggered=True,
                    level=TriggerLevel.CRITICAL,
                    actual_value=abs(btc_change),
                    threshold=20,
                    affected_strategies=list(range(1, 11)),  # ALL
                    timestamp=datetime.datetime.utcnow(),
                    metadata={"asset": "BTC", "price": price_data["BTC"]["price"]}
                ))
            elif btc_change < -10:
                results.append(TriggerResult(
                    trigger_id="MKT-BTC-L3",
                    triggered=True,
                    level=TriggerLevel.WARNING,
                    actual_value=abs(btc_change),
                    threshold=10,
                    affected_strategies=[3, 4, 5, 6, 7, 8, 9, 10],
                    timestamp=datetime.datetime.utcnow(),
                    metadata={"asset": "BTC", "price": price_data["BTC"]["price"]}
                ))
            elif btc_change > 15:
                results.append(TriggerResult(
                    trigger_id="MKT-BTC-UP",
                    triggered=True,
                    level=TriggerLevel.INFO,
                    actual_value=btc_change,
                    threshold=15,
                    affected_strategies=[3, 4, 6, 8, 10],
                    timestamp=datetime.datetime.utcnow(),
                    metadata={"asset": "BTC", "price": price_data["BTC"]["price"]}
                ))
        
        return results
    
    def _apply_cooldowns(self, results: List[TriggerResult]) -> List[TriggerResult]:
        """Apply cooldown periods to prevent alert spam."""
        COOLDOWN_MINUTES = {
            TriggerLevel.INFO: 240,      # 4 hours
            TriggerLevel.WATCH: 120,     # 2 hours
            TriggerLevel.CAUTION: 60,    # 1 hour
            TriggerLevel.WARNING: 30,    # 30 minutes
            TriggerLevel.CRITICAL: 15,   # 15 minutes
        }
        
        filtered = []
        now = datetime.datetime.utcnow()
        
        for result in results:
            cooldown_key = result.trigger_id
            cooldown_minutes = COOLDOWN_MINUTES.get(result.level, 60)
            
            last_triggered = self.cooldowns.get(cooldown_key)
            if last_triggered:
                elapsed = (now - last_triggered).total_seconds() / 60
                if elapsed < cooldown_minutes:
                    continue  # Still in cooldown
            
            # Not in cooldown, include and update
            filtered.append(result)
            self.cooldowns[cooldown_key] = now
        
        return filtered
```

---

## 4. Action Routing

### 4.1 Action Types

| Action Type | Description | Use Case |
|-------------|-------------|----------|
| `crisis_template` | Use crisis communication template | Market crashes, protocol incidents |
| `protocol_alert` | Protocol-specific alert | TVL drops, APY changes, depegs |
| `smart_money_insight` | Informational whale/estate update | Estate movements, whale activity |
| `performance_alert` | Strategy underperformance notice | Drift, yield below expectations |
| `opportunity_insight` | Positive market signal | BTC pump, accumulation patterns |
| `rebalance_suggestion` | Recommend portfolio rebalancing | Allocation drift detected |
| `migration_recommendation` | Suggest protocol migration | Severe protocol issues (Level 4) |

### 4.2 Trigger-to-Action Matrix

```python
TRIGGER_ACTION_MAP = {
    # Protocol Health - Sky
    "SKY-DEP-L1": {"action": "internal_only", "template": None},
    "SKY-DEP-L2": {"action": "protocol_alert", "template": "sky_caution"},
    "SKY-DEP-L3": {"action": "protocol_alert", "template": "sky_warning"},
    "SKY-DEP-L4": {"action": "migration_recommendation", "template": "sky_critical"},
    "SKY-TVL-L2": {"action": "protocol_alert", "template": "tvl_drop_caution"},
    "SKY-TVL-L3": {"action": "protocol_alert", "template": "tvl_drop_warning"},
    "SKY-BUF-L2": {"action": "protocol_alert", "template": "sky_buffer_low"},
    
    # Protocol Health - Sanctum
    "SAN-APY-L2": {"action": "performance_alert", "template": "apy_drop"},
    "SAN-TVL-L3": {"action": "protocol_alert", "template": "tvl_drop_warning"},
    "SAN-TVL-L4": {"action": "migration_recommendation", "template": "sanctum_critical"},
    
    # Protocol Health - JLP
    "JLP-UTL-L2": {"action": "protocol_alert", "template": "liquidity_stress"},
    "JLP-APY-L2": {"action": "performance_alert", "template": "apy_drop"},
    "JLP-TVL-L3": {"action": "protocol_alert", "template": "tvl_drop_warning"},
    
    # Market Conditions
    "MKT-BTC-L3": {"action": "crisis_template", "template": "market_volatility"},
    "MKT-BTC-L4": {"action": "crisis_template", "template": "market_crash"},
    "MKT-ETH-L3": {"action": "crisis_template", "template": "eth_volatility"},
    "MKT-SOL-L3": {"action": "crisis_template", "template": "sol_volatility"},
    "MKT-SOL-L4": {"action": "crisis_template", "template": "sol_crash"},
    "MKT-BTC-UP": {"action": "opportunity_insight", "template": "btc_rally"},
    "MKT-CAP-L3": {"action": "crisis_template", "template": "broad_market_crash"},
    
    # Estate & Whale
    "EST-MOV-INFO": {"action": "smart_money_insight", "template": "estate_movement"},
    "EST-MOV-L2": {"action": "smart_money_insight", "template": "significant_estate"},
    "EST-MOV-L3": {"action": "protocol_alert", "template": "major_liquidation"},
    "EST-MTGOX": {"action": "protocol_alert", "template": "mtgox_distribution"},
    "EST-FTX": {"action": "smart_money_insight", "template": "ftx_distribution"},
    "WHL-ACC-INFO": {"action": "smart_money_insight", "template": "whale_accumulation"},
    "WHL-DIST-L2": {"action": "smart_money_insight", "template": "whale_distribution"},
    
    # Macro
    "MAC-VIX-L2": {"action": "smart_money_insight", "template": "elevated_volatility"},
    "MAC-VIX-L3": {"action": "crisis_template", "template": "extreme_volatility"},
    "MAC-FED-INFO": {"action": "smart_money_insight", "template": "fed_decision"},
    "MAC-10Y-INFO": {"action": "smart_money_insight", "template": "treasury_move"},
    "MAC-STBL-L2": {"action": "protocol_alert", "template": "stablecoin_liquidity"},
}
```

### 4.3 Action Router Implementation

```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class RoutedAction:
    trigger_id: str
    action_type: str
    template_id: str
    affected_strategies: List[int]
    affected_users: List[str]  # User IDs
    channels: List[str]
    priority: str
    consolidation_group: Optional[str]
    metadata: Dict[str, Any]

class ActionRouter:
    """Routes triggers to appropriate actions and channels."""
    
    def __init__(self, action_map: dict, user_service):
        self.action_map = action_map
        self.user_service = user_service
    
    def route(self, trigger: TriggerResult) -> RoutedAction:
        """Route a trigger to an action."""
        
        action_config = self.action_map.get(trigger.trigger_id, {})
        
        # Get affected users
        affected_users = self._get_affected_users(trigger.affected_strategies)
        
        # Determine channels based on level
        channels = self._determine_channels(trigger.level)
        
        # Determine priority
        priority = self._level_to_priority(trigger.level)
        
        # Determine consolidation group
        consolidation_group = self._get_consolidation_group(trigger)
        
        return RoutedAction(
            trigger_id=trigger.trigger_id,
            action_type=action_config.get("action", "unknown"),
            template_id=action_config.get("template"),
            affected_strategies=trigger.affected_strategies,
            affected_users=affected_users,
            channels=channels,
            priority=priority,
            consolidation_group=consolidation_group,
            metadata=trigger.metadata
        )
    
    def _get_affected_users(self, strategy_ids: List[int]) -> List[str]:
        """Get all users subscribed to affected strategies."""
        users = set()
        for strategy_id in strategy_ids:
            strategy_users = self.user_service.get_users_by_strategy(strategy_id)
            users.update(strategy_users)
        return list(users)
    
    def _determine_channels(self, level: TriggerLevel) -> List[str]:
        """Determine notification channels based on alert level."""
        CHANNEL_MAP = {
            TriggerLevel.INFO: ["in_app"],
            TriggerLevel.WATCH: ["in_app"],
            TriggerLevel.CAUTION: ["in_app", "email"],
            TriggerLevel.WARNING: ["in_app", "email", "push"],
            TriggerLevel.CRITICAL: ["in_app", "email", "push", "sms"],
        }
        return CHANNEL_MAP.get(level, ["in_app"])
    
    def _level_to_priority(self, level: TriggerLevel) -> str:
        """Convert trigger level to priority."""
        PRIORITY_MAP = {
            TriggerLevel.INFO: "P3",
            TriggerLevel.WATCH: "P2",
            TriggerLevel.CAUTION: "P1",
            TriggerLevel.WARNING: "P0",
            TriggerLevel.CRITICAL: "P0",
        }
        return PRIORITY_MAP.get(level, "P2")
    
    def _get_consolidation_group(self, trigger: TriggerResult) -> Optional[str]:
        """Determine if trigger should be consolidated with others."""
        CONSOLIDATION_RULES = {
            "MKT-BTC-L3": "market_crash",
            "MKT-BTC-L4": "market_crash",
            "MKT-ETH-L3": "market_crash",
            "MKT-SOL-L3": "sol_ecosystem",
            "MKT-SOL-L4": "sol_ecosystem",
            "SKY-DEP-L2": "sky_protocol",
            "SKY-DEP-L3": "sky_protocol",
            "SKY-DEP-L4": "sky_protocol",
            "SKY-TVL-L2": "sky_protocol",
            "SKY-TVL-L3": "sky_protocol",
            "SAN-TVL-L3": "sol_ecosystem",
            "SAN-TVL-L4": "sol_ecosystem",
        }
        
        group = CONSOLIDATION_RULES.get(trigger.trigger_id)
        if group:
            date_str = trigger.timestamp.strftime("%Y-%m-%d")
            return f"{group}_{date_str}"
        return None
```

---

## 5. Rebalancing Engine

### 5.1 Rebalancing Thresholds by Strategy

| Strategy ID | Strategy Name | Risk Tier | Suggest Threshold | Force Threshold |
|-------------|---------------|-----------|-------------------|-----------------|
| 1 | Safe Harbor | Minimal | 5% | 10% |
| 2 | Beat Inflation | Low | 5% | 10% |
| 3 | Goal Keeper | Minimal | 5% | 10% |
| 4 | Steady Progress | Low-Medium | 7% | 15% |
| 5 | Patient Builder | Minimal | 5% | 10% |
| 6 | Balanced Builder | Medium | 7% | 15% |
| 7 | Steady Compounder | Minimal | 5% | 10% |
| 8 | Wealth Accelerator | High | 10% | 20% |
| 9 | Yield Maximizer | Low | 5% | 10% |
| 10 | Full Throttle | Very High | 10% | 25% |

### 5.2 Drift Calculation

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class DriftResult:
    strategy_id: int
    user_id: str
    max_drift_pct: float
    drift_by_allocation: Dict[str, float]
    action_required: str  # "none", "suggest", "strong_recommend"
    current_allocations: Dict[str, Dict[str, float]]
    target_allocations: Dict[str, Dict[str, float]]

REBALANCING_THRESHOLDS = {
    1: {"suggest": 5, "force": 10},
    2: {"suggest": 5, "force": 10},
    3: {"suggest": 5, "force": 10},
    4: {"suggest": 7, "force": 15},
    5: {"suggest": 5, "force": 10},
    6: {"suggest": 7, "force": 15},
    7: {"suggest": 5, "force": 10},
    8: {"suggest": 10, "force": 20},
    9: {"suggest": 5, "force": 10},
    10: {"suggest": 10, "force": 25},
}

def calculate_drift(
    strategy_id: int,
    user_id: str,
    current_allocations: Dict[str, Dict[str, float]],
    target_allocations: Dict[str, Dict[str, float]]
) -> DriftResult:
    """Calculate allocation drift from target."""
    
    drift_by_allocation = {}
    max_drift = 0.0
    
    for category in ["stable", "crypto"]:
        current_cat = current_allocations.get(category, {})
        target_cat = target_allocations.get(category, {})
        
        all_protocols = set(current_cat.keys()) | set(target_cat.keys())
        
        for protocol in all_protocols:
            current_pct = current_cat.get(protocol, 0)
            target_pct = target_cat.get(protocol, 0)
            drift = abs(current_pct - target_pct)
            
            drift_by_allocation[f"{category}.{protocol}"] = drift
            max_drift = max(max_drift, drift)
    
    # Determine action
    thresholds = REBALANCING_THRESHOLDS[strategy_id]
    if max_drift >= thresholds["force"]:
        action = "strong_recommend"
    elif max_drift >= thresholds["suggest"]:
        action = "suggest"
    else:
        action = "none"
    
    return DriftResult(
        strategy_id=strategy_id,
        user_id=user_id,
        max_drift_pct=max_drift,
        drift_by_allocation=drift_by_allocation,
        action_required=action,
        current_allocations=current_allocations,
        target_allocations=target_allocations
    )
```

### 5.3 Rebalancing Recommendation Generator

```python
@dataclass
class RebalanceRecommendation:
    recommendation_id: str
    timestamp: datetime.datetime
    user_id: str
    strategy_id: int
    recommendation_type: str  # "suggested", "strong"
    reason: str
    max_drift_pct: float
    current_allocations: Dict
    target_allocations: Dict
    estimated_gas_cost_usd: Optional[float]
    user_action_required: bool

def generate_rebalance_recommendation(drift: DriftResult) -> Optional[RebalanceRecommendation]:
    """Generate a rebalance recommendation if action required."""
    
    if drift.action_required == "none":
        return None
    
    return RebalanceRecommendation(
        recommendation_id=f"REB-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{drift.user_id[:8]}",
        timestamp=datetime.datetime.utcnow(),
        user_id=drift.user_id,
        strategy_id=drift.strategy_id,
        recommendation_type="strong" if drift.action_required == "strong_recommend" else "suggested",
        reason="allocation_drift",
        max_drift_pct=drift.max_drift_pct,
        current_allocations=drift.current_allocations,
        target_allocations=drift.target_allocations,
        estimated_gas_cost_usd=None,  # To be calculated by CTO
        user_action_required=True  # diBoaS NEVER auto-rebalances
    )
```

### 5.4 Critical Principle

**diBoaS NEVER automatically moves user funds.** All rebalancing is:
1. **Suggested** â€” User sees recommendation
2. **Requires explicit consent** â€” User must approve
3. **User-initiated** â€” User triggers the transaction

This aligns with the "Exit with Dignity" philosophy from Session 006.

---

## 6. Alert Consolidation

### 6.1 Why Consolidation Matters

When multiple related events occur (e.g., BTC, ETH, SOL all crash together), users should receive **one unified message**, not 10 separate alerts.

### 6.2 Consolidation Rules

```python
CONSOLIDATION_RULES = {
    "market_crash": {
        "root_cause": "broad_market_decline",
        "trigger_ids": ["MKT-BTC-L3", "MKT-BTC-L4", "MKT-ETH-L3", "MKT-SOL-L3", "MKT-CAP-L3"],
        "unified_template": "broad_market_crash_template",
        "max_window_minutes": 30
    },
    "sky_protocol": {
        "root_cause": "sky_protocol_stress",
        "trigger_ids": ["SKY-DEP-L2", "SKY-DEP-L3", "SKY-DEP-L4", "SKY-TVL-L2", "SKY-TVL-L3", "SKY-BUF-L2"],
        "unified_template": "sky_protocol_alert_template",
        "max_window_minutes": 60
    },
    "sol_ecosystem": {
        "root_cause": "solana_ecosystem_stress",
        "trigger_ids": ["MKT-SOL-L3", "MKT-SOL-L4", "SAN-TVL-L3", "SAN-TVL-L4", "SAN-APY-L2"],
        "unified_template": "sol_exposure_template",
        "max_window_minutes": 60
    }
}
```

### 6.3 Consolidation Engine

```python
from collections import defaultdict
from typing import List, Optional
import datetime

@dataclass
class ConsolidatedAlert:
    consolidation_id: str
    consolidation_group: str
    timestamp: datetime.datetime
    root_cause: str
    individual_triggers: List[TriggerResult]
    affected_strategies: List[int]
    highest_level: TriggerLevel
    priority: str
    unified_template: str

class AlertConsolidator:
    """Consolidates related alerts into unified communications."""
    
    def __init__(self, rules: dict):
        self.rules = rules
        self.pending_alerts = defaultdict(list)  # group -> [alerts]
        self.last_flush = {}
    
    def add_alert(self, routed_action: RoutedAction) -> Optional[ConsolidatedAlert]:
        """Add alert to consolidation buffer, return if should flush."""
        
        group = routed_action.consolidation_group
        
        if not group:
            # No consolidation, return as single alert
            return self._single_to_consolidated(routed_action)
        
        # Add to pending
        self.pending_alerts[group].append(routed_action)
        
        # Check if should flush (window exceeded or critical alert)
        rule = self._get_rule_for_group(group)
        window_minutes = rule.get("max_window_minutes", 30)
        
        first_alert_time = self.pending_alerts[group][0].metadata.get("timestamp", datetime.datetime.utcnow())
        elapsed = (datetime.datetime.utcnow() - first_alert_time).total_seconds() / 60
        
        # Flush if window exceeded or critical priority
        if elapsed >= window_minutes or routed_action.priority == "P0":
            return self.flush_group(group)
        
        return None
    
    def flush_group(self, group: str) -> Optional[ConsolidatedAlert]:
        """Flush a consolidation group into a single alert."""
        
        alerts = self.pending_alerts.pop(group, [])
        
        if not alerts:
            return None
        
        rule = self._get_rule_for_group(group)
        
        # Merge affected strategies
        all_strategies = set()
        for alert in alerts:
            all_strategies.update(alert.affected_strategies)
        
        # Find highest level
        highest_level = max(
            TriggerLevel[a.priority.replace("P", "").replace("0", "CRITICAL").replace("1", "WARNING").replace("2", "CAUTION").replace("3", "INFO")]
            for a in alerts
        )
        
        # Determine priority (highest among all)
        priorities = [a.priority for a in alerts]
        highest_priority = min(priorities)  # P0 is highest
        
        return ConsolidatedAlert(
            consolidation_id=f"CONS-{group}-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            consolidation_group=group,
            timestamp=datetime.datetime.utcnow(),
            root_cause=rule.get("root_cause", "multiple_events"),
            individual_triggers=[a.trigger_id for a in alerts],
            affected_strategies=list(all_strategies),
            highest_level=highest_level,
            priority=highest_priority,
            unified_template=rule.get("unified_template")
        )
    
    def _get_rule_for_group(self, group: str) -> dict:
        """Get consolidation rule for a group."""
        base_group = group.rsplit("_", 1)[0]  # Remove date suffix
        return self.rules.get(base_group, {})
    
    def _single_to_consolidated(self, action: RoutedAction) -> ConsolidatedAlert:
        """Convert single action to consolidated format for consistency."""
        return ConsolidatedAlert(
            consolidation_id=f"SINGLE-{action.trigger_id}-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            consolidation_group=None,
            timestamp=datetime.datetime.utcnow(),
            root_cause=action.action_type,
            individual_triggers=[action.trigger_id],
            affected_strategies=action.affected_strategies,
            highest_level=TriggerLevel.WARNING,  # Default
            priority=action.priority,
            unified_template=action.template_id
        )
```

---

## 7. Priority & Escalation

### 7.1 Priority Levels

| Priority | Name | Description | Max Delay | Channels |
|----------|------|-------------|-----------|----------|
| P0 | Critical | Requires immediate action | 15 min | All (including SMS) |
| P1 | High | Important information | 1 hour | Email, Push, In-app |
| P2 | Medium | Informational | 4 hours | Email, In-app |
| P3 | Low | Educational/context | Next newsletter | In-app, Newsletter |

### 7.2 Escalation Rules

```python
ESCALATION_RULES = {
    "P0": {
        "initial_timeout_minutes": 30,
        "escalation_path": ["strategy_board", "ceo_board"],
        "max_escalations": 2,
        "auto_actions": ["pause_deposits"]  # Only for Level 4 protocol issues
    },
    "P1": {
        "initial_timeout_minutes": 120,
        "escalation_path": ["strategy_board"],
        "max_escalations": 1,
        "auto_actions": []
    },
    "P2": {
        "initial_timeout_minutes": 480,
        "escalation_path": [],
        "max_escalations": 0,
        "auto_actions": []
    },
    "P3": {
        "initial_timeout_minutes": None,  # No timeout
        "escalation_path": [],
        "max_escalations": 0,
        "auto_actions": []
    }
}
```

### 7.3 Escalation Handler

```python
@dataclass
class Escalation:
    alert_id: str
    escalation_level: int
    escalated_to: str
    timestamp: datetime.datetime
    reason: str

class EscalationHandler:
    """Handles alert escalation when not acknowledged."""
    
    def __init__(self, rules: dict, notification_service):
        self.rules = rules
        self.notification_service = notification_service
        self.pending_acks = {}  # alert_id -> (alert, sent_time)
    
    def register_alert(self, alert: ConsolidatedAlert):
        """Register alert for acknowledgment tracking."""
        self.pending_acks[alert.consolidation_id] = {
            "alert": alert,
            "sent_time": datetime.datetime.utcnow(),
            "escalation_level": 0
        }
    
    def check_escalations(self) -> List[Escalation]:
        """Check for alerts needing escalation."""
        escalations = []
        now = datetime.datetime.utcnow()
        
        for alert_id, data in list(self.pending_acks.items()):
            alert = data["alert"]
            sent_time = data["sent_time"]
            current_level = data["escalation_level"]
            
            rule = self.rules.get(alert.priority, {})
            timeout_minutes = rule.get("initial_timeout_minutes")
            
            if not timeout_minutes:
                continue
            
            elapsed = (now - sent_time).total_seconds() / 60
            
            if elapsed >= timeout_minutes:
                escalation_path = rule.get("escalation_path", [])
                max_escalations = rule.get("max_escalations", 0)
                
                if current_level < max_escalations and current_level < len(escalation_path):
                    escalate_to = escalation_path[current_level]
                    
                    escalation = Escalation(
                        alert_id=alert_id,
                        escalation_level=current_level + 1,
                        escalated_to=escalate_to,
                        timestamp=now,
                        reason=f"No acknowledgment after {timeout_minutes} minutes"
                    )
                    escalations.append(escalation)
                    
                    # Update tracking
                    self.pending_acks[alert_id]["escalation_level"] += 1
                    self.pending_acks[alert_id]["sent_time"] = now
                    
                    # Notify escalation target
                    self.notification_service.notify_board(
                        escalate_to,
                        f"ESCALATION: Alert {alert_id} requires attention"
                    )
        
        return escalations
    
    def acknowledge(self, alert_id: str, acked_by: str):
        """Mark alert as acknowledged."""
        if alert_id in self.pending_acks:
            del self.pending_acks[alert_id]
            # Log acknowledgment for audit
```

---

## 8. Cross-Strategy Correlation

### 8.1 Strategy-Protocol Dependency Map

```python
STRATEGY_PROTOCOL_MAP = {
    # Stable-heavy strategies (Sky exposure)
    1: {"primary": ["sky_ssr"], "fallback": ["aave_v3", "compound_v3"]},
    3: {"primary": ["sky_ssr"], "fallback": ["aave_v3", "compound_v3"]},
    5: {"primary": ["sky_ssr"], "fallback": ["aave_v3", "compound_v3"]},
    7: {"primary": ["sky_ssr"], "fallback": ["aave_v3", "compound_v3"]},
    9: {"primary": ["sky_ssr"], "fallback": ["aave_v3", "compound_v3"]},
    
    # Crypto-exposure strategies (Solana exposure)
    2: {"primary": ["sky_ssr", "sanctum_inf"], "fallback": ["aave_v3", "jito"]},
    4: {"primary": ["sky_ssr", "sanctum_inf"], "fallback": ["aave_v3", "jito"]},
    6: {"primary": ["sky_ssr", "sanctum_inf", "jlp"], "fallback": ["aave_v3", "jito"]},
    8: {"primary": ["sky_ssr", "sanctum_inf", "jlp"], "fallback": ["aave_v3", "jito"]},
    10: {"primary": ["sky_ssr", "sanctum_inf", "jlp", "jito"], "fallback": ["aave_v3"]},
}
```

### 8.2 Correlation Impact Analysis

```python
def analyze_cross_strategy_impact(trigger: TriggerResult) -> Dict[str, List[int]]:
    """Analyze how a trigger affects strategies through correlations."""
    
    impact = {
        "direct": [],      # Directly affected
        "correlated": [],  # Affected through correlation
        "secondary": []    # Potentially affected
    }
    
    # Direct impact
    impact["direct"] = trigger.affected_strategies.copy()
    
    # Correlation analysis
    if trigger.trigger_id.startswith("MKT-BTC"):
        # BTC affects all crypto-exposed strategies
        impact["correlated"] = [s for s in range(1, 11) if s not in impact["direct"]]
    
    elif trigger.trigger_id.startswith("SKY"):
        # Sky affects all stable-heavy strategies
        stable_heavy = [1, 3, 5, 7, 9]
        impact["correlated"] = [s for s in stable_heavy if s not in impact["direct"]]
    
    elif trigger.trigger_id.startswith("MKT-SOL") or trigger.trigger_id.startswith("SAN"):
        # SOL/Sanctum affects all SOL-exposed strategies
        sol_exposed = [2, 4, 6, 8, 10]
        impact["correlated"] = [s for s in sol_exposed if s not in impact["direct"]]
    
    return impact
```

### 8.3 Simultaneous Alert Coordination

When related events affect multiple strategies, coordinate the messaging:

```python
def coordinate_multi_strategy_alert(
    consolidated: ConsolidatedAlert,
    impact_analysis: Dict[str, List[int]]
) -> Dict:
    """Coordinate alert messaging across affected strategies."""
    
    all_affected = set(
        impact_analysis["direct"] + 
        impact_analysis["correlated"] + 
        impact_analysis["secondary"]
    )
    
    # Group users by their primary strategy
    user_groups = defaultdict(list)
    for strategy_id in all_affected:
        users = get_users_by_strategy(strategy_id)
        for user in users:
            user_groups[strategy_id].append(user)
    
    # Determine message variant by impact type
    message_variants = {}
    for strategy_id in all_affected:
        if strategy_id in impact_analysis["direct"]:
            message_variants[strategy_id] = "direct_impact"
        elif strategy_id in impact_analysis["correlated"]:
            message_variants[strategy_id] = "correlated_impact"
        else:
            message_variants[strategy_id] = "context_only"
    
    return {
        "consolidated_alert": consolidated,
        "all_affected_strategies": list(all_affected),
        "user_groups": dict(user_groups),
        "message_variants": message_variants
    }
```

---

## 9. Configuration Files

### 9.1 Master Trigger Configuration

```yaml
# config/strategy_triggers.yaml

triggers:
  protocol_health:
    sky:
      depeg:
        - level: 1
          threshold_pct: 0.5
          action: internal_only
        - level: 2
          threshold_pct: 1.0
          action: protocol_alert
          template: sky_caution
        - level: 3
          threshold_pct: 2.0
          action: protocol_alert
          template: sky_warning
        - level: 4
          threshold_pct: 5.0
          action: migration_recommendation
          template: sky_critical
      tvl_drop:
        - level: 2
          threshold_pct: 10
          period_hours: 24
          action: protocol_alert
        - level: 3
          threshold_pct: 25
          period_hours: 24
          action: protocol_alert
      check_frequency_minutes: 5
      affected_strategies: [1, 3, 5, 7, 9]
    
    sanctum:
      apy_drop:
        - level: 2
          threshold_pct: 50
          vs: 7d_avg
          action: performance_alert
      tvl_drop:
        - level: 3
          threshold_pct: 20
          period_hours: 24
          action: protocol_alert
        - level: 4
          threshold_pct: 50
          period_hours: 24
          action: migration_recommendation
      check_frequency_minutes: 15
      affected_strategies: [2, 4, 6, 8, 10]
    
    jlp:
      utilization:
        - level: 2
          threshold_pct: 90
          action: protocol_alert
          template: liquidity_stress
      apy_drop:
        - level: 2
          threshold_pct: 40
          vs: 7d_avg
          action: performance_alert
      check_frequency_minutes: 15
      affected_strategies: [6, 8, 10]

  market_conditions:
    btc:
      drop:
        - level: 3
          threshold_pct: 10
          period_hours: 24
          affected: [3, 4, 5, 6, 7, 8, 9, 10]
        - level: 4
          threshold_pct: 20
          period_hours: 24
          affected: all
      pump:
        - level: info
          threshold_pct: 15
          period_hours: 24
          affected: [3, 4, 6, 8, 10]
      check_frequency_minutes: 5
    
    eth:
      drop:
        - level: 3
          threshold_pct: 15
          period_hours: 24
          affected: [2, 4, 6, 8, 10]
      check_frequency_minutes: 5
    
    sol:
      drop:
        - level: 3
          threshold_pct: 20
          period_hours: 24
          affected: [2, 4, 6, 8, 10]
        - level: 4
          threshold_pct: 30
          period_hours: 24
          affected: [2, 4, 6, 8, 10]
      check_frequency_minutes: 5

  estate_whale:
    estate_movement:
      - level: info
        threshold_usd: 10_000_000
        action: smart_money_insight
      - level: 2
        threshold_usd: 50_000_000
        action: smart_money_insight
      - level: 3
        threshold_usd: 100_000_000
        action: protocol_alert
    check_frequency_minutes: 60
    affected_strategies: all

  macro:
    vix:
      - level: 2
        threshold_value: 30
        action: smart_money_insight
      - level: 3
        threshold_value: 40
        action: crisis_template
    check_frequency_minutes: 15
    affected_strategies: all

rebalancing:
  thresholds:
    1: {suggest: 5, force: 10, risk_tier: Minimal}
    2: {suggest: 5, force: 10, risk_tier: Low}
    3: {suggest: 5, force: 10, risk_tier: Minimal}
    4: {suggest: 7, force: 15, risk_tier: Low-Medium}
    5: {suggest: 5, force: 10, risk_tier: Minimal}
    6: {suggest: 7, force: 15, risk_tier: Medium}
    7: {suggest: 5, force: 10, risk_tier: Minimal}
    8: {suggest: 10, force: 20, risk_tier: High}
    9: {suggest: 5, force: 10, risk_tier: Low}
    10: {suggest: 10, force: 25, risk_tier: Very High}
  
  check_frequency: daily
  auto_rebalance: false  # NEVER auto-rebalance

consolidation:
  market_crash:
    triggers: [MKT-BTC-L3, MKT-BTC-L4, MKT-ETH-L3, MKT-SOL-L3, MKT-CAP-L3]
    template: broad_market_crash_template
    window_minutes: 30
  
  sky_protocol:
    triggers: [SKY-DEP-L2, SKY-DEP-L3, SKY-DEP-L4, SKY-TVL-L2, SKY-TVL-L3]
    template: sky_protocol_alert_template
    window_minutes: 60
  
  sol_ecosystem:
    triggers: [MKT-SOL-L3, MKT-SOL-L4, SAN-TVL-L3, SAN-TVL-L4]
    template: sol_exposure_template
    window_minutes: 60

priority:
  P0:
    timeout_minutes: 30
    escalation_path: [strategy_board, ceo_board]
    channels: [in_app, email, push, sms]
  P1:
    timeout_minutes: 120
    escalation_path: [strategy_board]
    channels: [in_app, email, push]
  P2:
    timeout_minutes: 480
    escalation_path: []
    channels: [in_app, email]
  P3:
    timeout_minutes: null
    escalation_path: []
    channels: [in_app]
```

---

## 10. API Specifications

### 10.1 Intelligence Engine API

```yaml
openapi: 3.0.0
info:
  title: Strategy Board Intelligence API
  version: 1.0.0
  description: Layer 4 Intelligence Engine for diboas-analytics

paths:
  /api/intelligence/evaluate:
    post:
      summary: Evaluate all triggers against current data
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EvaluationInput'
      responses:
        200:
          description: Evaluation results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EvaluationResult'

  /api/intelligence/alerts:
    get:
      summary: Get active alerts
      parameters:
        - name: strategy_id
          in: query
          schema:
            type: integer
        - name: priority
          in: query
          schema:
            type: string
            enum: [P0, P1, P2, P3]
        - name: status
          in: query
          schema:
            type: string
            enum: [active, acknowledged, resolved]
      responses:
        200:
          description: List of alerts
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Alert'

  /api/intelligence/alerts/{alert_id}/acknowledge:
    post:
      summary: Acknowledge an alert
      parameters:
        - name: alert_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                acknowledged_by:
                  type: string
                notes:
                  type: string
      responses:
        200:
          description: Alert acknowledged

  /api/intelligence/rebalance/check:
    post:
      summary: Check if rebalancing needed for a user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: string
                strategy_id:
                  type: integer
                current_allocations:
                  $ref: '#/components/schemas/Allocations'
      responses:
        200:
          description: Rebalancing recommendation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RebalanceRecommendation'

  /api/intelligence/triggers/config:
    get:
      summary: Get current trigger configuration
      responses:
        200:
          description: Trigger configuration
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TriggerConfig'
    
    put:
      summary: Update trigger configuration
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TriggerConfig'
      responses:
        200:
          description: Configuration updated

components:
  schemas:
    EvaluationInput:
      type: object
      properties:
        protocol_health:
          type: object
        prices:
          type: object
        wallet_events:
          type: array
        macro:
          type: object

    EvaluationResult:
      type: object
      properties:
        triggered_alerts:
          type: array
          items:
            $ref: '#/components/schemas/Alert'
        rebalance_recommendations:
          type: array
          items:
            $ref: '#/components/schemas/RebalanceRecommendation'
        timestamp:
          type: string
          format: date-time

    Alert:
      type: object
      properties:
        alert_id:
          type: string
        trigger_id:
          type: string
        level:
          type: integer
        priority:
          type: string
        affected_strategies:
          type: array
          items:
            type: integer
        action_type:
          type: string
        template_id:
          type: string
        consolidation_group:
          type: string
        timestamp:
          type: string
          format: date-time

    RebalanceRecommendation:
      type: object
      properties:
        recommendation_id:
          type: string
        user_id:
          type: string
        strategy_id:
          type: integer
        recommendation_type:
          type: string
          enum: [suggested, strong]
        max_drift_pct:
          type: number
        current_allocations:
          $ref: '#/components/schemas/Allocations'
        target_allocations:
          $ref: '#/components/schemas/Allocations'

    Allocations:
      type: object
      properties:
        stable:
          type: object
          additionalProperties:
            type: number
        crypto:
          type: object
          additionalProperties:
            type: number

    TriggerConfig:
      type: object
      description: Full trigger configuration object
```

---

## 11. Database Schema

### 11.1 Alerts Table

```sql
CREATE TABLE intelligence_alerts (
    alert_id VARCHAR(64) PRIMARY KEY,
    trigger_id VARCHAR(32) NOT NULL,
    consolidation_id VARCHAR(64),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    level INTEGER NOT NULL,
    level_name VARCHAR(16) NOT NULL,
    priority VARCHAR(4) NOT NULL,
    category VARCHAR(32) NOT NULL,
    action_type VARCHAR(32) NOT NULL,
    template_id VARCHAR(64),
    affected_strategies JSONB NOT NULL,
    actual_value DECIMAL(20, 8),
    threshold DECIMAL(20, 8),
    metadata JSONB,
    status VARCHAR(16) NOT NULL DEFAULT 'active',
    acknowledged_at TIMESTAMP,
    acknowledged_by VARCHAR(64),
    resolved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_alerts_status (status),
    INDEX idx_alerts_priority (priority),
    INDEX idx_alerts_timestamp (timestamp),
    INDEX idx_alerts_consolidation (consolidation_id)
);
```

### 11.2 Rebalance Recommendations Table

```sql
CREATE TABLE rebalance_recommendations (
    recommendation_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    strategy_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recommendation_type VARCHAR(16) NOT NULL,
    reason VARCHAR(32) NOT NULL,
    max_drift_pct DECIMAL(8, 4) NOT NULL,
    current_allocations JSONB NOT NULL,
    target_allocations JSONB NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'pending',
    user_action VARCHAR(16),
    actioned_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_rebalance_user (user_id),
    INDEX idx_rebalance_strategy (strategy_id),
    INDEX idx_rebalance_status (status)
);
```

### 11.3 Escalations Table

```sql
CREATE TABLE alert_escalations (
    escalation_id SERIAL PRIMARY KEY,
    alert_id VARCHAR(64) NOT NULL REFERENCES intelligence_alerts(alert_id),
    escalation_level INTEGER NOT NULL,
    escalated_to VARCHAR(32) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    acknowledged_at TIMESTAMP,
    acknowledged_by VARCHAR(64),
    
    INDEX idx_escalations_alert (alert_id),
    INDEX idx_escalations_timestamp (timestamp)
);
```

### 11.4 Trigger Audit Log

```sql
CREATE TABLE trigger_audit_log (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    trigger_id VARCHAR(32) NOT NULL,
    evaluation_result BOOLEAN NOT NULL,
    actual_value DECIMAL(20, 8),
    threshold DECIMAL(20, 8),
    input_data JSONB,
    output_action JSONB,
    processing_time_ms INTEGER,
    
    INDEX idx_audit_timestamp (timestamp),
    INDEX idx_audit_trigger (trigger_id)
);
```

---

## 12. Integration Points

### 12.1 Upstream (Inputs)

| Source | Interface | Format | Frequency |
|--------|-----------|--------|-----------|
| QR Board Analytics | Internal API | JSON | On calculation |
| Protocol Health Collector | CSV/JSON | JSON | 5-15 min |
| Price Feed Collector | API | JSON | 5 min |
| Estate Wallet Collector | API | JSON | 60 min |
| Whale Wallet Collector | API | JSON | 60 min |
| Macro Collector | API | JSON | 15-60 min |

### 12.2 Downstream (Outputs)

| Target | Interface | Format | Delivery |
|--------|-----------|--------|----------|
| Adelaide Newsletter | Internal API | JSON | Real-time + batch |
| User Notification Service | Internal API | JSON | Priority-based |
| Strategy Board Dashboard | WebSocket | JSON | Real-time |
| Audit Log | Database | SQL | Every event |
| Slack Alerts (Internal) | Webhook | JSON | P0/P1 only |

### 12.3 Integration with Adelaide

The Intelligence Engine outputs are consumed by Adelaide for user communication:

```python
# Adelaide integration point
def send_to_adelaide(consolidated_alert: ConsolidatedAlert):
    """Send alert to Adelaide for user communication."""
    
    payload = {
        "alert_id": consolidated_alert.consolidation_id,
        "template_id": consolidated_alert.unified_template,
        "priority": consolidated_alert.priority,
        "affected_strategies": consolidated_alert.affected_strategies,
        "variables": {
            "root_cause": consolidated_alert.root_cause,
            "trigger_count": len(consolidated_alert.individual_triggers),
            "timestamp": consolidated_alert.timestamp.isoformat()
        },
        "routing": {
            "channels": get_channels_for_priority(consolidated_alert.priority),
            "user_segment": f"strategies_{','.join(map(str, consolidated_alert.affected_strategies))}"
        }
    }
    
    adelaide_client.enqueue_alert(payload)
```

---

## 13. Testing Requirements

### 13.1 Unit Tests

| Test Category | Test Cases |
|---------------|------------|
| Trigger Evaluation | Each trigger type with boundary values |
| Drift Calculation | Correct drift for various allocation scenarios |
| Action Routing | Correct template selection for each trigger |
| Consolidation | Correct grouping and timing |
| Priority Assignment | Correct priority for each level |

### 13.2 Integration Tests

| Test Scenario | Expected Behavior |
|---------------|-------------------|
| BTC -12% drop | MKT-BTC-L3 triggered, strategies 3-10 affected, P0 crisis template |
| USDS 1.5% depeg | SKY-DEP-L2 triggered, strategies 1,3,5,7,9 affected, P1 protocol alert |
| Multi-event crash | BTC + ETH + SOL all down â†’ single consolidated alert |
| 8% drift on Strategy 6 | Suggest rebalance (threshold is 7%) |
| P0 no ack for 35 min | Escalation to strategy_board |

### 13.3 Test Data

```python
# Test fixtures
TEST_SCENARIOS = {
    "btc_crash": {
        "prices": {
            "BTC": {"price": 38000, "change_24h_pct": -15.5}
        },
        "expected_triggers": ["MKT-BTC-L3"],
        "expected_priority": "P0"
    },
    "usds_minor_depeg": {
        "protocol_health": {
            "sky_ssr": {"usds_peg": 0.994}
        },
        "expected_triggers": ["SKY-DEP-L1"],
        "expected_priority": None  # Internal only
    },
    "broad_market_crash": {
        "prices": {
            "BTC": {"price": 35000, "change_24h_pct": -22.0},
            "ETH": {"price": 1800, "change_24h_pct": -18.0},
            "SOL": {"price": 65, "change_24h_pct": -25.0}
        },
        "expected_triggers": ["MKT-BTC-L4", "MKT-ETH-L3", "MKT-SOL-L3"],
        "expected_consolidation": "market_crash"
    }
}
```

---

## Appendix A: Strategy Reference

| ID | Name | Risk Tier | Sky Exposure | Crypto Exposure |
|----|------|-----------|--------------|-----------------|
| 1 | Safe Harbor | Minimal | 100% | 0% |
| 2 | Beat Inflation | Low | 70% | 30% |
| 3 | Goal Keeper | Minimal | 100% | 0% |
| 4 | Steady Progress | Low-Medium | 70% | 30% |
| 5 | Patient Builder | Minimal | 100% | 0% |
| 6 | Balanced Builder | Medium | 50% | 50% |
| 7 | Steady Compounder | Minimal | 100% | 0% |
| 8 | Wealth Accelerator | High | 30% | 70% |
| 9 | Yield Maximizer | Low | 100% | 0% |
| 10 | Full Throttle | Very High | 20% | 80% |

---

## Appendix B: Related Documents

| Document | Purpose | Location |
|----------|---------|----------|
| Strategy Board Operations Manual | Complete operations spec | `/mnt/project/strategy_board_operations_manual.md` |
| Strategies v2.1 | Current strategy definitions | `/mnt/project/strategies_v2_1.json` |
| QR Board Handoff | Analytics engine specs | QR Board deliverable |
| Rakia Handoff | Data collection specs | Rakia deliverable |
| Adelaide System | Presentation layer | `/mnt/project/diboas-analytics-v3-adelaide-system.md` |

---

**Document End**

*Strategy Board â€” Ready for CTO Board Implementation*
