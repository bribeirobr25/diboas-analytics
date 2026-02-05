# Validation Gates CTO Handoff
## Complete Pipeline Validation Framework

**Document Version:** 2.0  
**Date:** January 24, 2026  
**Prepared by:** Strategy Board (with inputs from Rakia, QR Board, CLO Board)  
**Updated by:** QR Board (Gap Analysis Fixes)  
**For:** CTO Board â€” diboas-analytics Implementation  
**Status:** Ready for Implementation

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | Strategy Board | Initial release |
| 2.0 | 2026-01-24 | QR Board | Added 15 missing CSV schemas (GAP-004), Added weekend/holiday handling for freshness checks (GAP-015) |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Validation Architecture](#2-validation-architecture)
3. [Gate 1: Raw Data Validation](#3-gate-1-raw-data-validation)
4. [Gate 2: Analytics Validation](#4-gate-2-analytics-validation)
5. [Gate 3: Intelligence Validation](#5-gate-3-intelligence-validation)
6. [Gate 4: Presentation Validation](#6-gate-4-presentation-validation)
7. [Gate Orchestration](#7-gate-orchestration)
8. [Failure Handling](#8-failure-handling)
9. [Logging & Audit](#9-logging--audit)
10. [Configuration](#10-configuration)
11. [API Specifications](#11-api-specifications)
12. [Database Schema](#12-database-schema)
13. [Testing Requirements](#13-testing-requirements)

---

## 1. Executive Summary

### 1.1 Purpose

This document specifies the **4 Validation Gates** in the diboas-analytics data pipeline. Each gate validates outputs before passing to the next layer, ensuring data quality, calculation correctness, business rule compliance, and legal adherence.

### 1.2 Why Validation Gates?

| Problem | Solution |
|---------|----------|
| Bad data propagates downstream | Gate 1 catches at source |
| Calculation errors compound | Gate 2 validates analytics |
| Wrong triggers fired | Gate 3 validates intelligence |
| Non-compliant content sent | Gate 4 validates before delivery |

### 1.3 Gate Ownership

| Gate | Primary Owner | Secondary Owner | What It Validates |
|------|---------------|-----------------|-------------------|
| Gate 1 | Rakia | QR Board | Raw data quality |
| Gate 2 | QR Board | Strategy Board | Analytics correctness |
| Gate 3 | Strategy Board | QR Board | Intelligence logic |
| Gate 4 | CLO Board | CMO Board | Presentation compliance |

### 1.4 Pipeline Flow with Gates

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Layer 1 â”‚     â”‚ Layer 3 â”‚     â”‚ Layer 4 â”‚     â”‚ Layer 5 â”‚     â”‚ Deliver â”‚
â”‚Collectionâ”‚â”€â”€â”€â”€â–¶â”‚Analyticsâ”‚â”€â”€â”€â”€â–¶â”‚Intellig.â”‚â”€â”€â”€â”€â–¶â”‚Present. â”‚â”€â”€â”€â”€â–¶â”‚ to User â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚               â”‚               â”‚               â”‚
     â–¼               â–¼               â–¼               â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ GATE 1  â”‚     â”‚ GATE 2  â”‚     â”‚ GATE 3  â”‚     â”‚ GATE 4  â”‚
â”‚Raw Validâ”‚     â”‚Analyticsâ”‚     â”‚Intellig.â”‚     â”‚Present. â”‚
â”‚  Rakia  â”‚     â”‚QR Board â”‚     â”‚Strategy â”‚     â”‚CLO/CMO  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. Validation Architecture

### 2.1 Validation Result Structure

All gates return a consistent validation result:

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
import datetime

class ValidationStatus(Enum):
    PASS = "pass"           # All checks passed
    WARN = "warn"           # Passed with warnings (proceed but flag)
    FAIL = "fail"           # Failed (block pipeline)
    SKIP = "skip"           # Validation skipped (not applicable)

class ValidationSeverity(Enum):
    ERROR = "error"         # Blocks pipeline
    WARNING = "warning"     # Proceeds but logged
    INFO = "info"           # Informational only

@dataclass
class ValidationIssue:
    code: str               # e.g., "G1-SCH-001"
    severity: ValidationSeverity
    message: str
    field: Optional[str]
    actual_value: Any
    expected_value: Any
    remediation: Optional[str]

@dataclass
class ValidationResult:
    gate: str               # "gate_1", "gate_2", "gate_3", "gate_4"
    status: ValidationStatus
    timestamp: datetime.datetime
    duration_ms: int
    issues: List[ValidationIssue]
    metadata: Dict[str, Any]
    
    @property
    def passed(self) -> bool:
        return self.status in [ValidationStatus.PASS, ValidationStatus.WARN]
    
    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]
    
    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]
```

### 2.2 Gate Interface

All gates implement a common interface:

```python
from abc import ABC, abstractmethod

class ValidationGate(ABC):
    """Base class for all validation gates."""
    
    def __init__(self, config: dict):
        self.config = config
        self.gate_name = self._get_gate_name()
    
    @abstractmethod
    def _get_gate_name(self) -> str:
        """Return gate identifier."""
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """Execute validation and return result."""
        pass
    
    def _create_result(
        self,
        status: ValidationStatus,
        issues: List[ValidationIssue],
        metadata: Dict,
        start_time: datetime.datetime
    ) -> ValidationResult:
        """Create standardized validation result."""
        return ValidationResult(
            gate=self.gate_name,
            status=status,
            timestamp=datetime.datetime.utcnow(),
            duration_ms=int((datetime.datetime.utcnow() - start_time).total_seconds() * 1000),
            issues=issues,
            metadata=metadata
        )
```

---

## 3. Gate 1: Raw Data Validation

### 3.1 Purpose

Gate 1 validates raw data collected from external sources (FRED, DeFiLlama, Etherscan, etc.) before it enters the analytics layer.

**Owner:** Rakia  
**Input:** Raw CSV/JSON data from collectors  
**Output:** Validated data or rejection

### 3.2 Validation Tiers (from Rakia Methodology)

| Tier | Type | Automation | Purpose |
|------|------|------------|---------|
| Tier 1 | Structural | Fully automated | Schema, types, nulls, ranges |
| Tier 2 | Cross-reference | Semi-automated | Known events, calculations |
| Tier 3 | Source verification | Manual + tools | On-chain, live API |

### 3.3 Tier 1: Structural Validation

```python
class Gate1RawDataValidation(ValidationGate):
    """Gate 1: Raw Data Validation (Rakia)"""
    
    def _get_gate_name(self) -> str:
        return "gate_1"
    
    def validate(self, data: dict) -> ValidationResult:
        """Validate raw data from collectors."""
        start_time = datetime.datetime.utcnow()
        issues = []
        
        # Tier 1: Structural validation
        issues.extend(self._validate_schema(data))
        issues.extend(self._validate_types(data))
        issues.extend(self._validate_nulls(data))
        issues.extend(self._validate_ranges(data))
        issues.extend(self._validate_dates(data))
        
        # Tier 2: Cross-reference validation
        issues.extend(self._validate_known_events(data))
        issues.extend(self._validate_calculations(data))
        issues.extend(self._validate_outliers(data))
        
        # Determine status
        errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
        status = ValidationStatus.FAIL if errors else (
            ValidationStatus.WARN if issues else ValidationStatus.PASS
        )
        
        return self._create_result(
            status=status,
            issues=issues,
            metadata={
                "data_source": data.get("source"),
                "record_count": data.get("record_count"),
                "date_range": data.get("date_range")
            },
            start_time=start_time
        )
    
    # --- Tier 1: Structural Checks ---
    
    def _validate_schema(self, data: dict) -> List[ValidationIssue]:
        """Check all required columns present."""
        issues = []
        source = data.get("source")
        schema = self.config["schemas"].get(source, {})
        required_columns = schema.get("required_columns", [])
        
        actual_columns = set(data.get("columns", []))
        missing = set(required_columns) - actual_columns
        
        for col in missing:
            issues.append(ValidationIssue(
                code="G1-SCH-001",
                severity=ValidationSeverity.ERROR,
                message=f"Required column missing: {col}",
                field=col,
                actual_value=None,
                expected_value="present",
                remediation=f"Add column '{col}' to data source"
            ))
        
        return issues
    
    def _validate_types(self, data: dict) -> List[ValidationIssue]:
        """Check column data types."""
        issues = []
        source = data.get("source")
        schema = self.config["schemas"].get(source, {})
        type_rules = schema.get("column_types", {})
        
        for col, expected_type in type_rules.items():
            if col in data.get("columns", []):
                actual_type = data.get("detected_types", {}).get(col)
                if actual_type != expected_type:
                    issues.append(ValidationIssue(
                        code="G1-TYP-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"Type mismatch for {col}",
                        field=col,
                        actual_value=actual_type,
                        expected_value=expected_type,
                        remediation=f"Convert {col} to {expected_type}"
                    ))
        
        return issues
    
    def _validate_nulls(self, data: dict) -> List[ValidationIssue]:
        """Check for nulls in required fields."""
        issues = []
        source = data.get("source")
        schema = self.config["schemas"].get(source, {})
        non_nullable = schema.get("non_nullable_columns", [])
        
        null_counts = data.get("null_counts", {})
        
        for col in non_nullable:
            null_count = null_counts.get(col, 0)
            if null_count > 0:
                issues.append(ValidationIssue(
                    code="G1-NUL-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Null values in required column: {col}",
                    field=col,
                    actual_value=null_count,
                    expected_value=0,
                    remediation=f"Fill or remove {null_count} null values in {col}"
                ))
        
        return issues
    
    def _validate_ranges(self, data: dict) -> List[ValidationIssue]:
        """Check values within valid ranges."""
        issues = []
        source = data.get("source")
        schema = self.config["schemas"].get(source, {})
        range_rules = schema.get("value_ranges", {})
        
        for col, rules in range_rules.items():
            stats = data.get("column_stats", {}).get(col, {})
            min_val = stats.get("min")
            max_val = stats.get("max")
            
            if rules.get("min") is not None and min_val is not None:
                if min_val < rules["min"]:
                    issues.append(ValidationIssue(
                        code="G1-RNG-001",
                        severity=ValidationSeverity.WARNING,
                        message=f"{col} has value below minimum",
                        field=col,
                        actual_value=min_val,
                        expected_value=f">= {rules['min']}",
                        remediation=f"Review values in {col}"
                    ))
            
            if rules.get("max") is not None and max_val is not None:
                if max_val > rules["max"]:
                    issues.append(ValidationIssue(
                        code="G1-RNG-002",
                        severity=ValidationSeverity.WARNING,
                        message=f"{col} has value above maximum",
                        field=col,
                        actual_value=max_val,
                        expected_value=f"<= {rules['max']}",
                        remediation=f"Review values in {col}"
                    ))
        
        return issues
    
    def _validate_dates(self, data: dict) -> List[ValidationIssue]:
        """Check dates within expected range."""
        issues = []
        date_range = data.get("date_range", {})
        min_date = date_range.get("min")
        max_date = date_range.get("max")
        
        expected_min = self.config.get("expected_date_range", {}).get("min")
        expected_max = datetime.date.today().isoformat()
        
        if min_date and expected_min and min_date < expected_min:
            issues.append(ValidationIssue(
                code="G1-DAT-001",
                severity=ValidationSeverity.WARNING,
                message="Data contains dates before expected range",
                field="date",
                actual_value=min_date,
                expected_value=f">= {expected_min}",
                remediation="Verify historical data is intentional"
            ))
        
        if max_date and max_date > expected_max:
            issues.append(ValidationIssue(
                code="G1-DAT-002",
                severity=ValidationSeverity.ERROR,
                message="Data contains future dates",
                field="date",
                actual_value=max_date,
                expected_value=f"<= {expected_max}",
                remediation="Remove or correct future-dated records"
            ))
        
        return issues
    
    # --- Tier 2: Cross-Reference Checks ---
    
    def _validate_known_events(self, data: dict) -> List[ValidationIssue]:
        """Cross-reference against known events."""
        issues = []
        source = data.get("source")
        
        # Check for known historical events
        KNOWN_EVENTS = {
            "btc_prices": [
                {"date": "2022-11-09", "event": "FTX collapse", "expected_drop": True},
                {"date": "2024-01-10", "event": "BTC ETF approval", "expected_pump": True},
            ],
            "usds_prices": [
                {"date": "2023-03-11", "event": "USDC depeg", "max_expected_peg": 0.95},
            ]
        }
        
        events = KNOWN_EVENTS.get(source, [])
        records = data.get("records", [])
        
        for event in events:
            event_date = event["date"]
            matching_records = [r for r in records if r.get("date") == event_date]
            
            if not matching_records:
                issues.append(ValidationIssue(
                    code="G1-EVT-001",
                    severity=ValidationSeverity.WARNING,
                    message=f"Missing data for known event: {event['event']}",
                    field="date",
                    actual_value=None,
                    expected_value=event_date,
                    remediation=f"Verify data coverage for {event_date}"
                ))
        
        return issues
    
    def _validate_calculations(self, data: dict) -> List[ValidationIssue]:
        """Verify calculated fields are correct."""
        issues = []
        
        # Example: Verify YoY calculations
        if "yoy_pct" in data.get("columns", []):
            records = data.get("records", [])
            for i, record in enumerate(records):
                if record.get("yoy_pct") is not None:
                    # Find year-ago value
                    current_val = record.get("value")
                    year_ago_val = self._find_year_ago_value(records, record.get("date"))
                    
                    if year_ago_val and current_val:
                        expected_yoy = ((current_val - year_ago_val) / year_ago_val) * 100
                        actual_yoy = record.get("yoy_pct")
                        
                        if abs(expected_yoy - actual_yoy) > 0.1:  # 0.1% tolerance
                            issues.append(ValidationIssue(
                                code="G1-CAL-001",
                                severity=ValidationSeverity.WARNING,
                                message=f"YoY calculation mismatch at row {i}",
                                field="yoy_pct",
                                actual_value=actual_yoy,
                                expected_value=round(expected_yoy, 2),
                                remediation="Recalculate YoY field"
                            ))
        
        return issues
    
    def _validate_outliers(self, data: dict) -> List[ValidationIssue]:
        """Flag statistical outliers."""
        issues = []
        
        numeric_columns = data.get("numeric_columns", [])
        
        for col in numeric_columns:
            stats = data.get("column_stats", {}).get(col, {})
            mean = stats.get("mean")
            std = stats.get("std")
            min_val = stats.get("min")
            max_val = stats.get("max")
            
            if mean is not None and std is not None and std > 0:
                # Check for values > 4 standard deviations
                lower_bound = mean - 4 * std
                upper_bound = mean + 4 * std
                
                if min_val < lower_bound or max_val > upper_bound:
                    issues.append(ValidationIssue(
                        code="G1-OUT-001",
                        severity=ValidationSeverity.WARNING,
                        message=f"Extreme outliers detected in {col}",
                        field=col,
                        actual_value=f"min={min_val}, max={max_val}",
                        expected_value=f"within [{round(lower_bound, 2)}, {round(upper_bound, 2)}]",
                        remediation=f"Review outliers in {col}"
                    ))
        
        return issues
    
    def _find_year_ago_value(self, records: list, current_date: str) -> Optional[float]:
        """Helper to find value from one year ago."""
        # Implementation details...
        pass
```

### 3.4 Data Source Schemas

**[UPDATED v2.0 - GAP-004 FIX: Added 15 missing CSV schemas]**

```yaml
# config/gate1_schemas.yaml
# Complete schema definitions for all 20 CSV data sources

schemas:
  # ============================================
  # MACRO ECONOMICS (04_MACRO_ECONOMICS.md)
  # ============================================
  
  treasury_yields:
    description: "US Treasury yield curve data from FRED"
    source_file: "treasury_yields.csv"
    required_columns: [date, dgs2, dgs10, dgs30]
    column_types:
      date: date
      dgs2: float
      dgs10: float
      dgs30: float
    non_nullable_columns: [date]
    value_ranges:
      dgs2: {min: 0, max: 20}
      dgs10: {min: 0, max: 20}
      dgs30: {min: 0, max: 20}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  real_yields:
    description: "Real yields (TIPS-adjusted) from FRED"
    source_file: "real_yields.csv"
    required_columns: [date, dfii5, dfii10, dfii30]
    column_types:
      date: date
      dfii5: float
      dfii10: float
      dfii30: float
    non_nullable_columns: [date]
    value_ranges:
      dfii5: {min: -5, max: 10}
      dfii10: {min: -5, max: 10}
      dfii30: {min: -5, max: 10}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  global_liquidity:
    description: "Global M2 money supply data"
    source_file: "global_liquidity.csv"
    required_columns: [date, country, m2_local, m2_usd, yoy_pct]
    column_types:
      date: date
      country: string
      m2_local: float
      m2_usd: float
      yoy_pct: float
    non_nullable_columns: [date, country, m2_usd]
    value_ranges:
      yoy_pct: {min: -50, max: 100}
    freshness_rules:
      max_age_hours: 720  # 30 days - monthly data
      publication_lag_weeks: 3  # [GAP-005 FIX: Corrected from 2 months]
      weekend_holiday_handling: false  # Monthly release
      expected_update_frequency: "monthly"
  
  # ============================================
  # TRADFI MARKETS (03_TRADFI_MARKETS.md)
  # ============================================
  
  tradfi_benchmark_data:
    description: "Traditional finance benchmark indices"
    source_file: "tradfi_benchmark_data.csv"
    required_columns: [date, spy_close, tlt_close, gld_close, vix_close]
    column_types:
      date: date
      spy_close: float
      tlt_close: float
      gld_close: float
      vix_close: float
    non_nullable_columns: [date, spy_close]
    value_ranges:
      spy_close: {min: 50, max: 1000}
      tlt_close: {min: 50, max: 200}
      gld_close: {min: 50, max: 500}
      vix_close: {min: 5, max: 100}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  commodities:
    description: "Commodity prices (Gold, Oil, Copper)"
    source_file: "commodities.csv"
    required_columns: [date, gold_usd, oil_wti_usd, copper_usd]
    column_types:
      date: date
      gold_usd: float
      oil_wti_usd: float
      copper_usd: float
    non_nullable_columns: [date, gold_usd]
    value_ranges:
      gold_usd: {min: 500, max: 5000}
      oil_wti_usd: {min: 10, max: 200}
      copper_usd: {min: 1, max: 10}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  credit_spreads:
    description: "Credit spread indicators (HY, IG)"
    source_file: "credit_spreads.csv"
    required_columns: [date, hy_spread_bps, ig_spread_bps, ted_spread_bps]
    column_types:
      date: date
      hy_spread_bps: float
      ig_spread_bps: float
      ted_spread_bps: float
    non_nullable_columns: [date, hy_spread_bps]
    value_ranges:
      hy_spread_bps: {min: 100, max: 2500}
      ig_spread_bps: {min: 50, max: 500}
      ted_spread_bps: {min: 0, max: 500}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  rotation_indicators:
    description: "Sector rotation and risk appetite indicators"
    source_file: "rotation_indicators.csv"
    required_columns: [date, xlf_xlu_ratio, iwm_spy_ratio, hyg_lqd_ratio, copper_gold_ratio]
    column_types:
      date: date
      xlf_xlu_ratio: float
      iwm_spy_ratio: float
      hyg_lqd_ratio: float
      copper_gold_ratio: float
    non_nullable_columns: [date]
    value_ranges:
      xlf_xlu_ratio: {min: 0.2, max: 5.0}
      iwm_spy_ratio: {min: 0.1, max: 1.0}
      hyg_lqd_ratio: {min: 0.5, max: 2.0}
      copper_gold_ratio: {min: 0.0001, max: 0.01}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
    calculation_notes:
      copper_gold_ratio: "copper_usd / gold_usd (unitless ratio ~0.002)"
  
  # ============================================
  # CRYPTO MARKETS (02_CRYPTO_MARKETS.md)
  # ============================================
  
  crypto_prices:
    description: "Cryptocurrency price data from CoinGecko"
    source_file: "crypto_prices.csv"
    required_columns: [date, btc_usd, eth_usd, sol_usd]
    column_types:
      date: date
      btc_usd: float
      eth_usd: float
      sol_usd: float
    non_nullable_columns: [date, btc_usd]
    value_ranges:
      btc_usd: {min: 1000, max: 500000}
      eth_usd: {min: 100, max: 50000}
      sol_usd: {min: 1, max: 1000}
    freshness_rules:
      max_age_hours: 1
      weekend_holiday_handling: false  # Crypto trades 24/7
      expected_update_frequency: "hourly"
  
  defillama_historical_apy:
    description: "DeFi protocol APY data from DeFiLlama"
    source_file: "defillama_historical_apy.csv"
    required_columns: [date, protocol, chain, pool, apy, tvl_usd]
    column_types:
      date: date
      protocol: string
      chain: string
      pool: string
      apy: float
      tvl_usd: float
    non_nullable_columns: [date, protocol, apy]
    value_ranges:
      apy: {min: 0, max: 1000}
      tvl_usd: {min: 0}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: false  # DeFi operates 24/7
      expected_update_frequency: "daily"
  
  jupiter_jlp_historical_apy:
    description: "Jupiter JLP pool APY history"
    source_file: "jupiter_jlp_historical_apy.csv"
    required_columns: [date, apy, tvl_usd, volume_24h]
    column_types:
      date: date
      apy: float
      tvl_usd: float
      volume_24h: float
    non_nullable_columns: [date, apy]
    value_ranges:
      apy: {min: 0, max: 500}
      tvl_usd: {min: 0}
      volume_24h: {min: 0}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: false
      expected_update_frequency: "daily"
  
  jito_historical_apy:
    description: "Jito staking APY history"
    source_file: "jito_historical_apy.csv"
    required_columns: [date, apy, tvl_sol, mev_rewards_usd]
    column_types:
      date: date
      apy: float
      tvl_sol: float
      mev_rewards_usd: float
    non_nullable_columns: [date, apy]
    value_ranges:
      apy: {min: 0, max: 50}
      tvl_sol: {min: 0}
      mev_rewards_usd: {min: 0}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: false
      expected_update_frequency: "daily"
  
  # ============================================
  # ON-CHAIN INTELLIGENCE (01_ON_CHAIN_INTELLIGENCE.md)
  # ============================================
  
  estate_wallet_tracker:
    description: "Bankruptcy estate wallet balances"
    source_file: "estate_wallet_tracker.csv"
    required_columns: [date, entity_name, wallet_address, chain, balance_usd, token_symbol]
    column_types:
      date: date
      entity_name: string  # Note: Column name is 'entity_name' not 'entity'
      wallet_address: string
      chain: string
      balance_usd: float
      token_symbol: string
    non_nullable_columns: [date, entity_name, wallet_address, chain]
    value_ranges:
      balance_usd: {min: 0}
    freshness_rules:
      max_age_hours: 6
      weekend_holiday_handling: false  # On-chain, 24/7
      expected_update_frequency: "every_6_hours"
    notes:
      - "Critical for liquidation risk monitoring"
      - "Manual-only data source - requires human verification"
  
  market_maker_wallet_tracker:
    description: "Major market maker wallet activity"
    source_file: "market_maker_wallet_tracker.csv"
    required_columns: [date, entity_alias, wallet_address, chain, balance_usd, net_flow_24h]
    column_types:
      date: date
      entity_alias: string
      wallet_address: string
      chain: string
      balance_usd: float
      net_flow_24h: float
    non_nullable_columns: [date, wallet_address, chain]
    value_ranges:
      balance_usd: {min: 0}
    freshness_rules:
      max_age_hours: 6
      weekend_holiday_handling: false
      expected_update_frequency: "every_6_hours"
    notes:
      - "Manual-only data source"
      - "Entity names anonymized per privacy policy"
  
  protocol_treasury_tracker:
    description: "Protocol treasury holdings"
    source_file: "protocol_treasury_tracker.csv"
    required_columns: [date, protocol, chain, treasury_usd, token_holdings]
    column_types:
      date: date
      protocol: string
      chain: string
      treasury_usd: float
      token_holdings: string
    non_nullable_columns: [date, protocol, treasury_usd]
    value_ranges:
      treasury_usd: {min: 0}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: false
      expected_update_frequency: "daily"
  
  whale_wallet_master_list:
    description: "Master list of tracked whale wallets"
    source_file: "whale_wallet_master_list.csv"
    required_columns: [wallet_address, chain, category, first_seen, last_active, estimated_value_usd]
    column_types:
      wallet_address: string
      chain: string
      category: string
      first_seen: date
      last_active: date
      estimated_value_usd: float
    non_nullable_columns: [wallet_address, chain, category]
    value_ranges:
      estimated_value_usd: {min: 0}
    freshness_rules:
      max_age_hours: 168  # Weekly updates acceptable
      weekend_holiday_handling: false
      expected_update_frequency: "weekly"
  
  # ============================================
  # INSTITUTIONAL FLOWS (05_INSTITUTIONAL_FLOWS.md)
  # ============================================
  
  btc_etf_holdings:
    description: "Bitcoin ETF holdings data"
    source_file: "btc_etf_holdings.csv"
    required_columns: [date, etf_ticker, btc_holdings, aum_usd, daily_flow_usd]
    column_types:
      date: date
      etf_ticker: string
      btc_holdings: float
      aum_usd: float
      daily_flow_usd: float
    non_nullable_columns: [date, etf_ticker, btc_holdings]
    value_ranges:
      btc_holdings: {min: 0}
      aum_usd: {min: 0}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  corporate_btc_holdings:
    description: "Public company Bitcoin holdings"
    source_file: "corporate_btc_holdings.csv"
    required_columns: [date, company, ticker, btc_holdings, cost_basis_usd, market_value_usd]
    column_types:
      date: date
      company: string
      ticker: string
      btc_holdings: float
      cost_basis_usd: float
      market_value_usd: float
    non_nullable_columns: [date, company, btc_holdings]
    value_ranges:
      btc_holdings: {min: 0}
      cost_basis_usd: {min: 0}
      market_value_usd: {min: 0}
    freshness_rules:
      max_age_hours: 168  # Weekly updates from SEC filings
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "weekly"
  
  institutional_13f:
    description: "13F institutional holdings filings"
    source_file: "institutional_13f.csv"
    required_columns: [filing_date, institution, ticker, shares, value_usd, change_pct]
    column_types:
      filing_date: date
      institution: string
      ticker: string
      shares: integer
      value_usd: float
      change_pct: float
    non_nullable_columns: [filing_date, institution, ticker, shares]
    value_ranges:
      shares: {min: 0}
      value_usd: {min: 0}
    freshness_rules:
      max_age_hours: 720  # 30 days - quarterly filings
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "quarterly"
  
  # ============================================
  # SENTIMENT (07_NEWS_AND_SENTIMENT.md)
  # ============================================
  
  sentiment_indicators:
    description: "Market sentiment indicators"
    source_file: "sentiment_indicators.csv"
    required_columns: [date, fear_greed_index, put_call_ratio, vix]
    column_types:
      date: date
      fear_greed_index: integer
      put_call_ratio: float
      vix: float
    non_nullable_columns: [date, fear_greed_index]
    value_ranges:
      fear_greed_index: {min: 0, max: 100}
      put_call_ratio: {min: 0.2, max: 3.0}
      vix: {min: 5, max: 100}
    freshness_rules:
      max_age_hours: 24
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "daily"
  
  aaii_sentiment:
    description: "AAII investor sentiment survey"
    source_file: "aaii_sentiment.csv"
    required_columns: [date, bullish_pct, bearish_pct, neutral_pct, bull_bear_spread]
    column_types:
      date: date
      bullish_pct: float
      bearish_pct: float
      neutral_pct: float
      bull_bear_spread: float
    non_nullable_columns: [date, bullish_pct, bearish_pct]
    value_ranges:
      bullish_pct: {min: 0, max: 100}
      bearish_pct: {min: 0, max: 100}
      neutral_pct: {min: 0, max: 100}
      bull_bear_spread: {min: -100, max: 100}
    freshness_rules:
      max_age_hours: 168  # Weekly survey
      weekend_holiday_handling: true  # [GAP-015 FIX]
      expected_update_frequency: "weekly"

# Global configuration
expected_date_range:
  min: "2020-01-01"
  max: "today"  # Dynamic - current date
```

### 3.5 Weekend and Holiday Handling

**[NEW in v2.0 - GAP-015 FIX]**

Traditional finance data sources (Treasury, ETFs, equities) do not publish on weekends and market holidays. The freshness check must account for this to avoid false alerts.

```python
import datetime
from typing import Optional
import holidays

class FreshnessChecker:
    """Check data freshness with weekend/holiday awareness."""
    
    def __init__(self, country: str = 'US'):
        self.holidays = holidays.US() if country == 'US' else holidays.country_holidays(country)
    
    def check_freshness(
        self,
        last_updated: datetime.datetime,
        data_type: str,
        schema_config: dict
    ) -> dict:
        """
        Check if data meets freshness requirements.
        
        [GAP-015 FIX]: Now accounts for weekends and market holidays
        for TradFi data sources.
        """
        freshness_rules = schema_config.get('freshness_rules', {})
        max_age_hours = freshness_rules.get('max_age_hours', 24)
        handles_weekends = freshness_rules.get('weekend_holiday_handling', False)
        
        now = datetime.datetime.utcnow()
        actual_age_hours = (now - last_updated).total_seconds() / 3600
        
        # Calculate effective age (excluding non-trading periods)
        if handles_weekends:
            effective_age_hours = self._calculate_effective_age(
                last_updated, now
            )
        else:
            effective_age_hours = actual_age_hours
        
        is_fresh = effective_age_hours <= max_age_hours
        
        return {
            'is_fresh': is_fresh,
            'actual_age_hours': round(actual_age_hours, 1),
            'effective_age_hours': round(effective_age_hours, 1),
            'max_allowed_hours': max_age_hours,
            'weekend_adjustment_applied': handles_weekends,
            'status': 'fresh' if is_fresh else 'stale'
        }
    
    def _calculate_effective_age(
        self,
        last_updated: datetime.datetime,
        now: datetime.datetime
    ) -> float:
        """
        Calculate effective age excluding weekends and holidays.
        
        Example: If data last updated Friday 5pm and it's Monday 9am,
        actual age = 64 hours, effective age = 16 hours (excluding Sat/Sun).
        """
        total_hours = 0
        current = last_updated
        
        while current < now:
            # Check if this hour is a trading hour
            if self._is_trading_day(current):
                total_hours += 1
            current += datetime.timedelta(hours=1)
        
        return total_hours
    
    def _is_trading_day(self, dt: datetime.datetime) -> bool:
        """Check if date is a trading day (not weekend or holiday)."""
        # Weekend check
        if dt.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        
        # Holiday check
        if dt.date() in self.holidays:
            return False
        
        return True
    
    def get_expected_latest_date(self, data_type: str) -> datetime.date:
        """
        Get the expected latest data date given weekends/holidays.
        
        If today is Monday, expected latest for TradFi = previous Friday.
        If today is a holiday, expected latest = last trading day.
        """
        today = datetime.date.today()
        
        # Walk backwards to find last trading day
        check_date = today
        for _ in range(10):  # Max 10 days back
            if self._is_trading_day(datetime.datetime.combine(check_date, datetime.time(12, 0))):
                return check_date
            check_date -= datetime.timedelta(days=1)
        
        return today - datetime.timedelta(days=1)


# Validation integration
def validate_data_freshness(
    data: dict,
    schema_config: dict
) -> List[ValidationIssue]:
    """
    Validate data freshness with weekend/holiday awareness.
    
    [GAP-015 FIX]: Uses FreshnessChecker for accurate freshness assessment.
    """
    issues = []
    checker = FreshnessChecker()
    
    last_updated = data.get('last_updated')
    if not last_updated:
        return issues
    
    if isinstance(last_updated, str):
        last_updated = datetime.datetime.fromisoformat(last_updated)
    
    result = checker.check_freshness(
        last_updated=last_updated,
        data_type=data.get('source'),
        schema_config=schema_config
    )
    
    if not result['is_fresh']:
        # Determine severity based on how stale
        if result['effective_age_hours'] > result['max_allowed_hours'] * 3:
            severity = ValidationSeverity.ERROR
        else:
            severity = ValidationSeverity.WARNING
        
        issues.append(ValidationIssue(
            code="G1-FRS-001",
            severity=severity,
            message=f"Data is stale: {result['effective_age_hours']}h effective age (max: {result['max_allowed_hours']}h)",
            field="last_updated",
            actual_value=f"{result['actual_age_hours']}h actual, {result['effective_age_hours']}h effective",
            expected_value=f"<= {result['max_allowed_hours']}h",
            remediation="Refresh data from source"
        ))
    
    return issues
```

---

## 4. Gate 2: Analytics Validation

### 4.1 Purpose

Gate 2 validates outputs from the QR Board analytics engines (Battle Test, Monte Carlo, risk metrics) before they enter the intelligence layer.

**Owner:** QR Board  
**Input:** Analytics engine outputs  
**Output:** Validated metrics or rejection

### 4.2 Validation Categories

| Category | What It Checks |
|----------|----------------|
| Completeness | All strategies have results |
| Value Bounds | No impossible values (VaR > 100%, negative Sharpe where invalid) |
| Statistical Sanity | Distributions make sense |
| Historical Consistency | Results within expected variance of previous runs |
| Cross-Metric Coherence | Related metrics are consistent |

### 4.3 Implementation

```python
class Gate2AnalyticsValidation(ValidationGate):
    """Gate 2: Analytics Validation (QR Board)"""
    
    def _get_gate_name(self) -> str:
        return "gate_2"
    
    def validate(self, data: dict) -> ValidationResult:
        """Validate analytics engine outputs."""
        start_time = datetime.datetime.utcnow()
        issues = []
        
        # Completeness checks
        issues.extend(self._validate_completeness(data))
        
        # Value bounds checks
        issues.extend(self._validate_bounds(data))
        
        # Statistical sanity checks
        issues.extend(self._validate_statistical_sanity(data))
        
        # Historical consistency checks
        issues.extend(self._validate_historical_consistency(data))
        
        # Cross-metric coherence checks
        issues.extend(self._validate_cross_metric_coherence(data))
        
        # Invalid value checks (NaN, Inf)
        issues.extend(self._validate_no_invalid_values(data))
        
        # Determine status
        errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
        status = ValidationStatus.FAIL if errors else (
            ValidationStatus.WARN if issues else ValidationStatus.PASS
        )
        
        return self._create_result(
            status=status,
            issues=issues,
            metadata={
                "strategies_validated": len(data.get("strategies", {})),
                "monte_carlo_paths": data.get("monte_carlo_config", {}).get("num_paths")
            },
            start_time=start_time
        )
    
    def _validate_completeness(self, data: dict) -> List[ValidationIssue]:
        """Check all strategies have results."""
        issues = []
        
        expected_strategies = set(range(1, 11))  # Strategies 1-10
        actual_strategies = set(data.get("strategies", {}).keys())
        
        # Convert to int if string keys
        actual_strategies = {int(s) for s in actual_strategies}
        
        missing = expected_strategies - actual_strategies
        
        for strategy_id in missing:
            issues.append(ValidationIssue(
                code="G2-CMP-001",
                severity=ValidationSeverity.ERROR,
                message=f"Missing results for strategy {strategy_id}",
                field=f"strategies.{strategy_id}",
                actual_value=None,
                expected_value="present",
                remediation=f"Run analytics for strategy {strategy_id}"
            ))
        
        # Check required metrics for each strategy
        required_metrics = ["var_95", "cvar_99", "sharpe_ratio", "max_drawdown", "median_return"]
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            for metric in required_metrics:
                if metric not in metrics or metrics[metric] is None:
                    issues.append(ValidationIssue(
                        code="G2-CMP-002",
                        severity=ValidationSeverity.ERROR,
                        message=f"Missing metric {metric} for strategy {strategy_id}",
                        field=f"strategies.{strategy_id}.{metric}",
                        actual_value=None,
                        expected_value="present",
                        remediation=f"Calculate {metric} for strategy {strategy_id}"
                    ))
        
        return issues
    
    def _validate_bounds(self, data: dict) -> List[ValidationIssue]:
        """Check values within valid bounds."""
        issues = []
        
        # NOTE: sharpe_ratio min is -5, allowing negative values
        # See Section 4.4 for explanation of when negative Sharpe is valid
        BOUNDS = {
            "var_95": {"min": 0, "max": 100, "unit": "%"},
            "cvar_99": {"min": 0, "max": 100, "unit": "%"},
            "sharpe_ratio": {"min": -5, "max": 10, "unit": "ratio"},  # Negative allowed
            "max_drawdown": {"min": 0, "max": 100, "unit": "%"},
            "probability_of_loss": {"min": 0, "max": 1, "unit": "probability"},
            "median_return": {"min": -100, "max": 500, "unit": "%"},
        }
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            for metric, bounds in BOUNDS.items():
                value = metrics.get(metric)
                if value is not None:
                    if value < bounds["min"]:
                        issues.append(ValidationIssue(
                            code="G2-BND-001",
                            severity=ValidationSeverity.ERROR,
                            message=f"{metric} below minimum for strategy {strategy_id}",
                            field=f"strategies.{strategy_id}.{metric}",
                            actual_value=value,
                            expected_value=f">= {bounds['min']} {bounds['unit']}",
                            remediation=f"Review {metric} calculation"
                        ))
                    if value > bounds["max"]:
                        severity = ValidationSeverity.ERROR if metric in ["var_95", "probability_of_loss"] else ValidationSeverity.WARNING
                        issues.append(ValidationIssue(
                            code="G2-BND-002",
                            severity=severity,
                            message=f"{metric} above maximum for strategy {strategy_id}",
                            field=f"strategies.{strategy_id}.{metric}",
                            actual_value=value,
                            expected_value=f"<= {bounds['max']} {bounds['unit']}",
                            remediation=f"Review {metric} calculation (value seems extreme)"
                        ))
        
        return issues
    
    def _validate_statistical_sanity(self, data: dict) -> List[ValidationIssue]:
        """Check statistical properties make sense."""
        issues = []
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            # Confidence intervals should be ordered
            ci_5th = metrics.get("ci_5th")
            ci_50th = metrics.get("median_return")
            ci_95th = metrics.get("ci_95th")
            
            if all(v is not None for v in [ci_5th, ci_50th, ci_95th]):
                if not (ci_5th <= ci_50th <= ci_95th):
                    issues.append(ValidationIssue(
                        code="G2-STA-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"Confidence intervals not ordered for strategy {strategy_id}",
                        field=f"strategies.{strategy_id}.ci",
                        actual_value=f"5th={ci_5th}, 50th={ci_50th}, 95th={ci_95th}",
                        expected_value="5th <= 50th <= 95th",
                        remediation="Review Monte Carlo quantile calculations"
                    ))
            
            # VaR should be less than or equal to CVaR
            var_95 = metrics.get("var_95")
            cvar_99 = metrics.get("cvar_99")
            
            if var_95 is not None and cvar_99 is not None:
                if cvar_99 < var_95:
                    issues.append(ValidationIssue(
                        code="G2-STA-002",
                        severity=ValidationSeverity.WARNING,
                        message=f"CVaR < VaR for strategy {strategy_id} (unusual)",
                        field=f"strategies.{strategy_id}.risk",
                        actual_value=f"VaR95={var_95}, CVaR99={cvar_99}",
                        expected_value="CVaR99 >= VaR95",
                        remediation="Review risk metric calculations"
                    ))
            
            # Higher risk strategies should have higher risk metrics
            risk_tier = self._get_risk_tier(int(strategy_id))
            if risk_tier == "high" and var_95 is not None and var_95 < 5:
                issues.append(ValidationIssue(
                    code="G2-STA-003",
                    severity=ValidationSeverity.WARNING,
                    message=f"High-risk strategy {strategy_id} has low VaR",
                    field=f"strategies.{strategy_id}.var_95",
                    actual_value=var_95,
                    expected_value=">= 5% for high-risk strategy",
                    remediation="Verify risk tier alignment"
                ))
        
        return issues
    
    def _validate_historical_consistency(self, data: dict) -> List[ValidationIssue]:
        """Check results consistent with previous runs."""
        issues = []
        
        previous_results = self._load_previous_results()
        if not previous_results:
            return issues  # No previous data to compare
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            prev_metrics = previous_results.get(str(strategy_id), {})
            
            for metric in ["var_95", "sharpe_ratio", "median_return"]:
                current = metrics.get(metric)
                previous = prev_metrics.get(metric)
                
                if current is not None and previous is not None:
                    # Check if change > 2 standard deviations
                    change_pct = abs((current - previous) / previous) * 100 if previous != 0 else 0
                    
                    if change_pct > 50:  # 50% change is significant
                        issues.append(ValidationIssue(
                            code="G2-HIS-001",
                            severity=ValidationSeverity.WARNING,
                            message=f"{metric} changed significantly for strategy {strategy_id}",
                            field=f"strategies.{strategy_id}.{metric}",
                            actual_value=f"current={current}, previous={previous}, change={change_pct:.1f}%",
                            expected_value="change < 50%",
                            remediation="Verify large change is expected"
                        ))
        
        return issues
    
    def _validate_cross_metric_coherence(self, data: dict) -> List[ValidationIssue]:
        """Check related metrics are consistent."""
        issues = []
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            # Higher Sharpe should correlate with lower probability of loss
            sharpe = metrics.get("sharpe_ratio")
            prob_loss = metrics.get("probability_of_loss")
            
            if sharpe is not None and prob_loss is not None:
                if sharpe > 2 and prob_loss > 0.3:
                    issues.append(ValidationIssue(
                        code="G2-COH-001",
                        severity=ValidationSeverity.WARNING,
                        message=f"High Sharpe with high loss probability for strategy {strategy_id}",
                        field=f"strategies.{strategy_id}",
                        actual_value=f"Sharpe={sharpe}, P(loss)={prob_loss}",
                        expected_value="High Sharpe should have low P(loss)",
                        remediation="Review metric calculations for consistency"
                    ))
            
            # Max drawdown should align with VaR
            max_dd = metrics.get("max_drawdown")
            var_95 = metrics.get("var_95")
            
            if max_dd is not None and var_95 is not None:
                if max_dd < var_95:
                    issues.append(ValidationIssue(
                        code="G2-COH-002",
                        severity=ValidationSeverity.WARNING,
                        message=f"Max drawdown less than VaR for strategy {strategy_id}",
                        field=f"strategies.{strategy_id}",
                        actual_value=f"MaxDD={max_dd}, VaR95={var_95}",
                        expected_value="MaxDD typically >= VaR95",
                        remediation="Verify historical drawdown calculation"
                    ))
        
        return issues
    
    def _validate_no_invalid_values(self, data: dict) -> List[ValidationIssue]:
        """Check for NaN, Inf, or other invalid values."""
        issues = []
        
        import math
        
        for strategy_id, metrics in data.get("strategies", {}).items():
            for metric, value in metrics.items():
                if isinstance(value, float):
                    if math.isnan(value):
                        issues.append(ValidationIssue(
                            code="G2-INV-001",
                            severity=ValidationSeverity.ERROR,
                            message=f"NaN value for {metric} in strategy {strategy_id}",
                            field=f"strategies.{strategy_id}.{metric}",
                            actual_value="NaN",
                            expected_value="valid number",
                            remediation=f"Fix {metric} calculation"
                        ))
                    elif math.isinf(value):
                        issues.append(ValidationIssue(
                            code="G2-INV-002",
                            severity=ValidationSeverity.ERROR,
                            message=f"Infinite value for {metric} in strategy {strategy_id}",
                            field=f"strategies.{strategy_id}.{metric}",
                            actual_value="Inf",
                            expected_value="finite number",
                            remediation=f"Fix {metric} calculation (check for division by zero)"
                        ))
        
        return issues
    
    def _get_risk_tier(self, strategy_id: int) -> str:
        """Get risk tier for a strategy."""
        RISK_TIERS = {
            1: "minimal", 2: "low", 3: "minimal", 4: "low-medium", 5: "minimal",
            6: "medium", 7: "minimal", 8: "high", 9: "low", 10: "very-high"
        }
        return RISK_TIERS.get(strategy_id, "unknown")
    
    def _load_previous_results(self) -> dict:
        """Load previous analytics results for comparison."""
        # Implementation: Load from database or file
        pass
```

### 4.4 Negative Sharpe Ratio Explanation

**[NEW in v2.0 - Added for clarity]**

A **negative Sharpe ratio** can occur and is mathematically valid. It indicates:

1. **Negative excess return**: The strategy's return is below the risk-free rate
2. **Interpretation**: The strategy lost money relative to simply holding Treasury bills

```python
# Sharpe Ratio Formula
sharpe_ratio = (strategy_return - risk_free_rate) / strategy_volatility

# Example: Negative Sharpe
# Strategy return: 2%
# Risk-free rate: 4%
# Volatility: 10%
# Sharpe = (0.02 - 0.04) / 0.10 = -0.20
```

**When negative Sharpe is expected:**
- Bear markets where crypto strategies underperform cash
- High-volatility strategies during drawdowns
- Strategies with crypto exposure in 2022 (FTX collapse year)

**Validation approach:**
- Do NOT flag negative Sharpe as an error
- Minimum bound is -5 (extremely negative would indicate calculation error)
- Cross-check with other metrics (negative Sharpe should correlate with high P(loss))

---

## 5. Gate 3: Intelligence Validation

### 5.1 Purpose

Gate 3 validates outputs from the Strategy Board intelligence engine (triggers, alerts, rebalancing recommendations) before they enter the presentation layer.

**Owner:** Strategy Board  
**Input:** Intelligence engine outputs (alerts, recommendations)  
**Output:** Validated alerts or rejection

### 5.2 Validation Categories

| Category | What It Checks |
|----------|----------------|
| Strategy Mapping | Only valid strategy IDs (1-10) |
| Threshold Logic | Alert levels are properly ordered |
| Deduplication | No duplicate alerts for same event |
| Priority Assignment | All alerts have valid priority |
| Escalation Paths | P0 alerts have escalation defined |
| Rate Limiting | Not overwhelming users |

### 5.3 Implementation

```python
class Gate3IntelligenceValidation(ValidationGate):
    """Gate 3: Intelligence Validation (Strategy Board)"""
    
    def _get_gate_name(self) -> str:
        return "gate_3"
    
    def validate(self, data: dict) -> ValidationResult:
        """Validate intelligence engine outputs."""
        start_time = datetime.datetime.utcnow()
        issues = []
        
        alerts = data.get("alerts", [])
        recommendations = data.get("rebalance_recommendations", [])
        
        # Alert validations
        issues.extend(self._validate_strategy_ids(alerts))
        issues.extend(self._validate_priority_assignment(alerts))
        issues.extend(self._validate_escalation_paths(alerts))
        issues.extend(self._validate_no_duplicates(alerts))
        issues.extend(self._validate_rate_limits(alerts))
        issues.extend(self._validate_consolidation_logic(alerts))
        issues.extend(self._validate_threshold_logic(alerts))
        
        # Rebalance recommendation validations
        issues.extend(self._validate_rebalance_recommendations(recommendations))
        
        # Determine status
        errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
        status = ValidationStatus.FAIL if errors else (
            ValidationStatus.WARN if issues else ValidationStatus.PASS
        )
        
        return self._create_result(
            status=status,
            issues=issues,
            metadata={
                "alerts_validated": len(alerts),
                "recommendations_validated": len(recommendations)
            },
            start_time=start_time
        )
    
    def _validate_strategy_ids(self, alerts: list) -> List[ValidationIssue]:
        """Validate all strategy IDs are valid."""
        issues = []
        valid_strategies = set(range(1, 11))  # 1-10
        
        for alert in alerts:
            affected = alert.get("affected_strategies", [])
            
            # Handle "all" keyword
            if affected == "all":
                continue
            
            for strategy_id in affected:
                if isinstance(strategy_id, str):
                    try:
                        strategy_id = int(strategy_id)
                    except ValueError:
                        issues.append(ValidationIssue(
                            code="G3-STR-001",
                            severity=ValidationSeverity.ERROR,
                            message=f"Invalid strategy ID format: {strategy_id}",
                            field="affected_strategies",
                            actual_value=strategy_id,
                            expected_value="integer 1-10",
                            remediation="Use integer strategy IDs"
                        ))
                        continue
                
                if strategy_id not in valid_strategies:
                    issues.append(ValidationIssue(
                        code="G3-STR-002",
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid strategy ID: {strategy_id}",
                        field="affected_strategies",
                        actual_value=strategy_id,
                        expected_value="1-10",
                        remediation="Use valid strategy ID (1-10)"
                    ))
        
        return issues
    
    def _validate_priority_assignment(self, alerts: list) -> List[ValidationIssue]:
        """Validate all alerts have valid priority."""
        issues = []
        valid_priorities = {"P0", "P1", "P2", "P3"}
        
        for alert in alerts:
            priority = alert.get("priority")
            
            if priority is None:
                issues.append(ValidationIssue(
                    code="G3-PRI-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Alert missing priority: {alert.get('alert_id')}",
                    field="priority",
                    actual_value=None,
                    expected_value="P0, P1, P2, or P3",
                    remediation="Assign priority to alert"
                ))
            elif priority not in valid_priorities:
                issues.append(ValidationIssue(
                    code="G3-PRI-002",
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid priority: {priority}",
                    field="priority",
                    actual_value=priority,
                    expected_value="P0, P1, P2, or P3",
                    remediation="Use valid priority level"
                ))
        
        return issues
    
    def _validate_escalation_paths(self, alerts: list) -> List[ValidationIssue]:
        """Validate P0 alerts have escalation defined."""
        issues = []
        
        for alert in alerts:
            if alert.get("priority") == "P0":
                escalation = alert.get("routing", {}).get("escalation")
                
                if not escalation or not escalation.get("escalate_to"):
                    issues.append(ValidationIssue(
                        code="G3-ESC-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"P0 alert missing escalation path: {alert.get('alert_id')}",
                        field="routing.escalation",
                        actual_value=escalation,
                        expected_value="escalation path defined",
                        remediation="Define escalation path for P0 alerts"
                    ))
        
        return issues
    
    def _validate_no_duplicates(self, alerts: list) -> List[ValidationIssue]:
        """Validate no duplicate alerts for same event."""
        issues = []
        seen = set()
        
        for alert in alerts:
            event_type = alert.get("event_type")
            timestamp = alert.get("timestamp")
            
            if timestamp:
                timestamp_key = timestamp[:16] if isinstance(timestamp, str) else timestamp.strftime("%Y-%m-%dT%H:%M")
            else:
                timestamp_key = "unknown"
            
            dedup_key = f"{event_type}_{timestamp_key}"
            
            if dedup_key in seen:
                issues.append(ValidationIssue(
                    code="G3-DUP-001",
                    severity=ValidationSeverity.WARNING,
                    message=f"Duplicate alert detected: {event_type}",
                    field="event_type",
                    actual_value=dedup_key,
                    expected_value="unique event",
                    remediation="Deduplicate alerts before processing"
                ))
            
            seen.add(dedup_key)
        
        return issues
    
    def _validate_rate_limits(self, alerts: list) -> List[ValidationIssue]:
        """Validate not overwhelming users with alerts."""
        issues = []
        
        user_alerts = {}
        for alert in alerts:
            users = alert.get("routing", {}).get("user_segments", [])
            for user in users:
                user_alerts.setdefault(user, []).append(alert)
        
        MAX_ALERTS_PER_HOUR = 10
        
        for user, user_alert_list in user_alerts.items():
            if len(user_alert_list) > MAX_ALERTS_PER_HOUR:
                issues.append(ValidationIssue(
                    code="G3-RAT-001",
                    severity=ValidationSeverity.WARNING,
                    message=f"User {user} would receive {len(user_alert_list)} alerts (limit: {MAX_ALERTS_PER_HOUR})",
                    field="routing.user_segments",
                    actual_value=len(user_alert_list),
                    expected_value=f"<= {MAX_ALERTS_PER_HOUR}",
                    remediation="Consolidate or throttle alerts"
                ))
        
        return issues
    
    def _validate_consolidation_logic(self, alerts: list) -> List[ValidationIssue]:
        """Validate alert consolidation is proper."""
        issues = []
        
        for alert in alerts:
            if alert.get("consolidation_group"):
                individual_triggers = alert.get("individual_triggers", [])
                
                if len(individual_triggers) < 2:
                    issues.append(ValidationIssue(
                        code="G3-CON-001",
                        severity=ValidationSeverity.WARNING,
                        message=f"Consolidated alert with only {len(individual_triggers)} trigger(s)",
                        field="consolidation_group",
                        actual_value=len(individual_triggers),
                        expected_value=">= 2",
                        remediation="Review consolidation logic"
                    ))
        
        return issues
    
    def _validate_threshold_logic(self, alerts: list) -> List[ValidationIssue]:
        """Validate threshold values are logical."""
        issues = []
        
        for alert in alerts:
            trigger = alert.get("trigger", {})
            actual = trigger.get("actual_value")
            threshold = trigger.get("threshold")
            condition = trigger.get("condition", "")
            
            if actual is not None and threshold is not None:
                if ">" in condition and actual <= threshold:
                    issues.append(ValidationIssue(
                        code="G3-THR-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"Trigger fired but condition not met: {condition}",
                        field="trigger",
                        actual_value=f"actual={actual}, threshold={threshold}",
                        expected_value=f"actual {condition}",
                        remediation="Review trigger evaluation logic"
                    ))
        
        return issues
    
    def _validate_rebalance_recommendations(self, recommendations: list) -> List[ValidationIssue]:
        """Validate rebalance recommendations."""
        issues = []
        
        for rec in recommendations:
            strategy_id = rec.get("strategy_id")
            max_drift = rec.get("max_drift_pct")
            rec_type = rec.get("recommendation_type")
            
            thresholds = self.config.get("rebalancing_thresholds", {}).get(strategy_id, {})
            suggest_threshold = thresholds.get("suggest", 5)
            force_threshold = thresholds.get("force", 10)
            
            if rec_type == "suggested" and max_drift >= force_threshold:
                issues.append(ValidationIssue(
                    code="G3-REB-001",
                    severity=ValidationSeverity.WARNING,
                    message=f"Drift {max_drift}% exceeds force threshold but only 'suggested'",
                    field="recommendation_type",
                    actual_value=rec_type,
                    expected_value="strong",
                    remediation="Upgrade to strong recommendation"
                ))
            
            if rec_type == "strong" and max_drift < suggest_threshold:
                issues.append(ValidationIssue(
                    code="G3-REB-002",
                    severity=ValidationSeverity.WARNING,
                    message=f"Drift {max_drift}% below suggest threshold but 'strong'",
                    field="recommendation_type",
                    actual_value=rec_type,
                    expected_value="none or suggested",
                    remediation="Review recommendation type"
                ))
            
            # diBoaS principle: user action always required
            if not rec.get("user_action_required", True):
                issues.append(ValidationIssue(
                    code="G3-REB-003",
                    severity=ValidationSeverity.ERROR,
                    message="Rebalance recommendation with auto-execution",
                    field="user_action_required",
                    actual_value=False,
                    expected_value=True,
                    remediation="diBoaS NEVER auto-rebalances without user consent"
                ))
        
        return issues
```

---

## 6. Gate 4: Presentation Validation

### 6.1 Purpose

Gate 4 validates final user-facing content before delivery, ensuring legal compliance, appropriate tone, and correct personalization.

**Owner:** CLO Board (legal), CMO Board (tone)  
**Input:** Formatted messages ready for delivery  
**Output:** Validated content or rejection

### 6.2 Validation Categories

| Category | What It Checks | Owner |
|----------|----------------|-------|
| Disclaimer Presence | Required disclaimers included | CLO |
| Prohibited Terms | No "guaranteed", "risk-free", etc. | CLO |
| Claims Validation | Return claims are QR-approved | CLO/QR |
| Jurisdiction Compliance | Content appropriate for user's region | CLO |
| Tone Appropriateness | Crisis messages not casual | CMO |
| Personalization | Placeholders are filled | CMO |
| Length Limits | SMS/email within limits | CMO |

### 6.3 Implementation

```python
class Gate4PresentationValidation(ValidationGate):
    """Gate 4: Presentation Validation (CLO + CMO)"""
    
    def _get_gate_name(self) -> str:
        return "gate_4"
    
    def validate(self, data: dict) -> ValidationResult:
        """Validate presentation/message content."""
        start_time = datetime.datetime.utcnow()
        issues = []
        
        messages = data.get("messages", [])
        
        for message in messages:
            # CLO validations
            issues.extend(self._validate_disclaimers(message))
            issues.extend(self._validate_prohibited_terms(message))
            issues.extend(self._validate_claims(message))
            issues.extend(self._validate_jurisdiction_compliance(message))
            
            # CMO validations
            issues.extend(self._validate_tone(message))
            issues.extend(self._validate_personalization(message))
            issues.extend(self._validate_length_limits(message))
        
        # Determine status
        errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
        status = ValidationStatus.FAIL if errors else (
            ValidationStatus.WARN if issues else ValidationStatus.PASS
        )
        
        return self._create_result(
            status=status,
            issues=issues,
            metadata={
                "messages_validated": len(messages)
            },
            start_time=start_time
        )
    
    # --- CLO Validations ---
    
    def _validate_disclaimers(self, message: dict) -> List[ValidationIssue]:
        """Validate required disclaimers are present."""
        issues = []
        content = message.get("body", "")
        jurisdiction = message.get("user_jurisdiction", "unknown")
        
        REQUIRED_DISCLAIMERS = {
            "EU": [
                "Past performance does not guarantee future results",
                "Your capital is at risk"
            ],
            "US": [
                "Not financial advice",
                "Past performance does not guarantee future results",
                "Consult a licensed financial advisor"
            ],
            "BR": [
                "Rentabilidade passada nÃ£o Ã© garantia de rentabilidade futura",
                "Investimentos envolvem riscos"
            ],
            "default": [
                "Past performance does not guarantee future results"
            ]
        }
        
        required = REQUIRED_DISCLAIMERS.get(jurisdiction, REQUIRED_DISCLAIMERS["default"])
        
        if self._contains_financial_claims(content):
            for disclaimer in required:
                if not self._disclaimer_present(content, disclaimer):
                    issues.append(ValidationIssue(
                        code="G4-DIS-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"Missing required disclaimer for {jurisdiction}",
                        field="body",
                        actual_value=None,
                        expected_value=disclaimer,
                        remediation=f"Add disclaimer: '{disclaimer}'"
                    ))
        
        return issues
    
    def _validate_prohibited_terms(self, message: dict) -> List[ValidationIssue]:
        """Validate no prohibited terms in content."""
        issues = []
        content = message.get("body", "").lower()
        
        PROHIBITED_TERMS = [
            ("guaranteed", "No return is guaranteed"),
            ("risk-free", "All investments carry risk"),
            ("certain return", "Returns are not certain"),
            ("cannot lose", "Losses are possible"),
            ("100% safe", "No investment is 100% safe"),
            ("no risk", "All investments carry some risk"),
            ("assured profit", "Profits are not assured"),
            ("sure thing", "No investment is a sure thing"),
            ("always wins", "Past performance doesn't guarantee future results"),
            ("never lose", "Losses are possible"),
        ]
        
        for term, reason in PROHIBITED_TERMS:
            if term in content:
                issues.append(ValidationIssue(
                    code="G4-PRO-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Prohibited term detected: '{term}'",
                    field="body",
                    actual_value=term,
                    expected_value=f"Remove or rephrase. {reason}",
                    remediation=f"Remove '{term}' from message"
                ))
        
        return issues
    
    def _validate_claims(self, message: dict) -> List[ValidationIssue]:
        """Validate return/performance claims are QR-approved."""
        issues = []
        content = message.get("body", "")
        
        import re
        
        claims = []
        
        # Percentage returns
        pct_pattern = r'(\d+\.?\d*)\s*%\s*(return|apy|yield|gain|growth)'
        for match in re.finditer(pct_pattern, content, re.IGNORECASE):
            claims.append({
                "type": "percentage_return",
                "value": match.group(1),
                "context": match.group(0)
            })
        
        # Outperformance claims
        outperform_pattern = r'(beat|outperform|better than|exceed)\s+(S&P|market|benchmark|inflation)'
        for match in re.finditer(outperform_pattern, content, re.IGNORECASE):
            claims.append({
                "type": "outperformance",
                "value": match.group(2),
                "context": match.group(0)
            })
        
        approved_claims = self._load_qr_approved_claims()
        
        for claim in claims:
            claim_key = f"{claim['type']}:{claim['value']}"
            if claim_key not in approved_claims:
                issues.append(ValidationIssue(
                    code="G4-CLM-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Unapproved claim: '{claim['context']}'",
                    field="body",
                    actual_value=claim["context"],
                    expected_value="QR Board approved claim",
                    remediation="Submit claim to QR Board for validation or remove"
                ))
        
        return issues
    
    def _validate_jurisdiction_compliance(self, message: dict) -> List[ValidationIssue]:
        """Validate content appropriate for user's jurisdiction."""
        issues = []
        content = message.get("body", "")
        jurisdiction = message.get("user_jurisdiction")
        
        import re
        
        if jurisdiction == "US":
            advice_patterns = [
                r'you should (buy|sell|invest)',
                r'I recommend (buying|selling|investing)',
                r'best investment for you',
            ]
            
            for pattern in advice_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        code="G4-JUR-001",
                        severity=ValidationSeverity.ERROR,
                        message="Direct investment advice not permitted for US users",
                        field="body",
                        actual_value=pattern,
                        expected_value="Educational/informational content only",
                        remediation="Rephrase as educational information, not advice"
                    ))
        
        if jurisdiction == "EU":
            misleading_patterns = [
                r'easy money',
                r'get rich',
                r'passive income guaranteed',
            ]
            
            for pattern in misleading_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        code="G4-JUR-002",
                        severity=ValidationSeverity.ERROR,
                        message="Potentially misleading content for EU (MiCA)",
                        field="body",
                        actual_value=pattern,
                        expected_value="Fair, clear, and not misleading",
                        remediation="Rephrase to be more balanced"
                    ))
        
        return issues
    
    # --- CMO Validations ---
    
    def _validate_tone(self, message: dict) -> List[ValidationIssue]:
        """Validate tone appropriate for message type."""
        issues = []
        content = message.get("body", "")
        alert_level = message.get("alert_level")
        priority = message.get("priority")
        
        if priority in ["P0", "P1"] or alert_level in ["warning", "critical"]:
            CASUAL_ELEMENTS = ["ðŸ˜€", "ðŸ˜Ž", "ðŸš€", "ðŸŽ‰", "ðŸ’ª", "ðŸ”¥", "lol", "haha", "awesome", "amazing"]
            
            for element in CASUAL_ELEMENTS:
                if element in content:
                    issues.append(ValidationIssue(
                        code="G4-TON-001",
                        severity=ValidationSeverity.WARNING,
                        message=f"Casual element in crisis message: '{element}'",
                        field="body",
                        actual_value=element,
                        expected_value="Professional tone",
                        remediation="Remove casual elements from crisis communications"
                    ))
        
        if alert_level == "info":
            negative_phrases = ["disaster", "terrible", "awful", "horrible"]
            for phrase in negative_phrases:
                if phrase in content.lower():
                    issues.append(ValidationIssue(
                        code="G4-TON-002",
                        severity=ValidationSeverity.WARNING,
                        message=f"Overly negative language in informational message",
                        field="body",
                        actual_value=phrase,
                        expected_value="Balanced, professional tone",
                        remediation="Use more measured language"
                    ))
        
        return issues
    
    def _validate_personalization(self, message: dict) -> List[ValidationIssue]:
        """Validate personalization placeholders are filled."""
        issues = []
        content = message.get("body", "")
        subject = message.get("subject", "")
        
        import re
        
        PLACEHOLDER_PATTERNS = [
            r'\{\{(\w+)\}\}',
            r'\{(\w+)\}',
            r'\[(\w+)\]',
            r'<(\w+)>',
        ]
        
        for pattern in PLACEHOLDER_PATTERNS:
            for text in [content, subject]:
                matches = re.findall(pattern, text)
                for match in matches:
                    issues.append(ValidationIssue(
                        code="G4-PER-001",
                        severity=ValidationSeverity.ERROR,
                        message=f"Unfilled placeholder: {match}",
                        field="body" if text == content else "subject",
                        actual_value=match,
                        expected_value="Filled value",
                        remediation=f"Fill placeholder '{match}' with actual value"
                    ))
        
        return issues
    
    def _validate_length_limits(self, message: dict) -> List[ValidationIssue]:
        """Validate message within length limits."""
        issues = []
        content = message.get("body", "")
        subject = message.get("subject", "")
        channel = message.get("channel")
        
        LENGTH_LIMITS = {
            "sms": {"body": 160, "subject": None},
            "push": {"body": 240, "subject": 50},
            "email": {"body": 50000, "subject": 100},
            "in_app": {"body": 5000, "subject": 100},
        }
        
        limits = LENGTH_LIMITS.get(channel, LENGTH_LIMITS["email"])
        
        if limits["body"] and len(content) > limits["body"]:
            issues.append(ValidationIssue(
                code="G4-LEN-001",
                severity=ValidationSeverity.ERROR if channel == "sms" else ValidationSeverity.WARNING,
                message=f"Message body exceeds {channel} limit",
                field="body",
                actual_value=len(content),
                expected_value=f"<= {limits['body']} characters",
                remediation=f"Shorten message to {limits['body']} characters"
            ))
        
        if limits["subject"] and subject and len(subject) > limits["subject"]:
            issues.append(ValidationIssue(
                code="G4-LEN-002",
                severity=ValidationSeverity.WARNING,
                message=f"Subject exceeds {channel} limit",
                field="subject",
                actual_value=len(subject),
                expected_value=f"<= {limits['subject']} characters",
                remediation=f"Shorten subject to {limits['subject']} characters"
            ))
        
        return issues
    
    # --- Helper Methods ---
    
    def _contains_financial_claims(self, content: str) -> bool:
        """Check if content contains financial claims requiring disclaimers."""
        import re
        patterns = [
            r'\d+\.?\d*\s*%',
            r'\$\d+',
            r'return|yield|apy|gain|profit|earn',
        ]
        return any(re.search(p, content, re.IGNORECASE) for p in patterns)
    
    def _disclaimer_present(self, content: str, disclaimer: str) -> bool:
        """Check if disclaimer or close variant is present."""
        if disclaimer.lower() in content.lower():
            return True
        
        key_phrases = disclaimer.lower().split()[:4]
        return all(phrase in content.lower() for phrase in key_phrases)
    
    def _load_qr_approved_claims(self) -> set:
        """Load set of QR Board approved claims."""
        # Implementation: Load from database or config
        return set()
```

---

## 7. Gate Orchestration

### 7.1 Pipeline Orchestrator

```python
class PipelineOrchestrator:
    """Orchestrates data flow through all validation gates."""
    
    def __init__(self, config: dict):
        self.gate1 = Gate1RawDataValidation(config.get("gate1", {}))
        self.gate2 = Gate2AnalyticsValidation(config.get("gate2", {}))
        self.gate3 = Gate3IntelligenceValidation(config.get("gate3", {}))
        self.gate4 = Gate4PresentationValidation(config.get("gate4", {}))
        self.notification_service = NotificationService()
    
    def run_pipeline(self, raw_data: dict) -> PipelineResult:
        """Run full pipeline with all gates."""
        
        results = []
        
        # Gate 1: Raw Data Validation
        gate1_result = self.gate1.validate(raw_data)
        results.append(gate1_result)
        
        if not gate1_result.passed:
            self._handle_failure("gate_1", gate1_result)
            return PipelineResult(
                completed=False,
                blocked_at="gate_1",
                gate_results=results,
                output=None
            )
        
        # Layer 3: Analytics (external call)
        analytics_output = self._run_analytics(raw_data)
        
        # Gate 2: Analytics Validation
        gate2_result = self.gate2.validate(analytics_output)
        results.append(gate2_result)
        
        if not gate2_result.passed:
            self._handle_failure("gate_2", gate2_result)
            return PipelineResult(
                completed=False,
                blocked_at="gate_2",
                gate_results=results,
                output=None
            )
        
        # Layer 4: Intelligence (external call)
        intelligence_output = self._run_intelligence(analytics_output)
        
        # Gate 3: Intelligence Validation
        gate3_result = self.gate3.validate(intelligence_output)
        results.append(gate3_result)
        
        if not gate3_result.passed:
            self._handle_failure("gate_3", gate3_result)
            return PipelineResult(
                completed=False,
                blocked_at="gate_3",
                gate_results=results,
                output=None
            )
        
        # Layer 5: Presentation (external call)
        presentation_output = self._run_presentation(intelligence_output)
        
        # Gate 4: Presentation Validation
        gate4_result = self.gate4.validate(presentation_output)
        results.append(gate4_result)
        
        if not gate4_result.passed:
            self._handle_failure("gate_4", gate4_result)
            return PipelineResult(
                completed=False,
                blocked_at="gate_4",
                gate_results=results,
                output=None
            )
        
        # All gates passed
        return PipelineResult(
            completed=True,
            blocked_at=None,
            gate_results=results,
            output=presentation_output
        )
    
    def _handle_failure(self, gate: str, result: ValidationResult):
        """Handle gate failure."""
        board_map = {
            "gate_1": "rakia",
            "gate_2": "qr_board",
            "gate_3": "strategy_board",
            "gate_4": "clo_board"
        }
        
        board = board_map.get(gate)
        
        self.notification_service.notify_board(
            board=board,
            message=f"Pipeline blocked at {gate}",
            errors=result.errors,
            severity="high" if result.errors else "medium"
        )
        
        self._log_failure(gate, result)
    
    def _run_analytics(self, data: dict) -> dict:
        """Placeholder for analytics engine call."""
        pass
    
    def _run_intelligence(self, data: dict) -> dict:
        """Placeholder for intelligence engine call."""
        pass
    
    def _run_presentation(self, data: dict) -> dict:
        """Placeholder for presentation engine call."""
        pass
    
    def _log_failure(self, gate: str, result: ValidationResult):
        """Log failure for audit trail."""
        pass


@dataclass
class PipelineResult:
    completed: bool
    blocked_at: Optional[str]
    gate_results: List[ValidationResult]
    output: Optional[dict]
```

---

## 8. Failure Handling

### 8.1 Failure Types and Actions

| Failure Type | Action | Notification | Retry? |
|--------------|--------|--------------|--------|
| Hard Error (blocking) | Stop pipeline | Immediate to board | No |
| Soft Error (warning) | Continue with flag | Daily digest | N/A |
| Transient Error | Retry with backoff | After max retries | Yes |

### 8.2 Retry Logic

```python
class RetryHandler:
    """Handle transient failures with retry logic."""
    
    MAX_RETRIES = 3
    BACKOFF_SECONDS = [5, 30, 120]
    
    def __init__(self, gate: ValidationGate):
        self.gate = gate
    
    async def validate_with_retry(self, data: dict) -> ValidationResult:
        """Attempt validation with retries for transient failures."""
        
        last_result = None
        
        for attempt in range(self.MAX_RETRIES):
            result = self.gate.validate(data)
            last_result = result
            
            if result.passed:
                return result
            
            transient_errors = [
                e for e in result.errors 
                if self._is_transient(e)
            ]
            
            if not transient_errors:
                return result
            
            if attempt < self.MAX_RETRIES - 1:
                await asyncio.sleep(self.BACKOFF_SECONDS[attempt])
        
        return last_result
    
    def _is_transient(self, error: ValidationIssue) -> bool:
        """Determine if error is transient (worth retrying)."""
        TRANSIENT_CODES = ["G1-API-001", "G1-NET-001", "G1-TIMEOUT"]
        return error.code in TRANSIENT_CODES
```

---

## 9. Logging & Audit

### 9.1 Audit Log Structure

```python
@dataclass
class AuditLog:
    log_id: str
    timestamp: datetime.datetime
    gate: str
    pipeline_run_id: str
    input_hash: str
    result: ValidationResult
    duration_ms: int
    operator: str
    
    def to_dict(self) -> dict:
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp.isoformat(),
            "gate": self.gate,
            "pipeline_run_id": self.pipeline_run_id,
            "input_hash": self.input_hash,
            "status": self.result.status.value,
            "error_count": len(self.result.errors),
            "warning_count": len(self.result.warnings),
            "duration_ms": self.duration_ms,
            "operator": self.operator
        }
```

### 9.2 Retention Policy

| Log Type | Retention | Storage |
|----------|-----------|---------|
| Pass logs | 90 days | Cold storage |
| Warning logs | 1 year | Warm storage |
| Error logs | 7 years | Hot storage |
| Audit summary | Indefinite | Archive |

---

## 10. Configuration

### 10.1 Gate Configuration Template

```yaml
# config/validation_gates.yaml

gate_1:
  schemas: "config/gate1_schemas.yaml"
  expected_date_range:
    min: "2020-01-01"
  outlier_threshold_std: 4.0
  max_null_percentage: 5.0

gate_2:
  strategies: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  required_metrics:
    - var_95
    - cvar_99
    - sharpe_ratio
    - max_drawdown
    - median_return
    - probability_of_loss
  bounds:
    sharpe_ratio: {min: -5, max: 10}
    var_95: {min: 0, max: 100}
    probability_of_loss: {min: 0, max: 1}
  historical_change_threshold: 0.50

gate_3:
  valid_priorities: [P0, P1, P2, P3]
  max_alerts_per_hour: 10
  rebalancing_thresholds:
    default: {suggest: 5, force: 10}
    
gate_4:
  prohibited_terms:
    - guaranteed
    - risk-free
    - certain return
    - cannot lose
  jurisdictions:
    EU:
      disclaimers:
        - "Past performance does not guarantee future results"
        - "Your capital is at risk"
    US:
      disclaimers:
        - "Not financial advice"
        - "Past performance does not guarantee future results"
    BR:
      disclaimers:
        - "Rentabilidade passada nÃ£o Ã© garantia de rentabilidade futura"
  length_limits:
    sms: {body: 160}
    push: {body: 240, subject: 50}
    email: {body: 50000, subject: 100}
```

---

## 11. API Specifications

### 11.1 Validation Endpoint

```yaml
openapi: 3.0.0
paths:
  /validate/gate/{gate_number}:
    post:
      summary: Run validation gate
      parameters:
        - name: gate_number
          in: path
          required: true
          schema:
            type: integer
            enum: [1, 2, 3, 4]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        200:
          description: Validation complete
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationResult'
        400:
          description: Invalid input
        500:
          description: Validation error

components:
  schemas:
    ValidationResult:
      type: object
      properties:
        gate:
          type: string
        status:
          type: string
          enum: [pass, warn, fail, skip]
        timestamp:
          type: string
          format: date-time
        duration_ms:
          type: integer
        issues:
          type: array
          items:
            $ref: '#/components/schemas/ValidationIssue'
            
    ValidationIssue:
      type: object
      properties:
        code:
          type: string
        severity:
          type: string
          enum: [error, warning, info]
        message:
          type: string
        field:
          type: string
        actual_value:
          type: string
        expected_value:
          type: string
        remediation:
          type: string
```

---

## 12. Database Schema

### 12.1 Validation Results Table

```sql
CREATE TABLE validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_run_id UUID NOT NULL,
    gate VARCHAR(10) NOT NULL,
    status VARCHAR(10) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duration_ms INTEGER,
    error_count INTEGER DEFAULT 0,
    warning_count INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_validation_results_pipeline ON validation_results(pipeline_run_id);
CREATE INDEX idx_validation_results_gate ON validation_results(gate);
CREATE INDEX idx_validation_results_status ON validation_results(status);
CREATE INDEX idx_validation_results_timestamp ON validation_results(timestamp);

CREATE TABLE validation_issues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES validation_results(id),
    code VARCHAR(20) NOT NULL,
    severity VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    field VARCHAR(100),
    actual_value TEXT,
    expected_value TEXT,
    remediation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_validation_issues_result ON validation_issues(result_id);
CREATE INDEX idx_validation_issues_code ON validation_issues(code);
```

---

## 13. Testing Requirements

### 13.1 Unit Test Coverage

| Gate | Minimum Coverage | Critical Paths |
|------|------------------|----------------|
| Gate 1 | 90% | Schema validation, null checks |
| Gate 2 | 95% | Bounds checking, statistical sanity |
| Gate 3 | 90% | Priority validation, deduplication |
| Gate 4 | 95% | Disclaimer presence, prohibited terms |

### 13.2 Test Fixtures

```python
# tests/fixtures/validation_fixtures.py

GATE1_VALID_DATA = {
    "source": "treasury_yields",
    "columns": ["date", "dgs2", "dgs10", "dgs30"],
    "record_count": 100,
    "date_range": {"min": "2024-01-01", "max": "2024-12-31"},
    "detected_types": {
        "date": "date",
        "dgs2": "float",
        "dgs10": "float",
        "dgs30": "float"
    },
    "null_counts": {"date": 0, "dgs2": 0, "dgs10": 0, "dgs30": 0}
}

GATE2_VALID_DATA = {
    "strategies": {
        "1": {
            "var_95": 2.3,
            "cvar_99": 3.1,
            "sharpe_ratio": 1.85,
            "max_drawdown": 5.2,
            "probability_of_loss": 0.03,
            "median_return": 4.1,
            "ci_5th": 2.8,
            "ci_95th": 5.9
        }
    }
}

GATE3_VALID_ALERTS = {
    "alerts": [
        {
            "alert_id": "ALT-001",
            "trigger_id": "MKT-BTC-L3",
            "affected_strategies": [3, 4, 5, 6, 7, 8, 9, 10],
            "priority": "P0",
            "event_type": "btc_price_drop",
            "routing": {
                "escalation": {"escalate_to": "strategy_board"}
            }
        }
    ]
}

GATE4_VALID_MESSAGE = {
    "messages": [
        {
            "body": "Market Alert: BTC has dropped 12% in the last 24 hours. Past performance does not guarantee future results. Your capital is at risk.",
            "channel": "email",
            "user_jurisdiction": "EU",
            "priority": "P0",
            "alert_level": "warning"
        }
    ]
}
```

### 13.3 Integration Test Scenarios

| Scenario | Input | Expected Result |
|----------|-------|-----------------|
| Happy path | Valid data through all gates | Pipeline completes, all gates pass |
| Gate 1 failure | Missing columns | Pipeline blocked at gate_1 |
| Gate 2 failure | NaN in VaR | Pipeline blocked at gate_2 |
| Gate 3 failure | Invalid strategy ID | Pipeline blocked at gate_3 |
| Gate 4 failure | Missing disclaimer | Pipeline blocked at gate_4 |
| Warnings only | Minor issues | Pipeline completes with warnings |

---

## Appendix A: Error Code Reference

| Code | Gate | Description |
|------|------|-------------|
| G1-SCH-001 | 1 | Required column missing |
| G1-TYP-001 | 1 | Type mismatch |
| G1-NUL-001 | 1 | Null in required field |
| G1-RNG-001 | 1 | Value below minimum |
| G1-RNG-002 | 1 | Value above maximum |
| G1-DAT-001 | 1 | Date before expected range |
| G1-DAT-002 | 1 | Future date detected |
| G1-EVT-001 | 1 | Missing known event data |
| G1-CAL-001 | 1 | Calculation mismatch |
| G1-OUT-001 | 1 | Extreme outlier detected |
| G1-FRS-001 | 1 | Data staleness (NEW in v2.0) |
| G2-CMP-001 | 2 | Missing strategy results |
| G2-CMP-002 | 2 | Missing required metric |
| G2-BND-001 | 2 | Metric below minimum bound |
| G2-BND-002 | 2 | Metric above maximum bound |
| G2-STA-001 | 2 | Confidence intervals not ordered |
| G2-STA-002 | 2 | CVaR less than VaR |
| G2-STA-003 | 2 | Risk tier mismatch |
| G2-HIS-001 | 2 | Significant change from previous |
| G2-COH-001 | 2 | Cross-metric incoherence |
| G2-COH-002 | 2 | Max drawdown less than VaR |
| G2-INV-001 | 2 | NaN value detected |
| G2-INV-002 | 2 | Infinite value detected |
| G3-STR-001 | 3 | Invalid strategy ID format |
| G3-STR-002 | 3 | Invalid strategy ID value |
| G3-PRI-001 | 3 | Missing priority |
| G3-PRI-002 | 3 | Invalid priority |
| G3-ESC-001 | 3 | P0 without escalation |
| G3-DUP-001 | 3 | Duplicate alert |
| G3-RAT-001 | 3 | Rate limit exceeded |
| G3-CON-001 | 3 | Invalid consolidation |
| G3-THR-001 | 3 | Threshold logic violation |
| G3-REB-001 | 3 | Recommendation type mismatch |
| G3-REB-002 | 3 | Unnecessary strong recommendation |
| G3-REB-003 | 3 | Auto-execution violation |
| G4-DIS-001 | 4 | Missing disclaimer |
| G4-PRO-001 | 4 | Prohibited term detected |
| G4-CLM-001 | 4 | Unapproved claim |
| G4-JUR-001 | 4 | US jurisdiction violation |
| G4-JUR-002 | 4 | EU jurisdiction violation |
| G4-TON-001 | 4 | Casual tone in crisis message |
| G4-TON-002 | 4 | Overly negative language |
| G4-PER-001 | 4 | Unfilled placeholder |
| G4-LEN-001 | 4 | Body exceeds length limit |
| G4-LEN-002 | 4 | Subject exceeds length limit |

---

## Appendix B: Related Documents

| Document | Purpose | Owner |
|----------|---------|-------|
| Strategy Board CTO Handoff | Layer 4 Intelligence | Strategy Board |
| QR Board CTO Handoff | Layer 3 Analytics | QR Board |
| Rakia Data Validation Handoff | Layer 1-2 Collection/Validation | Rakia |
| Adelaide System | Layer 5 Presentation | CMO Board |
| CLO Board Guidelines | Legal compliance rules | CLO Board |

---

## Appendix C: v2.0 Changes Summary

**GAP-004 Fix: Added 15 Missing CSV Schemas**

The following schemas were added to Section 3.4:

| CSV File | Schema Added |
|----------|--------------|
| real_yields.csv | âœ“ |
| tradfi_benchmark_data.csv | âœ“ |
| commodities.csv | âœ“ |
| credit_spreads.csv | âœ“ |
| rotation_indicators.csv | âœ“ |
| crypto_prices.csv | âœ“ |
| defillama_historical_apy.csv | âœ“ |
| jupiter_jlp_historical_apy.csv | âœ“ |
| jito_historical_apy.csv | âœ“ |
| market_maker_wallet_tracker.csv | âœ“ |
| protocol_treasury_tracker.csv | âœ“ |
| whale_wallet_master_list.csv | âœ“ |
| btc_etf_holdings.csv | âœ“ |
| corporate_btc_holdings.csv | âœ“ |
| institutional_13f.csv | âœ“ |
| sentiment_indicators.csv | âœ“ |
| aaii_sentiment.csv | âœ“ |

**GAP-015 Fix: Weekend/Holiday Handling**

Added Section 3.5 with `FreshnessChecker` class that:
- Calculates effective age excluding weekends and market holidays
- Uses `holidays` library for US market holiday detection
- Added `weekend_holiday_handling` flag to all schema freshness rules
- New error code G1-FRS-001 for staleness detection

---

**Document End**

*Validation Gates v2.0 â€” Ready for CTO Board Implementation*
