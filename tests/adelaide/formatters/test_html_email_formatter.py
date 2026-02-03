"""Tests for Adelaide HTML Email Formatter."""

import pytest

from src.adelaide.formatters import AdelaideHtmlEmailFormatter, EmailSection
from src.registries.output_registry import OutputRegistry


class TestAdelaideHtmlEmailFormatter:
    """Tests for HTML email formatter."""

    @pytest.fixture
    def formatter(self):
        """Create formatter instance."""
        return AdelaideHtmlEmailFormatter(config={})

    @pytest.fixture
    def sample_data(self):
        """Sample Adelaide content data."""
        return {
            "edition": {
                "type": "daily",
                "date": "2024-01-15",
                "persona": "ana",
                "locale": "en",
            },
            "content": {
                "subject": "Adelaide Daily - January 15",
                "preheader": "Markets steady, BTC holding gains",
                "greeting": "Good morning",
                "greeting_message": "Good morning! Here's your market update.",
                "market_snapshot": {
                    "btc_price": 45000.50,
                    "btc_24h_change": 2.5,
                    "eth_price": 2500.25,
                    "eth_24h_change": -1.2,
                    "sol_price": 95.75,
                    "sol_24h_change": 5.8,
                    "fear_greed_index": 65,
                    "fear_greed_label": "Greed",
                },
                "insight_content": "Bitcoin continues to show strength above $44k.",
                "strategy_summary": "All strategies performing within expectations.",
            }
        }

    def test_should_be_registered_in_output_registry(self):
        """Formatter is registered as 'html_email'."""
        registry = OutputRegistry.get_instance()
        formatter = registry.get("html_email", {})
        assert formatter is not None
        assert isinstance(formatter, AdelaideHtmlEmailFormatter)

    def test_should_have_correct_output_type(self, formatter):
        """Output type is 'html_email'."""
        assert formatter.output_type == "html_email"

    def test_should_generate_valid_html(self, formatter, sample_data):
        """Generates valid HTML structure."""
        html = formatter.format(sample_data)

        assert html.startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "</html>" in html
        assert "<head>" in html
        assert "<body" in html

    def test_should_include_preheader(self, formatter, sample_data):
        """Includes preheader for email preview."""
        html = formatter.format(sample_data)

        assert "Markets steady, BTC holding gains" in html
        # Preheader should be hidden
        assert "display:none" in html

    def test_should_include_subject_in_title(self, formatter, sample_data):
        """Subject appears in title tag."""
        html = formatter.format(sample_data)

        assert "<title>Adelaide Daily - January 15</title>" in html

    def test_should_include_greeting(self, formatter, sample_data):
        """Includes greeting message."""
        html = formatter.format(sample_data)

        assert "Good morning! Here&#x27;s your market update." in html or "Good morning! Here's your market update." in html

    def test_should_format_market_snapshot(self, formatter, sample_data):
        """Formats market snapshot as table."""
        html = formatter.format(sample_data)

        assert "BTC" in html
        assert "$45,000.50" in html
        assert "+2.50%" in html
        assert "ETH" in html
        assert "SOL" in html

    def test_should_include_fear_greed_index(self, formatter, sample_data):
        """Includes Fear & Greed Index."""
        html = formatter.format(sample_data)

        assert "Fear &amp; Greed Index" in html or "Fear & Greed Index" in html
        assert "65" in html
        assert "Greed" in html

    def test_should_include_insight_section(self, formatter, sample_data):
        """Includes Adelaide insight section."""
        html = formatter.format(sample_data)

        assert "Adelaide&#x27;s Insight" in html or "Adelaide's Insight" in html
        assert "Bitcoin continues to show strength" in html

    def test_should_include_strategy_section(self, formatter, sample_data):
        """Includes strategy updates section."""
        html = formatter.format(sample_data)

        assert "Strategy Updates" in html
        assert "All strategies performing within expectations" in html

    def test_should_include_disclaimer(self, formatter, sample_data):
        """Includes legal disclaimer."""
        html = formatter.format(sample_data)

        assert "not financial advice" in html
        assert "Past performance" in html

    def test_should_include_unsubscribe_link(self, formatter, sample_data):
        """Includes unsubscribe link placeholder."""
        html = formatter.format(sample_data)

        assert "{{unsubscribe_url}}" in html
        assert "Unsubscribe" in html

    def test_should_use_ana_signature_by_default(self, formatter, sample_data):
        """Uses Ana signature for Ana persona."""
        html = formatter.format(sample_data)

        assert "Ana" in html
        # Palm tree emoji (may be encoded)
        assert "127796" in html or "🌴" in html

    def test_should_use_maria_signature(self, formatter):
        """Uses Maria signature for Maria persona."""
        data = {
            "edition": {"persona": "maria"},
            "content": {}
        }
        html = formatter.format(data)

        assert "Maria" in html

    def test_should_use_felipe_signature(self, formatter):
        """Uses Felipe signature for Felipe persona."""
        data = {
            "edition": {"persona": "felipe"},
            "content": {}
        }
        html = formatter.format(data)

        assert "Felipe" in html

    def test_should_use_portuguese_disclaimer(self, formatter):
        """Uses Portuguese disclaimer for pt-BR locale."""
        data = {
            "edition": {"locale": "pt-BR"},
            "content": {}
        }
        html = formatter.format(data)

        assert "aconselhamento financeiro" in html or "financeiro" in html

    def test_should_include_mso_conditionals(self, formatter, sample_data):
        """Includes MSO conditionals for Outlook."""
        html = formatter.format(sample_data)

        assert "<!--[if mso]>" in html
        assert "<![endif]-->" in html

    def test_should_include_responsive_styles(self, formatter, sample_data):
        """Includes responsive media queries."""
        html = formatter.format(sample_data)

        assert "@media" in html
        assert "max-width: 600px" in html

    def test_should_include_dark_mode_support(self, formatter, sample_data):
        """Includes dark mode color scheme."""
        html = formatter.format(sample_data)

        assert "prefers-color-scheme: dark" in html
        assert "color-scheme" in html

    def test_should_use_inline_css(self, formatter, sample_data):
        """Uses inline CSS for email compatibility."""
        html = formatter.format(sample_data)

        # Should have inline styles, not class-only styling
        assert 'style="' in html
        assert "background-color:" in html
        assert "font-family:" in html

    def test_should_handle_empty_content(self, formatter):
        """Handles empty content gracefully."""
        data = {"content": {}}
        html = formatter.format(data)

        assert "<!DOCTYPE html>" in html
        assert "</html>" in html


class TestEmailSection:
    """Tests for EmailSection dataclass."""

    def test_should_create_section_with_defaults(self):
        """Creates section with default icon."""
        section = EmailSection(title="Test", content="Content")

        assert section.title == "Test"
        assert section.content == "Content"
        assert section.icon == "📊"

    def test_should_create_section_with_custom_icon(self):
        """Creates section with custom icon."""
        section = EmailSection(title="Alerts", content="Warning", icon="⚠️")

        assert section.icon == "⚠️"
