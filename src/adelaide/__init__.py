"""
Adelaide Newsletter Generation System.

Adelaide is the consumer-facing output - personalized newsletters
adapted for different investor personas across multiple channels.

Core Principles:
- NOT financial advice - educational market commentary
- Every message ends with "you decide" - empower autonomy
- Validate all choices, including exits
- Compliance-first (SEC/FINRA/MiCA)

Usage:
    from src.adelaide import AdelaideGenerator

    generator = AdelaideGenerator()
    result = generator.generate(
        analytics_data=data,
        persona="ana",
        locale="en",
        output_formats=["newsletter_md", "twitter_thread"]
    )
"""

from src.adelaide.generator import AdelaideGenerator
from src.adelaide.regime_classifier import RegimeClassifier, MarketRegime
from src.adelaide.templates import TemplateEngine
from src.adelaide.localization import LocalizationEngine

__all__ = [
    'AdelaideGenerator',
    'RegimeClassifier',
    'MarketRegime',
    'TemplateEngine',
    'LocalizationEngine',
]
