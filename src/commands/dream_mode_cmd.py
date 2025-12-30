"""
Dream Mode export command.
"""

import logging
from pathlib import Path

from src.engines.dream_mode_export import export_dream_mode
from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


def run_dream_mode_export(args):
    """
    Generate Dream Mode data for frontend.

    Args:
        args: Parsed command line arguments
    """
    print("Dream Mode Export")
    print("=" * 50)

    # Check for existing results
    bt_path = OUTPUT_DIR / 'battle_test_results.csv'
    mc_path = OUTPUT_DIR / 'monte_carlo_results.csv'

    if not bt_path.exists():
        print("Warning: No Battle Test results found.")
        print("  Run 'python main.py battle-test' first for accurate data.")
        print()

    if not mc_path.exists():
        print("Warning: No Monte Carlo results found.")
        print("  Run 'python main.py monte-carlo' first for accurate data.")
        print()

    output_path = args.output if hasattr(args, 'output') and args.output else None

    print("Generating Dream Mode data...")
    print()

    # Export
    try:
        result = export_dream_mode(output_path=output_path)

        print("Dream Mode Data Generated:")
        print("-" * 50)
        print(f"Version: {result.version}")
        print(f"Generated: {result.generated_at.isoformat()}")
        print()

        print("Paths:")
        for path_id, metrics in result.paths.items():
            print(f"  {metrics.label}:")
            print(f"    - Avg APY: {metrics.avg_apy}%")
            print(f"    - Max Drawdown: {metrics.max_drawdown}%")
            print(f"    - P(Loss): {metrics.probability_of_loss}%")
            if metrics.warning:
                print(f"    - Warning: {metrics.warning}")

        print()
        print("Projections (1 year, $1000 initial):")
        for path_id, metrics in result.paths.items():
            proj = metrics.projections.get('1_year')
            if proj:
                projected = 1000 * proj.multiplier
                bank = 1000 * proj.bank_multiplier
                print(f"  {metrics.label}: ${projected:,.0f} (Bank: ${bank:,.0f})")

        print()

        output_file = output_path or str(OUTPUT_DIR / 'dream_mode_data.json')
        print(f"Output: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        logger.exception("Dream Mode export failed")
        return

    print()
    print("Dream Mode export complete")
