"""
Social media formatters for Adelaide.

Contains:
- WhatsAppFormatter: WhatsApp-compatible messages (4096 chars max)
- TelegramFormatter: Telegram-compatible messages (4096 chars max)
- TwitterFormatter: Single tweet format (280 chars max)
- SubstackFormatter: Full article for Substack newsletter
"""

from typing import Any, Dict, Optional
import re
import logging

from src.registries.formatters.base import OutputFormatter, OutputRegistry

logger = logging.getLogger(__name__)


@OutputRegistry.register("whatsapp")
class WhatsAppFormatter(OutputFormatter):
    """
    Adelaide content formatted for WhatsApp.

    Platform Constraints:
    - Max length: 4,096 characters
    - Formatting: *bold*, _italic_ only
    - No markdown links, headers, tables
    - Convert tables to readable lists
    """

    MAX_LENGTH = 4096

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content for WhatsApp.

        Args:
            data: Adelaide content dict

        Returns:
            WhatsApp-compatible message (<=4,096 chars)
        """
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}
        locale = edition.get('locale', 'en')

        lines = []

        # Greeting (with WhatsApp-style bold)
        greeting = content.get('persona_greeting', '')
        if greeting:
            lines.append(f"*{self._strip_emojis_except_standard(greeting)}*")
            lines.append("")

        # Intro message
        intro = content.get('greeting_message', '')
        if intro:
            # Convert markdown bold to WhatsApp bold
            intro = self._convert_markdown_to_whatsapp(intro)
            lines.append(intro)
            lines.append("")

        # Market section header
        market_title = content.get('market_section_title', 'Market Update')
        lines.append(f"*{market_title}*")
        lines.append("")

        # Market data as list (no tables in WhatsApp)
        btc_price = content.get('btc_price', content.get('market_snapshot', {}).get('btc_price', 0))
        btc_change = content.get('btc_24h_change', content.get('market_snapshot', {}).get('btc_24h_change', 0))
        eth_price = content.get('eth_price', content.get('market_snapshot', {}).get('eth_price', 0))
        eth_change = content.get('eth_24h_change', content.get('market_snapshot', {}).get('eth_24h_change', 0))

        if btc_price:
            lines.append(f"* BTC: ${btc_price:,.0f} ({btc_change:+.1f}%)")
        if eth_price:
            lines.append(f"* ETH: ${eth_price:,.0f} ({eth_change:+.1f}%)")

        fg = content.get('fear_greed_index', 50)
        fg_label = content.get('fear_greed_label', 'Neutral')
        lines.append(f"* Fear & Greed: {fg} ({fg_label})")
        lines.append("")

        # Key insight (shortened)
        if content.get('insight_content'):
            insight = content['insight_content']
            # Take first 200 chars
            if len(insight) > 200:
                insight = insight[:197] + "..."
            insight = self._convert_markdown_to_whatsapp(insight)
            lines.append(f"[light bulb emoji] {insight}")
            lines.append("")

        # Closing
        closing = content.get('closing_wisdom', '')
        if closing:
            lines.append(f"_{closing}_")
            lines.append("")

        # Signature
        signature = content.get('signature', '- Adelaide | diBoaS')
        # Simplify signature for WhatsApp
        signature = signature.replace('\n', ' | ').replace('**', '*')
        lines.append(signature)

        # AI disclosure
        ai_disclosure = content.get('ai_disclosure', '[robot emoji] AI-generated content')
        lines.append("")
        lines.append(ai_disclosure)

        result = "\n".join(lines)

        # Ensure we don't exceed max length
        if len(result) > self.MAX_LENGTH:
            result = result[:self.MAX_LENGTH - 3] + "..."

        return result

    def _convert_markdown_to_whatsapp(self, text: str) -> str:
        """Convert markdown formatting to WhatsApp format."""
        # Convert **bold** to *bold*
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        # Keep _italic_ as is
        # Remove markdown links [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove headers
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        return text

    def _strip_emojis_except_standard(self, text: str) -> str:
        """Keep standard emojis but clean formatting."""
        return text.strip()

    @property
    def output_type(self) -> str:
        return "whatsapp"


@OutputRegistry.register("telegram")
class TelegramFormatter(OutputFormatter):
    """
    Adelaide content formatted for Telegram.

    Platform Constraints:
    - Max length: 4,096 characters
    - Formatting: *bold*, _italic_, [text](url) links
    - Supports more formatting than WhatsApp
    - No complex tables
    """

    MAX_LENGTH = 4096

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content for Telegram.

        Args:
            data: Adelaide content dict

        Returns:
            Telegram-compatible message (<=4,096 chars)
        """
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}
        locale = edition.get('locale', 'en')

        lines = []

        # Title
        title_emoji = content.get('title_emoji', '[chart emoji]')
        lines.append(f"{title_emoji} *Adelaide Daily Update*")
        lines.append("")

        # Greeting
        greeting = content.get('persona_greeting', '')
        if greeting:
            lines.append(greeting)
            lines.append("")

        # Intro message
        intro = content.get('greeting_message', '')
        if intro:
            intro = self._convert_markdown_to_telegram(intro)
            lines.append(intro)
            lines.append("")

        # Market section
        market_title = content.get('market_section_title', 'Market Update')
        lines.append(f"*{market_title}*")
        lines.append("")

        # Market data
        btc_change = content.get('btc_24h_change', 0)
        eth_change = content.get('eth_24h_change', 0)
        sol_change = content.get('sol_24h_change', 0)

        lines.append(f"[chart up emoji] BTC: {btc_change:+.1f}%")
        lines.append(f"[chart up emoji] ETH: {eth_change:+.1f}%")
        if sol_change:
            lines.append(f"[chart up emoji] SOL: {sol_change:+.1f}%")

        fg = content.get('fear_greed_index', 50)
        fg_label = content.get('fear_greed_label', 'Neutral')
        fg_emoji = content.get('fear_greed_emoji', '')
        lines.append(f"[fear emoji] Fear & Greed: {fg} ({fg_label}) {fg_emoji}")
        lines.append("")

        # Strategy status (simplified)
        strategy_note = content.get('strategy_note', '')
        if strategy_note:
            strategy_note = self._convert_markdown_to_telegram(strategy_note)
            lines.append(f"*Strategy Status:* {strategy_note}")
            lines.append("")

        # Insight
        if content.get('insight_content'):
            insight = content['insight_content']
            # Take first 300 chars for Telegram
            if len(insight) > 300:
                insight = insight[:297] + "..."
            insight = self._convert_markdown_to_telegram(insight)
            lines.append(f"[light bulb emoji] *Insight:* {insight}")
            lines.append("")

        # Closing
        closing = content.get('closing_wisdom', '')
        if closing:
            lines.append(f"_{closing}_")
            lines.append("")

        # Signature with link
        lines.append("- Adelaide | [diBoaS](https://diboas.com)")

        # AI disclosure
        ai_disclosure = content.get('ai_disclosure', '[robot emoji] AI-generated content')
        lines.append("")
        lines.append(f"_{ai_disclosure}_")

        result = "\n".join(lines)

        # Ensure we don't exceed max length
        if len(result) > self.MAX_LENGTH:
            result = result[:self.MAX_LENGTH - 3] + "..."

        return result

    def _convert_markdown_to_telegram(self, text: str) -> str:
        """Convert standard markdown to Telegram markdown."""
        # Telegram uses *bold* and _italic_
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        # Keep links as [text](url) - Telegram supports this
        return text

    @property
    def output_type(self) -> str:
        return "telegram"


@OutputRegistry.register("twitter")
class TwitterFormatter(OutputFormatter):
    """
    Adelaide content as single Twitter post.

    Platform Constraints:
    - Max length: 280 characters
    - Plain text only
    - URLs count as ~23 characters
    - Extract single key insight
    """

    MAX_LENGTH = 280
    URL_LENGTH = 23  # t.co shortened URLs

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content as single tweet.

        Args:
            data: Adelaide content dict

        Returns:
            Single tweet (<=280 chars)
        """
        content = data.get('content', data) if isinstance(data, dict) else data

        btc_change = content.get('btc_24h_change', 0)
        fg = content.get('fear_greed_index', 50)

        # Build hook based on market
        if btc_change > 3:
            hook = f"[chart up emoji] Markets up! BTC +{btc_change:.1f}%"
        elif btc_change < -3:
            hook = f"[chart down emoji] Markets down. BTC {btc_change:.1f}%"
        else:
            hook = f"[chart emoji] Markets steady. BTC {btc_change:+.1f}%"

        # Fear & Greed summary
        fg_text = f"Fear & Greed: {fg}"

        # Build tweet with link placeholder
        link = "diboas.com/daily"  # Will be shortened to ~23 chars

        # Calculate available space
        base = f"{hook}\n{fg_text}\n\nFull analysis: {link}"

        if len(base) <= self.MAX_LENGTH:
            return base

        # If too long, shorten
        return f"{hook}\n\nFull analysis: {link}"

    @property
    def output_type(self) -> str:
        return "twitter"


@OutputRegistry.register("substack")
class SubstackFormatter(OutputFormatter):
    """
    Full article format for Substack newsletter.

    Complete long-form content suitable for email newsletter.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content for Substack.

        Args:
            data: Adelaide content dict

        Returns:
            Full Substack article in Markdown
        """
        # Import here to avoid circular imports
        from src.registries.formatters.newsletter import NewsletterMarkdownFormatter

        # Substack uses the full newsletter format
        # Delegate to newsletter formatter but add Substack-specific headers
        newsletter_formatter = NewsletterMarkdownFormatter(self.config)
        base_content = newsletter_formatter.format(data, config)

        # Add Substack-specific frontmatter
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}

        lines = []

        # Substack frontmatter (for programmatic posting)
        lines.append("---")
        lines.append(f"title: Adelaide Daily - {edition.get('date', 'Today')}")
        lines.append("subtitle: Your daily market companion")
        lines.append("---")
        lines.append("")

        # Add the newsletter content
        lines.append(base_content)

        # Substack-specific footer
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Thanks for reading Adelaide Daily. Subscribe for free to receive new posts.*")
        lines.append("")
        lines.append("[Share](https://diboas.substack.com)")

        return "\n".join(lines)

    @property
    def output_type(self) -> str:
        return "substack"
