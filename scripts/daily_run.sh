#!/bin/bash
# =============================================================================
# diBoaS Analytics - Daily Run Script
# =============================================================================
# Run this script daily to update data and generate reports.
#
# Usage:
#   ./scripts/daily_run.sh
#
# This script will:
#   1. Collect new data incrementally (appends to existing files)
#   2. Run Battle Test
#   3. Run Monte Carlo simulation
#   4. Generate Adelaide newsletters for all personas
# =============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "  diBoaS Analytics - Daily Run"
echo "=========================================="
echo "Starting: $(date)"
echo ""

# Change to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Working directory: $(pwd)"
echo ""

# 1. Incremental data collection (appends to existing files)
echo "Step 1: Collecting new data (incremental mode)..."
python3 main.py collect --source all --append

echo ""
echo "Step 1 complete."
echo ""

# 2. Run Battle Test
echo "Step 2: Running Battle Test..."
python3 main.py battle-test

echo ""
echo "Step 2 complete."
echo ""

# 3. Run Monte Carlo
echo "Step 3: Running Monte Carlo simulation..."
python3 main.py monte-carlo --simulations 5000

echo ""
echo "Step 3 complete."
echo ""

# 4. Generate Adelaide newsletters
echo "Step 4: Generating Adelaide newsletters..."

# Portuguese - Brazil
echo "  Generating PT-BR newsletters..."
python3 main.py adelaide --locale pt-br --persona ana --format newsletter_md
python3 main.py adelaide --locale pt-br --persona maria --format newsletter_md
python3 main.py adelaide --locale pt-br --persona felipe --format newsletter_md

# English
echo "  Generating EN newsletters..."
python3 main.py adelaide --locale en --persona ana --format newsletter_md
python3 main.py adelaide --locale en --persona maria --format newsletter_md
python3 main.py adelaide --locale en --persona felipe --format newsletter_md

echo ""
echo "Step 4 complete."
echo ""

# Summary
echo "=========================================="
echo "  Daily Run Complete"
echo "=========================================="
echo "Finished: $(date)"
echo ""
echo "Generated outputs:"
ls -la outputs/*.md 2>/dev/null | tail -10 || echo "  No markdown files found"
echo ""
echo "Next: Review outputs and send to distribution channels."
echo ""
