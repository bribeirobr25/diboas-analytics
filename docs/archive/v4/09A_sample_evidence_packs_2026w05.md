# Examples

## 1) ep_2026w05_sig_02
```yaml
evidence_pack_id: "ep_2026w05_sig_02"
signal_id: "sig_crypto_risk_stabilized_v1"
edition_id: "adelaide_weekly_2026w05"
created_at: "2026-02-01T04:30:00Z"
claim:
  headline: "Crypto risk-taking stabilized"
  summary: "Leverage tone improved from very cautious to less cautious."
  horizon: "1-8 weeks"
  severity: "medium"
  confidence: 0.66
override: { edition_confidence_override: false, override_reason: null }
disclosures:
  - { type: "none_required", message: "No lag/proxy/derivation disclosures required for this signal. This does not change the educational nature of this commentary." }
drivers:
  - { contract_id: "crypto_btc_perps_funding_v1", feature: "level", value: 0.0001, direction: "up" }
  - { contract_id: "crypto_btc_perps_open_interest_v1", feature: "delta_7d_pct", value: 0.03, direction: "up" }
data_refs:
  - contract_id: "crypto_btc_perps_funding_v1"
    asof_ts: "2026-01-26T09:00:00Z"
    validation_status: "PASS"
    raw_hash: "sha256:mock_raw_02a"
    clean_hash: "sha256:mock_clean_02a"
    raw_to_clean_transform_hash: "sha256:mock_xform_02a"
    pipeline_version: "v4.0.3"
  - contract_id: "crypto_btc_perps_open_interest_v1"
    asof_ts: "2026-01-26T09:00:00Z"
    validation_status: "PASS"
    raw_hash: "sha256:mock_raw_02b"
    clean_hash: "sha256:mock_clean_02b"
    raw_to_clean_transform_hash: "sha256:mock_xform_02b"
    pipeline_version: "v4.0.3"
methods:
  confidence_model: "weighted_evidence_v1"
  components: { data_quality: 0.85, cross_confirmation: 0.55, historical_stability: 0.58, model_agreement: 0.65 }
invalidation_state: { current_status: "valid", last_checked_at: "2026-02-01T05:30:00Z" }
invalidation_conditions:
  - { condition: "crypto_btc_perps_funding_v1.value < 0 AND crypto_btc_perps_open_interest_v1.delta_7d_pct < -0.05", action: "flag_signal_invalid", severity: "medium" }
audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_2026w05_0002"
  approvals:
    - { board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z" }
    - { board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z" }
    - { board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z" }
  edition_id_reference: "adelaide_weekly_2026w05"
```


## 2) ep_2026w05_sig_03
```yaml
evidence_pack_id: "ep_2026w05_sig_03"
signal_id: "sig_borrowing_conditions_key_v1"
edition_id: "adelaide_weekly_2026w05"
created_at: "2026-02-01T04:30:00Z"
claim:
  headline: "Borrowing conditions remain key"
  summary: "Borrowing stress remains a lead indicator worth watching."
  horizon: "1-3 months"
  severity: "high"
  confidence: 0.61
override: { edition_confidence_override: false, override_reason: null }
disclosures:
  - { type: "cadence_lag", message: "Some borrowing-condition proxies update less frequently than daily; timestamps are shown in Layer B. This does not change the educational nature of this commentary." }
drivers:
  - { contract_id: "credit_hy_ig_spread_proxy_v1", feature: "delta_2w_bps", value: +2, direction: "up" }
  - { contract_id: "vol_vix_proxy_v1", feature: "pctl_rank", value: 0.45, direction: "flat" }
data_refs:
  - contract_id: "credit_hy_ig_spread_proxy_v1"
    asof_ts: "2026-01-24T00:00:00Z"
    validation_status: "PASS_WITH_FLAGS"
    raw_hash: "sha256:mock_raw_03a"
    clean_hash: "sha256:mock_clean_03a"
    raw_to_clean_transform_hash: "sha256:mock_xform_03a"
    pipeline_version: "v4.0.3"
  - contract_id: "vol_vix_proxy_v1"
    asof_ts: "2026-01-25T00:00:00Z"
    validation_status: "PASS"
    raw_hash: "sha256:mock_raw_03b"
    clean_hash: "sha256:mock_clean_03b"
    raw_to_clean_transform_hash: "sha256:mock_xform_03b"
    pipeline_version: "v4.0.3"
methods:
  confidence_model: "weighted_evidence_v1"
  components: { data_quality: 0.78, cross_confirmation: 0.52, historical_stability: 0.60, model_agreement: 0.55 }
invalidation_state: { current_status: "valid", last_checked_at: "2026-02-01T05:30:00Z" }
invalidation_conditions:
  - { condition: "credit_hy_ig_spread_proxy_v1.delta_2w_bps < -15 AND vol_vix_proxy_v1.pctl_rank < 0.30", action: "flag_signal_invalid", severity: "medium" }
audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_2026w05_0003"
  approvals:
    - { board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z" }
    - { board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z" }
    - { board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z" }
  edition_id_reference: "adelaide_weekly_2026w05"
```


## 3) ep_2026w05_sig_04
```yaml
evidence_pack_id: "ep_2026w05_sig_04"
signal_id: "sig_stablecoin_health_quiet_v1"
edition_id: "adelaide_weekly_2026w05"
created_at: "2026-02-01T04:30:00Z"
claim:
  headline: "Stablecoin health is quiet"
  summary: "No major stablecoin stress alerts triggered."
  horizon: "1-8 weeks"
  severity: "medium"
  confidence: 0.80
override: { edition_confidence_override: false, override_reason: null }
disclosures:
  - { type: "none_required", message: "No lag/proxy/derivation disclosures required for this signal. This does not change the educational nature of this commentary." }
drivers:
  - { contract_id: "stablecoin_depeg_events_v1", feature: "events_7d", value: 0, direction: "flat" }
data_refs:
  - contract_id: "stablecoin_depeg_events_v1"
    asof_ts: "2026-01-26T11:45:00Z"
    validation_status: "PASS"
    raw_hash: "sha256:mock_raw_04"
    clean_hash: "sha256:mock_clean_04"
    raw_to_clean_transform_hash: "sha256:mock_xform_04"
    pipeline_version: "v4.0.3"
methods:
  confidence_model: "weighted_evidence_v1"
  components: { data_quality: 0.92, cross_confirmation: 0.70, historical_stability: 0.85, model_agreement: 0.78 }
invalidation_state: { current_status: "valid", last_checked_at: "2026-02-01T05:30:00Z" }
invalidation_conditions:
  - { condition: "stablecoin_depeg_events_v1.events_1d >= 1", action: "block_publication", severity: "high" }
audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_2026w05_0004"
  approvals:
    - { board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z" }
    - { board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z" }
    - { board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z" }
  edition_id_reference: "adelaide_weekly_2026w05"
```

## 4) ep_2026w05_sig_05
```yaml
signal_id: "sig_defi_baseline_mixed_v1"
edition_id: "adelaide_weekly_2026w05"
created_at: "2026-02-01T04:30:00Z"
claim:
  headline: "DeFi baseline stable but uneven"
  summary: "Headline stable; breadth uneven; composite sensitivity higher."
  horizon: "1-3 months"
  severity: "low"
  confidence: 0.52
override: { edition_confidence_override: false, override_reason: null }
disclosures:
  - { type: "methodology", message: "DeFi yield benchmark is a composite and can shift with protocol mix changes. This does not change the educational nature of this commentary." }
  - { type: "data_quality", message: "Data heterogeneity reduces cross-confirmation; interpret cautiously. This does not change the educational nature of this commentary." }
drivers:
  - { contract_id: "defi_bluechip_tvl_v1", feature: "delta_2w_pct", value: -0.01, direction: "flat" }
  - { contract_id: "defi_yield_benchmark_v1", feature: "delta_2w_pct", value: +0.02, direction: "up" }
data_refs:
  - contract_id: "defi_bluechip_tvl_v1"
    asof_ts: "2026-01-25T00:00:00Z"
    validation_status: "PASS_WITH_FLAGS"
    raw_hash: "sha256:mock_raw_05a"
    clean_hash: "sha256:mock_clean_05a"
    raw_to_clean_transform_hash: "sha256:mock_xform_05a"
    pipeline_version: "v4.0.3"
  - contract_id: "defi_yield_benchmark_v1"
    asof_ts: "2026-01-25T00:00:00Z"
    validation_status: "PASS_WITH_FLAGS"
    raw_hash: "sha256:mock_raw_05b"
    clean_hash: "sha256:mock_clean_05b"
    raw_to_clean_transform_hash: "sha256:mock_xform_05b"
    pipeline_version: "v4.0.3"
methods:
  confidence_model: "weighted_evidence_v1"
  components: { data_quality: 0.60, cross_confirmation: 0.45, historical_stability: 0.58, model_agreement: 0.52 }
invalidation_state: { current_status: "valid", last_checked_at: "2026-02-01T05:30:00Z" }
invalidation_conditions:
  - { condition: "defi_bluechip_tvl_v1.delta_2w_pct < -0.10 AND vol_vix_proxy_v1.pctl_rank > 0.70", action: "flag_signal_invalid", severity: "medium" }
  - { condition: "defi_yield_benchmark_v1.methodology_version_changed == true", action: "require_correction", severity: "medium" }
audit:
  generated_by: "intelligence_engine_v4"
  gate3_trigger_id: "g3_2026w05_0005"
  approvals:
    - { board: "QR", status: "DATA_VALIDATED", at: "2026-02-01T05:10:00Z" }
    - { board: "Strategy", status: "SIGNAL_APPROVED", at: "2026-02-01T05:20:00Z" }
    - { board: "Compliance", status: "DISCLAIMER_VERIFIED", at: "2026-02-01T05:35:00Z" }
  edition_id_reference: "adelaide_weekly_2026w05"
```