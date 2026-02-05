# FILE: 03_v4_truth_contract_spec.md

# diBoaS v4 — Truth Contract Specification (YAML)

**Document ID:** V4-CONTRACT-SPEC-001  
**Status:** Enforceable  
**Rule:** No contract = no ingest

Truth Contracts define how a metric is sourced, refreshed, validated, reconciled, transformed, and governed.

---

## Required schema (YAML)

```yaml
contract_id: "rates_us10y_yield_v1"
version: "1.0.0"
domain: "rates | macro | tradfi | crypto | stablecoin | defi | rwa"
risk_tier: "critical | high | medium | low"

owner:
  board: "Rakia"
  steward: "name_or_role"

last_reviewed: "YYYY-MM-DD"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "Human description of the metric."

cadence:
  expected_update: "eod | hourly | 15m | weekly | monthly"
  timezone: "UTC"

freshness_sla:
  internal_sla: "PT60M"          # ISO 8601 duration
  publication_sla: "PT12H"       # ISO 8601 duration

units:
  standard_unit: "percent"       # conceptual unit
  clean_unit: "decimal"          # stored unit
  decimals: 6
  conversion:
    required: true
    formula: "clean = standard / 100"

sources:
  canonical:
    name: "FRED"
    tier: 1
    uri: "..."
  fallback:
    - name: "TradingEconomics"
      tier: 2
      uri: "..."

storage:
  raw_table: "raw.<table>"
  clean_table: "clean.<table>"
  primary_key: ["asof_ts"]

schema:
  fields:
    - name: "asof_ts"
      type: "timestamp"
      required: true
    - name: "value"
      type: "number"
      required: true

forward_fill_policy:
  allowed: false
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "Crypto must be false. TradFi may allow with disclosure."

derivations:
  is_derived: false
  inputs: []
  formula: null
  methodology_version: "1.0.0"

reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 0.0005
    relative: 0.01
  on_breach: "block_clean_promote_and_create_task"

gate_validations:
  gate1_raw:
    - id: "G1-SCHEMA-001"
    - id: "G1-FRESH-001"
    - id: "G1-SANITY-001"
  gate2_clean:
    - id: "G2-UNIT-001"
    - id: "G2-RECON-001"
    - id: "G2-DERIVE-001"
  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If forward_fill_policy.allowed == true AND applied == true -> disclosure required"
      - "If derivations.is_derived == true -> derivation disclosure required"
      - "If validation_status == PASS_WITH_FLAGS -> flags disclosure required"
      - "Disclosures must be non-empty if any forward_fill_policy.allowed == true (and applied) OR derivations used"

alerting:
  on_internal_sla_breach:
    board: "CTO Board"
    priority: "high"
  on_publication_sla_breach:
    board: "CTO Board"
    priority: "critical"
  on_reconciliation_breach:
    board: "QR Board"
    priority: "high"