# STRATEGY BOARD — PENDING TASK TRACKER

**Last Updated:** February 4, 2026  
**Source:** Full run review of diboas-analytics v3 (Feb 3, 2026)  
**Launch Date:** February 12, 2026

---

## 📊 SUMMARY

| Priority | Count | Status |
|----------|-------|--------|
| 🔴 P0 Critical | 0 | ✅ All resolved |
| 🟠 P1 High | 2 | ⏳ In progress |
| 🟡 P2 Medium | 4 | 📅 Post-launch |
| 🟢 P3 Low | 2 | 📅 Q2 2026 |

**Launch Readiness:** ✅ APPROVED (with conditions)

---

## ✅ P0 CRITICAL — ALL RESOLVED

| ID | Task | Resolution | Date |
|----|------|------------|------|
| STR-P0-1 | 30% Sky concentration cap | ✅ Implemented in strategies.json v2.1.0 | Feb 3, 2026 |
| STR-P0-2 | USDC/USDT depeg detection | ✅ 6 triggers implemented (L2/L3/L4) | Feb 3, 2026 |
| STR-P0-3 | Strategy allocations valid | ✅ All 10 strategies validated | Feb 4, 2026 |
| STR-P0-4 | Hypothetical performance disclaimer | ✅ Present in all outputs | Feb 3, 2026 |

---

## 🟠 P1 HIGH PRIORITY — PRE-LAUNCH

### STR-P1-1: Missing Data Files

| Field | Value |
|-------|-------|
| **Status** | ⏳ PENDING — Handoff to CTO Board |
| **Owner** | CTO Board |
| **Dependency** | None |
| **Blocking** | Partial — Some triggers disabled |
| **Deadline** | Feb 6, 2026 |

**Description:**  
12 CSV files missing from `data/` directory. Disables wallet triggers and some macro triggers.

**Missing Files:**
- Wallet: `estate_wallet_tracker.csv`, `whale_wallet_master_list.csv`, `market_maker_wallet_tracker.csv`, `protocol_treasury_tracker.csv`
- Institutional: `btc_etf_holdings.csv`, `corporate_btc_holdings.csv`, `institutional_13f.csv`
- Macro: `aaii_sentiment.csv`, `credit_spreads.csv`, `global_liquidity.csv`, `treasury_yields.csv`, `real_yields.csv`

**Action:** CTO Board to copy files from project folder or run collectors.

**Handoff Document:** `docs/STRATEGY_BOARD_CTO_DATA_HANDOFF.md`

---

### STR-P1-2: Verify All Triggers Fire Correctly

| Field | Value |
|-------|-------|
| **Status** | ⏳ PENDING — After data files populated |
| **Owner** | Strategy Board + CTO Board |
| **Dependency** | STR-P1-1 |
| **Blocking** | No |
| **Deadline** | Feb 7, 2026 |

**Description:**  
After data files are populated, run full pipeline and verify:
- At least one trigger from each category fires in test
- Cooldown manager persists state correctly
- Alert consolidation groups related alerts

**Acceptance Criteria:**
- [ ] Protocol triggers: ≥1 fires
- [ ] Market triggers: ≥1 fires
- [ ] Wallet triggers: ≥1 fires
- [ ] Macro triggers: ≥1 fires
- [ ] Cooldown state file created
- [ ] Consolidated alerts appear in output

---

## 🟡 P2 MEDIUM PRIORITY — POST-LAUNCH ACCEPTABLE

### STR-P2-1: Rebalancing Engine

| Field | Value |
|-------|-------|
| **Status** | 📅 POST-LAUNCH |
| **Owner** | CTO Board (implement) → Strategy Board (validate) |
| **Dependency** | None |
| **Target** | Q1 2026 (March) |

**Description:**  
Implement rebalancing suggestions when portfolio drifts from target allocation.

**Specification (from Session 016):**
```python
REBALANCING_THRESHOLDS = {
    "Minimal": {"suggest": 10, "force": 15},
    "Low": {"suggest": 10, "force": 15},
    "Low-Medium": {"suggest": 12, "force": 18},
    "Medium": {"suggest": 12, "force": 18},
    "High": {"suggest": 15, "force": 22},
    "Very High": {"suggest": 15, "force": 25},
}
```

**Drift Calculation (approved):**
```python
if target_pct >= 10:
    relative_drift = absolute_drift / target_pct * 100
    return max(absolute_drift, relative_drift)
return absolute_drift  # For tiny positions
```

**Workaround:** Adelaide can include manual guidance on rebalancing.

---

### STR-P2-2: Protocol Failure Scenarios in Monte Carlo

| Field | Value |
|-------|-------|
| **Status** | 📅 POST-LAUNCH |
| **Owner** | QR Board (spec) → CTO Board (implement) |
| **Dependency** | None |
| **Target** | Q1 2026 (March) |

**Description:**  
Add protocol-specific failure scenarios to Monte Carlo simulations.

**Specification (from Session 016):**
```python
PROTOCOL_FAILURE_SCENARIOS = {
    "sky_depeg": {"probability_annual": 0.02, "loss_if_occurs": 0.50},
    "aave_exploit": {"probability_annual": 0.01, "loss_if_occurs": 0.30},
    "sanctum_failure": {"probability_annual": 0.03, "loss_if_occurs": 0.80},
    "compound_exploit": {"probability_annual": 0.01, "loss_if_occurs": 0.30},
    "jlp_il_event": {"probability_annual": 0.05, "loss_if_occurs": 0.40},
    "jito_slashing": {"probability_annual": 0.02, "loss_if_occurs": 0.20},
}
```

**Current State:** Monte Carlo uses 4-regime switching (bull, bear, crash, recovery) which captures market-wide risk but not protocol-specific tail events.

**Impact:** May understate tail risks for specific protocols.

---

### STR-P2-3: Cross-Strategy Correlation Detection

| Field | Value |
|-------|-------|
| **Status** | 📅 POST-LAUNCH |
| **Owner** | CTO Board |
| **Dependency** | None |
| **Target** | Q2 2026 |

**Description:**  
Detect when multiple strategies are affected by correlated risks (e.g., all Solana strategies during SOL crash).

**Specification:** Strategy Board CTO Handoff Section 8

**Current State:** Not mentioned in CTO audit. Alert consolidator groups by category but doesn't detect cross-strategy correlation.

---

### STR-P2-4: Escalation Path Verification

| Field | Value |
|-------|-------|
| **Status** | 📅 POST-LAUNCH |
| **Owner** | CTO Board |
| **Dependency** | None |
| **Target** | Q1 2026 |

**Description:**  
Verify escalation flow: P0 → Strategy Board → CEO Board

**Current State:** Crisis management exists (5 components per CTO audit) but escalation path not explicitly verified.

---

## 🟢 P3 LOW PRIORITY — Q2 2026

### STR-P3-1: Per-Trigger Cooldown Configuration

| Field | Value |
|-------|-------|
| **Status** | 📅 Q2 2026 |
| **Owner** | CTO Board |
| **Target** | Q2 2026 |

**Description:**  
Implement different cooldown periods per trigger type instead of global 60-minute default.

**Specification:**
| Trigger Type | Cooldown |
|--------------|----------|
| Price movement | 15 min |
| Protocol health | 60 min |
| Wallet movement | 4 hours |
| Macro indicator | 24 hours |

**Current State:** Global 60-minute default works for launch.

---

### STR-P3-2: Antithetic Variates for Monte Carlo

| Field | Value |
|-------|-------|
| **Status** | 📅 Q2 2026 |
| **Owner** | QR Board (spec) → CTO Board (implement) |
| **Target** | Q2 2026 |

**Description:**  
Implement variance reduction technique for Monte Carlo efficiency.

**Current State:** 5,000 simulations provide adequate convergence for launch.

---

## ✅ COMPLETED ITEMS

| ID | Task | Resolution | Date |
|----|------|------------|------|
| STR-C-1 | 30% Sky cap decision | ✅ Option D approved | Feb 1, 2026 |
| STR-C-2 | Rebalancing thresholds decision | ✅ 10%/15% approved | Feb 1, 2026 |
| STR-C-3 | Drift calculation fix decision | ✅ Relative formula approved | Feb 1, 2026 |
| STR-C-4 | Protocol failure Monte Carlo decision | ✅ Methodology approved | Feb 1, 2026 |
| STR-C-5 | MEV Searchers | ✅ Dropped (defer to v4) | Feb 1, 2026 |
| STR-C-6 | Strategy 2 rename | ✅ "Beat Inflation" | Jan 19, 2026 |
| STR-C-7 | RWA in allocations | ✅ Blocked by CLO (data only) | Feb 1, 2026 |
| STR-C-8 | Identical minimal allocations | ✅ Acceptable | Feb 1, 2026 |
| STR-C-9 | Trigger categories structure | ✅ 4 categories implemented | Feb 3, 2026 |
| STR-C-10 | Regime classifier | ✅ 6 regimes + template mapping | Feb 3, 2026 |
| STR-C-11 | Alert consolidation (Jaccard) | ✅ Implemented | Feb 3, 2026 |
| STR-C-12 | Cooldown manager | ✅ File-based persistence | Feb 3, 2026 |
| STR-C-13 | Crisis detection | ✅ VIX, depeg, exploit thresholds | Feb 3, 2026 |

---

## 🔗 DEPENDENCY CHAIN

```
STR-P1-1 (CTO: Populate data files)
    ↓
STR-P1-2 (Strategy + CTO: Verify triggers)
    ↓
Launch Readiness ✅
```

```
STR-P2-1 (Rebalancing Engine)
    → Independent, can be added post-launch
    
STR-P2-2 (Protocol Failure Monte Carlo)
    → QR Board spec needed first
    → CTO Board implements
```

---

## 📅 TIMELINE

| Date | Milestone |
|------|-----------|
| Feb 4 | ✅ Strategy Board review complete |
| Feb 5 | CTO Board: Copy data files |
| Feb 6 | CTO Board: Verify pipeline runs |
| Feb 7 | Strategy Board: Verify triggers fire |
| Feb 8-11 | Final testing and bug fixes |
| **Feb 12** | **🚀 LAUNCH** |
| Mar 2026 | P2 items: Rebalancing, Protocol Failure MC |
| Q2 2026 | P3 items: Per-trigger cooldowns, Antithetic variates |

---

## 📋 BOARD HANDOFFS

| To Board | Document | Status |
|----------|----------|--------|
| CTO Board | `docs/STRATEGY_BOARD_CTO_DATA_HANDOFF.md` | ✅ Created |
| QR Board | Protocol failure Monte Carlo spec request | 📅 Post-launch |
| CMO Board | Rebalancing guidance in Adelaide (workaround) | 📅 If needed |

---

## 📊 METRICS

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| P0 items resolved | 4/4 | 4/4 | ✅ |
| P1 items resolved | 2/2 | 0/2 | ⏳ |
| Strategy allocations valid | 10/10 | 10/10 | ✅ |
| Triggers implemented | 35+ | 27 | ⚠️ (missing data) |
| Validation rules passing | 70/70 | 70/70 | ✅ |

---

*Last updated by Strategy Board — February 4, 2026*
