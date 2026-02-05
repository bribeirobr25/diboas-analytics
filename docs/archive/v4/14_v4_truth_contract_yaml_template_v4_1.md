# FILE: 14_v4_truth_contract_yaml_template_v4_1.md

# diBoaS v4 — Truth Contract YAML Template (v4.1)

**Document ID:** V4-CONTRACT-TEMPLATE-001  
**Status:** Enforceable template for registering Phase 0+ metrics  
**Last updated:** 2026-01-26  
**Rule:** No contract = no ingest

This template is the **engineering-ready** Truth Contract format used to register each metric (Phase 0 core contracts and beyond). It extends the v4 Truth Contract spec with $0-reality hardening:

- **History policy** (per-contract backtest depth requirements)
- **Final Truth Snapshot** compatibility (edition snapshot semantics)
- **Methodology drift** tracking for Tier 2/3 sources
- **Zombie API defenses** (null/zero floor checks)
- **Stale value detection** for ghost feeds
- **Collector group** scheduling (heartbeat collector orchestration)

---

## 1) Canonical YAML Template

```yaml
# -----------------------------
# Identity & Governance
# -----------------------------
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

description: "Human description of the metric and why it exists."

# -----------------------------
# Cadence & SLAs
# -----------------------------
cadence:
  expected_update: "eod | hourly | 15m | weekly | monthly"
  timezone: "UTC"

freshness_sla:
  internal_sla: "PT60M"          # ISO 8601 duration
  publication_sla: "PT12H"       # ISO 8601 duration

# Collector orchestration (heartbeat collector)
collector_policy:
  collector_group: "hourly | daily_00utc | weekly | monthly"
  heartbeat_tick: "PT1H"         # expected tick interval for orchestration
  pre_publish_refresh: true
  final_truth_snapshot_role: "depends_on_edition_snapshot"  # see docs: Final Truth Snapshot semantics

# -----------------------------
# History Policy (backtest depth)
# -----------------------------
history_policy:
  backtest_depth_required: "MAX_AVAILABLE | P15Y | P10Y | P6Y | P3Y"
  min_start_date: null           # e.g., "2010-01-01" or null
  reason: "macro regime coverage / data availability / product launch constraints"
  known_coverage_limits: "e.g., perps history starts ~2019; DeFi TVL starts ~2020"

# -----------------------------
# Units & Schema
# -----------------------------
units:
  standard_unit: "percent | decimal | usd | index | rate_per_8h | ..."
  clean_unit: "decimal | usd | index | ..."
  decimals: 6
  conversion:
    required: true
    formula: "clean = standard / 100"

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
    - name: "retrieved_at_ts"
      type: "timestamp"
      required: true
    - name: "source_name"
      type: "string"
      required: true
    - name: "source_tier"
      type: "number"
      required: true

# -----------------------------
# Sources & Methodology Drift Tracking
# -----------------------------
sources:
  canonical:
    name: "FRED | DefiLlama | CoinGecko | ExchangeAPI | ..."
    tier: 1
    uri: "..."
    method:
      # Provider or internal marker for how the source defines/calculates the metric
      source_methodology_version: "provider_version_or_internal_tag"
      methodology_notes: "What the provider means by this metric; known caveats."
  fallback:
    - name: "FallbackSourceName"
      tier: 2
      uri: "..."
      method:
        source_methodology_version: "provider_version_or_internal_tag"
        methodology_notes: "Fallback caveats."

methodology_drift_policy:
  enabled: true
  on_detected_change: "set_pass_with_flags_and_create_task"
  detection_signals:
    - "provider_version_changed"
    - "parser_transform_hash_changed"
    - "schema_changed"
  required_disclosure_label: "methodology_change"

# -----------------------------
# Forward Fill Policy
# -----------------------------
forward_fill_policy:
  allowed: false
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "Crypto must be false. TradFi may allow within policy window."

# -----------------------------
# Derivations & Reconciliation
# -----------------------------
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

# -----------------------------
# Gate Validations (Phase 0 minimum)
# -----------------------------
gate_validations:
  gate1_raw:
    - id: "G1-SCHEMA-001"
    - id: "G1-FRESH-001"
    - id: "G1-SANITY-001"

  gate2_clean:
    - id: "G2-UNIT-001"
    - id: "G2-RECON-001"
    - id: "G2-DERIVE-001"

    # Ghost / stuck pipe detection (timestamps update but value frozen)
    - id: "G2-STALE-VALUE-001"
      stale_value_check:
        enabled: true
        window_n_updates: 4
        rule: "if value unchanged for N consecutive expected updates"
        severity_by_risk_tier:
          critical: "FAIL"
          high: "PASS_WITH_FLAGS"
          medium: "PASS_WITH_FLAGS"
          low: "FLAG_ONLY"
        notes: "Mandatory for Tier 2/3 sources. Optional for Tier 1."

    # Zombie API detection (200 OK but null/zero nonsense)
    - id: "G2-NULL-ZERO-FLOOR-001"
      null_zero_floor_check:
        enabled: true
        field: "value"
        null_is_fail: true
        zero_is_fail: false                 # set true only if zero is invalid for this metric
        invalid_ranges: []                  # optional per metric
        severity_by_risk_tier:
          critical: "FAIL"
          high: "FAIL"
          medium: "PASS_WITH_FLAGS"
          low: "FLAG_ONLY"
        notes: "Prevents '0.0000' yields or null payloads from becoming truth."

  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If forward_fill_policy.allowed == true AND applied == true -> disclosure required"
      - "If derivations.is_derived == true -> derivation disclosure required"
      - "If validation_status == PASS_WITH_FLAGS -> flags disclosure required"
      - "If methodology_drift_policy detects change -> methodology disclosure required"
      - "If cadence lag exists -> cadence_lag disclosure required"

# -----------------------------
# Alerting
# -----------------------------
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
  on_methodology_drift:
    board: "QR Board"
    priority: "high"
  on_zombie_api_detected:
    board: "CTO Board"
    priority: "high"