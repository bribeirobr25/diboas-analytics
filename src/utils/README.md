# Utils Module Structure

This module provides shared utilities for the diBoaS Analytics codebase,
implementing Principles 7, 8, 10, 11, and 12 from the coding standards.

## Module Organization

### Facade Pattern for Backwards Compatibility

Some submodules use a facade pattern for backwards compatibility:

- `src/utils/errors.py` - Facade re-exporting from `errors/`
- `src/utils/errors/` - Actual implementation (types, recovery, handling)

Both import styles work:
```python
# Facade style (recommended for most uses)
from src.utils.errors import DiBoaSError, NetworkError, RecoveryStrategy

# Direct module access (for specific needs)
from src.utils.errors.types import NetworkError
from src.utils.errors.recovery import get_recovery_strategy
```

## Module Descriptions

### Core Utilities

| Module | Purpose | Principle |
|--------|---------|-----------|
| `serialization.py` | JSON-safe serialization (`to_dict_safe`, `Serializable`) | DRY |
| `validation/` | CLI and data validation helpers | 6 |
| `security/` | Input validation, log masking | 8 |
| `file_io.py` | Atomic file operations | 7 |
| `audit.py` | Audit trail tracking | 11 |

### Error Handling (Principle 7)

| Module | Purpose |
|--------|---------|
| `errors/types.py` | Custom exception hierarchy |
| `errors/recovery.py` | Recovery strategies and suggestions |
| `errors/handling.py` | Error handling decorators |
| `retry.py` | Retry decorators with backoff |
| `circuit_breaker.py` | Circuit breaker pattern for fault tolerance |

### Observability (Principle 12)

| Module | Purpose |
|--------|---------|
| `correlation.py` | Correlation ID support for request tracing |
| `health.py` | Health check utilities for monitoring |
| `metrics.py` | Execution metrics collection (planned) |
| `alerting.py` | Slack/webhook alerting (planned) |

### Event-Driven Architecture (Principles 10, 11)

| Module | Purpose |
|--------|---------|
| `events.py` | Event bus for pub/sub communication |

### Concurrency & Performance (Principle 8)

| Module | Purpose |
|--------|---------|
| `concurrency.py` | Thread pools, caching, rate limiting |

## Usage Examples

### Circuit Breaker
```python
from src.utils import get_circuit_breaker

breaker = get_circuit_breaker("external_api")
with breaker:
    response = make_api_call()
```

### Correlation IDs
```python
from src.utils import correlation_context, get_correlated_logger

logger = get_correlated_logger(__name__)

with correlation_context("operation_name"):
    logger.info("Processing started")  # Includes correlation ID
    process_data()
```

### Events
```python
from src.utils import subscribe, publish, EventNames

@subscribe(EventNames.DATA_LOADED)
def on_data_loaded(event):
    print(f"Data loaded: {event.data['rows']} rows")

# Elsewhere
publish(EventNames.DATA_LOADED, {"source": "prices.csv", "rows": 1000})
```

### Health Checks
```python
from src.utils import get_system_health

health = get_system_health(include_connectivity=True)
print(f"System status: {health['status']}")
```

### Caching
```python
from src.utils import timed_lru_cache

@timed_lru_cache(maxsize=128, ttl_seconds=300)
def expensive_computation(data):
    return process(data)
```

## Adding New Utilities

1. Create module in appropriate location
2. Add exports to `__init__.py` if commonly used
3. Update this README
4. Add tests in `tests/utils/`
5. Reference the applicable 12 Principles
