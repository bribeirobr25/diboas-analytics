# diBoaS Analytics Documentation

Welcome to the diBoaS Analytics documentation. This index provides navigation to all technical documentation.

## Quick Start

| Guide | Purpose |
|-------|---------|
| [Getting Started](../README.md) | Project overview and setup instructions |
| [Developer Guide](DEVELOPER_GUIDE.md) | Comprehensive guide for new developers |
| [CLI Reference](CLI_REFERENCE.md) | Complete command reference |

## Architecture & Design

| Document | Description |
|----------|-------------|
| [System Architecture](ARCHITECTURE.md) | System design, components, data flow |
| [Coding Standards (12 Principles)](coding-standards.md) | Code quality principles |
| [v3 Technical Deep Dive](diboas_analytics_v3_technical_deep_dive.md) | Detailed technical specifications |

## Operations

| Guide | Purpose |
|-------|---------|
| [Monitoring Guide](MONITORING_GUIDE.md) | Health checks, metrics, alerting |
| [CLI Reference](CLI_REFERENCE.md) | All CLI commands and options |

## Technical Specifications

| Document | Description |
|----------|-------------|
| [12 Principles](coding-standards.md) | Comprehensive coding standards |
| [Utils Module](../src/utils/README.md) | Utilities documentation |

## Planning & Roadmap

| Document | Description |
|----------|-------------|
| [v4 Index](../v4/00_INDEX.md) | v4 planning documentation |

## Historical Documentation (Archive)

Historical documentation is preserved in the archive directory:

- [CTO Handoff Package](archive/cto_handoff_package/) - Implementation documentation
- [Macro Mine OS](archive/macro_mine/) - Operating system documentation

---

## Key Concepts

### 10 Investment Strategies

Strategies 1-10 with varying risk profiles:
- **Safety** (1, 3, 5, 7, 9): 0% crypto exposure, stable yield only
- **Balance** (2, 4, 6): 30-40% crypto exposure
- **Growth** (8, 10): 70-85% crypto exposure

### 6 DeFi Protocols

| Protocol | Type | Strategies |
|----------|------|------------|
| Sky (sUSDS) | Stablecoin yield | 1-9 |
| Aave V3 | Lending | 1-9 |
| Compound V3 | Lending | 1-9 |
| Sanctum | LST yield | 2, 4, 6, 8, 10 |
| Jito | MEV yield | 10 only |
| Jupiter JLP | Perps LP | 4, 6, 8, 10 |

### Dream Mode Paths

Consumer-facing simplification:
- **Safety Path**: Strategies 1, 3, 5, 7, 9
- **Balance Path**: Strategies 2, 4, 6
- **Growth Path**: Strategies 8, 10

### Validation Gates

| Gate | Purpose |
|------|---------|
| Gate 1 | Data schema validation |
| Gate 2 | Analytics integrity |
| Gate 3 | Trigger validation |
| Gate 4 | CLO compliance |

---

## Contributing

1. Read the [Developer Guide](DEVELOPER_GUIDE.md)
2. Follow the [12 Principles](coding-standards.md)
3. Run tests before submitting: `pytest tests/ -v`
4. All 52 Adelaide outputs must pass verification

---

*Last updated: February 2026*
