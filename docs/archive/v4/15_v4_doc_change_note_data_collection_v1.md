# FILE: 15_v4_doc_change_note_data_collection_v1.md

# diBoaS v4 — Change Note: Data Collection Plan Updates (v1)

**Document ID:** V4-DATA-PLAN-CHANGES-001  
**Last updated:** 2026-01-26  
**Purpose:** Precise instructions to update `13_v4_data_collection_plan_zero_budget.md` and keep it as the single source of truth.

This change note exists so reviewers can see exactly what changed without diff-hunting.

---

## A) Rewrite policy (what to do)
1) Update `13_v4_data_collection_plan_zero_budget.md` **in place**.
2) Bump its header:
   - `Last updated: 2026-01-26`
   - optionally add `Revision: v1.1` (if you want simple doc versioning)
3) Add `14_v4_truth_contract_yaml_template_v4_1.md` to the documentation index.

---

## B) Additions to `13_v4_data_collection_plan_zero_budget.md`

### 1) Section §7: Heartbeat Collector + Pre-publish refresh
**Add a new subsection titled: “Final Truth Snapshot (Edition Snapshot Semantics)”**

Include these bullets verbatim-level strictness:

- `final_truth_snapshot_ts` is the **single timestamp** used to determine edition eligibility.
- Default: `Sunday 04:00 UTC` (configurable).
- For each contract: select latest observation where `asof_ts <= final_truth_snapshot_ts`.
- If any referenced contract is missing, stale, or fails publication SLA at snapshot time:
  - Telemetry => RED
  - Publication => BLOCKED
  - Tasks => created with severity based on risk tier

### 2) Section §8: Auditability rules
**Add explicit requirement:**
- Every stored observation must include `retrieved_at_ts`.

**Add explicit vintage/revision note:**
- If the source supports vintages/revisions (e.g., macro series), Evidence Packs must preserve what was seen at retrieval time.

### 3) Section §10: Failure modes and mitigations
**Add a new mitigation titled: “Zombie API / Null-Zero Floor Checks”**

- Define: “200 OK but null/zero/placeholder values are treated as failure.”
- Add a short config snippet (or prose rule) matching the template’s `null_zero_floor_check`.

**Clarify stale_value_check enforcement:**
- Mandatory for Tier 2/3 sources.
- Severity determined by `risk_tier` (critical/high stricter than low).

### 4) Section §3 (Source policy) or §12 (Organization)
**Add requirement: “Methodology drift tracking”**

- Each contract must declare `source_methodology_version` (provider-defined or internal tag).
- If methodology changes are detected (version change, parser hash change, schema change):
  - set `PASS_WITH_FLAGS`
  - create a QR task
  - require disclosure if referenced in a published edition

### 5) Section §2 (What we collect)
**Add an optional macro proxy:**
- `macro_us_m2_money_supply_v1` (monthly)
- Mandatory `cadence_lag` disclosure if referenced

---

## C) Removals / edits (tighten wording)
- Anywhere the doc implies “forward-fill solves weekends,” rewrite to:
  - “Alignment uses latest <= snapshot time; forward-fill only where contract allows and must be disclosed.”
- Anywhere “pre-publish refresh” sounds optional, make it **required** for Phase 0.

---

## D) Index update
Update `00_INDEX.md`:
- Add:
  - `13_v4_data_collection_plan_zero_budget.md`
  - `14_v4_truth_contract_yaml_template_v4_1.md`
  - `15_v4_doc_change_note_data_collection_v1.md`