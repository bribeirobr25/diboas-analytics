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
    adelaide        Generate personalized newsletters
    all             Run full pipeline
    registry        List available registry implementations

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
from src.utils.validation import validate_cli_args
from src.utils.validation.cli import print_validation_errors
from src.utils.errors import handle_error, DiBoaSError
from src.utils.audit import create_audit_trail
from src.utils.correlation import (
    new_correlation_id,
    set_correlation_id,
    setup_correlated_logging,
)


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
  python main.py adelaide --persona ana  Generate Adelaide newsletter
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
        '--offline', action='store_true',
        help='Use bundled data only'
    )
    collect_parser.add_argument(
        '--source',
        help='Data source (fred, yahoo_live, defillama_live, coingecko, alternative, all)'
    )
    collect_parser.add_argument(
        '--output',
        help='Output directory for collected data (default: data/)'
    )
    collect_parser.add_argument(
        '--start-date',
        help='Historical start date (YYYY-MM-DD), default: 2022-05-01'
    )
    collect_parser.add_argument(
        '--append', action='store_true',
        help='Append new data to existing files instead of overwriting'
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

    # Adelaide command
    adelaide_parser = subparsers.add_parser(
        'adelaide',
        help='Generate personalized newsletters'
    )
    adelaide_parser.add_argument(
        '--persona',
        choices=['ana', 'maria', 'felipe', 'all'],
        default='ana',
        help='Persona to generate for (default: ana)'
    )
    adelaide_parser.add_argument(
        '--locale',
        choices=['en', 'pt-br'],
        default='en',
        help='Locale for content (default: en)'
    )
    adelaide_parser.add_argument(
        '--format',
        default='newsletter_md',
        help='Output formats, comma-separated (newsletter_md, twitter_thread, linkedin_post, website_teaser, substack)'
    )
    adelaide_parser.add_argument(
        '--output',
        default='./outputs',
        help='Output directory (default: ./outputs)'
    )
    adelaide_parser.add_argument(
        '--data',
        help='Path to analytics data JSON (optional, will collect live if not provided)'
    )
    adelaide_parser.add_argument(
        '--tenant',
        default='diboas',
        help='Tenant ID for configuration (default: diboas)'
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

    # Registry command
    reg_parser = subparsers.add_parser('registry', help='List available registry implementations')
    reg_parser.add_argument(
        '--type',
        choices=['collectors', 'validators', 'engines', 'triggers', 'personas', 'outputs', 'all'],
        default='all',
        help='Registry type to list (default: all)'
    )

    # Triggers command
    triggers_parser = subparsers.add_parser('triggers', help='Evaluate intelligence triggers')
    triggers_parser.add_argument(
        '--data',
        help='Path to market data JSON (optional, will collect live if not provided)'
    )
    triggers_parser.add_argument(
        '--output',
        default='./outputs/trigger_results.json',
        help='Output file path (default: ./outputs/trigger_results.json)'
    )
    triggers_parser.add_argument(
        '--dry-run', action='store_true',
        help='Evaluate but do not record cooldowns'
    )

    # Validate CLO command
    validate_clo_parser = subparsers.add_parser('validate-clo', help='Run CLO Gate 4 compliance')
    validate_clo_parser.add_argument(
        '--content',
        help='Content to validate (or path to file)'
    )
    validate_clo_parser.add_argument(
        '--jurisdiction',
        choices=['US', 'EU', 'BR', 'UK'],
        default='US',
        help='Target jurisdiction (default: US)'
    )
    validate_clo_parser.add_argument(
        '--crisis-level', type=int, default=0,
        help='Crisis level 0-5 (default: 0)'
    )

    # Crisis queue command
    crisis_parser = subparsers.add_parser('crisis-queue', help='Manage crisis approval queue')
    crisis_subparsers = crisis_parser.add_subparsers(dest='crisis_action', help='Queue actions')

    crisis_list_parser = crisis_subparsers.add_parser('list', help='List pending requests')
    crisis_list_parser.add_argument(
        '--queue',
        help='Filter by queue name'
    )

    crisis_approve_parser = crisis_subparsers.add_parser('approve', help='Approve a request')
    crisis_approve_parser.add_argument(
        'request_id',
        help='Request ID to approve'
    )
    crisis_approve_parser.add_argument(
        '--approver', required=True,
        help='Approver email/name'
    )

    crisis_reject_parser = crisis_subparsers.add_parser('reject', help='Reject a request')
    crisis_reject_parser.add_argument(
        'request_id',
        help='Request ID to reject'
    )
    crisis_reject_parser.add_argument(
        '--approver', required=True,
        help='Approver email/name'
    )
    crisis_reject_parser.add_argument(
        '--reason',
        help='Rejection reason'
    )

    # Validate Gate 1 command
    validate_gate1_parser = subparsers.add_parser('validate-gate1', help='Run Gate 1 schema validation')
    validate_gate1_parser.add_argument(
        '--file',
        help='Specific file to validate (or all if not specified)'
    )
    validate_gate1_parser.add_argument(
        '--data-dir',
        default='data',
        help='Data directory (default: data/)'
    )
    validate_gate1_parser.add_argument(
        '--edition',
        choices=['pulse', 'weekly'],
        default='weekly',
        help='Adelaide edition type for SLA selection (default: weekly)'
    )
    validate_gate1_parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings (not just errors)'
    )
    validate_gate1_parser.add_argument(
        '--output',
        help='Output report file (optional)'
    )

    # Validate Gate 2 command
    validate_gate2_parser = subparsers.add_parser('validate-gate2', help='Run Gate 2 analytics validation')
    validate_gate2_parser.add_argument(
        '--battle-test',
        default='outputs/battle_test_results.json',
        help='Battle Test results file (default: outputs/battle_test_results.json)'
    )
    validate_gate2_parser.add_argument(
        '--monte-carlo',
        default='outputs/monte_carlo_results.json',
        help='Monte Carlo results file (default: outputs/monte_carlo_results.json)'
    )
    validate_gate2_parser.add_argument(
        '--risk-metrics',
        default='outputs/risk_metrics.json',
        help='Risk metrics file (default: outputs/risk_metrics.json)'
    )
    validate_gate2_parser.add_argument(
        '--output',
        help='Output report file (optional)'
    )

    # Health command
    from src.commands.health_cmd import add_health_parser
    add_health_parser(subparsers)

    # Tenants command
    tenants_parser = subparsers.add_parser('tenants', help='Manage tenant configurations')
    tenants_subparsers = tenants_parser.add_subparsers(dest='tenants_action', help='Tenant actions')

    # tenants list
    tenants_list_parser = tenants_subparsers.add_parser('list', help='List all tenants')

    # tenants validate
    tenants_validate_parser = tenants_subparsers.add_parser('validate', help='Validate tenant config')
    tenants_validate_parser.add_argument(
        '--tenant', required=True,
        help='Tenant ID to validate'
    )

    # tenants show
    tenants_show_parser = tenants_subparsers.add_parser('show', help='Show tenant details')
    tenants_show_parser.add_argument(
        '--tenant', required=True,
        help='Tenant ID to show'
    )

    # tenants policy
    tenants_policy_parser = tenants_subparsers.add_parser('policy', help='Show data access policy')
    tenants_policy_parser.add_argument(
        '--tenant',
        help='Tenant ID (default: diboas)'
    )

    args = parser.parse_args()

    # Setup logging with correlation support
    log_level = 'DEBUG' if args.verbose else 'INFO'
    setup_logging(level=log_level, log_file=True, console=True)
    setup_correlated_logging()

    logger = logging.getLogger('diboas')

    # Generate correlation ID for this CLI invocation
    correlation_id = new_correlation_id(prefix=f"cli-{args.command or 'help'}")
    logger.debug(f"Starting CLI with correlation_id={correlation_id}")

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Validate CLI arguments (Principle 8 - Security)
    validation_result = validate_cli_args(args)
    print_validation_errors(validation_result, command=args.command, exit_on_error=True)

    # Create audit trail for this execution
    audit = create_audit_trail(command=args.command)
    audit.set_parameters(vars(args))

    # Print banner
    print()
    print("  diBoaS Analytics v1.0")
    print("  Investment Strategy Analysis Tool")
    print(f"  Run ID: {audit.run_id}")
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

        elif args.command == 'adelaide':
            from src.commands.adelaide_cmd import run_adelaide
            run_adelaide(args)

        elif args.command == 'all':
            from src.commands.full_pipeline import run_all
            run_all(args)

        elif args.command == 'report':
            print("Report generation - use specific commands for now")
            print("  Battle Test report: outputs/battle_test_report.md")
            print("  Monte Carlo report: outputs/monte_carlo_report.md")

        elif args.command == 'registry':
            from src.commands.registry_cmd import run_registry
            run_registry(args)

        elif args.command == 'tenants':
            from src.commands.tenants_cmd import run_tenants
            run_tenants(args)

        elif args.command == 'triggers':
            from src.commands.triggers_cmd import run_triggers
            run_triggers(args)

        elif args.command == 'validate-clo':
            from src.commands.validate_clo_cmd import run_validate_clo
            run_validate_clo(args)

        elif args.command == 'crisis-queue':
            from src.commands.crisis_queue_cmd import run_crisis_queue
            run_crisis_queue(args)

        elif args.command == 'validate-gate1':
            from src.commands.validate_gate1_cmd import run_validate_gate1
            run_validate_gate1(args)

        elif args.command == 'validate-gate2':
            from src.commands.validate_gate2_cmd import run_validate_gate2
            run_validate_gate2(
                battle_test_file=args.battle_test,
                monte_carlo_file=args.monte_carlo,
                risk_metrics_file=args.risk_metrics,
                output_file=args.output,
            )

        elif args.command == 'health':
            from src.commands.health_cmd import run_health
            exit_code = run_health(args)
            if exit_code != 0:
                sys.exit(exit_code)

        # Save audit report on successful completion
        audit.log_event('execution_complete', f'Command {args.command} completed successfully')
        audit_path = audit.save_report()
        audit.print_summary()

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        audit.log_event('execution_cancelled', 'User cancelled operation', severity='warning')
        audit.save_report()
        sys.exit(1)

    except DiBoaSError as e:
        audit.log_error(e, context=args.command)
        audit.save_report()
        handle_error(e, context=args.command, verbose=args.verbose)

    except Exception as e:
        audit.log_error(e, context=args.command)
        audit.save_report()
        logger.exception(f"Error: {e}")
        handle_error(e, context=args.command, verbose=args.verbose)


if __name__ == '__main__':
    main()
