"""
Gate 1 Type Validator - Validates column data types.
"""

from datetime import datetime
from typing import List, Any
import re

from src.validators.gate1.gate1_schema_definitions import ColumnSchema, ColumnType


class Gate1ValidationIssue:
    """Validation issue - defined here to avoid circular imports."""

    def __init__(
        self,
        code: str,
        severity: str,
        message: str,
        file: str,
        column: str = None,
        row: int = None,
        value: Any = None
    ):
        self.code = code
        self.severity = severity
        self.message = message
        self.file = file
        self.column = column
        self.row = row
        self.value = value

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "file": self.file,
            "column": self.column,
            "row": self.row,
            "value": self.value,
        }


class Gate1TypeValidator:
    """
    Validates column values against expected types.

    Supports: STRING, FLOAT, INTEGER, DATE, DATETIME, BOOLEAN
    """

    # Date formats to try
    DATE_FORMATS = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
    ]

    DATETIME_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M",
    ]

    BOOLEAN_TRUE = {"true", "1", "yes", "y", "t"}
    BOOLEAN_FALSE = {"false", "0", "no", "n", "f"}

    def validate(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """
        Validate a single value against column schema.

        Args:
            value: String value from CSV
            col_schema: Column schema definition
            row_num: Row number for error reporting
            filename: File name for error reporting

        Returns:
            List of validation issues (empty if valid)
        """
        issues = []

        # Handle empty values
        if value is None or value.strip() == "":
            if col_schema.required:
                issues.append(Gate1ValidationIssue(
                    code="G1-TYP-001",
                    severity="error",
                    message=f"Required value is empty",
                    file=filename,
                    column=col_schema.name,
                    row=row_num,
                    value=value
                ))
            return issues

        value = value.strip()

        # Type-specific validation
        if col_schema.type == ColumnType.STRING:
            pass  # All values are valid strings

        elif col_schema.type == ColumnType.FLOAT:
            issues.extend(self._validate_float(value, col_schema, row_num, filename))

        elif col_schema.type == ColumnType.INTEGER:
            issues.extend(self._validate_integer(value, col_schema, row_num, filename))

        elif col_schema.type == ColumnType.DATE:
            issues.extend(self._validate_date(value, col_schema, row_num, filename))

        elif col_schema.type == ColumnType.DATETIME:
            issues.extend(self._validate_datetime(value, col_schema, row_num, filename))

        elif col_schema.type == ColumnType.BOOLEAN:
            issues.extend(self._validate_boolean(value, col_schema, row_num, filename))

        return issues

    def _validate_float(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate float value."""
        issues = []

        try:
            float(value)
        except ValueError:
            issues.append(Gate1ValidationIssue(
                code="G1-TYP-002",
                severity="error",
                message=f"Expected float, got '{value}'",
                file=filename,
                column=col_schema.name,
                row=row_num,
                value=value
            ))

        return issues

    def _validate_integer(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate integer value."""
        issues = []

        try:
            int(float(value))  # Allow "5.0" as integer
            if "." in value and float(value) != int(float(value)):
                issues.append(Gate1ValidationIssue(
                    code="G1-TYP-003",
                    severity="warning",
                    message=f"Expected integer, got float '{value}'",
                    file=filename,
                    column=col_schema.name,
                    row=row_num,
                    value=value
                ))
        except ValueError:
            issues.append(Gate1ValidationIssue(
                code="G1-TYP-003",
                severity="error",
                message=f"Expected integer, got '{value}'",
                file=filename,
                column=col_schema.name,
                row=row_num,
                value=value
            ))

        return issues

    def _validate_date(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate date value."""
        issues = []

        for fmt in self.DATE_FORMATS:
            try:
                datetime.strptime(value, fmt)
                return issues  # Valid date
            except ValueError:
                continue

        # No format matched
        issues.append(Gate1ValidationIssue(
            code="G1-TYP-004",
            severity="error",
            message=f"Invalid date format: '{value}'",
            file=filename,
            column=col_schema.name,
            row=row_num,
            value=value
        ))

        return issues

    def _validate_datetime(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate datetime value."""
        issues = []

        # Try datetime formats first
        for fmt in self.DATETIME_FORMATS:
            try:
                datetime.strptime(value, fmt)
                return issues
            except ValueError:
                continue

        # Fall back to date formats
        for fmt in self.DATE_FORMATS:
            try:
                datetime.strptime(value, fmt)
                return issues
            except ValueError:
                continue

        issues.append(Gate1ValidationIssue(
            code="G1-TYP-005",
            severity="error",
            message=f"Invalid datetime format: '{value}'",
            file=filename,
            column=col_schema.name,
            row=row_num,
            value=value
        ))

        return issues

    def _validate_boolean(
        self,
        value: str,
        col_schema: ColumnSchema,
        row_num: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """Validate boolean value."""
        issues = []

        if value.lower() not in self.BOOLEAN_TRUE | self.BOOLEAN_FALSE:
            issues.append(Gate1ValidationIssue(
                code="G1-TYP-006",
                severity="error",
                message=f"Invalid boolean: '{value}'",
                file=filename,
                column=col_schema.name,
                row=row_num,
                value=value
            ))

        return issues
