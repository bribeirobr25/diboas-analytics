"""
Full pipeline command - runs all analytics.
"""

import logging
from datetime import datetime
import time

from src.engines.battle_test import run_battle_test
from src.engines.monte_carlo import run_monte_carlo
from src.engines.dream_mode_export import export_dream_mode
from src.validators.result_validator import ResultValidator, ValidationReport
from src.reporters.csv_reporter import CSVReporter
from src.reporters.json_reporter import JSONReporter
from src.reporters.markdown_reporter import MarkdownReporter
from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


def run_all(args):
    """
    Execute full analytics pipeline.

    Args:
        args: Parsed command line arguments
    """
    print("=" * 60)
    print("diBoaS Analytics - Full Pipeline")
    print("=" * 60)
    print()

    start_time = time.time()
    offline = getattr(args, 'offline', True)

    # Initialize reporters
    csv_reporter = CSVReporter()
    json_reporter = JSONReporter()
    md_reporter = MarkdownReporter()

    # Step 1: Data Collection
    print("Step 1/5: Data Collection")
    print("-" * 40)

    from src.collectors.file_loader import FileLoader
    loader = FileLoader()

    try:
        data = loader.load_all()
        for source, df in data.items():
            if not df.empty:
                print(f"  {source}: {len(df):,} records")
    except Exception as e:
        print(f"  Error loading data: {e}")
        return

    print()

    # Step 2: Battle Test
    print("Step 2/5: Battle Test")
    print("-" * 40)

    try:
        bt_results, bt_metadata = run_battle_test(scenario='A')

        # Quick summary
        for r in bt_results:
            print(f"  {r.strategy_name}: {r.return_pct:+.1f}%")

        # Export
        csv_reporter.export_battle_test(bt_results)
        json_reporter.export_battle_test(bt_results, bt_metadata)
        md_reporter.generate_battle_test_report(bt_results, 'A')

    except Exception as e:
        print(f"  Error in Battle Test: {e}")
        logger.exception("Battle Test failed")
        bt_results = []

    print()

    # Step 3: Monte Carlo
    print("Step 3/5: Monte Carlo Simulation")
    print("-" * 40)

    try:
        mc_results, mc_metadata = run_monte_carlo()

        # Quick summary
        for r in mc_results:
            print(f"  {r.strategy_name}: {r.median_return:+.1f}% median, {r.prob_any_loss:.1f}% P(loss)")

        # Export
        csv_reporter.export_monte_carlo(mc_results)
        json_reporter.export_monte_carlo(mc_results, mc_metadata)
        md_reporter.generate_monte_carlo_report(mc_results)

    except Exception as e:
        print(f"  Error in Monte Carlo: {e}")
        logger.exception("Monte Carlo failed")
        mc_results = []

    print()

    # Step 4: Validation
    print("Step 4/5: Validation")
    print("-" * 40)

    validator = ResultValidator()
    all_validations = []

    for r in bt_results:
        validations = validator.validate_battle_test_result(r, 10000)
        all_validations.extend(validations)

    for r in mc_results:
        validations = validator.validate_monte_carlo_result(r)
        all_validations.extend(validations)

    report = ValidationReport(all_validations)
    print(f"  Status: {report.status}")
    print(f"  Passed: {sum(1 for v in all_validations if v.passed)}/{len(all_validations)}")

    if report.critical_failures:
        print(f"  Critical failures: {len(report.critical_failures)}")

    json_reporter.export_validation(report.to_dict())

    print()

    # Step 5: Dream Mode Export
    print("Step 5/5: Dream Mode Export")
    print("-" * 40)

    try:
        dream_data = export_dream_mode()
        for path_id, metrics in dream_data.paths.items():
            print(f"  {metrics.label}: {metrics.avg_apy:.1f}% APY")

    except Exception as e:
        print(f"  Error in Dream Mode export: {e}")
        logger.exception("Dream Mode export failed")

    print()

    # Summary
    total_time = time.time() - start_time

    print("=" * 60)
    print("Pipeline Complete")
    print("=" * 60)
    print()
    print(f"Total duration: {total_time:.1f} seconds")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    print("Generated files:")
    print("  - battle_test_results.csv")
    print("  - battle_test_results.json")
    print("  - battle_test_report.md")
    print("  - monte_carlo_results.csv")
    print("  - monte_carlo_results.json")
    print("  - monte_carlo_report.md")
    print("  - validation_report.json")
    print("  - dream_mode_data.json")
    print()
    print(f"Validation: {report.status}")
