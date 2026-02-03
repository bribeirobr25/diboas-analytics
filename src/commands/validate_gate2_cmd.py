"""CLI command for Gate 2 analytics validation."""
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def run_validate_gate2(
    battle_test_file: str = "outputs/battle_test_results.json",
    monte_carlo_file: str = "outputs/monte_carlo_results.json",
    risk_metrics_file: str = "outputs/risk_metrics.json",
    output_file: Optional[str] = None,
) -> int:
    """
    Run Gate 2 analytics validation.

    Args:
        battle_test_file: Path to Battle Test results JSON
        monte_carlo_file: Path to Monte Carlo results JSON
        risk_metrics_file: Path to risk metrics JSON
        output_file: Optional output file for results

    Returns:
        Exit code (0 for pass, 1 for fail)
    """
    from src.validators.gate2.gate2_analytics_validator import (
        Gate2AnalyticsValidator,
        Gate2ValidationStatus,
    )

    print("\n" + "=" * 50)
    print("  GATE 2: ANALYTICS VALIDATION")
    print("=" * 50 + "\n")

    # Load data files
    try:
        bt_path = Path(battle_test_file)
        mc_path = Path(monte_carlo_file)
        rm_path = Path(risk_metrics_file)

        # Check if files exist
        missing_files = []
        if not bt_path.exists():
            missing_files.append(f"Battle Test: {battle_test_file}")
        if not mc_path.exists():
            missing_files.append(f"Monte Carlo: {monte_carlo_file}")
        if not rm_path.exists():
            missing_files.append(f"Risk Metrics: {risk_metrics_file}")

        if missing_files:
            print("  Missing input files:")
            for f in missing_files:
                print(f"    - {f}")
            print("\n  Run the analytics engines first to generate these files.")
            return 1

        with open(bt_path) as f:
            bt_data = json.load(f)
        with open(mc_path) as f:
            mc_data = json.load(f)
        with open(rm_path) as f:
            rm_data = json.load(f)

        print(f"  Battle Test:  {battle_test_file}")
        print(f"  Monte Carlo:  {monte_carlo_file}")
        print(f"  Risk Metrics: {risk_metrics_file}")
        print()

    except json.JSONDecodeError as e:
        print(f"  ERROR: Invalid JSON in input file: {e}")
        return 1
    except Exception as e:
        print(f"  ERROR: Failed to load input files: {e}")
        return 1

    # Run validation
    validator = Gate2AnalyticsValidator()
    result = validator.validate(bt_data, mc_data, rm_data)

    # Display results
    status_emoji = {
        Gate2ValidationStatus.PASS: "PASS",
        Gate2ValidationStatus.WARN: "WARN",
        Gate2ValidationStatus.FAIL: "FAIL",
    }

    print(f"  Status: {status_emoji.get(result.status, '?')} - {result.status.value.upper()}")
    print(f"  Strategies Validated: {result.strategies_validated}")
    print(f"  Duration: {result.duration_ms}ms")
    print()

    # Show issues
    if result.errors:
        print(f"  Errors ({len(result.errors)}):")
        for issue in result.errors[:10]:
            print(f"    [{issue.code}] {issue.message}")
            if issue.remediation:
                print(f"              Remedy: {issue.remediation}")
        if len(result.errors) > 10:
            print(f"    ... and {len(result.errors) - 10} more errors")
        print()

    if result.warnings:
        print(f"  Warnings ({len(result.warnings)}):")
        for issue in result.warnings[:5]:
            print(f"    [{issue.code}] {issue.message}")
        if len(result.warnings) > 5:
            print(f"    ... and {len(result.warnings) - 5} more warnings")
        print()

    # Save output if requested
    if output_file:
        output_data = {
            "status": result.status.value,
            "strategies_validated": result.strategies_validated,
            "metrics_validated": result.metrics_validated,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
            "duration_ms": result.duration_ms,
            "issues": [
                {
                    "code": i.code,
                    "severity": i.severity.value,
                    "message": i.message,
                    "field": i.field,
                    "actual_value": str(i.actual_value) if i.actual_value else None,
                    "expected_value": str(i.expected_value) if i.expected_value else None,
                    "remediation": i.remediation,
                }
                for i in result.issues
            ],
        }
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"  Results saved to: {output_file}")

    return 0 if result.passed else 1
