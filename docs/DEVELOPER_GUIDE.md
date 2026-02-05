# Developer Guide

A comprehensive guide for developers working on diBoaS Analytics.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Key Concepts](#key-concepts)
4. [Development Workflow](#development-workflow)
5. [Code Patterns](#code-patterns)
6. [Testing Guidelines](#testing-guidelines)
7. [Deployment & Operations](#deployment-operations)

---

## Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd diboas-analytics

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_battle_test.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Basic Usage

```bash
# Load bundled data and run full pipeline
python main.py all --offline

# Run specific analysis
python main.py battle-test --strategy 1
python main.py monte-carlo --simulations 5000
```

---

## Architecture Overview

### Project Structure

```
diboas-analytics/
├── main.py                    # CLI entry point
├── config/
│   ├── strategies.json        # 10 strategy definitions (NEVER hardcode!)
│   ├── protocols.py           # 6 DeFi protocol definitions
│   ├── thresholds.py          # Alert thresholds
│   └── dream_mode.py          # Consumer path mappings
├── src/
│   ├── collectors/            # Data loading (FileLoader, API clients)
│   ├── engines/               # Core computation (battle_test, monte_carlo)
│   ├── validators/            # Gate 1-4 validation rules
│   ├── triggers/              # Intelligence triggers
│   ├── crisis/                # Crisis detection and routing
│   ├── adelaide/              # Newsletter generation
│   ├── commands/              # CLI command handlers
│   └── utils/                 # Shared utilities
├── data/                      # Bundled historical CSVs
├── outputs/                   # Generated results (git-ignored)
├── tests/                     # Test suite
└── docs/                      # Documentation
```

### Component Flow

```
CLI Entry (main.py)
    │
    ├── Data Collection
    │   └── collectors/file_loader.py (bundled) or live collectors
    │
    ├── Validation Gate 1
    │   └── validators/gate1/ (schema validation)
    │
    ├── Analysis Engines
    │   ├── engines/battle_test.py (historical backtesting)
    │   └── engines/monte_carlo.py (risk simulation)
    │
    ├── Validation Gate 2
    │   └── validators/gate2/ (analytics integrity)
    │
    ├── Trigger Evaluation
    │   └── triggers/ (intelligence triggers)
    │
    ├── Validation Gate 3
    │   └── validators/gate3/ (trigger validation)
    │
    ├── Adelaide Generation
    │   └── adelaide/ (personalized newsletters)
    │
    └── Validation Gate 4
        └── validators/clo/ (CLO compliance)
```

---

## Key Concepts

### 10 Investment Strategies

Always load from `config/strategies.json`. NEVER hardcode strategy definitions.

```python
# Good
from config.strategies import load_strategies
strategies = load_strategies()

# Bad - NEVER do this
strategies = {"1": {"name": "Safe Harbor", ...}}
```

**Risk Categories:**
- Strategies 1, 3, 5, 7, 9: 0% crypto exposure
- Strategies 2, 4, 6: 30-40% crypto exposure
- Strategies 8, 10: 70-85% crypto exposure

### 6 DeFi Protocols

| Protocol | Exposure Type | Strategies |
|----------|---------------|------------|
| Sky (sUSDS) | Stablecoin yield | All except 10 |
| Aave V3 | Lending | 1-9 |
| Compound V3 | Lending | 1-9 |
| Sanctum | LST yield | 2, 4, 6, 8, 10 |
| Jito | MEV yield | 10 only |
| Jupiter JLP | Perps LP | 4, 6, 8, 10 |

### JLP Basket Weights

```python
# Correct (per specification)
JLP_WEIGHTS = {
    "SOL": 0.45,  # 45%
    "ETH": 0.27,  # 27%
    "BTC": 0.27,  # 27% - NOT 0.28!
}
```

### Dream Mode Paths

Consumer-facing simplification:
- **Safety**: Strategies 1, 3, 5, 7, 9
- **Balance**: Strategies 2, 4, 6
- **Growth**: Strategies 8, 10

### Validation Gates

| Gate | Purpose | SLA |
|------|---------|-----|
| Gate 1 | Data schema validation | Pre-analysis |
| Gate 2 | Analytics integrity | Post-analysis |
| Gate 3 | Trigger validation | Pre-output |
| Gate 4 | CLO compliance | Pre-publish |

---

## Development Workflow

### 1. Feature Development

1. Create feature branch from `main`
2. Implement feature following 12 Principles
3. Write tests (aim for 80%+ coverage)
4. Run full test suite: `pytest tests/ -v`
5. Run 52 output verification: `python scripts/verify_52_outputs.py`
6. Create PR with description

### 2. Code Style

Follow the [12 Principles](coding-standards.md):

1. **Domain-Driven Design** - Model business concepts explicitly
2. **Event-Driven** - Use events for loose coupling
3. **Service Abstraction** - Interface-based design
4. **DRY** - Don't Repeat Yourself
5. **Semantic Naming** - Clear, intention-revealing names
6. **File Organization** - <250 lines per file
7. **Error Handling** - Graceful degradation with recovery suggestions
8. **Security** - Input validation, log masking
9. **Performance** - Caching, lazy loading
10. **KPIs** - Track business metrics
11. **Audit** - Comprehensive audit trails
12. **Monitoring** - Health checks, correlation IDs

### 3. Commit Messages

```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

---

## Code Patterns

### Circuit Breaker

```python
from src.utils.circuit_breaker import get_circuit_breaker

breaker = get_circuit_breaker("external_api")

with breaker:
    response = external_api.call()
```

### Correlation IDs

```python
from src.utils.correlation import correlation_context, get_correlated_logger

logger = get_correlated_logger(__name__)

with correlation_context("my_operation"):
    logger.info("Processing started")  # Includes correlation ID
    process_data()
```

### Event Emission

```python
from src.utils.events import publish, EventNames

# After data load
publish(EventNames.DATA_LOADED, {
    "source": "crypto_prices.csv",
    "rows": len(df)
})

# After trigger fires
publish(EventNames.TRIGGER_FIRED, {
    "trigger_id": result.trigger_id,
    "priority": result.priority.value
})
```

### Error Handling

```python
from src.utils.errors import (
    DataNotFoundError,
    graceful_degradation,
    get_recovery_strategy
)

@graceful_degradation(fallback_value=pd.DataFrame())
def load_data(source: str) -> pd.DataFrame:
    if not file_exists(source):
        raise DataNotFoundError(
            filepath=source,
            data_type="price data"
        )
    return pd.read_csv(source)
```

### Health Checks

```python
from src.utils.health import get_system_health

health = get_system_health(include_connectivity=True)
if health["status"] != "healthy":
    logger.warning(f"System degraded: {health}")
```

### Metrics Collection

```python
from src.utils.metrics import get_metrics_collector

collector = get_metrics_collector()
collector.start_execution("battle-test")

# ... run analysis ...

collector.record(strategies_tested=10, simulations_run=5000)
collector.end_execution(success=True)
```

---

## Testing Guidelines

### Test Structure

```
tests/
├── test_battle_test.py        # Unit tests for engines
├── test_monte_carlo.py
├── collectors/
│   └── test_file_loader.py
├── validators/
│   └── clo/
│       └── test_disclaimer_validator.py
├── triggers/
│   └── test_stablecoin_depeg.py
├── utils/
│   ├── test_circuit_breaker.py
│   ├── test_correlation.py
│   └── test_events.py
└── integration/
    └── test_full_pipeline.py
```

### Writing Tests

```python
class TestMyFeature:
    """Tests for my feature."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        return {"key": "value"}

    def test_happy_path(self, setup_data):
        """Feature works with valid input."""
        result = my_function(setup_data)
        assert result.success is True

    def test_error_handling(self):
        """Feature handles errors gracefully."""
        with pytest.raises(ValidationError):
            my_function(invalid_data)
```

### Test Coverage Goals

- Unit tests: 80%+
- Integration tests: Key workflows
- All 52 Adelaide outputs must verify

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific module
pytest tests/utils/ -v

# Single test
pytest tests/test_battle_test.py::TestBattleTest::test_strategy_1 -v
```

---

## Deployment & Operations

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SLACK_WEBHOOK_URL` | Slack webhook for alerts | None |
| `ALERT_ENABLED` | Enable/disable alerts | `true` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Health Monitoring

```bash
# Check system health
python main.py health

# Check with connectivity tests
python main.py health --connectivity

# JSON output for scripts
python main.py health --json
```

### Alerting

Alerts are sent via Slack when `SLACK_WEBHOOK_URL` is configured:

- **CRITICAL**: Crisis level 4-5 detected
- **ERROR**: Circuit breaker opened, execution failed
- **WARNING**: Validation failures, degraded state

### Output Verification

After any pipeline run, verify outputs:

```bash
python scripts/verify_52_outputs.py
cat outputs/verification/verification_report.md
```

Expected: 52 Adelaide outputs across all personas and formats.

---

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Stale data:**
```bash
# Check data freshness
python main.py health

# Refresh data
python main.py collect --source all
```

**Test failures:**
```bash
# Reset depeg state between tests (auto-handled by fixtures)
# Ensure AI disclosure in CLO test content
```

### Getting Help

1. Check this guide
2. Review [12 Principles](coding-standards.md)
3. Check existing tests for patterns
4. Review error messages and recovery suggestions

---

## Resources

- [CLI Reference](CLI_REFERENCE.md)
- [System Architecture](ARCHITECTURE.md)
- [12 Principles](coding-standards.md)
- [Monitoring Guide](MONITORING_GUIDE.md)

---

*Last updated: February 2026*
