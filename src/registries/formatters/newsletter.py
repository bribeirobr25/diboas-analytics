"""
Newsletter formatters for Adelaide.

Contains:
- NewsletterMarkdownFormatter: Full newsletter in Markdown
- TwitterThreadFormatter: Multi-tweet thread format
- WebsiteTeaserFormatter: Short teaser for website
- LinkedInPostFormatter: Professional LinkedIn format
"""

from typing import Any, Dict, Optional
from datetime import datetime
import logging

from src.registries.formatters.base import OutputFormatter, OutputRegistry

logger = logging.getLogger(__name__)


@OutputRegistry.register("newsletter_md")
class NewsletterMarkdownFormatter(OutputFormatter):
    """
    Adelaide newsletter in Markdown format.

    Full newsletter with all sections:
    - Header with date and edition type
    - Market snapshot table
    - Strategy performance section
    - Adelaide insight block
    - Disclaimers
    - Footer
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content as full Markdown newsletter.

        Args:
            data: Adelaide content dict with keys:
                - edition: {type, date, persona, locale, regime}
                - content: {greeting, market_snapshot, insight, etc.}
                - metadata: {word_count, read_time, etc.}

        Returns:
            Complete Markdown newsletter
        """
        config = config or {}

        # Handle both raw data and structured Adelaide output
        if isinstance(data, dict) and 'rendered_content' in data:
            # Already rendered by Adelaide generator
            return data['rendered_content']

        # Build newsletter from data
        lines = []

        # Header
        edition = data.get('edition', {})
        date_str = edition.get('date', datetime.now().strftime('%Y-%m-%d'))
        persona = edition.get('persona', 'ana')
        edition_type = edition.get('type', 'daily').title()

        lines.append(f"# Adelaide {edition_type} Update")
        lines.append("")
        lines.append(f"**{date_str}** | {persona.title()} Edition")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Greeting
        content = data.get('content', data)
        if content.get('greeting_message'):
            lines.append(f"## {content.get('greeting', 'Hello')}")
            lines.append("")
            lines.append(content['greeting_message'])
            lines.append("")
            lines.append("---")
            lines.append("")

        # Market snapshot
        if content.get('market_snapshot'):
            lines.append("## Market Snapshot")
            lines.append("")
            lines.append("| Asset | Price | 24h Change |")
            lines.append("|-------|-------|------------|")

            snapshot = content['market_snapshot']
            for asset in ['btc', 'eth', 'sol', 'sp500']:
                if f'{asset}_price' in snapshot:
                    price = snapshot.get(f'{asset}_price', 'N/A')
                    change = snapshot.get(f'{asset}_24h_change', 0)
                    lines.append(f"| {asset.upper()} | ${price:,.2f} | {change:+.2f}% |")

            lines.append("")
            if 'fear_greed_index' in snapshot:
                fg = snapshot['fear_greed_index']
                label = snapshot.get('fear_greed_label', 'Neutral')
                lines.append(f"**Fear & Greed Index:** {fg} ({label})")
                lines.append("")

            lines.append("---")
            lines.append("")

        # Strategy section
        if content.get('strategy_summary'):
            lines.append("## Strategy Overview")
            lines.append("")
            lines.append(content['strategy_summary'])
            lines.append("")
            lines.append("---")
            lines.append("")

        # Insight
        if content.get('insight_content'):
            lines.append("## Adelaide's Insight")
            lines.append("")
            if content.get('insight_title'):
                lines.append(f"**{content['insight_title']}**")
                lines.append("")
            lines.append(content['insight_content'])
            lines.append("")
            lines.append("---")
            lines.append("")

        # Disclaimer
        disclaimer = content.get('disclaimer', self._get_default_disclaimer())
        lines.append(disclaimer)
        lines.append("")

        # Footer
        lines.append("---")
        lines.append("")
        signature = content.get('signature', 'Adelaide')
        lines.append(signature)
        lines.append("")
        lines.append("**You decide what's best for your situation.**")

        return "\n".join(lines)

    def _get_default_disclaimer(self) -> str:
        """Get default disclaimer."""
        return """**Important Disclosures**

This content is for educational purposes only and does not constitute investment advice. Past performance is not indicative of future results. Consider consulting a licensed financial adviser for guidance specific to your situation."""

    @property
    def output_type(self) -> str:
        return "newsletter_md"


@OutputRegistry.register("twitter_thread")
class TwitterThreadFormatter(OutputFormatter):
    """
    Adelaide content formatted as Twitter thread.

    5-7 tweets, each <=280 characters.

    Structure:
    1. Hook tweet with market summary
    2. Key data points
    3. Insight tweet
    4. Action/perspective tweet
    5. CTA to full content
    """

    MAX_TWEET_LENGTH = 280
    MIN_TWEETS = 5
    MAX_TWEETS = 7

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content as Twitter thread.

        Args:
            data: Adelaide content dict

        Returns:
            Numbered thread format (1/n, 2/n, etc.)
        """
        tweets = []

        # Handle both raw data and structured Adelaide output
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}

        # Tweet 1: Hook with market summary
        btc_change = content.get('btc_24h_change', 0)
        if btc_change > 2:
            hook = f"Markets up today. BTC {btc_change:+.1f}%"
        elif btc_change < -2:
            hook = f"Markets down today. BTC {btc_change:+.1f}%"
        else:
            hook = f"Quiet day in markets. BTC {btc_change:+.1f}%"

        tweets.append(f"{hook}\n\nHere's what you need to know:")

        # Tweet 2: Key data points
        fg = content.get('fear_greed_index', 50)
        fg_label = content.get('fear_greed_label', 'Neutral')
        tweets.append(f"Fear & Greed Index: {fg} ({fg_label})\n\nSentiment is {fg_label.lower()} across the market.")

        # Tweet 3: Strategy performance
        if content.get('strategy_summary'):
            summary = content['strategy_summary'][:200]
            tweets.append(f"Strategy update:\n\n{summary}...")

        # Tweet 4: Insight
        if content.get('insight_content'):
            insight = content['insight_content']
            if len(insight) > 250:
                insight = insight[:247] + "..."
            tweets.append(insight)

        # Tweet 5: Perspective
        tweets.append("Remember: Daily moves matter less than your long-term plan.\n\nStay informed, stay calm.")

        # Tweet 6: CTA
        tweets.append("Want the full analysis? Check our daily newsletter.\n\nLink in bio.")

        # Format as numbered thread
        total = len(tweets)
        formatted = []
        for i, tweet in enumerate(tweets, 1):
            formatted.append(f"{i}/{total} {tweet}")

        return "\n\n---\n\n".join(formatted)

    def format_as_list(self, data: Any, config: Optional[Dict[str, Any]] = None) -> list:
        """Return tweets as a list instead of joined string."""
        formatted = self.format(data, config)
        return formatted.split("\n\n---\n\n")

    @property
    def output_type(self) -> str:
        return "twitter_thread"


@OutputRegistry.register("website_teaser")
class WebsiteTeaserFormatter(OutputFormatter):
    """
    Adelaide content as website teaser (max 150 words).

    Short teaser that hooks reader to full content.

    Structure:
    - Hook headline
    - 2-3 key insights
    - "Read more" CTA
    """

    MAX_WORDS = 150

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content as website teaser.

        Args:
            data: Adelaide content dict

        Returns:
            Short teaser text with CTA
        """
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}

        lines = []

        # Hook headline based on market
        btc_change = content.get('btc_24h_change', 0)
        if btc_change > 5:
            lines.append("**Markets Rally: What It Means for You**")
        elif btc_change < -5:
            lines.append("**Market Dip: Staying Calm**")
        else:
            lines.append("**Today's Market Update**")

        lines.append("")

        # Key insight
        if content.get('insight_content'):
            insight = content['insight_content']
            # Truncate to ~50 words
            words = insight.split()[:50]
            lines.append(' '.join(words) + "...")
        else:
            fg = content.get('fear_greed_index', 50)
            lines.append(f"Fear & Greed at {fg}. Markets are showing mixed signals today.")

        lines.append("")

        # CTA
        lines.append("**[Read the full Adelaide Daily ->]**")

        return "\n".join(lines)

    @property
    def output_type(self) -> str:
        return "website_teaser"


@OutputRegistry.register("linkedin_post")
class LinkedInPostFormatter(OutputFormatter):
    """
    Adelaide content formatted for LinkedIn.

    Professional tone, 300-500 words.

    Structure:
    - Professional headline
    - Market context
    - Key insights
    - Takeaways
    - Engagement hook
    """

    MIN_WORDS = 300
    MAX_WORDS = 500

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content for LinkedIn.

        Args:
            data: Adelaide content dict

        Returns:
            LinkedIn-optimized post
        """
        content = data.get('content', data) if isinstance(data, dict) else data
        edition = data.get('edition', {}) if isinstance(data, dict) else {}

        lines = []

        # Professional headline
        btc_change = content.get('btc_24h_change', 0)
        if abs(btc_change) > 5:
            lines.append(f"Crypto Markets Move {abs(btc_change):.1f}% - Here's the Context")
        else:
            lines.append("Daily Crypto Market Analysis")

        lines.append("")

        # Market context
        fg = content.get('fear_greed_index', 50)
        fg_label = content.get('fear_greed_label', 'Neutral')

        lines.append(f"Today's Fear & Greed Index: {fg} ({fg_label})")
        lines.append("")
        lines.append(f"Bitcoin moved {btc_change:+.2f}% in the last 24 hours. Here's what the data tells us:")
        lines.append("")

        # Key insights
        if content.get('insight_content'):
            lines.append("KEY INSIGHT:")
            lines.append(content['insight_content'])
            lines.append("")

        # Strategy context
        if content.get('strategy_summary'):
            lines.append("WHAT THIS MEANS:")
            lines.append(content['strategy_summary'])
            lines.append("")

        # Takeaways
        lines.append("TAKEAWAYS:")
        lines.append("* Daily moves are normal - focus on your timeframe")
        lines.append("* Sentiment indicators help, but don't predict")
        lines.append("* Your strategy should match your goals")
        lines.append("")

        # Professional closing
        lines.append("---")
        lines.append("")
        lines.append("What's your approach to market volatility? Share in the comments.")
        lines.append("")
        lines.append("#Crypto #DigitalAssets #MarketAnalysis #DeFi #Investment")

        return "\n".join(lines)

    @property
    def output_type(self) -> str:
        return "linkedin_post"
