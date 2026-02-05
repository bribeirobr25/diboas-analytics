# Monitoring Guide

A comprehensive guide to monitoring, alerting, and observability for diBoaS Analytics.

## Table of Contents

1. [Overview](#overview)
2. [Health Checks](#health-checks)
3. [Metrics Collection](#metrics-collection)
4. [Alerting](#alerting)
5. [Correlation IDs](#correlation-ids)
6. [Circuit Breakers](#circuit-breakers)
7. [Event Monitoring](#event-monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Overview

diBoaS Analytics implements Principle 12 (Monitoring & Observability) through:

- **Health Checks**: System status and component health
- **Metrics**: Execution tracking and performance data
- **Alerting**: Slack notifications for critical events
- **Correlation IDs**: Request tracing across components
- **Circuit Breakers**: Fault tolerance monitoring
- **Event Bus**: System-wide event visibility

All monitoring features are designed for zero-budget operation (no paid monitoring services required).

---

## Health Checks

### CLI Usage

```bash
# Basic health check
python main.py health

# Include connectivity tests (API endpoints)
python main.py health --connectivity

# JSON output for scripts/automation
python main.py health --json

# Verbose output with details
python main.py health --verbose
```

### Health Check Output

```
================================================================================
                         diBoaS Analytics Health Check
================================================================================

Overall Status: HEALTHY

Component Status:
  Data Files.............. HEALTHY
  Configuration........... HEALTHY
  Output Directory........ HEALTHY
  Python Environment...... HEALTHY

Data Freshness:
  crypto_prices.csv....... FRESH (2 days old)
  protocol_yields.csv..... FRESH (2 days old)

Circuit Breakers:
  defillama_api........... CLOSED (0 failures)
  coingecko_api........... CLOSED (0 failures)

================================================================================
```

### Programmatic Usage

```python
from src.utils.health import get_system_health

# Get health status
health = get_system_health(include_connectivity=True)

# Check overall status
if health["status"] != "healthy":
    print(f"System degraded: {health}")

# Check specific components
for component, status in health["components"].items():
    if status["healthy"] is False:
        print(f"Component {component} unhealthy: {status['message']}")
```

### Health Check Components

| Component | Checks | Healthy When |
|-----------|--------|--------------|
| Data Files | Existence, readability | All required files exist |
| Configuration | strategies.json valid | 10 strategies loaded |
| Output Directory | Writable | Can create files |
| Python Environment | Dependencies | Required packages installed |
| Data Freshness | File age | Files < 7 days old |
| Circuit Breakers | State | All circuits CLOSED |
| API Connectivity | Response | 200 OK within timeout |

---

## Metrics Collection

### Automatic Metrics

Every CLI execution automatically collects metrics:

```python
from src.utils.metrics import get_metrics_collector

collector = get_metrics_collector()

# Metrics are automatically recorded for:
# - Command executed
# - Duration (ms)
# - Success/failure
# - Strategies tested
# - Triggers evaluated/fired
# - Validations passed/failed
```

### Metrics Storage

Metrics are stored in `outputs/metrics/execution_metrics.json`:

```json
{
  "runs": [
    {
      "correlation_id": "cli-all-20260205-abc123",
      "command": "all --offline",
      "start_time": "2026-02-05T10:00:00Z",
      "end_time": "2026-02-05T10:00:45Z",
      "duration_ms": 45000,
      "success": true,
      "strategies_tested": 10,
      "triggers_evaluated": 45,
      "triggers_fired": 3,
      "validations_passed": 7,
      "validations_failed": 0,
      "outputs_generated": 52,
      "errors": []
    }
  ]
}
```

### Querying Metrics

```bash
# View last 10 runs
cat outputs/metrics/execution_metrics.json | python -c "
import json, sys
data = json.load(sys.stdin)
for run in data['runs'][-10:]:
    print(f\"{run['start_time']}: {run['command']} - {'OK' if run['success'] else 'FAIL'} ({run['duration_ms']}ms)\")
"

# Calculate average duration
cat outputs/metrics/execution_metrics.json | python -c "
import json, sys
data = json.load(sys.stdin)
durations = [r['duration_ms'] for r in data['runs']]
print(f'Average: {sum(durations)/len(durations):.0f}ms')
"

# Count failures
cat outputs/metrics/execution_metrics.json | python -c "
import json, sys
data = json.load(sys.stdin)
failures = [r for r in data['runs'] if not r['success']]
print(f'Failures: {len(failures)}/{len(data[\"runs\"])} ({len(failures)/len(data[\"runs\"])*100:.1f}%)')
"
```

### Custom Metrics

```python
from src.utils.metrics import get_metrics_collector

collector = get_metrics_collector()

# Start tracking
collector.start_execution("custom-analysis")

# Record custom metrics
collector.record(
    strategies_tested=5,
    simulations_run=1000,
    custom_metric=42
)

# End tracking
collector.end_execution(success=True)
```

---

## Alerting

### Configuration

Set up Slack webhook for alerts:

```bash
# Add to environment or .env file
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: disable alerts
export ALERT_ENABLED="false"
```

### Alert Severity Levels

| Level | Emoji | Use Case |
|-------|-------|----------|
| INFO | ℹ️ | Informational messages |
| WARNING | ⚠️ | Non-critical issues |
| ERROR | ❌ | Failures requiring attention |
| CRITICAL | 🚨 | Immediate action required |

### Programmatic Alerting

```python
from src.utils.alerting import (
    send_alert,
    AlertSeverity,
    alert_crisis_detected,
    alert_circuit_opened,
    alert_validation_failure,
    alert_execution_failed,
)

# Basic alert
send_alert("Processing complete", severity=AlertSeverity.INFO)

# Alert with context
send_alert(
    "High volatility detected",
    severity=AlertSeverity.WARNING,
    context={
        "symbol": "SOL",
        "change_24h": "15.2%",
        "affected_strategies": [8, 10]
    }
)

# Convenience functions
alert_crisis_detected(
    crisis_level=4,
    trigger_id="usdc_depeg_l4",
    message="USDC depeg > 2%",
    affected_strategies=[1, 2, 3, 4, 5, 6, 7, 8, 9]
)

alert_circuit_opened(
    circuit_name="defillama_api",
    failure_count=5,
    last_error="Connection timeout"
)

alert_validation_failure(
    gate="Gate 2",
    error_count=3,
    issues=["Negative portfolio value", "Invalid drawdown"]
)

alert_execution_failed(
    command="battle-test",
    error="Data file not found",
    correlation_id="cli-battle-test-abc123"
)
```

### Alert Triggers

Automatic alerts are sent for:

| Event | Severity | Message |
|-------|----------|---------|
| Crisis Level 4-5 | CRITICAL | Crisis detected with level and trigger |
| Circuit Breaker Open | ERROR | Circuit name and failure count |
| Validation Gate Failure | WARNING | Gate name and error count |
| Command Execution Failure | ERROR | Command and error message |

### Fallback Behavior

When `SLACK_WEBHOOK_URL` is not configured:
- Alerts are logged to the application log
- Log level matches alert severity
- No external notifications sent

---

## Correlation IDs

### Purpose

Correlation IDs trace requests across components:

```
CLI Command ──▶ Collector ──▶ Engine ──▶ Validator ──▶ Output
     │              │            │           │            │
     └──────────────┴────────────┴───────────┴────────────┘
                    All share correlation ID
```

### Automatic Assignment

Every CLI command gets a correlation ID:

```
cli-battle-test-20260205-a1b2c3d4
│   │            │        │
│   │            │        └── Random suffix
│   │            └── Date
│   └── Command name
└── Prefix
```

### Log Output

Logs include correlation ID:

```
2026-02-05 10:00:00 INFO [cli-all-20260205-abc123] Loading crypto_prices.csv
2026-02-05 10:00:01 INFO [cli-all-20260205-abc123] Loaded 1095 rows
2026-02-05 10:00:05 INFO [cli-all-20260205-abc123] Battle test complete
2026-02-05 10:00:10 WARNING [cli-all-20260205-abc123] Trigger fired: usdc_depeg_l2
```

### Programmatic Usage

```python
from src.utils.correlation import (
    correlation_context,
    get_correlated_logger,
    get_correlation_id,
    with_correlation_id,
)

# Get correlated logger
logger = get_correlated_logger(__name__)

# Use context manager
with correlation_context("my_operation"):
    logger.info("Processing started")  # Includes correlation ID
    process_data()
    logger.info("Processing complete")

# Use decorator
@with_correlation_id(prefix="analysis")
def run_analysis():
    logger.info("Running analysis")  # Has correlation ID

# Get current correlation ID
cid = get_correlation_id()
print(f"Current correlation ID: {cid}")
```

### Tracing Requests

To trace a specific request:

```bash
# Find all logs for a correlation ID
grep "cli-all-20260205-abc123" outputs/logs/*.log

# Find errors for a correlation ID
grep "cli-all-20260205-abc123" outputs/logs/*.log | grep -i error
```

---

## Circuit Breakers

### Purpose

Circuit breakers prevent cascading failures:

```
Normal Operation         Failures Detected         Recovery
      │                        │                      │
   CLOSED ──(5 failures)──▶ OPEN ──(30s timeout)──▶ HALF_OPEN
      ▲                        │                      │
      │                        │                      │
      └────────────────────────┴──────(success)───────┘
```

### Named Circuit Breakers

| Name | Protected Resource | Threshold |
|------|-------------------|-----------|
| `defillama_api` | DeFiLlama API | 5 failures |
| `coingecko_api` | CoinGecko API | 5 failures |
| `file_system` | File operations | 3 failures |

### Checking Circuit Health

```python
from src.utils.circuit_breaker import (
    get_circuit_breaker,
    get_all_circuit_health,
)

# Check all circuits
health = get_all_circuit_health()
for name, state in health.items():
    print(f"{name}: {state['state']} ({state['failure_count']} failures)")

# Check specific circuit
breaker = get_circuit_breaker("defillama_api")
print(f"State: {breaker.state}")
print(f"Failures: {breaker.failure_count}")
```

### Circuit Breaker Alerts

When a circuit opens:

```
🚨 [ERROR] Circuit breaker 'defillama_api' opened after 5 failures
  • circuit_name: defillama_api
  • failure_count: 5
  • last_error: Connection timeout
```

### Manual Circuit Reset

```python
from src.utils.circuit_breaker import get_circuit_breaker

breaker = get_circuit_breaker("defillama_api")
breaker.reset()  # Force back to CLOSED state
```

---

## Event Monitoring

### Subscribing to Events

```python
from src.utils.events import subscribe, EventNames

@subscribe(EventNames.DATA_LOADED)
def on_data_loaded(event):
    print(f"Data loaded: {event.data['source']} ({event.data['rows']} rows)")

@subscribe(EventNames.TRIGGER_FIRED)
def on_trigger_fired(event):
    print(f"Trigger fired: {event.data['trigger_id']}")

@subscribe(EventNames.CRISIS_DETECTED)
def on_crisis(event):
    print(f"CRISIS: Level {event.data['level']} - {event.data['message']}")
```

### Event Types

| Event | Data Fields |
|-------|-------------|
| `data.loaded` | source, rows, columns |
| `battle_test.completed` | strategies_tested, duration |
| `trigger.fired` | trigger_id, priority, message |
| `trigger.evaluated` | trigger_id, fired |
| `crisis.detected` | level, trigger_id, message |
| `validation.passed` | gate, items_validated |
| `validation.failed` | gate, error_count, issues |

### Event Logging

All events are logged with correlation IDs:

```python
from src.utils.events import enable_event_logging

# Enable automatic event logging
enable_event_logging()

# Now all events are logged:
# 2026-02-05 10:00:00 INFO [cli-all-abc123] Event data.loaded: {'source': 'crypto_prices.csv', 'rows': 1095}
```

---

## Troubleshooting

### Common Issues

#### No Slack Alerts

```bash
# Check webhook URL is set
echo $SLACK_WEBHOOK_URL

# Test webhook manually
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  $SLACK_WEBHOOK_URL

# Check if alerting is disabled
echo $ALERT_ENABLED  # Should not be "false"
```

#### Missing Correlation IDs in Logs

```python
# Ensure correlated logging is set up
from src.utils.correlation import setup_correlated_logging
setup_correlated_logging()

# Use correlated logger
from src.utils.correlation import get_correlated_logger
logger = get_correlated_logger(__name__)
```

#### Circuit Breaker Stuck Open

```python
from src.utils.circuit_breaker import get_circuit_breaker

# Check circuit state
breaker = get_circuit_breaker("api_name")
print(f"State: {breaker.state}")
print(f"Time until half-open: {breaker.time_until_half_open()}")

# Force reset if needed
breaker.reset()
```

#### Metrics Not Recording

```python
from src.utils.metrics import get_metrics_collector

collector = get_metrics_collector()

# Check if collector is active
print(f"Active: {collector.is_active}")

# Check metrics file location
print(f"Metrics file: {collector.metrics_file}")
```

### Log Locations

| Log Type | Location |
|----------|----------|
| Application logs | `outputs/logs/diboas.log` |
| Error logs | `outputs/logs/errors.log` |
| Metrics | `outputs/metrics/execution_metrics.json` |
| Health reports | `outputs/health/` |

### Debug Mode

Enable verbose logging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with verbose flag
python main.py all --offline -v
```

### Monitoring Checklist

Daily:
- [ ] Check `python main.py health`
- [ ] Review any alerts received
- [ ] Check circuit breaker states

Weekly:
- [ ] Review metrics trends
- [ ] Check data freshness
- [ ] Review error logs

Monthly:
- [ ] Audit correlation ID coverage
- [ ] Review alert thresholds
- [ ] Archive old metrics

---

*Last updated: February 2026*
