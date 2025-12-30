"""
Date utilities for diBoaS Analytics.
"""

from datetime import date, datetime, timedelta
from typing import Optional, Iterator
import pandas as pd


def parse_date(date_str: str) -> date:
    """
    Parse a date string in various formats.

    Supports: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, etc.
    """
    formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%Y%m%d',
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Could not parse date: {date_str}")


def date_range(
    start: date,
    end: date,
    inclusive: bool = True
) -> Iterator[date]:
    """
    Generate dates in a range.

    Args:
        start: Start date
        end: End date
        inclusive: Whether to include end date

    Yields:
        Each date in the range
    """
    current = start
    end_date = end if inclusive else end - timedelta(days=1)

    while current <= end_date:
        yield current
        current += timedelta(days=1)


def trading_days(
    start: date,
    end: date,
    exclude_weekends: bool = False
) -> list[date]:
    """
    Get list of trading days in a range.

    For crypto, all days are trading days. For traditional markets,
    weekends can be excluded.

    Args:
        start: Start date
        end: End date
        exclude_weekends: Whether to exclude weekends

    Returns:
        List of trading days
    """
    days = list(date_range(start, end))

    if exclude_weekends:
        days = [d for d in days if d.weekday() < 5]

    return days


def count_days(start: date, end: date) -> int:
    """Count days between two dates (inclusive)."""
    return (end - start).days + 1


def count_months(start: date, end: date) -> int:
    """Count complete months between two dates."""
    return (end.year - start.year) * 12 + (end.month - start.month)


def is_month_start(d: date) -> bool:
    """Check if date is the start of a month."""
    return d.day == 1


def is_month_end(d: date) -> bool:
    """Check if date is the end of a month."""
    next_day = d + timedelta(days=1)
    return next_day.month != d.month


def get_month_dates(year: int, month: int) -> tuple[date, date]:
    """Get first and last date of a month."""
    first = date(year, month, 1)
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return first, last


def align_to_month_boundaries(
    start: date,
    end: date
) -> tuple[date, date]:
    """
    Align dates to month boundaries.

    Start is moved to first of month, end to last of month.
    """
    aligned_start = date(start.year, start.month, 1)

    if end.month == 12:
        aligned_end = date(end.year + 1, 1, 1) - timedelta(days=1)
    else:
        aligned_end = date(end.year, end.month + 1, 1) - timedelta(days=1)

    return aligned_start, aligned_end


def format_date(d: date, fmt: str = '%Y-%m-%d') -> str:
    """Format a date to string."""
    return d.strftime(fmt)


def format_duration(days: int) -> str:
    """Format duration in human-readable form."""
    if days < 7:
        return f"{days} days"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''}"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''}"
    else:
        years = days / 365
        return f"{years:.1f} years"
