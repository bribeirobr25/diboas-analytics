# diBoaS Analytics — Project Context & Background

**Document Purpose:** Provide Claude Code with full business and technical context
**Created:** December 29, 2025
**Updated:** December 30, 2025 (Added Dream Mode Export — Innovation Board decision)
**Created By:** CTO Board (Claude Web Interface)
**Companion Document:** CLAUDE_CODE_HANDOFF.md (technical specification)

---

## HOW TO USE THIS DOCUMENT

This document provides **context and reasoning**. The companion document `CLAUDE_CODE_HANDOFF.md` provides **technical specifications**.

Read this document first to understand:
- What diBoaS is and why it exists
- The governance structure that validated the requirements
- Why architectural decisions were made
- What quality standards are expected
- How the system should evolve over time

Then use `CLAUDE_CODE_HANDOFF.md` for implementation details.

---

# PART 1: WHAT IS diBoaS?

## 1.1 The Vision

diBoaS (pronounced "dee-bo-ahs") is a **OneFi platform** designed to democratize wealth growth for 5.4 billion fintech users by combining banking, investing, crypto, and DeFi into a unified application.

**The Problem We Solve:**

Bar's grandmother in Rio de Janeiro saved diligently her entire life but couldn't build wealth. Why? Because banks earn 8-15% on customer deposits but pay savers only 0.1-2%. This gap — between what banks earn and what they share — is the systemic issue diBoaS aims to solve.

**Our Solution:**

Give everyday users direct access to the same yield-generating protocols that institutions use, but with:
- Simple, persona-based investment strategies (not complex DeFi interfaces)
- AI-powered education and guidance (Aqua, Mystic, Coral mascots)
- Non-custodial architecture (we never hold user funds)
- Low fees (0.9% on withdraw/transfer)

## 1.2 Target Users (Personas)

| Persona | Profile | Deposit Range | Risk Tolerance |
|---------|---------|---------------|----------------|
| **Ana** | Conservative saver, new to investing | €5 - €50 | Very Low |
| **Maria** | Moderate investor, some experience | €100 - €500 | Low-Medium |
| **Felipe** | Sophisticated, understands markets | €1,000+ | Medium-High |

## 1.3 Launch Parameters

| Parameter | Value |
|-----------|-------|
| **Launch Date** | January 2nd, 2026 |
| **Initial Markets** | EU (geo-blocking US and Brazil for product launch) |
| **Initial Chain** | Arbitrum (Solana for specific protocols) |
| **Phase 1 Focus** | DeFi yield strategies |
| **Phase 2** | RWA (Real World Assets) like Ondo USDY |

---

# PART 2: GOVERNANCE STRUCTURE

## 2.1 The Board System

diBoaS uses AI-powered advisory boards to guide strategic decisions. Each board has specialized expertise:

| Board | Chair | Focus |
|-------|-------|-------|
| **CEO Board** | Tobias Lütke | Overall strategy, launch readiness |
| **CTO Board** | — | Technical architecture, implementation |
| **CMO Board** | — | Marketing, messaging, brand |
| **CLO Board** | Ruth Bader Ginsburg | Legal, regulatory, compliance |
| **Strategy Board** | Ray Dalio | Investment strategies, allocations |
| **QR Board** | Jim Simons | Quantitative validation, statistics |
| **Innovation Board** | Steve Jobs | New features, user experience, pre-launch enhancements |
| **Rakia** | — | DeFi protocol research, data collection |

## 2.2 What Each Board Validated

### Strategy Board ✅
- Defined 10 investment strategies across 5 goals × 2 crypto comfort levels
- Set official v2.0 allocations for each strategy
- Approved Sanctum integration (replaced Jito+Lido in Stable Growth)
- Removed USDY from Phase 1 (deferred to Phase 2)

### QR Board ✅
- Validated Battle Test methodology (1,334 days, May 2022 - Dec 2025)
- Ran Monte Carlo simulations (5,000 paths per strategy)
- Calculated confidence intervals, VaR, CVaR, probability of loss
- Created validation rules CV-01 through CV-07
- Approved gas cost assumptions and minimum viable deposits

### Rakia ✅
- Researched 32 protocols (26 whitelisted, 6 blacklisted categories)
- Created Gas Cost Matrix with per-action costs
- Defined minimum viable deposits per strategy
- Built Protocol Monitoring Playbook with 35+ metrics
- Collected 65K+ historical data records

### CLO Board ✅
- Approved geo-blocking for US and Brazil (product launch, not pre-launch)
- Confirmed non-custodial architecture is legally sound
- Deferred USDY to Phase 2 due to regulatory constraints
- Set compliance budget at €20-27K
- **Approved Dream Mode with mandatory disclaimers** (see Part 13)

### Innovation Board ✅ (NEW)
- Decided to add **Dream Mode** to pre-launch
- Defined "Future You" Calculator for anonymous visitors
- Simplified 10 strategies → 3 paths for consumer display
- Set pre-launch enhancement timeline (4-5 days)

### CTO Board (This Session)
- Decided on separate repository (security, deployment isolation)
- Designed system architecture (layered, extensible)
- Chose SQLite for Phase 1 storage
- Planned GitHub Actions for scheduled execution
- Designed learning/improvement feedback loop
- **Added Dream Mode Export module** to support frontend feature

---

# PART 3: THE 10 INVESTMENT STRATEGIES

## 3.1 Strategy Framework

The strategies are organized by **Goal** (rows) and **Crypto Comfort** (columns):

| Goal | Crypto-Averse (0%) | Crypto-Comfortable (30-85%) |
|------|-------------------|----------------------------|
| **Emergency Fund** | Safe Harbor | Stable Growth |
| **Short-Term** | Goal Keeper | Steady Progress |
| **Medium-Term** | Patient Builder | Balanced Builder |
| **Long-Term** | Steady Compounder | Wealth Accelerator |
| **Wealth Building** | Yield Maximizer | Full Throttle |

## 3.2 Official v2.0 Allocations

**CRITICAL: These allocations are the single source of truth. They were validated by Strategy Board and QR Board.**

| ID | Strategy | Crypto % | Allocation | Risk Tier |
|----|----------|----------|------------|-----------|
| 1 | Safe Harbor | 0% | 50% Sky + 30% Aave + 20% Compound | Minimal |
| 2 | Stable Growth | 30% | 70% Sky + 30% Sanctum | Low |
| 3 | Goal Keeper | 0% | 60% Sky + 25% Aave + 15% Compound | Minimal |
| 4 | Steady Progress | 35% | 65% Sky + 35% Sanctum | Low-Medium |
| 5 | Patient Builder | 0% | 50% Sky + 30% Aave + 20% Compound | Minimal |
| 6 | Balanced Builder | 40% | 60% Sky + 25% Sanctum + 15% JLP | Medium |
| 7 | Steady Compounder | 0% | 55% Sky + 30% Aave + 15% Compound | Minimal |
| 8 | Wealth Accelerator | 70% | 30% Sky + 35% Sanctum + 35% JLP | High |
| 9 | Yield Maximizer | 0% | 45% Sky + 35% Aave + 20% Compound | Minimal |
| 10 | Full Throttle | 85% | 15% Sky + 30% Sanctum + 35% JLP + 20% Jito | Very High |

## 3.3 Key Rules

- ❌ **NO Huma** in any strategy (removed in v2.0)
- ❌ **Jito ONLY in Full Throttle** (Strategy 10)
- ⚠️ **Never hardcode allocations** — always load from config file
- ⚠️ **JLP basket is 45/27/27** (SOL/ETH/BTC), not 50/25/25

## 3.4 Simplified Paths for Dream Mode

The Innovation Board decided to simplify 10 strategies into **3 paths** for consumer-facing features:

| Path | Strategies Included | Label | Description | Risk Level |
|------|---------------------|-------|-------------|------------|
| **Safety** | 1, 3, 5, 7, 9 | "Safety First" | Stable yield, no crypto exposure | Minimal |
| **Balance** | 2, 4, 6 | "Balanced Growth" | Moderate crypto (30-40%) | Low-Medium |
| **Growth** | 8, 10 | "Maximum Growth" | High crypto (70-85%) | High-Very High |

This mapping is used by Dream Mode to show users simpler choices while the backend uses the full 10 strategies.

## 3.5 Variance Warnings

These strategies have extreme outcome ranges and require special handling:

| Strategy | Monte Carlo Range | Probability of Loss | Special Requirements |
|----------|-------------------|---------------------|---------------------|
| **Wealth Accelerator** | -60% to +200% | ~24% | Enhanced risk acknowledgment |
| **Full Throttle** | -78% to +12,000% | ~27% | 24h cooling period, max 20% portfolio, $200 minimum |

---

# PART 4: VALIDATED RESULTS

## 4.1 Battle Test v3.1 Results

**Test Period:** May 2022 - December 2025 (1,334 days)
**Major Events Captured:** Terra/Luna crash, FTX collapse, USDC depeg

### Scenario A: $10,000 + $200/month (Total Deposited: $18,600)

| Strategy | Crypto % | Return % | Max Drawdown % | Final Value |
|----------|----------|----------|----------------|-------------|
| Safe Harbor | 0% | +9.9% | 0.0% | $20,445 |
| Stable Growth | 30% | +20.5% | 8.1% | $22,409 |
| Goal Keeper | 0% | +8.7% | 0.0% | $20,218 |
| Steady Progress | 35% | +27.2% | 10.9% | $23,659 |
| Patient Builder | 0% | +9.9% | 0.0% | $20,445 |
| Balanced Builder | 40% | +40.6% | 13.0% | $26,160 |
| Steady Compounder | 0% | +9.3% | 0.0% | $20,324 |
| Wealth Accelerator | 70% | +151.4% | 46.5% | $46,755 |
| Yield Maximizer | 0% | +10.5% | 0.0% | $20,553 |
| Full Throttle | 85% | +216.6% | 66.1% | $58,890 |

### Key Findings

1. **All 5 stable-only strategies show exactly 0% max drawdown** ✅
2. **Linear correlation:** Max Drawdown ≈ 0.61 × Crypto %
3. **DCA through crash** produces exceptional recovery returns
4. **Full Throttle's 66.1% drawdown** is the worst-case scenario we tested

## 4.2 Monte Carlo Simulation Results

**Simulations:** 5,000 paths per strategy
**Horizon:** 48 months (4 years)
**Total Deposited:** $19,400

### Probability of Loss

| Strategy | P(Any Loss) | P(>10% Loss) | P(>50% Loss) |
|----------|-------------|--------------|--------------|
| Stable-only (5 strategies) | **0.0%** | 0.0% | 0.0% |
| Stable Growth | 21.8% | 9.2% | 0.0% |
| Steady Progress | 16.3% | 8.5% | 0.2% |
| Balanced Builder | 18.1% | 11.3% | 0.5% |
| Wealth Accelerator | 24.1% | 21.2% | 8.9% |
| Full Throttle | 26.8% | 24.5% | 13.9% |

### 90% Confidence Intervals

| Strategy | Crypto % | Median Return | 90% CI Width |
|----------|----------|---------------|--------------|
| Stable-only | 0% | +9-11% | ~3% (very tight) |
| Stable Growth | 30% | +17.5% | 88.5% |
| Full Throttle | 85% | +221.1% | 12,535% (extremely wide) |

---

# PART 5: WHY A SEPARATE REPOSITORY?

## 5.1 The Decision

The CTO Board decided to build this analytics application in a **separate private repository** rather than inside the main `diboas-platform` repo.

## 5.2 Rationale

| Factor | Separate Repo ✅ | Same Repo ❌ |
|--------|-----------------|--------------|
| **Security** | API keys isolated from public-facing code | Risk of key exposure |
| **Deployment** | Independent schedule (cron jobs) | Tied to web app CI/CD |
| **Access Control** | Share analytics without platform access | All-or-nothing access |
| **Scope** | Internal operations tool | User-facing product |
| **Tech Stack** | Python + data science libs | Next.js + React |

## 5.3 Sync Mechanism

The canonical `strategies_v2_0.json` configuration can be:
1. Duplicated in both repos (manual sync)
2. Published as private npm package `@diboas/strategy-config`
3. Fetched from a shared source (GitHub raw, S3)

For Phase 1, manual duplication is acceptable.

## 5.4 Dream Mode Data Flow

The analytics application produces `dream_mode_data.json` which the frontend consumes:

```
diboas-analytics                    diboas-platform (frontend)
       │                                     │
       ├─► dream_mode_data.json ────────────►│
       │   (generated daily)                 │
       │                                     ▼
       │                            Dream Mode UI
       │                            - Strategy selector
       │                            - Growth visualization
       │                            - Shareable Dream Cards
```

---

# PART 6: ARCHITECTURAL DECISIONS

## 6.1 Development Principles

The CTO Board evaluated whether to apply the full 12 development principles from the platform. Decision: **Pragmatic application**.

| Principle | Apply Fully? | Notes |
|-----------|--------------|-------|
| **API-Agnostic Abstraction** | ✅ Yes | Data sources WILL change |
| **No Hardcoding** | ✅ Yes | Strategies, thresholds, formulas in config |
| **DRY + Reusability** | ✅ Yes | Shared validation, calculations |
| **Security** | ✅ Yes | Secrets management, output access |
| **Testability** | ✅ Yes | Financial calculations must be verifiable |
| **DDD (Domain-Driven Design)** | ⚠️ Lighter | Use domain concepts but skip tactical patterns |
| **Event-Driven** | ⚠️ Optional | Only for monitoring alerts |
| **Performance** | ⚠️ Good enough | 5,000 simulations < 60s is fine |

## 6.2 Storage Decision

| Option | Verdict | Rationale |
|--------|---------|-----------|
| **SQLite** | ✅ Phase 1 | Zero setup, portable, SQL queries |
| PostgreSQL | Phase 2 | If scaling needed |
| Files only | ❌ | No querying, no indexing |

## 6.3 Execution Model

| Trigger | Mechanism | Frequency |
|---------|-----------|-----------|
| Data collection | Cron job | Daily 00:00 UTC |
| Protocol monitoring | Cron job | Every 15 minutes |
| Battle Test / Monte Carlo | CLI command | On-demand |
| Dream Mode Export | CLI command | After Battle Test / Monte Carlo |
| Alert-triggered re-simulation | Event | On P0/P1 alerts |

## 6.4 Deployment

| Option | Verdict | Rationale |
|--------|---------|-----------|
| **GitHub Actions** | ✅ Phase 1 | Free tier, simple, reliable |
| Railway/Render | Phase 2 | If persistent server needed |
| AWS Lambda | Phase 2 | If scaling needed |

---

# PART 7: EXTENSIBILITY REQUIREMENTS

## 7.1 Design for Change

The application must be easy to modify without code changes:

| Component | Change Mechanism |
|-----------|------------------|
| **Add/remove protocols** | Edit `protocols.py` registry |
| **Add/remove strategies** | Edit `strategies.json` |
| **Change thresholds** | Edit `thresholds.py` |
| **Add data sources** | Implement `DataProvider` interface |
| **Add notification channels** | Implement `Notifier` interface |
| **Add blockchains** | Edit `chains.py` registry |
| **Change Dream Mode paths** | Edit `dream_mode_config.py` |

## 7.2 Abstract Interfaces

Every external dependency should have an abstract interface:

```python
# Data sources
class DataProvider(ABC):
    def fetch_historical(self, start, end) -> pd.DataFrame
    def fetch_current(self) -> dict

# Notifications
class Notifier(ABC):
    def send(self, alert: Alert) -> bool

# Storage
class StorageAdapter(ABC):
    def save(self, data: pd.DataFrame, table: str)
    def load(self, table: str) -> pd.DataFrame
```

## 7.3 Adding a New Protocol (Example)

To add a new protocol in the future:

```python
# 1. Add to config/protocols.py
'new_protocol': {
    'name': 'New Protocol',
    'chain': 'base',
    'collector': 'defillama',
    'defillama_project': 'new-protocol',
    'enabled': False  # Disabled until validated
}

# 2. If custom data source needed, implement DataProvider
class NewProtocolProvider(DataProvider):
    def fetch_historical(self, start, end):
        # Custom API logic
        pass

# 3. Add to strategy allocations in strategies.json
# No code changes needed - just config
```

---

# PART 8: LEARNING & IMPROVEMENT LOOP

## 8.1 The Concept

The system should learn and improve over time, not just execute static calculations.

```
Data Collection → Battle Test → Monte Carlo → Monitoring → Anomaly Detection
       ↑                                                          ↓
       └──────────── Feedback & Calibration ←─────────────────────┘
```

## 8.2 Learning Mechanisms

| Mechanism | Description | Frequency |
|-----------|-------------|-----------|
| **Performance Tracking** | Compare actual vs. projected returns | Weekly |
| **Proxy Calibration** | Adjust proxy formulas based on real data | Quarterly |
| **Threshold Tuning** | Adjust alert thresholds based on false positive/negative rates | Monthly |
| **Model Retraining** | Update Isolation Forest, Z-score parameters | Monthly |
| **Correlation Updates** | Recalculate crypto correlation matrix | Quarterly |
| **Strategy Optimization** | Suggest allocation changes based on Sharpe ratio | Quarterly (human review) |

## 8.3 Weekly Performance Report (Example Output)

```json
{
  "period": "Week of 2025-12-23",
  "strategies": [
    {
      "id": 1,
      "name": "Safe Harbor",
      "projected_weekly_return": 0.15,
      "actual_weekly_return": 0.14,
      "delta": -0.01,
      "status": "WITHIN_EXPECTATIONS"
    }
  ],
  "anomalies_detected": 3,
  "alerts_triggered": 1,
  "recommendations": [
    "Consider reviewing Sanctum proxy formula — actual returns 5% higher than projected"
  ]
}
```

## 8.4 Re-Execution Triggers

The Protocol Monitoring Playbook defines when to automatically re-run simulations:

| Trigger Event | Action |
|---------------|--------|
| TVL drop >30% | Re-run Battle Test for affected strategies |
| APY deviation >100% | Re-run Monte Carlo |
| Protocol exploit/hack | Immediate re-run of all affected strategies |
| New protocol added | Full simulation suite before enabling |

---

# PART 9: QUALITY STANDARDS

## 9.1 Validation Rules

Every Battle Test and Monte Carlo run must pass these validation rules:

| Rule | Check | Severity |
|------|-------|----------|
| **CV-01** | Portfolio value never negative | 🔴 Critical |
| **CV-02** | Drawdown between 0% and 100% | 🔴 Critical |
| **CV-03** | Stable strategies have 0% max drawdown | 🟡 Warning |
| **CV-04** | Final value >= deposited for stable strategies | 🟡 Warning |
| **CV-05** | Return % matches calculation | 🔴 Critical |
| **CV-06** | Net return > 0 after gas costs | 🔴 Critical |
| **CV-07** | Initial deposit >= per-strategy minimum | 🟡 Warning |

## 9.2 Minimum Viable Deposits (CV-07)

| Strategy | Minimum (USD) | Minimum (EUR) | Rationale |
|----------|---------------|---------------|-----------|
| 1, 3, 5, 7, 9 | $50 | €45 | Arbitrum gas costs |
| 2, 4 | $20 | €18 | Mixed chain, higher yield |
| 6 | $30 | €27 | Mixed chain, medium yield |
| 8 | $100 | €90 | Higher complexity |
| 10 | $200 | €180 | Highest complexity |

## 9.3 Gas Cost Assumptions (CV-06)

| Chain | Cost per Transaction |
|-------|---------------------|
| Arbitrum | $0.30 |
| Solana | $0.005 |

## 9.4 Test Coverage Requirements

| Component | Minimum Coverage |
|-----------|------------------|
| Validation rules | 100% |
| Battle Test calculations | 95% |
| Monte Carlo engine | 90% |
| Data collectors | 80% |
| Dream Mode export | 90% |

---

# PART 10: DATA FILES AVAILABLE

## 10.1 Historical Data (Bundled)

| File | Records | Coverage | Source |
|------|---------|----------|--------|
| `defillama_historical_apy.csv` | 47,496 | May 2022 - Dec 2025 | DeFiLlama |
| `yahoo_historical_prices.csv` | 4,380 | May 2022 - Dec 2025 | Yahoo Finance |
| `jupiter_jlp_historical_apy.csv` | 697 | Jan 2024 - Dec 2025 | Jupiter |
| `perps_lp_combined_apy.csv` | 1,400+ | Various | GMX + Jupiter |

## 10.2 Reference Results (For Validation)

| File | Description |
|------|-------------|
| `battle_test_v3_1_results.csv` | Expected Battle Test outputs |
| `monte_carlo_production_results.csv` | Expected Monte Carlo outputs |

## 10.3 Configuration

| File | Description |
|------|-------------|
| `strategies_v2_0.json` | Canonical strategy definitions |

---

# PART 11: EXPECTED OUTPUTS

## 11.1 After Running Full Pipeline

```
outputs/
├── battle_test_results.csv       # All strategies × scenarios
├── battle_test_report.md         # Human-readable report
├── monte_carlo_results.csv       # Risk metrics per strategy
├── monte_carlo_report.md         # Risk analysis report
├── protocol_health.json          # Current protocol status
├── anomaly_scores.json           # Detected anomalies
├── validation_report.json        # CV rule compliance
├── dream_mode_data.json          # 🆕 Consumer-ready data for frontend
└── execution_metadata.json       # Run parameters, timestamps
```

## 11.2 Sample Validation Report

```json
{
  "timestamp": "2025-12-29T12:00:00Z",
  "run_id": "bt-20251229-001",
  "config_hash": "abc123def456",
  "validations": [
    {"rule": "CV-01", "passed": true, "severity": "critical"},
    {"rule": "CV-02", "passed": true, "severity": "critical"},
    {"rule": "CV-03", "passed": true, "severity": "warning"},
    {"rule": "CV-04", "passed": true, "severity": "warning"},
    {"rule": "CV-05", "passed": true, "severity": "critical"},
    {"rule": "CV-06", "passed": true, "severity": "critical"},
    {"rule": "CV-07", "passed": false, "severity": "warning", "note": "Scenario B below minimums"}
  ],
  "overall_status": "PASS_WITH_WARNINGS"
}
```

---

# PART 12: IMPLEMENTATION PRIORITIES

## 12.1 Recommended Order

| Priority | Module | Effort | Dependencies |
|----------|--------|--------|--------------|
| 1 | Config loading (strategies, protocols) | 1 hour | None |
| 2 | File loader (bundled CSVs) | 1 hour | Config |
| 3 | Battle Test engine | 3 hours | File loader |
| 4 | Validation rules (CV-01 to CV-07) | 2 hours | Battle Test |
| 5 | Monte Carlo engine | 3 hours | File loader |
| 6 | CLI interface | 1 hour | All engines |
| 7 | Protocol monitoring | 2 hours | File loader |
| 8 | Anomaly detection | 2 hours | File loader |
| 9 | Reporters (CSV, JSON, Markdown) | 1 hour | All engines |
| 10 | **Dream Mode Export** | 2 hours | Battle Test, Monte Carlo |
| 11 | Tests | 2 hours | All modules |

**Total estimate:** 20-22 hours

## 12.2 Definition of Done

Each module is complete when:

1. ✅ Core functionality implemented
2. ✅ Validation rules pass
3. ✅ Unit tests written and passing
4. ✅ Output format matches specification
5. ✅ No hardcoded values (all from config)
6. ✅ Error handling for edge cases
7. ✅ Logging for audit trail

---

# PART 13: DREAM MODE (NEW — Innovation Board Decision)

## 13.1 What is Dream Mode?

Dream Mode is a **pre-launch feature** that lets waitlist users simulate what their money could become using real historical data. It's designed to:

- Reduce first-deposit anxiety (users "practice" before real money)
- Create viral shareable content (Dream Cards)
- Build engagement during the waitlist period
- Position diBoaS as educational, not just transactional

## 13.2 How Dream Mode Works

```
User Flow:
1. User enters Dream Mode from waitlist portal
2. Chooses one of 3 simplified paths (Safety, Balance, Growth)
3. Enters starting amount (€50 - €10,000 slider)
4. Sees animated growth visualization with real APY data
5. Can "fast forward" to see 1 week, 1 month, 1 year, 5 years
6. Always sees bank comparison ("Your bank would give you €X")
7. Generates shareable Dream Card with #WhileISlept branding
```

## 13.3 What Analytics Application Provides

The analytics application generates `dream_mode_data.json` containing:

| Data Element | Source | Used For |
|--------------|--------|----------|
| Path definitions | Strategy mapping | "Choose your path" UI |
| Aggregated metrics per path | Battle Test + Monte Carlo | Risk/return display |
| Pre-calculated projections | Historical averages | Growth visualization |
| Bank comparison baseline | ECB data (0.5% APY) | "Your bank gives you €X" |
| Data source metadata | All sources | CLO-required disclaimers |
| CLO-approved disclaimers | Legal text | Compliance display |

## 13.4 CLO Board Requirements (MANDATORY)

The CLO Board approved Dream Mode with these **non-negotiable requirements**:

### Required Disclaimers

**Entry Disclaimer (shown before Dream Mode starts):**
> ⚠️ This is a simulation
> 
> Dream Mode shows what your money *could have* earned based on historical data from May 2022 to December 2025. This is NOT a prediction of future performance. Actual results may vary significantly. Past performance does not guarantee future returns. Capital is at risk. This is for educational purposes only and does not constitute investment advice.

**On Every Dream Card (shareable):**
> "⚠️ SIMULATION — Based on historical data. Not a guarantee. diboas.com"

**Bank Comparison Footnote:**
> "Bank comparison based on average EU savings account rate of 0.5% APY. Source: ECB Statistics, December 2024. Rates may vary."

### Enhanced Disclaimers (Brazil/US)

**PT-BR:**
> "⚠️ SIMULAÇÃO EDUCACIONAL — Este recurso utiliza dados históricos apenas para fins ilustrativos. Não constitui oferta de investimento, promessa de retorno ou aconselhamento financeiro. Resultados reais podem diferir significativamente."

**US (if accessed via VPN):**
> "⚠️ EDUCATIONAL SIMULATION — This feature uses historical data for illustrative purposes only. It does not constitute an offer of investment, promise of returns, or financial advice."

## 13.5 Why This Matters

Dream Mode bridges the gap between:
- **Analytics** (what we've validated works)
- **Marketing** (what users see and share)
- **Legal** (what we're allowed to claim)

The `dream_mode_data.json` file ensures the frontend displays **exactly what we've validated** — not more, not less.

---

# SUMMARY

## What You're Building

A Python CLI application that:
1. **Collects** historical DeFi yield and crypto price data
2. **Backtests** 10 investment strategies against real market data
3. **Simulates** 5,000+ future scenarios to quantify risk
4. **Monitors** protocol health and detects anomalies
5. **Validates** all results against strict quality rules
6. **Reports** findings in CSV, JSON, and Markdown formats
7. **Exports** consumer-ready data for Dream Mode frontend (NEW)

## Why It Matters

This application provides the **quantitative foundation** for diBoaS:
- Regulatory compliance (EU requires probability-based disclosures)
- User protection (accurate risk communication)
- Strategy validation (before offering to users)
- Ongoing monitoring (detect issues before they become crises)
- **Dream Mode** (turn validated data into user engagement)

## Quality Bar

This is a **production-grade internal tool**. It must be:
- Accurate (validated by QR Board methodology)
- Extensible (easy to add protocols, strategies, data sources)
- Auditable (complete logging and metadata)
- Testable (comprehensive test coverage)

---

**Now proceed to `CLAUDE_CODE_HANDOFF.md` for technical implementation details.**
