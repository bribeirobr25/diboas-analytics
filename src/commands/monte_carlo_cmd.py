"""
Monte Carlo command.
"""

import logging

from src.engines.monte_carlo import MonteCarloEngine, run_monte_carlo
from src.validators.result_validator import ResultValidator, ValidationReport
from src.reporters.csv_reporter import CSVReporter
from src.reporters.json_reporter import JSONReporter
from src.reporters.markdown_reporter import MarkdownReporter
from config.settings import DEFAULT_SIMULATIONS

logger = logging.getLogger(__name__)


def run_monte_carlo_cmd(args):
    """
    Execute Monte Carlo simulation.

    Args:
        args: Parsed command line arguments
    """
    print("Monte Carlo Simulation")
    print("=" * 50)

    n_simulations = args.simulations or DEFAULT_SIMULATIONS
    seed = args.seed or 42

    print(f"Simulations: {n_simulations:,}")
    print(f"Random seed: {seed}")

    if args.strategy:
        print(f"Strategy: {args.strategy}")
    else:
        print("Strategies: All (1-10)")

    print()
    print("Running simulation...")
    print("(This may take a minute)")
    print()

    # Run Monte Carlo
    results, metadata = run_monte_carlo(
        strategy_id=args.strategy,
        n_simulations=n_simulations,
        random_seed=seed
    )

    # Display results
    print("Results:")
    print("-" * 80)
    print(f"{'Strategy':<25} {'Median Return':>15} {'P(Loss)':>10} {'VaR 95%':>15}")
    print("-" * 80)

    for r in results:
        print(f"{r.strategy_name:<25} {r.median_return:>+14.1f}% {r.prob_any_loss:>9.1f}% ${r.var_95:>13,.0f}")

    print("-" * 80)
    print()

    # Run validation
    print("Validating results...")
    validator = ResultValidator()
    all_validations = []

    for r in results:
        validations = validator.validate_monte_carlo_result(r)
        all_validations.extend(validations)

    report = ValidationReport(all_validations)
    print(f"Validation status: {report.status}")

    if report.critical_failures:
        print(f"  Critical failures: {len(report.critical_failures)}")

    if report.warnings:
        print(f"  Warnings: {len(report.warnings)}")

    print()

    # Export results
    print("Exporting results...")

    csv_reporter = CSVReporter()
    json_reporter = JSONReporter()
    md_reporter = MarkdownReporter()

    csv_path = csv_reporter.export_monte_carlo(results)
    json_reporter.export_monte_carlo(results, metadata)
    md_reporter.generate_monte_carlo_report(results)

    print(f"  CSV: {csv_path}")
    print()

    # Summary
    print(f"Duration: {metadata.duration_seconds:.1f} seconds")
    print(f"Run ID: {metadata.run_id}")
    print()
    print("Monte Carlo simulation complete")
