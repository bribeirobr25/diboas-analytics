"""
Protocol monitoring command.
"""

import logging
from datetime import datetime

from src.engines.monitoring import MonitoringEngine
from src.collectors.file_loader import FileLoader
from src.reporters.json_reporter import JSONReporter
from config.protocols import PROTOCOLS

logger = logging.getLogger(__name__)


def run_monitor(args):
    """
    Execute protocol health monitoring.

    Args:
        args: Parsed command line arguments
    """
    print("Protocol Monitoring")
    print("=" * 50)

    # Load latest data
    loader = FileLoader()

    try:
        apy_data = loader.load('defillama')
    except FileNotFoundError:
        print("Error: No DeFiLlama data found. Run 'collect' first.")
        return

    # Get latest and previous day data
    if 'date' not in apy_data.columns:
        print("Error: No date column in data")
        return

    dates = sorted(apy_data['date'].unique())
    if len(dates) < 2:
        print("Error: Need at least 2 days of data for monitoring")
        return

    latest_date = dates[-1]
    prev_date = dates[-2]

    print(f"Latest data: {latest_date}")
    print(f"Previous data: {prev_date}")
    print()

    # Build current and previous metrics
    current_data = {}
    previous_data = {}

    for protocol_id, protocol_config in PROTOCOLS.items():
        project = protocol_config.get('defillama_project')
        if not project:
            continue

        # Get current metrics
        current_rows = apy_data[
            (apy_data['date'] == latest_date) &
            (apy_data['project'] == project)
        ]

        if not current_rows.empty:
            current_data[protocol_id] = {
                'tvl': current_rows['tvl_usd'].mean(),
                'apy': current_rows['apy'].mean()
            }

        # Get previous metrics
        prev_rows = apy_data[
            (apy_data['date'] == prev_date) &
            (apy_data['project'] == project)
        ]

        if not prev_rows.empty:
            previous_data[protocol_id] = {
                'tvl': prev_rows['tvl_usd'].mean(),
                'apy': prev_rows['apy'].mean()
            }

    # Run monitoring
    engine = MonitoringEngine()
    health_reports = engine.check_all_protocols(current_data, previous_data)

    # Display results
    print("Protocol Health Status:")
    print("-" * 70)
    print(f"{'Protocol':<15} {'TVL':>15} {'APY':>10} {'Status':>10} {'Alerts':>10}")
    print("-" * 70)

    for health in health_reports:
        status = "HEALTHY" if health.is_healthy else "UNHEALTHY"
        status_color = status
        tvl_str = f"${health.tvl:,.0f}" if health.tvl else "N/A"
        apy_str = f"{health.apy:.1f}%" if health.apy else "N/A"

        print(f"{health.protocol:<15} {tvl_str:>15} {apy_str:>10} {status:>10} {len(health.alerts):>10}")

    print("-" * 70)
    print()

    # Show active alerts
    active_alerts = engine.get_active_alerts(health_reports)

    if args.alerts_only or active_alerts:
        print(f"Active Alerts: {len(active_alerts)}")
        print()

        for alert in active_alerts:
            severity_marker = {
                'emergency': '!!!',
                'critical': '!!',
                'warning': '!',
                'info': 'i'
            }.get(alert.severity.value, '')

            print(f"  [{severity_marker}] {alert.protocol}: {alert.message}")

        if not active_alerts:
            print("  No active alerts")

    print()

    # Export results
    json_reporter = JSONReporter()
    summary = engine.generate_summary(health_reports)
    json_reporter.export_protocol_health([h.to_dict() for h in health_reports])

    print("Monitoring complete")
