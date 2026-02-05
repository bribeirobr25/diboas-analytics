# FILE: 05_v4_evidence_pack_spec.md

# diBoaS v4 — Evidence Pack Specification (YAML)

**Document ID:** V4-EVIDENCE-SPEC-001  
**Status:** Enforceable  
**Rule:** No evidence pack = no publish

Evidence Packs are the receipts connecting any published signal to:
- exact data used (contract IDs + timestamps)
- validation statuses
- pipeline version + hashes (reproducibility)
- invalidation rules
- approvals + overrides

---

## Required schema

```yaml
evidence_pack_id: "ep_YYYYwWW_sig_XX"
signal_id: "sig_some_signal_v1"
edition_id: "adelaide_weekly_YYYYwWW"
created_at: "2026-02-01T04:30:00Z"

claim:
  headline: "Human headline"
  summary: "Human summary"
  horizon: "1-8 weeks | 1-3 months | 3-12 months"
  severity: "low | medium | high"
  confidence: 0.72

override:
  edition_confidence_override: false
  override_reason: null

disclosures:
  - type: "cadence_lag | forward_fill | proxy | derivation | methodology | data_quality | pass_with_flags | none_required"
    message: "Disclosure message shown to users (must end with: 'This does not change the educational nature of this commentary.')"

drivers:
  - contract_id: "some_contract_v1"
    feature: "delta_5d_bps"
    value: -10
    direction: "down"

data_refs:
  - contract_id: "some_contract_v1"
    asof_ts: "2026-01-25T21:00:00Z"
    validation_status: "PASS | PASS_WITH_FLAGS | FAIL"
    raw_hash: "sha256:..."
    clean_hash: "sha256:..."
    raw_to_clean_transform_hash: "sha256:..."
    pipeline_version: "v4.0.3"

methods:
  confidence_model: "weighted_evidence_v1"
  components:
    data_quality: 0.85
    cross_confirmation: 0.60
    historical_stability: 0.65
    model_agreement: 0.70

invalidation_state:
  current_status: "valid | flagged | invalid"
  last_checked_at: "2026-02-01T05:30:00Z"

invalidation_conditions:
  - condition: "rates_us10y_real_yield_v1.delta_5d > 0.25"
    action: "flag_signal_invalid | block_publication | require_correction"
    severity: "low | medium | high"

audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_YYYYwWW_0001"
  approvals:
    - {board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z"}
    - {board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z"}
    - {board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z"}
  edition_id_reference: "adelaide_weekly_YYYYwWW"