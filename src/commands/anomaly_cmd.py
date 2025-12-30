"""
Anomaly detection command.
"""

import logging
import pandas as pd

from src.engines.anomaly import AnomalyEngine, ZScoreDetector
from src.collectors.file_loader import FileLoader
from src.reporters.json_reporter import JSONReporter

logger = logging.getLogger(__name__)


def run_anomaly(args):
    """
    Execute anomaly detection.

    Args:
        args: Parsed command line arguments
    """
    print("Anomaly Detection")
    print("=" * 50)

    # Load data
    loader = FileLoader()

    try:
        apy_data = loader.load('defillama')
        price_data = loader.load('yahoo')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run 'collect' first.")
        return

    print(f"Analyzing {len(apy_data):,} APY records")
    print(f"Analyzing {len(price_data):,} price records")
    print()

    # Initialize engine
    engine = AnomalyEngine()

    all_anomalies = []

    # APY anomaly detection
    print("Checking APY data for anomalies...")

    if 'project' in apy_data.columns and 'apy' in apy_data.columns:
        for project in apy_data['project'].unique():
            if args.protocol and args.protocol != project:
                continue

            project_data = apy_data[apy_data['project'] == project].copy()

            if len(project_data) > 30:  # Need enough data for rolling window
                project_data = project_data.sort_values('date').set_index('date')
                apy_series = project_data['apy']
                apy_series.name = 'apy'

                detector = ZScoreDetector()
                anomalies = detector.detect(apy_series, project)
                all_anomalies.extend(anomalies)

    # Price anomaly detection
    print("Checking price data for anomalies...")

    if 'symbol' in price_data.columns and 'close' in price_data.columns:
        for symbol in price_data['symbol'].unique():
            symbol_data = price_data[price_data['symbol'] == symbol].copy()

            if len(symbol_data) > 30:
                symbol_data = symbol_data.sort_values('date').set_index('date')
                returns = symbol_data['close'].pct_change()
                returns.name = 'daily_return'

                detector = ZScoreDetector(threshold=3.5)  # Higher threshold for prices
                anomalies = detector.detect(returns, f'price_{symbol}')
                all_anomalies.extend(anomalies)

    # Display results
    print()
    print(f"Total anomalies detected: {len(all_anomalies)}")
    print("-" * 70)

    if all_anomalies:
        # Group by detection method
        by_method = {}
        for a in all_anomalies:
            method = a.detection_method
            by_method[method] = by_method.get(method, 0) + 1

        print("By detection method:")
        for method, count in by_method.items():
            print(f"  {method}: {count}")

        print()
        print("Recent anomalies (last 10):")
        print("-" * 70)

        recent = sorted(all_anomalies, key=lambda x: x.timestamp, reverse=True)[:10]
        for a in recent:
            print(f"  {a.protocol}: {a.metric} = {a.value:.4f} (score: {a.score:.2f})")

    else:
        print("No anomalies detected")

    print()

    # Export results
    report = engine.generate_report(all_anomalies)

    json_reporter = JSONReporter()
    json_reporter.export_anomalies(report)

    print("Anomaly detection complete")
