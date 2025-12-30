"""
Battle Test command.
"""

import logging
from datetime import datetime

from src.engines.battle_test import BattleTestEngine, SCENARIOS, run_battle_test
from src.validators.result_validator import ResultValidator, ValidationReport
from src.reporters.csv_reporter import CSVReporter
from src.reporters.json_reporter import JSONReporter
from src.reporters.markdown_reporter import MarkdownReporter

logger = logging.getLogger(__name__)


def run_battle_test_cmd(args):
    """
    Execute Battle Test simulation.

    Args:
        args: Parsed command line arguments
    """
    print("Battle Test - Historical Backtesting")
    print("=" * 50)

    # Parse dates
    start_date = None
    end_date = None
    if args.start_date:
        from src.utils.dates import parse_date
        start_date = parse_date(args.start_date)
    if args.end_date:
        from src.utils.dates import parse_date
        end_date = parse_date(args.end_date)

    # Determine scenario
    scenario = args.scenario or 'A'
    print(f"Scenario: {scenario} - {SCENARIOS[scenario]['name']}")

    if args.strategy:
        print(f"Strategy: {args.strategy}")
    else:
        print("Strategies: All (1-10)")

    print()
    print("Running simulation...")
    print()

    # Run Battle Test
    results, metadata = run_battle_test(
        strategy_id=args.strategy,
        scenario=scenario,
        start_date=start_date,
        end_date=end_date
    )

    # Display results
    print("Results:")
    print("-" * 70)
    print(f"{'Strategy':<25} {'Return':>10} {'Max DD':>10} {'Final Value':>15}")
    print("-" * 70)

    for r in results:
        print(f"{r.strategy_name:<25} {r.return_pct:>+9.1f}% {r.max_drawdown_pct:>9.1f}% ${r.final_value:>13,.0f}")

    print("-" * 70)
    print()

    # Run validation
    print("Validating results...")
    validator = ResultValidator()
    all_validations = []

    for r in results:
        scenario_config = SCENARIOS[scenario]
        if scenario == 'C':
            initial = scenario_config['minimums'][r.strategy_id]['initial']
        else:
            initial = scenario_config['initial_deposit']

        validations = validator.validate_battle_test_result(r, initial)
        all_validations.extend(validations)

    report = ValidationReport(all_validations)
    print(f"Validation status: {report.status}")

    if report.critical_failures:
        print(f"  Critical failures: {len(report.critical_failures)}")
        for v in report.critical_failures:
            print(f"    - {v.rule_id}: {v.message}")

    if report.warnings:
        print(f"  Warnings: {len(report.warnings)}")

    print()

    # Export results
    print("Exporting results...")

    csv_reporter = CSVReporter()
    json_reporter = JSONReporter()
    md_reporter = MarkdownReporter()

    csv_path = csv_reporter.export_battle_test(results)
    json_reporter.export_battle_test(results, metadata)
    md_reporter.generate_battle_test_report(results, scenario)
    json_reporter.export_validation(report.to_dict())

    print(f"  CSV: {csv_path}")
    print()

    # Summary
    print(f"Duration: {metadata.duration_seconds:.1f} seconds")
    print(f"Run ID: {metadata.run_id}")
    print()
    print("Battle Test complete")
