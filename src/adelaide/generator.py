"""
Adelaide Generator - Main orchestrator for newsletter generation.

Generates personalized newsletters by combining:
- Market data → Regime classification
- Templates → Content structure
- Personas → Voice adaptation
- Formatters → Multi-channel output
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date
from pathlib import Path
import logging

from src.registries import PersonaRegistry, OutputRegistry
from src.adelaide.regime_classifier import RegimeClassifier, MarketRegime
from src.adelaide.templates import TemplateEngine, select_insight
from src.adelaide.localization import LocalizationEngine

logger = logging.getLogger(__name__)


class AdelaideGenerator:
    """
    Orchestrates Adelaide newsletter generation.

    Generates personalized, multi-channel content from analytics data.

    Usage:
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=data,
            persona="ana",
            locale="en",
            output_formats=["newsletter_md", "twitter_thread"]
        )
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Adelaide generator.

        Args:
            config: Optional configuration dict with:
                - template_dir: Custom template directory
                - default_locale: Default locale (en)
                - recent_insights: List of recently used insight IDs
        """
        self.config = config or {}

        # Initialize components
        self.persona_registry = PersonaRegistry.get_instance()
        self.output_registry = OutputRegistry.get_instance()
        self.regime_classifier = RegimeClassifier()
        self.template_engine = TemplateEngine(
            template_dir=self.config.get('template_dir')
        )
        self.localization = LocalizationEngine(
            default_locale=self.config.get('default_locale', 'en')
        )

        # Track recent insights to avoid repetition
        self._recent_insights = self.config.get('recent_insights', [])

    def generate(
        self,
        analytics_data: Dict[str, Any],
        persona: str = "ana",
        locale: str = "en",
        output_formats: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Adelaide content.

        Args:
            analytics_data: Output from analytics layer containing:
                - btc_price, btc_24h_change: Bitcoin data
                - eth_price, eth_24h_change: Ethereum data
                - sol_price, sol_24h_change: Solana data
                - sp500_price, sp500_24h_change: S&P 500 data
                - vix: VIX level
                - fear_greed_index: Fear & Greed (0-100)
                - credit_spread: HY credit spread
                - strategy_performance: Dict of strategy metrics
                - alerts: List of active alerts
            persona: Persona name ("ana", "maria", or "felipe")
            locale: Locale code ("en" or "pt-br")
            output_formats: List of output formats (default: ["newsletter_md"])

        Returns:
            Dict with:
                - edition: Edition metadata
                - content: Generated content for each format
                - metadata: Generation metadata
        """
        output_formats = output_formats or ["newsletter_md"]
        logger.info(f"Generating Adelaide for persona={persona}, locale={locale}")

        # Step 1: Classify market regime
        regime = self.regime_classifier.classify(analytics_data)
        template_name = self.regime_classifier.get_template_name(regime)
        logger.info(f"Classified regime: {regime.value}, template: {template_name}")

        # Step 2: Prepare base content data
        content_data = self._prepare_content_data(analytics_data, regime, locale)

        # Step 3: Select insight
        insight = self._select_insight(regime, analytics_data)
        if insight:
            content_data['insight_id'] = insight['id']
            content_data['insight_title'] = insight['title']
            content_data['insight_content'] = insight['content']
            self._recent_insights.append(insight['id'])

        # Step 4: Apply persona adaptation FIRST (before rendering)
        # This fills in persona-specific placeholders
        persona_obj = self.persona_registry.get(persona, {})
        adapted_content = persona_obj.adapt(content_data, locale)

        # Step 5: Apply localization
        localized_content = self.localization.localize_content(adapted_content, locale)

        # Step 6: Render template with adapted + localized content
        rendered_template = self.template_engine.render(
            template_name,
            localized_content,
            persona=persona,
            locale=locale
        )
        localized_content['rendered_template'] = rendered_template

        # Step 7: Generate outputs for each format
        outputs = {}
        for format_name in output_formats:
            try:
                formatter = self.output_registry.get(format_name, {})
                outputs[format_name] = formatter.format({
                    'edition': {
                        'type': 'daily',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'persona': persona,
                        'locale': locale,
                        'regime': regime.value,
                    },
                    'content': localized_content,
                    'rendered_content': rendered_template,
                })
            except Exception as e:
                logger.error(f"Failed to format {format_name}: {e}")
                outputs[format_name] = f"Error generating {format_name}"

        # Build result
        result = {
            'edition': {
                'type': 'daily',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'persona': persona,
                'locale': locale,
                'regime': regime.value,
                'template': template_name,
            },
            'content': outputs,
            'metadata': {
                'word_count': self._count_words(outputs.get('newsletter_md', '')),
                'read_time_minutes': self._estimate_read_time(outputs.get('newsletter_md', '')),
                'template_used': template_name,
                'insights_included': [insight['id']] if insight else [],
                'generated_at': datetime.utcnow().isoformat(),
            }
        }

        logger.info(f"Generated Adelaide: {result['metadata']['word_count']} words")
        return result

    def generate_all_personas(
        self,
        analytics_data: Dict[str, Any],
        locale: str = "en",
        output_formats: List[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate Adelaide content for all personas.

        Args:
            analytics_data: Analytics data
            locale: Locale code
            output_formats: List of output formats

        Returns:
            Dict mapping persona name to generated content
        """
        personas = ['ana', 'maria', 'felipe']
        results = {}

        for persona in personas:
            results[persona] = self.generate(
                analytics_data=analytics_data,
                persona=persona,
                locale=locale,
                output_formats=output_formats
            )

        return results

    def _prepare_content_data(
        self,
        analytics_data: Dict[str, Any],
        regime: MarketRegime,
        locale: str
    ) -> Dict[str, Any]:
        """Prepare content data for template rendering."""
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
            'regime_description': self.regime_classifier.get_regime_description(regime),

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
            'fear_greed_label': self.localization.get_fear_greed_label(
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
                'fear_greed_label': self.localization.get_fear_greed_label(
                    analytics_data.get('fear_greed_index', 50), locale
                ),
            },

            # Whale/Estate alerts
            'has_whale_activity': bool(analytics_data.get('whale_alerts')),
            'whale_summary': analytics_data.get('whale_summary', ''),
            'has_estate_alerts': bool(analytics_data.get('estate_alerts')),
            'estate_summary': analytics_data.get('estate_summary', ''),

            # Strategy performance
            'strategy_summary': self._build_strategy_summary(analytics_data),
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
            'greeting_message': self._get_greeting_message(regime, locale),

            # Outlook
            'outlook_message': self._get_outlook_message(regime, locale),
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

    def _select_insight(
        self,
        regime: MarketRegime,
        analytics_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Select an appropriate insight based on regime and data."""
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
            recent_insights=self._recent_insights[-14:],  # Last 2 weeks
            market_conditions=analytics_data
        )

    def _build_strategy_summary(self, data: Dict[str, Any]) -> str:
        """Build strategy summary text."""
        btc_change = data.get('btc_24h_change', 0)

        if btc_change > 5:
            return "All strategies are performing well today. Growth strategies leading gains."
        elif btc_change > 0:
            return "Strategies are tracking markets. Yields continue to accumulate."
        elif btc_change > -5:
            return "Modest pullback across strategies. Conservative strategies holding steady."
        else:
            return "Significant market movement affecting all strategies. Conservative allocations showing resilience."

    def _get_greeting_message(self, regime: MarketRegime, locale: str) -> str:
        """Get greeting message based on regime."""
        messages = {
            MarketRegime.RISK_ON_BULL: "Markets are showing strength today. Let's look at what it means.",
            MarketRegime.RISK_OFF_BEAR: "Markets are down today, but that's part of the journey. Here's what's happening.",
            MarketRegime.TRANSITION: "Markets are mixed today. Here's your update.",
            MarketRegime.CRISIS: "Important market update. Please read carefully.",
        }
        return messages.get(regime, "Here's your daily market update.")

    def _get_outlook_message(self, regime: MarketRegime, locale: str) -> str:
        """Get outlook message based on regime."""
        messages = {
            MarketRegime.RISK_ON_BULL: "Momentum remains positive, but markets can change quickly.",
            MarketRegime.RISK_OFF_BEAR: "Volatility may continue short-term. Focus on your timeframe.",
            MarketRegime.TRANSITION: "Watch for direction as markets digest recent moves.",
            MarketRegime.CRISIS: "We'll continue monitoring and provide updates as situation evolves.",
        }
        return messages.get(regime, "Markets continue to evolve. Stay informed.")

    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())

    def _estimate_read_time(self, text: str, wpm: int = 200) -> int:
        """Estimate read time in minutes."""
        words = self._count_words(text)
        return max(1, round(words / wpm))


def generate_adelaide(
    analytics_data: Dict[str, Any],
    persona: str = "ana",
    locale: str = "en",
    output_formats: List[str] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Convenience function to generate Adelaide content.

    Args:
        analytics_data: Analytics data
        persona: Persona name
        locale: Locale code
        output_formats: List of output formats
        config: Optional generator config

    Returns:
        Generated Adelaide content
    """
    generator = AdelaideGenerator(config=config)
    return generator.generate(
        analytics_data=analytics_data,
        persona=persona,
        locale=locale,
        output_formats=output_formats
    )
