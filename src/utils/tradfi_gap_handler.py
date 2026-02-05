"""
TradFi Data Gap Handler.

Handles gaps in traditional finance data caused by:
- Weekends (Saturday/Sunday)
- US Market Holidays (MLK Day, Presidents Day, etc.)
- Pre-market close (data not yet available)

Strategy: Forward-fill with disclosure tracking (max 4 days).
"""

import pandas as pd
from datetime import date, datetime, timedelta
from typing import Dict, Tuple, Optional, List, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class GapType(Enum):
    """Types of TradFi data gaps."""
    NONE = "none"                   # No gap, data is current
    WEEKEND = "weekend"             # Saturday/Sunday
    HOLIDAY = "holiday"             # US Market Holiday
    PRE_MARKET_CLOSE = "pre_market_close"  # Run before 4PM ET
    EXTENDED_GAP = "extended_gap"   # Gap > 4 days (unusual)


# US Market Holidays 2026 (markets closed)
US_HOLIDAYS_2026 = {
    date(2026, 1, 1): "New Year's Day",
    date(2026, 1, 20): "MLK Day",
    date(2026, 2, 17): "Presidents Day",
    date(2026, 4, 3): "Good Friday",
    date(2026, 5, 25): "Memorial Day",
    date(2026, 7, 3): "Independence Day (observed)",
    date(2026, 9, 7): "Labor Day",
    date(2026, 11, 26): "Thanksgiving",
    date(2026, 12, 25): "Christmas",
}

# TradFi columns that need gap handling
TRADFI_COLUMNS = [
    'spy_close', 'qqq_close', 'dia_close', 'iwm_close',
    'gld_close', 'tlt_close', 'hyg_close', 'vix_close'
]

# Maximum forward-fill days (handles long weekends like Thanksgiving)
MAX_FORWARD_FILL_DAYS = 4


@dataclass
class GapMetadata:
    """Metadata about a data gap."""
    has_gap: bool
    gap_type: GapType
    original_date: Optional[date]
    gap_days: int
    columns_filled: List[str]
    holiday_name: Optional[str] = None


def classify_gap(target_date: date, gap_days: int) -> Tuple[GapType, Optional[str]]:
    """
    Classify the type of gap based on date and duration.

    Args:
        target_date: The date we're trying to get data for
        gap_days: Number of days since last data

    Returns:
        Tuple of (GapType, holiday_name or None)
    """
    if gap_days == 0:
        return GapType.NONE, None

    # Check if target date is a weekend
    weekday = target_date.weekday()
    if weekday == 5:  # Saturday
        return GapType.WEEKEND, None
    elif weekday == 6:  # Sunday
        return GapType.WEEKEND, None

    # Check if target date is a US holiday
    if target_date in US_HOLIDAYS_2026:
        return GapType.HOLIDAY, US_HOLIDAYS_2026[target_date]

    # Check if day before was a holiday (gap from holiday)
    yesterday = target_date - timedelta(days=1)
    if yesterday in US_HOLIDAYS_2026:
        return GapType.HOLIDAY, US_HOLIDAYS_2026[yesterday]

    # Check for weekend gap on Monday
    if weekday == 0 and gap_days <= 3:  # Monday with 1-3 day gap
        return GapType.WEEKEND, None

    # If gap is just 1 day on a weekday, likely pre-market close
    if gap_days == 1:
        return GapType.PRE_MARKET_CLOSE, None

    # Check for holiday gaps (typically 1-3 days)
    if gap_days <= 3:
        return GapType.HOLIDAY, None

    # Extended gap (unusual, might indicate data issue)
    if gap_days > MAX_FORWARD_FILL_DAYS:
        return GapType.EXTENDED_GAP, None

    return GapType.HOLIDAY, None


def get_tradfi_value_with_fill(
    df: pd.DataFrame,
    column: str,
    target_date: date
) -> Tuple[Optional[float], Dict[str, Any]]:
    """
    Get TradFi value with business-day forward-fill.

    Args:
        df: DataFrame with date index and TradFi columns
        column: Column name to retrieve
        target_date: Target date for data

    Returns:
        Tuple of (value, metadata dict)
        metadata includes:
          - forward_filled: bool
          - original_date: date used
          - gap_days: int
          - gap_type: str
    """
    df = df.copy()

    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

    target_ts = pd.Timestamp(target_date)

    # Try to get exact date
    if target_ts in df.index:
        value = df.loc[target_ts, column] if column in df.columns else None
        if pd.notna(value):
            return value, {"forward_filled": False, "gap_type": GapType.NONE.value}

    # Forward-fill: get last known value before target_date
    prior_data = df[df.index < target_ts]
    if column in prior_data.columns:
        prior_data = prior_data[prior_data[column].notna()]

    if prior_data.empty:
        return None, {
            "forward_filled": True,
            "error": "No prior data available",
            "gap_type": GapType.EXTENDED_GAP.value
        }

    last_row = prior_data.iloc[-1]
    last_date = last_row.name.date() if hasattr(last_row.name, 'date') else last_row.name
    gap_days = (target_date - last_date).days

    gap_type, holiday_name = classify_gap(target_date, gap_days)

    metadata = {
        "forward_filled": True,
        "original_date": str(last_date),
        "gap_days": gap_days,
        "gap_type": gap_type.value,
    }

    if holiday_name:
        metadata["holiday_name"] = holiday_name

    return last_row[column], metadata


def prepare_tradfi_data(
    df: pd.DataFrame,
    tradfi_columns: List[str] = None
) -> Tuple[pd.DataFrame, GapMetadata]:
    """
    Prepare TradFi data with forward-fill gap handling.

    Forward-fills weekend/holiday gaps but tracks them for disclosure.
    Maximum forward-fill is 4 days to handle long weekends.

    Args:
        df: DataFrame with date column and TradFi data
        tradfi_columns: List of TradFi columns to process (default: TRADFI_COLUMNS)

    Returns:
        Tuple of (prepared DataFrame, GapMetadata)
    """
    tradfi_columns = tradfi_columns or TRADFI_COLUMNS
    df = df.copy()

    # Get columns that exist in this DataFrame
    existing_cols = [c for c in tradfi_columns if c in df.columns]

    if not existing_cols:
        return df, GapMetadata(
            has_gap=False,
            gap_type=GapType.NONE,
            original_date=None,
            gap_days=0,
            columns_filled=[]
        )

    # Forward-fill within a max of 4 days (handles long weekends)
    df[existing_cols] = df[existing_cols].ffill(limit=MAX_FORWARD_FILL_DAYS)

    # Track which rows were filled by comparing original to filled
    # A row is "filled" if it had NaN before and now has a value
    filled_mask = df[existing_cols].isna().any(axis=1)

    # Add tracking column
    df['tradfi_forward_filled'] = filled_mask

    # Determine gap metadata for the most recent gap
    has_gap = filled_mask.any()
    gap_type = GapType.NONE
    original_date = None
    gap_days = 0
    columns_filled = []

    if has_gap:
        # Find the last filled row
        last_filled_idx = filled_mask[filled_mask].index[-1] if filled_mask.any() else None
        if last_filled_idx is not None:
            # Determine which columns were filled
            for col in existing_cols:
                if pd.isna(df.loc[last_filled_idx, col]):
                    columns_filled.append(col)

            # Calculate gap info
            if 'date' in df.columns:
                target_date = pd.to_datetime(df.loc[last_filled_idx, 'date']).date()
            else:
                target_date = last_filled_idx.date() if hasattr(last_filled_idx, 'date') else None

            if target_date:
                gap_type, holiday_name = classify_gap(target_date, 1)

    metadata = GapMetadata(
        has_gap=has_gap,
        gap_type=gap_type,
        original_date=original_date,
        gap_days=gap_days,
        columns_filled=columns_filled
    )

    return df, metadata


def get_complete_rows(
    df: pd.DataFrame,
    required_columns: List[str]
) -> pd.DataFrame:
    """
    Return only rows where all required columns have values.

    Used for correlation calculations where we need complete data.

    Args:
        df: DataFrame to filter
        required_columns: Columns that must have values

    Returns:
        DataFrame with only complete rows
    """
    existing_cols = [c for c in required_columns if c in df.columns]
    if not existing_cols:
        return df
    return df.dropna(subset=existing_cols)


def is_market_closed(target_date: date) -> Tuple[bool, Optional[str]]:
    """
    Check if US stock markets are closed on a given date.

    Args:
        target_date: Date to check

    Returns:
        Tuple of (is_closed: bool, reason: str or None)
    """
    weekday = target_date.weekday()

    # Weekend
    if weekday == 5:
        return True, "Saturday"
    if weekday == 6:
        return True, "Sunday"

    # Holiday
    if target_date in US_HOLIDAYS_2026:
        return True, US_HOLIDAYS_2026[target_date]

    return False, None


def get_last_trading_day(target_date: date) -> date:
    """
    Get the last trading day on or before the target date.

    Args:
        target_date: Starting date

    Returns:
        Most recent trading day
    """
    current = target_date
    max_lookback = 7  # Maximum days to look back

    for _ in range(max_lookback):
        is_closed, _ = is_market_closed(current)
        if not is_closed:
            return current
        current -= timedelta(days=1)

    # Fallback (shouldn't happen)
    logger.warning(f"Could not find trading day within {max_lookback} days of {target_date}")
    return target_date
