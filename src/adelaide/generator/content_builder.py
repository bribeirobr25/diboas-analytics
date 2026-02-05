"""
Content builder helpers for Adelaide generator.

Contains functions for preparing content data and building summaries.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from src.adelaide.regime_classifier import MarketRegime
from src.adelaide.templates import select_insight


def prepare_content_data(
    analytics_data: Dict[str, Any],
    regime: MarketRegime,
    locale: str,
    regime_classifier,
    localization
) -> Dict[str, Any]:
    """
    Prepare content data for template rendering.

    Args:
        analytics_data: Raw analytics data
        regime: Classified market regime
        locale: Locale code
        regime_classifier: RegimeClassifier instance
        localization: LocalizationEngine instance

    Returns:
        Dict with prepared content data
    """
    now = datetime.now()

    # Determine time of day
    hour = now.hour
    if 5 <= hour < 12:
        time_of_day = 'morning'
    elif 12 <= hour < 18:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'evening'

    # Build content data
    data = {
        'date': now,
        'time_of_day': time_of_day,
        'edition_type': 'Daily Edition',
        'regime': regime.value,
        'regime_description': regime_classifier.get_regime_description(regime),

        # Market data
        'btc_price': analytics_data.get('btc_price', 0),
        'btc_24h_change': analytics_data.get('btc_24h_change', 0),
        'eth_price': analytics_data.get('eth_price', 0),
        'eth_24h_change': analytics_data.get('eth_24h_change', 0),
        'sol_price': analytics_data.get('sol_price', 0),
        'sol_24h_change': analytics_data.get('sol_24h_change', 0),
        'sp500_price': analytics_data.get('sp500_price', 0),
        'sp500_24h_change': analytics_data.get('sp500_24h_change', 0),

        # Sentiment
        'fear_greed_index': analytics_data.get('fear_greed_index', 50),
        'fear_greed_label': localization.get_fear_greed_label(
            analytics_data.get('fear_greed_index', 50), locale
        ),
        'vix': analytics_data.get('vix', 20),
        'credit_spread': analytics_data.get('credit_spread', 350),

        # Market snapshot for formatters
        'market_snapshot': {
            'btc_price': analytics_data.get('btc_price', 0),
            'btc_24h_change': analytics_data.get('btc_24h_change', 0),
            'eth_price': analytics_data.get('eth_price', 0),
            'eth_24h_change': analytics_data.get('eth_24h_change', 0),
            'sol_price': analytics_data.get('sol_price', 0),
            'sol_24h_change': analytics_data.get('sol_24h_change', 0),
            'sp500_price': analytics_data.get('sp500_price', 0),
            'sp500_24h_change': analytics_data.get('sp500_24h_change', 0),
            'fear_greed_index': analytics_data.get('fear_greed_index', 50),
            'fear_greed_label': localization.get_fear_greed_label(
                analytics_data.get('fear_greed_index', 50), locale
            ),
        },

        # Whale/Estate alerts
        'has_whale_activity': bool(analytics_data.get('whale_alerts')),
        'whale_summary': analytics_data.get('whale_summary', ''),
        'has_estate_alerts': bool(analytics_data.get('estate_alerts')),
        'estate_summary': analytics_data.get('estate_summary', ''),

        # Strategy performance
        'strategy_summary': build_strategy_summary(analytics_data),
        'conservative_status': 'Normal',
        'conservative_7d': analytics_data.get('conservative_7d', 0),
        'conservative_30d': analytics_data.get('conservative_30d', 0),
        'conservative_today': analytics_data.get('conservative_today', 0),
        'balanced_status': 'Normal',
        'balanced_7d': analytics_data.get('balanced_7d', 0),
        'balanced_30d': analytics_data.get('balanced_30d', 0),
        'balanced_today': analytics_data.get('balanced_today', 0),
        'growth_status': 'Normal',
        'growth_7d': analytics_data.get('growth_7d', 0),
        'growth_30d': analytics_data.get('growth_30d', 0),
        'growth_today': analytics_data.get('growth_today', 0),

        # Greeting (will be adapted by persona)
        'greeting_message': get_greeting_message(regime, locale),

        # Outlook
        'outlook_message': get_outlook_message(regime, locale),
        'closing_wisdom': "Your strategy is working for you, not against you.",

        # Historical context for down days
        'historical_context': analytics_data.get('historical_context', ''),
        'down_days_count': analytics_data.get('down_days_count', 0),
        'avg_recovery_days': analytics_data.get('avg_recovery_days', 0),

        # Options for down day template
        'option_stay_description': "Keep your current strategy. No action needed.",
        'stay_outcome': "recovery within 30-90 days on average",
        'option_reduce_description': "Move to a more conservative allocation.",
        'option_withdraw_description': "Withdraw some or all funds.",
    }

    return data


def build_strategy_summary(data: Dict[str, Any]) -> str:
    """Build strategy summary text based on market data."""
    btc_change = data.get('btc_24h_change', 0)

    if btc_change > 5:
        return "All strategies are performing well today. Growth strategies leading gains."
    elif btc_change > 0:
        return "Strategies are tracking markets. Yields continue to accumulate."
    elif btc_change > -5:
        return "Modest pullback across strategies. Conservative strategies holding steady."
    else:
        return "Significant market movement affecting all strategies. Conservative allocations showing resilience."


def get_greeting_message(regime: MarketRegime, locale: str) -> str:
    """Get greeting message based on regime."""
    messages = {
        MarketRegime.RISK_ON_BULL: "Markets are showing strength today. Let's look at what it means.",
        MarketRegime.RISK_OFF_BEAR: "Markets are down today, but that's part of the journey. Here's what's happening.",
        MarketRegime.TRANSITION: "Markets are mixed today. Here's your update.",
        MarketRegime.CRISIS: "Important market update. Please read carefully.",
    }
    return messages.get(regime, "Here's your daily market update.")


def get_outlook_message(regime: MarketRegime, locale: str) -> str:
    """Get outlook message based on regime."""
    messages = {
        MarketRegime.RISK_ON_BULL: "Momentum remains positive, but markets can change quickly.",
        MarketRegime.RISK_OFF_BEAR: "Volatility may continue short-term. Focus on your timeframe.",
        MarketRegime.TRANSITION: "Watch for direction as markets digest recent moves.",
        MarketRegime.CRISIS: "We'll continue monitoring and provide updates as situation evolves.",
    }
    return messages.get(regime, "Markets continue to evolve. Stay informed.")


def select_regime_insight(
    regime: MarketRegime,
    analytics_data: Dict[str, Any],
    recent_insights: list
) -> Optional[Dict[str, Any]]:
    """
    Select an appropriate insight based on regime and data.

    Args:
        regime: Market regime
        analytics_data: Analytics data for context
        recent_insights: List of recently used insight IDs

    Returns:
        Selected insight dict or None
    """
    # Map regime to insight category
    category_map = {
        MarketRegime.RISK_ON_BULL: 'behavioral',  # Avoid FOMO
        MarketRegime.RISK_OFF_BEAR: 'behavioral',  # Stay calm
        MarketRegime.TRANSITION: 'market',
        MarketRegime.CRISIS: 'technical',
    }
    category = category_map.get(regime, 'strategy')

    return select_insight(
        category=category,
        recent_insights=recent_insights[-14:],  # Last 2 weeks
        market_conditions=analytics_data
    )


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def estimate_read_time(text: str, wpm: int = 200) -> int:
    """Estimate read time in minutes."""
    words = count_words(text)
    return max(1, round(words / wpm))
