# Claude Code Data Collection Verification Checklist

**Document:** CLAUDE_CODE_DATA_COLLECTION_VERIFICATION.md  
**Created:** February 4, 2026  
**Author:** Rakia Board  
**Purpose:** Verification checklist for Claude Code implementation of data collection enhancements

---

## 1. APPEND-ONLY BEHAVIOR VERIFICATION

### 1.1 Current State Audit

| # | Check | Command/Location | Expected | Actual | Pass? |
|---|-------|------------------|----------|--------|-------|
| A1 | Check if `--append` flag exists in CLI | `main.py` argparse | Flag defined | | ☐ |
| A2 | Check if `collect.py` handles `--append` | `src/commands/collect.py` | Append logic exists | | ☐ |
| A3 | Check if collectors have `save_to_csv_incremental()` | `src/collectors/*.py` | Method exists | | ☐ |
| A4 | Check `daily_run.sh` uses `--append` | `scripts/daily_run.sh` | `--append` flag present | | ☐ |
| A5 | Check `first_run.sh` does NOT use `--append` | `scripts/first_run.sh` | No `--append` (full backfill) | | ☐ |

### 1.2 Required Implementation

If checks A1-A4 fail, implement the following:

#### 1.2.1 Base Collector Interface Update

**File:** `src/collectors/base.py`

```python
class DataProvider(ABC):
    # ... existing methods ...
    
    def get_last_date(self, file_path: Path) -> Optional[date]:
        """
        Get the last date in existing data file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Last date in file, or None if file doesn't exist/empty
        """
        if not file_path.exists():
            return None
        
        df = pd.read_csv(file_path)
        if df.empty or 'date' not in df.columns:
            return None
        
        df['date'] = pd.to_datetime(df['date'])
        return df['date'].max().date()
    
    def save_incremental(
        self,
        new_data: pd.DataFrame,
        file_path: Path,
        date_column: str = 'date'
    ) -> int:
        """
        Append new data to existing file, avoiding duplicates.
        
        Args:
            new_data: New data to append
            file_path: Path to CSV file
            date_column: Name of date column
            
        Returns:
            Number of rows appended
        """
        if new_data.empty:
            return 0
        
        if not file_path.exists():
            new_data.to_csv(file_path, index=False)
            return len(new_data)
        
        existing = pd.read_csv(file_path)
        existing[date_column] = pd.to_datetime(existing[date_column])
        new_data[date_column] = pd.to_datetime(new_data[date_column])
        
        # Get only rows newer than existing data
        last_existing = existing[date_column].max()
        new_rows = new_data[new_data[date_column] > last_existing]
        
        if new_rows.empty:
            return 0
        
        # Append to file
        new_rows.to_csv(file_path, mode='a', header=False, index=False)
        return len(new_rows)
```

#### 1.2.2 Collector Implementation Pattern

**Each collector should implement:**

```python
def save_to_csv_incremental(self, output_dir: str) -> dict:
    """
    Incremental save - only append new data.
    
    1. Check last date in existing file
    2. Fetch data from last_date + 1 to today
    3. Append new rows only
    """
    from pathlib import Path
    output_path = Path(output_dir)
    
    results = {}
    
    for filename, fetch_method in self.FILE_METHODS.items():
        file_path = output_path / filename
        last_date = self.get_last_date(file_path)
        
        if last_date is None:
            # No existing data - do full fetch
            start_date = self.config.get('backfill_start', date(2000, 1, 1))
        else:
            # Incremental - fetch from next day
            start_date = last_date + timedelta(days=1)
        
        if start_date > date.today():
            results[filename] = {'status': 'up_to_date', 'rows_added': 0}
            continue
        
        new_data = fetch_method(start_date, date.today())
        rows_added = self.save_incremental(new_data, file_path)
        
        results[filename] = {'status': 'updated', 'rows_added': rows_added}
    
    return results
```

#### 1.2.3 Daily Run Script Update

**File:** `scripts/daily_run.sh`

```bash
#!/bin/bash
# Daily data collection - INCREMENTAL MODE
# Only appends new data, never overwrites historical

set -e

echo "=== diBoaS Analytics Daily Run ==="
echo "Mode: INCREMENTAL (append-only)"
echo "Date: $(date)"

cd "$(dirname "$0")/.."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run collection with --append flag
python main.py collect --source all --append --output data/

# Run validation
python main.py validate-gate1 --data data/

# Log completion
echo "Daily run complete at $(date)" >> outputs/logs/daily_runs.log
```

#### 1.2.4 First Run Script (Full Backfill)

**File:** `scripts/first_run.sh`

```bash
#!/bin/bash
# First-time data collection - FULL BACKFILL MODE
# Fetches complete historical data from earliest available

set -e

echo "=== diBoaS Analytics First Run ==="
echo "Mode: FULL BACKFILL"
echo "WARNING: This will overwrite existing data files"
echo "Date: $(date)"

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

cd "$(dirname "$0")/.."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run full backfill (no --append flag)
python main.py collect --source all --output data/

# Run validation
python main.py validate-gate1 --data data/

echo "First run complete at $(date)"
```

### 1.3 Verification Tests

After implementation, run these tests:

```bash
# Test 1: Check CSV row count before and after daily run
wc -l data/crypto_prices.csv  # Note count
python main.py collect --source all --append --output data/
wc -l data/crypto_prices.csv  # Should be +1 row (or same if already today)

# Test 2: Verify no data loss
# Compare checksums of historical rows
head -100 data/crypto_prices.csv > /tmp/before.csv
python main.py collect --source all --append --output data/
head -100 data/crypto_prices.csv > /tmp/after.csv
diff /tmp/before.csv /tmp/after.csv  # Should be identical

# Test 3: Verify append behavior
tail -5 data/crypto_prices.csv  # Check last dates before
python main.py collect --source all --append --output data/
tail -5 data/crypto_prices.csv  # Should have new date appended
```

---

## 2. HISTORICAL DATA EXTENSION VERIFICATION

### 2.1 FRED Series Start Dates

| # | Series | FRED Code | Expected Start | Actual Start | Pass? |
|---|--------|-----------|----------------|--------------|-------|
| F1 | Treasury 2Y | DGS2 | 1976-06-01 | | ☐ |
| F2 | Treasury 5Y | DGS5 | 1962-01-02 | | ☐ |
| F3 | Treasury 10Y | DGS10 | 1962-01-02 | | ☐ |
| F4 | Treasury 30Y | DGS30 | 1977-02-15 | | ☐ |
| F5 | Real Yield 10Y | DFII10 | 2003-01-02 | | ☐ |
| F6 | M2 Money Supply | M2SL | 1959-01-01 | | ☐ |
| F7 | Fed Balance Sheet | WALCL | 2002-12-18 | | ☐ |
| F8 | HY Credit Spread | BAMLH0A0HYM2 | 1996-12-31 | | ☐ |
| F9 | IG Credit Spread | BAMLC0A4CBBB | 1996-12-31 | | ☐ |
| F10 | Breakeven Inflation | T10YIE | 2003-01-02 | | ☐ |
| F11 | NFCI | NFCI | 1971-01-08 | | ☐ |
| F12 | Unemployment | UNRATE | 1948-01-01 | | ☐ |
| F13 | CPI | CPIAUCSL | 1947-01-01 | | ☐ |

### 2.2 Yahoo Finance Start Dates

| # | Asset | Ticker | Expected Start | Actual Start | Pass? |
|---|-------|--------|----------------|--------------|-------|
| Y1 | S&P 500 ETF | SPY | 1993-01-29 | | ☐ |
| Y2 | Nasdaq 100 ETF | QQQ | 1999-03-10 | | ☐ |
| Y3 | Russell 2000 ETF | IWM | 2000-05-26 | | ☐ |
| Y4 | Dow Jones ETF | DIA | 1998-01-20 | | ☐ |
| Y5 | VIX | ^VIX | 1990-01-02 | | ☐ |
| Y6 | Bitcoin | BTC-USD | 2014-09-17 | | ☐ |
| Y7 | Ethereum | ETH-USD | 2017-11-09 | | ☐ |
| Y8 | Solana | SOL-USD | 2020-04-10 | | ☐ |
| Y9 | Gold | GC=F | 1979-12-31 | | ☐ |
| Y10 | Silver | SI=F | 1979-12-31 | | ☐ |
| Y11 | WTI Oil | CL=F | 1983-03-30 | | ☐ |
| Y12 | Natural Gas | NG=F | 1990-04-03 | | ☐ |
| Y13 | Copper | HG=F | 1988-09-01 | | ☐ |
| Y14 | Corn | ZC=F | 1959-07-01 | | ☐ |
| Y15 | Wheat | ZW=F | 1959-07-01 | | ☐ |
| Y16 | Soybeans | ZS=F | 1959-11-02 | | ☐ |
| Y17 | Dollar Index | DX-Y.NYB | 1985-01-02 | | ☐ |

### 2.3 Verification Commands

```bash
# Check earliest date in each file
for f in data/*.csv; do
    echo "=== $f ==="
    head -2 "$f"
    echo ""
done

# Specific checks
head -2 data/treasury_yields.csv    # Should start 1962 or 1976
head -2 data/commodities.csv        # Should start 1959 (corn) or 1979 (gold)
head -2 data/crypto_prices.csv      # Should start 2014 (BTC)
head -2 data/macro_indicators.csv   # Should start 1947 (CPI)
```

---

## 3. NEW COMMODITIES VERIFICATION

### 3.1 commodities.csv Schema

| # | Column | Expected | Present? | Valid Range? |
|---|--------|----------|----------|--------------|
| C1 | date | DATE | ☐ | N/A |
| C2 | gold_usd | FLOAT | ☐ | 100-10000 |
| C3 | silver_usd | FLOAT | ☐ | 1-200 |
| C4 | oil_wti_usd | FLOAT | ☐ | 0-300 |
| C5 | natural_gas_usd | FLOAT | ☐ | 0-50 |
| C6 | copper_usd | FLOAT | ☐ | 0-20 |
| C7 | corn_usd | FLOAT | ☐ | 0-2000 |
| C8 | wheat_usd | FLOAT | ☐ | 0-2000 |
| C9 | soybeans_usd | FLOAT | ☐ | 0-3000 |
| C10 | dxy_index | FLOAT | ☐ | 50-200 |

### 3.2 Verification Command

```bash
# Check commodities columns
head -1 data/commodities.csv
# Expected: date,gold_usd,silver_usd,oil_wti_usd,natural_gas_usd,copper_usd,corn_usd,wheat_usd,soybeans_usd,dxy_index

# Check row count (should be ~11,000+ for full history)
wc -l data/commodities.csv
```

---

## 4. NEW MACRO INDICATORS FILE VERIFICATION

### 4.1 macro_indicators.csv Schema

| # | Column | Expected | Present? | Valid Range? |
|---|--------|----------|----------|--------------|
| M1 | date | DATE | ☐ | N/A |
| M2 | breakeven_inflation_10y | FLOAT | ☐ | -5 to 10 |
| M3 | nfci | FLOAT | ☐ | -5 to 5 |
| M4 | unemployment_rate | FLOAT | ☐ | 0-30 |
| M5 | cpi_yoy | FLOAT | ☐ | -20 to 30 |

### 4.2 Verification Command

```bash
# Check file exists and has correct columns
head -1 data/macro_indicators.csv
# Expected: date,breakeven_inflation_10y,nfci,unemployment_rate,cpi_yoy

# Check row count (should be ~20,000+ for full history back to 1947)
wc -l data/macro_indicators.csv

# Check date range
head -2 data/macro_indicators.csv  # Should start 1947
tail -2 data/macro_indicators.csv  # Should end today
```

---

## 5. SCHEMA UPDATES VERIFICATION

### 5.1 gate1_schema_definitions.py Updates

| # | Schema | Change | Verified? |
|---|--------|--------|-----------|
| S1 | commodities.csv | 9 columns (was 2) | ☐ |
| S2 | commodities.csv | min_rows = 1000 | ☐ |
| S3 | macro_indicators.csv | NEW schema added | ☐ |
| S4 | macro_indicators.csv | 5 columns defined | ☐ |

### 5.2 Verification Command

```bash
# Run Gate 1 validation on all files
python main.py validate-gate1 --data data/

# Expected: All files PASS
```

---

## 6. FINAL SIGN-OFF

| Category | Status | Verified By | Date |
|----------|--------|-------------|------|
| Append-only implementation | ☐ PASS / ☐ FAIL | | |
| Historical FRED extension | ☐ PASS / ☐ FAIL | | |
| Historical Yahoo extension | ☐ PASS / ☐ FAIL | | |
| New commodities added | ☐ PASS / ☐ FAIL | | |
| macro_indicators.csv created | ☐ PASS / ☐ FAIL | | |
| Schema updates applied | ☐ PASS / ☐ FAIL | | |
| Gate 1 validation passes | ☐ PASS / ☐ FAIL | | |

**Overall Status:** ☐ READY FOR PRODUCTION / ☐ NEEDS FIXES

---

*Document created by Rakia Board for Claude Code implementation verification*
