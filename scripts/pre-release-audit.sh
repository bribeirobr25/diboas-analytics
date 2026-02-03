#!/bin/bash
# ==========================================================================
# diBoaS Analytics Pre-Release Audit Script
# ==========================================================================
#
# Purpose: Run comprehensive checks before release to ensure code quality,
#          security, and compliance with project standards.
#
# Usage:
#   ./scripts/pre-release-audit.sh          # Interactive mode (full output)
#   ./scripts/pre-release-audit.sh --ci     # CI mode (exits non-zero on critical issues)
#   ./scripts/pre-release-audit.sh --fix    # Auto-fix mode (where possible)
#
# Requirements:
#   - Python 3.10+
#   - pytest, ruff (optional), pip-audit (optional)
#
# ==========================================================================

set -e

# Use project root reliably
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Track errors for CI mode
CRITICAL_ERRORS=0
WARNINGS=0

# Mode flags
CI_MODE=false
FIX_MODE=false

for arg in "$@"; do
  case $arg in
    --ci) CI_MODE=true ;;
    --fix) FIX_MODE=true ;;
  esac
done

# Colors for output (disabled in CI mode)
if [ "$CI_MODE" = true ]; then
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  NC=""
else
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  NC='\033[0m' # No Color
fi

# Helper functions
print_section() {
  echo ""
  echo -e "${BLUE}==========================================${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}==========================================${NC}"
}

print_check() {
  echo ""
  echo -e "--- $1 ---"
}

print_ok() {
  echo -e "${GREEN}OK:${NC} $1"
}

print_fail() {
  echo -e "${RED}FAIL:${NC} $1"
}

print_warn() {
  echo -e "${YELLOW}WARN:${NC} $1"
}

print_skip() {
  echo -e "${YELLOW}SKIP:${NC} $1"
}

# ==========================================================================
# HEADER
# ==========================================================================
print_section "diBoaS Analytics PRE-RELEASE AUDIT"
echo "Project: $PROJECT_ROOT"
echo "Mode: $([ "$CI_MODE" = true ] && echo 'CI (strict)' || echo 'Interactive')$([ "$FIX_MODE" = true ] && echo ' + Auto-fix')"
echo "Python: $(python3 --version 2>&1)"
echo "Date: $(date)"

# ==========================================================================
# CHECK 1: Python Syntax Check
# ==========================================================================
print_check "1/12: Python Syntax Check"
SYNTAX_ERRORS=0
for file in $(find . -name "*.py" -not -path "./.venv/*" -not -path "./__pycache__/*" 2>/dev/null); do
  if ! python3 -m py_compile "$file" 2>/dev/null; then
    echo "  Syntax error in: $file"
    ((SYNTAX_ERRORS++)) || true
  fi
done

if [ "$SYNTAX_ERRORS" -eq 0 ]; then
  print_ok "All Python files have valid syntax"
else
  print_fail "$SYNTAX_ERRORS file(s) with syntax errors"
  ((CRITICAL_ERRORS++)) || true
fi

# ==========================================================================
# CHECK 2: Import Verification
# ==========================================================================
print_check "2/12: Import Verification"
IMPORT_TEST=$(python3 -c "
import sys
sys.path.insert(0, '.')
errors = []
modules = [
    'config.settings',
    'config.protocols',
    'config.chains',
    'config.thresholds',
    'config.dream_mode',
    'src.collectors.file_loader',
    'src.engines.battle_test',
    'src.engines.monte_carlo',
    'src.engines.monitoring',
    'src.engines.anomaly',
    'src.domain.strategy',
    'src.domain.simulation',
    'src.validators.result_validator',
    'src.reporters.csv_reporter',
    'src.reporters.json_reporter',
]
for mod in modules:
    try:
        __import__(mod)
    except Exception as e:
        errors.append(f'{mod}: {e}')
if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print('OK')
" 2>&1) || true

if echo "$IMPORT_TEST" | grep -q "^OK"; then
  print_ok "All core modules import successfully"
else
  print_fail "Import errors detected"
  echo "$IMPORT_TEST"
  ((CRITICAL_ERRORS++)) || true
fi

# ==========================================================================
# CHECK 3: Linting (Ruff or Flake8)
# ==========================================================================
print_check "3/12: Linting"
if command -v ruff &> /dev/null; then
  if [ "$FIX_MODE" = true ]; then
    ruff check src/ config/ --fix 2>/dev/null || true
    print_ok "Ruff auto-fix applied"
  fi
  LINT_OUTPUT=$(ruff check src/ config/ main.py 2>&1) || true
  LINT_ERRORS=$(echo "$LINT_OUTPUT" | grep -cE "^.+:\d+:\d+:" || true)

  if [ "$LINT_ERRORS" -eq 0 ]; then
    print_ok "No linting errors (ruff)"
  else
    print_warn "$LINT_ERRORS linting issues found"
    echo "$LINT_OUTPUT" | head -20
    ((WARNINGS++)) || true
  fi
elif command -v flake8 &> /dev/null; then
  LINT_OUTPUT=$(flake8 src/ config/ main.py --max-line-length=120 2>&1) || true
  LINT_ERRORS=$(echo "$LINT_OUTPUT" | wc -l | tr -d ' ')

  if [ "$LINT_ERRORS" -le 1 ]; then
    print_ok "No linting errors (flake8)"
  else
    print_warn "$LINT_ERRORS linting issues found"
    echo "$LINT_OUTPUT" | head -20
    ((WARNINGS++)) || true
  fi
else
  print_skip "No linter installed (install: pip install ruff)"
fi

# ==========================================================================
# CHECK 4: Type Checking (MyPy - Optional)
# ==========================================================================
print_check "4/12: Type Checking (Optional)"
if command -v mypy &> /dev/null; then
  MYPY_OUTPUT=$(mypy src/ --ignore-missing-imports --no-error-summary 2>&1) || true
  MYPY_ERRORS=$(echo "$MYPY_OUTPUT" | grep -c "error:" || true)

  if [ "$MYPY_ERRORS" -eq 0 ]; then
    print_ok "No type errors"
  else
    print_warn "$MYPY_ERRORS type issues found (informational)"
    echo "$MYPY_OUTPUT" | grep "error:" | head -10
  fi
else
  print_skip "MyPy not installed (install: pip install mypy)"
fi

# ==========================================================================
# CHECK 5: Security Vulnerabilities
# ==========================================================================
print_check "5/12: Security Vulnerabilities"
if command -v pip-audit &> /dev/null; then
  AUDIT_OUTPUT=$(pip-audit -r requirements.txt 2>&1) || true
  if echo "$AUDIT_OUTPUT" | grep -q "No known vulnerabilities"; then
    print_ok "No known vulnerabilities"
  elif echo "$AUDIT_OUTPUT" | grep -qi "vulnerability"; then
    print_fail "Security vulnerabilities found"
    echo "$AUDIT_OUTPUT"
    ((CRITICAL_ERRORS++)) || true
  else
    print_ok "No vulnerabilities detected"
  fi
elif command -v safety &> /dev/null; then
  if safety check -r requirements.txt 2>/dev/null; then
    print_ok "No known vulnerabilities (safety)"
  else
    print_fail "Security vulnerabilities found"
    ((CRITICAL_ERRORS++)) || true
  fi
else
  print_skip "No security scanner installed (install: pip install pip-audit)"
fi

# ==========================================================================
# CHECK 6: Tests
# ==========================================================================
print_check "6/12: Test Suite"
if command -v pytest &> /dev/null; then
  if pytest tests/ -q --tb=no 2>&1; then
    print_ok "All tests passed"
  else
    print_fail "Tests failed"
    ((CRITICAL_ERRORS++)) || true
  fi
else
  print_skip "pytest not installed"
fi

# ==========================================================================
# CHECK 7: print() Statements (should use logging)
# ==========================================================================
print_check "7/12: print() Statements"
# Exclude main.py banner prints which are intentional
PRINT_COUNT=$(grep -rn "^\s*print(" src/ config/ --include="*.py" 2>/dev/null | grep -v "# noqa" | wc -l | tr -d ' ')

if [ "$PRINT_COUNT" -eq 0 ]; then
  print_ok "No print() statements in src/ (using logging)"
elif [ "$PRINT_COUNT" -lt 5 ]; then
  print_warn "$PRINT_COUNT print() statement(s) found (prefer logging)"
  grep -rn "^\s*print(" src/ config/ --include="*.py" 2>/dev/null | grep -v "# noqa" | head -10
  ((WARNINGS++)) || true
else
  print_warn "$PRINT_COUNT print() statements found"
  grep -rn "^\s*print(" src/ config/ --include="*.py" 2>/dev/null | grep -v "# noqa" | head -10
  ((WARNINGS++)) || true
fi

# ==========================================================================
# CHECK 8: TODO/FIXME Comments
# ==========================================================================
print_check "8/12: TODO/FIXME Comments"
TODO_COUNT=$(grep -rE "TODO|FIXME|HACK|XXX" src/ config/ --include="*.py" 2>/dev/null | wc -l | tr -d ' ')

echo "Found: $TODO_COUNT TODO/FIXME comments"
if [ "$TODO_COUNT" -gt 0 ]; then
  grep -rn "TODO\|FIXME\|HACK\|XXX" src/ config/ --include="*.py" 2>/dev/null | head -15
  if [ "$TODO_COUNT" -gt 10 ]; then
    ((WARNINGS++)) || true
  fi
fi

# ==========================================================================
# CHECK 9: Hardcoded Secrets
# ==========================================================================
print_check "9/12: Hardcoded Secrets Scan"
SECRET_PATTERNS="(api[_-]?key|password|secret|token|private[_-]?key)\s*=\s*['\"][^'\"]{8,}['\"]"
SECRETS_FOUND=$(grep -rE "$SECRET_PATTERNS" src/ config/ --include="*.py" 2>/dev/null | grep -v "os\.environ\|getenv\|\.example\|# noqa" | wc -l | tr -d ' ')

if [ "$SECRETS_FOUND" -gt 0 ]; then
  print_fail "POTENTIAL SECRETS FOUND - REVIEW IMMEDIATELY"
  grep -rn "$SECRET_PATTERNS" src/ config/ --include="*.py" 2>/dev/null | grep -v "os\.environ\|getenv"
  ((CRITICAL_ERRORS++)) || true
else
  print_ok "No obvious hardcoded secrets detected"
fi

# Also check .env files aren't committed
if [ -f ".env" ]; then
  if git ls-files --error-unmatch .env 2>/dev/null; then
    print_fail ".env file is tracked by git - add to .gitignore!"
    ((CRITICAL_ERRORS++)) || true
  fi
fi

# ==========================================================================
# CHECK 10: Data Files Integrity
# ==========================================================================
print_check "10/12: Data Files Integrity"
REQUIRED_DATA_FILES=(
  "data/defillama_historical_apy.csv"
  "data/yahoo_historical_prices.csv"
  "data/jupiter_jlp_historical_apy.csv"
  "config/strategies.json"
)

MISSING_FILES=0
for file in "${REQUIRED_DATA_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "  Missing: $file"
    ((MISSING_FILES++)) || true
  fi
done

if [ "$MISSING_FILES" -eq 0 ]; then
  print_ok "All required data files present"

  # Check data file sizes (should not be empty)
  for file in "${REQUIRED_DATA_FILES[@]}"; do
    SIZE=$(wc -l < "$file" | tr -d ' ')
    if [ "$SIZE" -lt 10 ]; then
      print_warn "$file has only $SIZE lines (possibly corrupted)"
      ((WARNINGS++)) || true
    fi
  done
else
  print_fail "$MISSING_FILES required file(s) missing"
  ((CRITICAL_ERRORS++)) || true
fi

# ==========================================================================
# CHECK 11: Configuration Validation
# ==========================================================================
print_check "11/12: Configuration Validation"
CONFIG_CHECK=$(python3 -c "
import json
import sys

# Check strategies.json
try:
    with open('config/strategies.json') as f:
        data = json.load(f)

    strategies = data.get('strategies', [])
    if len(strategies) != 10:
        print(f'ERROR: Expected 10 strategies, found {len(strategies)}')
        sys.exit(1)

    for s in strategies:
        if 'id' not in s or 'name' not in s or 'allocations' not in s:
            print(f'ERROR: Strategy missing required fields: {s.get(\"id\", \"unknown\")}')
            sys.exit(1)

        # Check allocations sum to 100% (stable + crypto)
        allocs = s['allocations']
        stable_total = sum(allocs.get('stable', {}).values())
        crypto_total = sum(allocs.get('crypto', {}).values())
        total = stable_total + crypto_total

        if abs(total - 1.0) > 0.01:
            print(f'ERROR: Strategy {s[\"id\"]} allocations sum to {total*100}%, not 100%')
            sys.exit(1)

        # Verify crypto_pct matches allocations
        expected_crypto = s.get('crypto_pct', 0) / 100
        if abs(crypto_total - expected_crypto) > 0.01:
            print(f'WARN: Strategy {s[\"id\"]} crypto_pct={s[\"crypto_pct\"]}% but crypto allocations={crypto_total*100}%')

    print('OK: strategies.json is valid (10 strategies, allocations verified)')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1) || true

if echo "$CONFIG_CHECK" | grep -q "^OK:"; then
  print_ok "Configuration files are valid"
else
  print_fail "Configuration validation failed"
  echo "$CONFIG_CHECK"
  ((CRITICAL_ERRORS++)) || true
fi

# ==========================================================================
# CHECK 12: CLI Smoke Test
# ==========================================================================
print_check "12/12: CLI Smoke Test"
CLI_TEST=$(timeout 10 python3 main.py --help 2>&1) || true

if echo "$CLI_TEST" | grep -q "diBoaS Analytics"; then
  print_ok "CLI starts successfully"

  # Check all commands are registered
  EXPECTED_COMMANDS=("collect" "battle-test" "monte-carlo" "monitor" "anomaly" "dream-mode-export" "all")
  for cmd in "${EXPECTED_COMMANDS[@]}"; do
    if ! echo "$CLI_TEST" | grep -q "$cmd"; then
      print_warn "Command '$cmd' not found in help output"
      ((WARNINGS++)) || true
    fi
  done
else
  print_fail "CLI failed to start"
  echo "$CLI_TEST"
  ((CRITICAL_ERRORS++)) || true
fi

# ==========================================================================
# SUMMARY
# ==========================================================================
print_section "AUDIT SUMMARY"

echo ""
echo "Results:"
echo -e "  Critical Errors: ${RED}$CRITICAL_ERRORS${NC}"
echo -e "  Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ "$CRITICAL_ERRORS" -gt 0 ]; then
  echo -e "${RED}CRITICAL ISSUES REQUIRE ATTENTION:${NC}"
  echo "  - Fix syntax errors"
  echo "  - Fix import errors"
  echo "  - Address security vulnerabilities"
  echo "  - Fix failing tests"
  echo "  - Remove any hardcoded secrets"
  echo "  - Ensure all data files are present"
  echo ""
fi

if [ "$WARNINGS" -gt 0 ]; then
  echo -e "${YELLOW}WARNINGS TO REVIEW:${NC}"
  echo "  - Replace print() with logging"
  echo "  - Address TODO comments or document for later"
  echo "  - Fix linting issues"
  echo ""
fi

# Generate config hash for audit trail
echo "Configuration Hash:"
python3 -c "
from src.utils.hashing import hash_config
import json
with open('config/strategies.json') as f:
    data = json.load(f)
print(f'  strategies.json: {hash_config(data)}')
" 2>/dev/null || echo "  (could not generate hash)"

echo ""

# Exit with error code in CI mode if critical errors found
if [ "$CI_MODE" = true ] && [ "$CRITICAL_ERRORS" -gt 0 ]; then
  echo -e "${RED}CI MODE: Failing due to $CRITICAL_ERRORS critical error(s)${NC}"
  exit 1
fi

if [ "$CRITICAL_ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  echo -e "${GREEN}ALL CHECKS PASSED - Ready for release!${NC}"
elif [ "$CRITICAL_ERRORS" -eq 0 ]; then
  echo -e "${YELLOW}PASSED WITH WARNINGS - Review before release${NC}"
fi

echo ""
echo "Audit completed at $(date)"
