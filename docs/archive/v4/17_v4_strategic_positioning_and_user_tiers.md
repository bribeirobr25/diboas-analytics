# FILE: 17_v4_strategic_positioning_and_user_tiers.md

# diBoaS v4 — Strategic Positioning and User Tiers

**Document ID:** V4-STRAT-001  
**Status:** Enforceable strategic guardrails  
**Last updated:** 2026-01-26  
**Guiding principle:** Auditable intelligence over prescriptive advice.

diBoaS is a **filter** and a **receipt machine**, not a forecast oracle.

- It collects a small set of high-signal market data.
- It validates and reconciles it.
- It generates explainable signals with invalidation rules.
- It publishes only when the system is healthy (telemetry-governed).
- It speaks in calm, educational language (Gate 4 enforced).

---

## 0) So What (the product promise, in one paragraph)
diBoaS delivers “economic weather” and regime awareness with receipts:
- **What changed**
- **Why it matters (in plain language)**
- **What to watch next**
- **What would invalidate this**
- **How confident the system is, and why**

Same truth spine, different packaging for different audiences.

---

## 1) What diBoaS can deliver (by user type)

### 1.1 Normal users (almost zero finance knowledge)
**Delivery:** Tier A (“Weather Report”)  
- 1 short weekly edition (Layer A)
- Simple snapshot table + 3–7 signals
- Minimal jargon (glossary tooltips on web)
- Rare “safety alerts” only for high-severity stress classes (see §3)

**So What:** They gain situational awareness without being manipulated by hype.

---

### 1.2 Interested learners (some finance/investing interest)
**Delivery:** Tier B (“Regime Meter”)  
- Weekly edition + optional “watchlist” section
- More explicit drivers (“rates eased”, “borrowing stress mixed”)
- Confidence labels + invalidation summaries
- Links to Layer B evidence appendix

**So What:** They learn how to think in scenarios and uncertainty.

---

### 1.3 Experts and traders
**Delivery:** Tier C (“Audit Pack”)  
- Layer B appendix: Evidence Packs, timestamps, gate statuses, reconciliation notes
- Deterministic event class outputs (Doc 18)
- Exportable structured objects (signals/evidence) for their own workflows

**So What:** They save time. You’re selling cleaned reality, not opinions.

---

### 1.4 Local businesses (pub, bakery, barber shop)
**Delivery:** Tier A + a small “real-life pulse” module  
- Inflation/energy/credit conditions described plainly
- If Phase 0.5 commodities included: “input cost pulse” context
- No instructions (“raise prices”, “take loans”) because that’s advice

**So What:** They get early awareness of cost/financing climate changes.

---

### 1.5 SMBs
**Delivery:** Tier B with “financing climate” framing  
- Borrowing conditions + stress regime summaries
- Scenario framing (what worsens vs what improves)
- Optional regional context (e.g., SELIC for Brazil)

**So What:** They can pressure-test plans without being told what to do.

---

### 1.6 Businesses with treasury allocation
**Delivery:** Tier C + regime classification + auditability  
- Liquidity/stress regime map (event classes)
- Evidence Packs as audit artifacts
- Strict disclosures on lag/proxy and system confidence

**So What:** They get board-friendly situational awareness with traceability.

---

## 2) What diBoaS is not
- Not a trading bot
- Not a personalized advisor
- Not a “guaranteed edge”
- Not a predictor of micro-catalysts (ETF headlines, lawsuits, tweets) on a $0 data stack

diBoaS detects **classes of conditions**, not specific catalysts.

---

## 3) Public alerting policy (don’t spam humans)
Tier A users get **rare** alerts only.

**Public safety alert eligibility (must all be true):**
- Event severity = **High/Critical** (per Doc 18)
- Event state = **Triggered**
- Evidence Pack exists and is valid
- Referenced contracts meet publication SLA
- Gate 4 PASS
- System confidence is not low (or includes explicit uncertainty caveat)

**Rate limit:**  
- **Max 1–2 public safety alerts per month**  
- Default channel for alerts: web canonical first, then Telegram/email pointing back to canonical

**So What:** Normal users don’t drown. The product stays trustworthy.

---

## 4) Safe language protocol (Gate 4 aligned)
Public phrasing must be descriptive, not directive.

**FAIL → PASS examples**
- “Good time to save” → “Cash purchasing-power pressure increased.”
- “Secure your credit line now” → “Financing conditions may tighten if this persists.”
- “Rotate out of crypto” → “This regime has historically coincided with reduced risk appetite.”

**Mandatory framing**
- “historically associated with…”
- “can change quickly…”
- “one possible interpretation…”
- “this does not change the educational nature of this commentary.”

---

## 5) Can diBoaS identify market events with current data?
Yes, within scope.

- **Strong:** liquidity tightening/easing, risk-off cascades, crypto leverage unwind, stablecoin stress, Japan carry stress (with Phase 0.5)
- **Partial:** capital rotation (needs sector witnesses)
- **No (by design):** micro-catalysts without news/flows stack

Doc 18 defines the deterministic event classes and what is required.

---

## 6) Technical analysis (TA): is it worth it?
**Yes, but only “boring TA,” and only as contract-based context.**

Allowed:
- moving averages / trend baselines
- z-scores / percentiles
- simple regime labels (above/below baseline)

Forbidden in public:
- execution timing language
- “breakout” hype
- anything that implies action

If TA is added:
- it must be a **derived Truth Contract** with explicit formula
- it must include invalidation conditions
- it must not override the regime logic or Gate 4

---

## 7) Slow macro (GDP, unemployment, etc.): should we add it?
Yes, but treat it as **regime context**, not alert fuel.

Recommended sequencing:
- Phase 0.5 / early: faster macro proxies (weekly jobless claims, weekly NFCI, monthly PMI)
- Phase 1: GDP (quarterly) and unemployment (monthly), with **vintage/revision awareness**
- Evidence Packs must store:
  - `asof_ts` (economic period)
  - `retrieved_at_ts` (what diBoaS saw at publish time)

**So What:** Adds foundational context without pretending it predicts next week.

---