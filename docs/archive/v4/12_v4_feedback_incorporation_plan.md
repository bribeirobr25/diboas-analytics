# FILE: 12_v4_feedback_incorporation_plan.md

# diBoaS v4 — Feedback Incorporation Plan (Post–Trust Score Review)

**Status:** READY (repo-ready)  
**Objective:** Capture the *useful* feedback points, explain why they matter, and specify exactly which v4 documents must be updated and how.

This is not a “nice to have” memo. These changes close real-world failure modes: broken pipes that look healthy, quota blowups, multi-language compliance leaks, and governance drift.

---

## 1) Useful Feedback Points (What to keep)

### FP-01 — Make `cc_map_v1.yaml` Governance Explicit
**Why useful:** Cross-confirmation is the easiest thing to “adjust” to make Trust Score look better. If governance isn’t explicit, someone will eventually “tune” it under pressure.

**Impact:** Prevents gaming; makes audits defensible.

**Update targets:**
- `11_trust_score_v1.md`
- (new file) `cc_map_v1.yaml` header block

**What to add:**
- Owner + reviewers + versioning rules for CC map.
- Mandatory Strategy review (because CC assumptions are market/strategy-dependent, not purely QA).

---

### FP-02 — OPS Penalty for “Pending Gate 4 Findings”
**Why useful:** Your system can be “green” operationally but still “fragile” editorially. If Gate 4 is PASS_WITH_FLAGS (or findings pending resolution), Trust Score should reflect that.

**Impact:** Encourages teams to resolve compliance flags early, not 5 minutes before publishing.

**Update targets:**
- `11_trust_score_v1.md`

**What to add:**
- New OPS penalty:
  - `pending_gate4_findings → -0.08`
- Include in penalties list output.

---

### FP-03 — Make Trust Score Mandatory in Evidence Packs
**Why useful:** If Trust Score is optional, it won’t exist when you need it most. Evidence Packs are the “receipt.” The score snapshot must be part of that receipt.

**Impact:** Reproducibility and audit completeness.

**Update targets:**
- `v4-evidence-pack-spec.md` (your Evidence Pack spec file)

**What to add:**
- `trust_score_v1` as a **required** object:
  - `aggregate`
  - `components`
  - `penalties`
  - `version`
  - `calculated_at`

---

### FP-04 — Add a Concrete “Policy Hook” Example for Low Trust
**Why useful:** Engineering needs deterministic rules. “Use Trust Score” is vague. A policy hook shows how content changes when trust is low, without turning it into advice.

**Impact:** Consistent editorial behavior; fewer debates.

**Update targets:**
- `11_trust_score_v1.md`
- optionally `06_v4_adelaide_weekly_output_contract.md` (output contract)

**What to add (example):**
- If `trust_score < 0.60`:
  - add Layer A caveat sentence:  
    “This insight has lower overall system confidence due to **[top_penalty]**.”
  - require QR review flag in Layer B.

---

### FP-05 — Add “Ghost Signal” / Stuck Pipe Detection (`stale_value_check`)
**Why useful:** Free or flaky APIs can “update” timestamps but freeze values. Freshness checks alone won’t catch this. Markets rarely print identical values across many intervals unless something is broken.

**Impact:** Prevents silently broken feeds from producing “valid” signals.

**Update targets:**
- `v4-truth-contract-spec.md` (Truth Contract template)
- `VALIDATION_GATES_CTO_HANDOFF.md` or your Gate 2 validation spec doc (where Gate 2 rules live)
- `07_v4_telemetry_dashboard_spec.md` (telemetry display)

**What to add:**
- In Truth Contract template:
  ```yaml
  gate2_validations:
    stale_value_check:
      enabled: true
      window_n_updates: 4
      rule: "if value unchanged for N consecutive expected updates"
      severity_by_risk_tier:
        critical: "FAIL"
        high: "PASS_WITH_FLAGS"
        medium: "PASS_WITH_FLAGS"
        low: "FLAG_ONLY"