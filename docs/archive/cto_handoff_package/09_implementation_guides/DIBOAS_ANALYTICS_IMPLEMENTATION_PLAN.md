# diBoaS Analytics v3 â€” Implementation Plan for The Coder

**Version:** 2.0  
**Date:** January 25, 2026  
**Prepared by:** CTO Board (with Innovation Board requirements)  
**For:** The Coder (Claude Code implementation)

---

## Executive Summary

This document provides complete instructions for building diboas-analytics v3. The approach is **HYBRID** â€” we preserve existing validated business logic while adding new infrastructure for B2B extensibility.

### Key Principles

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                           IMPLEMENTATION APPROACH                            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚   âœ… KEEP: Existing algorithms (Battle Test, Monte Carlo, Validators)       â”‚
â”‚   âœ… WRAP: Existing code in Registry pattern for extensibility             â”‚
â”‚   âœ… ADD: New collectors, Adelaide generator, multi-channel outputs        â”‚
â”‚   âœ… REFERENCE: Manual execution results as validation baseline            â”‚
â”‚                                                                             â”‚
â”‚   âŒ DON'T: Rewrite working business logic                                  â”‚
â”‚   âŒ DON'T: Delete validated code                                           â”‚
â”‚   âŒ DON'T: Ignore manual execution outputs                                 â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Budget Targets

| Phase | Timeline | Infrastructure Cost | Revenue Required |
|-------|----------|---------------------|------------------|
| Phase 1 | Weeks 1-4 | $0/month | $0 |
| Phase 2 | When first B2B client | $5-50/month | $99+/month |
| Phase 3 | 5+ clients | $100-500/month | $500+/month |
| Phase 4 | Enterprise demand | $500+/month | $2000+/month |

---

## Table of Contents

1. [Architecture Principles](#1-architecture-principles)
2. [Current State Assessment](#2-current-state-assessment)
3. [Target Directory Structure](#3-target-directory-structure)
4. [Phase 1: Core Pipeline ($0)](#4-phase-1-core-pipeline)
5. [Phase 2: API Layer (First Client)](#5-phase-2-api-layer)
6. [Phase 3: B2B Platform (Scale)](#6-phase-3-b2b-platform)
7. [Phase 4: Enterprise Features](#7-phase-4-enterprise-features)
8. [Reference: Existing Code to Preserve](#8-reference-existing-code-to-preserve)
9. [Reference: Manual Execution Results](#9-reference-manual-execution-results)
10. [Reference: Configuration Schemas](#10-reference-configuration-schemas)
11. [Appendix: Code Templates](#appendix-a-code-templates)

---

## 1. Architecture Principles

### 1.1 The 12 Principles (Adapted for Analytics)

| # | Principle | Application | Priority |
|---|-----------|-------------|----------|
| 1 | Domain-Driven Design | Strategy, Protocol, Simulation domains | MEDIUM |
| 2 | Event-Driven | Hooks for future events (empty now) | LOW (hooks only) |
| 3 | Service Agnostic | All collectors use abstract interface | HIGH |
| 4 | Code Reusability | Shared validators, formatters | HIGH |
| 5 | Semantic Naming | Clear naming conventions | HIGH |
| 6 | File Decoupling | Max 200 lines per file | MEDIUM |
| 7 | Error Handling | Retry, fallback, graceful degradation | HIGH |
| 8 | Security | API key management, output sanitization | HIGH |
| 9 | Performance | 10K Monte Carlo < 60s | MEDIUM |
| 10 | Observability | Logging with correlation IDs | HIGH |
| 11 | Concurrency | Idempotent operations | MEDIUM |
| 12 | Testability | 80% coverage target | HIGH |

### 1.2 Registry Pattern (Core Architecture)

All components are registered in type-safe registries that enable:
- Runtime discovery of available implementations
- Configuration-driven activation per tenant
- Easy addition of new implementations without code changes

```python
# Pattern used throughout the system
@SomeRegistry.register("implementation_name")
class SomeImplementation(BaseClass):
    """Implementations are discovered via decorators."""
    pass

# Usage
registry = SomeRegistry()
impl = registry.get("implementation_name", config)
result = impl.execute(data)
```

### 1.3 Tenant-Aware Design

Every operation is scoped to a tenant from day one:

```python
# Even for diBoaS-only Phase 1, we use tenant context
tenant = TenantContext.load("diboas")  # Default tenant
pipeline = Pipeline(tenant=tenant)
pipeline.run()
```

---

## 2. Current State Assessment

### 2.1 What EXISTS and Must Be PRESERVED

Based on CODEBASE_AUDIT_REPORT.md:

| Component | Location | Status | Action |
|-----------|----------|--------|--------|
| Battle Test Engine | `src/engines/battle_test.py` | âœ… Working | WRAP in registry |
| Monte Carlo Engine | `src/engines/monte_carlo.py` | âœ… Working | WRAP in registry |
| Validators CV-01 to CV-07 | `src/validators/result_validator.py` | âœ… Working | WRAP in registry |
| Domain Models | `src/domain/*.py` | âœ… Working | KEEP as-is |
| File Loader | `src/collectors/file_loader.py` | âœ… Working | WRAP in registry |
| Reporters | `src/reporters/*.py` | âœ… Working | WRAP in registry |
| Configuration | `config/*.py` | âœ… Working | MIGRATE to YAML |
| Tests | `tests/*.py` | âœ… Working | EXTEND |

### 2.2 What DOESN'T EXIST and Must Be CREATED

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

### 2.3 Current Limitations to Address

| Limitation | Current State | Target State |
|------------|---------------|--------------|
| Data collection | CSV files only | Live APIs + CSV fallback |
| Adelaide | Documentation only | Working code generator |
| Output channels | MD/JSON only | Email, Substack, Twitter, LinkedIn, Website |
| Configuration | Python files | YAML per tenant |
| Extensibility | Hardcoded | Registry pattern |
| API access | CLI only | REST API (Phase 2) |
| CI/CD | None | GitHub Actions |

---

## 3. Target Directory Structure

```
diboas-analytics/
â”œâ”€â”€ main.py                          # CLI entry point
â”œâ”€â”€ requirements.txt                 # Python dependencies
â”œâ”€â”€ pyproject.toml                   # Project metadata (NEW)
â”œâ”€â”€ .env.example                     # Environment template
â”œâ”€â”€ CLAUDE.md                        # Claude Code guidance
â”‚
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/                   # NEW - CI/CD
â”‚       â”œâ”€â”€ daily-collection.yml     # Daily at 2 AM UTC
â”‚       â”œâ”€â”€ weekly-analytics.yml     # Sunday 3 AM UTC
â”‚       â”œâ”€â”€ adelaide-daily.yml       # Daily newsletter generation
â”‚       â””â”€â”€ tests.yml                # PR validation
â”‚
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ tenants/                     # NEW - Per-tenant configuration
â”‚   â”‚   â””â”€â”€ diboas.yaml              # Default tenant
â”‚   â”œâ”€â”€ tiers.yaml                   # NEW - Feature tiers (Free/Starter/Pro/Enterprise)
â”‚   â”œâ”€â”€ strategies.yaml              # MIGRATED from JSON
â”‚   â”œâ”€â”€ protocols.yaml               # NEW - Protocol definitions
â”‚   â”œâ”€â”€ thresholds.yaml              # NEW - Alert thresholds
â”‚   â”œâ”€â”€ sources.yaml                 # NEW - Data source configuration
â”‚   â””â”€â”€ adelaide.yaml                # NEW - Newsletter configuration
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚
â”‚   â”œâ”€â”€ registries/                  # NEW - Plugin framework
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py                  # Registry base class
â”‚   â”‚   â”œâ”€â”€ collector_registry.py    # Data collectors
â”‚   â”‚   â”œâ”€â”€ validator_registry.py    # Validation gates
â”‚   â”‚   â”œâ”€â”€ engine_registry.py       # Analytics engines
â”‚   â”‚   â”œâ”€â”€ trigger_registry.py      # Alert triggers
â”‚   â”‚   â”œâ”€â”€ persona_registry.py      # Adelaide personas
â”‚   â”‚   â””â”€â”€ output_registry.py       # Output formatters & distributors
â”‚   â”‚
â”‚   â”œâ”€â”€ collectors/                  # EXTENDED
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py                  # KEEP - Abstract base
â”‚   â”‚   â”œâ”€â”€ file_loader.py           # KEEP - CSV loading
â”‚   â”‚   â”œâ”€â”€ fred_collector.py        # NEW - FRED API
â”‚   â”‚   â”œâ”€â”€ yahoo_collector.py       # NEW - Yahoo Finance API
â”‚   â”‚   â”œâ”€â”€ defillama_collector.py   # NEW - DeFiLlama API
â”‚   â”‚   â”œâ”€â”€ coingecko_collector.py   # NEW - CoinGecko API
â”‚   â”‚   â”œâ”€â”€ etherscan_collector.py   # NEW - Etherscan API
â”‚   â”‚   â””â”€â”€ alternative_collector.py # NEW - Fear & Greed API
â”‚   â”‚
â”‚   â”œâ”€â”€ validators/                  # EXTENDED
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ result_validator.py      # KEEP - CV-01 to CV-07
â”‚   â”‚   â”œâ”€â”€ gate1_schema.py          # NEW - Schema validation
â”‚   â”‚   â”œâ”€â”€ gate2_analytics.py       # NEW - Analytics validation
â”‚   â”‚   â”œâ”€â”€ gate3_intelligence.py    # NEW - Trigger validation
â”‚   â”‚   â””â”€â”€ gate4_content.py         # NEW - Content validation
â”‚   â”‚
â”‚   â”œâ”€â”€ engines/                     # KEEP - Wrap in registry
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ battle_test.py           # KEEP - Historical backtesting
â”‚   â”‚   â”œâ”€â”€ monte_carlo.py           # KEEP - Risk simulation
â”‚   â”‚   â”œâ”€â”€ monitoring.py            # KEEP - Protocol health
â”‚   â”‚   â”œâ”€â”€ anomaly.py               # KEEP - ML anomaly detection
â”‚   â”‚   â””â”€â”€ dream_mode_export.py     # KEEP - Consumer export
â”‚   â”‚
â”‚   â”œâ”€â”€ triggers/                    # NEW - Alert system
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py                  # Trigger base class
â”‚   â”‚   â”œâ”€â”€ protocol_triggers.py     # Protocol health triggers
â”‚   â”‚   â”œâ”€â”€ market_triggers.py       # Market condition triggers
â”‚   â”‚   â”œâ”€â”€ macro_triggers.py        # Macro indicator triggers
â”‚   â”‚   â”œâ”€â”€ estate_triggers.py       # Estate wallet triggers
â”‚   â”‚   â”œâ”€â”€ whale_triggers.py        # Whale movement triggers
â”‚   â”‚   â””â”€â”€ sentiment_triggers.py    # Sentiment triggers
â”‚   â”‚
â”‚   â”œâ”€â”€ adelaide/                    # NEW - Newsletter system
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ generator.py             # Content generation orchestrator
â”‚   â”‚   â”œâ”€â”€ regime.py                # Regime classification
â”‚   â”‚   â”œâ”€â”€ templates/               # Content templates
â”‚   â”‚   â”‚   â”œâ”€â”€ daily_calm.md
â”‚   â”‚   â”‚   â”œâ”€â”€ daily_alert.md
â”‚   â”‚   â”‚   â”œâ”€â”€ weekly_summary.md
â”‚   â”‚   â”‚   â””â”€â”€ crisis_communication.md
â”‚   â”‚   â”œâ”€â”€ personas/                # Persona adapters
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ base.py              # Persona base class
â”‚   â”‚   â”‚   â”œâ”€â”€ ana.py               # Conservative (warm, emoji-rich)
â”‚   â”‚   â”‚   â”œâ”€â”€ maria.py             # Balanced (educational)
â”‚   â”‚   â”‚   â””â”€â”€ felipe.py            # Aggressive (data-forward)
â”‚   â”‚   â””â”€â”€ formatters/              # Output formatters
â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚       â”œâ”€â”€ newsletter_html.py   # Full HTML newsletter
â”‚   â”‚       â”œâ”€â”€ newsletter_md.py     # Markdown newsletter
â”‚   â”‚       â”œâ”€â”€ website_teaser.py    # Partial content for website
â”‚   â”‚       â”œâ”€â”€ substack.py          # Substack format
â”‚   â”‚       â”œâ”€â”€ twitter_thread.py    # Twitter thread (280 char chunks)
â”‚   â”‚       â”œâ”€â”€ linkedin_post.py     # LinkedIn professional format
â”‚   â”‚       â””â”€â”€ instagram_carousel.py # Visual summary (manual)
â”‚   â”‚
â”‚   â”œâ”€â”€ distributors/                # NEW - Delivery channels
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py                  # Distributor base class
â”‚   â”‚   â”œâ”€â”€ email_resend.py          # Resend API
â”‚   â”‚   â”œâ”€â”€ slack_webhook.py         # Slack notifications
â”‚   â”‚   â”œâ”€â”€ static_file.py           # Static file output
â”‚   â”‚   â””â”€â”€ whatsapp.py              # WhatsApp Business (Phase 2)
â”‚   â”‚
â”‚   â”œâ”€â”€ policies/                    # NEW - Access control
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â””â”€â”€ data_access.py           # B2B data restrictions
â”‚   â”‚
â”‚   â”œâ”€â”€ domain/                      # KEEP - Data models
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ strategy.py
â”‚   â”‚   â”œâ”€â”€ protocol.py
â”‚   â”‚   â”œâ”€â”€ simulation.py
â”‚   â”‚   â”œâ”€â”€ alert.py
â”‚   â”‚   â””â”€â”€ dream_mode.py
â”‚   â”‚
â”‚   â”œâ”€â”€ reporters/                   # KEEP - Output formatters
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ csv_reporter.py
â”‚   â”‚   â”œâ”€â”€ json_reporter.py
â”‚   â”‚   â””â”€â”€ markdown_reporter.py
â”‚   â”‚
â”‚   â”œâ”€â”€ models/                      # KEEP - ML models
â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚
â”‚   â”œâ”€â”€ commands/                    # KEEP - CLI commands
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ collect.py
â”‚   â”‚   â”œâ”€â”€ battle_test_cmd.py
â”‚   â”‚   â”œâ”€â”€ monte_carlo_cmd.py
â”‚   â”‚   â”œâ”€â”€ monitor_cmd.py
â”‚   â”‚   â”œâ”€â”€ anomaly_cmd.py
â”‚   â”‚   â”œâ”€â”€ dream_mode_cmd.py
â”‚   â”‚   â”œâ”€â”€ adelaide_cmd.py          # NEW - Adelaide generation
â”‚   â”‚   â””â”€â”€ full_pipeline.py
â”‚   â”‚
â”‚   â”œâ”€â”€ utils/                       # KEEP - Utilities
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ proxies.py
â”‚   â”‚   â”œâ”€â”€ dates.py
â”‚   â”‚   â”œâ”€â”€ logging.py
â”‚   â”‚   â”œâ”€â”€ hashing.py
â”‚   â”‚   â”œâ”€â”€ retry.py
â”‚   â”‚   â”œâ”€â”€ validation.py
â”‚   â”‚   â”œâ”€â”€ errors.py
â”‚   â”‚   â””â”€â”€ audit.py
â”‚   â”‚
â”‚   â””â”€â”€ api/                         # NEW - REST API (Phase 2)
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ main.py                  # FastAPI app
â”‚       â”œâ”€â”€ auth.py                  # API key authentication
â”‚       â”œâ”€â”€ routes/
â”‚       â”‚   â”œâ”€â”€ strategies.py
â”‚       â”‚   â”œâ”€â”€ analytics.py
â”‚       â”‚   â”œâ”€â”€ adelaide.py
â”‚       â”‚   â””â”€â”€ alerts.py
â”‚       â””â”€â”€ middleware/
â”‚           â”œâ”€â”€ tenant.py            # Tenant resolution
â”‚           â”œâ”€â”€ rate_limit.py        # Rate limiting
â”‚           â””â”€â”€ tier_enforcement.py  # Feature tier checks
â”‚
â”œâ”€â”€ data/                            # Historical data (bundled)
â”‚   â”œâ”€â”€ crypto_prices.csv
â”‚   â”œâ”€â”€ defillama_historical_apy.csv
â”‚   â”œâ”€â”€ treasury_yields.csv
â”‚   â””â”€â”€ ... (20 CSV files)
â”‚
â”œâ”€â”€ outputs/                         # Generated results
â”‚   â”œâ”€â”€ battle_test/
â”‚   â”œâ”€â”€ monte_carlo/
â”‚   â”œâ”€â”€ adelaide/
â”‚   â””â”€â”€ public/                      # Vercel-served static files
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ fixtures/                    # NEW - Test fixtures
â”‚   â”‚   â””â”€â”€ manual_execution/        # Copy of manual execution results
â”‚   â”œâ”€â”€ test_validators.py
â”‚   â”œâ”€â”€ test_battle_test.py
â”‚   â”œâ”€â”€ test_monte_carlo.py
â”‚   â”œâ”€â”€ test_collectors.py
â”‚   â”œâ”€â”€ test_dream_mode.py
â”‚   â”œâ”€â”€ test_adelaide.py             # NEW
â”‚   â””â”€â”€ test_registries.py           # NEW
â”‚
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ collect.py                   # Data collection entry
â”‚   â”œâ”€â”€ analyze.py                   # Analysis entry
â”‚   â”œâ”€â”€ generate_adelaide.py         # Newsletter generation
â”‚   â””â”€â”€ export_public.py             # Public JSON export
â”‚
â””â”€â”€ cto_handoff_package/             # KEEP - Reference documentation
    â”œâ”€â”€ 01_collection_specs/
    â”œâ”€â”€ 02_collection_support/
    â”œâ”€â”€ 03_validation_methodology/
    â”œâ”€â”€ 04_validation_results/
    â”œâ”€â”€ 05_architecture/
    â””â”€â”€ 06_results_manual_execution/ # CRITICAL - Validation baseline
```

---

## 4. Phase 1: Core Pipeline ($0)

**Timeline:** Weeks 1-4  
**Cost:** $0/month  
**Goal:** Working pipeline for diBoaS with B2B-ready architecture

### 4.1 Week 1: Registry Framework

Create the plugin architecture that wraps existing code.

#### 4.1.1 Base Registry Class

```python
# src/registries/base.py

from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic, Optional, Any
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
    
    def get(self, name: str, config: Optional[Dict[str, Any]] = None) -> T:
        """Get an instance of a registered implementation."""
        if name not in self._registry:
            available = list(self._registry.keys())
            raise KeyError(f"Unknown implementation: {name}. Available: {available}")
        
        impl_class = self._registry[name]
        return impl_class(config or {})
    
    def list_available(self) -> list:
        """List all registered implementations."""
        return list(self._registry.keys())
    
    def is_registered(self, name: str) -> bool:
        """Check if an implementation is registered."""
        return name in self._registry


class RegistryComponent(ABC):
    """Base class for all registry-managed components."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the component's main logic."""
        pass
    
    def validate_config(self) -> bool:
        """Validate component configuration."""
        return True
```

#### 4.1.2 Collector Registry (Wrapping Existing Code)

```python
# src/registries/collector_registry.py

from typing import Dict, Any, List
from datetime import datetime
from .base import Registry, RegistryComponent

class DataCollector(RegistryComponent):
    """Base class for all data collectors."""
    
    @property
    def source_name(self) -> str:
        raise NotImplementedError
    
    @property
    def supported_tickers(self) -> List[str]:
        raise NotImplementedError
    
    def collect(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect data for specified tickers and date range."""
        raise NotImplementedError
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registry interface - calls collect()."""
        return self.collect(
            tickers=data.get("tickers", self.supported_tickers),
            start_date=data.get("start_date", datetime(2020, 1, 1)),
            end_date=data.get("end_date", datetime.now())
        )


class CollectorRegistry(Registry[DataCollector]):
    """Registry for data collectors."""
    pass


# WRAP EXISTING FILE LOADER
from src.collectors.file_loader import FileLoader as ExistingFileLoader

@CollectorRegistry.register("csv_file")
class CSVFileCollector(DataCollector):
    """Wrapper for existing FileLoader - provides CSV fallback."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._loader = ExistingFileLoader()  # Reuse existing code!
    
    @property
    def source_name(self) -> str:
        return "csv_file"
    
    @property
    def supported_tickers(self) -> List[str]:
        return ["*"]  # Supports any ticker in bundled files
    
    def collect(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Load from bundled CSV files."""
        data_type = self.config.get("data_type", "defillama")
        df = self._loader.load(data_type)
        
        # Filter by date range
        if "date" in df.columns:
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        
        return {
            "source": self.source_name,
            "data_type": data_type,
            "rows": len(df),
            "data": df.to_dict(orient="records")
        }
```

#### 4.1.3 Engine Registry (Wrapping Existing Code)

```python
# src/registries/engine_registry.py

from typing import Dict, Any
from .base import Registry, RegistryComponent

class AnalyticsEngine(RegistryComponent):
    """Base class for all analytics engines."""
    
    @property
    def engine_name(self) -> str:
        raise NotImplementedError
    
    def run_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the analysis and return results."""
        raise NotImplementedError
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registry interface - calls run_analysis()."""
        return self.run_analysis(data)


class EngineRegistry(Registry[AnalyticsEngine]):
    """Registry for analytics engines."""
    pass


# WRAP EXISTING BATTLE TEST ENGINE
from src.engines.battle_test import BattleTestEngine as ExistingBattleTest

@EngineRegistry.register("battle_test")
class BattleTestEnginePlugin(AnalyticsEngine):
    """Wrapper for existing BattleTestEngine."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._engine = ExistingBattleTest()  # Reuse existing code!
    
    @property
    def engine_name(self) -> str:
        return "battle_test"
    
    def run_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run Battle Test using existing engine."""
        scenarios = self.config.get("scenarios", [
            "covid_crash",
            "ftx_collapse", 
            "terra_luna",
            "bear_2022",
            "recovery_2023"
        ])
        
        # Call existing engine methods
        results = self._engine.run(
            strategies=data["strategies"],
            historical_data=data["historical_data"],
            scenarios=scenarios
        )
        
        return {
            "engine": self.engine_name,
            "scenarios": scenarios,
            "results": results
        }


# WRAP EXISTING MONTE CARLO ENGINE
from src.engines.monte_carlo import MonteCarloEngine as ExistingMonteCarlo

@EngineRegistry.register("monte_carlo")
class MonteCarloEnginePlugin(AnalyticsEngine):
    """Wrapper for existing MonteCarloEngine."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._engine = ExistingMonteCarlo()  # Reuse existing code!
    
    @property
    def engine_name(self) -> str:
        return "monte_carlo"
    
    def run_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run Monte Carlo using existing engine."""
        num_simulations = self.config.get("num_simulations", 10000)
        projection_years = self.config.get("projection_years", 4)
        
        results = self._engine.run(
            strategies=data["strategies"],
            historical_data=data["historical_data"],
            num_simulations=num_simulations,
            projection_years=projection_years
        )
        
        return {
            "engine": self.engine_name,
            "num_simulations": num_simulations,
            "projection_years": projection_years,
            "results": results
        }
```

#### 4.1.4 Validator Registry (Wrapping Existing Code)

```python
# src/registries/validator_registry.py

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from .base import Registry, RegistryComponent

class ValidationStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"

@dataclass
class ValidationIssue:
    code: str
    severity: str  # "error", "warning", "info"
    message: str
    field: str = ""
    actual_value: str = ""
    expected_value: str = ""
    remediation: str = ""

@dataclass
class ValidationResult:
    gate: str
    status: ValidationStatus
    issues: List[ValidationIssue]
    metadata: Dict[str, Any]


class Validator(RegistryComponent):
    """Base class for all validators."""
    
    @property
    def gate_name(self) -> str:
        raise NotImplementedError
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data and return result."""
        raise NotImplementedError
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registry interface - calls validate()."""
        result = self.validate(data)
        return {
            "gate": result.gate,
            "status": result.status.value,
            "issues": [vars(i) for i in result.issues],
            "metadata": result.metadata
        }


class ValidatorRegistry(Registry[Validator]):
    """Registry for validators."""
    pass


# WRAP EXISTING RESULT VALIDATOR (CV-01 to CV-07)
from src.validators.result_validator import ResultValidator as ExistingValidator

@ValidatorRegistry.register("result_validator")
class ResultValidatorPlugin(Validator):
    """Wrapper for existing ResultValidator (CV-01 to CV-07)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._validator = ExistingValidator()  # Reuse existing code!
    
    @property
    def gate_name(self) -> str:
        return "gate_2_analytics"
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate using existing CV-01 to CV-07 rules."""
        # Call existing validator
        validation_report = self._validator.validate(data["results"])
        
        # Convert to standard format
        issues = []
        for error in validation_report.errors:
            issues.append(ValidationIssue(
                code=error.rule,
                severity="error",
                message=error.message,
                field=error.field,
                actual_value=str(error.actual),
                expected_value=str(error.expected)
            ))
        
        for warning in validation_report.warnings:
            issues.append(ValidationIssue(
                code=warning.rule,
                severity="warning",
                message=warning.message
            ))
        
        status = ValidationStatus.PASS
        if any(i.severity == "error" for i in issues):
            status = ValidationStatus.FAIL
        elif any(i.severity == "warning" for i in issues):
            status = ValidationStatus.WARN
        
        return ValidationResult(
            gate=self.gate_name,
            status=status,
            issues=issues,
            metadata={"rules_checked": ["CV-01", "CV-02", "CV-03", "CV-04", "CV-05", "CV-06", "CV-07"]}
        )
```

### 4.2 Week 2: Live API Collectors

Add new collectors for live data while keeping CSV fallback.

#### 4.2.1 FRED Collector

```python
# src/collectors/fred_collector.py

import requests
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
from src.registries.collector_registry import CollectorRegistry, DataCollector

@CollectorRegistry.register("fred")
class FREDCollector(DataCollector):
    """FRED API collector for macroeconomic data."""
    
    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
    
    SERIES_MAP = {
        "DGS10": "10Y Treasury Yield",
        "DGS2": "2Y Treasury Yield", 
        "T10YIE": "10Y Breakeven Inflation",
        "DFF": "Fed Funds Rate",
        "WM2NS": "M2 Money Supply",
        "BAMLH0A0HYM2": "High Yield Spread",
        "BAMLC0A4CBBB": "BBB Spread"
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("FRED_API_KEY")
    
    @property
    def source_name(self) -> str:
        return "fred"
    
    @property
    def supported_tickers(self) -> List[str]:
        return list(self.SERIES_MAP.keys())
    
    def collect(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect FRED data for specified series."""
        all_data = []
        
        for series_id in tickers:
            if series_id not in self.SERIES_MAP:
                self._logger.warning(f"Unknown FRED series: {series_id}")
                continue
            
            try:
                params = {
                    "series_id": series_id,
                    "api_key": self.api_key,
                    "file_type": "json",
                    "observation_start": start_date.strftime("%Y-%m-%d"),
                    "observation_end": end_date.strftime("%Y-%m-%d")
                }
                
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                
                observations = response.json().get("observations", [])
                
                for obs in observations:
                    if obs["value"] != ".":  # FRED uses "." for missing
                        all_data.append({
                            "date": obs["date"],
                            "series_id": series_id,
                            "series_name": self.SERIES_MAP[series_id],
                            "value": float(obs["value"])
                        })
                        
            except Exception as e:
                self._logger.error(f"Failed to fetch {series_id}: {e}")
                continue
        
        return {
            "source": self.source_name,
            "rows": len(all_data),
            "series_collected": len(set(d["series_id"] for d in all_data)),
            "data": all_data
        }
```

#### 4.2.2 Yahoo Finance Collector

```python
# src/collectors/yahoo_collector.py

import yfinance as yf
from datetime import datetime
from typing import Dict, Any, List
from src.registries.collector_registry import CollectorRegistry, DataCollector

@CollectorRegistry.register("yahoo")
class YahooFinanceCollector(DataCollector):
    """Yahoo Finance collector for market data."""
    
    TICKER_MAP = {
        # Crypto
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum", 
        "SOL-USD": "Solana",
        
        # Equity Indices
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
        "^RUT": "Russell 2000",
        
        # Rotation ETFs
        "SPY": "S&P 500 ETF",
        "TLT": "20+ Year Treasury",
        "XLF": "Financials ETF",
        "XLU": "Utilities ETF",
        "IWM": "Russell 2000 ETF",
        
        # Commodities
        "GC=F": "Gold Futures",
        "CL=F": "Crude Oil Futures",
        
        # Volatility
        "^VIX": "VIX"
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
    
    @property
    def source_name(self) -> str:
        return "yahoo"
    
    @property
    def supported_tickers(self) -> List[str]:
        return list(self.TICKER_MAP.keys())
    
    def collect(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect Yahoo Finance data."""
        all_data = []
        
        for ticker in tickers:
            try:
                yf_ticker = yf.Ticker(ticker)
                hist = yf_ticker.history(
                    start=start_date.strftime("%Y-%m-%d"),
                    end=end_date.strftime("%Y-%m-%d")
                )
                
                for date, row in hist.iterrows():
                    all_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "ticker": ticker,
                        "ticker_name": self.TICKER_MAP.get(ticker, ticker),
                        "open": row["Open"],
                        "high": row["High"],
                        "low": row["Low"],
                        "close": row["Close"],
                        "volume": row["Volume"]
                    })
                    
            except Exception as e:
                self._logger.error(f"Failed to fetch {ticker}: {e}")
                continue
        
        return {
            "source": self.source_name,
            "rows": len(all_data),
            "tickers_collected": len(set(d["ticker"] for d in all_data)),
            "data": all_data
        }
```

#### 4.2.3 DeFiLlama Collector

```python
# src/collectors/defillama_collector.py

import requests
from datetime import datetime
from typing import Dict, Any, List
from src.registries.collector_registry import CollectorRegistry, DataCollector

@CollectorRegistry.register("defillama")
class DeFiLlamaCollector(DataCollector):
    """DeFiLlama API collector for DeFi protocol data."""
    
    BASE_URL = "https://api.llama.fi"
    
    PROTOCOL_MAP = {
        "aave-v3": "Aave V3",
        "compound-v3": "Compound V3",
        "sky": "Sky (MakerDAO)",
        "lido": "Lido",
        "jito": "Jito",
        "jupiter-lp": "Jupiter JLP"
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
    
    @property
    def source_name(self) -> str:
        return "defillama"
    
    @property
    def supported_tickers(self) -> List[str]:
        return list(self.PROTOCOL_MAP.keys())
    
    def collect(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect DeFiLlama protocol data."""
        all_data = []
        
        for protocol in tickers:
            try:
                # Get protocol TVL history
                response = requests.get(
                    f"{self.BASE_URL}/protocol/{protocol}",
                    timeout=30
                )
                response.raise_for_status()
                
                protocol_data = response.json()
                tvl_history = protocol_data.get("tvl", [])
                
                for entry in tvl_history:
                    entry_date = datetime.fromtimestamp(entry["date"])
                    if start_date <= entry_date <= end_date:
                        all_data.append({
                            "date": entry_date.strftime("%Y-%m-%d"),
                            "protocol": protocol,
                            "protocol_name": self.PROTOCOL_MAP.get(protocol, protocol),
                            "tvl_usd": entry["totalLiquidityUSD"]
                        })
                        
            except Exception as e:
                self._logger.error(f"Failed to fetch {protocol}: {e}")
                continue
        
        # Get yields separately
        try:
            yields_response = requests.get(f"{self.BASE_URL}/pools", timeout=30)
            yields_response.raise_for_status()
            pools = yields_response.json().get("data", [])
            
            for pool in pools:
                if pool.get("project") in tickers:
                    all_data.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "protocol": pool["project"],
                        "pool": pool.get("symbol", "unknown"),
                        "chain": pool.get("chain", "unknown"),
                        "apy": pool.get("apy", 0),
                        "tvl_usd": pool.get("tvlUsd", 0)
                    })
        except Exception as e:
            self._logger.error(f"Failed to fetch yields: {e}")
        
        return {
            "source": self.source_name,
            "rows": len(all_data),
            "protocols_collected": len(set(d.get("protocol") for d in all_data)),
            "data": all_data
        }
```

### 4.3 Week 3: Adelaide Content Generator

Create the newsletter generation system using manual execution outputs as reference.

#### 4.3.1 Adelaide Generator

```python
# src/adelaide/generator.py

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json

from src.registries.persona_registry import PersonaRegistry
from src.registries.output_registry import OutputRegistry


class MarketRegime(Enum):
    RISK_ON_BULL = "risk_on_bull"
    RISK_OFF_BEAR = "risk_off_bear"
    NEUTRAL = "neutral"
    CRISIS = "crisis"


@dataclass
class AdelaideContent:
    """Generated Adelaide content."""
    edition_date: datetime
    regime: MarketRegime
    regime_confidence: float
    crisis_level: int  # 0-4
    alerts: List[Dict[str, Any]]
    sections: Dict[str, str]
    metadata: Dict[str, Any]


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
        
        # 2. Select template based on regime and crisis level
        crisis_level = self._assess_crisis_level(analytics_data)
        template = self._select_template(regime, crisis_level)
        
        # 3. Assemble base content
        base_content = self._assemble_content(
            analytics_data=analytics_data,
            regime=regime,
            template=template
        )
        
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
            "edition_date": datetime.now().isoformat(),
            "persona": persona,
            "locale": locale,
            "regime": regime.value,
            "regime_confidence": confidence,
            "crisis_level": crisis_level,
            "outputs": outputs,
            "metadata": {
                "template": template,
                "alerts_count": len(analytics_data.get("alerts", [])),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _classify_regime(self, data: Dict[str, Any]) -> tuple:
        """Classify market regime from analytics data."""
        # Use regime classification from Layer 4
        regime_data = data.get("regime_classification", {})
        
        regime_map = {
            "risk_on_bull": MarketRegime.RISK_ON_BULL,
            "risk_off_bear": MarketRegime.RISK_OFF_BEAR,
            "neutral": MarketRegime.NEUTRAL,
            "crisis": MarketRegime.CRISIS
        }
        
        regime_str = regime_data.get("regime", "neutral")
        confidence = regime_data.get("confidence", 0.5)
        
        return regime_map.get(regime_str, MarketRegime.NEUTRAL), confidence
    
    def _assess_crisis_level(self, data: Dict[str, Any]) -> int:
        """Assess crisis level (0-4) from analytics data."""
        alerts = data.get("alerts", [])
        
        p0_count = sum(1 for a in alerts if a.get("priority") == "P0")
        p1_count = sum(1 for a in alerts if a.get("priority") == "P1")
        
        if p0_count > 0:
            return 4  # Critical
        elif p1_count >= 3:
            return 3  # High
        elif p1_count >= 1:
            return 2  # Elevated
        elif len(alerts) > 5:
            return 1  # Low
        else:
            return 0  # Normal
    
    def _select_template(self, regime: MarketRegime, crisis_level: int) -> str:
        """Select appropriate template based on conditions."""
        if crisis_level >= 3:
            return "crisis_communication"
        elif crisis_level >= 2:
            return "daily_alert"
        else:
            return "daily_calm"
    
    def _assemble_content(
        self,
        analytics_data: Dict[str, Any],
        regime: MarketRegime,
        template: str
    ) -> Dict[str, Any]:
        """Assemble raw content sections."""
        
        # Extract key data points
        battle_test = analytics_data.get("battle_test", {})
        monte_carlo = analytics_data.get("monte_carlo", {})
        risk_metrics = analytics_data.get("risk_metrics", {})
        alerts = analytics_data.get("alerts", [])
        anomalies = analytics_data.get("anomalies", [])
        
        return {
            "template": template,
            "regime": regime,
            "sections": {
                "greeting": self._generate_greeting(regime),
                "market_overview": self._generate_market_overview(analytics_data),
                "strategy_spotlight": self._generate_strategy_spotlight(battle_test),
                "alerts_summary": self._generate_alerts_summary(alerts),
                "looking_ahead": self._generate_looking_ahead(monte_carlo),
                "wisdom": self._generate_wisdom(regime),
                "disclaimer": self._generate_disclaimer()
            },
            "data": {
                "regime": regime.value,
                "vix": analytics_data.get("market_data", {}).get("vix"),
                "fear_greed": analytics_data.get("sentiment", {}).get("fear_greed"),
                "top_strategy": self._get_top_strategy(battle_test),
                "alerts": alerts
            }
        }
    
    # Helper methods for content generation
    def _generate_greeting(self, regime: MarketRegime) -> str:
        greetings = {
            MarketRegime.RISK_ON_BULL: "Markets are showing strength today.",
            MarketRegime.RISK_OFF_BEAR: "Markets are cautious today.",
            MarketRegime.NEUTRAL: "Markets are steady today.",
            MarketRegime.CRISIS: "Important market update."
        }
        return greetings.get(regime, "Good morning.")
    
    def _generate_market_overview(self, data: Dict[str, Any]) -> str:
        market = data.get("market_data", {})
        return f"VIX at {market.get('vix', 'N/A')}, sentiment shows {market.get('fear_greed', 'N/A')}."
    
    def _generate_strategy_spotlight(self, battle_test: Dict[str, Any]) -> str:
        return "Strategy performance analysis available."
    
    def _generate_alerts_summary(self, alerts: List[Dict]) -> str:
        if not alerts:
            return "No significant alerts today."
        return f"{len(alerts)} items to monitor."
    
    def _generate_looking_ahead(self, monte_carlo: Dict[str, Any]) -> str:
        return "Forward projections based on current conditions."
    
    def _generate_wisdom(self, regime: MarketRegime) -> str:
        wisdom = {
            MarketRegime.RISK_ON_BULL: "Patience in good times prepares us for challenges.",
            MarketRegime.RISK_OFF_BEAR: "Every storm passes. Stay the course.",
            MarketRegime.NEUTRAL: "Steady hands build lasting wealth.",
            MarketRegime.CRISIS: "This too shall pass. Your strategy is designed for this."
        }
        return wisdom.get(regime, "Trust your plan.")
    
    def _generate_disclaimer(self) -> str:
        return "This is educational content, not financial advice. Past performance does not guarantee future results."
    
    def _get_top_strategy(self, battle_test: Dict[str, Any]) -> Optional[Dict]:
        results = battle_test.get("results", [])
        if results:
            return max(results, key=lambda x: x.get("total_return", 0))
        return None
```

#### 4.3.2 Persona Adapters

```python
# src/adelaide/personas/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.registries.base import Registry, RegistryComponent


class PersonaAdapter(RegistryComponent):
    """Base class for Adelaide persona adapters."""
    
    @property
    @abstractmethod
    def persona_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def traits(self) -> Dict[str, Any]:
        """Return persona traits (formality, emoji use, etc.)."""
        pass
    
    @abstractmethod
    def adapt(self, content: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Adapt content to this persona's voice."""
        pass


class PersonaRegistry(Registry[PersonaAdapter]):
    """Registry for Adelaide personas."""
    pass


# src/adelaide/personas/ana.py

from src.adelaide.personas.base import PersonaRegistry, PersonaAdapter

@PersonaRegistry.register("ana")
class AnaPersona(PersonaAdapter):
    """Ana - Conservative, warm, grandmother voice."""
    
    @property
    def persona_name(self) -> str:
        return "ana"
    
    @property
    def traits(self) -> Dict[str, Any]:
        return {
            "formality": "warm",
            "emoji_density": "high",  # 3-15 emojis per newsletter
            "emoji_types": ["â˜€ï¸", "ðŸŒ¸", "ðŸ’š", "ðŸ¡", "â˜•", "ðŸŒ¿", "âœ¨", "ðŸ’«", "ðŸŒˆ", "ðŸ¦‹"],
            "sentence_length": "medium",
            "use_analogies": True,
            "explain_jargon": True,
            "sign_off": "With love and steady hands"
        }
    
    def adapt(self, content: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Adapt content to Ana's warm, grandmother voice."""
        adapted = content.copy()
        sections = adapted.get("sections", {})
        
        # Add warm greeting
        sections["greeting"] = self._warm_greeting(sections.get("greeting", ""), locale)
        
        # Add emojis appropriately
        for key, text in sections.items():
            if isinstance(text, str):
                sections[key] = self._add_emojis(text)
        
        # Add wisdom closing
        sections["wisdom"] = self._add_wisdom_frame(sections.get("wisdom", ""), locale)
        
        # Add sign-off
        sections["sign_off"] = self._get_sign_off(locale)
        
        adapted["sections"] = sections
        adapted["persona"] = self.persona_name
        adapted["locale"] = locale
        
        return adapted
    
    def _warm_greeting(self, text: str, locale: str) -> str:
        greetings = {
            "en": "Good morning, dear ones! â˜€ï¸",
            "pt-br": "Bom dia, queridos! â˜€ï¸"
        }
        return greetings.get(locale, greetings["en"]) + " " + text
    
    def _add_emojis(self, text: str) -> str:
        """Add appropriate emojis to text."""
        # Simple emoji injection (production would be smarter)
        if "market" in text.lower():
            text = text.replace("market", "market ðŸŒ¿")
        if "strategy" in text.lower():
            text = text.replace("strategy", "strategy âœ¨")
        return text
    
    def _add_wisdom_frame(self, text: str, locale: str) -> str:
        frames = {
            "en": f"ðŸ’« *A word of wisdom:* {text}",
            "pt-br": f"ðŸ’« *Uma palavra de sabedoria:* {text}"
        }
        return frames.get(locale, frames["en"])
    
    def _get_sign_off(self, locale: str) -> str:
        sign_offs = {
            "en": "With love and steady hands,\nâ€” Adelaide ðŸŒ¸",
            "pt-br": "Com amor e mÃ£os firmes,\nâ€” Adelaide ðŸŒ¸"
        }
        return sign_offs.get(locale, sign_offs["en"])


# src/adelaide/personas/maria.py

@PersonaRegistry.register("maria")
class MariaPersona(PersonaAdapter):
    """Maria - Balanced, educational voice."""
    
    @property
    def persona_name(self) -> str:
        return "maria"
    
    @property
    def traits(self) -> Dict[str, Any]:
        return {
            "formality": "professional_friendly",
            "emoji_density": "medium",  # 3-8 emojis
            "emoji_types": ["ðŸ“Š", "ðŸ“ˆ", "ðŸ’¡", "âœ…", "ðŸ“Œ", "ðŸŽ¯"],
            "sentence_length": "medium",
            "use_analogies": True,
            "explain_jargon": True,
            "sign_off": "Stay informed, stay confident"
        }
    
    def adapt(self, content: Dict[str, Any], locale: str) -> Dict[str, Any]:
        adapted = content.copy()
        sections = adapted.get("sections", {})
        
        # Add educational framing
        for key, text in sections.items():
            if isinstance(text, str):
                sections[key] = self._add_educational_notes(text)
        
        sections["sign_off"] = self._get_sign_off(locale)
        
        adapted["sections"] = sections
        adapted["persona"] = self.persona_name
        adapted["locale"] = locale
        
        return adapted
    
    def _add_educational_notes(self, text: str) -> str:
        return text  # Production would add explanatory notes
    
    def _get_sign_off(self, locale: str) -> str:
        sign_offs = {
            "en": "Stay informed, stay confident ðŸ“Š\nâ€” Adelaide",
            "pt-br": "Mantenha-se informado, mantenha-se confiante ðŸ“Š\nâ€” Adelaide"
        }
        return sign_offs.get(locale, sign_offs["en"])


# src/adelaide/personas/felipe.py

@PersonaRegistry.register("felipe")
class FelipePersona(PersonaAdapter):
    """Felipe - Aggressive/Technical, data-forward voice."""
    
    @property
    def persona_name(self) -> str:
        return "felipe"
    
    @property
    def traits(self) -> Dict[str, Any]:
        return {
            "formality": "technical",
            "emoji_density": "none",  # 0 emojis
            "emoji_types": [],
            "sentence_length": "short",
            "use_analogies": False,
            "explain_jargon": False,
            "sign_off": "Data speaks."
        }
    
    def adapt(self, content: Dict[str, Any], locale: str) -> Dict[str, Any]:
        adapted = content.copy()
        sections = adapted.get("sections", {})
        
        # Remove emojis
        for key, text in sections.items():
            if isinstance(text, str):
                sections[key] = self._remove_emojis(text)
        
        # Terse sign-off
        sections["sign_off"] = self._get_sign_off(locale)
        
        adapted["sections"] = sections
        adapted["persona"] = self.persona_name
        adapted["locale"] = locale
        
        return adapted
    
    def _remove_emojis(self, text: str) -> str:
        import re
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub('', text)
    
    def _get_sign_off(self, locale: str) -> str:
        return "â€” Adelaide"
```

#### 4.3.3 Output Formatters

```python
# src/adelaide/formatters/__init__.py

from typing import Dict, Any
from src.registries.base import Registry, RegistryComponent


class OutputFormatter(RegistryComponent):
    """Base class for output formatters."""
    
    @property
    def format_name(self) -> str:
        raise NotImplementedError
    
    def format(self, content: Dict[str, Any]) -> str:
        """Format content for output channel."""
        raise NotImplementedError
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"formatted": self.format(data)}


class OutputRegistry(Registry[OutputFormatter]):
    """Registry for output formatters."""
    
    def get_formatter(self, name: str, config: Dict[str, Any] = None) -> OutputFormatter:
        return self.get(name, config)


# src/adelaide/formatters/newsletter_md.py

from src.adelaide.formatters import OutputRegistry, OutputFormatter

@OutputRegistry.register("newsletter_md")
class MarkdownNewsletterFormatter(OutputFormatter):
    """Format Adelaide content as Markdown newsletter."""
    
    @property
    def format_name(self) -> str:
        return "newsletter_md"
    
    def format(self, content: Dict[str, Any]) -> str:
        sections = content.get("sections", {})
        persona = content.get("persona", "ana")
        locale = content.get("locale", "en")
        
        md = []
        
        # Header
        md.append(f"# Adelaide Daily")
        md.append(f"*{content.get('data', {}).get('edition_date', 'Today')}*")
        md.append("")
        
        # Greeting
        if sections.get("greeting"):
            md.append(sections["greeting"])
            md.append("")
        
        # Market Overview
        md.append("## What's Happening")
        md.append(sections.get("market_overview", ""))
        md.append("")
        
        # Strategy Spotlight
        md.append("## Strategy Spotlight")
        md.append(sections.get("strategy_spotlight", ""))
        md.append("")
        
        # Alerts
        if sections.get("alerts_summary"):
            md.append("## Things to Watch")
            md.append(sections["alerts_summary"])
            md.append("")
        
        # Looking Ahead
        md.append("## Looking Ahead")
        md.append(sections.get("looking_ahead", ""))
        md.append("")
        
        # Wisdom
        if sections.get("wisdom"):
            md.append("---")
            md.append(sections["wisdom"])
            md.append("")
        
        # Sign-off
        if sections.get("sign_off"):
            md.append(sections["sign_off"])
            md.append("")
        
        # Disclaimer
        md.append("---")
        md.append(f"*{sections.get('disclaimer', '')}*")
        
        return "\n".join(md)


# src/adelaide/formatters/twitter_thread.py

@OutputRegistry.register("twitter_thread")
class TwitterThreadFormatter(OutputFormatter):
    """Format Adelaide content as Twitter thread."""
    
    MAX_TWEET = 280
    MAX_THREAD = 10
    
    @property
    def format_name(self) -> str:
        return "twitter_thread"
    
    def format(self, content: Dict[str, Any]) -> str:
        sections = content.get("sections", {})
        data = content.get("data", {})
        
        tweets = []
        
        # Tweet 1: Hook
        regime = data.get("regime", "neutral")
        tweets.append(f"ðŸ§µ Adelaide Daily Thread\n\nMarket regime: {regime.upper()}\n\nHere's what you need to know today ðŸ‘‡")
        
        # Tweet 2: Market overview
        overview = sections.get("market_overview", "")[:250]
        tweets.append(f"ðŸ“Š MARKET OVERVIEW\n\n{overview}")
        
        # Tweet 3: Strategy
        strategy = sections.get("strategy_spotlight", "")[:250]
        tweets.append(f"ðŸ’¡ STRATEGY SPOTLIGHT\n\n{strategy}")
        
        # Tweet 4: Alerts (if any)
        alerts = sections.get("alerts_summary", "")
        if alerts and alerts != "No significant alerts today.":
            tweets.append(f"âš ï¸ WATCH LIST\n\n{alerts[:250]}")
        
        # Tweet 5: Looking ahead
        ahead = sections.get("looking_ahead", "")[:250]
        tweets.append(f"ðŸ”® LOOKING AHEAD\n\n{ahead}")
        
        # Tweet 6: Wisdom + CTA
        wisdom = sections.get("wisdom", "")[:200]
        tweets.append(f"âœ¨ WISDOM\n\n{wisdom}\n\nFollow for daily updates. Like if this helped! â¤ï¸")
        
        # Format as thread
        thread = []
        for i, tweet in enumerate(tweets[:self.MAX_THREAD], 1):
            thread.append(f"[{i}/{len(tweets)}]\n{tweet}")
        
        return "\n\n---\n\n".join(thread)


# src/adelaide/formatters/website_teaser.py

@OutputRegistry.register("website_teaser")
class WebsiteTeaserFormatter(OutputFormatter):
    """Format partial content for website with CTA to full version."""
    
    @property
    def format_name(self) -> str:
        return "website_teaser"
    
    def format(self, content: Dict[str, Any]) -> str:
        sections = content.get("sections", {})
        
        teaser = []
        
        # Show greeting and market overview
        teaser.append(sections.get("greeting", ""))
        teaser.append("")
        teaser.append("## What's Happening")
        teaser.append(sections.get("market_overview", ""))
        teaser.append("")
        
        # Truncate with CTA
        teaser.append("---")
        teaser.append("")
        teaser.append("**Want the full analysis?**")
        teaser.append("")
        teaser.append("Read the complete Adelaide Daily on [Substack](https://diboas.substack.com) â†’")
        
        return "\n".join(teaser)


# src/adelaide/formatters/linkedin_post.py

@OutputRegistry.register("linkedin_post")
class LinkedInPostFormatter(OutputFormatter):
    """Format Adelaide content for LinkedIn professional audience."""
    
    @property
    def format_name(self) -> str:
        return "linkedin_post"
    
    def format(self, content: Dict[str, Any]) -> str:
        sections = content.get("sections", {})
        data = content.get("data", {})
        
        post = []
        
        # Professional hook
        regime = data.get("regime", "neutral").replace("_", " ").title()
        post.append(f"ðŸ“Š Adelaide Market Intelligence | {regime}")
        post.append("")
        
        # Key insights (bullet style for LinkedIn)
        post.append("Key observations for today:")
        post.append("")
        post.append(f"â€¢ {sections.get('market_overview', '')}")
        post.append(f"â€¢ {sections.get('strategy_spotlight', '')}")
        
        if sections.get("alerts_summary") and "No significant" not in sections["alerts_summary"]:
            post.append(f"â€¢ Watch: {sections['alerts_summary']}")
        
        post.append("")
        post.append("---")
        post.append("")
        post.append("Full analysis: diboas.substack.com")
        post.append("")
        post.append("#fintech #defi #investing #marketanalysis")
        
        return "\n".join(post)
```

### 4.4 Week 4: GitHub Actions & Integration

#### 4.4.1 Daily Collection Workflow

```yaml
# .github/workflows/daily-collection.yml

name: Daily Data Collection

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
  workflow_dispatch:  # Manual trigger

env:
  FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
  PYTHON_VERSION: '3.11'

jobs:
  collect:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run data collection
        run: |
          python scripts/collect.py --tenant diboas --all
      
      - name: Validate collected data (Gate 1)
        run: |
          python main.py validate --gate 1
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: collected-data-${{ github.run_id }}
          path: data/
          retention-days: 7
      
      - name: Commit updated data
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/
          git diff --staged --quiet || git commit -m "chore: daily data collection $(date +%Y-%m-%d)"
          git push
```

#### 4.4.2 Adelaide Daily Workflow

```yaml
# .github/workflows/adelaide-daily.yml

name: Adelaide Daily Newsletter

on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM UTC daily
  workflow_dispatch:
    inputs:
      persona:
        description: 'Persona (ana/maria/felipe)'
        required: false
        default: 'ana'
      locale:
        description: 'Locale (en/pt-br)'
        required: false
        default: 'en'

env:
  RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
  SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}

jobs:
  generate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run analytics pipeline
        run: |
          python main.py pipeline --tenant diboas --skip-collection
      
      - name: Generate Adelaide content
        run: |
          python main.py adelaide generate \
            --tenant diboas \
            --personas ana,maria,felipe \
            --locales en,pt-br \
            --formats newsletter_md,website_teaser,twitter_thread,linkedin_post
      
      - name: Validate content (Gate 4)
        run: |
          python main.py validate --gate 4
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: adelaide-${{ github.run_id }}
          path: outputs/adelaide/
          retention-days: 30
      
      - name: Commit Adelaide outputs
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add outputs/adelaide/
          git add outputs/public/
          git diff --staged --quiet || git commit -m "chore: adelaide daily $(date +%Y-%m-%d)"
          git push
      
      - name: Notify Slack
        if: always()
        run: |
          python scripts/notify_slack.py --status ${{ job.status }}
```

#### 4.4.3 Tests Workflow

```yaml
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

### 4.5 Data Access Policies (B2B Ethical Guardrails)

```python
# src/policies/data_access.py

from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass


class AccessLevel(Enum):
    FULL = "full"
    AGGREGATED = "aggregated"
    DELAYED = "delayed"  # 24-hour delay
    NONE = "none"


class ClientType(Enum):
    RETAIL = "retail"          # Adelaide B2C
    ENTERPRISE = "enterprise"  # Adelaide white-label
    API = "api"                # B2B API clients


@dataclass
class DataAccessPolicy:
    """
    Mission-aligned data access restrictions.
    
    Philosophy: Retail gets the full product. B2B gets a subset.
    This protects retail users from front-running by institutional players.
    """
    
    # Data type â†’ Access level per client type
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
        # Regime classification: Open to all
        "regime_classification": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
        # Battle Test results: Open to all
        "battle_test": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
        # Monte Carlo results: Open to all
        "monte_carlo": {
            ClientType.RETAIL: AccessLevel.FULL,
            ClientType.ENTERPRISE: AccessLevel.FULL,
            ClientType.API: AccessLevel.FULL,
        },
    }
    
    @classmethod
    def can_access(cls, data_type: str, client_type: ClientType) -> AccessLevel:
        """Check access level for data type and client."""
        return cls.POLICIES.get(data_type, {}).get(client_type, AccessLevel.NONE)
    
    @classmethod
    def filter_response(cls, data: Dict, data_type: str, client_type: ClientType) -> Dict:
        """Filter response based on access level."""
        access = cls.can_access(data_type, client_type)
        
        if access == AccessLevel.NONE:
            return {
                "error": "access_denied",
                "message": "This data type is not available for API clients",
                "reason": "Mission alignment: Retail users get priority access",
                "upgrade_path": "Contact sales for enterprise discussion"
            }
        
        if access == AccessLevel.AGGREGATED:
            return cls._aggregate_data(data, data_type)
        
        if access == AccessLevel.DELAYED:
            return cls._delay_data(data, hours=24)
        
        return data  # FULL access
    
    @classmethod
    def _aggregate_data(cls, data: Dict, data_type: str) -> Dict:
        """Aggregate individual wallet data to prevent targeting."""
        if data_type == "whale_tracking":
            # Return only aggregated metrics, not individual wallets
            wallets = data.get("wallets", [])
            return {
                "aggregated": True,
                "total_wallets": len(wallets),
                "total_holdings_usd": sum(w.get("balance_usd", 0) for w in wallets),
                "net_flow_24h_usd": sum(w.get("net_flow_24h", 0) for w in wallets),
                "individual_data": "REDACTED - Aggregated access only"
            }
        return data
    
    @classmethod
    def _delay_data(cls, data: Dict, hours: int) -> Dict:
        """Add delay notice to data."""
        from datetime import datetime, timedelta
        
        data["access_note"] = f"Data delayed by {hours} hours"
        data["data_timestamp"] = (datetime.now() - timedelta(hours=hours)).isoformat()
        return data
```

---

## 5. Phase 2: API Layer (First Client)

**Timeline:** When first B2B client signs  
**Cost:** $5-50/month  
**Goal:** REST API for external access

### 5.1 FastAPI Application

```python
# src/api/main.py

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from src.api.auth import verify_api_key, get_tenant
from src.api.middleware.rate_limit import RateLimitMiddleware
from src.api.middleware.tier_enforcement import TierEnforcementMiddleware
from src.api.routes import strategies, analytics, adelaide, alerts

app = FastAPI(
    title="diBoaS Analytics API",
    description="Market intelligence and DeFi analytics",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure per tenant in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(strategies.router, prefix="/v1/strategies", tags=["Strategies"])
app.include_router(analytics.router, prefix="/v1/analytics", tags=["Analytics"])
app.include_router(adelaide.router, prefix="/v1/adelaide", tags=["Adelaide"])
app.include_router(alerts.router, prefix="/v1/alerts", tags=["Alerts"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/v1/strategies")
async def list_strategies(tenant = Depends(get_tenant)):
    """List available strategies (public info only)."""
    from src.config import load_strategies
    strategies = load_strategies(tenant.id)
    return {
        "strategies": [
            {"id": s.id, "name": s.name, "risk_level": s.risk_level}
            for s in strategies
        ]
    }
```

### 5.2 Authentication

```python
# src/api/auth.py

from fastapi import Header, HTTPException, Depends
from typing import Optional
from dataclasses import dataclass
import os

@dataclass
class Tenant:
    id: str
    name: str
    tier: str  # free, starter, professional, enterprise

# Simple API key storage (use database in production)
API_KEYS = {
    "diboas-internal": Tenant("diboas", "diBoaS Platform", "enterprise"),
    # Add more as clients sign up
}

async def verify_api_key(x_api_key: str = Header(...)) -> Tenant:
    """Verify API key and return tenant."""
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[x_api_key]

async def get_tenant(tenant: Tenant = Depends(verify_api_key)) -> Tenant:
    """Get current tenant from verified API key."""
    return tenant
```

---

## 6. Phase 3: B2B Platform (Scale)

**Timeline:** 5+ clients  
**Cost:** $100-500/month  
**Goal:** Multi-tenant platform with LLM integration

### 6.1 LLM Integration (Optional)

```python
# src/llm/providers.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os

class LLMProvider(ABC):
    """Abstract LLM provider for content generation."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        pass

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",  # Use Sonnet for cost efficiency
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

class TemplateProvider(LLMProvider):
    """Template-based generation (no LLM cost)."""
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        # Use templates instead of LLM
        return prompt  # Template already contains the content
```

### 6.2 White-Label Configuration

```yaml
# config/tenants/example_client.yaml

tenant_id: "wealth_manager_global"
name: "Global Wealth Advisors"
tier: "professional"

branding:
  identity:
    company_name: "Global Wealth Advisors"
    product_name: "Market Intelligence"
    tagline: "Institutional-Grade Insights"
  
  visual:
    colors:
      primary: "#1E3A5F"  # Navy blue
      secondary: "#C9A962"  # Gold
    typography:
      heading_font: "Playfair Display"
      body_font: "Inter"
  
  footer:
    powered_by_visible: false  # Enterprise feature

voice:
  personality:
    traits: ["authoritative", "trustworthy", "sophisticated"]
    formality: "formal"
  
  vocabulary:
    preferred:
      cryptocurrency: "digital assets"
      DeFi: "decentralized finance protocols"
    avoided: ["moon", "WAGMI", "diamond hands"]
  
  templates:
    greeting: "Dear Valued Client,"
    sign_off: "Best regards,\nThe Market Intelligence Team"

features:
  collectors: ["fred", "yahoo", "defillama"]
  engines: ["battle_test", "monte_carlo"]
  personas: ["professional"]  # Custom persona
  output_formats: ["newsletter_html", "pdf_report"]
  
  refresh_interval: "6h"
  history_months: 36
  monte_carlo_simulations: 5000

limits:
  api_calls_per_month: 100000
  strategies: 50
  triggers: 100
```

---

## 7. Phase 4: Enterprise Features

**Timeline:** When market demands  
**Cost:** $500+/month  
**Goal:** Decentralization readiness, premium features

### 7.1 Decentralization Interfaces

```python
# src/decentralization/interfaces.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class VerifiableResult:
    """Result that can be verified on-chain."""
    data: Dict[str, Any]
    hash: str
    proof: str
    verification_method: str

class DataSource(ABC):
    """Abstract data source - can be centralized or decentralized."""
    
    @abstractmethod
    def fetch(self, query: Dict) -> VerifiableResult:
        pass
    
    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return 'centralized' or 'decentralized'."""
        pass

class ComputationEngine(ABC):
    """Abstract computation - can be trusted or verifiable."""
    
    @abstractmethod
    def compute(self, inputs: Dict) -> VerifiableResult:
        pass
    
    @property
    @abstractmethod
    def computation_type(self) -> str:
        """Return 'trusted' or 'verifiable'."""
        pass

# Phase 1 implementations (centralized)
class CentralizedAPISource(DataSource):
    def source_type(self) -> str:
        return "centralized"

class PythonComputationEngine(ComputationEngine):
    def computation_type(self) -> str:
        return "trusted"

# Phase 4 implementations (decentralized) - FUTURE
# class ChainlinkOracleSource(DataSource):
#     def source_type(self) -> str:
#         return "decentralized"
#
# class ZKComputationEngine(ComputationEngine):
#     def computation_type(self) -> str:
#         return "verifiable"
```

---

## 8. Reference: Existing Code to Preserve

### 8.1 Files to KEEP and WRAP

| File | What It Does | How to Wrap |
|------|--------------|-------------|
| `src/engines/battle_test.py` | Historical backtesting | `@EngineRegistry.register("battle_test")` |
| `src/engines/monte_carlo.py` | Risk simulation | `@EngineRegistry.register("monte_carlo")` |
| `src/engines/monitoring.py` | Protocol health | `@EngineRegistry.register("monitoring")` |
| `src/engines/anomaly.py` | ML anomaly detection | `@EngineRegistry.register("anomaly")` |
| `src/validators/result_validator.py` | CV-01 to CV-07 | `@ValidatorRegistry.register("result_validator")` |
| `src/collectors/file_loader.py` | CSV loading | `@CollectorRegistry.register("csv_file")` |
| `src/reporters/*.py` | Output formatting | `@OutputRegistry.register(...)` |
| `src/domain/*.py` | Data models | KEEP as-is |
| `config/strategies.json` | Strategy definitions | MIGRATE to YAML |

### 8.2 Files to DELETE (Replaced by Registry)

None. All existing code is wrapped, not replaced.

---

## 9. Reference: Manual Execution Results

### 9.1 Location

```
cto_handoff_package/06_results_manual_execution/
â”œâ”€â”€ layer01_collection/        # 20 CSV files (validation baseline)
â”œâ”€â”€ layer02_validation/        # Validation reports
â”œâ”€â”€ layer03_analytics/         # Battle Test, Monte Carlo, Risk results
â”œâ”€â”€ layer04_intelligence/      # Triggers, Alerts, Regime classification
â””â”€â”€ layer05_presentation/      # Adelaide persona outputs
```

### 9.2 Using as Test Fixtures

```python
# tests/fixtures/manual_execution/
# Copy entire 06_results_manual_execution/ directory

# tests/test_adelaide.py

def test_adelaide_ana_structure_matches_manual():
    """Ensure automated Adelaide matches manual execution structure."""
    
    # Load manual reference
    with open("tests/fixtures/manual_execution/layer05_presentation/adelaide_daily_ana_en.md") as f:
        manual_output = f.read()
    
    # Generate new output
    generator = AdelaideGenerator(config={})
    result = generator.generate(
        analytics_data=load_test_analytics_data(),
        persona="ana",
        locale="en",
        output_formats=["newsletter_md"]
    )
    automated_output = result["outputs"]["newsletter_md"]
    
    # Validate structure
    assert "Adelaide Daily" in automated_output
    assert "What's Happening" in automated_output
    assert "Strategy Spotlight" in automated_output
    assert "Looking Ahead" in automated_output
    assert "Adelaide ðŸŒ¸" in automated_output  # Ana's signature
```

### 9.3 Validation Baseline

The manual execution results serve as the "known good" baseline:

| Output | Manual Result | Use As |
|--------|---------------|--------|
| battle_test_results.json | 23KB, 5 scenarios Ã— 10 strategies | Expected output format |
| monte_carlo_results.json | 8KB, 10,000 simulations | Expected output format |
| risk_metrics.json | 4KB, all strategies | Expected output format |
| adelaide_daily_ana_en.md | ~2.6KB | Tone, structure, emoji count reference |
| adelaide_daily_felipe_en.md | ~2.4KB | Technical tone reference (0 emojis) |

---

## 10. Reference: Configuration Schemas

### 10.1 Tenant Configuration

```yaml
# config/tenants/diboas.yaml (Default tenant)

tenant_id: "diboas"
name: "diBoaS Platform"
tier: "enterprise"

features:
  collectors:
    enabled:
      - fred
      - yahoo
      - defillama
      - coingecko
      - etherscan
      - alternative  # Fear & Greed
    refresh_interval: "24h"
  
  engines:
    enabled:
      - battle_test
      - monte_carlo
      - monitoring
      - anomaly
    monte_carlo_simulations: 10000
  
  validators:
    enabled:
      - gate1_schema
      - gate2_analytics
      - gate3_intelligence
      - gate4_content
  
  triggers:
    enabled: true
    categories:
      - protocol_health
      - market_conditions
      - macro_indicators
      - estate_movements
      - whale_movements
      - sentiment
  
  personas:
    enabled:
      - ana
      - maria
      - felipe
  
  output_formats:
    enabled:
      - newsletter_md
      - newsletter_html
      - website_teaser
      - twitter_thread
      - linkedin_post
  
  locales:
    enabled:
      - en
      - pt-br

limits:
  api_calls_per_month: unlimited
  strategies: unlimited
  triggers: unlimited
  history_months: 60
```

### 10.2 Feature Tiers

```yaml
# config/tiers.yaml

tiers:
  free:
    collectors: 3
    refresh_interval: "24h"
    history_months: 12
    engines: 2
    monte_carlo_simulations: 1000
    strategies: 3
    triggers: 10
    personas: 1
    locales: 1
    output_formats: 1
    api_calls_per_month: 1000
    support: "community"
    sla: "95%"
    custom_branding: false
  
  starter:
    collectors: 4
    refresh_interval: "6h"
    history_months: 36
    engines: 3
    monte_carlo_simulations: 5000
    strategies: 10
    triggers: 28
    personas: 3
    locales: 3
    output_formats: 3
    api_calls_per_month: 10000
    support: "email"
    sla: "99%"
    custom_branding: false
  
  professional:
    collectors: "all"
    refresh_interval: "1h"
    history_months: 60
    engines: "all"
    monte_carlo_simulations: 50000
    strategies: 50
    triggers: 100
    custom_triggers: true
    personas: "all"
    custom_personas: true
    locales: "all"
    output_formats: "all"
    api_calls_per_month: 100000
    support: "priority"
    sla: "99.9%"
    custom_branding: true
    custom_domain: true
  
  enterprise:
    collectors: "custom"
    refresh_interval: "15min"
    history_months: 120
    engines: "custom"
    monte_carlo_simulations: 500000
    strategies: "unlimited"
    triggers: "unlimited"
    custom_triggers: true
    personas: "custom"
    custom_personas: true
    locales: "custom"
    output_formats: "custom"
    api_calls_per_month: "unlimited"
    support: "dedicated"
    sla: "99.99%"
    custom_branding: true
    custom_domain: true
    white_label: true
```

---

## Appendix A: Code Templates

### A.1 Registry Pattern Template

```python
# Template for creating new registries

from typing import Dict, Type, TypeVar, Any
from src.registries.base import Registry, RegistryComponent

T = TypeVar('T', bound='NewComponent')

class NewComponent(RegistryComponent):
    """Base class for new component type."""
    
    @property
    def component_name(self) -> str:
        raise NotImplementedError
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.process(data)


class NewComponentRegistry(Registry[NewComponent]):
    """Registry for new components."""
    pass


# Usage
@NewComponentRegistry.register("implementation_name")
class SpecificImplementation(NewComponent):
    
    @property
    def component_name(self) -> str:
        return "implementation_name"
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation logic
        return {"result": "processed"}
```

### A.2 Test Template

```python
# Template for testing registry components

import pytest
from src.registries.new_component_registry import NewComponentRegistry

class TestNewComponent:
    
    def setup_method(self):
        self.registry = NewComponentRegistry._get_instance()
    
    def test_implementation_registered(self):
        assert "implementation_name" in self.registry.list_available()
    
    def test_implementation_executes(self):
        component = self.registry.get("implementation_name", {})
        result = component.execute({"input": "test"})
        assert "result" in result
    
    def test_implementation_matches_manual_execution(self):
        """Compare against manual execution baseline."""
        component = self.registry.get("implementation_name", {})
        result = component.execute(load_test_input())
        
        with open("tests/fixtures/manual_execution/expected_output.json") as f:
            expected = json.load(f)
        
        assert_structure_matches(result, expected)
```

---

## Summary: Implementation Checklist

### Phase 1 Deliverables (Weeks 1-4)

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
- [ ] Twitter thread formatter
- [ ] LinkedIn post formatter
- [ ] Website teaser formatter
- [ ] Data Access Policy
- [ ] Tenant configuration (diboas.yaml)
- [ ] GitHub Actions workflows
- [ ] Tests with manual execution fixtures

### Phase 2 Deliverables (First Client)

- [ ] FastAPI application
- [ ] API key authentication
- [ ] Rate limiting middleware
- [ ] Tier enforcement middleware
- [ ] API routes (strategies, analytics, adelaide, alerts)
- [ ] Second tenant configuration

### Phase 3 Deliverables (Scale)

- [ ] LLM integration (optional)
- [ ] White-label engine
- [ ] Admin UI (basic)
- [ ] Usage tracking

### Phase 4 Deliverables (Enterprise)

- [ ] Decentralization interfaces
- [ ] ML/Self-learning modules
- [ ] Premium data source integrations

---

**Document End**

*This document was prepared by CTO Board for The Coder implementation.*
*Reference: Innovation Board Session 003, CTO Board Session 015*
