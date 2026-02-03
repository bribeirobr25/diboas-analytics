"""
Data collection command.

Uses registry framework for pluggable collector access.
Supports both bundled data and live API collection.
"""

import logging
from pathlib import Path
from datetime import datetime, date
import pandas as pd

from src.registries import CollectorRegistry
from config.settings import DATA_DIR

# Import collectors to trigger registration
import src.collectors  # noqa: F401

logger = logging.getLogger(__name__)

# Live API sources
LIVE_SOURCES = ['fred', 'yahoo_live', 'defillama_live', 'coingecko', 'alternative']

# Bundled data sources
BUNDLED_SOURCES = ['file_loader', 'defillama', 'yahoo', 'jupiter']


def run_collect(args):
    """
    Execute data collection.

    Supports:
    - --offline: Use bundled historical data
    - --source <name>: Collect from specific source
    - --source all: Collect from all live API sources
    - --output <dir>: Save collected data to directory
    - --start-date: Historical start date (YYYY-MM-DD)
    - --append: Append new data to existing files

    Args:
        args: Parsed command line arguments
    """
    print("Data Collection")
    print("=" * 50)

    registry = CollectorRegistry.get_instance()

    # Determine output directory
    output_dir = Path(args.output) if hasattr(args, 'output') and args.output else DATA_DIR

    # Parse start date if provided
    start_date = None
    if hasattr(args, 'start_date') and args.start_date:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
        print(f"Using historical start date: {start_date}")

    # Check if append mode
    append_mode = hasattr(args, 'append') and args.append
    if append_mode:
        print("Mode: Incremental append (preserving existing data)")

    if args.offline:
        _collect_offline(registry)

    elif args.source:
        source = args.source.lower()

        if source == 'all':
            _collect_all_live(registry, output_dir, start_date, append_mode)
        elif source in LIVE_SOURCES:
            _collect_single_live(registry, source, output_dir, start_date, append_mode)
        elif source in BUNDLED_SOURCES or registry.is_registered(source):
            _collect_single_bundled(registry, source)
        else:
            print(f"Unknown source: {source}")
            print(f"Available sources: {', '.join(sorted(LIVE_SOURCES + BUNDLED_SOURCES))}")
            return

    else:
        # Default: show status and available collectors
        _show_status(registry)

    print()
    print("Data collection complete")


def _collect_offline(registry):
    """Collect from bundled historical data only."""
    print("Mode: Offline (using bundled data only)")
    print()

    collector = registry.get("file_loader", {})
    data = collector.collect()

    for source, df in data.items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            print(f"{source}:")
            print(f"  Records: {len(df):,}")
            if 'date' in df.columns:
                print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
            print()

    print("Bundled data loaded successfully")


def _collect_single_bundled(registry, source):
    """Collect from a single bundled source."""
    print(f"Loading bundled data from: {source}")
    print()

    try:
        collector = registry.get(source, {})
        data = collector.collect()

        if isinstance(data, pd.DataFrame):
            print(f"Loaded {len(data):,} records")
            if 'date' in data.columns:
                print(f"Date range: {data['date'].min()} to {data['date'].max()}")
        elif isinstance(data, dict):
            for key, df in data.items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    print(f"  {key}: {len(df):,} records")

    except Exception as e:
        print(f"Error collecting from {source}: {e}")


def _collect_single_live(registry, source, output_dir, start_date=None, append_mode=False):
    """Collect from a single live API source."""
    print(f"Collecting from live API: {source}")
    print()

    try:
        # Pass start_date in config if provided
        config = {}
        if start_date:
            config['start_date'] = start_date

        collector = registry.get(source, config)

        # Check if API key is configured (for sources that need it)
        if source == 'fred':
            from config.settings import settings
            if not settings.has('FRED_API_KEY'):
                print("Warning: FRED_API_KEY not configured in .env file")
                print("Get a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html")
                return

        print("Fetching data...")

        # Use incremental mode if requested and supported
        if append_mode and hasattr(collector, 'save_to_csv_incremental'):
            print("Using incremental append mode...")
            paths = collector.save_to_csv_incremental(str(output_dir))
        elif hasattr(collector, 'save_to_csv'):
            paths = collector.save_to_csv(str(output_dir))

            if isinstance(paths, dict):
                print(f"\nSaved files:")
                for key, path in paths.items():
                    if path and not isinstance(path, dict):
                        print(f"  {key}: {path}")
                    elif isinstance(path, dict):
                        for subkey, subpath in path.items():
                            print(f"  {key}/{subkey}: {subpath}")
            elif paths:
                print(f"Saved to: {paths}")
        else:
            data = collector.collect()
            _display_collected_data(source, data)

    except Exception as e:
        logger.exception(f"Error collecting from {source}")
        print(f"Error: {e}")


def _collect_all_live(registry, output_dir, start_date=None, append_mode=False):
    """Collect from all live API sources."""
    print("Mode: Live API Collection (all sources)")
    print(f"Output directory: {output_dir}")
    if start_date:
        print(f"Start date: {start_date}")
    if append_mode:
        print("Append mode: enabled")
    print()

    # If append mode, collect sources individually to use incremental methods
    if append_mode:
        print("Collecting sources individually in append mode...")
        for source in LIVE_SOURCES:
            print(f"\n--- {source.upper()} ---")
            _collect_single_live(registry, source, output_dir, start_date, append_mode)
        return

    # Pass start_date in config if provided
    config = {}
    if start_date:
        config['start_date'] = start_date

    # Get aggregator
    try:
        aggregator = registry.get("aggregator", config)
    except KeyError:
        print("Aggregator collector not registered. Collecting sources individually.")
        for source in LIVE_SOURCES:
            print(f"\n--- {source.upper()} ---")
            _collect_single_live(registry, source, output_dir, start_date, append_mode)
        return

    print("Collecting from all live sources...")
    print()

    # Use aggregator to save all data
    saved = aggregator.save_all(str(output_dir))

    print("\nResults:")
    print("-" * 40)

    for source, result in saved.items():
        if isinstance(result, dict) and 'error' in result:
            print(f"  {source}: FAILED - {result['error']}")
        elif isinstance(result, dict):
            print(f"  {source}:")
            for key, path in result.items():
                if path:
                    print(f"    - {key}: saved")
        elif result:
            print(f"  {source}: saved")
        else:
            print(f"  {source}: no data")

    print("-" * 40)

    # Also collect Jupiter JLP APY (calculated from fees/TVL)
    _collect_jupiter_jlp_live(registry, output_dir)


def _collect_jupiter_jlp_live(registry, output_dir):
    """
    Collect Jupiter JLP live APY data.

    Jupiter JLP APY is calculated from DeFiLlama fees/TVL data,
    not available directly from the yields API.
    """
    print("\n--- JUPITER JLP (Live Calculation) ---")

    try:
        collector = registry.get("defillama_live", {})
        apy, metadata = collector.collect_jupiter_jlp_apy(str(output_dir))

        if apy is not None:
            print(f"  Jupiter JLP APY: {apy:.2f}%")
            print(f"  TVL: ${metadata.get('tvl_usd', 0):,.0f}")
            print(f"  Daily Fees: ${metadata.get('daily_fees_usd', 0):,.0f}")
            print(f"  Data appended to jupiter_jlp_historical_apy.csv")
        else:
            print("  Warning: Could not calculate Jupiter JLP APY")
            print("  Using bundled historical data as fallback")

    except Exception as e:
        logger.warning(f"Jupiter JLP live collection failed: {e}")
        print(f"  Error: {e}")
        print("  Falling back to bundled historical data")


def _display_collected_data(source, data):
    """Display collected data summary."""
    if isinstance(data, pd.DataFrame):
        print(f"\nCollected {len(data):,} records from {source}")
        if 'date' in data.columns:
            print(f"Date range: {data['date'].min()} to {data['date'].max()}")
        print(f"Columns: {', '.join(data.columns)}")

    elif isinstance(data, dict):
        print(f"\nCollected data from {source}:")
        for key, df in data.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                print(f"  {key}: {len(df):,} records")
            elif isinstance(df, dict) and 'error' in df:
                print(f"  {key}: ERROR - {df['error']}")


def _show_status(registry):
    """Show collector status and help."""
    print("Available Data Sources")
    print("-" * 40)
    print()

    print("Live API Sources:")
    for source in LIVE_SOURCES:
        registered = "OK" if registry.is_registered(source) else "NOT REGISTERED"
        print(f"  {source}: {registered}")

    print()
    print("Bundled Data Sources:")
    for source in BUNDLED_SOURCES:
        registered = "OK" if registry.is_registered(source) else "NOT REGISTERED"
        print(f"  {source}: {registered}")

    print()
    print("Usage:")
    print("  python main.py collect --offline                       Load bundled data")
    print("  python main.py collect --source fred                   Collect from FRED API")
    print("  python main.py collect --source yahoo_live             Collect from Yahoo Finance")
    print("  python main.py collect --source all                    Collect from all live APIs")
    print("  python main.py collect --source all --output data/")
    print("  python main.py collect --source all --start-date 2022-05-01  Full historical")
    print("  python main.py collect --source all --append           Incremental daily update")
