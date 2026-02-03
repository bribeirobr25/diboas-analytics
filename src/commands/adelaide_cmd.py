"""
Adelaide command - Generate personalized newsletters.

Usage:
    python main.py adelaide --persona ana --locale en --format newsletter_md
    python main.py adelaide --persona all --format newsletter_md
    python main.py adelaide --persona ana --format newsletter_md,twitter_thread
"""

import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def run_adelaide(args):
    """
    Generate Adelaide newsletter content.

    Args:
        args: Parsed command line arguments with:
            - persona: "ana", "maria", "felipe", or "all"
            - locale: "en" or "pt-br"
            - format: Comma-separated list of formats
            - output: Output directory
            - data: Optional path to analytics data JSON
    """
    from src.adelaide import AdelaideGenerator
    from config.settings import OUTPUT_DIR

    print("Adelaide Newsletter Generator")
    print("=" * 50)
    print()

    # Parse arguments
    persona = getattr(args, 'persona', 'ana')
    locale = getattr(args, 'locale', 'en')
    formats_str = getattr(args, 'format', 'newsletter_md')
    output_formats = [f.strip() for f in formats_str.split(',')]
    output_dir = Path(getattr(args, 'output', OUTPUT_DIR))

    print(f"Persona: {persona}")
    print(f"Locale: {locale}")
    print(f"Formats: {', '.join(output_formats)}")
    print(f"Output: {output_dir}")
    print()

    # Get or generate analytics data
    analytics_data = _get_analytics_data(args)

    if not analytics_data:
        print("No analytics data available. Using sample data.")
        analytics_data = _get_sample_data()

    print("Generating Adelaide content...")
    print()

    # Initialize generator
    generator = AdelaideGenerator()

    # Generate for specified persona(s)
    if persona == 'all':
        personas = ['ana', 'maria', 'felipe']
    else:
        personas = [persona]

    results = {}
    for p in personas:
        print(f"Generating for {p.title()}...")
        result = generator.generate(
            analytics_data=analytics_data,
            persona=p,
            locale=locale,
            output_formats=output_formats
        )
        results[p] = result

        # Save outputs
        for fmt, content in result['content'].items():
            filename = f"adelaide_{p}_{locale}_{fmt.replace('_', '')}.md"
            if fmt == 'twitter_thread':
                filename = f"adelaide_{p}_{locale}_twitter.txt"
            elif fmt == 'linkedin_post':
                filename = f"adelaide_{p}_{locale}_linkedin.md"

            filepath = output_dir / filename
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  Saved: {filepath}")

    print()
    print("-" * 50)
    print("Generation Complete")
    print()

    # Print summary
    for p, result in results.items():
        meta = result['metadata']
        print(f"{p.title()} Edition:")
        print(f"  Regime: {result['edition']['regime']}")
        print(f"  Word count: {meta['word_count']}")
        print(f"  Read time: {meta['read_time_minutes']} min")
        print()

    # Print sample content for first persona
    first_persona = personas[0]
    if 'newsletter_md' in results[first_persona]['content']:
        print("=" * 50)
        print(f"PREVIEW ({first_persona.title()} - first 1000 chars):")
        print("=" * 50)
        preview = results[first_persona]['content']['newsletter_md'][:1000]
        print(preview)
        print("...")
        print()


def _get_analytics_data(args) -> dict:
    """Get analytics data from file or collectors."""
    import json

    # Check if data file provided
    data_path = getattr(args, 'data', None)
    if data_path and Path(data_path).exists():
        with open(data_path) as f:
            return json.load(f)

    # Try to collect live data
    try:
        return _collect_live_data()
    except Exception as e:
        logger.warning(f"Could not collect live data: {e}")
        return None


def _collect_live_data() -> dict:
    """Collect live data from APIs."""
    from src.registries import CollectorRegistry, ensure_collectors_registered

    ensure_collectors_registered()
    registry = CollectorRegistry.get_instance()

    data = {}

    # Try to get Fear & Greed
    try:
        alt_collector = registry.get('alternative', {})
        current = alt_collector.get_current()
        data['fear_greed_index'] = current.get('value', 50)
        data['fear_greed_label'] = current.get('classification', 'Neutral')
    except Exception as e:
        logger.warning(f"Could not get Fear & Greed: {e}")
        data['fear_greed_index'] = 50
        data['fear_greed_label'] = 'Neutral'

    # Try to get crypto prices
    try:
        import yfinance as yf

        btc = yf.Ticker("BTC-USD")
        btc_hist = btc.history(period="2d")
        if len(btc_hist) >= 2:
            data['btc_price'] = btc_hist['Close'].iloc[-1]
            data['btc_24h_change'] = ((btc_hist['Close'].iloc[-1] / btc_hist['Close'].iloc[-2]) - 1) * 100

        eth = yf.Ticker("ETH-USD")
        eth_hist = eth.history(period="2d")
        if len(eth_hist) >= 2:
            data['eth_price'] = eth_hist['Close'].iloc[-1]
            data['eth_24h_change'] = ((eth_hist['Close'].iloc[-1] / eth_hist['Close'].iloc[-2]) - 1) * 100

        sol = yf.Ticker("SOL-USD")
        sol_hist = sol.history(period="2d")
        if len(sol_hist) >= 2:
            data['sol_price'] = sol_hist['Close'].iloc[-1]
            data['sol_24h_change'] = ((sol_hist['Close'].iloc[-1] / sol_hist['Close'].iloc[-2]) - 1) * 100

        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="2d")
        if len(spy_hist) >= 2:
            data['sp500_price'] = spy_hist['Close'].iloc[-1]
            data['sp500_24h_change'] = ((spy_hist['Close'].iloc[-1] / spy_hist['Close'].iloc[-2]) - 1) * 100

        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="1d")
        if len(vix_hist) >= 1:
            data['vix'] = vix_hist['Close'].iloc[-1]

    except Exception as e:
        logger.warning(f"Could not get prices: {e}")

    return data if data else None


def _get_sample_data() -> dict:
    """Get sample analytics data for testing."""
    return {
        'btc_price': 104500.00,
        'btc_24h_change': -1.5,
        'eth_price': 3300.00,
        'eth_24h_change': -2.1,
        'sol_price': 250.00,
        'sol_24h_change': -3.2,
        'sp500_price': 6050.00,
        'sp500_24h_change': 0.3,
        'vix': 16.5,
        'fear_greed_index': 55,
        'fear_greed_label': 'Neutral',
        'credit_spread': 340,

        # Strategy performance
        'conservative_7d': 0.12,
        'conservative_30d': 0.48,
        'balanced_7d': -0.35,
        'balanced_30d': 1.2,
        'growth_7d': -1.8,
        'growth_30d': 3.5,

        # Alerts
        'whale_alerts': [],
        'estate_alerts': [],
    }
