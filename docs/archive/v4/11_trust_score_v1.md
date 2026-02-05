# FILE: 11_trust_score_v1.md

# diBoaS v4 — Trust Score v1 Specification

**Document ID:** KPI-TS-001  
**KPI ID:** trust_score_v1  
**Status:** DRAFT (enforceable once QR + Compliance sign-off is recorded)  
**Owner:** QR Board (definition) + CTO Board (implementation)  
**Last reviewed:** 2026-01-26  
**Change control:** Any change requires QR Board review + version bump + changelog entry

This defines a single **versioned** KPI that summarizes Trust Spine health into one number **without replacing hard blockers**.

If you try to use Trust Score to “greenwash” a red system, the correct response is: no.

---

## 1) Purpose

Trust Score answers: **“How reliable is this signal/edition right now?”** using telemetry-backed inputs:
- Gate PASS rates
- freshness vs SLAs
- reconciliation drift
- evidence pack invalidation state
- open tasks affecting referenced contracts

It exists to:
- help humans triage (what’s weak and why)
- provide a stable KPI on the dashboard
- create consistent confidence framing across outputs (especially Layer B)

It does **not** override:
- Adelaide hard publication blockers (`06_v4_adelaide_weekly_output_contract.md`)
- Gate 4 compliance (`08_gate4_compliance_ruleset_v1.md`)

---

## 2) Where Trust Score is used

### 2.1 Telemetry dashboard
- Display edition-level trust score
- Display per-signal trust score
- Show component breakdown and top penalties

### 2.2 Evidence Packs
Evidence Packs must store the Trust Score snapshot at generation time:
- aggregate score
- component scores
- version
- timestamp

### 2.3 Editorial guidance (optional policy hooks)
- If score is borderline, require an extra caveat sentence in Layer A
- If score is low, block signal or force manual review (configurable policy)

---

## 3) Definitions (objects scored)

Trust Score can be calculated for:
- **Contract** (single Truth Contract health snapshot)
- **Signal** (set of referenced contracts + Gate 3 outputs)
- **Edition** (set of signals + overall Gate/G4 status)

This spec defines:
- `trust_score_contract_v1`
- `trust_score_signal_v1`
- `trust_score_edition_v1`

All use the same components and weights.

---

## 4) Output format (canonical)

### 4.1 Canonical JSON payload (stored in telemetry and/or evidence packs)
```json
{
  "trust_score_v1": {
    "scope": "signal",
    "aggregate": 0.72,
    "components": {
      "dq": 0.85,
      "cc": 0.60,
      "rs": 0.80,
      "ops": 0.65
    },
    "penalties": [
      {
        "type": "freshness_near_breach",
        "target": "credit_hy_ig_spread_proxy_v1",
        "amount": 0.05,
        "explanation": "Contract is within 6h of publication SLA breach."
      }
    ],
    "version": "1.0.0",
    "calculated_at": "2026-02-01T05:30:00Z"
  }
}