#!/usr/bin/env python3
"""
diBoaS Analytics - Investment Strategy Analysis Tool

A production-grade CLI application for:
- Historical backtesting (Battle Test)
- Monte Carlo simulation
- Protocol monitoring
- Anomaly detection
- Dream Mode data export

Usage:
    python main.py <command> [options]

Commands:
    collect         Collect data from APIs or load bundled data
    battle-test     Run historical backtesting
    monte-carlo     Run Monte Carlo simulation
    monitor         Check protocol health
    anomaly         Run anomaly detection
    dream-mode-export  Generate Dream Mode data for frontend
    all             Run full pipeline

Examples:
    python main.py collect --offline
    python main.py battle-test --scenario A
    python main.py monte-carlo --simulations 5000
    python main.py all
"""

import argparse
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logging import setup_logging


def main():
    """Main entry point for diBoaS Analytics CLI."""

    parser = argparse.ArgumentParser(
        description='diBoaS Analytics - Investment Strategy Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py collect --offline       Load bundled historical data
  python main.py battle-test             Run full Battle Test (all strategies)
  python main.py battle-test --strategy 1  Test only Safe Harbor
  python main.py monte-carlo             Run Monte Carlo simulation
  python main.py monitor                 Check protocol health
  python main.py anomaly                 Run anomaly detection
  python main.py dream-mode-export       Generate Dream Mode data
  python main.py all                     Run full pipeline
        """
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect data from APIs')
    collect_parser.add_argument(
        '--all', action='store_true',
        help='Fetch from all sources'
    )
    collect_parser.add_argument(
        '--offline', action='store_true',
        help='Use bundled data only'
    )
    collect_parser.add_argument(
        '--source',
        choices=['defillama', 'yahoo', 'jupiter'],
        help='Specific source to load'
    )

    # Battle Test command
    bt_parser = subparsers.add_parser('battle-test', help='Run historical backtesting')
    bt_parser.add_argument(
        '--strategy', type=int,
        help='Specific strategy ID (1-10)'
    )
    bt_parser.add_argument(
        '--scenario',
        choices=['A', 'B', 'C'],
        default='A',
        help='Test scenario (A=Felipe, B=Ana, C=Per-strategy minimum)'
    )
    bt_parser.add_argument(
        '--start-date',
        help='Start date (YYYY-MM-DD)'
    )
    bt_parser.add_argument(
        '--end-date',
        help='End date (YYYY-MM-DD)'
    )

    # Monte Carlo command
    mc_parser = subparsers.add_parser('monte-carlo', help='Run Monte Carlo simulation')
    mc_parser.add_argument(
        '--strategy', type=int,
        help='Specific strategy ID (1-10)'
    )
    mc_parser.add_argument(
        '--simulations', type=int, default=5000,
        help='Number of simulations (default: 5000)'
    )
    mc_parser.add_argument(
        '--seed', type=int, default=42,
        help='Random seed for reproducibility (default: 42)'
    )

    # Monitor command
    mon_parser = subparsers.add_parser('monitor', help='Check protocol health')
    mon_parser.add_argument(
        '--protocol',
        help='Specific protocol to check'
    )
    mon_parser.add_argument(
        '--alerts-only', action='store_true',
        help='Show only active alerts'
    )

    # Anomaly command
    anom_parser = subparsers.add_parser('anomaly', help='Run anomaly detection')
    anom_parser.add_argument(
        '--model',
        choices=['zscore', 'isolation', 'correlation'],
        help='Specific detection model'
    )
    anom_parser.add_argument(
        '--protocol',
        help='Specific protocol to analyze'
    )

    # Dream Mode Export command
    dm_parser = subparsers.add_parser(
        'dream-mode-export',
        help='Generate Dream Mode data for frontend'
    )
    dm_parser.add_argument(
        '--output',
        default='./outputs/dream_mode_data.json',
        help='Output file path'
    )

    # All command
    all_parser = subparsers.add_parser('all', help='Run full pipeline')
    all_parser.add_argument(
        '--offline', action='store_true',
        help='Use bundled data only'
    )

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate summary report')
    report_parser.add_argument(
        '--format',
        choices=['csv', 'json', 'markdown'],
        default='markdown',
        help='Output format'
    )

    args = parser.parse_args()

    # Setup logging
    log_level = 'DEBUG' if args.verbose else 'INFO'
    setup_logging(level=log_level, log_file=True, console=True)

    logger = logging.getLogger('diboas')

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Print banner
    print()
    print("  diBoaS Analytics v1.0")
    print("  Investment Strategy Analysis Tool")
    print()

    try:
        # Route to appropriate handler
        if args.command == 'collect':
            from src.commands.collect import run_collect
            run_collect(args)

        elif args.command == 'battle-test':
            from src.commands.battle_test_cmd import run_battle_test_cmd
            run_battle_test_cmd(args)

        elif args.command == 'monte-carlo':
            from src.commands.monte_carlo_cmd import run_monte_carlo_cmd
            run_monte_carlo_cmd(args)

        elif args.command == 'monitor':
            from src.commands.monitor_cmd import run_monitor
            run_monitor(args)

        elif args.command == 'anomaly':
            from src.commands.anomaly_cmd import run_anomaly
            run_anomaly(args)

        elif args.command == 'dream-mode-export':
            from src.commands.dream_mode_cmd import run_dream_mode_export
            run_dream_mode_export(args)

        elif args.command == 'all':
            from src.commands.full_pipeline import run_all
            run_all(args)

        elif args.command == 'report':
            print("Report generation - use specific commands for now")
            print("  Battle Test report: outputs/battle_test_report.md")
            print("  Monte Carlo report: outputs/monte_carlo_report.md")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)

    except Exception as e:
        logger.exception(f"Error: {e}")
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
