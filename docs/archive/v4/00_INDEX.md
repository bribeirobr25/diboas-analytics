# FILE: 00_INDEX.md

# diBoaS-Analytics v4 Repo Docs Bundle (Generated)

**Status:** Current working set (overwrite-in-place index)  
**Last updated:** 2026-01-26  
**Purpose:** Single map of v4 documentation (specs, contracts, gates, data plans, positioning, event logic).

This folder contains repo-ready markdown docs produced for **diBoaS-Analytics v4**.

---

## Golden rules (non-negotiable)
- **No contract = no ingest.**
- **No evidence pack = no publish.**
- **Gate 4 is mandatory for all public-facing content.** (See `08_gate4_compliance_ruleset_v1.md`)
- **Telemetry is the final arbiter of publication eligibility.** (See `07_v4_telemetry_dashboard_spec.md`)

---

## Files (in recommended reading order)

### Core v4 spec pack
1. `01_v4_progress_summary.md` — Narrative overview: what v4 is and why it exists  
2. `02_v4_phase0_core_contracts.md` — Phase 0 Truth Spine contract list (granular)  
3. `03_v4_truth_contract_spec.md` — Truth Contract YAML spec (enforceable)  
4. `04_v4_truth_contract_examples.md` — Example Truth Contracts (rates, spreads, crypto perps, RWA)  
5. `05_v4_evidence_pack_spec.md` — Evidence Pack schema (“the receipt”)  
6. `06_v4_adelaide_weekly_output_contract.md` — Golden Path output spec for Adelaide weekly  
7. `07_v4_telemetry_dashboard_spec.md` — Trust dashboard: eligibility + gates + diffs + invalidation  
8. `08_gate4_compliance_ruleset_v1.md` — Publication firewall ruleset (deterministic + classifier)  
9. `09_sample_adelaide_weekly_mock_2026w05_v3.md` — Mock weekly edition demonstrating end-to-end  
10. `10_repo_placement_guide.md` — Where docs/config/contracts should live

### Trust and feedback loop
11. `11_trust_score_v1.md` — Versioned Trust Score KPI spec (informational; never overrides hard blockers)  
12. `12_v4_feedback_incorporation_plan.md` — How to incorporate feedback without breaking the system

### Data collection & global expansion
13. `13_v4_data_collection_plan_zero_budget.md` — $0 data plan: what/why/sources/endpoints/frequencies/failure modes  
16. `16_v4_phase0_5_global_macro_extension_pack.md` — Phase 0.5 global macro add-ons (Japan/commodities/Brazil), fail-closed integration

### Strategic positioning & event logic
17. `17_v4_strategic_positioning_and_user_tiers.md` — What diBoaS can deliver by audience tier, safely, without advice  
18. `18_v4_event_class_definitions_v1.md` — Deterministic event classes + triggers + invalidation + alert routing

---

## Notes for implementers (because reality exists)
- **“Phase 0” and “Phase 0.5” are separate on purpose.** Phase 0.5 must not block Phase 0 publication eligibility unless Phase 0.5 data is explicitly referenced in an edition.
- **Event detection is regime/stress classification, not prophecy.** You’re building situational awareness with receipts, not a fortune teller.
- **If someone tries to “score away” a red system, stop them.** That’s what hard blockers are for.

---