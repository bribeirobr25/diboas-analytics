# FILE: 08_gate4_compliance_ruleset_v1.md

# Gate 4 Compliance Ruleset v1 (Publication Firewall)

**Document ID:** GATE4-RULESET-001  
**Ruleset ID:** gate4_compliance_ruleset_v1  
**Status:** Enforceable  
**Scope:** Applies to every rendered output (Layer A, Layer B, Web, Email, Substack, Telegram), including titles, subtitles, footnotes, and disclaimers.

Gate 4 is the final publication blocker. If Gate 4 fails, the edition cannot be published.

---

## 1) Purpose
Ensure diBoaS content remains:
- educational market commentary
- non-personalized
- non-recommendation
- non-deceptive and non-overconfident
- transparent about limitations (lags, proxies, derivations, forward-fill, flags)

---

## 2) Hard PASS/FAIL criteria

Gate 4 returns **PASS** only if ALL are true:

1) No prohibited phrases (Rule Group A)
2) Recommendation-likeness classifier score < FAIL threshold (Rule Group B)
3) Backtest/performance framing complies with channel rules (Rule Group C)
4) Disclosures present and correctly placed when triggered (Rule Group D)
5) Personalization prohibited patterns absent (Rule Group E)
6) False precision / certainty claims absent (Rule Group F)
7) Overrides follow policy; break-glass rules respected (Rule Group G)
8) Mandatory disclaimers present per channel + jurisdiction
9) Translations/localizations comply with the same intent (language packs)

If any violation exists → **FAIL**.

---

## 3) Rule Group A — Prohibited phrases (deterministic blocklist)

### A1: Direct transaction directives (always FAIL)
Examples (non-exhaustive):
- buy, sell, long, short
- “ape in”, “load up”, “take profit”, “exit now”
- “rotate into”, “allocate X% to”
- “you should add”, “you should reduce”
- “this is a great entry”

### A2: Suitability/personalization (always FAIL)
- “for your portfolio”
- “you should…”
- “if you have $X… do Y”
- “best for you”, “right for you”
- “your retirement”, “your savings should…”

### A3: Guaranteed / near-guaranteed outcomes (always FAIL)
- guaranteed, risk-free, sure thing
- “can’t lose”, “no downside”
- “almost certain”, “highly likely to outperform”
- “this will outperform”, “this will moon”

### A4: Regulatory red flags (always FAIL)
- “insider”, “guaranteed edge”
- “we found a loophole”
- “front-run”

#### Allowed alternatives (safe phrasing examples)
- “historically associated with…”
- “may increase downside risk…”
- “can change quickly…”
- “one possible interpretation…”
- “illustrative scenario… not a guarantee”

---

## 4) Rule Group B — Recommendation-likeness classifier

Because blocklists are easy to dodge with synonyms, Gate 4 also runs a classifier.

### B1: Score output
Classifier returns score in [0, 1] for each sentence and an edition-level max score.

### B2: Default thresholds (versioned)
- PASS if max score < 0.30
- PASS_WITH_FLAGS if 0.30–0.45 (requires edits or explicit compliance override with reason)
- FAIL if > 0.45

**Thresholds must be versioned** (e.g., `classifier_v1_thresholds`) and require QR + Compliance approval to change.

### B3: Features that increase score (examples)
- imperative verbs (“do this”, “move into”, “switch to”)
- second-person targeting (“you”, “your”)
- certainty language (“will”, “surely”)
- action framing (“best move is…”)
- numeric allocation prescriptions (“put 20% into…”)

### B4: Findings must be explainable
When failing, Gate 4 must output:
- offending sentence(s)
- score
- top contributing features (human-readable)

---

## 5) Rule Group C — Backtest / performance framing

### C1: Layer A + Telegram (strict)
Forbidden:
- “would have made X%”
- “if you followed this, you’d have…”
- expected return claims (“we expect +12%”)
- “win rate”, “success rate”, “92% success rate”

Allowed:
- “In similar past setups, outcomes varied widely.”
- “This is a historical reference, not a prediction.”
- “Illustrative scenario based on assumptions.”

### C2: Layer B (more permissive, still constrained)
Allowed:
- scenario ranges with assumptions and limitations
Required:
- “hypothetical”
- methodology reference
- limitations / caveats
Forbidden:
- certainty claims
- individualized return expectations

---

## 6) Rule Group D — Disclosures (triggered + placement enforced)

### D1: Disclosure triggers (must be machine-detectable)
Disclosures required when any signal or edition uses:
- lagging data (macro proxies, issuer lag)
- proxy metrics
- derivations with assumptions
- forward-fill applied
- PASS_WITH_FLAGS
- methodology-sensitive composites (e.g., DeFi yield benchmark)

### D2: Placement rules
- Web/Email/Substack: signal-level disclosures appear **immediately after the signal block**
- Telegram: at minimum, include a short disclaimer; disclosures must appear via link to canonical web edition

### D3: Disclosure content requirements
Disclosure must specify:
- what is lagging/proxy/derived/filled
- maximum lag window or condition
- why it matters (plain language)

Every disclosure must end with:
> “This does not change the educational nature of this commentary.”

---

## 7) Rule Group E — Personalization (hard ban)
Public outputs must not address the reader’s specific situation:
- No “you should…”
- No portfolio tailoring
- No amounts, allocations, or execution instructions

---

## 8) Rule Group F — False precision and overconfidence

### F1: Forbidden (FAIL)
- “95% accuracy”
- “92% historical success”
- “high probability” without caveats
- “almost certain”, “highly likely to outperform”
- precise forecasts without uncertainty framing

### F2: Allowed (with constraints)
- broad probability ranges (e.g., “low/medium/high confidence”) tied to Evidence Pack confidence
- “possible outcomes include…” without numeric certainty

---

## 9) Rule Group G — Overrides and break-glass

### G1: Normal override policy
Overrides are allowed only to:
- correct phrasing into compliant language
- add missing disclosures/disclaimers
- remove a signal failing confidence/invalidation rules

All overrides require:
- audit log
- reason
- edition_version bump (at least patch)

### G2: Break-glass override (rare)
Break-glass is allowed only when:
- telemetry is RED due to operational issues (delay, outage),
- AND all Rule Group A checks are clean,
- AND classifier does not FAIL,
- AND Compliance approves.

**Break-glass is forbidden if any Rule Group A prohibited phrase violation exists. No exceptions.**

Break-glass requires:
- dual sign-off (CTO + Compliance)
- forced public note in header
- postmortem within 72 hours

---

## 10) Mandatory disclaimers (short + long)

### 10.1 Short disclaimer (required on all channels)
> Educational market commentary. Not financial, legal, or tax advice. No recommendation to buy or sell any asset. Investing involves risk.

### 10.2 Long disclaimer (required on Web + Layer B)
diBoaS provides educational market intelligence and commentary for general informational purposes only. This is not personalized financial advice and is not a recommendation to buy, sell, or hold any asset. Investing involves risk, including loss of principal. Cryptoassets and DeFi carry additional risks (volatility, liquidity, smart contract risk, and counterparty risk). Any scenarios or historical references are hypothetical, based on assumptions, and not guarantees. Past performance is not indicative of future results.

---

## 11) Multi-jurisdiction + localization requirements

### 11.1 Language packs
Prohibited phrases and classifier checks must exist for each supported language.
Example: PT-BR must include equivalents for “buy/sell/guaranteed/you should” (e.g., “compre”, “venda”, “garantido”, “você deveria”).

### 11.2 Telegram pinned disclaimer (optional)
To reduce disclaimer spam, Telegram may use:
- pinned long-form disclaimer message or channel bio link
- each message must still include minimal short reminder:
  - “Educational commentary, not advice. See pinned disclaimer.”

Gate 4 must verify pinned disclaimer is active if this mode is enabled.

---

## 12) Gate 4 findings output format (machine-readable)

```yaml
gate4_result:
  status: "PASS | PASS_WITH_FLAGS | FAIL"
  ruleset_id: "gate4_compliance_ruleset_v1"
  classifier:
    max_score: 0.22
    threshold_profile: "classifier_v1_thresholds"
  findings:
    - rule_id: "A1"
      severity: "FAIL"
      location: "Layer A Signal 2"
      snippet: "You should buy ETH here"
      reason: "Direct transaction directive / personalization"
    - rule_id: "F1"
      severity: "FAIL"
      location: "Layer A Signal 4"
      snippet: "This setup has 92% historical success rate"
      reason: "False precision / overconfidence claim"