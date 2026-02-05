"""
Freshness SLA definitions for Adelaide editions.

Adelaide Pulse (daily) requires tighter SLAs for real-time market data.
Adelaide Weekly allows standard 24h SLAs for most data.

Implementation based on: docs/all_boards/Rakia/DUAL_FRESHNESS_SLAS_SPEC.md
"""

from typing import Dict, List


# SLA values in hours
FRESHNESS_SLAS: Dict[str, Dict[str, int]] = {

    # Adelaide Pulse (Daily) - Tighter SLAs
    "pulse": {
        # Critical real-time data (4h SLA)
        "crypto_prices.csv": 4,
        "sentiment_indicators.csv": 4,
        "tradfi_benchmark_data.csv": 4,

        # DeFi data (8h SLA - updates less frequently)
        "defillama_historical_apy.csv": 8,
        "jito_historical_apy.csv": 8,
        "jupiter_jlp_historical_apy.csv": 8,

        # Macro data (24h SLA - daily updates OK)
        "treasury_yields.csv": 24,
        "real_yields.csv": 24,
        "credit_spreads.csv": 24,
        "commodities.csv": 24,
        "rotation_indicators.csv": 24,

        # Wallet data (168h SLA - weekly updates OK)
        "estate_wallet_tracker.csv": 168,
        "whale_wallet_master_list.csv": 168,
        "market_maker_wallet_tracker.csv": 168,
        "protocol_treasury_tracker.csv": 168,

        # Institutional data (168h+ SLA)
        "btc_etf_holdings.csv": 168,
        "corporate_btc_holdings.csv": 168,
        "institutional_13f.csv": 720,  # 30 days - quarterly filings
        "aaii_sentiment.csv": 168,
        "global_liquidity.csv": 168,
    },

    # Adelaide Weekly - Standard SLAs
    "weekly": {
        # All data gets standard 24h SLA for weekly edition
        "crypto_prices.csv": 24,
        "sentiment_indicators.csv": 24,
        "tradfi_benchmark_data.csv": 24,
        "defillama_historical_apy.csv": 24,
        "jito_historical_apy.csv": 24,
        "jupiter_jlp_historical_apy.csv": 24,
        "treasury_yields.csv": 24,
        "real_yields.csv": 24,
        "credit_spreads.csv": 24,
        "commodities.csv": 24,
        "rotation_indicators.csv": 48,

        # Wallet data - weekly OK
        "estate_wallet_tracker.csv": 168,
        "whale_wallet_master_list.csv": 168,
        "market_maker_wallet_tracker.csv": 168,
        "protocol_treasury_tracker.csv": 168,

        # Institutional data
        "btc_etf_holdings.csv": 168,
        "corporate_btc_holdings.csv": 168,
        "institutional_13f.csv": 720,
        "aaii_sentiment.csv": 168,
        "global_liquidity.csv": 168,
    }
}

# Default SLA if file not in config
DEFAULT_SLA_HOURS = 24

# Critical files that MUST pass freshness for Pulse
PULSE_CRITICAL_FILES: List[str] = [
    "crypto_prices.csv",
    "sentiment_indicators.csv",
]

# Critical files that MUST pass freshness for Weekly
WEEKLY_CRITICAL_FILES: List[str] = [
    "crypto_prices.csv",
    "defillama_historical_apy.csv",
    "treasury_yields.csv",
]


def get_sla(filename: str, edition: str = "weekly") -> int:
    """
    Get freshness SLA for a file based on edition type.

    Args:
        filename: Name of the CSV file
        edition: "pulse" or "weekly"

    Returns:
        SLA in hours
    """
    edition_slas = FRESHNESS_SLAS.get(edition, FRESHNESS_SLAS["weekly"])
    return edition_slas.get(filename, DEFAULT_SLA_HOURS)


def get_critical_files(edition: str = "weekly") -> List[str]:
    """
    Get list of critical files that must pass freshness check.

    Args:
        edition: "pulse" or "weekly"

    Returns:
        List of critical filenames
    """
    if edition == "pulse":
        return PULSE_CRITICAL_FILES.copy()
    return WEEKLY_CRITICAL_FILES.copy()


def get_all_tracked_files() -> List[str]:
    """
    Get list of all files tracked by freshness SLAs.

    Returns:
        List of all tracked filenames
    """
    return list(FRESHNESS_SLAS["weekly"].keys())


def is_critical_file(filename: str, edition: str = "weekly") -> bool:
    """
    Check if a file is critical for the given edition.

    Args:
        filename: Name of the CSV file
        edition: "pulse" or "weekly"

    Returns:
        True if file is critical, False otherwise
    """
    critical_files = get_critical_files(edition)
    return filename in critical_files
