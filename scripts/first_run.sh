#!/bin/bash
# =============================================================================
# diBoaS Analytics - First Run Script
# =============================================================================
# Run this script on first deployment to collect full historical data.
#
# Usage:
#   ./scripts/first_run.sh
#
# This script will:
#   1. Collect full historical data from all live API sources (from May 2022)
#   2. Copy bundled Jupiter JLP data (no API available)
#   3. Verify data completeness
# =============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "  diBoaS Analytics - First Run"
echo "=========================================="
echo "Starting: $(date)"
echo ""

# Change to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Working directory: $(pwd)"
echo ""

# 1. Full historical collection from all live sources
echo "Step 1: Collecting full historical data..."
echo "  Start date: 2022-05-01"
echo "  This may take several minutes..."
echo ""

python3 main.py collect --source all --start-date 2022-05-01

echo ""
echo "Step 1 complete."
echo ""

# 2. Copy Jupiter bundled data (no API available)
echo "Step 2: Checking Jupiter JLP data..."
JUPITER_FILE="data/jupiter_jlp_historical_apy.csv"
BUNDLED_JUPITER="cto_handoff_package/08_results_manual_execution/layer01_csv/jupiter_jlp_historical_apy.csv"

if [ ! -f "$JUPITER_FILE" ]; then
    if [ -f "$BUNDLED_JUPITER" ]; then
        echo "  Copying bundled Jupiter JLP data..."
        cp "$BUNDLED_JUPITER" "$JUPITER_FILE"
        echo "  Done."
    else
        echo "  WARNING: Jupiter bundled data not found at $BUNDLED_JUPITER"
        echo "  JLP strategies may not work correctly."
    fi
else
    echo "  Jupiter data already exists."
fi
echo ""

# 3. Verify data completeness
echo "Step 3: Verifying data completeness..."
echo ""

python3 -c "
import pandas as pd
from datetime import date

files = {
    'defillama_historical_apy.csv': date(2022, 6, 1),
    'crypto_prices.csv': date(2022, 6, 1),
    'tradfi_benchmark_data.csv': date(2022, 6, 1),
    'jito_historical_apy.csv': date(2024, 2, 1),
    'jupiter_jlp_historical_apy.csv': date(2023, 11, 1),
}

print('Data File Verification:')
print('-' * 70)

all_ok = True
for filename, expected_start in files.items():
    filepath = f'data/{filename}'
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        actual_start = df['date'].min().date()
        actual_end = df['date'].max().date()
        rows = len(df)

        status = 'OK' if actual_start <= expected_start else 'WARN'
        if status == 'WARN':
            all_ok = False

        print(f'  [{status}] {filename}')
        print(f'       Rows: {rows:,}  |  Range: {actual_start} to {actual_end}')
    except FileNotFoundError:
        print(f'  [MISSING] {filename}')
        all_ok = False
    except Exception as e:
        print(f'  [ERROR] {filename}: {e}')
        all_ok = False

print('-' * 70)
if all_ok:
    print('All data files verified successfully!')
else:
    print('WARNING: Some data files may have insufficient coverage.')
"

echo ""
echo "=========================================="
echo "  First Run Complete"
echo "=========================================="
echo "Finished: $(date)"
echo ""
echo "Next steps:"
echo "  1. Run: python3 main.py battle-test"
echo "  2. Run: python3 main.py monte-carlo --simulations 5000"
echo "  3. Run: python3 main.py adelaide --locale pt-br --persona ana --format newsletter_md"
echo ""
