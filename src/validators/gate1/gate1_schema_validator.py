"""
Gate 1 Schema Validator - Validates raw CSV data against schemas.

Implements validation rules from VALIDATION_GATES_CTO_HANDOFF_v2.md Section 3.
"""

import csv
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.validators.gate1.gate1_schema_definitions import (
    GATE1_SCHEMAS,
    FileSchema,
    ColumnSchema,
    ColumnType,
    get_schema,
)
from src.validators.gate1.gate1_freshness_checker import Gate1FreshnessChecker
from src.validators.gate1.gate1_type_validator import (
    Gate1TypeValidator,
    Gate1ValidationIssue,
)

logger = logging.getLogger(__name__)


@dataclass
class Gate1ValidationResult:
    """Result of validating a single file."""
    file: str
    passed: bool
    issues: List[Gate1ValidationIssue] = field(default_factory=list)
    rows_validated: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def errors(self) -> List[Gate1ValidationIssue]:
        """Get error-level issues."""
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> List[Gate1ValidationIssue]:
        """Get warning-level issues."""
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def error_count(self) -> int:
        """Count of errors."""
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return len(self.warnings)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "file": self.file,
            "passed": self.passed,
            "rows_validated": self.rows_validated,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "timestamp": self.timestamp.isoformat(),
            "issues": [i.to_dict() for i in self.issues],
        }


class Gate1SchemaValidator:
    """
    Validates CSV files against defined schemas.

    Checks:
    1. Required columns present
    2. Column types correct
    3. Values within bounds
    4. Data freshness
    5. Minimum row count
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.freshness_checker = Gate1FreshnessChecker()
        self.type_validator = Gate1TypeValidator()

    def validate_file(self, filename: str) -> Gate1ValidationResult:
        """
        Validate a single CSV file against its schema.

        Args:
            filename: Name of the file to validate

        Returns:
            Gate1ValidationResult with pass/fail and issues
        """
        schema = get_schema(filename)

        if not schema:
            return Gate1ValidationResult(
                file=filename,
                passed=False,
                issues=[Gate1ValidationIssue(
                    code="G1-SCH-001",
                    severity="error",
                    message=f"No schema defined for {filename}",
                    file=filename
                )]
            )

        file_path = self.data_dir / filename

        if not file_path.exists():
            return Gate1ValidationResult(
                file=filename,
                passed=False,
                issues=[Gate1ValidationIssue(
                    code="G1-FIL-001",
                    severity="error",
                    message=f"File not found: {filename}",
                    file=filename
                )]
            )

        issues = []
        rows_validated = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []

                # Check required columns
                issues.extend(self._validate_columns(schema, headers, filename))

                # Check freshness
                freshness_issues = self.freshness_checker.check(
                    file_path, schema.max_age_hours, filename
                )
                issues.extend(freshness_issues)

                # Validate each row
                for row_num, row in enumerate(reader, start=2):
                    row_issues = self._validate_row(schema, row, row_num, filename)
                    issues.extend(row_issues)
                    rows_validated += 1

                # Check minimum rows
                if rows_validated < schema.min_rows:
                    issues.append(Gate1ValidationIssue(
                        code="G1-ROW-001",
                        severity="error",
                        message=f"Insufficient rows: {rows_validated} < {schema.min_rows}",
                        file=filename
                    ))

        except Exception as e:
            logger.error(f"Error validating {filename}: {e}")
            issues.append(Gate1ValidationIssue(
                code="G1-ERR-001",
                severity="error",
                message=f"Validation error: {str(e)}",
                file=filename
            ))

        has_errors = any(i.severity == "error" for i in issues)

        return Gate1ValidationResult(
            file=filename,
            passed=not has_errors,
            issues=issues,
            rows_validated=rows_validated
        )

    def validate_all(self) -> Dict[str, Gate1ValidationResult]:
        """
        Validate all files with defined schemas.

        Returns:
            Dict mapping filename to validation result
        """
        results = {}

        for filename in GATE1_SCHEMAS.keys():
            results[filename] = self.validate_file(filename)

        return results

    def _validate_columns(
        self,
        schema: FileSchema,
        headers: List[str],
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Check that all required columns are present."""
        issues = []

        for col_schema in schema.columns:
            if col_schema.required and col_schema.name not in headers:
                issues.append(Gate1ValidationIssue(
                    code="G1-COL-001",
                    severity="error",
                    message=f"Missing required column: {col_schema.name}",
                    file=filename,
                    column=col_schema.name
                ))

        return issues

    def _validate_row(
        self,
        schema: FileSchema,
        row: Dict[str, str],
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate a single row against schema."""
        issues = []

        for col_schema in schema.columns:
            if col_schema.name not in row:
                continue

            value = row[col_schema.name]

            # Type validation
            type_issues = self.type_validator.validate(
                value, col_schema, row_num, filename
            )
            issues.extend(type_issues)

            # Bounds validation (if type is valid)
            if not type_issues:
                bounds_issues = self._validate_bounds(
                    value, col_schema, row_num, filename
                )
                issues.extend(bounds_issues)

        return issues

    def _validate_bounds(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate value is within bounds."""
        issues = []

        if col_schema.type in [ColumnType.FLOAT, ColumnType.INTEGER]:
            try:
                num_value = float(value)

                if col_schema.min_value is not None and num_value < col_schema.min_value:
                    issues.append(Gate1ValidationIssue(
                        code="G1-BND-001",
                        severity="warning",
                        message=f"Value {num_value} below minimum {col_schema.min_value}",
                        file=filename,
                        column=col_schema.name,
                        row=row_num,
                        value=num_value
                    ))

                if col_schema.max_value is not None and num_value > col_schema.max_value:
                    issues.append(Gate1ValidationIssue(
                        code="G1-BND-002",
                        severity="warning",
                        message=f"Value {num_value} above maximum {col_schema.max_value}",
                        file=filename,
                        column=col_schema.name,
                        row=row_num,
                        value=num_value
                    ))
            except ValueError:
                pass  # Type validation will catch this

        return issues


class Gate1ValidationReport:
    """Generate validation report from results."""

    def __init__(self, results: Dict[str, Gate1ValidationResult]):
        self.results = results

    @property
    def all_passed(self) -> bool:
        """Check if all files passed validation."""
        return all(r.passed for r in self.results.values())

    @property
    def files_passed(self) -> int:
        """Count of files that passed."""
        return sum(1 for r in self.results.values() if r.passed)

    @property
    def files_failed(self) -> int:
        """Count of files that failed."""
        return sum(1 for r in self.results.values() if not r.passed)

    @property
    def total_errors(self) -> int:
        """Total error count across all files."""
        return sum(r.error_count for r in self.results.values())

    @property
    def total_warnings(self) -> int:
        """Total warning count across all files."""
        return sum(r.warning_count for r in self.results.values())

    @property
    def total_rows(self) -> int:
        """Total rows validated across all files."""
        return sum(r.rows_validated for r in self.results.values())

    @property
    def status(self) -> str:
        """Get overall status."""
        if self.files_failed > 0:
            return "FAILED"
        elif self.total_warnings > 0:
            return "PASS_WITH_WARNINGS"
        else:
            return "PASSED"

    def get_failed_files(self) -> List[str]:
        """Get list of failed file names."""
        return [f for f, r in self.results.items() if not r.passed]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "total_files": len(self.results),
            "files_passed": self.files_passed,
            "files_failed": self.files_failed,
            "total_errors": self.total_errors,
            "total_warnings": self.total_warnings,
            "total_rows_validated": self.total_rows,
            "failed_files": self.get_failed_files(),
            "results": {f: r.to_dict() for f, r in self.results.items()},
        }
