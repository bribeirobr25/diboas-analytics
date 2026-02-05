# FILE: 07_v4_telemetry_dashboard_spec.md

# diBoaS v4 — Telemetry Dashboard Spec (Phase 0)

**Document ID:** V4-TELEMETRY-001  
**Status:** Enforceable  
**Purpose:** Single pane of glass for Trust Spine health and **final publication arbiter**.

If telemetry says “not eligible,” the system response is: **No**.

---

## 1) Objective
Make trust observable and enforceable across:
- Phase 0 core contracts
- Gate executions (1–4)
- Reconciliation drift
- Evidence Pack validity & invalidation state
- Edition readiness (pre-flight checklist)

---

## 2) Scope (Phase 0)
- Phase 0 contract set (see `02_v4_phase0_core_contracts.md`)
- Gate 1–4 execution logs
- Evidence pack generation + invalidation monitoring
- Alerting/task creation integration

---

## 3) Top-level KPI: Publication Eligibility (Go/No-Go)

### 3.1 Eligibility states
- **GREEN (Eligible):** publish permitted
- **YELLOW (Eligible with flags):** publish blocked by default; requires audited override
- **RED (Not eligible):** publish blocked; override generally forbidden except break-glass rules

### 3.2 Eligibility logic (minimum)
An edition is **Eligible (GREEN)** only if:
1) Gate 4 for the edition == PASS  
2) 3–7 signals selected  
3) All signals have Evidence Packs (schema-valid)  
4) Evidence Packs all have `invalidation_state.current_status == valid`  
5) All referenced contracts meet **publication SLA** at last check  
6) No referenced contracts are FAIL at Gate 1/2  
7) No unresolved **high or critical reconciliation diffs** on referenced contracts (last 7 days)  
8) No open critical/high tasks affecting referenced contracts  
9) All mandatory disclaimers present for the channel + jurisdiction(s)

If any fail → RED.

If only PASS_WITH_FLAGS issues exist but fully disclosed and reconciliations are resolved → YELLOW.

---

## 4) Views / Sections

### 4.1 View A — Trust Spine Freshness (Per Contract)
Table per contract:

| contract_id | risk_tier | last_update_utc | age | internal_sla_status | publication_sla_status | time_to_publication_breach | validation_status | reconciliation_status | forward_fill_applied_recently | disclosures_required_now |

Color rules:
- Green: within SLA
- Yellow: between SLA and 2×SLA (or “time_to_breach < 6h”)
- Red: > 2×SLA or publication SLA breached

**Time-to-breach predictor (required):**
- `time_to_publication_breach` shows “T-minus” time (e.g., 45m) before publication SLA breach.

**Near-real-time contracts (required):**
- For `stablecoin_depeg_events_v1` and other near-real-time contracts, show:
  - `last_checked_at_utc` even if data is unchanged (proves monitoring is live).

---

### 4.2 View B — Gate Health Overview (Last 7d & 30d)
Table:

| gate | total_runs | PASS % | PASS_WITH_FLAGS % | FAIL % | top_failure_reason | MTTR | trend |

Required drilldown:
- click gate -> list of failed runs (contract_id, run_id, timestamp, reason, resolution status, owner)

---

### 4.3 View C — Reconciliation Diffs (Vendor Drift Monitor)
Sortable table:

| contract_id | risk_tier | canonical_vs_fallback_diff | tolerance | timestamp | status | resolved | qr_override | notes |

Rules:
- Any **high/critical** diff unresolved for referenced contracts -> blocks eligibility.
- Overrides must be logged (who/why/when).

---

### 4.4 View D — Evidence Pack Monitor (Receipt Health)
Table:

| evidence_pack_id | signal_id | edition_id | invalidation_status | last_checked | triggered_conditions | downstream_action | notes |

Also include a chronological log:
- invalidation triggered -> signal flagged -> edition blocked -> correction required

---

### 4.5 View E — Edition Readiness (Pre-flight Checklist)
This is the “what will be published next” view.

#### 4.5.1 Proposed Signal Set
| signal_id | headline | severity | confidence | evidence_pack_id | invalidation_status | signal_freshness_ok |

`signal_freshness_ok = yes` only if all referenced contracts meet publication SLA at last check.

#### 4.5.2 Dependency Map
Show which contracts each signal depends on:
- signal -> contracts -> freshness/gate/recon statuses

#### 4.5.3 Blocking Issues
List:
- publication SLA breaches
- Gate FAIL
- unresolved diffs
- invalidation flagged/invalid
- missing disclaimers / Gate 4 FAIL

---

## 5) Alerting and task creation

### 5.1 Severity routing
- **Critical:** immediate task to owning board + CTO (priority=critical)
- **High:** business-day response (priority=high)
- **Medium/Low:** batched daily summary

### 5.2 Alert triggers (minimum)
- publication SLA breach on any critical contract
- Gate 1/2 FAIL spike (PASS < 95% in last 24h for critical contracts)
- reconciliation diff breach on high/critical contracts
- evidence pack invalidation for a signal in next scheduled edition
- eligibility status changes from green -> yellow/red

### 5.3 Daily summary
Daily summary message includes:
- freshness drift outliers
- reconciliation top diffs
- gate fail hotspots
- invalidations triggered
- current eligibility for next edition

---

## 6) Audit and governance requirements
- Log every:
  - eligibility decision (who/what/when)
  - override (who/why/when)
  - export/download action (who/when/edition_id if applicable)
- Trust Score formula (if used) must be:
  - versioned (e.g. `trust_score_v1`)
  - change-controlled via QR Board review

---

## 7) Break-glass protocol (explicit)
Break-glass is an emergency override path. It is intentionally painful.

**Break-glass MAY be used only if:**
- edition is RED due to SLA breach or reconciliation delay,
- AND there are no Gate 4 prohibited language violations,
- AND compliance approves disclosure language.

**Break-glass FORBIDDEN if:**
- Gate 4 has any Rule Group A prohibited phrase violations (no exceptions),
- or recommendation-likeness classifier FAIL.

Break-glass requirements:
- dual sign-off (CTO + Compliance) + recorded reason
- forced edition_version bump
- forced public note in edition header (web canonical)
- postmortem required within 72h

---

## 8) Risk-tier visual hierarchy (required)
Dashboard must visually separate:
- Critical contracts (top section, always visible)
- High/Medium/Low (below, collapsible)

Low-risk staleness must not drown critical failures.

---

## 9) Phase 0 exit criteria
Phase 0 is complete when:
- 100% Phase 0 contracts have Truth Contracts in repo
- Telemetry shows:
  - Gate PASS >= 95% for last 7 days
  - zero open critical tasks older than 24h
  - zero unresolved high/critical reconciliation diffs older than 24h for referenced contracts
- One full weekly edition produced end-to-end with:
  - GREEN eligibility at send time
  - valid evidence packs for every signal
  - Gate 4 PASS