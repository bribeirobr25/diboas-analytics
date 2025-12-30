"""
Data collection command.
"""

import logging
from src.collectors.file_loader import FileLoader

logger = logging.getLogger(__name__)


def run_collect(args):
    """
    Execute data collection.

    Args:
        args: Parsed command line arguments
    """
    print("Data Collection")
    print("=" * 50)

    loader = FileLoader()

    if args.offline:
        print("Mode: Offline (using bundled data only)")
        print()

        # Load and display info about bundled files
        data = loader.load_all()

        for source, df in data.items():
            if not df.empty:
                print(f"{source}:")
                print(f"  Records: {len(df):,}")
                if 'date' in df.columns:
                    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
                print()

        print("Bundled data loaded successfully")

    elif args.source:
        print(f"Loading data from: {args.source}")
        df = loader.load(args.source)
        print(f"Loaded {len(df):,} records")

    else:
        print("Mode: All sources")
        print()

        # For now, we only support bundled data
        # Live API collection can be added in Phase 2
        print("Note: Live API collection not yet implemented.")
        print("Using bundled historical data.")
        print()

        data = loader.load_all()
        for source, df in data.items():
            if not df.empty:
                print(f"  {source}: {len(df):,} records")

    print()
    print("Data collection complete")
