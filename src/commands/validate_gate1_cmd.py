"""
Validate Gate 1 command handler - Run schema validation on CSV files.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def run_validate_gate1(args):
    """
    Run Gate 1 schema validation.

    Args:
        args: CLI arguments with:
            - file: Specific file to validate (or all if not specified)
            - data_dir: Data directory path
            - output: Output report file (optional)
    """
    from src.validators.gate1 import (
        Gate1SchemaValidator,
        Gate1ValidationReport,
        list_schemas,
    )

    print("Running Gate 1 Schema Validation")
    print("=" * 40)
    print()

    validator = Gate1SchemaValidator(data_dir=args.data_dir)
    print(f"  Data directory: {args.data_dir}")
    print()

    if args.file:
        # Validate single file
        print(f"  Validating: {args.file}")
        print()

        result = validator.validate_file(args.file)
        _print_file_result(result)

        results = {args.file: result}
    else:
        # Validate all files
        schemas = list_schemas()
        print(f"  Validating {len(schemas)} files...")
        print()

        results = validator.validate_all()

        # Print summary
        passed = sum(1 for r in results.values() if r.passed)
        failed = len(results) - passed

        print(f"  Results: {passed} passed, {failed} failed")
        print()

        # Show failed files
        if failed > 0:
            print("  Failed files:")
            for filename, result in results.items():
                if not result.passed:
                    print(f"    - {filename}")
                    for issue in result.errors[:3]:  # Show first 3 errors
                        print(f"        [{issue.code}] {issue.message}")
                    if len(result.errors) > 3:
                        print(f"        ... and {len(result.errors) - 3} more errors")
            print()

        # Show warnings
        total_warnings = sum(r.warning_count for r in results.values())
        if total_warnings > 0:
            print(f"  Total warnings: {total_warnings}")
            for filename, result in results.items():
                if result.warnings:
                    print(f"    {filename}: {result.warning_count} warning(s)")

    # Generate report
    report = Gate1ValidationReport(results)
    print()
    print("  Summary")
    print("  -------")
    print(f"  Status: {report.status}")
    print(f"  Files validated: {len(results)}")
    print(f"  Files passed: {report.files_passed}")
    print(f"  Files failed: {report.files_failed}")
    print(f"  Total errors: {report.total_errors}")
    print(f"  Total warnings: {report.total_warnings}")
    print(f"  Total rows: {report.total_rows}")

    # Save report if output specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)

        print()
        print(f"  Report saved to: {output_path}")


def _print_file_result(result):
    """Print validation result for a single file."""
    status = "PASS" if result.passed else "FAIL"

    print(f"  Status: {status}")
    print(f"  Rows validated: {result.rows_validated}")
    print(f"  Errors: {result.error_count}")
    print(f"  Warnings: {result.warning_count}")

    if result.issues:
        print()
        print("  Issues:")
        for issue in result.issues:
            severity = issue.severity.upper()
            location = ""
            if issue.row:
                location = f" (row {issue.row})"
            if issue.column:
                location += f" [{issue.column}]"
            print(f"    [{severity}] {issue.code}: {issue.message}{location}")
