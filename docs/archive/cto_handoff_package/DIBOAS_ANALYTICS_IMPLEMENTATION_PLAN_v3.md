# diBoaS Analytics v3 — Complete Implementation Plan

**Version:** 3.0  
**Date:** January 25, 2026  
**Prepared by:** CTO Board (Session 015) + Innovation Board (Session 003)  
**For:** The Coder (Claude Code implementation)

---

## Document Hierarchy

This document is the **primary implementation guide**. It references:
- `CTO_HANDOFF_MANIFEST.md` — Definitive list of 56 documents to read
- All board handoff documents (see Section 12)
- Manual execution results in `cto_handoff_package/` (test fixtures)

**Reading order:**
1. This document (implementation approach)
2. `CTO_HANDOFF_MANIFEST.md` (document inventory)
3. Board handoffs by layer (Tier 1 in manifest)

---

## Executive Summary

### What We're Building

**diboas-analytics** is a 5-layer data pipeline that:
1. **Collects** market data from 20+ sources
2. **Validates** data quality through 4 gates
3. **Analyzes** with Battle Test, Monte Carlo, Risk Metrics
4. **Generates intelligence** via triggers, alerts, regime classification
5. **Presents** via Adelaide newsletter (3 personas × 4 languages × 6 channels)

### Key Strategic Decisions (CTO Board + Innovation Board)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Approach** | HYBRID — wrap existing code | 3-5 weeks of validated logic preserved |
| **Budget** | $0/month Phase 1 | GitHub Actions + free tier APIs |
| **Architecture** | Registry pattern with 6 extension points | B2B multi-tenant ready |
| **B2B Model** | Mission-aligned restrictions | Estate data blocked for API clients |
| **Adelaide** | Multi-channel with content tiering | Website teaser → Social full → WhatsApp paid |
| **Decentralization** | Interface abstraction (Phase 4) | Pluggable when market demands |

### The Grandmother Test

Every decision passes the "grandmother test" from Innovation Board:

> "Would this help my grandmother build wealth, or help sophisticated players extract value from her?"

If the answer is the latter, we don't build it.

---

## Table of Contents

1. [Architecture Principles](#1-architecture-principles)
2. [CTO Board Decisions (Session 015)](#2-cto-board-decisions-session-015)
3. [Innovation Board Decisions (Session 003)](#3-innovation-board-decisions-session-003)
4. [Hybrid Implementation Approach](#4-hybrid-implementation-approach)
5. [Phase 1: Core Pipeline ($0/month)](#5-phase-1-core-pipeline)
6. [Phase 2: API Layer (First Client)](#6-phase-2-api-layer)
7. [Phase 3: B2B Platform (Scale)](#7-phase-3-b2b-platform)
8. [Phase 4: Enterprise & Decentralization](#8-phase-4-enterprise--decentralization)
9. [DataAccessPolicy — Ethical B2B Guardrails](#9-dataaccesspolicy--ethical-b2b-guardrails)
10. [Adelaide Multi-Channel Distribution](#10-adelaide-multi-channel-distribution)
11. [Directory Structure](#11-directory-structure)
12. [Reference: Board Handoff Documents](#12-reference-board-handoff-documents)
13. [Reference: Manual Execution Results](#13-reference-manual-execution-results)
14. [Appendix: Code Templates](#appendix-code-templates)

---

## 1. Architecture Principles

### 1.1 The 6 Extension Points (B2B Ready)

From CTO Board Session 015, the architecture supports 6 pluggable extension points:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIBOAS-ANALYTICS PLUGIN ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ 1. COLLECTORS   │ ← Data sources (FRED, Yahoo, DeFiLlama, custom)       │
│  │    Registry     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │ 2. VALIDATORS   │ ← Quality gates (schema, freshness, completeness)     │
│  │    Registry     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │ 3. ENGINES      │ ← Analytics (Battle Test, Monte Carlo, custom)        │
│  │    Registry     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │ 4. TRIGGERS     │ ← Intelligence (alerts, rebalancing, custom)          │
│  │    Registry     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │ 5. PERSONAS     │ ← Content adaptation (Ana, Maria, Felipe, custom)     │
│  │    Registry     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │ 6. OUTPUTS      │ ← Channels (Email, Substack, Twitter, WhatsApp)       │
│  │    Registry     │                                                        │
│  └─────────────────┘                                                        │
│                                                                             │
│  Each registry supports: register(), get(), list(), is_registered()        │
│  Each tenant can enable/disable implementations via YAML config             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Cost-Phased Infrastructure

| Phase | Trigger | Monthly Cost | Infrastructure |
|-------|---------|--------------|----------------|
| **Phase 1** | Now | $0 | GitHub Actions, free APIs, Vercel |
| **Phase 2** | First B2B client | $5-50 | + Resend, Railway |
| **Phase 3** | 5+ clients | $100-500 | + Supabase, Redis |
| **Phase 4** | Enterprise demand | $500+ | + Managed Postgres, CDN |

**Principle:** We don't spend money we don't have. Infrastructure scales with revenue.

### 1.3 Coding Standards (Pragmatic Application)

From `coding-standards.md`, apply these principles:

| Principle | Application | Priority |
|-----------|-------------|----------|
| **Service Agnostic** | All collectors use abstract interface | HIGH |
| **No Hardcoding** | Strategies, thresholds, formulas in YAML | HIGH |
| **DRY + Reusability** | Shared validators, formatters | HIGH |
| **Security** | API key management, output sanitization | HIGH |
| **Testability** | 80% coverage target | HIGH |
| DDD | Use domain concepts, skip full tactical patterns | MEDIUM |
| Event-Driven | Only for alerts → Slack, not core batch | LOW |
| Performance | Correctness first, then optimize | MEDIUM |
| SEO | Not applicable (no web frontend) | N/A |

---

## 2. CTO Board Decisions (Session 015)

### 2.1 Extensible Architecture

**Decision:** Build with 6 extension points from day one.

**Rationale:**
- B2B clients need custom collectors (proprietary data)
- B2B clients need custom personas (brand voice)
- B2B clients need custom triggers (business rules)
- Registry pattern adds minimal overhead (~5% more code)
- Enables multi-tenant without rewrite

### 2.2 Technology Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.11+ | Existing code, data science ecosystem |
| **Package Manager** | pip + requirements.txt | Simple, existing setup |
| **CI/CD** | GitHub Actions | Free, existing repo |
| **Static Hosting** | Vercel | Free tier, existing setup |
| **API (Phase 2)** | FastAPI | Async, auto-docs, type hints |
| **Database (Phase 3)** | Supabase | Free tier, Postgres, auth |
| **Email (Phase 2)** | Resend | 3K free/month, API-first |

### 2.3 AI/ML Integration Strategy

**Decision:** Template-based first, LLM optional.

| Approach | Phase | Cost | Use Case |
|----------|-------|------|----------|
| **Template-based** | Phase 1-2 | $0 | Regime → Template mapping |
| **LLM (Sonnet)** | Phase 3+ | ~$0.003/1K tokens | Custom voice adaptation |

**Why template-first:**
- Adelaide's voice is well-defined (3 personas documented)
- Templates are deterministic (same input → same output)
- LLM adds cost and latency without clear benefit initially
- Can always add LLM layer later as "voice enhancement"

### 2.4 Decentralization Readiness

**Decision:** Interface abstraction, not premature implementation.

```python
# Phase 1: Centralized implementations
class CentralizedDataSource(DataSource):
    def source_type(self) -> str:
        return "centralized"

class PythonComputationEngine(ComputationEngine):
    def computation_type(self) -> str:
        return "trusted"

# Phase 4 (future): Decentralized implementations (when market demands)
# class ChainlinkOracleSource(DataSource):
#     def source_type(self) -> str:
#         return "decentralized"
# 
# class ZKComputationEngine(ComputationEngine):
#     def computation_type(self) -> str:
#         return "verifiable"
```

**Why not now:**
- Zero paying customers demanding verifiable computation
- ZK infrastructure still immature for complex analytics
- Adds complexity without revenue
- Interfaces allow migration when ready

### 2.5 Hybrid Implementation Approach

**Decision:** KEEP existing code, WRAP in registries, ADD new components.

| Category | Files | Action |
|----------|-------|--------|
| **KEEP** | battle_test.py, monte_carlo.py, result_validator.py, domain/*.py | Preserve business logic |
| **WRAP** | All existing modules | Add registry decorators |
| **ADD** | Collectors, Adelaide generator, GitHub Actions | New functionality |
| **REFERENCE** | Manual execution CSVs and outputs | Test fixtures |

**Why not rewrite:**
- Battle Test: 5 scenarios × 10 strategies validated
- Monte Carlo: 10,000 simulations, regime-switching model validated
- CV-01 to CV-07: All validators tested and working
- Rewrite cost: 3-5 weeks of unnecessary work

---

## 3. Innovation Board Decisions (Session 003)

### 3.1 B2B Ethical Framework

**Core principle:** Retail gets the full product. B2B gets a subset.

| Data Type | Retail (Adelaide) | B2B API | Rationale |
|-----------|-------------------|---------|-----------|
| **Estate Wallets** | ✅ Full (delayed 24h) | ❌ Blocked | Prevent front-running |
| **Whale Tracking** | ✅ Full | ⚠️ Aggregated only | Prevent targeting |
| **Yield Comparisons** | ✅ Full | ✅ Full | Educational, helps everyone |
| **Risk Metrics** | ✅ Full | ✅ Full | Educational value |
| **Regime Classification** | ✅ Full | ✅ Full | Market sentiment |
| **Battle Test** | ✅ Full | ✅ Full | Strategy validation |
| **Monte Carlo** | ✅ Full | ✅ Full | Risk projections |

**Implementation:** `DataAccessPolicy` class (see Section 9)

### 3.2 Adelaide Distribution Model

**Decision:** Multi-channel with content tiering.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADELAIDE DISTRIBUTION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: FREE (Website)                                         │
│  ├── Basic Adelaide content                                     │
│  └── Premium teaser (partial, with CTA)                         │
│           │                                                     │
│           ▼                                                     │
│  TIER 2: FREE (Social Platforms)                                │
│  ├── Substack (full newsletter)                                 │
│  ├── X/Twitter (threads)                                        │
│  ├── LinkedIn (professional angle)                              │
│  ├── Instagram (visual summaries) ← Phase 2                     │
│  └── YouTube (video breakdowns) ← Phase 2                       │
│           │                                                     │
│           ▼                                                     │
│  TIER 3: PAID ($5/month)                                        │
│  └── WhatsApp community (direct access, Q&A, early alerts)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Phase 1 channels (3 maximum):**
1. Website (owned)
2. Substack (full newsletter)
3. WhatsApp (paid community)

**Why WhatsApp:** Grandmother wouldn't use Discord. 2+ billion people already on WhatsApp.

### 3.3 Adelaide Enterprise White-Label

**Decision:** Configuration-driven from start.

B2B clients can customize:
- Branding (colors, fonts, logo)
- Voice (vocabulary, formality, sign-off)
- Personas (create custom beyond Ana/Maria/Felipe)
- Languages (add beyond EN/PT-BR/DE/ES)
- Channels (their own Substack, email list)

**What stays diBoaS-owned:**
- Data collection infrastructure
- Analytics engines
- Validation gates
- Estate/whale tracking (exclusive moat)

### 3.4 Monetization Phases

From Innovation Board:

| Phase | Timeline | Product | Revenue Target |
|-------|----------|---------|----------------|
| **Phase 1** | Now → Feb 15 | Adelaide manual launch | $0 (proof of concept) |
| **Phase 2** | March → April | Adelaide Premium | $500-1,100/month |
| **Phase 3** | Q2 → Q3 | Adelaide Enterprise | $10,000-30,000/month |
| **Phase 4** | Q3 → Q4 | Analytics API | $20,000-50,000/month |

---

## 4. Hybrid Implementation Approach

### 4.1 What EXISTS and Must Be PRESERVED

Based on codebase audit:

| Component | Location | Status | Action |
|-----------|----------|--------|--------|
| Battle Test Engine | `src/engines/battle_test.py` | ✅ Working | WRAP in registry |
| Monte Carlo Engine | `src/engines/monte_carlo.py` | ✅ Working | WRAP in registry |
| Validators CV-01 to CV-07 | `src/validators/result_validator.py` | ✅ Working | WRAP in registry |
| Domain Models | `src/domain/*.py` | ✅ Working | KEEP as-is |
| File Loader | `src/collectors/file_loader.py` | ✅ Working | WRAP in registry |
| Reporters | `src/reporters/*.py` | ✅ Working | WRAP in registry |
| Configuration | `config/*.py` | ✅ Working | MIGRATE to YAML |
| Tests | `tests/*.py` | ✅ Working | EXTEND |

### 4.2 What DOESN'T EXIST and Must Be CREATED

| Component | Priority | Phase |
|-----------|----------|-------|
| Registry Framework | P0 | Phase 1 |
| Live API Collectors (FRED, Yahoo, DeFiLlama) | P0 | Phase 1 |
| Adelaide Content Generator | P0 | Phase 1 |
| Multi-Channel Output Formatters | P0 | Phase 1 |
| GitHub Actions Workflows | P0 | Phase 1 |
| Data Access Policies | P1 | Phase 1 |
| Tenant Configuration System | P1 | Phase 1 |
| FastAPI Layer | P2 | Phase 2 |
| LLM Integration | P3 | Phase 3 |
| White-Label Engine | P3 | Phase 3 |

### 4.3 The Wrapping Pattern

**DON'T rewrite. DO wrap.**

```python
# BEFORE: Direct import (existing code)
from src.engines.battle_test import BattleTestEngine

# AFTER: Registry wrapper (new code wrapping existing)
from src.registries import EngineRegistry
from src.engines.battle_test import BattleTestEngine  # Keep this!

@EngineRegistry.register("battle_test")
class BattleTestEnginePlugin(AnalyticsEngine):
    """Wrapper that makes existing code registry-compatible."""
    
    def __init__(self, config: dict):
        self.engine = BattleTestEngine()  # Reuse existing!
        self.config = config
    
    def run(self, data: dict) -> dict:
        # Call existing engine methods unchanged
        return self.engine.run_analysis(
            strategies=data["strategies"],
            historical_data=data["historical_data"],
            scenarios=self.config.get("scenarios", [...])
        )
```

---

## 5. Phase 1: Core Pipeline ($0/month)

**Timeline:** Weeks 1-4  
**Cost:** $0/month  
**Goal:** Working pipeline for diBoaS with B2B-ready architecture

### 5.1 Week 1: Registry Framework

Create 6 registries that wrap existing code:

| Registry | File | Wraps |
|----------|------|-------|
| CollectorRegistry | `src/registries/collector_registry.py` | file_loader.py |
| ValidatorRegistry | `src/registries/validator_registry.py` | result_validator.py |
| EngineRegistry | `src/registries/engine_registry.py` | battle_test.py, monte_carlo.py |
| TriggerRegistry | `src/registries/trigger_registry.py` | (new triggers) |
| PersonaRegistry | `src/registries/persona_registry.py` | (new personas) |
| OutputRegistry | `src/registries/output_registry.py` | reporters/*.py |

### 5.2 Week 2: Live API Collectors

Add collectors for live data while keeping CSV fallback:

| Collector | API | Rate Limit | Cost |
|-----------|-----|------------|------|
| FREDCollector | FRED API | 120/min | Free |
| YahooCollector | yfinance | Unlimited | Free |
| DeFiLlamaCollector | DeFiLlama | 300/5min | Free |
| CoinGeckoCollector | CoinGecko | 30/min | Free |
| AlternativeCollector | Alternative.me | Unlimited | Free |

### 5.3 Week 3: Adelaide Generator

Create newsletter generation using manual outputs as reference:

| Component | Reference File | Purpose |
|-----------|----------------|---------|
| AdelaideGenerator | adelaide_daily_draft.md | Orchestration |
| AnaPersona | adelaide_daily_ana_en.md | Conservative voice |
| MariaPersona | adelaide_daily_maria_en.md | Balanced voice |
| FelipePersona | adelaide_daily_felipe_en.md | Technical voice |
| NewsletterFormatter | All persona files | MD output |
| TwitterFormatter | (new) | Thread format |
| WebsiteTeaserFormatter | (new) | Partial + CTA |

### 5.4 Week 4: GitHub Actions & Integration

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| daily-collection.yml | 2 AM UTC | Collect all data sources |
| weekly-analytics.yml | Sunday 3 AM | Run full analytics suite |
| adelaide-daily.yml | 6 AM UTC | Generate newsletters |
| tests.yml | On PR | Validate code changes |

---

## 6. Phase 2: API Layer (First Client)

**Timeline:** When first B2B client signs  
**Cost:** $5-50/month  
**Goal:** REST API for external access

### 6.1 Infrastructure Additions

| Service | Cost | Purpose |
|---------|------|---------|
| Railway | $5/month | FastAPI hosting |
| Resend | Free (3K/month) | Email delivery |

### 6.2 API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/strategies` | GET | API Key | List available strategies |
| `/v1/analytics/battle-test` | GET | API Key | Battle Test results |
| `/v1/analytics/monte-carlo` | GET | API Key | Monte Carlo projections |
| `/v1/analytics/risk-metrics` | GET | API Key | Risk metrics |
| `/v1/adelaide/latest` | GET | API Key | Latest newsletter |
| `/v1/alerts` | GET | API Key | Active alerts |

### 6.3 Rate Limiting by Tier

| Tier | Rate Limit | Monthly Cap |
|------|------------|-------------|
| Free | 10/min | 1,000 calls |
| Starter ($99) | 60/min | 10,000 calls |
| Professional ($299) | 300/min | 100,000 calls |
| Enterprise (custom) | Custom | Unlimited |

---

## 7. Phase 3: B2B Platform (Scale)

**Timeline:** 5+ clients  
**Cost:** $100-500/month  
**Goal:** Multi-tenant platform with customization

### 7.1 Infrastructure Additions

| Service | Cost | Purpose |
|---------|------|---------|
| Supabase | $25/month | Postgres + Auth |
| Upstash Redis | $10/month | Caching |
| Anthropic API | ~$50/month | LLM for custom voices |

### 7.2 White-Label Features

| Feature | Configuration |
|---------|---------------|
| Branding | `tenant.branding.colors`, `.fonts`, `.logo_url` |
| Voice | `tenant.voice.personality`, `.vocabulary`, `.templates` |
| Personas | `tenant.personas.enabled[]`, `.custom[]` |
| Languages | `tenant.locales.enabled[]` |
| Channels | `tenant.output_formats.enabled[]` |
| Data | `tenant.features.collectors[]`, `.engines[]` |

---

## 8. Phase 4: Enterprise & Decentralization

**Timeline:** When market demands  
**Cost:** $500+/month  
**Goal:** Premium features and verifiable computation

### 8.1 Decentralization Interfaces

```python
# Abstract interfaces ready for future implementations
class DataSource(ABC):
    @abstractmethod
    def fetch(self, query: Dict) -> VerifiableResult:
        pass
    
    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return 'centralized' or 'decentralized'."""
        pass

class ComputationEngine(ABC):
    @abstractmethod
    def compute(self, inputs: Dict) -> VerifiableResult:
        pass
    
    @property
    @abstractmethod
    def computation_type(self) -> str:
        """Return 'trusted' or 'verifiable'."""
        pass
```

### 8.2 When to Implement

| Signal | Response |
|--------|----------|
| Enterprise client requests verifiable computation | Evaluate ZK options |
| Regulatory requirement for audit trail | Implement on-chain logging |
| Competitor launches decentralized analytics | Accelerate roadmap |
| None of the above | Stay centralized, focus on features |

---

## 9. DataAccessPolicy — Ethical B2B Guardrails

From Innovation Board Session 003:

```python
# src/policies/data_access.py

from enum import Enum
from typing import Dict, Any

class AccessLevel(Enum):
    FULL = "full"
    AGGREGATED = "aggregated"
    DELAYED = "delayed"  # 24-hour delay
    NONE = "none"

class ClientType(Enum):
    RETAIL = "retail"          # Adelaide B2C
    ENTERPRISE = "enterprise"  # Adelaide white-label
    API = "api"                # B2B API clients

class DataAccessPolicy:
    """
    Mission-aligned data access restrictions.
    
    Philosophy: Retail gets the full product. B2B gets a subset.
    This protects retail users from front-running by institutional players.
    
    The Grandmother Test: Would this help my grandmother, or help
    sophisticated players extract value from her?
    """
    
    POLICIES: Dict[str, Dict[ClientType, AccessLevel]] = {
        # Estate wallets: BLOCKED for B2B API (front-running protection)
        "estate_wallets": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.NONE,
        },
        # Whale tracking: Only aggregated for B2B API
        "whale_tracking": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.AGGREGATED,
        },
        # Yield comparisons: Open to all
        "yield_comparisons": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
        # Risk metrics: Open to all (educational)
        "risk_metrics": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
        # Battle Test: Open to all
        "battle_test": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
        # Monte Carlo: Open to all
        "monte_carlo": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
    }
    
    @classmethod
    def can_access(cls, data_type: str, client_type: ClientType) -> AccessLevel:
        return cls.POLICIES.get(data_type, {}).get(client_type, AccessLevel.NONE)
    
    @classmethod
    def filter_response(cls, data: Dict, data_type: str, client_type: ClientType) -> Dict:
        access = cls.can_access(data_type, client_type)
        
        if access == AccessLevel.NONE:
            return {
                "error": "access_denied",
                "message": "This data is not available for API clients",
                "reason": "Mission alignment: Retail users get priority access",
                "upgrade_path": "Contact sales for enterprise discussion"
            }
        
        if access == AccessLevel.AGGREGATED:
            return cls._aggregate_data(data, data_type)
        
        return data  # FULL access
```

---

## 10. Adelaide Multi-Channel Distribution

### 10.1 Output Formatters

| Formatter | Output | Content Level | Phase |
|-----------|--------|---------------|-------|
| `newsletter_md.py` | Full Markdown | Full | Phase 1 |
| `newsletter_html.py` | Full HTML email | Full | Phase 1 |
| `website_teaser.py` | Partial + CTA | Teaser | Phase 1 |
| `twitter_thread.py` | 280-char chunks | Full | Phase 1 |
| `linkedin_post.py` | Professional | Full | Phase 1 |
| `substack.py` | Substack format | Full | Phase 1 |
| `instagram_carousel.py` | Visual summary | Summary | Phase 2 |
| `youtube_script.py` | Video script | Full | Phase 2 |
| `whatsapp_message.py` | Short alert | Alert | Phase 2 |

### 10.2 Content Tiering Logic

```python
def get_content_for_channel(channel: str, full_content: dict) -> dict:
    """Apply content tiering based on Innovation Board decisions."""
    
    if channel == "website":
        # Tier 1: Basic + teaser of premium
        return {
            "basic": full_content["basic"],
            "premium_teaser": truncate(full_content["premium"], max_words=50),
            "cta": "Read full analysis on Substack →"
        }
    
    elif channel in ["substack", "twitter", "linkedin"]:
        # Tier 2: Full content (free on social)
        return full_content
    
    elif channel == "whatsapp":
        # Tier 3: Full + early alerts + Q&A access
        return {
            **full_content,
            "early_alerts": True,
            "community_access": True
        }
```

---

## 11. Directory Structure

```
diboas-analytics/
├── main.py                          # CLI entry point
├── requirements.txt                 # Dependencies
├── pyproject.toml                   # Project metadata
├── .env.example                     # Environment template
├── CLAUDE.md                        # Claude Code guidance
│
├── .github/workflows/               # CI/CD
│   ├── daily-collection.yml
│   ├── weekly-analytics.yml
│   ├── adelaide-daily.yml
│   └── tests.yml
│
├── config/
│   ├── tenants/
│   │   └── diboas.yaml              # Default tenant
│   ├── tiers.yaml                   # Feature tiers
│   ├── strategies.yaml              # Migrated from JSON
│   ├── thresholds.yaml              # Alert thresholds
│   └── adelaide.yaml                # Newsletter config
│
├── src/
│   ├── registries/                  # Plugin framework
│   │   ├── base.py
│   │   ├── collector_registry.py
│   │   ├── validator_registry.py
│   │   ├── engine_registry.py
│   │   ├── trigger_registry.py
│   │   ├── persona_registry.py
│   │   └── output_registry.py
│   │
│   ├── collectors/                  # Data sources
│   │   ├── base.py
│   │   ├── file_loader.py           # KEEP (wrap)
│   │   ├── fred_collector.py        # NEW
│   │   ├── yahoo_collector.py       # NEW
│   │   └── defillama_collector.py   # NEW
│   │
│   ├── validators/                  # Quality gates
│   │   ├── result_validator.py      # KEEP (wrap)
│   │   ├── gate1_schema.py          # NEW
│   │   └── gate4_content.py         # NEW
│   │
│   ├── engines/                     # Analytics
│   │   ├── battle_test.py           # KEEP (wrap)
│   │   ├── monte_carlo.py           # KEEP (wrap)
│   │   └── monitoring.py            # KEEP (wrap)
│   │
│   ├── triggers/                    # Intelligence
│   │   ├── base.py
│   │   ├── protocol_triggers.py
│   │   ├── estate_triggers.py
│   │   └── whale_triggers.py
│   │
│   ├── adelaide/                    # Content generation
│   │   ├── generator.py
│   │   ├── regime.py
│   │   ├── personas/
│   │   │   ├── ana.py
│   │   │   ├── maria.py
│   │   │   └── felipe.py
│   │   └── formatters/
│   │       ├── newsletter_md.py
│   │       ├── website_teaser.py
│   │       ├── twitter_thread.py
│   │       └── linkedin_post.py
│   │
│   ├── policies/                    # Access control
│   │   └── data_access.py           # DataAccessPolicy
│   │
│   ├── domain/                      # Data models (KEEP)
│   │   ├── strategy.py
│   │   ├── protocol.py
│   │   └── simulation.py
│   │
│   └── api/                         # REST API (Phase 2)
│       ├── main.py
│       ├── auth.py
│       └── routes/
│
├── data/                            # Bundled historical data
│   └── (20 CSV files)
│
├── outputs/
│   ├── adelaide/
│   └── public/                      # Vercel-served
│
└── tests/
    ├── fixtures/
    │   └── manual_execution/        # Copy from handoff
    └── test_*.py
```

---

## 12. Reference: Board Handoff Documents

See `CTO_HANDOFF_MANIFEST.md` for the complete 56-document list with reading order.

### Quick Reference by Layer

| Layer | Primary Documents |
|-------|-------------------|
| **Layer 1** | 00-08 data specs, TICKER_MASTER_LIST.yaml |
| **Layer 2** | VALIDATION_GATES_CTO_HANDOFF_v2.md (Gate 1) |
| **Layer 3** | QR_BOARD_CTO_HANDOFF_v2.md (Battle Test, Monte Carlo) |
| **Layer 4** | STRATEGY_BOARD_CTO_HANDOFF.md (Triggers, Alerts) |
| **Layer 5** | CMO_BOARD_CTO_HANDOFF.md + CMO_01-08 + CLO_BOARD_CTO_HANDOFF.md |
| **Adelaide** | adelaide_01-03_REVISED.md (Philosophy, Templates, Roadmap) |

---

## 13. Reference: Manual Execution Results

Located in `cto_handoff_package/08_results_manual_execution/` (after unzip):

| Folder | Contents | Use As |
|--------|----------|--------|
| `layer01_csv/` | 20 CSV data files | Test input data |
| `layer02_validation/` | Validation reports | Expected gate outputs |
| `layer03_analytics/` | Battle Test, Monte Carlo, Risk results | Expected engine outputs |
| `layer04_intelligence/` | Triggers, Alerts, Regime | Expected trigger outputs |
| `layer05_presentation/` | Adelaide persona outputs | Expected newsletter format |

### Key Files for Testing

```python
# tests/test_adelaide.py

def test_ana_persona_matches_reference():
    """Ensure Ana persona output matches manual execution."""
    with open("tests/fixtures/manual_execution/layer05_presentation/adelaide_daily_ana_en.md") as f:
        expected = f.read()
    
    generator = AdelaideGenerator(config={})
    actual = generator.generate(test_data, persona="ana", locale="en")
    
    # Structure checks
    assert "Adelaide Daily" in actual
    assert "What's Happening" in actual
    assert "Adelaide 🌸" in actual  # Ana's signature
    
    # Emoji count (Ana: 3-15 emojis)
    emoji_count = count_emojis(actual)
    assert 3 <= emoji_count <= 15

def test_felipe_persona_no_emojis():
    """Felipe is data-forward with zero emojis."""
    generator = AdelaideGenerator(config={})
    actual = generator.generate(test_data, persona="felipe", locale="en")
    
    emoji_count = count_emojis(actual)
    assert emoji_count == 0
```

---

## Appendix: Code Templates

### A.1 Registry Base Class

```python
# src/registries/base.py

from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic, Any
import logging

T = TypeVar('T')

class Registry(Generic[T], ABC):
    """Base class for all registries."""
    
    _instances: Dict[str, 'Registry'] = {}
    
    def __init__(self):
        self._registry: Dict[str, Type[T]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @classmethod
    def register(cls, name: str):
        """Decorator to register implementations."""
        def decorator(impl_class: Type[T]) -> Type[T]:
            instance = cls._get_instance()
            instance._registry[name] = impl_class
            instance._logger.info(f"Registered {name}: {impl_class.__name__}")
            return impl_class
        return decorator
    
    @classmethod
    def _get_instance(cls) -> 'Registry[T]':
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = cls()
        return cls._instances[cls.__name__]
    
    def get(self, name: str, config: Dict[str, Any] = None) -> T:
        if name not in self._registry:
            raise KeyError(f"Unknown: {name}. Available: {list(self._registry.keys())}")
        return self._registry[name](config or {})
    
    def list_available(self) -> list:
        return list(self._registry.keys())
```

### A.2 Tenant Configuration

```yaml
# config/tenants/diboas.yaml

tenant_id: "diboas"
name: "diBoaS Platform"
tier: "enterprise"

features:
  collectors:
    enabled: [fred, yahoo, defillama, coingecko, alternative]
    refresh_interval: "24h"
  
  engines:
    enabled: [battle_test, monte_carlo, monitoring, anomaly]
    monte_carlo_simulations: 10000
  
  personas:
    enabled: [ana, maria, felipe]
  
  output_formats:
    enabled: [newsletter_md, website_teaser, twitter_thread, linkedin_post]
  
  locales:
    enabled: [en, pt-br]

data_access:
  # Mission-aligned: retail gets everything
  estate_wallets: full
  whale_tracking: full
  
limits:
  api_calls_per_month: unlimited
  strategies: unlimited
```

### A.3 Adelaide Generator Skeleton

```python
# src/adelaide/generator.py

from typing import Dict, Any, List
from src.registries.persona_registry import PersonaRegistry
from src.registries.output_registry import OutputRegistry

class AdelaideGenerator:
    """Orchestrates Adelaide newsletter generation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.persona_registry = PersonaRegistry._get_instance()
        self.output_registry = OutputRegistry._get_instance()
    
    def generate(
        self,
        analytics_data: Dict[str, Any],
        persona: str = "ana",
        locale: str = "en",
        output_formats: List[str] = None
    ) -> Dict[str, Any]:
        """Generate Adelaide content for specified persona and formats."""
        
        # 1. Classify market regime
        regime, confidence = self._classify_regime(analytics_data)
        
        # 2. Select template based on regime
        template = self._select_template(regime)
        
        # 3. Assemble base content
        base_content = self._assemble_content(analytics_data, regime, template)
        
        # 4. Adapt to persona
        persona_adapter = self.persona_registry.get(persona, self.config)
        adapted_content = persona_adapter.adapt(base_content, locale)
        
        # 5. Format for output channels
        output_formats = output_formats or ["newsletter_md"]
        outputs = {}
        
        for format_name in output_formats:
            formatter = self.output_registry.get_formatter(format_name, self.config)
            outputs[format_name] = formatter.format(adapted_content)
        
        return {
            "persona": persona,
            "locale": locale,
            "regime": regime.value,
            "outputs": outputs
        }
```

---

## Summary: Implementation Checklist

### Phase 1 (Weeks 1-4, $0/month)

- [ ] Registry framework (6 registries)
- [ ] Wrap existing Battle Test in registry
- [ ] Wrap existing Monte Carlo in registry
- [ ] Wrap existing validators in registry
- [ ] FRED collector (live API)
- [ ] Yahoo Finance collector (live API)
- [ ] DeFiLlama collector (live API)
- [ ] Adelaide generator
- [ ] Ana, Maria, Felipe personas
- [ ] Newsletter MD formatter
- [ ] Website teaser formatter (Innovation Board)
- [ ] Twitter thread formatter
- [ ] LinkedIn post formatter
- [ ] DataAccessPolicy class (Innovation Board)
- [ ] Tenant configuration (diboas.yaml)
- [ ] GitHub Actions workflows
- [ ] Tests with manual execution fixtures

### Phase 2 (First Client, $5-50/month)

- [ ] FastAPI application
- [ ] API key authentication
- [ ] Rate limiting middleware
- [ ] Tier enforcement with DataAccessPolicy
- [ ] Second tenant configuration

### Phase 3 (5+ Clients, $100-500/month)

- [ ] LLM integration (optional voice enhancement)
- [ ] White-label configuration engine
- [ ] Admin UI (basic)
- [ ] WhatsApp community integration

### Phase 4 (Enterprise, $500+/month)

- [ ] Decentralization interfaces
- [ ] Premium data source integrations
- [ ] Custom computation engines

---

**Document End**

*Prepared by CTO Board (Session 015) with Innovation Board (Session 003) requirements integrated.*  
*Reference: CEO Board Document Audit (January 25, 2026)*
