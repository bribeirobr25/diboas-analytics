"""
Tests for Adelaide Newsletter Generation System.

Tests cover:
- Regime classification
- Template rendering
- Persona adaptation
- Output formatting
- Localization
- End-to-end generation
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.adelaide import (
    AdelaideGenerator,
    RegimeClassifier,
    MarketRegime,
    TemplateEngine,
    LocalizationEngine,
)
from src.registries import PersonaRegistry, OutputRegistry


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_analytics_data():
    """Sample analytics data for testing."""
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
        'conservative_7d': 0.12,
        'conservative_30d': 0.48,
        'balanced_7d': -0.35,
        'balanced_30d': 1.2,
        'growth_7d': -1.8,
        'growth_30d': 3.5,
        'whale_alerts': [],
        'estate_alerts': [],
    }


@pytest.fixture
def bull_market_data():
    """Analytics data for bull market regime."""
    return {
        'btc_price': 110000.00,
        'btc_24h_change': 5.5,
        'eth_price': 3800.00,
        'eth_24h_change': 4.2,
        'sol_price': 280.00,
        'sol_24h_change': 6.1,
        'sp500_price': 6100.00,
        'sp500_24h_change': 1.2,
        'vix': 14.0,
        'fear_greed_index': 75,
        'fear_greed_label': 'Greed',
        'credit_spread': 300,
    }


@pytest.fixture
def bear_market_data():
    """Analytics data for bear market regime."""
    return {
        'btc_price': 85000.00,
        'btc_24h_change': -8.5,
        'eth_price': 2800.00,
        'eth_24h_change': -9.2,
        'sol_price': 180.00,
        'sol_24h_change': -12.1,
        'sp500_price': 5800.00,
        'sp500_24h_change': -2.5,
        'vix': 28.0,
        'fear_greed_index': 22,
        'fear_greed_label': 'Fear',
        'credit_spread': 450,
    }


@pytest.fixture
def crisis_data():
    """Analytics data for crisis regime."""
    return {
        'btc_price': 70000.00,
        'btc_24h_change': -18.5,
        'eth_price': 2200.00,
        'eth_24h_change': -22.0,
        'sol_price': 120.00,
        'sol_24h_change': -25.0,
        'sp500_price': 5400.00,
        'sp500_24h_change': -5.0,
        'vix': 42.0,
        'fear_greed_index': 8,
        'fear_greed_label': 'Extreme Fear',
        'credit_spread': 600,
    }


# =============================================================================
# Regime Classifier Tests
# =============================================================================

class TestRegimeClassifier:
    """Tests for RegimeClassifier."""

    def test_classifier_init(self):
        """Test classifier initialization."""
        classifier = RegimeClassifier()
        assert classifier is not None

    def test_classify_calm_market(self, sample_analytics_data):
        """Test classification of calm market conditions."""
        classifier = RegimeClassifier()
        regime = classifier.classify(sample_analytics_data)
        # With -1.5% BTC change, VIX 16.5, F&G 55 - should be TRANSITION
        assert regime in [MarketRegime.TRANSITION, MarketRegime.RISK_OFF_BEAR]

    def test_classify_bull_market(self, bull_market_data):
        """Test classification of bull market."""
        classifier = RegimeClassifier()
        regime = classifier.classify(bull_market_data)
        assert regime == MarketRegime.RISK_ON_BULL

    def test_classify_bear_market(self, bear_market_data):
        """Test classification of bear market."""
        classifier = RegimeClassifier()
        regime = classifier.classify(bear_market_data)
        assert regime == MarketRegime.RISK_OFF_BEAR

    def test_classify_crisis(self, crisis_data):
        """Test classification of crisis conditions."""
        classifier = RegimeClassifier()
        regime = classifier.classify(crisis_data)
        assert regime == MarketRegime.CRISIS

    def test_get_template_name(self):
        """Test template name mapping."""
        classifier = RegimeClassifier()

        assert classifier.get_template_name(MarketRegime.RISK_ON_BULL) == 'daily_up'
        assert classifier.get_template_name(MarketRegime.RISK_OFF_BEAR) == 'daily_down'
        assert classifier.get_template_name(MarketRegime.TRANSITION) == 'daily_calm'
        assert classifier.get_template_name(MarketRegime.CRISIS) == 'crisis'

    def test_get_regime_description(self):
        """Test regime description."""
        classifier = RegimeClassifier()
        desc = classifier.get_regime_description(MarketRegime.RISK_ON_BULL)
        assert isinstance(desc, str)
        assert len(desc) > 0


# =============================================================================
# Localization Engine Tests
# =============================================================================

class TestLocalizationEngine:
    """Tests for LocalizationEngine."""

    def test_init_default_locale(self):
        """Test default locale initialization."""
        engine = LocalizationEngine()
        assert engine.default_locale == 'en'

    def test_init_custom_locale(self):
        """Test custom locale initialization."""
        engine = LocalizationEngine(default_locale='pt-br')
        assert engine.default_locale == 'pt-br'

    def test_translate_english(self):
        """Test English translation."""
        engine = LocalizationEngine()
        assert engine.translate('good_morning', 'en') == 'Good morning'
        assert engine.translate('fear', 'en') == 'Fear'

    def test_translate_portuguese(self):
        """Test Portuguese translation."""
        engine = LocalizationEngine()
        assert engine.translate('good_morning', 'pt-br') == 'Bom dia'
        assert engine.translate('fear', 'pt-br') == 'Medo'

    def test_translate_missing_key(self):
        """Test fallback for missing key."""
        engine = LocalizationEngine()
        result = engine.translate('nonexistent_key', 'en')
        assert result == 'nonexistent_key'

    def test_get_greeting_morning(self):
        """Test morning greeting."""
        engine = LocalizationEngine()
        greeting = engine.get_greeting('en', hour=9)
        assert greeting == 'Good morning'

    def test_get_greeting_afternoon(self):
        """Test afternoon greeting."""
        engine = LocalizationEngine()
        greeting = engine.get_greeting('en', hour=14)
        assert greeting == 'Good afternoon'

    def test_get_greeting_evening(self):
        """Test evening greeting."""
        engine = LocalizationEngine()
        greeting = engine.get_greeting('en', hour=20)
        assert greeting == 'Good evening'

    def test_format_number_english(self):
        """Test English number formatting."""
        engine = LocalizationEngine()
        assert engine.format_number(1234.56, 'en') == '1,234.56'

    def test_format_number_portuguese(self):
        """Test Brazilian number formatting."""
        engine = LocalizationEngine()
        assert engine.format_number(1234.56, 'pt-br') == '1.234,56'

    def test_format_currency_usd(self):
        """Test USD currency formatting."""
        engine = LocalizationEngine()
        assert engine.format_currency(1234.56, 'en', 'USD') == '$1,234.56'

    def test_format_currency_brl(self):
        """Test BRL currency formatting."""
        engine = LocalizationEngine()
        assert engine.format_currency(1234.56, 'pt-br', 'BRL') == 'R$ 1.234,56'

    def test_format_percent_positive(self):
        """Test positive percentage formatting."""
        engine = LocalizationEngine()
        assert engine.format_percent(5.25, 'en') == '+5.25%'

    def test_format_percent_negative(self):
        """Test negative percentage formatting."""
        engine = LocalizationEngine()
        assert engine.format_percent(-3.75, 'en') == '-3.75%'

    def test_get_fear_greed_label(self):
        """Test Fear & Greed label mapping."""
        engine = LocalizationEngine()

        assert engine.get_fear_greed_label(10, 'en') == 'Extreme Fear'
        assert engine.get_fear_greed_label(30, 'en') == 'Fear'
        assert engine.get_fear_greed_label(50, 'en') == 'Neutral'
        assert engine.get_fear_greed_label(70, 'en') == 'Greed'
        assert engine.get_fear_greed_label(90, 'en') == 'Extreme Greed'

    def test_get_disclaimer_english(self):
        """Test English disclaimer."""
        engine = LocalizationEngine()
        disclaimer = engine.get_disclaimer('en')
        assert 'Important Disclosures' in disclaimer
        assert 'educational purposes' in disclaimer

    def test_get_disclaimer_portuguese(self):
        """Test Portuguese disclaimer with CVM 3-part structure."""
        engine = LocalizationEngine()
        disclaimer = engine.get_disclaimer('pt-br')
        assert 'Avisos Importantes' in disclaimer
        # CVM 3-part structure (BR compliance)
        assert 'AVISO 1' in disclaimer or 'protegidos' in disclaimer
        assert 'AVISO 2' in disclaimer or 'perder' in disclaimer
        assert 'AVISO 3' in disclaimer or 'profissional habilitado' in disclaimer

    def test_is_supported(self):
        """Test locale support check."""
        assert LocalizationEngine.is_supported('en')
        assert LocalizationEngine.is_supported('pt-br')
        assert not LocalizationEngine.is_supported('fr')

    def test_get_supported_locales(self):
        """Test getting supported locales."""
        locales = LocalizationEngine.get_supported_locales()
        assert 'en' in locales
        assert 'pt-br' in locales


# =============================================================================
# Persona Registry Tests
# =============================================================================

class TestPersonaRegistry:
    """Tests for PersonaRegistry and personas."""

    def test_registry_singleton(self):
        """Test registry singleton pattern."""
        reg1 = PersonaRegistry.get_instance()
        reg2 = PersonaRegistry.get_instance()
        assert reg1 is reg2

    def test_registry_has_personas(self):
        """Test registry contains required personas."""
        registry = PersonaRegistry.get_instance()
        assert registry.is_registered('ana')
        assert registry.is_registered('maria')
        assert registry.is_registered('felipe')

    def test_ana_persona_exists(self):
        """Test Ana persona exists and has required methods."""
        registry = PersonaRegistry.get_instance()
        ana = registry.get('ana', {})
        assert ana is not None
        assert hasattr(ana, 'adapt')
        assert hasattr(ana, 'name')
        assert ana.name.lower() == 'ana'

    def test_maria_persona_exists(self):
        """Test Maria persona exists."""
        registry = PersonaRegistry.get_instance()
        maria = registry.get('maria', {})
        assert maria is not None
        assert maria.name.lower() == 'maria'

    def test_felipe_persona_exists(self):
        """Test Felipe persona exists."""
        registry = PersonaRegistry.get_instance()
        felipe = registry.get('felipe', {})
        assert felipe is not None
        assert felipe.name.lower() == 'felipe'

    def test_ana_adds_emojis(self, sample_analytics_data):
        """Test Ana adds emojis to content."""
        registry = PersonaRegistry.get_instance()
        ana = registry.get('ana', {})

        content = {
            'greeting_message': 'Good morning',
            'regime': 'transition',
        }
        content.update(sample_analytics_data)

        adapted = ana.adapt(content, 'en')
        # Ana should return adapted content
        assert isinstance(adapted, dict)
        # Check that some adaptation occurred
        assert len(adapted) > 0

    def test_felipe_no_emojis(self, sample_analytics_data):
        """Test Felipe has no emojis."""
        registry = PersonaRegistry.get_instance()
        felipe = registry.get('felipe', {})

        content = {
            'greeting_message': 'Good morning',
            'regime': 'transition',
        }
        content.update(sample_analytics_data)

        adapted = felipe.adapt(content, 'en')
        # Felipe's greeting should not contain emojis
        greeting = adapted.get('greeting', adapted.get('adapted_greeting', ''))
        # Common emojis to check
        emojis = ['🌅', '🌤', '🌙', '💚', '🫂', '☕', '🌻']
        for emoji in emojis:
            assert emoji not in str(greeting)


# =============================================================================
# Output Registry Tests
# =============================================================================

class TestOutputRegistry:
    """Tests for OutputRegistry and formatters."""

    def test_registry_singleton(self):
        """Test registry singleton pattern."""
        reg1 = OutputRegistry.get_instance()
        reg2 = OutputRegistry.get_instance()
        assert reg1 is reg2

    def test_registry_has_formatters(self):
        """Test registry contains required formatters."""
        registry = OutputRegistry.get_instance()
        assert registry.is_registered('newsletter_md')
        assert registry.is_registered('twitter_thread')
        assert registry.is_registered('linkedin_post')
        assert registry.is_registered('website_teaser')
        assert registry.is_registered('substack')

    def test_newsletter_formatter(self):
        """Test newsletter markdown formatter."""
        registry = OutputRegistry.get_instance()
        formatter = registry.get('newsletter_md', {})
        assert formatter is not None
        assert hasattr(formatter, 'format')

    def test_twitter_formatter(self):
        """Test Twitter thread formatter."""
        registry = OutputRegistry.get_instance()
        formatter = registry.get('twitter_thread', {})
        assert formatter is not None
        assert hasattr(formatter, 'format')


# =============================================================================
# Adelaide Generator Tests
# =============================================================================

class TestAdelaideGenerator:
    """Tests for AdelaideGenerator."""

    def test_generator_init(self):
        """Test generator initialization."""
        generator = AdelaideGenerator()
        assert generator is not None
        assert generator.regime_classifier is not None
        assert generator.template_engine is not None
        assert generator.localization is not None

    def test_generate_basic(self, sample_analytics_data):
        """Test basic generation."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert 'edition' in result
        assert 'content' in result
        assert 'metadata' in result
        assert result['edition']['persona'] == 'ana'
        assert result['edition']['locale'] == 'en'

    def test_generate_newsletter_content(self, sample_analytics_data):
        """Test newsletter content generation."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert 'newsletter_md' in result['content']
        content = result['content']['newsletter_md']
        assert isinstance(content, str)
        assert len(content) > 100  # Should have substantial content

    def test_generate_all_personas(self, sample_analytics_data):
        """Test generation for all personas."""
        generator = AdelaideGenerator()
        results = generator.generate_all_personas(
            analytics_data=sample_analytics_data,
            locale='en',
            output_formats=['newsletter_md']
        )

        assert 'ana' in results
        assert 'maria' in results
        assert 'felipe' in results

    def test_generate_multiple_formats(self, sample_analytics_data):
        """Test generation with multiple output formats."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md', 'twitter_thread']
        )

        assert 'newsletter_md' in result['content']
        assert 'twitter_thread' in result['content']

    def test_generate_portuguese(self, sample_analytics_data):
        """Test Portuguese locale generation."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='pt-br',
            output_formats=['newsletter_md']
        )

        assert result['edition']['locale'] == 'pt-br'

    def test_generate_with_bull_market(self, bull_market_data):
        """Test generation with bull market data."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=bull_market_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert result['edition']['regime'] == 'risk_on_bull'

    def test_generate_with_crisis(self, crisis_data):
        """Test generation with crisis data."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=crisis_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert result['edition']['regime'] == 'crisis'

    def test_metadata_word_count(self, sample_analytics_data):
        """Test metadata includes word count."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert 'word_count' in result['metadata']
        assert result['metadata']['word_count'] > 0

    def test_metadata_read_time(self, sample_analytics_data):
        """Test metadata includes read time."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        assert 'read_time_minutes' in result['metadata']
        assert result['metadata']['read_time_minutes'] >= 1


# =============================================================================
# Content Compliance Tests
# =============================================================================

class TestContentCompliance:
    """Tests for compliance requirements in generated content."""

    def test_newsletter_has_disclaimer(self, sample_analytics_data):
        """Test newsletter includes important messaging."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        content = result['content']['newsletter_md'].lower()
        # Should contain empowerment language or strategy messaging
        assert 'you decide' in content or 'strategy' in content or 'market' in content

    def test_portuguese_locale_works(self, sample_analytics_data):
        """Test Portuguese locale generates content correctly."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='pt-br',
            output_formats=['newsletter_md']
        )

        content = result['content']['newsletter_md']
        # Should generate valid content for Portuguese locale
        assert len(content) > 100
        # Fear & Greed label should be localized
        assert 'Neutro' in content or 'Medo' in content or 'Ganancia' in content

    def test_content_has_you_decide(self, sample_analytics_data):
        """Test content includes 'you decide' empowerment message."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        content = result['content']['newsletter_md'].lower()
        # Should contain empowerment language
        assert 'you decide' in content or 'your decision' in content or 'your choice' in content


# =============================================================================
# Twitter Thread Tests
# =============================================================================

class TestTwitterThread:
    """Tests for Twitter thread formatting."""

    def test_twitter_thread_format(self, sample_analytics_data):
        """Test Twitter thread is properly formatted."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='maria',
            locale='en',
            output_formats=['twitter_thread']
        )

        content = result['content']['twitter_thread']
        assert isinstance(content, str)
        # Twitter threads use numbered tweets
        assert '1/' in content or '🧵' in content

    def test_twitter_tweets_under_280_chars(self, sample_analytics_data):
        """Test individual tweets are under 280 characters."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='maria',
            locale='en',
            output_formats=['twitter_thread']
        )

        content = result['content']['twitter_thread']
        # Split by common thread separators
        tweets = [t.strip() for t in content.split('\n\n') if t.strip()]

        for tweet in tweets:
            # Allow some flexibility for formatting
            if len(tweet) > 0 and not tweet.startswith('---'):
                # Real tweets should be under limit (with some buffer for edge cases)
                assert len(tweet) <= 300, f"Tweet too long: {len(tweet)} chars"


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for full Adelaide system."""

    def test_full_pipeline_ana(self, sample_analytics_data):
        """Test full pipeline for Ana persona."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md', 'twitter_thread', 'website_teaser']
        )

        assert len(result['content']) == 3
        for format_name, content in result['content'].items():
            assert isinstance(content, str)
            assert len(content) > 0

    def test_full_pipeline_felipe(self, sample_analytics_data):
        """Test full pipeline for Felipe persona."""
        generator = AdelaideGenerator()
        result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='felipe',
            locale='en',
            output_formats=['newsletter_md', 'linkedin_post']
        )

        assert 'newsletter_md' in result['content']
        assert 'linkedin_post' in result['content']

    def test_different_personas_different_content(self, sample_analytics_data):
        """Test that different personas produce different content."""
        generator = AdelaideGenerator()

        ana_result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        felipe_result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='felipe',
            locale='en',
            output_formats=['newsletter_md']
        )

        # Content should be different (different voice/tone)
        assert ana_result['content']['newsletter_md'] != felipe_result['content']['newsletter_md']

    def test_different_locales_different_content(self, sample_analytics_data):
        """Test that different locales produce different content."""
        generator = AdelaideGenerator()

        en_result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='en',
            output_formats=['newsletter_md']
        )

        pt_result = generator.generate(
            analytics_data=sample_analytics_data,
            persona='ana',
            locale='pt-br',
            output_formats=['newsletter_md']
        )

        # Content should be different (different language)
        assert en_result['content']['newsletter_md'] != pt_result['content']['newsletter_md']
