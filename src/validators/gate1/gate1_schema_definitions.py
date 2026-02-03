"""
Schema definitions for all 20 CSV files.

From VALIDATION_GATES_CTO_HANDOFF_v2.md Section 3.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ColumnType(Enum):
    """Supported column data types."""
    STRING = "string"
    FLOAT = "float"
    INTEGER = "integer"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"


@dataclass
class ColumnSchema:
    """Schema definition for a single column."""
    name: str
    type: ColumnType
    required: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[str]] = None


@dataclass
class FileSchema:
    """Schema definition for a CSV file."""
    filename: str
    columns: List[ColumnSchema]
    min_rows: int = 1
    max_age_hours: int = 48
    date_column: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# SCHEMA DEFINITIONS FOR ALL 20 CSV FILES
# ─────────────────────────────────────────────────────────────────────────────

GATE1_SCHEMAS: Dict[str, FileSchema] = {

    # ── MACRO ECONOMICS ──────────────────────────────────────────────────────

    "treasury_yields.csv": FileSchema(
        filename="treasury_yields.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("us_2y", ColumnType.FLOAT, min_value=0, max_value=20),
            ColumnSchema("us_10y", ColumnType.FLOAT, min_value=0, max_value=20),
            ColumnSchema("us_30y", ColumnType.FLOAT, min_value=0, max_value=20),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    "real_yields.csv": FileSchema(
        filename="real_yields.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("us_10y_real", ColumnType.FLOAT, min_value=-5, max_value=10),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    "global_liquidity.csv": FileSchema(
        filename="global_liquidity.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("m2_usd_trillion", ColumnType.FLOAT, min_value=0),
            ColumnSchema("fed_balance_sheet", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=50,
        max_age_hours=168,
        date_column="date"
    ),

    "credit_spreads.csv": FileSchema(
        filename="credit_spreads.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("ig_spread_bps", ColumnType.FLOAT, min_value=0, max_value=1000),
            ColumnSchema("hy_spread_bps", ColumnType.FLOAT, min_value=0, max_value=3000),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    "commodities.csv": FileSchema(
        filename="commodities.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("gold_usd", ColumnType.FLOAT, min_value=500, max_value=5000),
            ColumnSchema("oil_wti_usd", ColumnType.FLOAT, min_value=0, max_value=300),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    # ── TRADFI MARKETS ───────────────────────────────────────────────────────

    "tradfi_benchmark_data.csv": FileSchema(
        filename="tradfi_benchmark_data.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("spy_close", ColumnType.FLOAT, min_value=0),
            ColumnSchema("qqq_close", ColumnType.FLOAT, min_value=0),
            ColumnSchema("vix_close", ColumnType.FLOAT, min_value=0, max_value=100),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    "rotation_indicators.csv": FileSchema(
        filename="rotation_indicators.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("risk_on_score", ColumnType.FLOAT, min_value=-1, max_value=1),
        ],
        min_rows=50,
        max_age_hours=48,
        date_column="date"
    ),

    # ── CRYPTO PRICES ────────────────────────────────────────────────────────

    "crypto_prices.csv": FileSchema(
        filename="crypto_prices.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("btc_usd", ColumnType.FLOAT, min_value=0),
            ColumnSchema("eth_usd", ColumnType.FLOAT, min_value=0),
            ColumnSchema("sol_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=100,
        max_age_hours=4,
        date_column="date"
    ),

    # ── DEFI APY DATA ────────────────────────────────────────────────────────

    "defillama_historical_apy.csv": FileSchema(
        filename="defillama_historical_apy.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("protocol", ColumnType.STRING),
            ColumnSchema("pool", ColumnType.STRING),
            ColumnSchema("apy", ColumnType.FLOAT, min_value=-100, max_value=10000),
            ColumnSchema("tvl_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=100,
        max_age_hours=24,
        date_column="date"
    ),

    "jupiter_jlp_historical_apy.csv": FileSchema(
        filename="jupiter_jlp_historical_apy.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("apy", ColumnType.FLOAT, min_value=-100, max_value=500),
            ColumnSchema("tvl_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=50,
        max_age_hours=24,
        date_column="date"
    ),

    "jito_historical_apy.csv": FileSchema(
        filename="jito_historical_apy.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("apy", ColumnType.FLOAT, min_value=0, max_value=100),
        ],
        min_rows=50,
        max_age_hours=24,
        date_column="date"
    ),

    # ── WALLET TRACKERS ──────────────────────────────────────────────────────

    "estate_wallet_tracker.csv": FileSchema(
        filename="estate_wallet_tracker.csv",
        columns=[
            ColumnSchema("entity", ColumnType.STRING),
            ColumnSchema("wallet_address", ColumnType.STRING),
            ColumnSchema("chain", ColumnType.STRING),
            ColumnSchema("current_balance", ColumnType.FLOAT, min_value=0),
            ColumnSchema("balance_usd", ColumnType.FLOAT, min_value=0),
            ColumnSchema("last_movement", ColumnType.DATE, required=False),
            ColumnSchema("status", ColumnType.STRING),
        ],
        min_rows=5,
        max_age_hours=168,
    ),

    "whale_wallet_master_list.csv": FileSchema(
        filename="whale_wallet_master_list.csv",
        columns=[
            ColumnSchema("entity", ColumnType.STRING),
            ColumnSchema("wallet_address", ColumnType.STRING),
            ColumnSchema("chain", ColumnType.STRING),
            ColumnSchema("balance_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=10,
        max_age_hours=168,
    ),

    "market_maker_wallet_tracker.csv": FileSchema(
        filename="market_maker_wallet_tracker.csv",
        columns=[
            ColumnSchema("entity", ColumnType.STRING),
            ColumnSchema("wallet_address", ColumnType.STRING),
            ColumnSchema("chain", ColumnType.STRING),
            ColumnSchema("balance_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=5,
        max_age_hours=168,
    ),

    "protocol_treasury_tracker.csv": FileSchema(
        filename="protocol_treasury_tracker.csv",
        columns=[
            ColumnSchema("protocol", ColumnType.STRING),
            ColumnSchema("wallet_address", ColumnType.STRING),
            ColumnSchema("chain", ColumnType.STRING),
            ColumnSchema("balance_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=5,
        max_age_hours=168,
    ),

    # ── INSTITUTIONAL FLOWS ──────────────────────────────────────────────────

    "btc_etf_holdings.csv": FileSchema(
        filename="btc_etf_holdings.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("ticker", ColumnType.STRING),
            ColumnSchema("btc_holdings", ColumnType.FLOAT, min_value=0),
            ColumnSchema("aum_usd", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=10,
        max_age_hours=24,
        date_column="date"
    ),

    "corporate_btc_holdings.csv": FileSchema(
        filename="corporate_btc_holdings.csv",
        columns=[
            ColumnSchema("company", ColumnType.STRING),
            ColumnSchema("btc_holdings", ColumnType.FLOAT, min_value=0),
            ColumnSchema("avg_cost_basis", ColumnType.FLOAT, min_value=0),
        ],
        min_rows=5,
        max_age_hours=168,
    ),

    "institutional_13f.csv": FileSchema(
        filename="institutional_13f.csv",
        columns=[
            ColumnSchema("institution", ColumnType.STRING),
            ColumnSchema("filing_date", ColumnType.DATE),
            ColumnSchema("btc_exposure_usd", ColumnType.FLOAT),
        ],
        min_rows=5,
        max_age_hours=720,
    ),

    # ── SENTIMENT ────────────────────────────────────────────────────────────

    "sentiment_indicators.csv": FileSchema(
        filename="sentiment_indicators.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("fear_greed_index", ColumnType.INTEGER, min_value=0, max_value=100),
        ],
        min_rows=50,
        max_age_hours=24,
        date_column="date"
    ),

    "aaii_sentiment.csv": FileSchema(
        filename="aaii_sentiment.csv",
        columns=[
            ColumnSchema("date", ColumnType.DATE),
            ColumnSchema("bullish_pct", ColumnType.FLOAT, min_value=0, max_value=100),
            ColumnSchema("bearish_pct", ColumnType.FLOAT, min_value=0, max_value=100),
            ColumnSchema("neutral_pct", ColumnType.FLOAT, min_value=0, max_value=100),
        ],
        min_rows=50,
        max_age_hours=168,
        date_column="date"
    ),
}


def get_schema(filename: str) -> Optional[FileSchema]:
    """Get schema for a file."""
    return GATE1_SCHEMAS.get(filename)


def list_schemas() -> List[str]:
    """List all defined schema filenames."""
    return list(GATE1_SCHEMAS.keys())
