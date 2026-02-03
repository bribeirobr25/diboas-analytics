# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

diBoaS Analytics is a Python CLI application for analyzing DeFi investment strategies. It performs historical backtesting (Battle Test), Monte Carlo risk simulations, protocol monitoring, anomaly detection, and generates consumer-facing data for the diBoaS fintech platform.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
pytest tests/test_battle_test.py -v  # Single test file

# Main CLI commands
python main.py collect --offline          # Load bundled historical data
python main.py battle-test                # Run historical backtesting (all strategies)
python main.py battle-test --strategy 1   # Test single strategy
python main.py monte-carlo --simulations 5000  # Monte Carlo simulation
python main.py monitor                    # Check protocol health
python main.py anomaly                    # Run anomaly detection
python main.py dream-mode-export          # Generate consumer data for frontend
python main.py all --offline              # Run full pipeline

# Verbose logging
python main.py battle-test -v
```

## Architecture

```
main.py                    # CLI entry point (argparse-based)
config/
  strategies.json          # 10 official strategies - NEVER HARDCODE, always load from here
  protocols.py             # 6 DeFi protocol definitions
  thresholds.py            # Alert thresholds
  dream_mode.py            # Strategy-to-consumer-path mappings
src/
  collectors/              # Data loading (FileLoader for bundled CSVs)
  engines/                 # Core computation (battle_test.py, monte_carlo.py, etc.)
  validators/              # CV-01 through CV-07 validation rules
  models/                  # ML anomaly detectors (zscore, isolation_forest)
  reporters/               # Output generators (CSV, JSON, Markdown)
  commands/                # CLI command handlers
  utils/                   # Logging, validation, audit trails
data/                      # Bundled historical CSVs (May 2022 - Dec 2025)
outputs/                   # Generated results (git-ignored)
```

## Key Concepts

**10 Strategies** with different risk profiles:
- Strategies 1, 3, 5, 7, 9: 0% crypto exposure (stable yield only)
- Strategies 2, 4, 6: 30-40% crypto (balanced)
- Strategies 8, 10: 70-85% crypto (high risk)

**6 Protocols**: Sky, Aave V3, Compound V3 (stablecoins), Sanctum, Jito, Jupiter JLP (crypto exposure)

**Dream Mode Paths**: Consumer-facing simplification - Safety (strategies 1,3,5,7,9), Balance (2,4,6), Growth (8,10)

**Validation Rules** (CV-01 to CV-07):
- Portfolio value never negative
- Drawdown 0-100%
- Stable strategies (0% crypto) must have 0% drawdown
- Return calculations accurate

## Critical Rules

1. **Never hardcode strategies** - Always load from `config/strategies.json`
2. **JLP basket weights**: 45% SOL, 27% ETH, 27% BTC (not 50/25/25)
3. **Jito only in Strategy 10** (Full Throttle)
4. **No Huma** in any strategy (removed in v2.0)

## Proxy Calculations

When historical data is unavailable, use formulas in `src/utils/proxies.py`:
- Sanctum: `Lido_ETH_APY × 2.0 + 0.5%`
- Jito: `Lido_ETH_APY × 2.0 + 1.0%`
- JLP: Fixed 25% APY (before Jan 2024)

## Related Documentation

- `CLAUDE_CODE_HANDOFF.md` - Complete technical specification with algorithms
- `CLAUDE_CODE_CONTEXT.md` - Business context and governance decisions
