# System Architecture

A comprehensive overview of the diBoaS Analytics system architecture.

## Table of Contents

1. [High-Level Overview](#high-level-overview)
2. [Component Diagram](#component-diagram)
3. [Data Flow](#data-flow)
4. [Directory Structure](#directory-structure)
5. [Core Components](#core-components)
6. [12 Principles Mapping](#12-principles-mapping)
7. [Event Flow](#event-flow)
8. [Error Handling Strategy](#error-handling-strategy)

---

## High-Level Overview

diBoaS Analytics is a CLI-based financial analytics platform that:

1. **Collects** historical and real-time DeFi protocol data
2. **Analyzes** 10 investment strategies through backtesting and simulation
3. **Validates** results through 4-gate validation pipeline
4. **Generates** consumer-facing newsletters (Adelaide) with compliance checks
5. **Monitors** system health and protocol anomalies

### Technology Stack

- **Language**: Python 3.9+
- **CLI Framework**: argparse
- **Testing**: pytest
- **Data Processing**: pandas, numpy
- **Logging**: Python logging with correlation IDs
- **Alerting**: Slack webhooks (zero budget)

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLI Entry (main.py)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   collect   │  │ battle-test │  │ monte-carlo │  │   health    │  ...   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Command Handlers (src/commands/)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ collect_cmd │  │battle_test_ │  │monte_carlo_ │  │ health_cmd  │  ...   │
│  │             │  │    cmd      │  │    cmd      │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Collectors    │ │     Engines     │ │   Validators    │ │     Utils       │
│ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │
│ │ FileLoader  │ │ │ │ BattleTest  │ │ │ │   Gate 1    │ │ │ │  Health     │ │
│ │ APIClients  │ │ │ │ MonteCarlo  │ │ │ │   Gate 2    │ │ │ │  Metrics    │ │
│ │ RateLimiter │ │ │ │ Anomaly     │ │ │ │   Gate 3    │ │ │ │  Alerting   │ │
│ └─────────────┘ │ │ └─────────────┘ │ │ │   Gate 4    │ │ │ │  Events     │ │
└─────────────────┘ └─────────────────┘ │ └─────────────┘ │ │ └─────────────┘ │
                                        └─────────────────┘ └─────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Data Layer                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  data/*.csv │  │  outputs/*  │  │ config/*.py │  │ metrics.json│        │
│  │  (bundled)  │  │ (generated) │  │   (config)  │  │  (state)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Full Pipeline Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Collect    │────▶│   Gate 1     │────▶│   Analyze    │────▶│   Gate 2     │
│   Data       │     │  (Schema)    │     │  (Engines)   │     │ (Integrity)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
       ┌───────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Triggers   │────▶│   Gate 3     │────▶│   Adelaide   │────▶│   Gate 4     │
│  (Evaluate)  │     │  (Triggers)  │     │ (Generate)   │     │    (CLO)     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
                                                              ┌──────────────┐
                                                              │   Deliver    │
                                                              │  (52 outputs)│
                                                              └──────────────┘
```

### Strategy Analysis Flow

```
strategies.json ───▶ BattleTestEngine ───▶ Results
      │                     │                 │
      │                     ▼                 │
      │              Historical Data          │
      │              (crypto_prices,          │
      │               protocol_yields,        │
      │               etc.)                   │
      │                     │                 │
      │                     ▼                 │
      └──────────▶ Strategy Weights ──────────┘
                   (protocol allocations)
```

---

## Directory Structure

```
diboas-analytics/
├── main.py                     # CLI entry point
│
├── config/                     # Configuration (source of truth)
│   ├── strategies.json         # 10 strategy definitions (NEVER hardcode!)
│   ├── protocols.py            # 6 DeFi protocol definitions
│   ├── thresholds.py           # Alert thresholds
│   └── dream_mode.py           # Consumer path mappings
│
├── src/                        # Source code
│   ├── commands/               # CLI command handlers
│   │   ├── collect_cmd.py
│   │   ├── battle_test_cmd.py
│   │   ├── monte_carlo_cmd.py
│   │   ├── health_cmd.py
│   │   └── ...
│   │
│   ├── collectors/             # Data collection
│   │   ├── file_loader.py      # Bundled CSV loader
│   │   ├── defillama_collector.py
│   │   └── ...
│   │
│   ├── engines/                # Core computation
│   │   ├── battle_test.py      # Historical backtesting
│   │   ├── monte_carlo.py      # Risk simulation
│   │   └── ...
│   │
│   ├── validators/             # 4-gate validation
│   │   ├── gate1/              # Schema validation
│   │   ├── gate2/              # Analytics integrity
│   │   ├── gate3/              # Trigger validation
│   │   └── clo/                # Gate 4 - CLO compliance
│   │
│   ├── triggers/               # Intelligence triggers
│   │   ├── intelligence_trigger_evaluator.py
│   │   └── protocol/           # Protocol-specific triggers
│   │
│   ├── crisis/                 # Crisis detection
│   │   ├── crisis_level_classifier.py
│   │   └── crisis_router.py
│   │
│   ├── adelaide/               # Newsletter generation
│   │   └── adelaide_edition_tracker.py
│   │
│   └── utils/                  # Shared utilities
│       ├── errors/             # Error handling (types, recovery)
│       ├── validation/         # Input validation
│       ├── security/           # Security utilities
│       ├── circuit_breaker.py  # Fault tolerance
│       ├── correlation.py      # Request tracing
│       ├── events.py           # Event bus
│       ├── health.py           # Health checks
│       ├── metrics.py          # Metrics collection
│       └── alerting.py         # Slack alerting
│
├── data/                       # Bundled historical data
│   ├── crypto_prices.csv       # SOL, ETH, BTC prices
│   ├── protocol_yields.csv     # APY data
│   └── ...
│
├── outputs/                    # Generated results (git-ignored)
│   ├── battle_test/
│   ├── monte_carlo/
│   ├── adelaide/
│   ├── metrics/
│   └── verification/
│
├── tests/                      # Test suite
│   ├── test_battle_test.py
│   ├── collectors/
│   ├── validators/
│   ├── triggers/
│   ├── utils/
│   └── integration/
│
└── docs/                       # Documentation
    ├── README.md               # Documentation index
    ├── DEVELOPER_GUIDE.md
    ├── ARCHITECTURE.md         # This file
    ├── CLI_REFERENCE.md
    └── MONITORING_GUIDE.md
```

---

## Core Components

### Collectors

**Purpose:** Load data from various sources (bundled files, APIs).

| Collector | Source | Rate Limit |
|-----------|--------|------------|
| FileLoader | data/*.csv | N/A |
| DefiLlamaCollector | DeFiLlama API | 60 req/min |
| CoinGeckoCollector | CoinGecko API | 30 req/min |

**Key Features:**
- Circuit breaker integration for API failures
- Event emission on data load
- Fallback to bundled data

### Engines

**Purpose:** Core analytical computations.

| Engine | Purpose | Output |
|--------|---------|--------|
| BattleTestEngine | Historical backtesting | Strategy performance metrics |
| MonteCarloEngine | Risk simulation | VaR, CVaR, probability distributions |
| AnomalyDetector | Outlier detection | Anomaly scores, alerts |

### Validators

**Purpose:** Ensure data and output quality through 4-gate pipeline.

| Gate | Stage | Validates |
|------|-------|-----------|
| Gate 1 | Pre-analysis | Data schema, required fields |
| Gate 2 | Post-analysis | Analytics integrity, value ranges |
| Gate 3 | Pre-output | Trigger logic, fire conditions |
| Gate 4 | Pre-publish | CLO compliance, disclaimers, AI disclosure |

### Triggers

**Purpose:** Detect conditions requiring attention or action.

| Category | Examples |
|----------|----------|
| Protocol | Stablecoin depeg, yield anomaly |
| Market | Volatility spike, correlation breakdown |
| Portfolio | Drawdown threshold, rebalance needed |

### Crisis Module

**Purpose:** Classify and route crisis-level events.

| Level | Description | Routing |
|-------|-------------|---------|
| 0 | Normal | Auto-deliver |
| 1-2 | Informational | Auto-deliver with flag |
| 3 | Warning | Queue for review |
| 4-5 | Critical | Immediate escalation |

---

## 12 Principles Mapping

| Principle | Implementation Location |
|-----------|------------------------|
| 1. Domain-Driven Design | `config/strategies.json`, `config/protocols.py` |
| 2. Event-Driven | `src/utils/events.py` - pub/sub event bus |
| 3. Service Abstraction | Abstract collector/validator interfaces |
| 4. DRY | Shared utilities in `src/utils/` |
| 5. Semantic Naming | Clear function/class names throughout |
| 6. File Organization | <250 lines per file, modular structure |
| 7. Error Handling | `src/utils/errors/` - typed exceptions, recovery |
| 8. Security | `src/utils/security/` - input validation, masking |
| 9. Performance | `src/utils/concurrency.py` - caching, rate limiting |
| 10. KPIs | `src/utils/metrics.py` - execution tracking |
| 11. Audit | `src/utils/audit.py` - audit trails |
| 12. Monitoring | `src/utils/health.py`, `alerting.py`, `correlation.py` |

---

## Event Flow

### Event Bus Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Event Bus                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Subscriptions                        │   │
│  │  data.loaded ──────▶ [MetricsCollector, Logger]        │   │
│  │  trigger.fired ────▶ [AlertingService, AuditTrail]     │   │
│  │  crisis.detected ──▶ [AlertingService, CrisisRouter]   │   │
│  │  validation.passed ▶ [MetricsCollector]                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
        ▲                    ▲                    ▲
        │                    │                    │
   Publishers           Publishers           Publishers
   (Collectors)         (Triggers)          (Validators)
```

### Event Types

| Event Name | Payload | Emitted By |
|------------|---------|------------|
| `data.loaded` | source, rows, columns | FileLoader |
| `battle_test.completed` | strategies_tested, duration | BattleTestEngine |
| `trigger.fired` | trigger_id, priority, message | TriggerEvaluator |
| `trigger.evaluated` | trigger_id, fired (bool) | TriggerEvaluator |
| `crisis.detected` | level, trigger_id, message | CrisisClassifier |
| `validation.passed` | gate, items_validated | Validators |
| `validation.failed` | gate, error_count, issues | Validators |

---

## Error Handling Strategy

### Exception Hierarchy

```
DiBoaSError (base)
├── DataError
│   ├── DataNotFoundError
│   ├── DataSchemaError
│   └── DataFreshnessError
├── NetworkError
│   ├── APITimeoutError
│   └── RateLimitError
├── ValidationError
│   ├── SchemaValidationError
│   └── IntegrityValidationError
├── ConfigurationError
└── ProcessingError
```

### Recovery Strategies

| Error Type | Strategy | Fallback |
|------------|----------|----------|
| DataNotFoundError | Load from bundled data | Empty DataFrame |
| APITimeoutError | Retry with backoff | Circuit breaker open |
| RateLimitError | Wait and retry | Use cached data |
| ValidationError | Log and continue | Skip item |

### Circuit Breaker States

```
CLOSED ──(failures > threshold)──▶ OPEN
   ▲                                  │
   │                                  │
   └──(success)──◀── HALF_OPEN ◀──(timeout)──┘
```

---

## Security Considerations

### Input Validation

- All CLI arguments validated before processing
- File paths checked for traversal attacks
- Strategy IDs must be 1-10
- Simulation counts bounded (100-100,000)

### Log Masking

Sensitive data automatically masked in logs:
- API keys
- Webhook URLs
- Personal identifiers

### Output Sanitization

- Adelaide content validated for prohibited terms
- AI disclosure required (California SB 942)
- Jurisdiction-specific disclaimers enforced

---

## Performance Characteristics

### Typical Execution Times

| Operation | Duration | Notes |
|-----------|----------|-------|
| Data load (bundled) | <1s | FileLoader with caching |
| Battle test (10 strategies) | 5-15s | Depends on data range |
| Monte Carlo (5000 sims) | 10-30s | Parallelizable |
| Full pipeline | 30-60s | With all validations |

### Resource Usage

- Memory: ~500MB typical, ~2GB peak (Monte Carlo)
- CPU: Benefits from multi-core for simulations
- Disk: ~100MB bundled data, ~50MB outputs

---

## Deployment Considerations

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SLACK_WEBHOOK_URL` | Alerting | None |
| `ALERT_ENABLED` | Enable/disable alerts | true |
| `LOG_LEVEL` | Logging verbosity | INFO |
| `PYTHONPATH` | Module resolution | . |

### Health Monitoring

```bash
# Check system health
python main.py health

# With connectivity tests
python main.py health --connectivity

# JSON output for scripts
python main.py health --json
```

---

*Last updated: February 2026*
