"""Tests for Gate 1 Schema Validator."""

import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta

from src.validators.gate1 import (
    Gate1SchemaValidator,
    Gate1ValidationResult,
    Gate1ValidationReport,
    Gate1TypeValidator,
    Gate1FreshnessChecker,
    ColumnSchema,
    ColumnType,
    FileSchema,
    GATE1_SCHEMAS,
    get_schema,
    list_schemas,
)


class TestGate1SchemaDefinitions:
    """Tests for schema definitions."""

    def test_should_have_20_schemas_defined(self):
        """All 20 CSV schemas are defined."""
        assert len(GATE1_SCHEMAS) == 20

    def test_should_get_schema_by_filename(self):
        """Can retrieve schema by filename."""
        schema = get_schema("treasury_yields.csv")
        assert schema is not None
        assert schema.filename == "treasury_yields.csv"

    def test_should_return_none_for_unknown_schema(self):
        """Returns None for unknown filename."""
        schema = get_schema("unknown_file.csv")
        assert schema is None

    def test_should_list_all_schema_filenames(self):
        """Can list all schema filenames."""
        schemas = list_schemas()
        assert len(schemas) == 20
        assert "treasury_yields.csv" in schemas
        assert "crypto_prices.csv" in schemas

    def test_treasury_yields_schema_has_correct_columns(self):
        """Treasury yields schema has expected columns."""
        schema = get_schema("treasury_yields.csv")
        column_names = [c.name for c in schema.columns]
        assert "date" in column_names
        assert "us_2y" in column_names
        assert "us_10y" in column_names
        assert "us_30y" in column_names


class TestGate1TypeValidator:
    """Tests for type validation."""

    @pytest.fixture
    def validator(self):
        """Create type validator."""
        return Gate1TypeValidator()

    def test_should_pass_valid_float(self, validator):
        """Valid float passes validation."""
        col = ColumnSchema("price", ColumnType.FLOAT)
        issues = validator.validate("123.45", col, 1, "test.csv")
        assert len(issues) == 0

    def test_should_fail_invalid_float(self, validator):
        """Invalid float fails validation."""
        col = ColumnSchema("price", ColumnType.FLOAT)
        issues = validator.validate("not_a_number", col, 1, "test.csv")
        assert len(issues) == 1
        assert issues[0].code == "G1-TYP-002"

    def test_should_pass_valid_integer(self, validator):
        """Valid integer passes validation."""
        col = ColumnSchema("count", ColumnType.INTEGER)
        issues = validator.validate("42", col, 1, "test.csv")
        assert len(issues) == 0

    def test_should_warn_float_for_integer(self, validator):
        """Float value for integer column warns."""
        col = ColumnSchema("count", ColumnType.INTEGER)
        issues = validator.validate("42.5", col, 1, "test.csv")
        assert len(issues) == 1
        assert issues[0].severity == "warning"

    def test_should_pass_valid_date(self, validator):
        """Valid date passes validation."""
        col = ColumnSchema("date", ColumnType.DATE)
        issues = validator.validate("2024-01-15", col, 1, "test.csv")
        assert len(issues) == 0

    def test_should_pass_alternate_date_format(self, validator):
        """Alternate date format passes validation."""
        col = ColumnSchema("date", ColumnType.DATE)
        issues = validator.validate("15/01/2024", col, 1, "test.csv")
        assert len(issues) == 0

    def test_should_fail_invalid_date(self, validator):
        """Invalid date fails validation."""
        col = ColumnSchema("date", ColumnType.DATE)
        issues = validator.validate("not-a-date", col, 1, "test.csv")
        assert len(issues) == 1
        assert issues[0].code == "G1-TYP-004"

    def test_should_pass_valid_boolean(self, validator):
        """Valid boolean passes validation."""
        col = ColumnSchema("active", ColumnType.BOOLEAN)
        for val in ["true", "false", "1", "0", "yes", "no"]:
            issues = validator.validate(val, col, 1, "test.csv")
            assert len(issues) == 0

    def test_should_fail_invalid_boolean(self, validator):
        """Invalid boolean fails validation."""
        col = ColumnSchema("active", ColumnType.BOOLEAN)
        issues = validator.validate("maybe", col, 1, "test.csv")
        assert len(issues) == 1
        assert issues[0].code == "G1-TYP-006"

    def test_should_fail_empty_required_value(self, validator):
        """Empty value for required column fails."""
        col = ColumnSchema("name", ColumnType.STRING, required=True)
        issues = validator.validate("", col, 1, "test.csv")
        assert len(issues) == 1
        assert issues[0].code == "G1-TYP-001"

    def test_should_pass_empty_optional_value(self, validator):
        """Empty value for optional column passes."""
        col = ColumnSchema("name", ColumnType.STRING, required=False)
        issues = validator.validate("", col, 1, "test.csv")
        assert len(issues) == 0


class TestGate1FreshnessChecker:
    """Tests for freshness checking."""

    @pytest.fixture
    def checker(self):
        """Create freshness checker."""
        return Gate1FreshnessChecker()

    def test_should_pass_fresh_file(self, checker):
        """Fresh file passes freshness check."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            f.flush()
            try:
                issues = checker.check(Path(f.name), 24, "test.csv")
                assert len(issues) == 0
            finally:
                os.unlink(f.name)

    def test_should_warn_stale_file(self, checker):
        """Stale file warns."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            f.flush()
            # Make file appear old
            old_time = (datetime.utcnow() - timedelta(hours=48)).timestamp()
            os.utime(f.name, (old_time, old_time))
            try:
                issues = checker.check(Path(f.name), 24, "test.csv")
                assert len(issues) == 1
                assert issues[0].code == "G1-FRS-001"
                assert issues[0].severity == "warning"
            finally:
                os.unlink(f.name)

    def test_should_report_file_age(self, checker):
        """Can get file age in hours."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            f.flush()
            try:
                age = checker.get_file_age_hours(Path(f.name))
                assert age >= 0
                assert age < 1  # Just created
            finally:
                os.unlink(f.name)

    def test_should_check_is_fresh(self, checker):
        """Can check if file is fresh."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            f.flush()
            try:
                assert checker.is_fresh(Path(f.name), 24) is True
            finally:
                os.unlink(f.name)


class TestGate1SchemaValidator:
    """Tests for main schema validator."""

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def validator(self, temp_data_dir):
        """Create validator with temp directory."""
        return Gate1SchemaValidator(data_dir=temp_data_dir)

    def test_should_fail_when_file_not_found(self, validator):
        """Missing file fails validation."""
        result = validator.validate_file("treasury_yields.csv")
        assert result.passed is False
        assert any(i.code == "G1-FIL-001" for i in result.issues)

    def test_should_fail_when_no_schema_defined(self, validator):
        """Unknown file fails validation."""
        result = validator.validate_file("unknown_file.csv")
        assert result.passed is False
        assert any(i.code == "G1-SCH-001" for i in result.issues)

    def test_should_pass_valid_csv(self, temp_data_dir):
        """Valid CSV passes validation."""
        from datetime import date, timedelta

        # Create valid treasury_yields.csv with 100+ valid dates
        csv_content = "date,us_2y,us_10y,us_30y\n"
        start_date = date(2024, 1, 1)
        for i in range(105):
            d = start_date + timedelta(days=i)
            csv_content += f"{d.isoformat()},4.5,4.2,4.8\n"

        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        # May have freshness warning but should pass (no errors)
        assert result.passed is True or all(i.severity == "warning" for i in result.issues)

    def test_should_fail_missing_required_column(self, temp_data_dir):
        """Missing required column fails validation."""
        csv_content = """date,us_2y,us_10y
2024-01-01,4.5,4.2
"""
        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        assert result.passed is False
        assert any(i.code == "G1-COL-001" for i in result.issues)

    def test_should_warn_value_below_minimum(self, temp_data_dir):
        """Value below minimum warns."""
        from datetime import date, timedelta

        # Create CSV with negative yield (below 0 minimum)
        csv_content = "date,us_2y,us_10y,us_30y\n"
        csv_content += "2024-01-01,-1.0,4.2,4.8\n"
        start_date = date(2024, 1, 2)
        for i in range(105):
            d = start_date + timedelta(days=i)
            csv_content += f"{d.isoformat()},4.5,4.2,4.8\n"

        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        assert any(i.code == "G1-BND-001" for i in result.issues)

    def test_should_warn_value_above_maximum(self, temp_data_dir):
        """Value above maximum warns."""
        from datetime import date, timedelta

        # Create CSV with yield above 20 (maximum)
        csv_content = "date,us_2y,us_10y,us_30y\n"
        csv_content += "2024-01-01,25.0,4.2,4.8\n"
        start_date = date(2024, 1, 2)
        for i in range(105):
            d = start_date + timedelta(days=i)
            csv_content += f"{d.isoformat()},4.5,4.2,4.8\n"

        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        assert any(i.code == "G1-BND-002" for i in result.issues)

    def test_should_fail_insufficient_rows(self, temp_data_dir):
        """Insufficient rows fails validation."""
        # Create CSV with only 5 rows (treasury_yields requires 100)
        csv_content = """date,us_2y,us_10y,us_30y
2024-01-01,4.5,4.2,4.8
2024-01-02,4.6,4.3,4.9
2024-01-03,4.5,4.2,4.8
2024-01-04,4.6,4.3,4.9
2024-01-05,4.5,4.2,4.8
"""
        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        assert result.passed is False
        assert any(i.code == "G1-ROW-001" for i in result.issues)

    def test_should_count_errors_and_warnings(self, temp_data_dir):
        """Result counts errors and warnings correctly."""
        csv_content = """date,us_2y,us_10y,us_30y
2024-01-01,-1.0,25.0,4.8
"""
        csv_path = Path(temp_data_dir) / "treasury_yields.csv"
        csv_path.write_text(csv_content)

        validator = Gate1SchemaValidator(data_dir=temp_data_dir)
        result = validator.validate_file("treasury_yields.csv")

        # Should have warnings for bounds and error for insufficient rows
        assert result.warning_count >= 2  # Below min and above max
        assert result.error_count >= 1  # Insufficient rows


class TestGate1ValidationReport:
    """Tests for validation report."""

    def test_should_report_all_passed(self):
        """Report shows all passed status."""
        results = {
            "file1.csv": Gate1ValidationResult(file="file1.csv", passed=True),
            "file2.csv": Gate1ValidationResult(file="file2.csv", passed=True),
        }
        report = Gate1ValidationReport(results)

        assert report.all_passed is True
        assert report.status == "PASSED"
        assert report.files_passed == 2
        assert report.files_failed == 0

    def test_should_report_failures(self):
        """Report shows failures."""
        results = {
            "file1.csv": Gate1ValidationResult(file="file1.csv", passed=True),
            "file2.csv": Gate1ValidationResult(file="file2.csv", passed=False),
        }
        report = Gate1ValidationReport(results)

        assert report.all_passed is False
        assert report.status == "FAILED"
        assert report.files_passed == 1
        assert report.files_failed == 1
        assert "file2.csv" in report.get_failed_files()

    def test_should_convert_to_dict(self):
        """Report converts to dictionary."""
        results = {
            "file1.csv": Gate1ValidationResult(
                file="file1.csv",
                passed=True,
                rows_validated=100
            ),
        }
        report = Gate1ValidationReport(results)
        data = report.to_dict()

        assert data["status"] == "PASSED"
        assert data["total_files"] == 1
        assert data["total_rows_validated"] == 100
