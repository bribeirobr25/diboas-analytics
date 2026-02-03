"""
Gate Validation Aggregator - Unified pipeline validation report.

Aggregates results from all validation gates (1, 3, 4) into a single report.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class GateResult:
    """Result from a single validation gate."""
    gate_id: str
    name: str
    passed: bool
    error_count: int = 0
    warning_count: int = 0
    items_validated: int = 0
    issues: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "gate_id": self.gate_id,
            "name": self.name,
            "passed": self.passed,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "items_validated": self.items_validated,
            "timestamp": self.timestamp.isoformat(),
            "issues": self.issues,
        }


@dataclass
class AggregatedValidationReport:
    """Aggregated report from all validation gates."""
    gates: List[GateResult] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def all_passed(self) -> bool:
        """Check if all gates passed."""
        return all(g.passed for g in self.gates)

    @property
    def gates_passed(self) -> int:
        """Count of gates that passed."""
        return sum(1 for g in self.gates if g.passed)

    @property
    def gates_failed(self) -> int:
        """Count of gates that failed."""
        return sum(1 for g in self.gates if not g.passed)

    @property
    def total_errors(self) -> int:
        """Total errors across all gates."""
        return sum(g.error_count for g in self.gates)

    @property
    def total_warnings(self) -> int:
        """Total warnings across all gates."""
        return sum(g.warning_count for g in self.gates)

    @property
    def status(self) -> str:
        """Get overall status."""
        if self.gates_failed > 0:
            return "FAILED"
        elif self.total_warnings > 0:
            return "PASS_WITH_WARNINGS"
        else:
            return "PASSED"

    def get_failed_gates(self) -> List[str]:
        """Get list of failed gate IDs."""
        return [g.gate_id for g in self.gates if not g.passed]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "total_gates": len(self.gates),
            "gates_passed": self.gates_passed,
            "gates_failed": self.gates_failed,
            "total_errors": self.total_errors,
            "total_warnings": self.total_warnings,
            "failed_gates": self.get_failed_gates(),
            "timestamp": self.timestamp.isoformat(),
            "gates": [g.to_dict() for g in self.gates],
        }


class GateValidationAggregator:
    """
    Aggregates results from all validation gates.

    Gates:
    - Gate 1: Raw data schema validation
    - Gate 2: Analytics output validation (QR Board)
    - Gate 3: Trigger output validation
    - Gate 4: CLO compliance validation
    """

    def __init__(self):
        self.report = AggregatedValidationReport()

    def add_gate1_result(
        self,
        results: Dict[str, Any]
    ) -> None:
        """
        Add Gate 1 schema validation results.

        Args:
            results: Dict mapping filename to Gate1ValidationResult
        """
        total_files = len(results)
        files_passed = sum(1 for r in results.values() if r.passed)
        total_errors = sum(r.error_count for r in results.values())
        total_warnings = sum(r.warning_count for r in results.values())
        total_rows = sum(r.rows_validated for r in results.values())

        issues = []
        for filename, result in results.items():
            for issue in result.issues:
                issues.append({
                    "file": filename,
                    "code": issue.code,
                    "severity": issue.severity,
                    "message": issue.message,
                })

        self.report.gates.append(GateResult(
            gate_id="Gate1",
            name="Raw Data Schema Validation",
            passed=(total_errors == 0),
            error_count=total_errors,
            warning_count=total_warnings,
            items_validated=total_rows,
            issues=issues[:50],  # Limit to first 50 issues
        ))

    def add_gate2_result(
        self,
        result: Any
    ) -> None:
        """
        Add Gate 2 analytics validation result.

        Args:
            result: Gate2ValidationResult
        """
        issues = []
        for issue in result.issues:
            issues.append({
                "code": issue.code,
                "severity": issue.severity.value,
                "message": issue.message,
                "field": issue.field,
            })

        from src.validators.gate2.gate2_analytics_validator import Gate2ValidationStatus
        passed = result.status != Gate2ValidationStatus.FAIL

        self.report.gates.append(GateResult(
            gate_id="Gate2",
            name="Analytics Output Validation",
            passed=passed,
            error_count=result.error_count,
            warning_count=result.warning_count,
            items_validated=result.strategies_validated,
            issues=issues[:50],
        ))

    def add_gate3_result(
        self,
        result: Any
    ) -> None:
        """
        Add Gate 3 trigger validation result.

        Args:
            result: Gate3ValidationResult
        """
        issues = []
        for issue in result.issues:
            issues.append({
                "trigger_id": issue.trigger_id,
                "code": issue.code,
                "severity": issue.severity,
                "message": issue.message,
            })

        self.report.gates.append(GateResult(
            gate_id="Gate3",
            name="Trigger Output Validation",
            passed=result.passed,
            error_count=result.error_count,
            warning_count=result.warning_count,
            items_validated=result.triggers_validated,
            issues=issues[:50],
        ))

    def add_gate4_result(
        self,
        result: Any
    ) -> None:
        """
        Add Gate 4 CLO compliance validation result.

        Args:
            result: CLOValidationResult
        """
        issues = []
        for issue in result.issues:
            if isinstance(issue, dict):
                issues.append(issue)
            else:
                issues.append({
                    "code": getattr(issue, "code", "CLO"),
                    "severity": str(getattr(issue, "severity", "warning")),
                    "message": getattr(issue, "message", str(issue)),
                })

        # CLO validation doesn't have explicit error/warning counts
        error_count = sum(1 for i in issues if i.get("severity") == "error")
        warning_count = len(issues) - error_count

        from src.validators.clo.clo_validation_types import CLOValidationStatus
        passed = result.status in [CLOValidationStatus.PASS, CLOValidationStatus.WARN]

        self.report.gates.append(GateResult(
            gate_id="Gate4",
            name="CLO Compliance Validation",
            passed=passed,
            error_count=error_count,
            warning_count=warning_count,
            items_validated=1,  # Single content item
            issues=issues[:50],
        ))

    def get_report(self) -> AggregatedValidationReport:
        """Get the aggregated report."""
        return self.report

    def print_summary(self) -> None:
        """Print a summary to console."""
        report = self.report

        print()
        print("=" * 50)
        print("  PIPELINE VALIDATION SUMMARY")
        print("=" * 50)
        print()
        print(f"  Status: {report.status}")
        print(f"  Gates: {report.gates_passed}/{len(report.gates)} passed")
        print(f"  Total Errors: {report.total_errors}")
        print(f"  Total Warnings: {report.total_warnings}")
        print()

        for gate in report.gates:
            status = "PASS" if gate.passed else "FAIL"
            print(f"  [{status}] {gate.gate_id}: {gate.name}")
            if gate.error_count > 0:
                print(f"         Errors: {gate.error_count}")
            if gate.warning_count > 0:
                print(f"         Warnings: {gate.warning_count}")

        print()

        if report.gates_failed > 0:
            print("  Failed gates:", ", ".join(report.get_failed_gates()))
            print()
