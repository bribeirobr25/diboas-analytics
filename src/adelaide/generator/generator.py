"""
Adelaide Generator - Main orchestrator for newsletter generation.

Generates personalized newsletters by combining:
- Market data -> Regime classification
- Templates -> Content structure
- Personas -> Voice adaptation
- Formatters -> Multi-channel output
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

from src.registries import PersonaRegistry, OutputRegistry
from src.adelaide.regime_classifier import RegimeClassifier, MarketRegime
from src.adelaide.templates import TemplateEngine
from src.adelaide.localization import LocalizationEngine
from src.adelaide.generator.content_builder import (
    prepare_content_data,
    select_regime_insight,
    count_words,
    estimate_read_time,
)
from src.adelaide.generator.template_translations import get_template_translations

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
            analytics_data: Output from analytics layer
            persona: Persona name ("ana", "maria", "felipe", etc.)
            locale: Locale code ("en", "pt-br", "de", "es")
            output_formats: List of output formats (default: ["newsletter_md"])

        Returns:
            Dict with edition, content, and metadata
        """
        output_formats = output_formats or ["newsletter_md"]
        logger.info(f"Generating Adelaide for persona={persona}, locale={locale}")

        # Step 1: Classify market regime
        classification_result = self.regime_classifier.classify_with_result(
            analytics_data,
            target_date=analytics_data.get('target_date')
        )
        regime = classification_result.regime
        template_name = classification_result.template_name
        logger.info(f"Classified regime: {regime.value}, template: {template_name}")

        # Log TradFi gap if present
        if classification_result.has_tradfi_gap:
            gap_info = classification_result.tradfi_gap_disclosure
            logger.info(
                f"TradFi data gap: {gap_info.get('gap_type')}, "
                f"market closed: {gap_info.get('market_closed_reason')}"
            )

        # Step 2: Prepare base content data
        content_data = prepare_content_data(
            analytics_data, regime, locale,
            self.regime_classifier, self.localization
        )

        # Step 2b: Add TradFi gap disclosure if needed
        if classification_result.has_tradfi_gap:
            gap_info = classification_result.tradfi_gap_disclosure
            content_data['tradfi_gap_disclosure'] = self.localization.get_tradfi_gap_disclosure(
                gap_type=gap_info.get('gap_type', 'weekend'),
                locale=locale,
                data_date=gap_info.get('data_date')
            )
            content_data['has_tradfi_gap'] = True
        else:
            content_data['tradfi_gap_disclosure'] = ''
            content_data['has_tradfi_gap'] = False

        # Step 3: Select insight
        insight = select_regime_insight(regime, analytics_data, self._recent_insights)
        if insight:
            content_data['insight_id'] = insight['id']
            content_data['insight_title'] = insight['title']
            content_data['insight_content'] = insight['content']
            self._recent_insights.append(insight['id'])

        # Step 4: Apply persona adaptation
        persona_obj = self.persona_registry.get(persona, {})
        adapted_content = persona_obj.adapt(content_data, locale)

        # Step 5: Apply localization
        localized_content = self.localization.localize_content(adapted_content, locale)

        # Step 6: Add template translations
        localized_content.update(get_template_translations(self.localization, locale))

        # Step 7: Render template
        rendered_template = self.template_engine.render(
            template_name,
            localized_content,
            persona=persona,
            locale=locale
        )
        localized_content['rendered_template'] = rendered_template

        # Step 8: Generate outputs for each format
        outputs = self._generate_outputs(
            output_formats, localized_content, rendered_template,
            persona, locale, regime
        )

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
                'word_count': count_words(outputs.get('newsletter_md', '')),
                'read_time_minutes': estimate_read_time(outputs.get('newsletter_md', '')),
                'template_used': template_name,
                'insights_included': [insight['id']] if insight else [],
                'generated_at': datetime.utcnow().isoformat(),
            }
        }

        logger.info(f"Generated Adelaide: {result['metadata']['word_count']} words")
        return result

    def _generate_outputs(
        self,
        output_formats: List[str],
        localized_content: Dict[str, Any],
        rendered_template: str,
        persona: str,
        locale: str,
        regime: MarketRegime
    ) -> Dict[str, str]:
        """Generate outputs for each requested format."""
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

        return outputs

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
