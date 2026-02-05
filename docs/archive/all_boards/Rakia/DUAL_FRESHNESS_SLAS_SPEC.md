# Dual Freshness SLAs Implementation Specification

**Document:** DUAL_FRESHNESS_SLAS_SPEC.md  
**Created:** February 4, 2026  
**Author:** Rakia Board  
**Priority:** P0 (Pre-Launch)  
**Effort:** 0.5 day

---

## 1. OVERVIEW

### 1.1 Problem Statement

Currently, Gate 1 freshness checking uses a single SLA per file (defined in `gate1_schema_definitions.py`). However, Adelaide has two different editions with different freshness requirements:

| Edition | Purpose | Freshness Requirement |
|---------|---------|----------------------|
| **Adelaide Pulse** | Daily market update | 4 hours for critical data |
| **Adelaide Weekly** | Comprehensive analysis | 24 hours standard |

### 1.2 Solution

Implement dual SLA checking that validates data freshness against the appropriate threshold based on which Adelaide edition is being generated.

---

## 2. IMPLEMENTATION SPECIFICATION

### 2.1 New Configuration: `config/freshness_slas.py`

```python
"""
Freshness SLA definitions for Adelaide editions.

Adelaide Pulse (daily) requires tighter SLAs for real-time market data.
Adelaide Weekly allows standard 24h SLAs for most data.
"""

from typing import Dict

# SLA values in hours
FRESHNESS_SLAS: Dict[str, Dict[str, int]] = {
    
    # Adelaide Pulse (Daily) - Tighter SLAs
    "pulse": {
        # Critical real-time data (4h SLA)
        "crypto_prices.csv": 4,
        "sentiment_indicators.csv": 4,
        "tradfi_benchmark_data.csv": 4,
        
        # DeFi data (8h SLA - updates less frequently)
        "defillama_historical_apy.csv": 8,
        "jito_historical_apy.csv": 8,
        "jupiter_jlp_historical_apy.csv": 8,
        
        # Macro data (24h SLA - daily updates OK)
        "treasury_yields.csv": 24,
        "real_yields.csv": 24,
        "credit_spreads.csv": 24,
        "commodities.csv": 24,
        "macro_indicators.csv": 24,
        "rotation_indicators.csv": 24,
        
        # Wallet data (168h SLA - weekly updates OK)
        "estate_wallet_tracker.csv": 168,
        "whale_wallet_master_list.csv": 168,
        "market_maker_wallet_tracker.csv": 168,
        "protocol_treasury_tracker.csv": 168,
        
        # Institutional data (168h+ SLA)
        "btc_etf_holdings.csv": 168,
        "corporate_btc_holdings.csv": 168,
        "institutional_13f.csv": 720,
        "aaii_sentiment.csv": 168,
    },
    
    # Adelaide Weekly - Standard SLAs
    "weekly": {
        # All data gets standard 24h SLA for weekly edition
        "crypto_prices.csv": 24,
        "sentiment_indicators.csv": 24,
        "tradfi_benchmark_data.csv": 24,
        "defillama_historical_apy.csv": 24,
        "jito_historical_apy.csv": 24,
        "jupiter_jlp_historical_apy.csv": 24,
        "treasury_yields.csv": 24,
        "real_yields.csv": 24,
        "credit_spreads.csv": 24,
        "commodities.csv": 24,
        "macro_indicators.csv": 24,
        "rotation_indicators.csv": 48,
        
        # Wallet data - weekly OK
        "estate_wallet_tracker.csv": 168,
        "whale_wallet_master_list.csv": 168,
        "market_maker_wallet_tracker.csv": 168,
        "protocol_treasury_tracker.csv": 168,
        
        # Institutional data
        "btc_etf_holdings.csv": 168,
        "corporate_btc_holdings.csv": 168,
        "institutional_13f.csv": 720,
        "aaii_sentiment.csv": 168,
    }
}

# Default SLA if file not in config
DEFAULT_SLA_HOURS = 24

# Critical files that MUST pass freshness for Pulse
PULSE_CRITICAL_FILES = [
    "crypto_prices.csv",
    "sentiment_indicators.csv",
]

# Critical files that MUST pass freshness for Weekly
WEEKLY_CRITICAL_FILES = [
    "crypto_prices.csv",
    "defillama_historical_apy.csv",
    "treasury_yields.csv",
]


def get_sla(filename: str, edition: str = "weekly") -> int:
    """
    Get freshness SLA for a file based on edition type.
    
    Args:
        filename: Name of the CSV file
        edition: "pulse" or "weekly"
        
    Returns:
        SLA in hours
    """
    edition_slas = FRESHNESS_SLAS.get(edition, FRESHNESS_SLAS["weekly"])
    return edition_slas.get(filename, DEFAULT_SLA_HOURS)


def get_critical_files(edition: str = "weekly") -> list:
    """
    Get list of critical files that must pass freshness check.
    
    Args:
        edition: "pulse" or "weekly"
        
    Returns:
        List of critical filenames
    """
    if edition == "pulse":
        return PULSE_CRITICAL_FILES
    return WEEKLY_CRITICAL_FILES
```

### 2.2 Updated Freshness Checker: `src/validators/gate1/gate1_freshness_checker.py`

```python
"""
Gate 1 Freshness Checker - Validates data is not stale.

Updated to support dual SLAs for Adelaide Pulse vs Weekly editions.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import os

from src.validators.gate1.gate1_type_validator import Gate1ValidationIssue
from config.freshness_slas import get_sla, get_critical_files, DEFAULT_SLA_HOURS


class Gate1FreshnessChecker:
    """
    Check data freshness based on file modification time.
    
    Supports dual SLAs:
    - Adelaide Pulse (daily): Tighter SLAs for real-time data
    - Adelaide Weekly: Standard 24h SLAs
    """
    
    def __init__(self, edition: str = "weekly"):
        """
        Initialize freshness checker.
        
        Args:
            edition: "pulse" or "weekly" - determines which SLAs to use
        """
        self.edition = edition

    def check(
        self,
        file_path: Path,
        max_age_hours: Optional[int] = None,
        filename: Optional[str] = None
    ) -> List[Gate1ValidationIssue]:
        """
        Check if file is fresher than SLA threshold.
        
        Args:
            file_path: Path to the file
            max_age_hours: Override SLA (if None, uses edition-based SLA)
            filename: File name for error reporting and SLA lookup
            
        Returns:
            List of validation issues (empty if fresh)
        """
        issues = []
        
        if filename is None:
            filename = file_path.name
        
        # Get SLA based on edition if not overridden
        if max_age_hours is None:
            max_age_hours = get_sla(filename, self.edition)

        try:
            mtime = os.path.getmtime(file_path)
            file_age = datetime.utcnow() - datetime.utcfromtimestamp(mtime)
            max_age = timedelta(hours=max_age_hours)

            if file_age > max_age:
                hours_old = file_age.total_seconds() / 3600
                
                # Determine severity based on criticality
                critical_files = get_critical_files(self.edition)
                severity = "error" if filename in critical_files else "warning"
                
                issues.append(Gate1ValidationIssue(
                    code="G1-FRS-001",
                    severity=severity,
                    message=(
                        f"Data is {hours_old:.1f}h old "
                        f"(max: {max_age_hours}h for {self.edition} edition)"
                    ),
                    file=filename,
                    metadata={
                        "age_hours": round(hours_old, 2),
                        "sla_hours": max_age_hours,
                        "edition": self.edition,
                        "is_critical": filename in critical_files
                    }
                ))

        except OSError as e:
            issues.append(Gate1ValidationIssue(
                code="G1-FRS-002",
                severity="warning",
                message=f"Could not check freshness: {e}",
                file=filename
            ))

        return issues

    def check_all(
        self,
        data_dir: Path,
        files: Optional[List[str]] = None
    ) -> dict:
        """
        Check freshness of all data files.
        
        Args:
            data_dir: Directory containing data files
            files: List of filenames to check (None = all CSV files)
            
        Returns:
            Dict with 'passed', 'failed', 'issues' keys
        """
        if files is None:
            files = [f.name for f in data_dir.glob("*.csv")]
        
        all_issues = []
        passed = []
        failed = []
        
        for filename in files:
            file_path = data_dir / filename
            if not file_path.exists():
                continue
                
            issues = self.check(file_path, filename=filename)
            
            if issues:
                # Check if any issue is an error (critical file)
                has_error = any(i.severity == "error" for i in issues)
                if has_error:
                    failed.append(filename)
                else:
                    passed.append(filename)  # Warnings don't fail
                all_issues.extend(issues)
            else:
                passed.append(filename)
        
        return {
            "edition": self.edition,
            "passed": passed,
            "failed": failed,
            "issues": all_issues,
            "summary": {
                "total": len(passed) + len(failed),
                "passed": len(passed),
                "failed": len(failed),
                "status": "PASS" if not failed else "FAIL"
            }
        }

    def get_file_age_hours(self, file_path: Path) -> float:
        """Get file age in hours."""
        try:
            mtime = os.path.getmtime(file_path)
            file_age = datetime.utcnow() - datetime.utcfromtimestamp(mtime)
            return file_age.total_seconds() / 3600
        except OSError:
            return -1

    def is_fresh(
        self,
        file_path: Path,
        max_age_hours: Optional[int] = None
    ) -> bool:
        """Check if file is fresh."""
        if max_age_hours is None:
            max_age_hours = get_sla(file_path.name, self.edition)
            
        age = self.get_file_age_hours(file_path)
        if age < 0:
            return False
        return age <= max_age_hours


# Factory function for easy instantiation
def create_freshness_checker(edition: str = "weekly") -> Gate1FreshnessChecker:
    """
    Create a freshness checker for the specified edition.
    
    Args:
        edition: "pulse" for daily Adelaide Pulse, "weekly" for Adelaide Weekly
        
    Returns:
        Configured Gate1FreshnessChecker instance
    """
    return Gate1FreshnessChecker(edition=edition)
```

### 2.3 CLI Integration: Update `src/commands/validate_gate1_cmd.py`

```python
# Add --edition argument to validate-gate1 command

def add_gate1_args(parser):
    """Add Gate 1 validation arguments."""
    parser.add_argument(
        '--data',
        type=str,
        default='data/',
        help='Path to data directory'
    )
    parser.add_argument(
        '--edition',
        type=str,
        choices=['pulse', 'weekly'],
        default='weekly',
        help='Adelaide edition type for SLA selection (default: weekly)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings (not just errors)'
    )


def run_validate_gate1(args):
    """Run Gate 1 validation with edition-specific SLAs."""
    from src.validators.gate1.gate1_freshness_checker import create_freshness_checker
    
    edition = getattr(args, 'edition', 'weekly')
    checker = create_freshness_checker(edition=edition)
    
    print(f"Gate 1 Validation (Edition: {edition.upper()})")
    print("=" * 50)
    
    results = checker.check_all(Path(args.data))
    
    # ... rest of validation logic
```

### 2.4 Adelaide Generator Integration

```python
# In src/adelaide/generator.py

from src.validators.gate1.gate1_freshness_checker import create_freshness_checker

class AdelaideGenerator:
    
    def validate_data_freshness(self, edition: str = "weekly") -> bool:
        """
        Validate data freshness before generating Adelaide edition.
        
        Args:
            edition: "pulse" or "weekly"
            
        Returns:
            True if all critical data is fresh, False otherwise
        """
        checker = create_freshness_checker(edition=edition)
        results = checker.check_all(self.data_dir)
        
        if results["summary"]["status"] == "FAIL":
            logger.error(
                f"Data freshness check failed for {edition} edition: "
                f"{results['failed']}"
            )
            return False
        
        if results["issues"]:
            logger.warning(
                f"Data freshness warnings for {edition} edition: "
                f"{len(results['issues'])} issues"
            )
        
        return True
    
    def generate(self, edition: str = "weekly", **kwargs):
        """Generate Adelaide edition with freshness validation."""
        
        # Validate freshness before generating
        if not self.validate_data_freshness(edition):
            raise ValueError(
                f"Cannot generate {edition} edition: critical data is stale"
            )
        
        # ... continue with generation
```

---

## 3. USAGE EXAMPLES

### 3.1 Command Line

```bash
# Validate for Adelaide Pulse (daily) - tighter SLAs
python main.py validate-gate1 --data data/ --edition pulse

# Validate for Adelaide Weekly - standard SLAs
python main.py validate-gate1 --data data/ --edition weekly

# Strict mode - fail on warnings too
python main.py validate-gate1 --data data/ --edition pulse --strict
```

### 3.2 Programmatic

```python
from src.validators.gate1.gate1_freshness_checker import create_freshness_checker
from pathlib import Path

# Check for Pulse edition
pulse_checker = create_freshness_checker(edition="pulse")
pulse_results = pulse_checker.check_all(Path("data/"))

if pulse_results["summary"]["status"] == "FAIL":
    print("Cannot generate Adelaide Pulse - data is stale!")
    for issue in pulse_results["issues"]:
        print(f"  - {issue.file}: {issue.message}")

# Check for Weekly edition
weekly_checker = create_freshness_checker(edition="weekly")
weekly_results = weekly_checker.check_all(Path("data/"))
```

---

## 4. VERIFICATION CHECKLIST

| # | Item | Command | Expected | Pass? |
|---|------|---------|----------|-------|
| 1 | `freshness_slas.py` exists | `ls config/freshness_slas.py` | File exists | ☐ |
| 2 | Pulse SLAs defined | `grep "pulse" config/freshness_slas.py` | 4h for crypto_prices | ☐ |
| 3 | Weekly SLAs defined | `grep "weekly" config/freshness_slas.py` | 24h for crypto_prices | ☐ |
| 4 | `--edition` flag works | `python main.py validate-gate1 --help` | Shows edition option | ☐ |
| 5 | Pulse validation runs | `python main.py validate-gate1 --edition pulse` | Completes | ☐ |
| 6 | Weekly validation runs | `python main.py validate-gate1 --edition weekly` | Completes | ☐ |
| 7 | Different results for pulse vs weekly | Compare outputs | Different SLAs applied | ☐ |

---

## 5. MIGRATION NOTES

### 5.1 Backward Compatibility

- Default edition is "weekly" to maintain current behavior
- Existing code calling `Gate1FreshnessChecker()` without edition will use weekly SLAs
- Schema-defined `max_age_hours` can still override edition-based SLAs

### 5.2 Files to Create/Modify

| File | Action |
|------|--------|
| `config/freshness_slas.py` | CREATE |
| `src/validators/gate1/gate1_freshness_checker.py` | MODIFY |
| `src/commands/validate_gate1_cmd.py` | MODIFY |
| `src/adelaide/generator.py` | MODIFY |

---

*Specification created by Rakia Board for dual freshness SLA implementation*
