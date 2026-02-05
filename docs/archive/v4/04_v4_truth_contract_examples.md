# FILE: 04_v4_truth_contract_examples.md

# diBoaS v4 — Truth Contract Examples

**Document ID:** V4-CONTRACT-EXAMPLES-001  
**Status:** Examples conforming to `V4-CONTRACT-SPEC-001`

These examples cover:
- TradFi EOD data with optional forward-fill (disclosed)
- Explicit derived metric formula (2s10s)
- Crypto high-frequency metric with no forward-fill
- RWA flows with explicit derivation and lag disclosure

---

## Example A — US 10Y Yield (TradFi EOD; forward-fill allowed with disclosure)

```yaml
contract_id: "rates_us10y_yield_v1"
version: "1.0.0"
domain: "rates"
risk_tier: "critical"

owner:
  board: "Rakia"
  steward: "rates_owner"

last_reviewed: "2026-01-26"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "US 10-year Treasury yield (EOD close)."

cadence:
  expected_update: "eod"
  timezone: "UTC"

freshness_sla:
  internal_sla: "P1D"
  publication_sla: "P2D"

units:
  standard_unit: "percent"
  clean_unit: "decimal"
  decimals: 6
  conversion:
    required: true
    formula: "clean = standard / 100"

sources:
  canonical:
    name: "FRED"
    tier: 1
    uri: "fred:..."
  fallback:
    - name: "TradingEconomics"
      tier: 2
      uri: "te:..."

storage:
  raw_table: "raw.treasury_yields"
  clean_table: "clean.treasury_yields"
  primary_key: ["asof_ts"]

schema:
  fields:
    - { name: "asof_ts", type: "timestamp", required: true }
    - { name: "value", type: "number", required: true }

forward_fill_policy:
  allowed: true
  max_window: "P1D"
  disclosure_label: "forward_fill_applied"
  notes: "Allowed for TradFi holidays/weekends. If applied, must disclose in Evidence Pack and Layer A when referenced."

derivations:
  is_derived: false
  inputs: []
  formula: null
  methodology_version: "1.0.0"

reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 0.0007
    relative: 0.02
  on_breach: "block_clean_promote_and_create_task"

gate_validations:
  gate1_raw:
    - { id: "G1-SCHEMA-001" }
    - { id: "G1-FRESH-001" }
    - { id: "G1-SANITY-001" }
  gate2_clean:
    - { id: "G2-UNIT-001" }
    - { id: "G2-RECON-001" }
  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If forward_fill_policy.allowed == true AND applied == true -> disclosure required"
      - "Disclosures must end with: 'This does not change the educational nature of this commentary.'"

alerting:
  on_internal_sla_breach: { board: "CTO Board", priority: "high" }
  on_publication_sla_breach: { board: "CTO Board", priority: "critical" }
  on_reconciliation_breach: { board: "QR Board", priority: "high" }
```


## Example B — 2s10s Spread Derived Explicit Formula

```yaml
contract_id: "rates_2s10s_spread_v1"
version: "1.0.0"
domain: "rates"
risk_tier: "high"

owner:
  board: "Rakia"
  steward: "rates_owner"

last_reviewed: "2026-01-26"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "2s10s yield curve spread: US 10Y minus US 2Y."

cadence:
  expected_update: "eod"
  timezone: "UTC"

freshness_sla:
  internal_sla: "P1D"
  publication_sla: "P2D"

units:
  standard_unit: "percent"
  clean_unit: "decimal"
  decimals: 6
  conversion:
    required: true
    formula: "clean = standard / 100"

sources:
  canonical:
    name: "Derived"
    tier: 1
    uri: "derived:rates_us10y_yield_v1 - rates_us2y_yield_v1"
  fallback: []

storage:
  raw_table: "raw.derived"
  clean_table: "clean.curve_spreads"
  primary_key: ["asof_ts"]

schema:
  fields:
    - { name: "asof_ts", type: "timestamp", required: true }
    - { name: "value", type: "number", required: true }

forward_fill_policy:
  allowed: true
  max_window: "P1D"
  disclosure_label: "forward_fill_applied"
  notes: "If either input is forward-filled, this derived metric inherits disclosure requirements."

derivations:
  is_derived: true
  inputs: ["rates_us10y_yield_v1", "rates_us2y_yield_v1"]
  formula: "clean.rates_us10y_yield_v1.value - clean.rates_us2y_yield_v1.value"
  methodology_version: "1.0.0"

reconciliation:
  required: false
  compare_to: null
  tolerance_band: { absolute: null, relative: null }
  on_breach: "n/a"

gate_validations:
  gate1_raw:
    - { id: "G1-SCHEMA-001" }
    - { id: "G1-FRESH-001" }
  gate2_clean:
    - { id: "G2-UNIT-001" }
    - { id: "G2-DERIVE-001" }
  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If derivations.is_derived == true -> derivation disclosure required"
      - "Disclosures must be non-empty if derivations used"

alerting:
  on_internal_sla_breach: { board: "CTO Board", priority: "high" }
  on_publication_sla_breach: { board: "CTO Board", priority: "critical" }
```


## Example C — BTC Perps Funding - Crypto Forward Fill Banned

```yaml
contract_id: "crypto_btc_perps_funding_v1"
version: "1.0.0"
domain: "crypto"
risk_tier: "high"

owner:
  board: "Rakia"
  steward: "crypto_owner"

last_reviewed: "2026-01-26"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "BTC perpetual futures funding rate (standardized to rate per 8h)."

cadence:
  expected_update: "hourly"
  timezone: "UTC"

freshness_sla:
  internal_sla: "PT60M"
  publication_sla: "PT12H"

units:
  standard_unit: "rate_per_8h"
  clean_unit: "decimal"
  decimals: 8
  conversion:
    required: false
    formula: null

sources:
  canonical:
    name: "ExchangeAggregate"
    tier: 2
    uri: "agg:funding_rate_btc_perps"
  fallback:
    - name: "SecondaryAggregate"
      tier: 3
      uri: "agg2:funding_rate_btc_perps"

storage:
  raw_table: "raw.crypto_perps"
  clean_table: "clean.crypto_perps"
  primary_key: ["asof_ts", "venue"]

schema:
  fields:
    - { name: "asof_ts", type: "timestamp", required: true }
    - { name: "venue", type: "string", required: true }
    - { name: "value", type: "number", required: true }

forward_fill_policy:
  allowed: false
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "Crypto is 24/7. Forward-fill creates ghost data. Forbidden."

derivations:
  is_derived: true
  inputs: ["raw.crypto_perps.*"]
  formula: "weighted_median_by_oi(value) across venues"
  methodology_version: "1.0.0"

reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 0.0002
    relative: 0.25
  on_breach: "create_task_and_set_pass_with_flags"

gate_validations:
  gate1_raw:
    - { id: "G1-SCHEMA-001" }
    - { id: "G1-FRESH-001" }
    - { id: "G1-SANITY-001" }
  gate2_clean:
    - { id: "G2-UNIT-001" }
    - { id: "G2-DERIVE-001" }
    - { id: "G2-RECON-001" }
  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If validation_status == PASS_WITH_FLAGS -> flags disclosure required"

alerting:
  on_internal_sla_breach: { board: "CTO Board", priority: "high" }
  on_publication_sla_breach: { board: "CTO Board", priority: "critical" }
  on_reconciliation_breach: { board: "QR Board", priority: "high" }
```


## Example D — RWA Tokenized Treasury Net Flows - Derived Disclosure

```yaml
contract_id: "rwa_tokenized_treasury_net_flows_v1"
version: "1.0.0"
domain: "rwa"
risk_tier: "high"

owner:
  board: "Rakia"
  steward: "rwa_owner"

last_reviewed: "2026-01-26"
deprecation_policy: "notify 90d before removal"

change_control:
  requires_qr_review: true
  review_board: "QR Board"
  min_review_days: 7

description: "Daily net flows for tokenized Treasury products (derived from TVL/NAV delta if direct flow data not available)."

cadence:
  expected_update: "eod"
  timezone: "UTC"

freshness_sla:
  internal_sla: "P2D"
  publication_sla: "P3D"

units:
  standard_unit: "usd"
  clean_unit: "usd"
  decimals: 2
  conversion:
    required: false
    formula: null

sources:
  canonical:
    name: "IssuerAndOnchain"
    tier: 2
    uri: "issuer+onchain:rwa_treasury_products"
  fallback:
    - name: "Aggregator"
      tier: 3
      uri: "agg:rwa_treasury_products"

storage:
  raw_table: "raw.rwa_treasuries"
  clean_table: "clean.rwa_treasuries"
  primary_key: ["asof_ts", "product_id"]

schema:
  fields:
    - { name: "asof_ts", type: "timestamp", required: true }
    - { name: "product_id", type: "string", required: true }
    - { name: "value", type: "number", required: true }

forward_fill_policy:
  allowed: false
  max_window: "P0D"
  disclosure_label: "forward_fill_applied"
  notes: "RWA issuer data can lag; do not forward-fill. Use lag disclosure."

derivations:
  is_derived: true
  inputs: ["rwa_tokenized_treasury_tvl_nav_v1"]
  formula: "clean.rwa_tokenized_treasury_tvl_nav_v1.value_delta_1d"
  methodology_version: "1.0.0"

reconciliation:
  required: true
  compare_to: "fallback"
  tolerance_band:
    absolute: 5000000
    relative: 0.10
  on_breach: "create_task_and_set_pass_with_flags"

gate_validations:
  gate1_raw:
    - { id: "G1-SCHEMA-001" }
    - { id: "G1-FRESH-001" }
  gate2_clean:
    - { id: "G2-DERIVE-001" }
    - { id: "G2-RECON-001" }
  gate4_publication:
    compliance_ruleset_required: "gate4_compliance_ruleset_v1"
    disclosure_rules:
      - "If derivations.is_derived == true -> derivation disclosure required"
      - "If cadence lag exists -> cadence_lag disclosure required"
      - "Disclosures must end with: 'This does not change the educational nature of this commentary.'"

alerting:
  on_internal_sla_breach: { board: "CTO Board", priority: "high" }
  on_publication_sla_breach: { board: "CTO Board", priority: "critical" }
  on_reconciliation_breach: { board: "QR Board", priority: "high" }
```