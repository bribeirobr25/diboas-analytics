# FILE: 18_v4_event_class_definitions_v1.md

# diBoaS v4 — Event Class Definitions v1

**Document ID:** V4-EVENTS-001  
**Status:** Enforceable (Gate 3 intelligence policy surface)  
**Last updated:** 2026-01-26  
**Purpose:** Deterministic regime/stress events derived from validated contracts, with clear triggers, persistence, invalidation, and alert routing.

This is how you stop “analysis vibes” from becoming production output.

---

## 0) Global rules

### 0.1 Event states
- **WATCH:** conditions forming; not confirmed
- **TRIGGERED:** conditions met with persistence; eligible for internal routing, and sometimes public alerting
- **RESOLVED:** conditions reverted; important to communicate, especially for stress regimes

### 0.2 Evidence requirement
Every TRIGGERED event that appears in any published output must have:
- a valid Evidence Pack
- referenced contract timestamps and validation statuses
- disclosures (proxy/lag/pass_with_flags) when applicable
- invalidation conditions

### 0.3 Persistence rule (anti-noise)
Default: an event may become **TRIGGERED** only if the trigger condition is met in **2 consecutive checks**.

### 0.4 Minimum resolution requirement (no fake triggers from monthly data)
Each event defines a **minimum required cadence** for at least one key witness contract.

If the minimum cadence is not met:
- the event may be **WATCH** only
- it cannot become TRIGGERED

### 0.5 Confidence input (Trust Score)
Event confidence must be informed by `trust_score_v1` for the referenced contracts:
- Low trust_score should cap event confidence and force stronger caveats in Layer A.

---

## 1) Canonical event schema (renderable)
```yaml
event:
  id: "EC-07"
  name: "Japan Carry Stress"
  state: "WATCH | TRIGGERED | RESOLVED"
  severity: "low | medium | high | critical"
  horizon: "hours-days | 1-8 weeks | 1-3 months"
  confidence:
    score: 0.72
    label: "low | medium | high"
  required_contracts:
    - "fx_usdjpy_spot_v1"
    - "rates_jp10y_yield_proxy_daily_v1"
  minimum_resolution_requirement:
    requires_at_least_one_daily_witness: true
  trigger:
    description: "Human readable condition"
    rule: "machine rule expression"
    persistence_checks: 2
  invalidation:
    - rule: "expression"
      action: "set_resolved | downgrade_to_watch | flag_event_invalid"
  disclosures:
    - "cadence_lag | proxy | pass_with_flags | methodology"
  routing:
    internal: ["CTO Board", "QR Board", "Strategy Board"]
    public_allowed: true
  layer_a_phrasing:
    triggered: "Safe phrasing"
    watch: "Safe phrasing"
    resolved: "Safe phrasing"
```

## 2) Event classes (v1)
### EC-01 Liquidity Tightening (Macro Gravity Up)
Severity: High
Horizon: 1–8 weeks
Required contracts (Phase 0): USD proxy, rates, credit proxy (as available)
Minimum resolution requirement: Daily or EOD for at least one rates + one USD/credit witness
Trigger (example):
rates rising materially over 2w AND USD up over 2w AND credit spreads widening beyond threshold
Invalidation / Resolve:
credit spreads compress back below threshold OR rates revert meaningfully
Layer A phrasing
WATCH: “Borrowing pressure and the dollar are trending firmer; this has sometimes coincided with less appetite for risk.”
TRIGGERED: “Borrowing pressure and stress indicators strengthened together; historically this can coincide with reduced risk appetite, but conditions can change quickly.”
RESOLVED: “This condition has resolved: the indicators that triggered it have reverted toward baseline.”

### EC-02 Risk-Off Cascade (Stress Cluster)
Severity: High
Horizon: hours-days to 1–8 weeks
Required: volatility proxy + credit stress proxy
Min resolution: daily/EOD witnesses
Trigger: volatility spike + credit widening (persisted)
Layer A
TRIGGERED: “Stress indicators rose together, which has historically coincided with more fragile market conditions.”
RESOLVED: “Stress indicators have eased back toward baseline.”
Public alerts: Allowed (rare) under Doc 17 policy.

### EC-03 Liquidity Easing (Macro Gravity Down)
Severity: Medium
Horizon: 1–8 weeks
Required: rates easing + stress not worsening
Min resolution: daily/EOD
Trigger: rates down over 2w AND credit/vol not worsening
Layer A
TRIGGERED: “Borrowing pressure eased and stress did not worsen. When this persists, it has historically coincided with less pressure on risk assets, but confirmation matters.”

### EC-04 Stablecoin Depeg Event (Crypto Plumbing Alarm)
Severity: Critical
Horizon: hours-days
Required: stablecoin_depeg_events_v1 (near real time)
Min resolution: near real-time checks (per contract SLA)
Trigger: confirmed depeg event per contract rules
Layer A
TRIGGERED: “A stablecoin stress event was detected. These can spread quickly through crypto liquidity, so monitoring is elevated.”
RESOLVED: “Stablecoin prices and stress indicators have stabilized toward normal ranges.”
Public alerts: Allowed (rare) under Doc 17 policy.

### EC-05 Crypto Leverage Unwind
Severity: High
Horizon: hours-days to 1–8 weeks
Required: perps funding + open interest (BTC/ETH)
Min resolution: hourly or better
Trigger (example):
funding flips negative AND open interest drops beyond threshold (persisted)
Invalidation / Resolve:
funding normalizes AND OI stabilizes for N checks
Layer A
WATCH: “Leverage conditions look less supportive; this can change quickly.”
TRIGGERED: “Leverage conditions deteriorated together (funding and positioning). Historically this can coincide with fragile crypto conditions.”
RESOLVED: “Leverage stress has eased: funding and positioning indicators have stabilized toward baseline.”

### EC-06 Capital Rotation (Partial vs Complete)
Severity: Medium
Horizon: 1–3 months
Required: sector witnesses for “complete”
Min resolution: daily/EOD
Definitions
Partial rotation: macro regime suggests rotation risk, but witnesses missing
Complete rotation: requires at least one equity witness + one commodity/energy witness
Complete rotation requires (minimum):
Equity/growth proxy (e.g., NASDAQ) AND energy/commodity proxy (e.g., WTI) AND rates/real yields context
Layer A
PARTIAL: “Some indicators resemble regimes that have coincided with reallocations across assets, but confirmation requires additional sector evidence.”
COMPLETE (only if witnesses present): “Sector proxies diverged in a way historically associated with rotations, but outcomes vary and confirmation matters.”
RESOLVED: “The rotation pattern has weakened as the key witnesses reverted toward baseline.”

### EC-07 Japan Carry Stress (Unwind Risk)
Severity: High
Horizon: hours-days to 1–8 weeks
Required (Phase 0.5):
fx_usdjpy_spot_v1 (daily)
rates_jp10y_yield_proxy_daily_v1 (daily proxy)
Minimum resolution requirement: At least one daily Japan yield witness is mandatory to TRIGGER.
If only monthly JGB series exists → state can be WATCH only.
Trigger (example):
sharp USD/JPY move AND Japan yield proxy rises meaningfully (persisted)
Resolve:
USD/JPY stabilizes AND yield proxy reverts/stops rising (persisted)
Layer A
WATCH: “Yen-related indicators are moving more than usual. In past regimes, abrupt shifts here have sometimes coincided with global risk stress.”
TRIGGERED: “Yen and Japan yield indicators moved sharply together. Historically, this has sometimes coincided with broader liquidity stress, but conditions can change quickly.”
RESOLVED: “Japan-related stress indicators have stabilized toward baseline.”

### EC-08 Credit Stress Widening (Adult Supervision)
Severity: High
Horizon: 1–8 weeks to 1–3 months
Required: credit spread proxy
Min resolution: daily/EOD
Trigger: spreads widen beyond threshold (persisted)
Layer A
TRIGGERED: “Borrowing stress increased. This has historically coincided with more cautious market conditions.”

### EC-09 DeFi Baseline Deterioration (Breadth Risk)
Severity: Medium
Horizon: 1–3 months
Required: DeFi TVL + yield benchmark (composite disclosures)
Min resolution: daily/EOD
Trigger: TVL down materially AND benchmark yield rises due to risk compensation (persisted)
Layer A
TRIGGERED: “DeFi baseline indicators weakened. Composite metrics can be sensitive to methodology, so interpretation stays cautious.”

### EC-10 RWA Flow Shock (Tokenized Treasuries)
Severity: Medium
Horizon: 1–8 weeks
Required: RWA TVL/NAV + derived flows
Min resolution: EOD (with lag disclosure)
Trigger: large negative net flows beyond threshold (persisted)
Layer A
TRIGGERED: “Tokenized treasury flows shifted sharply. Issuer reporting can lag, so timestamps and disclosures matter.”

### EC-11 Commodity Inflation Pulse (Phase 0.5)
Severity: Medium
Horizon: 1–3 months
Required (Phase 0.5): WTI + Copper
Min resolution: daily/EOD
Trigger (example):
WTI up over 2w beyond threshold AND copper up over 2w beyond threshold (persisted)
Layer A
TRIGGERED: “Energy and industrial metals rose together, historically associated with inflation pressure pulses, though outcomes vary.”


## 3) Routing policy (internal vs public)
Internal routing: always allowed (tasks/triage)
Public alerts: only for high/critical safety classes and only under Doc 17 limits
Typical: EC-04 stablecoin depeg, EC-02 stress cascade
Everything else: appears in weekly edition as calm “watch items,” not breaking-news spam.