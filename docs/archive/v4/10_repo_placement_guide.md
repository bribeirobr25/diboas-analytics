# FILE: 10_repo_placement_guide.md

# diBoaS v4 — Repo Placement Guide

**Status:** Enforceable  
**Goal:** Define where v4 docs, configs, contracts, samples, and outputs live so the repo stays navigable, auditable, and CI-enforceable.

This guide assumes a single repo that contains:
- the v4 “Spec Pack” (markdown)
- versioned configurations (YAML)
- Truth Contracts (YAML)
- sample editions + Evidence Packs (MD/YAML/JSON)
- governance artifacts (change logs, approvals, ADRs)
- tools/validators/generators used in CI and local runs

**Canonical map:** `00_INDEX.md` is the source of truth for what exists, what is current, and dependencies.


## 1) Top-Level Structure (Recommended)

### 1.1 Recommended repo layout (stable, enforceable)
/docs
/v4
00_INDEX.md
/spec
01_v4_progress_summary.md
03_v4_truth_contract_spec.md
04_v4_truth_contract_examples.md
05_v4_evidence_pack_spec.md
06_v4_adelaide_weekly_output_contract.md
07_v4_telemetry_dashboard_spec.md
08_gate4_compliance_ruleset_v1.md
09_sample_adelaide_weekly_mock_2026w05_v3.md
11_trust_score_v1.md
12_v4_feedback_incorporation_plan.md
17_v4_strategic_positioning_and_user_tiers.md
18_v4_event_class_definitions_v1.md
/contracts
02_v4_phase0_core_contracts.md
13_v4_data_collection_plan_zero_budget.md
16_v4_phase0_5_global_macro_extension_pack.md
10_repo_placement_guide.md

/config
/trust_score
trust_score_v1_weights.yaml
cc_map_v1.yaml
trust_score_formula_versions.yaml
/gate4
gate4_language_pack_en_v1.yaml
gate4_language_pack_ptbr_v1.yaml
classifier_thresholds_v1.yaml
/telemetry
alert_thresholds_v1.yaml
publication_eligibility_v1.yaml
/events
routing_policy_v1.yaml
public_alert_limits_v1.yaml
event_thresholds_v1.yaml

/contracts
/truth_contracts
/phase0
...yaml
/phase0_5
...yaml
/derived
...yaml
/deprecated
...yaml

/samples
/adelaide
/weekly
/2026w05
adelaide_weekly_2026w05_v3.md
telemetry_snapshot.json
gate4_findings.yaml
/evidence_packs
ep_2026w05_sig_01.yaml
ep_2026w05_sig_02.yaml
...

/schema
truth_contract.schema.json
evidence_pack.schema.json
adelaide_weekly.schema.json
event_snapshot.schema.json

/governance
CHANGELOG.md
APPROVALS.md
/decisions
ADR-0001-v4-truth-contracts.md
ADR-0002-no-contract-no-ingest.md
ADR-0003-layerA-layerB-split.md
ADR-0004-gate4-hard-blocker.md
ADR-0005-event-classes-and-routing.md

/tools
/collectors
/validators
/generators
/gate4
/telemetry
/events

### 1.2 Why split `/docs/v4/spec` vs `/docs/v4/contracts`
- **Specs** are normative rules (how the system must behave).
- **Contracts docs** are inventories/registries (what metrics exist, what’s in Phase 0/0.5, what gets collected).
This prevents “policy drift” and keeps reviewers focused.


## 2) What Goes Where (Rules)

### 2.1 `/docs/v4` (Human-readable constitution)
**Contains:** the v4 documentation package (specs + contract registries + examples + samples).  
**Must be:** version-controlled, reviewed, stable.  
**Must not contain:** secrets, environment-specific values, raw data dumps.

**Rule:** `00_INDEX.md` must be updated for any doc add/remove/rename.

### 2.2 `/contracts/truth_contracts` (Machine-enforced “No Contract = No Ingest”)
**Contains:** canonical YAML Truth Contracts.  
**Rule:** every ingested dataset must map to exactly one Truth Contract file.

Recommended contract folders:
- `/phase0/` = Phase 0 required spine
- `/phase0_5/` = Global macro extension pack contracts
- `/derived/` = derived metrics and “boring TA” contracts (explicit formulas)
- `/deprecated/` = deprecated contracts with replacement pointers

**Naming rule:** `snake_case_contract_id_vN.yaml` must match `contract_id` exactly.

**Required fields (minimum):**
- `contract_id`, `version`, `description`
- `source` (endpoint + parameters)
- `cadence` (expected frequency + schedule window)
- `freshness_sla`
- `timezone_policy`
- `null_zero_floor_policy`
- `revisions_vintage_policy` (if applicable)
- `validation` (schema + reconciliation rules)
- `deprecation_policy` (only if deprecated)

### 2.3 `/config` (Versioned knobs, not vibes)
**Contains:** configuration policies used by runtime + CI:
- Gate 4 language packs + thresholds
- trust_score weights + mappings
- telemetry thresholds + publication eligibility policies
- event routing policy + public alert caps

**Rule:** configs affecting publication eligibility or alerting must be versioned and reviewed like specs.

Recommended additions:
- `/config/events/routing_policy_v1.yaml` (internal vs public routing rules)
- `/config/events/public_alert_limits_v1.yaml` (hard caps + pacing rules)
- `/config/events/event_thresholds_v1.yaml` (centralized thresholds used by Gate 3 event evaluation)

### 2.4 `/samples` (Proof the system works)
**Contains:** self-contained “golden path” demonstrations:
- a weekly edition markdown
- evidence packs (YAML)
- telemetry snapshot (JSON)
- gate 4 findings (YAML), even if empty

**Rule:** samples must be reproducible with no external dependencies beyond the repo.

**No silent edits:** published samples are immutable. Corrections = new version folder/file.

### 2.5 `/schema` (CI validation contracts)
**Contains:** JSON schemas for:
- Truth Contract YAML
- Evidence Pack YAML
- Adelaide output structure
- Event snapshot payload (recommended)

**Rule:** schema changes require QR + CTO review and a version bump.

### 2.6 `/governance` (Who approved what, and why)
**Contains:**
- `CHANGELOG.md` for every spec/config version bump
- `APPROVALS.md` listing sign-offs
- ADRs capturing major decisions

**Rule:** any break-glass override or manual publication must be recorded here.

### 2.7 `/tools` (Implementation glue that makes “enforceable” true)
**Contains:** collectors, validators, generators, and evaluation code.

Recommended submodules:
- `/tools/collectors/` heartbeat collectors and source adapters
- `/tools/validators/` schema + reconciliation + freshness validators
- `/tools/events/` Gate 3 event evaluation (EC-01..EC-11 logic)
- `/tools/gate4/` compliance checks
- `/tools/telemetry/` snapshot creation + eligibility computation

**Rule:** thresholds belong in `/config`, not hard-coded.


## 3) CI / Enforcement Expectations (Minimum)

CI must fail the build if any of the following are violated:

1. Truth Contract YAML validates against `schema/truth_contract.schema.json`
2. Evidence Pack YAML validates against `schema/evidence_pack.schema.json`
3. Sample weekly edition validates against `schema/adelaide_weekly.schema.json`
4. Every sample edition references only valid `contract_id`s and `evidence_pack_id`s
5. Gate 4 ruleset version referenced exists in `/docs/v4/spec` and configs exist in `/config/gate4`
6. trust_score version referenced exists in `/docs/v4/spec/11_trust_score_v1.md` and configs exist in `/config/trust_score`
7. Event classes evaluation:
   - event engine reads the EC definitions (Doc 18) and thresholds/configs (if extracted)
   - event payload validates against `schema/event_snapshot.schema.json` (recommended)
   - “minimum resolution requirement” is enforced (event cannot Trigger if required daily/weekly contract cadence is missing)
8. Publication eligibility:
   - telemetry snapshot produced
   - `publication_eligibility_v1.yaml` applied
   - Gate 4 PASS is a hard blocker for public output

**Hard rules:**
- Contract YAML missing → ingestion fails
- Evidence Pack missing → signal removed
- Gate 4 fails → publication blocked
- Telemetry FAIL → public publication blocked (fail-closed)


## 4) Versioning Rules (Simple and enforceable)

### 4.1 Specs (docs)
- Any material change → update doc header (“Last reviewed”) and add a changelog line in `/governance/CHANGELOG.md`
- `00_INDEX.md` must reflect doc version and status

### 4.2 Truth Contracts
- `contract_id` includes `_vN`
- Breaking change → bump N
- Deprecation requires:
  - `deprecation_policy` field set
  - a replacement `contract_id`

### 4.3 Evidence Packs
- Evidence pack ids are edition-specific:
  - `ep_YYYYwWW_sig_XX`
- Evidence packs are immutable once published (corrections are new versions)

### 4.4 Event policies (routing/thresholds)
- Routing policy changes and public alert cap changes require:
  - config version bump (`*_vN.yaml`)
  - changelog entry
  - explicit QA sign-off (Gate 4 implications)


## 5) Where the Examples Fit (Quick Reference)

- Truth Contract examples → `/docs/v4/spec/04_v4_truth_contract_examples.md`
- Evidence Pack examples → `/samples/adelaide/weekly/YYYYwWW/evidence_packs/*.yaml`
- Canonical mock weekly edition → `/docs/v4/spec/09_sample_adelaide_weekly_mock_*.md`
  - optionally mirrored into `/samples/.../adelaide_weekly_*.md` for fully bundled demos
- Event class definitions (EC-01..EC-11) → `/docs/v4/spec/18_v4_event_class_definitions_v1.md`
- Strategic positioning + tiered delivery rules → `/docs/v4/spec/17_v4_strategic_positioning_and_user_tiers.md`
- Phase 0.5 extension contracts registry → `/docs/v4/contracts/16_v4_phase0_5_global_macro_extension_pack.md`


## 6) Practical Repo Hygiene Rules

1. **No bundles as Truth Contracts.** Bundles belong to rendering/output only.
2. **No silent edits to published samples.** New version files only.
3. **No magic numbers in code.** Thresholds must live in `/config`.
4. **Every eligibility blocker must have a config + spec reference.**
5. **Everything important must be reproducible from saved snapshots.**
6. **Public alerts are rate-limited by policy** (see `/config/events/public_alert_limits_v1.yaml`).
7. **Event triggers must be auditable** (save event snapshot + referenced Evidence Packs).


## 7) Minimal “Starter Commit” Checklist

To consider v4 “bootstrapped,” the repo must contain:

- `/docs/v4/00_INDEX.md` fully current
- `/docs/v4/spec/` containing the enforceable spec set (including 17 and 18)
- `/docs/v4/contracts/` containing Phase 0 and Phase 0.5 registries (including 16, and the data collection plan if used)
- Phase 0 Truth Contracts in `/contracts/truth_contracts/phase0/`
- Phase 0.5 Truth Contracts in `/contracts/truth_contracts/phase0_5/` (if extension pack enabled)
- Gate 4 configs in `/config/gate4/`
- trust_score configs in `/config/trust_score/`
- telemetry + publication eligibility configs in `/config/telemetry/`
- event routing policy + alert limits in `/config/events/` (or explicitly documented as “embedded in Doc 18” until extracted)
- at least one sample weekly edition with:
  - edition markdown
  - complete evidence packs
  - telemetry snapshot
  - gate 4 findings