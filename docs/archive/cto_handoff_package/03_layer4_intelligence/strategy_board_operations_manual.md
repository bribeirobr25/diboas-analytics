# Strategy Board Operations Manual
## Technical Specification for diboas-analytics Automation

**Document Version:** 1.0  
**Date:** January 19, 2026  
**Prepared by:** Strategy Board  
**Purpose:** Enable CTO Board to implement automated strategy management in diboas-analytics  
**Status:** Ready for Implementation

---

## Table of Contents

1. [Overview](#1-overview)
2. [Strategy Lifecycle Management](#2-strategy-lifecycle-management)
3. [Protocol Management](#3-protocol-management)
4. [Allocation Rules Engine](#4-allocation-rules-engine)
5. [Monitoring System](#5-monitoring-system)
6. [Alert System](#6-alert-system)
7. [Validation Framework](#7-validation-framework)
8. [Contingency Automation](#8-contingency-automation)
9. [APY Range Management](#9-apy-range-management)
10. [Data Dependencies](#10-data-dependencies)
11. [Decision Workflows](#11-decision-workflows)
12. [Reporting Requirements](#12-reporting-requirements)
13. [API Specifications](#13-api-specifications)
14. [Database Schema](#14-database-schema)

---

## 1. Overview

### 1.1 Purpose

This document specifies all Strategy Board operations that should be automated in the diboas-analytics application. It covers the complete lifecycle of investment strategies from creation to retirement.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Strategy CRUD operations | User interface design |
| Allocation calculations | Payment processing |
| Protocol health monitoring | Wallet management |
| Alert generation | On-chain execution |
| Validation rules | Customer support |
| Contingency triggers | Marketing content |
| Reporting | Legal document generation |

### 1.3 System Architecture Context

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    diboas-analytics v3                          â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”             â”‚
â”‚  â”‚   Data      â”‚  â”‚  Strategy   â”‚  â”‚   Alert     â”‚             â”‚
â”‚  â”‚  Collector  â”‚â”€â”€â”‚   Engine    â”‚â”€â”€â”‚   System    â”‚             â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜             â”‚
â”‚         â”‚               â”‚               â”‚                       â”‚
â”‚         â–¼               â–¼               â–¼                       â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”           â”‚
â”‚  â”‚              Strategy Board Module               â”‚           â”‚
â”‚  â”‚  â€¢ Lifecycle Manager                            â”‚           â”‚
â”‚  â”‚  â€¢ Allocation Engine                            â”‚           â”‚
â”‚  â”‚  â€¢ Monitoring Service                           â”‚           â”‚
â”‚  â”‚  â€¢ Validation Service                           â”‚           â”‚
â”‚  â”‚  â€¢ Contingency Handler                          â”‚           â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜           â”‚
â”‚                          â”‚                                      â”‚
â”‚                          â–¼                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”           â”‚
â”‚  â”‚                  Data Lake                       â”‚           â”‚
â”‚  â”‚  â€¢ strategies.json                              â”‚           â”‚
â”‚  â”‚  â€¢ protocols.json                               â”‚           â”‚
â”‚  â”‚  â€¢ alerts.json                                  â”‚           â”‚
â”‚  â”‚  â€¢ contingency_plans.json                       â”‚           â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜           â”‚
â”‚                                                                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. Strategy Lifecycle Management

### 2.1 Strategy States

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  DRAFT   â”‚â”€â”€â”€â”€â–¶â”‚  REVIEW  â”‚â”€â”€â”€â”€â–¶â”‚  ACTIVE  â”‚â”€â”€â”€â”€â–¶â”‚ RETIRED  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                      â”‚                 â”‚
                      â”‚                 â–¼
                      â”‚           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                      â”‚           â”‚  PAUSED  â”‚
                      â”‚           â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                      â”‚                 â”‚
                      â–¼                 â”‚
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”            â”‚
                â”‚ REJECTED â”‚â—€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 2.2 State Definitions

| State | Description | Allowed Transitions | User Visibility |
|-------|-------------|---------------------|-----------------|
| `DRAFT` | Strategy being designed | â†’ REVIEW | Hidden |
| `REVIEW` | Awaiting QR Board validation | â†’ ACTIVE, â†’ REJECTED | Hidden |
| `ACTIVE` | Available to users | â†’ PAUSED, â†’ RETIRED | Visible |
| `PAUSED` | Temporarily unavailable | â†’ ACTIVE, â†’ RETIRED | Visible (labeled) |
| `RETIRED` | Permanently discontinued | None (terminal) | Hidden (legacy users only) |
| `REJECTED` | Failed validation | â†’ DRAFT | Hidden |

### 2.3 State Transition Rules

```python
# Strategy State Machine
class StrategyState(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    ACTIVE = "active"
    PAUSED = "paused"
    RETIRED = "retired"
    REJECTED = "rejected"

VALID_TRANSITIONS = {
    StrategyState.DRAFT: [StrategyState.REVIEW],
    StrategyState.REVIEW: [StrategyState.ACTIVE, StrategyState.REJECTED],
    StrategyState.ACTIVE: [StrategyState.PAUSED, StrategyState.RETIRED],
    StrategyState.PAUSED: [StrategyState.ACTIVE, StrategyState.RETIRED],
    StrategyState.RETIRED: [],  # Terminal state
    StrategyState.REJECTED: [StrategyState.DRAFT],
}

def can_transition(current: StrategyState, target: StrategyState) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])
```

### 2.4 Lifecycle Operations

#### 2.4.1 CREATE Strategy

**Trigger:** Manual (Strategy Board decision)

**Input Schema:**
```json
{
  "id": "integer (auto-increment)",
  "name": "string (unique, 3-50 chars)",
  "goal": "enum: Emergency Fund | Beat Inflation | Short-Term | Medium-Term | Long-Term | Wealth Building",
  "crypto_pct": "integer (0-100)",
  "risk_tier": "enum: Minimal | Low | Low-Medium | Medium | High | Very High",
  "target_apy_range": "string (format: 'X-Y%')",
  "target_user": "string (persona reference)",
  "allocations": {
    "stable": {"protocol_id": "decimal (0-1)"},
    "crypto": {"protocol_id": "decimal (0-1)"}
  },
  "created_by": "string (board reference)",
  "created_at": "datetime"
}
```

**Validation Rules:**
```python
def validate_new_strategy(strategy: dict) -> ValidationResult:
    errors = []
    
    # Rule 1: Allocations must sum to 100%
    total = sum(strategy["allocations"]["stable"].values()) + \
            sum(strategy["allocations"]["crypto"].values())
    if abs(total - 1.0) > 0.001:
        errors.append("Allocations must sum to 100%")
    
    # Rule 2: crypto_pct must match crypto allocations
    crypto_sum = sum(strategy["allocations"]["crypto"].values())
    if abs(crypto_sum - strategy["crypto_pct"] / 100) > 0.001:
        errors.append("crypto_pct must match crypto allocations sum")
    
    # Rule 3: All protocols must be whitelisted
    all_protocols = list(strategy["allocations"]["stable"].keys()) + \
                   list(strategy["allocations"]["crypto"].keys())
    for protocol in all_protocols:
        if not is_protocol_whitelisted(protocol):
            errors.append(f"Protocol {protocol} is not whitelisted")
    
    # Rule 4: Name must be unique
    if strategy_name_exists(strategy["name"]):
        errors.append("Strategy name already exists")
    
    # Rule 5: Risk tier must match crypto exposure
    if not validate_risk_tier(strategy["risk_tier"], strategy["crypto_pct"]):
        errors.append("Risk tier inconsistent with crypto exposure")
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

**Risk Tier Mapping:**
```python
RISK_TIER_RULES = {
    "Minimal": {"crypto_pct_max": 0},
    "Low": {"crypto_pct_max": 35},
    "Low-Medium": {"crypto_pct_max": 50},
    "Medium": {"crypto_pct_max": 60},
    "High": {"crypto_pct_max": 80},
    "Very High": {"crypto_pct_max": 100},
}

def validate_risk_tier(tier: str, crypto_pct: int) -> bool:
    max_allowed = RISK_TIER_RULES.get(tier, {}).get("crypto_pct_max", 0)
    return crypto_pct <= max_allowed
```

#### 2.4.2 UPDATE Strategy

**Trigger:** Manual (Strategy Board decision) OR Automated (rebalancing rules)

**Update Types:**

| Type | Requires QR Validation | User Notification |
|------|------------------------|-------------------|
| Allocation change (>5%) | Yes | Yes |
| Allocation change (â‰¤5%) | No | No |
| APY range update | Yes | Yes |
| Protocol swap (same type) | Yes | Yes |
| Protocol addition | Yes | Yes |
| Protocol removal | Yes | Yes |
| Metadata only | No | No |

**Update Workflow:**
```python
def update_strategy(strategy_id: int, changes: dict) -> UpdateResult:
    current = get_strategy(strategy_id)
    
    # Determine if QR validation needed
    needs_validation = False
    
    if "allocations" in changes:
        diff = calculate_allocation_diff(current["allocations"], changes["allocations"])
        if diff > 0.05:  # >5% change
            needs_validation = True
    
    if "target_apy_range" in changes:
        needs_validation = True
    
    if any(key in changes for key in ["add_protocol", "remove_protocol", "swap_protocol"]):
        needs_validation = True
    
    if needs_validation:
        # Move to REVIEW state
        set_strategy_state(strategy_id, StrategyState.REVIEW)
        create_qr_validation_request(strategy_id, changes)
        return UpdateResult(status="pending_validation", validation_id=...)
    else:
        # Apply directly
        apply_strategy_changes(strategy_id, changes)
        return UpdateResult(status="applied")
```

#### 2.4.3 PAUSE Strategy

**Trigger:** Manual OR Automated (contingency trigger)

**Pause Reasons:**
```python
class PauseReason(Enum):
    PROTOCOL_INCIDENT = "protocol_incident"      # Security issue
    EXTREME_VOLATILITY = "extreme_volatility"    # Market conditions
    LIQUIDITY_CRISIS = "liquidity_crisis"        # Can't execute
    REGULATORY_CONCERN = "regulatory_concern"    # Legal issue
    MANUAL_REVIEW = "manual_review"              # Strategy Board decision
    DATA_INTEGRITY = "data_integrity"            # Data collection failed
```

**Pause Workflow:**
```python
def pause_strategy(strategy_id: int, reason: PauseReason, details: str) -> PauseResult:
    # Step 1: Update state
    set_strategy_state(strategy_id, StrategyState.PAUSED)
    
    # Step 2: Record pause event
    create_pause_event({
        "strategy_id": strategy_id,
        "reason": reason,
        "details": details,
        "paused_at": datetime.utcnow(),
        "paused_by": "system" if automated else "strategy_board"
    })
    
    # Step 3: Generate alerts
    create_alert(AlertType.STRATEGY_PAUSED, {
        "strategy_id": strategy_id,
        "strategy_name": get_strategy_name(strategy_id),
        "reason": reason,
        "affected_users": count_affected_users(strategy_id)
    })
    
    # Step 4: Notify boards
    notify_boards(["CEO", "CMO", "CLO"], "strategy_paused", {
        "strategy_id": strategy_id,
        "reason": reason
    })
    
    return PauseResult(success=True, users_affected=...)
```

#### 2.4.4 REACTIVATE Strategy

**Trigger:** Manual (Strategy Board decision after review)

**Reactivation Requirements:**
```python
def can_reactivate(strategy_id: int) -> ReactivationCheck:
    checks = []
    
    # Check 1: Pause reason resolved
    pause_event = get_latest_pause_event(strategy_id)
    if pause_event.reason == PauseReason.PROTOCOL_INCIDENT:
        protocol_healthy = check_protocol_health(pause_event.protocol_id)
        checks.append(("protocol_health", protocol_healthy))
    
    # Check 2: All protocols currently healthy
    for protocol_id in get_strategy_protocols(strategy_id):
        healthy = check_protocol_health(protocol_id)
        checks.append((f"protocol_{protocol_id}_health", healthy))
    
    # Check 3: Data collection functioning
    data_fresh = check_data_freshness(strategy_id)
    checks.append(("data_freshness", data_fresh))
    
    # Check 4: QR Board approval (if material changes during pause)
    if has_pending_changes(strategy_id):
        qr_approved = check_qr_approval(strategy_id)
        checks.append(("qr_approval", qr_approved))
    
    all_passed = all(check[1] for check in checks)
    return ReactivationCheck(can_reactivate=all_passed, checks=checks)
```

#### 2.4.5 RETIRE Strategy

**Trigger:** Manual (Strategy Board decision)

**Retirement Workflow:**
```python
def retire_strategy(strategy_id: int, reason: str, migration_target: int = None) -> RetirementResult:
    # Step 1: Check for active users
    active_users = get_active_users(strategy_id)
    
    if len(active_users) > 0 and migration_target is None:
        return RetirementResult(
            success=False,
            error="Cannot retire strategy with active users without migration target"
        )
    
    # Step 2: If migration target, validate it
    if migration_target:
        if not is_valid_migration_target(strategy_id, migration_target):
            return RetirementResult(
                success=False,
                error="Invalid migration target"
            )
    
    # Step 3: Create retirement plan
    retirement_plan = {
        "strategy_id": strategy_id,
        "reason": reason,
        "migration_target": migration_target,
        "affected_users": len(active_users),
        "retirement_date": datetime.utcnow() + timedelta(days=30),  # 30-day notice
        "created_at": datetime.utcnow()
    }
    
    # Step 4: Set state to PAUSED with retirement pending
    set_strategy_state(strategy_id, StrategyState.PAUSED)
    set_retirement_pending(strategy_id, retirement_plan)
    
    # Step 5: Notify users
    schedule_user_notifications(active_users, retirement_plan)
    
    # Step 6: After 30 days, complete retirement
    schedule_task("complete_retirement", {
        "strategy_id": strategy_id,
        "execute_at": retirement_plan["retirement_date"]
    })
    
    return RetirementResult(success=True, retirement_plan=retirement_plan)
```

---

## 3. Protocol Management

### 3.1 Protocol States

```python
class ProtocolState(Enum):
    RESEARCH = "research"           # Being evaluated by Rakia
    WHITELISTED = "whitelisted"     # Approved, not yet in strategies
    ACTIVE = "active"               # Used in at least one strategy
    DEPRECATED = "deprecated"       # Being phased out
    BLACKLISTED = "blacklisted"     # Banned from use
```

### 3.2 Protocol Schema

```json
{
  "id": "string (unique identifier)",
  "name": "string",
  "chain": "enum: Ethereum | Arbitrum | Solana | Polygon | ...",
  "asset": "string (primary asset)",
  "type": "enum: stablecoin_yield | lending | liquid_staking | liquid_staking_mev | perps_lp | rwa",
  "crypto_exposure": "boolean",
  "price_exposure": "string (if crypto_exposure=true, e.g., 'SOL', 'ETH')",
  "defillama_project": "string (DeFiLlama project slug)",
  "defillama_pool_id": "string (specific pool UUID)",
  "state": "ProtocolState",
  "risk_score": "integer (1-10, from Rakia)",
  "min_tvl_usd": "integer (minimum acceptable TVL)",
  "max_allocation_pct": "integer (maximum % in any strategy)",
  "audit_status": {
    "audited": "boolean",
    "auditors": ["string"],
    "last_audit_date": "date",
    "bug_bounty_usd": "integer"
  },
  "metadata": {
    "website": "string",
    "docs": "string",
    "governance": "string"
  },
  "added_at": "datetime",
  "added_by": "string (board reference)"
}
```

### 3.3 Protocol Evaluation Criteria

**[DEPENDENCY: Rakia to provide evaluation methodology]**

```python
# Placeholder - Rakia to define specific scoring criteria
class ProtocolEvaluationCriteria:
    """
    Rakia Researcher should define:
    1. TVL thresholds by protocol type
    2. Audit requirements
    3. Track record requirements (months of operation)
    4. Incident history weighting
    5. Governance decentralization scoring
    6. Smart contract complexity assessment
    """
    pass
```

### 3.4 Protocol Health Monitoring

**Health Check Frequency:**

| Check Type | Frequency | Data Source |
|------------|-----------|-------------|
| TVL monitoring | Every 15 minutes | DeFiLlama API |
| APY monitoring | Hourly | DeFiLlama API |
| Smart contract activity | Real-time (if available) | Etherscan/Solscan |
| Governance proposals | Daily | Protocol governance |
| Social sentiment | Hourly | Twitter API (optional) |
| Depeg monitoring (stables) | Every 5 minutes | CoinGecko/DEX prices |

**Health Score Calculation:**

**[DEPENDENCY: QR Board to provide health score formula]**

```python
# Placeholder - QR Board to define specific formula
def calculate_protocol_health_score(protocol_id: str) -> float:
    """
    QR Board should define:
    1. Weight for each health metric
    2. Threshold values for each metric
    3. Aggregation formula
    4. Historical vs current weighting
    
    Returns: float between 0.0 (critical) and 1.0 (healthy)
    """
    pass
```

### 3.5 Protocol Addition Workflow

```python
def add_protocol(protocol_data: dict) -> AddProtocolResult:
    # Step 1: Validate protocol data
    validation = validate_protocol_data(protocol_data)
    if not validation.valid:
        return AddProtocolResult(success=False, errors=validation.errors)
    
    # Step 2: Check Rakia evaluation exists
    rakia_evaluation = get_rakia_evaluation(protocol_data["id"])
    if not rakia_evaluation:
        return AddProtocolResult(
            success=False,
            error="Protocol must be evaluated by Rakia first"
        )
    
    # Step 3: Check minimum requirements
    if rakia_evaluation["risk_score"] > 7:
        return AddProtocolResult(
            success=False,
            error="Risk score too high (max 7)"
        )
    
    # Step 4: Create protocol record
    protocol_data["state"] = ProtocolState.WHITELISTED
    protocol_data["added_at"] = datetime.utcnow()
    save_protocol(protocol_data)
    
    # Step 5: Initialize monitoring
    initialize_protocol_monitoring(protocol_data["id"])
    
    # Step 6: Notify boards
    notify_boards(["Strategy", "QR", "CTO"], "protocol_added", protocol_data)
    
    return AddProtocolResult(success=True, protocol_id=protocol_data["id"])
```

### 3.6 Protocol Removal/Blacklisting

```python
def blacklist_protocol(protocol_id: str, reason: str, immediate: bool = False) -> BlacklistResult:
    # Step 1: Get affected strategies
    affected_strategies = get_strategies_using_protocol(protocol_id)
    
    if immediate:
        # Emergency blacklist - pause all affected strategies
        for strategy_id in affected_strategies:
            pause_strategy(strategy_id, PauseReason.PROTOCOL_INCIDENT, reason)
    else:
        # Scheduled blacklist - 7 day migration window
        for strategy_id in affected_strategies:
            create_migration_task(strategy_id, protocol_id, days=7)
    
    # Step 2: Update protocol state
    set_protocol_state(protocol_id, ProtocolState.BLACKLISTED)
    
    # Step 3: Record event
    create_blacklist_event({
        "protocol_id": protocol_id,
        "reason": reason,
        "immediate": immediate,
        "affected_strategies": affected_strategies,
        "blacklisted_at": datetime.utcnow()
    })
    
    # Step 4: Critical alert
    create_alert(AlertType.PROTOCOL_BLACKLISTED, {
        "protocol_id": protocol_id,
        "reason": reason,
        "affected_strategies": len(affected_strategies)
    }, severity="critical")
    
    return BlacklistResult(
        success=True,
        affected_strategies=affected_strategies,
        migration_deadline=datetime.utcnow() + timedelta(days=0 if immediate else 7)
    )
```

---

## 4. Allocation Rules Engine

### 4.1 Core Allocation Constraints

```python
ALLOCATION_CONSTRAINTS = {
    # Global constraints
    "min_protocols_per_strategy": 2,
    "max_protocols_per_strategy": 6,
    "min_allocation_per_protocol": 0.10,  # 10%
    "max_allocation_per_protocol": 0.70,  # 70% (Sky cap from Session 006)
    
    # Type constraints
    "stable_protocols": {
        "max_single_protocol": 0.40,  # 40% max (Sky cap for Q2)
        "min_diversification": 2,     # At least 2 stable protocols if >50% stable
    },
    "crypto_protocols": {
        "max_single_protocol": 0.50,  # 50% of crypto allocation
        "correlation_limit": 0.85,    # Max correlation between crypto protocols
    },
    
    # Chain constraints
    "max_single_chain_exposure": 0.80,  # 80% max on one chain
}
```

### 4.2 Allocation Validation

```python
def validate_allocations(strategy: dict) -> AllocationValidation:
    errors = []
    warnings = []
    
    allocations = strategy["allocations"]
    all_allocations = {**allocations["stable"], **allocations["crypto"]}
    
    # Constraint 1: Sum to 100%
    total = sum(all_allocations.values())
    if abs(total - 1.0) > 0.001:
        errors.append(f"Allocations sum to {total*100:.1f}%, must be 100%")
    
    # Constraint 2: Protocol count
    protocol_count = len(all_allocations)
    if protocol_count < ALLOCATION_CONSTRAINTS["min_protocols_per_strategy"]:
        errors.append(f"Minimum {ALLOCATION_CONSTRAINTS['min_protocols_per_strategy']} protocols required")
    if protocol_count > ALLOCATION_CONSTRAINTS["max_protocols_per_strategy"]:
        errors.append(f"Maximum {ALLOCATION_CONSTRAINTS['max_protocols_per_strategy']} protocols allowed")
    
    # Constraint 3: Individual protocol limits
    for protocol_id, allocation in all_allocations.items():
        if allocation < ALLOCATION_CONSTRAINTS["min_allocation_per_protocol"]:
            errors.append(f"{protocol_id}: {allocation*100:.0f}% below minimum 10%")
        if allocation > ALLOCATION_CONSTRAINTS["max_allocation_per_protocol"]:
            errors.append(f"{protocol_id}: {allocation*100:.0f}% exceeds maximum 70%")
        
        # Check protocol-specific max
        protocol = get_protocol(protocol_id)
        if protocol and allocation > protocol.get("max_allocation_pct", 100) / 100:
            errors.append(f"{protocol_id}: exceeds protocol max allocation of {protocol['max_allocation_pct']}%")
    
    # Constraint 4: Sky cap (from Session 006)
    if "sky" in all_allocations and all_allocations["sky"] > 0.40:
        warnings.append(f"Sky allocation {all_allocations['sky']*100:.0f}% exceeds recommended 40% cap")
    
    # Constraint 5: Chain diversification
    chain_exposure = calculate_chain_exposure(all_allocations)
    for chain, exposure in chain_exposure.items():
        if exposure > ALLOCATION_CONSTRAINTS["max_single_chain_exposure"]:
            warnings.append(f"{chain} exposure {exposure*100:.0f}% exceeds 80% recommendation")
    
    # Constraint 6: Crypto correlation check
    if allocations["crypto"]:
        correlation_issues = check_crypto_correlations(allocations["crypto"])
        warnings.extend(correlation_issues)
    
    return AllocationValidation(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )

def calculate_chain_exposure(allocations: dict) -> dict:
    """Calculate exposure to each blockchain."""
    chain_exposure = defaultdict(float)
    for protocol_id, allocation in allocations.items():
        protocol = get_protocol(protocol_id)
        if protocol:
            chain_exposure[protocol["chain"]] += allocation
    return dict(chain_exposure)
```

### 4.3 Rebalancing Rules

**Rebalancing Triggers:**

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Allocation drift | >5% from target | Suggest rebalance |
| Allocation drift | >10% from target | Force rebalance review |
| Protocol APY drop | >50% from 7-day avg | Alert + suggest reallocation |
| Protocol TVL drop | >20% in 24h | Alert + review |
| New protocol available | Whitelisted + better risk/reward | Suggest addition |

```python
def check_rebalancing_needs(strategy_id: int) -> RebalanceCheck:
    strategy = get_strategy(strategy_id)
    current_allocations = get_current_allocations(strategy_id)  # Live on-chain
    target_allocations = strategy["allocations"]
    
    rebalance_suggestions = []
    
    for category in ["stable", "crypto"]:
        for protocol_id, target in target_allocations[category].items():
            current = current_allocations.get(category, {}).get(protocol_id, 0)
            drift = abs(current - target)
            
            if drift > 0.10:  # >10% drift
                rebalance_suggestions.append({
                    "protocol_id": protocol_id,
                    "current": current,
                    "target": target,
                    "drift": drift,
                    "priority": "high",
                    "action": "force_review"
                })
            elif drift > 0.05:  # >5% drift
                rebalance_suggestions.append({
                    "protocol_id": protocol_id,
                    "current": current,
                    "target": target,
                    "drift": drift,
                    "priority": "medium",
                    "action": "suggest_rebalance"
                })
    
    return RebalanceCheck(
        needs_rebalancing=len([s for s in rebalance_suggestions if s["priority"] == "high"]) > 0,
        suggestions=rebalance_suggestions
    )
```

### 4.4 Fallback Allocation System

**From Session 006 - Sky Contingency:**

```python
# Pre-defined fallback allocations (approved Session 006)
FALLBACK_ALLOCATIONS = {
    "sky_failure": {
        1: {"aave": 0.60, "compound": 0.40},  # Safe Harbor
        2: {"aave": 0.50, "compound": 0.20, "sanctum": 0.30},  # Beat Inflation
        3: {"aave": 0.65, "compound": 0.35},  # Goal Keeper
        4: {"aave": 0.45, "compound": 0.20, "sanctum": 0.35},  # Steady Progress
        5: {"aave": 0.60, "compound": 0.40},  # Patient Builder
        6: {"aave": 0.40, "compound": 0.20, "sanctum": 0.25, "jlp": 0.15},  # Balanced Builder
        7: {"aave": 0.65, "compound": 0.35},  # Steady Compounder
        8: {"aave": 0.20, "compound": 0.10, "sanctum": 0.35, "jlp": 0.35},  # Wealth Accelerator
        9: {"aave": 0.60, "compound": 0.40},  # Yield Maximizer
        10: {"aave": 0.10, "compound": 0.05, "sanctum": 0.30, "jlp": 0.35, "jito": 0.20},  # Full Throttle
    }
}

def get_fallback_allocation(strategy_id: int, failed_protocol: str) -> dict:
    """Get pre-approved fallback allocation when a protocol fails."""
    fallback_key = f"{failed_protocol}_failure"
    if fallback_key in FALLBACK_ALLOCATIONS:
        return FALLBACK_ALLOCATIONS[fallback_key].get(strategy_id)
    return None

def apply_fallback_allocation(strategy_id: int, failed_protocol: str) -> FallbackResult:
    """Apply fallback allocation when protocol fails."""
    
    fallback = get_fallback_allocation(strategy_id, failed_protocol)
    if not fallback:
        return FallbackResult(
            success=False,
            error="No pre-approved fallback for this scenario"
        )
    
    # Create migration recommendation (user must approve)
    migration = {
        "strategy_id": strategy_id,
        "reason": f"{failed_protocol} failure",
        "current_allocations": get_strategy(strategy_id)["allocations"],
        "recommended_allocations": fallback,
        "created_at": datetime.utcnow(),
        "requires_user_approval": True  # diBoaS never moves funds without consent
    }
    
    save_migration_recommendation(migration)
    
    # Alert users
    create_user_alert(strategy_id, "migration_recommended", migration)
    
    return FallbackResult(success=True, migration=migration)
```

---

## 5. Monitoring System

### 5.1 Monitoring Layers

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    MONITORING LAYERS                            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  Layer 1: MACRO (External)                                      â”‚
â”‚  â”œâ”€â”€ Fed rate decisions                                         â”‚
â”‚  â”œâ”€â”€ CPI/inflation data                                         â”‚
â”‚  â”œâ”€â”€ VIX volatility index                                       â”‚
â”‚  â””â”€â”€ DXY dollar index                                           â”‚
â”‚                                                                 â”‚
â”‚  Layer 2: TRADFI (Markets)                                      â”‚
â”‚  â”œâ”€â”€ S&P 500 performance                                        â”‚
â”‚  â”œâ”€â”€ 10Y Treasury yield                                         â”‚
â”‚  â””â”€â”€ Sector ETFs (XLF, XLK, etc.)                              â”‚
â”‚                                                                 â”‚
â”‚  Layer 3: CRYPTO MACRO                                          â”‚
â”‚  â”œâ”€â”€ BTC/ETH/SOL prices                                         â”‚
â”‚  â”œâ”€â”€ Total crypto market cap                                    â”‚
â”‚  â”œâ”€â”€ Stablecoin supply (USDT, USDC, USDS)                      â”‚
â”‚  â””â”€â”€ ETF flows (IBIT, ETHA, etc.)                              â”‚
â”‚                                                                 â”‚
â”‚  Layer 4: PROTOCOL HEALTH                                       â”‚
â”‚  â”œâ”€â”€ Protocol TVL changes                                       â”‚
â”‚  â”œâ”€â”€ Protocol APY changes                                       â”‚
â”‚  â”œâ”€â”€ Smart contract activity                                    â”‚
â”‚  â”œâ”€â”€ Governance proposals                                       â”‚
â”‚  â””â”€â”€ Depeg monitoring                                           â”‚
â”‚                                                                 â”‚
â”‚  Layer 5: WHALE/ESTATE                                          â”‚
â”‚  â”œâ”€â”€ Estate wallet movements                                    â”‚
â”‚  â”œâ”€â”€ Whale wallet activity                                      â”‚
â”‚  â””â”€â”€ Market maker flows                                         â”‚
â”‚                                                                 â”‚
â”‚  Layer 6: STRATEGY PERFORMANCE                                  â”‚
â”‚  â”œâ”€â”€ Actual vs expected returns                                 â”‚
â”‚  â”œâ”€â”€ Volatility metrics                                         â”‚
â”‚  â””â”€â”€ User behavior signals                                      â”‚
â”‚                                                                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 5.2 Monitoring Configuration

```python
MONITORING_CONFIG = {
    "protocol_health": {
        "tvl": {
            "check_frequency_minutes": 15,
            "alert_threshold_drop_pct": 10,  # 10% drop in 24h
            "critical_threshold_drop_pct": 25,  # 25% drop in 24h
            "data_source": "defillama_api"
        },
        "apy": {
            "check_frequency_minutes": 60,
            "alert_threshold_drop_pct": 30,  # 30% drop from 7d avg
            "critical_threshold_drop_pct": 50,  # 50% drop from 7d avg
            "data_source": "defillama_api"
        },
        "depeg": {
            "check_frequency_minutes": 5,
            "alert_threshold_pct": 0.5,   # 0.5% off peg
            "warning_threshold_pct": 1.0,  # 1% off peg
            "critical_threshold_pct": 2.0,  # 2% off peg
            "emergency_threshold_pct": 5.0,  # 5% off peg
            "data_source": "coingecko_api"
        }
    },
    "estate_wallets": {
        "check_frequency_minutes": 60,
        "alert_threshold_movement_usd": 10_000_000,  # $10M
        "critical_threshold_movement_usd": 100_000_000,  # $100M
        "data_source": "etherscan_api"
    },
    "whale_wallets": {
        "check_frequency_minutes": 60,
        "alert_threshold_movement_usd": 50_000_000,  # $50M
        "data_source": "arkham_api"
    },
    "strategy_performance": {
        "check_frequency_minutes": 1440,  # Daily
        "underperformance_threshold_pct": 20,  # 20% below target
        "data_source": "internal"
    }
}
```

### 5.3 Monitoring Implementation

```python
class StrategyMonitor:
    """Core monitoring service for Strategy Board automation."""
    
    def __init__(self, config: dict):
        self.config = config
        self.alert_service = AlertService()
        self.data_collector = DataCollector()
    
    async def run_monitoring_cycle(self):
        """Main monitoring loop."""
        while True:
            try:
                # Protocol health checks
                await self.check_protocol_health()
                
                # Estate wallet checks
                await self.check_estate_wallets()
                
                # Strategy performance checks
                await self.check_strategy_performance()
                
                # Allocation drift checks
                await self.check_allocation_drift()
                
            except Exception as e:
                self.alert_service.create_alert(
                    AlertType.SYSTEM_ERROR,
                    {"error": str(e), "component": "monitoring"}
                )
            
            await asyncio.sleep(60)  # 1 minute base cycle
    
    async def check_protocol_health(self):
        """Check health of all active protocols."""
        protocols = get_active_protocols()
        
        for protocol in protocols:
            # TVL check
            current_tvl = await self.data_collector.get_protocol_tvl(protocol["id"])
            historical_tvl = get_historical_tvl(protocol["id"], days=1)
            
            if historical_tvl > 0:
                tvl_change_pct = (current_tvl - historical_tvl) / historical_tvl * 100
                
                if tvl_change_pct < -self.config["protocol_health"]["tvl"]["critical_threshold_drop_pct"]:
                    await self.handle_critical_tvl_drop(protocol, tvl_change_pct)
                elif tvl_change_pct < -self.config["protocol_health"]["tvl"]["alert_threshold_drop_pct"]:
                    await self.handle_tvl_drop_alert(protocol, tvl_change_pct)
            
            # APY check
            current_apy = await self.data_collector.get_protocol_apy(protocol["id"])
            avg_apy_7d = get_average_apy(protocol["id"], days=7)
            
            if avg_apy_7d > 0:
                apy_change_pct = (current_apy - avg_apy_7d) / avg_apy_7d * 100
                
                if apy_change_pct < -self.config["protocol_health"]["apy"]["critical_threshold_drop_pct"]:
                    await self.handle_critical_apy_drop(protocol, apy_change_pct)
                elif apy_change_pct < -self.config["protocol_health"]["apy"]["alert_threshold_drop_pct"]:
                    await self.handle_apy_drop_alert(protocol, apy_change_pct)
            
            # Depeg check (for stablecoin protocols)
            if protocol["type"] == "stablecoin_yield":
                price = await self.data_collector.get_stablecoin_price(protocol["asset"])
                depeg_pct = abs(price - 1.0) * 100
                
                if depeg_pct > self.config["protocol_health"]["depeg"]["emergency_threshold_pct"]:
                    await self.handle_emergency_depeg(protocol, depeg_pct)
                elif depeg_pct > self.config["protocol_health"]["depeg"]["critical_threshold_pct"]:
                    await self.handle_critical_depeg(protocol, depeg_pct)
                elif depeg_pct > self.config["protocol_health"]["depeg"]["warning_threshold_pct"]:
                    await self.handle_warning_depeg(protocol, depeg_pct)
                elif depeg_pct > self.config["protocol_health"]["depeg"]["alert_threshold_pct"]:
                    await self.handle_depeg_alert(protocol, depeg_pct)
    
    async def handle_emergency_depeg(self, protocol: dict, depeg_pct: float):
        """Handle emergency depeg (>5%) - from Session 006 Sky Contingency."""
        # Level 4 Alert - Critical
        self.alert_service.create_alert(
            AlertType.PROTOCOL_DEPEG_EMERGENCY,
            {
                "protocol_id": protocol["id"],
                "protocol_name": protocol["name"],
                "depeg_pct": depeg_pct,
                "asset": protocol["asset"],
                "action": "recommend_migration"
            },
            severity="critical",
            boards=["CEO", "Strategy", "CMO", "CLO"]
        )
        
        # Get affected strategies
        affected_strategies = get_strategies_using_protocol(protocol["id"])
        
        # Create migration recommendations for each
        for strategy_id in affected_strategies:
            apply_fallback_allocation(strategy_id, protocol["id"])
        
        # Pause new allocations to this protocol
        set_protocol_allocation_paused(protocol["id"], True)
```

### 5.4 Sky-Specific Monitoring (Session 006)

```python
# From Session 006 - Sky Contingency Alert Levels
SKY_ALERT_LEVELS = {
    "level_1_watch": {
        "depeg_range": (0.5, 1.0),  # 0.5-1% off peg
        "action": "internal_alert",
        "notification": ["Strategy Board"],
        "user_communication": None
    },
    "level_2_caution": {
        "depeg_range": (1.0, 2.0),  # 1-2% off peg
        "tvl_drop_24h": 10,  # OR 10% TVL drop
        "action": "prepare_communication",
        "notification": ["Strategy Board", "CMO Board"],
        "user_communication": "draft"
    },
    "level_3_warning": {
        "depeg_range": (2.0, 5.0),  # 2-5% off peg
        "unusual_contract_activity": True,
        "action": "alert_users",
        "notification": ["Strategy Board", "CMO Board", "CLO Board"],
        "user_communication": "send_warning"
    },
    "level_4_critical": {
        "depeg_range": (5.0, 100.0),  # >5% off peg
        "confirmed_exploit": True,
        "action": "recommend_migration",
        "notification": ["All Boards", "CEO"],
        "user_communication": "urgent_migration"
    }
}

async def monitor_sky_health():
    """Dedicated Sky SSR monitoring (highest priority)."""
    
    # Get current USDS price
    usds_price = await get_stablecoin_price("USDS")
    depeg_pct = abs(usds_price - 1.0) * 100
    
    # Get Sky TVL
    sky_tvl = await get_protocol_tvl("sky")
    sky_tvl_24h_ago = get_historical_tvl("sky", hours=24)
    tvl_change_pct = (sky_tvl - sky_tvl_24h_ago) / sky_tvl_24h_ago * 100 if sky_tvl_24h_ago > 0 else 0
    
    # Determine alert level
    alert_level = None
    
    if depeg_pct >= 5.0:
        alert_level = "level_4_critical"
    elif depeg_pct >= 2.0:
        alert_level = "level_3_warning"
    elif depeg_pct >= 1.0 or tvl_change_pct <= -10:
        alert_level = "level_2_caution"
    elif depeg_pct >= 0.5:
        alert_level = "level_1_watch"
    
    if alert_level:
        await handle_sky_alert(alert_level, depeg_pct, tvl_change_pct)
```

---

## 6. Alert System

### 6.1 Alert Types

```python
class AlertType(Enum):
    # Protocol alerts
    PROTOCOL_TVL_DROP = "protocol_tvl_drop"
    PROTOCOL_APY_DROP = "protocol_apy_drop"
    PROTOCOL_DEPEG = "protocol_depeg"
    PROTOCOL_DEPEG_EMERGENCY = "protocol_depeg_emergency"
    PROTOCOL_EXPLOIT = "protocol_exploit"
    PROTOCOL_GOVERNANCE = "protocol_governance"
    PROTOCOL_BLACKLISTED = "protocol_blacklisted"
    
    # Strategy alerts
    STRATEGY_PAUSED = "strategy_paused"
    STRATEGY_REACTIVATED = "strategy_reactivated"
    STRATEGY_RETIRED = "strategy_retired"
    STRATEGY_UNDERPERFORMING = "strategy_underperforming"
    STRATEGY_ALLOCATION_DRIFT = "strategy_allocation_drift"
    
    # Market alerts
    ESTATE_WALLET_MOVEMENT = "estate_wallet_movement"
    WHALE_MOVEMENT = "whale_movement"
    MARKET_VOLATILITY = "market_volatility"
    
    # System alerts
    DATA_COLLECTION_FAILED = "data_collection_failed"
    SYSTEM_ERROR = "system_error"
    VALIDATION_FAILED = "validation_failed"
```

### 6.2 Alert Severity

```python
class AlertSeverity(Enum):
    INFO = "info"           # Informational, no action required
    WARNING = "warning"     # Attention needed, not urgent
    HIGH = "high"           # Action required within 24h
    CRITICAL = "critical"   # Immediate action required
    EMERGENCY = "emergency" # Drop everything, handle now
```

### 6.3 Alert Schema

```json
{
  "id": "uuid",
  "type": "AlertType",
  "severity": "AlertSeverity",
  "title": "string",
  "message": "string",
  "data": {
    "protocol_id": "string (optional)",
    "strategy_id": "integer (optional)",
    "wallet_address": "string (optional)",
    "threshold_breached": "string",
    "current_value": "number",
    "threshold_value": "number"
  },
  "boards_notified": ["string"],
  "user_notification": "boolean",
  "created_at": "datetime",
  "acknowledged_at": "datetime (optional)",
  "acknowledged_by": "string (optional)",
  "resolved_at": "datetime (optional)",
  "resolved_by": "string (optional)",
  "resolution_notes": "string (optional)"
}
```

### 6.4 Alert Routing

```python
ALERT_ROUTING = {
    AlertType.PROTOCOL_TVL_DROP: {
        "severity_default": AlertSeverity.WARNING,
        "boards": ["Strategy", "QR"],
        "slack_channel": "#alerts-protocol",
        "user_notification": False
    },
    AlertType.PROTOCOL_DEPEG_EMERGENCY: {
        "severity_default": AlertSeverity.EMERGENCY,
        "boards": ["CEO", "Strategy", "CMO", "CLO", "CTO"],
        "slack_channel": "#alerts-critical",
        "user_notification": True,
        "sms_enabled": True
    },
    AlertType.STRATEGY_PAUSED: {
        "severity_default": AlertSeverity.HIGH,
        "boards": ["CEO", "Strategy", "CMO"],
        "slack_channel": "#alerts-strategy",
        "user_notification": True
    },
    AlertType.ESTATE_WALLET_MOVEMENT: {
        "severity_default": AlertSeverity.WARNING,
        "boards": ["Strategy", "Macro Game"],
        "slack_channel": "#alerts-whale",
        "user_notification": False  # Adelaide handles this
    },
    # ... more routing rules
}

def route_alert(alert: Alert):
    """Route alert to appropriate channels."""
    routing = ALERT_ROUTING.get(alert.type, {})
    
    # Slack notification
    if routing.get("slack_channel"):
        send_slack_alert(routing["slack_channel"], alert)
    
    # Board notifications
    for board in routing.get("boards", []):
        create_board_notification(board, alert)
    
    # User notification
    if routing.get("user_notification") and alert.data.get("affected_users"):
        schedule_user_notifications(alert)
    
    # SMS for emergencies
    if routing.get("sms_enabled") and alert.severity == AlertSeverity.EMERGENCY:
        send_sms_to_oncall(alert)
```

### 6.5 Alert Lifecycle

```python
async def handle_alert_lifecycle(alert_id: str):
    """Manage alert from creation to resolution."""
    alert = get_alert(alert_id)
    
    # Auto-escalation if not acknowledged
    if alert.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
        escalation_minutes = 15 if alert.severity == AlertSeverity.EMERGENCY else 60
        
        schedule_task("escalate_alert", {
            "alert_id": alert_id,
            "execute_at": datetime.utcnow() + timedelta(minutes=escalation_minutes)
        })
    
    # Auto-resolution check for certain alert types
    if alert.type in [AlertType.PROTOCOL_TVL_DROP, AlertType.PROTOCOL_APY_DROP]:
        schedule_task("check_alert_resolution", {
            "alert_id": alert_id,
            "execute_at": datetime.utcnow() + timedelta(hours=1)
        })

async def check_alert_resolution(alert_id: str):
    """Check if alert condition has resolved."""
    alert = get_alert(alert_id)
    
    if alert.type == AlertType.PROTOCOL_TVL_DROP:
        current_tvl = await get_protocol_tvl(alert.data["protocol_id"])
        threshold = alert.data["threshold_value"]
        
        if current_tvl >= threshold:
            resolve_alert(alert_id, "auto", "TVL recovered above threshold")
    
    elif alert.type == AlertType.PROTOCOL_DEPEG:
        current_price = await get_stablecoin_price(alert.data["asset"])
        if abs(current_price - 1.0) < 0.005:  # Within 0.5%
            resolve_alert(alert_id, "auto", "Price returned to peg")
```

---

## 7. Validation Framework

### 7.1 Validation Types

```python
class ValidationType(Enum):
    STRATEGY_CREATE = "strategy_create"
    STRATEGY_UPDATE = "strategy_update"
    ALLOCATION_CHANGE = "allocation_change"
    PROTOCOL_ADD = "protocol_add"
    APY_RANGE_UPDATE = "apy_range_update"
    FALLBACK_ALLOCATION = "fallback_allocation"
    MONTE_CARLO = "monte_carlo"
    BATTLE_TEST = "battle_test"
```

### 7.2 Validation Request Schema

```json
{
  "id": "uuid",
  "type": "ValidationType",
  "requestor": "string (board name)",
  "subject_id": "string (strategy_id or protocol_id)",
  "changes": {
    "before": {},
    "after": {}
  },
  "validation_requirements": {
    "qr_board": "boolean",
    "clo_board": "boolean",
    "battle_test": "boolean",
    "monte_carlo": "boolean"
  },
  "status": "enum: pending | approved | rejected | expired",
  "created_at": "datetime",
  "deadline": "datetime",
  "approvals": [
    {
      "board": "string",
      "approved": "boolean",
      "approved_by": "string",
      "approved_at": "datetime",
      "notes": "string"
    }
  ]
}
```

### 7.3 Validation Workflow

```python
def create_validation_request(
    validation_type: ValidationType,
    subject_id: str,
    changes: dict
) -> ValidationRequest:
    """Create a new validation request."""
    
    # Determine required approvals
    requirements = get_validation_requirements(validation_type)
    
    request = ValidationRequest(
        id=generate_uuid(),
        type=validation_type,
        requestor="Strategy Board",
        subject_id=subject_id,
        changes=changes,
        validation_requirements=requirements,
        status="pending",
        created_at=datetime.utcnow(),
        deadline=datetime.utcnow() + get_deadline(validation_type),
        approvals=[]
    )
    
    save_validation_request(request)
    
    # Notify required boards
    if requirements.get("qr_board"):
        notify_board("QR", "validation_requested", request)
    if requirements.get("clo_board"):
        notify_board("CLO", "validation_requested", request)
    
    return request

def get_validation_requirements(validation_type: ValidationType) -> dict:
    """Get required validations for each type."""
    
    REQUIREMENTS = {
        ValidationType.STRATEGY_CREATE: {
            "qr_board": True,
            "clo_board": True,
            "battle_test": True,
            "monte_carlo": True
        },
        ValidationType.STRATEGY_UPDATE: {
            "qr_board": True,
            "clo_board": False,
            "battle_test": False,
            "monte_carlo": False
        },
        ValidationType.ALLOCATION_CHANGE: {
            "qr_board": True,
            "clo_board": False,
            "battle_test": True,
            "monte_carlo": True
        },
        ValidationType.APY_RANGE_UPDATE: {
            "qr_board": True,
            "clo_board": True,
            "battle_test": True,
            "monte_carlo": True
        },
        ValidationType.PROTOCOL_ADD: {
            "qr_board": True,
            "clo_board": True,
            "battle_test": False,
            "monte_carlo": False
        },
        ValidationType.FALLBACK_ALLOCATION: {
            "qr_board": True,
            "clo_board": False,
            "battle_test": True,
            "monte_carlo": True
        }
    }
    
    return REQUIREMENTS.get(validation_type, {})
```

### 7.4 QR Board Validation Interface

**[DEPENDENCY: QR Board to implement validation endpoints]**

```python
# QR Board should implement these validation functions
class QRBoardValidationInterface:
    """
    Interface that QR Board must implement for automated validation.
    
    QR Board should provide:
    1. Battle Test runner with configurable scenarios
    2. Monte Carlo simulation runner
    3. APY range validation logic
    4. Allocation risk scoring
    """
    
    async def validate_strategy(self, strategy: dict) -> QRValidationResult:
        """
        Validate a strategy configuration.
        
        Returns:
            QRValidationResult with:
            - valid: bool
            - confidence: float (0-1)
            - battle_test_results: dict
            - monte_carlo_results: dict
            - warnings: list
            - errors: list
        """
        pass
    
    async def validate_allocations(self, allocations: dict) -> AllocationValidationResult:
        """
        Validate allocation percentages and risk profile.
        
        Returns:
            AllocationValidationResult with:
            - valid: bool
            - risk_score: float
            - concentration_warnings: list
            - correlation_analysis: dict
        """
        pass
    
    async def validate_apy_range(
        self,
        strategy_id: int,
        proposed_range: str
    ) -> APYRangeValidationResult:
        """
        Validate proposed APY range against historical data and simulations.
        
        Returns:
            APYRangeValidationResult with:
            - valid: bool
            - recommended_range: str
            - confidence_interval: tuple
            - historical_performance: dict
        """
        pass
    
    async def run_battle_test(
        self,
        strategy_id: int,
        scenarios: list = None
    ) -> BattleTestResult:
        """
        Run Battle Test backtesting for a strategy.
        
        Returns:
            BattleTestResult with:
            - passed: bool
            - scenarios_tested: list
            - performance_by_scenario: dict
            - max_drawdown: float
            - sharpe_ratio: float
        """
        pass
    
    async def run_monte_carlo(
        self,
        strategy_id: int,
        simulations: int = 5000
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation for a strategy.
        
        Returns:
            MonteCarloResult with:
            - simulations_run: int
            - prob_loss: float
            - median_return: float
            - p5_return: float
            - p95_return: float
            - confidence: str
        """
        pass
```

---

## 8. Contingency Automation

### 8.1 Contingency Plans

```python
CONTINGENCY_PLANS = {
    "sky_failure": {
        "trigger_conditions": {
            "any": [
                {"type": "depeg", "threshold_pct": 5.0},
                {"type": "exploit_confirmed"},
                {"type": "governance_attack"},
                {"type": "regulatory_action"}
            ]
        },
        "actions": [
            {"action": "pause_sky_allocations"},
            {"action": "alert_all_boards", "severity": "emergency"},
            {"action": "alert_affected_users"},
            {"action": "recommend_fallback_allocations"},
            {"action": "prepare_migration_ui"}
        ],
        "fallback_allocations": "FALLBACK_ALLOCATIONS['sky_failure']",
        "communication_template": "sky_emergency_template",
        "approved_by": "Strategy Board Session 006",
        "approved_date": "2026-01-19"
    },
    
    "sanctum_failure": {
        "trigger_conditions": {
            "any": [
                {"type": "tvl_drop_pct", "threshold": 50, "period_hours": 24},
                {"type": "exploit_confirmed"},
                {"type": "smart_contract_pause"}
            ]
        },
        "actions": [
            {"action": "pause_sanctum_allocations"},
            {"action": "alert_boards", "boards": ["Strategy", "CEO", "CMO"]},
            {"action": "alert_affected_users"},
            {"action": "recommend_jito_migration"}  # Sanctum â†’ Jito for SOL exposure
        ],
        "fallback_protocol": "jito",
        "communication_template": "protocol_incident_template"
    },
    
    "jlp_failure": {
        "trigger_conditions": {
            "any": [
                {"type": "tvl_drop_pct", "threshold": 40, "period_hours": 24},
                {"type": "exploit_confirmed"},
                {"type": "jupiter_pause"}
            ]
        },
        "actions": [
            {"action": "pause_jlp_allocations"},
            {"action": "alert_boards", "boards": ["Strategy", "CEO", "CMO"]},
            {"action": "alert_affected_users"},
            {"action": "recommend_gmx_migration"}  # JLP â†’ GMX V2 (if whitelisted)
        ],
        "fallback_protocol": "gmx_v2",  # Requires protocol to be whitelisted
        "communication_template": "protocol_incident_template"
    },
    
    "market_crash": {
        "trigger_conditions": {
            "all": [
                {"type": "btc_drop_pct", "threshold": 20, "period_hours": 24},
                {"type": "eth_drop_pct", "threshold": 25, "period_hours": 24}
            ]
        },
        "actions": [
            {"action": "alert_boards", "boards": ["Strategy", "CEO", "Macro Game"]},
            {"action": "increase_monitoring_frequency"},
            {"action": "prepare_crisis_communication"}
            # Note: Do NOT auto-pause or auto-migrate - user choice
        ],
        "communication_template": "market_volatility_template"
    }
}

async def check_contingency_triggers():
    """Check all contingency plan triggers."""
    for plan_name, plan in CONTINGENCY_PLANS.items():
        triggered = await evaluate_trigger_conditions(plan["trigger_conditions"])
        
        if triggered:
            await execute_contingency_plan(plan_name, plan)

async def evaluate_trigger_conditions(conditions: dict) -> bool:
    """Evaluate if contingency trigger conditions are met."""
    
    if "any" in conditions:
        # OR logic - any condition triggers
        for condition in conditions["any"]:
            if await check_single_condition(condition):
                return True
        return False
    
    elif "all" in conditions:
        # AND logic - all conditions must trigger
        for condition in conditions["all"]:
            if not await check_single_condition(condition):
                return False
        return True
    
    return False

async def check_single_condition(condition: dict) -> bool:
    """Check a single trigger condition."""
    
    if condition["type"] == "depeg":
        price = await get_stablecoin_price("USDS")
        return abs(price - 1.0) * 100 >= condition["threshold_pct"]
    
    elif condition["type"] == "tvl_drop_pct":
        # Implementation needed
        pass
    
    elif condition["type"] == "exploit_confirmed":
        # Check exploit detection service
        pass
    
    # ... more condition types

async def execute_contingency_plan(plan_name: str, plan: dict):
    """Execute a contingency plan."""
    
    log_contingency_activation(plan_name)
    
    for action in plan["actions"]:
        await execute_contingency_action(action)
    
    # Record execution
    create_contingency_event({
        "plan_name": plan_name,
        "executed_at": datetime.utcnow(),
        "actions_taken": plan["actions"]
    })
```

### 8.2 Migration Recommendation System

```python
async def recommend_migration(
    strategy_id: int,
    failed_protocol: str,
    fallback_protocol: str = None
) -> MigrationRecommendation:
    """
    Create a migration recommendation for users.
    
    IMPORTANT: diBoaS never moves user funds automatically.
    This creates a recommendation that users must approve.
    """
    
    strategy = get_strategy(strategy_id)
    affected_users = get_users_in_strategy(strategy_id)
    
    # Get fallback allocation
    if fallback_protocol:
        new_allocations = create_single_protocol_fallback(
            strategy["allocations"],
            failed_protocol,
            fallback_protocol
        )
    else:
        new_allocations = FALLBACK_ALLOCATIONS.get(f"{failed_protocol}_failure", {}).get(strategy_id)
    
    if not new_allocations:
        return MigrationRecommendation(
            success=False,
            error="No fallback allocation available"
        )
    
    recommendation = {
        "id": generate_uuid(),
        "strategy_id": strategy_id,
        "strategy_name": strategy["name"],
        "reason": f"{failed_protocol} incident",
        "failed_protocol": failed_protocol,
        "current_allocations": strategy["allocations"],
        "recommended_allocations": new_allocations,
        "affected_users": len(affected_users),
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
        "status": "pending",
        "user_approvals": {}
    }
    
    save_migration_recommendation(recommendation)
    
    # Notify users
    for user_id in affected_users:
        create_user_notification(user_id, "migration_recommended", recommendation)
    
    return MigrationRecommendation(success=True, recommendation=recommendation)
```

---

## 9. APY Range Management

### 9.1 APY Range Format

```python
# APY ranges are stored as strings in format "X-Y%"
# Examples: "4-6%", "7-12%", "5-9%"

def parse_apy_range(range_str: str) -> tuple:
    """Parse APY range string to (min, max) tuple."""
    match = re.match(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)%", range_str)
    if match:
        return (float(match.group(1)), float(match.group(2)))
    return None

def format_apy_range(min_apy: float, max_apy: float) -> str:
    """Format APY range as string."""
    return f"{min_apy:.0f}-{max_apy:.0f}%"
```

### 9.2 APY Range Calculation

**[DEPENDENCY: QR Board to provide calculation methodology]**

```python
async def calculate_recommended_apy_range(
    strategy_id: int,
    confidence_level: float = 0.90
) -> APYRangeRecommendation:
    """
    Calculate recommended APY range based on historical data and simulations.
    
    QR Board should implement the actual calculation logic including:
    1. Historical performance analysis
    2. Monte Carlo simulation results
    3. Current market conditions
    4. Protocol APY trends
    """
    
    # Get historical data
    historical_returns = await get_historical_strategy_returns(strategy_id, months=12)
    
    # Get Monte Carlo results
    monte_carlo = await run_monte_carlo(strategy_id)
    
    # Get current protocol APYs
    current_apys = await get_current_protocol_apys(strategy_id)
    
    # QR Board calculation
    # [PLACEHOLDER - QR Board to implement]
    recommended_min = monte_carlo["p25_return"]  # 25th percentile
    recommended_max = monte_carlo["p75_return"]  # 75th percentile
    
    return APYRangeRecommendation(
        strategy_id=strategy_id,
        current_range=get_strategy(strategy_id)["target_apy_range"],
        recommended_range=format_apy_range(recommended_min, recommended_max),
        confidence_level=confidence_level,
        methodology="monte_carlo_percentiles",
        data_sources={
            "historical_months": 12,
            "monte_carlo_simulations": monte_carlo["simulations_run"],
            "current_protocol_apys": current_apys
        }
    )
```

### 9.3 APY Range Update Triggers

```python
APY_RANGE_UPDATE_TRIGGERS = {
    "protocol_apy_change": {
        "threshold_pct": 30,  # 30% change in weighted average protocol APY
        "period_days": 30
    },
    "monte_carlo_divergence": {
        "threshold_pct": 20,  # 20% difference between stated and simulated range
    },
    "scheduled_review": {
        "frequency_days": 90  # Quarterly review
    }
}

async def check_apy_range_update_needed(strategy_id: int) -> bool:
    """Check if strategy APY range needs updating."""
    
    strategy = get_strategy(strategy_id)
    current_range = parse_apy_range(strategy["target_apy_range"])
    
    # Check protocol APY changes
    weighted_apy = await calculate_weighted_protocol_apy(strategy_id)
    historical_weighted_apy = await get_historical_weighted_apy(strategy_id, days=30)
    
    if historical_weighted_apy > 0:
        apy_change_pct = abs(weighted_apy - historical_weighted_apy) / historical_weighted_apy * 100
        if apy_change_pct > APY_RANGE_UPDATE_TRIGGERS["protocol_apy_change"]["threshold_pct"]:
            return True
    
    # Check Monte Carlo divergence
    monte_carlo = await run_monte_carlo(strategy_id, simulations=1000)  # Quick run
    mc_range = (monte_carlo["p25_return"], monte_carlo["p75_return"])
    
    range_midpoint = (current_range[0] + current_range[1]) / 2
    mc_midpoint = (mc_range[0] + mc_range[1]) / 2
    
    divergence_pct = abs(range_midpoint - mc_midpoint) / range_midpoint * 100
    if divergence_pct > APY_RANGE_UPDATE_TRIGGERS["monte_carlo_divergence"]["threshold_pct"]:
        return True
    
    # Check scheduled review
    last_review = get_last_apy_range_review(strategy_id)
    if last_review:
        days_since_review = (datetime.utcnow() - last_review).days
        if days_since_review >= APY_RANGE_UPDATE_TRIGGERS["scheduled_review"]["frequency_days"]:
            return True
    
    return False
```

---

## 10. Data Dependencies

### 10.1 Required Data Sources

| Data Type | Source | Frequency | Owner |
|-----------|--------|-----------|-------|
| Protocol APY | DeFiLlama API | Hourly | Rakia/CTO |
| Protocol TVL | DeFiLlama API | 15 min | Rakia/CTO |
| Stablecoin prices | CoinGecko API | 5 min | CTO |
| Crypto prices | Yahoo Finance / CoinGecko | Hourly | CTO |
| Estate wallets | Etherscan / Arkham | Hourly | Rakia |
| Whale wallets | Arkham | Hourly | Rakia |
| TradFi benchmarks | Yahoo Finance | Daily | Rakia |
| Inflation data | FRED / ECB | Monthly | Rakia |

### 10.2 Data File Dependencies

**From Rakia's Data Catalog:**

| File | Used By | Update Frequency |
|------|---------|------------------|
| `sky_ssr_historical_apy.csv` | Battle Test, Monte Carlo | Daily |
| `compound_v3_arbitrum_usdc_apy.csv` | Battle Test, Monte Carlo | Daily |
| `sanctum_inf_historical_apy.csv` | Battle Test, Monte Carlo | Daily |
| `jito_extended_apy.csv` | Battle Test, Monte Carlo | Daily |
| `jupiter_jlp_historical_apy.csv` | Battle Test, Monte Carlo | Daily |
| `yahoo_historical_prices.csv` | Performance comparison | Daily |
| `estate_wallet_tracker.csv` | Estate monitoring | Weekly |
| `whale_wallet_master_list.csv` | Whale monitoring | Weekly |

### 10.3 Rakia Research Dependencies

**[DEPENDENCY: Rakia to provide these deliverables]**

| Deliverable | Purpose | Deadline |
|-------------|---------|----------|
| Kamino Lend risk assessment | Protocol addition evaluation | Before Q2 |
| GMX V2 vs JLP comparison | Perps LP diversification decision | Before Q2 |
| Sky governance tracking | Rate change prediction | Ongoing |
| RWA protocol readiness | Phase 2 planning | Q2 |
| Protocol evaluation methodology | Automated protocol scoring | Q1 |

---

## 11. Decision Workflows

### 11.1 Strategy Board Decision Types

| Decision Type | Approval Required | Timeline | Automation Level |
|---------------|-------------------|----------|------------------|
| APY range adjustment | QR Board | 3-5 days | Semi-automated |
| Minor allocation change (â‰¤5%) | None | Immediate | Automated |
| Major allocation change (>5%) | QR Board | 5-7 days | Semi-automated |
| Protocol addition | QR + CLO | 2-4 weeks | Manual |
| Protocol removal | QR Board | 1-2 weeks | Semi-automated |
| Strategy pause | None | Immediate | Automated |
| Strategy retirement | CEO + CMO | 30 days | Manual |
| Emergency contingency | None | Immediate | Automated |

### 11.2 Approval Workflow

```python
class ApprovalWorkflow:
    """Manage multi-board approval workflows."""
    
    WORKFLOW_DEFINITIONS = {
        "strategy_create": {
            "required_approvals": ["QR", "CLO"],
            "optional_approvals": ["CEO"],
            "timeout_hours": 168,  # 7 days
            "auto_reject_on_timeout": True
        },
        "allocation_change_major": {
            "required_approvals": ["QR"],
            "optional_approvals": [],
            "timeout_hours": 120,  # 5 days
            "auto_reject_on_timeout": True
        },
        "protocol_add": {
            "required_approvals": ["QR", "CLO"],
            "optional_approvals": ["CEO"],
            "timeout_hours": 336,  # 14 days
            "auto_reject_on_timeout": True
        },
        "apy_range_update": {
            "required_approvals": ["QR", "CLO"],
            "optional_approvals": [],
            "timeout_hours": 120,  # 5 days
            "auto_reject_on_timeout": False  # Extends, doesn't reject
        }
    }
    
    async def create_approval_request(
        self,
        workflow_type: str,
        subject: dict,
        requestor: str
    ) -> ApprovalRequest:
        """Create a new approval request."""
        
        workflow = self.WORKFLOW_DEFINITIONS.get(workflow_type)
        if not workflow:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        request = ApprovalRequest(
            id=generate_uuid(),
            workflow_type=workflow_type,
            subject=subject,
            requestor=requestor,
            required_approvals=workflow["required_approvals"],
            optional_approvals=workflow["optional_approvals"],
            status="pending",
            created_at=datetime.utcnow(),
            deadline=datetime.utcnow() + timedelta(hours=workflow["timeout_hours"]),
            approvals={}
        )
        
        save_approval_request(request)
        
        # Notify required approvers
        for board in workflow["required_approvals"]:
            notify_board(board, "approval_requested", request)
        
        return request
    
    async def process_approval(
        self,
        request_id: str,
        board: str,
        approved: bool,
        notes: str = None
    ) -> ApprovalResult:
        """Process an approval from a board."""
        
        request = get_approval_request(request_id)
        
        if request.status != "pending":
            return ApprovalResult(success=False, error="Request not pending")
        
        if board not in request.required_approvals + request.optional_approvals:
            return ApprovalResult(success=False, error="Board not authorized")
        
        # Record approval
        request.approvals[board] = {
            "approved": approved,
            "timestamp": datetime.utcnow(),
            "notes": notes
        }
        
        # Check if fully approved or rejected
        required_approvals = [
            request.approvals.get(b, {}).get("approved")
            for b in request.required_approvals
        ]
        
        if all(a == True for a in required_approvals if a is not None):
            request.status = "approved"
            await self.execute_approved_request(request)
        elif any(a == False for a in required_approvals):
            request.status = "rejected"
        
        save_approval_request(request)
        
        return ApprovalResult(success=True, status=request.status)
```

---

## 12. Reporting Requirements

### 12.1 Automated Reports

| Report | Frequency | Recipients | Content |
|--------|-----------|------------|---------|
| Strategy Performance Daily | Daily | Strategy Board | APY, drift, alerts |
| Protocol Health Weekly | Weekly | Strategy, QR | TVL, APY trends, incidents |
| Allocation Drift Report | Weekly | Strategy Board | Per-strategy drift analysis |
| Monte Carlo Summary | Monthly | All Boards | Simulation results |
| Contingency Readiness | Monthly | CEO, Strategy | Plan status, test results |

### 12.2 Report Schemas

```python
class StrategyPerformanceReport:
    """Daily strategy performance report."""
    
    def __init__(self, date: datetime):
        self.date = date
        self.strategies = []
    
    async def generate(self) -> dict:
        """Generate the report."""
        
        for strategy in get_active_strategies():
            strategy_data = {
                "id": strategy["id"],
                "name": strategy["name"],
                "current_apy": await get_current_strategy_apy(strategy["id"]),
                "target_apy_range": strategy["target_apy_range"],
                "within_target": self.is_within_target(strategy),
                "allocation_drift": await calculate_allocation_drift(strategy["id"]),
                "protocol_health": await get_protocol_health_summary(strategy["id"]),
                "alerts_today": get_alerts_for_strategy(strategy["id"], self.date),
                "users_count": count_users_in_strategy(strategy["id"])
            }
            self.strategies.append(strategy_data)
        
        return {
            "report_type": "strategy_performance_daily",
            "date": self.date.isoformat(),
            "generated_at": datetime.utcnow().isoformat(),
            "strategies": self.strategies,
            "summary": {
                "total_strategies": len(self.strategies),
                "strategies_within_target": sum(1 for s in self.strategies if s["within_target"]),
                "strategies_with_alerts": sum(1 for s in self.strategies if s["alerts_today"]),
                "total_users": sum(s["users_count"] for s in self.strategies)
            }
        }
```

---

## 13. API Specifications

### 13.1 Strategy API Endpoints

```yaml
# Strategy Management API
openapi: 3.0.0
info:
  title: Strategy Board API
  version: 1.0.0

paths:
  /api/strategies:
    get:
      summary: List all strategies
      parameters:
        - name: state
          in: query
          schema:
            type: string
            enum: [draft, review, active, paused, retired]
      responses:
        200:
          description: List of strategies
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Strategy'
    
    post:
      summary: Create new strategy
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StrategyCreate'
      responses:
        201:
          description: Strategy created
        400:
          description: Validation error
  
  /api/strategies/{id}:
    get:
      summary: Get strategy by ID
      responses:
        200:
          description: Strategy details
    
    patch:
      summary: Update strategy
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StrategyUpdate'
      responses:
        200:
          description: Update applied or pending validation
  
  /api/strategies/{id}/pause:
    post:
      summary: Pause strategy
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
                  enum: [protocol_incident, extreme_volatility, liquidity_crisis, regulatory_concern, manual_review, data_integrity]
      responses:
        200:
          description: Strategy paused
  
  /api/strategies/{id}/reactivate:
    post:
      summary: Reactivate paused strategy
      responses:
        200:
          description: Strategy reactivated
        400:
          description: Cannot reactivate (checks failed)
  
  /api/strategies/{id}/performance:
    get:
      summary: Get strategy performance metrics
      parameters:
        - name: period
          in: query
          schema:
            type: string
            enum: [1d, 7d, 30d, 90d, 1y]
      responses:
        200:
          description: Performance metrics

  /api/protocols:
    get:
      summary: List all protocols
      parameters:
        - name: state
          in: query
          schema:
            type: string
            enum: [research, whitelisted, active, deprecated, blacklisted]
    
    post:
      summary: Add new protocol
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProtocolCreate'

  /api/protocols/{id}/blacklist:
    post:
      summary: Blacklist a protocol
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
                immediate:
                  type: boolean

  /api/alerts:
    get:
      summary: List alerts
      parameters:
        - name: severity
          in: query
          schema:
            type: string
            enum: [info, warning, high, critical, emergency]
        - name: status
          in: query
          schema:
            type: string
            enum: [open, acknowledged, resolved]
    
  /api/alerts/{id}/acknowledge:
    post:
      summary: Acknowledge an alert
      
  /api/alerts/{id}/resolve:
    post:
      summary: Resolve an alert
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                resolution_notes:
                  type: string

  /api/validations:
    get:
      summary: List validation requests
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, approved, rejected, expired]
    
  /api/validations/{id}/approve:
    post:
      summary: Approve a validation request
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                board:
                  type: string
                notes:
                  type: string

  /api/contingency/check:
    post:
      summary: Manually check contingency triggers
      responses:
        200:
          description: Check results

  /api/reports/strategy-performance:
    get:
      summary: Generate strategy performance report
      parameters:
        - name: date
          in: query
          schema:
            type: string
            format: date
```

---

## 14. Database Schema

### 14.1 Core Tables

```sql
-- Strategies table
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    goal VARCHAR(50) NOT NULL,
    crypto_pct INTEGER NOT NULL CHECK (crypto_pct >= 0 AND crypto_pct <= 100),
    risk_tier VARCHAR(20) NOT NULL,
    target_apy_range VARCHAR(20),
    target_user VARCHAR(100),
    state VARCHAR(20) NOT NULL DEFAULT 'draft',
    allocations JSONB NOT NULL,
    monte_carlo_validated JSONB,
    variance_warning TEXT,
    access_requirements JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Protocols table
CREATE TABLE protocols (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    chain VARCHAR(50) NOT NULL,
    asset VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    crypto_exposure BOOLEAN NOT NULL,
    price_exposure VARCHAR(20),
    defillama_project VARCHAR(100),
    defillama_pool_id VARCHAR(100),
    state VARCHAR(20) NOT NULL DEFAULT 'research',
    risk_score INTEGER CHECK (risk_score >= 1 AND risk_score <= 10),
    min_tvl_usd BIGINT,
    max_allocation_pct INTEGER,
    audit_status JSONB,
    metadata JSONB,
    added_at TIMESTAMP DEFAULT NOW(),
    added_by VARCHAR(50)
);

-- Alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    data JSONB,
    boards_notified TEXT[],
    user_notification BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    acknowledged_at TIMESTAMP,
    acknowledged_by VARCHAR(50),
    resolved_at TIMESTAMP,
    resolved_by VARCHAR(50),
    resolution_notes TEXT
);

-- Validation requests table
CREATE TABLE validation_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,
    requestor VARCHAR(50) NOT NULL,
    subject_id VARCHAR(50),
    changes JSONB NOT NULL,
    validation_requirements JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    deadline TIMESTAMP,
    approvals JSONB DEFAULT '{}'::jsonb
);

-- Strategy events table (audit log)
CREATE TABLE strategy_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id INTEGER REFERENCES strategies(id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Protocol health snapshots
CREATE TABLE protocol_health_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protocol_id VARCHAR(50) REFERENCES protocols(id),
    tvl_usd BIGINT,
    apy DECIMAL(10, 4),
    health_score DECIMAL(5, 4),
    snapshot_at TIMESTAMP DEFAULT NOW()
);

-- Contingency events
CREATE TABLE contingency_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_name VARCHAR(50) NOT NULL,
    trigger_conditions JSONB,
    actions_taken JSONB,
    executed_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    resolution_notes TEXT
);

-- Migration recommendations
CREATE TABLE migration_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id INTEGER REFERENCES strategies(id),
    reason TEXT NOT NULL,
    failed_protocol VARCHAR(50),
    current_allocations JSONB,
    recommended_allocations JSONB,
    affected_users INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Indexes
CREATE INDEX idx_strategies_state ON strategies(state);
CREATE INDEX idx_protocols_state ON protocols(state);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
CREATE INDEX idx_validation_status ON validation_requests(status);
CREATE INDEX idx_protocol_health_snapshot_at ON protocol_health_snapshots(snapshot_at);
```

---

## Appendix A: Dependency Summary

### Dependencies on Other Boards

| Board | Dependency | Section Reference |
|-------|------------|-------------------|
| **QR Board** | Validation interface implementation | Section 7.4 |
| **QR Board** | Health score calculation formula | Section 3.4 |
| **QR Board** | APY range calculation methodology | Section 9.2 |
| **QR Board** | Battle Test runner | Section 7.4 |
| **QR Board** | Monte Carlo runner | Section 7.4 |
| **Rakia** | Protocol evaluation methodology | Section 3.3 |
| **Rakia** | Kamino Lend research | Section 10.3 |
| **Rakia** | GMX V2 research | Section 10.3 |
| **Rakia** | Data collection automation | Section 10.1 |
| **CLO Board** | Protocol approval process | Section 11.1 |
| **CLO Board** | User communication templates | Section 8 |
| **CMO Board** | Alert user notification templates | Section 6.4 |
| **CTO Board** | Implementation of all above | All sections |

### Implementation Priority

| Priority | Component | Dependencies |
|----------|-----------|--------------|
| P0 | Monitoring system | Data collection |
| P0 | Alert system | Monitoring |
| P0 | Contingency automation | Monitoring, Alerts |
| P1 | Validation framework | QR Board interface |
| P1 | Lifecycle management | Validation |
| P2 | Reporting | All above |
| P2 | Full API | All above |

---

## Appendix B: Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-19 | Initial document | Strategy Board |

---

**Document Status:** Ready for CTO Board Implementation

**Next Steps:**
1. CTO Board review and technical feasibility assessment
2. QR Board implements validation interface (Section 7.4)
3. Rakia provides missing research deliverables (Section 10.3)
4. CLO Board approves user communication templates
5. CTO Board begins implementation starting with monitoring (P0)

---

*End of Document*
