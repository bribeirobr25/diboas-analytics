# CLI Reference

Complete reference for all diBoaS Analytics CLI commands.

## Usage

```bash
python main.py <command> [options]
```

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable verbose output (DEBUG logging) |
| `-h, --help` | Show help message |

---

## Data Commands

### collect

Load data from APIs or bundled files.

```bash
python main.py collect [--offline] [--source SOURCE] [--output DIR]
```

| Option | Description |
|--------|-------------|
| `--offline` | Use bundled data only (no API calls) |
| `--source` | Data source: `fred`, `yahoo_live`, `defillama_live`, `coingecko`, `alternative`, `all` |
| `--output` | Output directory (default: `data/`) |
| `--start-date` | Historical start date (YYYY-MM-DD, default: 2022-05-01) |
| `--append` | Append to existing files instead of overwriting |

**Examples:**
```bash
python main.py collect --offline                    # Load bundled data
python main.py collect --source defillama_live      # Fetch fresh DeFiLlama data
```

---

## Analysis Commands

### battle-test

Run historical backtesting (Battle Test).

```bash
python main.py battle-test [--strategy N] [--scenario SCENARIO]
```

| Option | Description |
|--------|-------------|
| `--strategy` | Strategy ID (1-10), or all if not specified |
| `--scenario` | Test scenario: `A` (Felipe), `B` (Ana), `C` (per-strategy) |
| `--start-date` | Custom start date (YYYY-MM-DD) |
| `--end-date` | Custom end date (YYYY-MM-DD) |

**Examples:**
```bash
python main.py battle-test                  # All strategies, scenario A
python main.py battle-test --strategy 1     # Just Strategy 1 (Safe Harbor)
python main.py battle-test --scenario B     # Ana scenario ($2,000 initial)
```

### monte-carlo

Run Monte Carlo risk simulation.

```bash
python main.py monte-carlo [--strategy N] [--simulations N]
```

| Option | Description |
|--------|-------------|
| `--strategy` | Strategy ID (1-10), or all if not specified |
| `--simulations` | Number of simulations (default: 5000) |
| `--seed` | Random seed for reproducibility (default: 42) |

**Examples:**
```bash
python main.py monte-carlo                    # 5,000 simulations, all strategies
python main.py monte-carlo --simulations 10000  # 10,000 simulations
```

### monitor

Check protocol health status.

```bash
python main.py monitor [--protocol NAME] [--alerts-only]
```

| Option | Description |
|--------|-------------|
| `--protocol` | Specific protocol to check |
| `--alerts-only` | Show only active alerts |

### anomaly

Run anomaly detection models.

```bash
python main.py anomaly [--model MODEL] [--protocol NAME]
```

| Option | Description |
|--------|-------------|
| `--model` | Detection model: `zscore`, `isolation`, `correlation` |
| `--protocol` | Specific protocol to analyze |

---

## Output Commands

### dream-mode-export

Generate Dream Mode data for frontend.

```bash
python main.py dream-mode-export [--output FILE]
```

| Option | Description |
|--------|-------------|
| `--output` | Output file path (default: `outputs/dream_mode_data.json`) |

### adelaide

Generate personalized Adelaide newsletters.

```bash
python main.py adelaide [--persona NAME] [--locale CODE] [--format FORMATS]
```

| Option | Description |
|--------|-------------|
| `--persona` | Persona: `ana`, `maria`, `felipe`, `all` (default: `ana`) |
| `--locale` | Locale: `en`, `pt-br` (default: `en`) |
| `--format` | Output formats (comma-separated): `newsletter_md`, `twitter_thread`, `linkedin_post`, `website_teaser`, `substack` |
| `--output` | Output directory (default: `outputs/`) |
| `--data` | Path to analytics data JSON |
| `--tenant` | Tenant ID (default: `diboas`) |

**Examples:**
```bash
python main.py adelaide --persona ana --locale en
python main.py adelaide --persona all --format newsletter_md,twitter_thread
```

---

## Validation Commands

### validate-gate1

Run Gate 1 schema validation on data files.

```bash
python main.py validate-gate1 [--file NAME] [--data-dir DIR]
```

| Option | Description |
|--------|-------------|
| `--file` | Specific file to validate |
| `--data-dir` | Data directory (default: `data/`) |
| `--edition` | Adelaide edition type: `pulse`, `weekly` |
| `--strict` | Fail on warnings |
| `--output` | Output report file |

### validate-gate2

Run Gate 2 analytics validation.

```bash
python main.py validate-gate2 [--battle-test FILE] [--monte-carlo FILE]
```

| Option | Description |
|--------|-------------|
| `--battle-test` | Battle Test results file |
| `--monte-carlo` | Monte Carlo results file |
| `--risk-metrics` | Risk metrics file |
| `--output` | Output report file |

### validate-clo

Run CLO Gate 4 compliance validation.

```bash
python main.py validate-clo [--content TEXT] [--jurisdiction CODE]
```

| Option | Description |
|--------|-------------|
| `--content` | Content to validate (or path to file) |
| `--jurisdiction` | Target jurisdiction: `US`, `EU`, `BR`, `UK` |
| `--crisis-level` | Crisis level 0-5 (default: 0) |

---

## Trigger Commands

### triggers

Evaluate intelligence triggers.

```bash
python main.py triggers [--data FILE] [--output FILE]
```

| Option | Description |
|--------|-------------|
| `--data` | Path to market data JSON |
| `--output` | Output file path (default: `outputs/trigger_results.json`) |
| `--dry-run` | Evaluate without recording cooldowns |

---

## System Commands

### health

Check system health status.

```bash
python main.py health [--connectivity] [--json]
```

| Option | Description |
|--------|-------------|
| `--connectivity` | Include network connectivity checks (slower) |
| `--json` | Output in JSON format |
| `--verbose` | Include detailed check information |

**Exit Codes:**
- `0`: Healthy
- `1`: Degraded
- `2`: Unhealthy

**Example Output:**
```
✅ System Health: HEALTHY
   Timestamp: 2026-02-05T10:00:00
--------------------------------------------------
✅ data_freshness
   All data files fresh
✅ disk_space
   Adequate disk space available
✅ circuit_breakers
   No circuit breakers registered

Summary: 3/3 checks healthy
```

### all

Run full pipeline (collect, battle-test, monte-carlo, dream-mode-export).

```bash
python main.py all [--offline]
```

| Option | Description |
|--------|-------------|
| `--offline` | Use bundled data only |

---

## Administration Commands

### crisis-queue

Manage crisis approval queue.

```bash
python main.py crisis-queue list [--queue NAME]
python main.py crisis-queue approve REQUEST_ID --approver EMAIL
python main.py crisis-queue reject REQUEST_ID --approver EMAIL [--reason TEXT]
```

### registry

List available registry implementations.

```bash
python main.py registry [--type TYPE]
```

| Option | Description |
|--------|-------------|
| `--type` | Registry type: `collectors`, `validators`, `engines`, `triggers`, `personas`, `outputs`, `all` |

### tenants

Manage tenant configurations.

```bash
python main.py tenants list
python main.py tenants validate --tenant TENANT_ID
python main.py tenants show --tenant TENANT_ID
python main.py tenants policy [--tenant TENANT_ID]
```

---

## Common Workflows

### Full Pipeline Run

```bash
# Offline (using bundled data)
python main.py all --offline

# With live data collection
python main.py all
```

### Quick Health Check

```bash
python main.py health --json | jq '.status'
```

### Generate Adelaide for All Personas

```bash
python main.py adelaide --persona all --locale en
python main.py adelaide --persona all --locale pt-br
```

### Validate New Content

```bash
python main.py validate-clo --content "Your newsletter content here" --jurisdiction US
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error or degraded state |
| 2 | Unhealthy state (health command) |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SLACK_WEBHOOK_URL` | Slack webhook URL for alerting |
| `ALERT_ENABLED` | Set to "false" to disable alerts |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) |

---

*Last updated: February 2026*
