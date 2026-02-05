# FILE: 06_v4_adelaide_weekly_output_contract.md

# diBoaS v4 — Adelaide Weekly Output Contract

**Document ID:** V4-ADELAIDE-OUTPUT-001  
**Status:** Enforceable  
**Canonical channel:** Web (website)  
**Distribution channels:** Web + Email + Substack + Telegram  
**Audience:** B2C + B2B (Layer A + Layer B)

This contract defines:
- The weekly edition structure
- Signal schema and limits
- Layer A (B2C) vs Layer B (B2B) mapping
- Channel formatting rules
- Hard publication blockers
- Corrections/retractions protocol
- Versioning and governance

---

## 1) Edition schedule and cadence
- **Weekly edition cadence:** Weekly (Sunday 06:00 UTC as default trigger)
- **Cutoff:** All referenced contracts must satisfy `publication_sla` at last eligibility check.
- **Edition ID format:** `adelaide_weekly_YYYYwWW`
- **Edition versioning:** semantic-like `major.minor.patch` where:
  - **major:** format/schema change
  - **minor:** materially changed signal set or narrative
  - **patch:** corrections, typo fixes, non-substantive edits

---

## 2) Hard publication blockers (must all pass)

An edition may be published only if **all** are true:

1) **Gate 4 status == PASS**  
2) **Signal count is 3–7**  
3) Every signal has a valid **Evidence Pack** (`evidence_pack_id` exists, schema-valid)  
4) Every signal’s Evidence Pack has `invalidation_state.current_status == "valid"`  
5) Every referenced contract satisfies `publication_sla` at last check  
6) No referenced contract has `validation_status == FAIL`  
7) No unresolved **high or critical reconciliation diffs** on referenced contracts (last 7d)  
8) No prohibited language or recommendation-likeness classifier FAIL (Gate 4)  
9) Mandatory disclaimers present per channel + jurisdiction

If any fail → **BLOCK PUBLICATION**.

---

## 3) Layer A vs Layer B definitions

### 3.1 Layer A (B2C)
Goal: Calm, plain-language, educational commentary.
- **Length:** 500–900 words total (excluding tables/disclaimers)
- **Style:** “Explain like a smart grandmother.” No jargon, no tickers, no trading talk.
- **Must include:**
  - What Changed (short narrative)
  - Market Snapshot (plain-language table)
  - 3–7 Signals (<= 120 words each)
  - What to Watch Next (short bullets)
  - Top-level Disclosures (if any)
  - General Caveats
  - Short disclaimer (always)

### 3.2 Layer B (B2B appendix)
Goal: Full audit and receipts.
- Must include:
  - Signal Index table (severity/horizon/confidence/evidence pack ID/invalidation status)
  - Contract Freshness table (contract_id, asof_ts, SLA compliance, gate statuses, reconciliation status, notes)
  - Methodology Notes (confidence model, key rules, disclosure logic)
  - Overrides & Approvals Summary
  - Evidence Packs (full YAML objects or canonical links)
  - Long disclaimer (web canonical)

---

## 4) Signal schema (canonical)
Each signal must be renderable from this schema:

```yaml
signal:
  id: "sig_xxx_v1"
  headline: "Short headline in plain language"
  why_it_matters: "Plain-language explanation"
  horizon: "1-8 weeks | 1-3 months | 3-12 months"
  severity: "low | medium | high"
  confidence:
    score: 0.72
    label: "low | medium | high"
  drivers:
    - "short driver phrase"
  watch_items:
    - "thing to watch"
  invalidation_summary: "Plain-language: what would make this wrong"
  evidence_pack_id: "ep_YYYYwWW_sig_XX"
  disclosures:
    - "optional disclosure shown immediately after the signal"