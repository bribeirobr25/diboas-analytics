# CTO Handoff Manifest — Definitive Document List

**Version:** 1.0  
**Date:** January 25, 2026  
**Prepared by:** CEO Board (audited), CTO Board (validated)  
**Purpose:** Single source of truth for what The Coder should read to build diboas-analytics

---

## Executive Summary

This manifest lists exactly **49 core documents** required to build diboas-analytics v3. Documents are organized into 5 tiers by purpose. The Coder should read them in tier order.

**Important:** All documents listed are **v2/v3 FINAL** versions. Superseded documents (v1, older versions) are explicitly excluded. If you find a document with the same name but different version, **always use the version listed here**.

---

## Reading Order Recommendation

```
START HERE
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 5: IMPLEMENTATION GUIDES (Read First)                     │
│  Understand the phased approach and pipeline flow               │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 1: CORE SPECIFICATIONS (Build From These)                 │
│  The actual specs for each layer                                │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 2: DATA COLLECTION SPECS (Layer 1 Details)                │
│  What data to collect and from where                            │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 3: VALIDATION EVIDENCE (Test Fixtures)                    │
│  Expected outputs from manual pipeline execution                │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 4: CONTENT EXAMPLES (Adelaide Reference)                  │
│  What Adelaide output should look like                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## TIER 1: CORE SPECIFICATION DOCUMENTS (19 files)

**Purpose:** The actual specifications for building each layer

### 1.1 Board Handoff Documents (Layer Specifications)

| # | Document | Owner | Layer | Size | Read Order |
|---|----------|-------|-------|------|------------|
| 1 | `QR_BOARD_CTO_HANDOFF_v2.md` | QR Board | Layer 3 (Analytics) | ~66KB | 1st |
| 2 | `VALIDATION_GATES_CTO_HANDOFF_v2.md` | QR Board | Gates 1-4 | ~97KB | 2nd |
| 3 | `STRATEGY_BOARD_CTO_HANDOFF.md` | Strategy Board | Layer 4 (Intelligence) | ~45KB | 3rd |
| 4 | `CMO_BOARD_CTO_HANDOFF.md` | CMO Board | Layer 5 (Presentation) | ~25KB | 4th |
| 5 | `CLO_BOARD_CTO_HANDOFF.md` | CLO Board | Layer 5 (Compliance) | ~30KB | 5th |

### 1.2 CMO Sub-Specifications (Adelaide Engines)

| # | Document | Purpose | Size |
|---|----------|---------|------|
| 6 | `CMO_01_CONTENT_ASSEMBLY_ENGINE.md` | Adelaide content generation | ~39KB |
| 7 | `CMO_02_PERSONA_SEGMENTATION_ENGINE.md` | Ana/Maria/Felipe adaptation | ~34KB |
| 8 | `CMO_03_MULTI_CHANNEL_DISTRIBUTION.md` | Email/Substack/Social delivery | ~40KB |
| 9 | `CMO_04_LOCALIZATION_PIPELINE.md` | EN/PT-BR/DE/ES translation | ~31KB |
| 10 | `CMO_05_SOCIAL_ASSET_GENERATION.md` | Social media cards/posts | ~15KB |
| 11 | `CMO_06_RETENTION_AUTOMATION.md` | Re-engagement flows | ~15KB |
| 12 | `CMO_07_GATE4_CMO_VALIDATIONS.md` | Content validation rules | ~18KB |
| 13 | `CMO_08_ANALYTICS_AB_TESTING.md` | Performance tracking | ~15KB |

### 1.3 Adelaide Core Philosophy

| # | Document | Purpose | Size |
|---|----------|---------|------|
| 14 | `adelaide_01_philosophy_guidelines_REVISED.md` | Voice, tone, grandmother wisdom | ~25KB |
| 15 | `adelaide_02_template_library_REVISED.md` | Newsletter templates | ~30KB |
| 16 | `adelaide_03_implementation_roadmap_REVISED.md` | Phase 1/2/3 rollout | ~20KB |

### 1.4 Strategy & Data Configuration

| # | Document | Purpose | Size |
|---|----------|---------|------|
| 17 | `strategies_v2_1.json` | 10 strategy definitions | ~40KB |
| 18 | `06_CAPITAL_ROTATION_v2.md` | Rotation ratios and phase specs | ~15KB |
| 19 | `strategy_board_operations_manual.md` | Trigger/alert/rebalancing rules | ~20KB |

---

## TIER 2: DATA COLLECTION SPECIFICATIONS (9 files)

**Purpose:** What data to collect, from where, and how to validate

| # | Document | Data Domain | Source |
|---|----------|-------------|--------|
| 20 | `00_MASTER_INDEX.md` | Index of all data specs | Rakia |
| 21 | `01_ON_CHAIN_INTELLIGENCE_v3.md` | Wallet tracking, estate/whale | Rakia |
| 22 | `02_CRYPTO_MARKETS.md` | Crypto prices, DeFi APY | Rakia |
| 23 | `03_TRADFI_MARKETS_v3.md` | Equities, commodities, VIX | Rakia |
| 24 | `04_MACRO_ECONOMICS.md` | Treasury yields, M2, credit spreads | Rakia |
| 25 | `05_INSTITUTIONAL_FLOWS_v3.md` | ETF holdings, 13F filings | Rakia |
| 26 | `07_NEWS_AND_SENTIMENT_v3.md` | Fear & Greed, AAII | Rakia |
| 27 | `08_ADELAIDE_INTEGRATION.md` | Adelaide data requirements | Rakia |
| 28 | `TICKER_MASTER_LIST.yaml` | All tickers with sources | Rakia |

---

## TIER 3: VALIDATION EVIDENCE (12 files)

**Purpose:** Expected outputs from manual pipeline execution — use as test fixtures

### 3.1 CSV Data Files (Collected Data)

| # | File | Rows | Purpose |
|---|------|------|---------|
| 29 | `crypto_prices.csv` | ~2,200 | BTC/ETH/SOL daily OHLCV |
| 30 | `defillama_historical_apy.csv` | ~1,500 | Protocol APY history |
| 31 | `treasury_yields.csv` | ~1,300 | 2Y/10Y yields |
| 32 | `estate_wallet_tracker.csv` | ~20 | Bankruptcy estate holdings |
| 33 | `whale_wallet_master_list.csv` | ~50 | Major wallet addresses |
| 34 | `btc_etf_holdings.csv` | ~500 | ETF AUM tracking |
| 35 | `sentiment_indicators.csv` | ~1,300 | Fear & Greed history |

*(Full list of 20 CSVs — see VALIDATION_GATES_CTO_HANDOFF_v2.md Section 5 for complete schemas)*

### 3.2 Analytics Output Files (Layer 3-4 Results)

| # | File | Purpose |
|---|------|---------|
| 36 | `battle_test_results.json` | 5 scenarios × 10 strategies |
| 37 | `monte_carlo_results.json` | 10,000 simulations results |
| 38 | `risk_metrics.json` | Sharpe, Sortino, VaR, etc. |
| 39 | `anomalies_detected.json` | Current market anomalies |
| 40 | `triggered_actions.json` | Layer 4 trigger outputs |
| 41 | `consolidated_alerts.json` | Consolidated alert list |
| 42 | `regime_classification.json` | Market regime assessment |
| 43 | `adelaide_daily_data.json` | Structured data for templates |

### 3.3 Validation Reports

| # | File | Purpose |
|---|------|---------|
| 44 | `gate2_validation_report.json` | Analytics validation proof |
| 45 | `gate3_validation_report.json` | Intelligence validation proof |
| 46 | `gate4_cmo_validation.json` | Content validation proof |
| 47 | `gate4_clo_validation_report.json` | Legal validation proof |

---

## TIER 4: CONTENT EXAMPLES (5 files)

**Purpose:** Expected Adelaide output — what the newsletter should look like

| # | File | Persona | Locale | Purpose |
|---|------|---------|--------|---------|
| 48 | `adelaide_daily_draft.md` | Base | EN | Raw content before persona |
| 49 | `adelaide_daily_ana_en.md` | Ana (Conservative) | EN | Warm, emoji-rich |
| 50 | `adelaide_daily_maria_en.md` | Maria (Balanced) | EN | Educational |
| 51 | `adelaide_daily_felipe_en.md` | Felipe (Aggressive) | EN | Data-forward, no emojis |
| 52 | `adelaide_daily_ana_ptbr.md` | Ana (Conservative) | PT-BR | Localized example |

---

## TIER 5: IMPLEMENTATION GUIDES (4 files)

**Purpose:** How to build — read these FIRST

| # | Document | Purpose | Read Order |
|---|----------|---------|------------|
| 53 | `DIBOAS_ANALYTICS_IMPLEMENTATION_PLAN_v3.md` | Complete implementation guide with CTO + Innovation Board decisions | **READ FIRST** |
| 54 | `MANUAL_PIPELINE_EXECUTION_GUIDE_v3.md` | How the 5-layer pipeline flows | 2nd |
| 55 | `data_validation_handoff_package.md` | Data validation methodology | 3rd |
| 56 | `QR_BOARD_GAP_ANALYSIS_REPORT.md` | Gaps found during dry run (now fixed) | Reference |

---

## ❌ EXPLICITLY EXCLUDED (Do NOT Use)

These documents are **superseded** or were for **manual execution only**:

| Document | Reason |
|----------|--------|
| `QR_BOARD_CTO_HANDOFF.md` (v1) | Superseded by v2 |
| `VALIDATION_GATES_CTO_HANDOFF.md` (v1) | Superseded by v2 |
| `MANUAL_PIPELINE_EXECUTION_GUIDE.md` (v1) | Superseded by v3 |
| `MANUAL_PIPELINE_EXECUTION_GUIDE_v2.md` | Superseded by v3 |
| `01_ON_CHAIN_INTELLIGENCE.md` (v1) | Superseded by v3 |
| `03_TRADFI_MARKETS.md` (v1) | Superseded by v3 |
| `05_INSTITUTIONAL_FLOWS.md` (v1) | Superseded by v3 |
| `06_CAPITAL_ROTATION.md` (v1) | Superseded by v2 |
| `07_NEWS_AND_SENTIMENT.md` (v1) | Superseded by v3 |
| `strategies_v2_0.json` | Superseded by v2_1 |
| `diboas-analytics-v3-qr-board-specs.md` | Superseded by QR_BOARD_CTO_HANDOFF_v2.md |
| `diboas-analytics-v3-adelaide-system.md` | Superseded by adelaide_0*_REVISED.md |
| `ANALYST_LAYER3_EXECUTION_PLAN.md` | Manual execution artifact |
| `OPERATOR_LAYER4_EXECUTION_PLAN.md` | Manual execution artifact |
| `PRESENTER_LAYER5_EXECUTION_PLAN.md` | Manual execution artifact |
| `CLO_PRESENTER_LAYER5_EXECUTION_PLAN.md` | Manual execution artifact |
| `RAKIA_RESEARCHER_COMPREHENSIVE_PLAN.md` | Manual execution artifact |
| `LAYER1_DOCUMENTATION_GAP_ANALYSIS.md` | Gaps already fixed |
| `LAYER2_SPEC_GAP_ANALYSIS.md` | Gaps already fixed |
| `CTO_AUTOMATION_READINESS_ASSESSMENT.md` | Assessment, not spec |
| `Strategy_Board_Session_006_*.md` | Session notes, not specs |
| `CLO_Board_Adelaide_Legal_Review_Session.md` | Session notes |

---

## Document Location

All documents are located in:
- **Project root:** `/mnt/project/` (or `cto_handoff_package/` if using the downloaded zip)
- **CSV files:** `/mnt/project/*.csv`
- **JSON files:** `/mnt/project/*.json`

---

## Quick Reference: Documents by Layer

| Layer | Primary Documents |
|-------|-------------------|
| **Layer 1 (Collection)** | 00-08 specs + TICKER_MASTER_LIST.yaml |
| **Layer 2 (Validation)** | VALIDATION_GATES_CTO_HANDOFF_v2.md (Gate 1) |
| **Layer 3 (Analytics)** | QR_BOARD_CTO_HANDOFF_v2.md + VALIDATION_GATES_CTO_HANDOFF_v2.md (Gate 2) |
| **Layer 4 (Intelligence)** | STRATEGY_BOARD_CTO_HANDOFF.md + VALIDATION_GATES_CTO_HANDOFF_v2.md (Gate 3) |
| **Layer 5 (Presentation)** | CMO_BOARD_CTO_HANDOFF.md + CMO_01-08 + adelaide_01-03_REVISED + CLO_BOARD_CTO_HANDOFF.md + VALIDATION_GATES_CTO_HANDOFF_v2.md (Gate 4) |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Tier 1: Core Specifications** | 19 |
| **Tier 2: Data Collection** | 9 |
| **Tier 3: Validation Evidence** | 19 |
| **Tier 4: Content Examples** | 5 |
| **Tier 5: Implementation Guides** | 4 |
| **TOTAL CORE DOCUMENTS** | **56** |
| **Explicitly Excluded** | 21+ |

---

*Manifest prepared by CEO Board, validated by CTO Board — January 25, 2026*
