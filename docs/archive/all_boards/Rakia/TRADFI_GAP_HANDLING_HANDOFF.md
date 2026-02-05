# CTO/QR Board Handoff: TradFi Data Gap Handling

**Document:** TRADFI_GAP_HANDLING_HANDOFF.md  
**Created:** February 4, 2026  
**From:** Rakia Board  
**To:** CTO Board + QR Board  
**Priority:** P0 (Pre-Launch Verification)

---

## 1. ISSUE SUMMARY

During the Feb 3, 2026 full run review, we observed sparse data in `tradfi_benchmark_data.csv`:

```csv
date,spy_close,qqq_close,vix_close,dia_close,iwm_close,gld_close,tlt_close,hyg_close
2026-02-02,6976.43,23592.10,16.34,695.40,86.55,262.17,54.02,42.61
2026-02-03,,,16.30,,,,,
```

**SPY, QQQ, DIA, IWM, GLD, TLT, HYG** are empty for Feb 3, while **VIX** is populated.

### 1.1 Root Cause

This is **expected behavior** for TradFi data:
- Stock exchanges are closed on weekends and holidays
- The run happened before market close (4PM ET) on Feb 3
- VIX is available because CBOE publishes intraday values

### 1.2 Impact on Engines

The question is: **How should engines (Battle Test, Monte Carlo, Regime Classifier) handle these gaps?**

---

## 2. TRADFI DATA CHARACTERISTICS

### 2.1 Market Hours and Availability

| Data Type | Trading Hours | Update Frequency | Weekend/Holiday |
|-----------|---------------|------------------|-----------------|
| US Equities (SPY, QQQ, IWM, DIA) | 9:30 AM - 4:00 PM ET | EOD | NO DATA |
| VIX | 9:30 AM - 4:15 PM ET | Near real-time | NO DATA (but may have delayed) |
| Treasury ETFs (TLT) | 9:30 AM - 4:00 PM ET | EOD | NO DATA |
| Bond ETFs (HYG) | 9:30 AM - 4:00 PM ET | EOD | NO DATA |
| Gold ETF (GLD) | 9:30 AM - 4:00 PM ET | EOD | NO DATA |
| FRED Data (Yields, M2) | N/A | Business day EOD | NO DATA |
| Crypto | 24/7 | Real-time | ALWAYS AVAILABLE |
| DeFi APYs | 24/7 | ~15 min | ALWAYS AVAILABLE |

### 2.2 Expected Gap Patterns

| Gap Type | Frequency | Example |
|----------|-----------|---------|
| Weekend | Every week | Sat-Sun no data |
| US Market Holiday | ~10/year | MLK Day, Presidents Day, etc. |
| Pre-market close | Daily if run before 4PM ET | Today's SPY empty until 4PM |
| Fed data release delay | Occasional | FRED updates ~3PM ET |

### 2.3 US Market Holidays 2026

| Date | Holiday |
|------|---------|
| Jan 1 | New Year's Day |
| Jan 20 | MLK Day |
| Feb 17 | Presidents Day |
| Apr 3 | Good Friday |
| May 25 | Memorial Day |
| Jul 3 | Independence Day (observed) |
| Sep 7 | Labor Day |
| Nov 26 | Thanksgiving |
| Dec 25 | Christmas |

---

## 3. RECOMMENDED HANDLING STRATEGIES

### 3.1 Option A: Forward-Fill with Disclosure (RECOMMENDED)

**Approach:** Use the last known value for missing days, but track and disclose.

```python
def get_tradfi_value_with_fill(
    df: pd.DataFrame,
    column: str,
    target_date: date
) -> Tuple[float, Dict]:
    """
    Get TradFi value with business-day forward-fill.
    
    Returns:
        Tuple of (value, metadata)
        metadata includes:
          - forward_filled: bool
          - original_date: date used
          - gap_days: int
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Try to get exact date
    exact = df.loc[df['date'] == pd.Timestamp(target_date), column]
    
    if not exact.empty and not pd.isna(exact.iloc[0]):
        return exact.iloc[0], {"forward_filled": False}
    
    # Forward-fill: get last known value before target_date
    prior_data = df[df['date'] < pd.Timestamp(target_date)]
    prior_data = prior_data[prior_data[column].notna()]
    
    if prior_data.empty:
        return None, {"forward_filled": True, "error": "No prior data"}
    
    last_row = prior_data.iloc[-1]
    gap_days = (target_date - last_row['date'].date()).days
    
    return last_row[column], {
        "forward_filled": True,
        "original_date": str(last_row['date'].date()),
        "gap_days": gap_days,
        "gap_type": _classify_gap(target_date, gap_days)
    }


def _classify_gap(target_date: date, gap_days: int) -> str:
    """Classify the type of gap."""
    weekday = target_date.weekday()
    
    if weekday == 5:  # Saturday
        return "weekend"
    elif weekday == 6:  # Sunday
        return "weekend"
    elif gap_days == 1:
        return "pre_market_close"  # Data not yet available
    elif gap_days <= 3:
        return "holiday"
    else:
        return "extended_gap"
```

**Pros:**
- Engines continue to work without crashing
- Disclosure provides transparency
- Consistent with how financial systems handle gaps

**Cons:**
- Slightly outdated data used

### 3.2 Option B: Skip Days with Missing Data

**Approach:** Only process days with complete data.

```python
def get_complete_rows(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
    """Return only rows where all required columns have values."""
    return df.dropna(subset=required_columns)
```

**Pros:**
- Only uses actual data points
- No risk of stale data

**Cons:**
- Battle Test may skip weekends entirely
- Monte Carlo correlation matrices may be affected

### 3.3 Option C: Hybrid Approach

**Approach:** Use Option A for most calculations, but Option B for specific scenarios.

| Calculation | Handling |
|-------------|----------|
| Daily returns | Forward-fill (gap counts as 0% return) |
| Volatility | Skip missing days |
| Correlation | Skip missing days |
| Moving averages | Forward-fill |
| Regime classification | Forward-fill with disclosure |

---

## 4. ENGINE-SPECIFIC RECOMMENDATIONS

### 4.1 Battle Test (`src/engines/battle_test.py`)

**Current Behavior:** Unknown — needs verification  
**Recommended Behavior:** Forward-fill with disclosure

```python
class BattleTest:
    def _prepare_tradfi_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare TradFi data with gap handling.
        
        Forward-fills weekend/holiday gaps but tracks them.
        """
        tradfi_columns = ['spy_close', 'qqq_close', 'dia_close', 'iwm_close']
        
        # Forward-fill within a max of 4 days (handles long weekends)
        df[tradfi_columns] = df[tradfi_columns].fillna(method='ffill', limit=4)
        
        # Track which rows were filled
        df['tradfi_forward_filled'] = df[tradfi_columns].isna().any(axis=1)
        
        return df
```

**Verification Required:**
- [ ] Check how battle_test.py handles NaN values in TradFi columns
- [ ] Verify it doesn't crash on weekend gaps
- [ ] Confirm returns are calculated correctly across gaps

### 4.2 Monte Carlo (`src/engines/monte_carlo.py`)

**Current Behavior:** Unknown — needs verification  
**Recommended Behavior:** Skip missing days for correlation, forward-fill for simulation

```python
class MonteCarlo:
    def _calculate_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate correlation matrix excluding days with missing TradFi data.
        """
        # Use only complete rows for correlation
        complete = df.dropna(subset=self.tradfi_columns)
        return complete[self.correlation_columns].corr()
    
    def _simulate_path(self, ...):
        """
        Simulate price path using forward-filled data.
        Weekend/holiday gaps are treated as 0% return days.
        """
        # Forward-fill for simulation continuity
        df_filled = df.fillna(method='ffill')
        # ... simulation logic
```

**Verification Required:**
- [ ] Check how monte_carlo.py calculates correlations
- [ ] Verify simulation doesn't crash on gaps
- [ ] Confirm weekend gaps don't artificially reduce volatility

### 4.3 Regime Classifier (`src/adelaide/regime_classifier.py`)

**Current Behavior:** Unknown — needs verification  
**Recommended Behavior:** Forward-fill with "last known regime" persistence

```python
class RegimeClassifier:
    def classify(self, data: Dict) -> str:
        """
        Classify current market regime.
        
        If TradFi data is missing (weekend/holiday/pre-close),
        returns last known regime with disclosure flag.
        """
        spy_close = data.get('spy_close')
        vix_close = data.get('vix_close')
        
        # Check for missing TradFi data
        if spy_close is None or pd.isna(spy_close):
            return self._get_last_known_regime(), {
                "disclosure": "Using last known regime due to TradFi gap",
                "gap_type": "pre_market_close"
            }
        
        # Normal classification logic
        return self._classify_regime(data)
```

**Verification Required:**
- [ ] Check how regime_classifier.py handles missing SPY/VIX
- [ ] Verify it doesn't produce invalid regimes on weekends
- [ ] Confirm Adelaide can generate on weekends using last known regime

### 4.4 Anomaly Detection (`src/engines/anomaly.py`)

**Current Behavior:** Unknown — needs verification  
**Recommended Behavior:** Exclude gaps from anomaly detection

```python
class AnomalyDetector:
    def detect(self, df: pd.DataFrame) -> List[Anomaly]:
        """
        Detect anomalies, excluding known TradFi gaps.
        """
        # Don't flag weekend/holiday gaps as anomalies
        df = df[~df['tradfi_forward_filled']]
        
        # Normal anomaly detection on complete data
        return self._detect_anomalies(df)
```

**Verification Required:**
- [ ] Check that weekends aren't flagged as "missing data" anomalies
- [ ] Verify legitimate anomalies are still detected

---

## 5. VERIFICATION CHECKLIST FOR CTO/QR BOARD

### 5.1 Battle Test Verification

| # | Test | Command | Expected | Actual | Pass? |
|---|------|---------|----------|--------|-------|
| BT1 | Run battle test on data with weekend gaps | `python main.py battle-test` | Completes without error | | ☐ |
| BT2 | Check returns calculation across weekend | Manual inspection | Fri-Mon return correct | | ☐ |
| BT3 | Verify scenarios include gap handling | Code review | Forward-fill logic present | | ☐ |

### 5.2 Monte Carlo Verification

| # | Test | Command | Expected | Actual | Pass? |
|---|------|---------|----------|--------|-------|
| MC1 | Run Monte Carlo on data with weekend gaps | `python main.py monte-carlo` | Completes without error | | ☐ |
| MC2 | Check correlation matrix excludes gaps | Code review | dropna before corr() | | ☐ |
| MC3 | Verify volatility isn't artificially low | Compare to actual | Within 10% of expected | | ☐ |

### 5.3 Regime Classifier Verification

| # | Test | Command | Expected | Actual | Pass? |
|---|------|---------|----------|--------|-------|
| RC1 | Run classifier on Saturday | Manual test | Returns last known regime | | ☐ |
| RC2 | Run classifier pre-market close | Manual test | Uses available data (VIX) | | ☐ |
| RC3 | Check disclosure flag present | Code review | Metadata tracks gaps | | ☐ |

### 5.4 Adelaide Generation Verification

| # | Test | Command | Expected | Actual | Pass? |
|---|------|---------|----------|--------|-------|
| AD1 | Generate Adelaide on Saturday | `python main.py adelaide` | Completes with disclosure | | ☐ |
| AD2 | Check weekend output mentions data age | Output inspection | "Based on Friday's close" | | ☐ |
| AD3 | Generate Adelaide pre-market | `python main.py adelaide` | Uses available data | | ☐ |

---

## 6. IMPLEMENTATION RECOMMENDATIONS

### 6.1 Minimum Viable (Pre-Launch)

1. **Add forward-fill to engines** — Use `fillna(method='ffill', limit=4)` in data prep
2. **Add disclosure flag** — Track when forward-fill was used
3. **Don't flag gaps as anomalies** — Exclude weekends from anomaly detection

**Effort:** 0.5 day

### 6.2 Full Implementation (Post-Launch)

1. **Gap classification** — Distinguish weekend vs holiday vs pre-close
2. **Metadata tracking** — Log all gaps in collection_metadata.json
3. **Adelaide disclosure** — Add "Data as of Friday close" when appropriate
4. **API endpoint** — Add `/api/data-status` to show latest data availability

**Effort:** 1-2 days

---

## 7. ACTION ITEMS

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Verify Battle Test gap handling | CTO Board | Feb 6 |
| 2 | Verify Monte Carlo gap handling | QR Board | Feb 6 |
| 3 | Verify Regime Classifier gap handling | CTO Board | Feb 6 |
| 4 | Add forward-fill to engines if missing | CTO Board | Feb 8 |
| 5 | Add disclosure tracking | CTO Board | Feb 8 |
| 6 | Test Adelaide weekend generation | CMO Board | Feb 9 |

---

## 8. QUESTIONS FOR BAR

1. **Weekend Adelaide:** Should we generate Adelaide on weekends using Friday's data with disclosure, or skip weekend editions entirely?

2. **Holiday handling:** Same question for market holidays — generate with disclosure or skip?

3. **Disclosure format:** How should Adelaide communicate data gaps? Options:
   - A) "Market data as of Friday, February 6" (subtle)
   - B) "Note: US markets were closed today" (explicit)
   - C) Different template for weekend editions

---

*Handoff document created by Rakia Board for CTO/QR Board verification*
