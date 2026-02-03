"""
Output Registry for output formatters.

Wraps existing reporters and provides interface for future Adelaide formatters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


class OutputFormatter(ABC):
    """
    Abstract base class for all output formatters.

    All formatters must implement format() and declare their output_type.
    """

    @abstractmethod
    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data for output.

        Args:
            data: Data to format (type depends on formatter)
            config: Optional formatting configuration

        Returns:
            Formatted string output
        """
        pass

    @property
    @abstractmethod
    def output_type(self) -> str:
        """
        Return the type of output.

        Returns:
            One of: 'json', 'csv', 'markdown', 'newsletter', 'twitter', 'html', etc.
        """
        pass

    def get_name(self) -> str:
        """Get the formatter name for logging."""
        return self.__class__.__name__

    def export(self, data: Any, filepath: Path, config: Optional[Dict[str, Any]] = None) -> Path:
        """
        Format and export data to a file.

        Args:
            data: Data to format
            filepath: Output file path
            config: Optional formatting configuration

        Returns:
            Path to the output file
        """
        content = self.format(data, config)
        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Exported {self.output_type} to {filepath}")
        return filepath


class OutputRegistry(Registry[OutputFormatter]):
    """
    Registry for output formatters.

    Usage:
        formatter = OutputRegistry.get_instance().get("json", {})
        output = formatter.format(results)
    """
    pass


# =============================================================================
# Wrapped Implementations
# =============================================================================

@OutputRegistry.register("json")
class JSONOutputFormatter(OutputFormatter):
    """
    Wrapper for JSONReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.json_reporter import JSONReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = JSONReporter(output_dir=Path(output_dir)) if output_dir else JSONReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as JSON.

        Args:
            data: Data to format (results, validation report, etc.)
            config: Optional config with:
                - indent: JSON indentation (default: 2)
                - include_metadata: Whether to include metadata

        Returns:
            JSON string
        """
        import json
        from datetime import datetime

        config = config or {}
        indent = config.get('indent', 2)

        # Build output structure
        output = {
            'generated_at': datetime.utcnow().isoformat()
        }

        # Handle different data types
        if isinstance(data, list):
            if data and hasattr(data[0], 'to_dict'):
                output['results'] = [item.to_dict() for item in data]
            else:
                output['results'] = data
        elif hasattr(data, 'to_dict'):
            output.update(data.to_dict())
        elif isinstance(data, dict):
            output.update(data)
        else:
            output['data'] = str(data)

        return json.dumps(output, indent=indent, default=str)

    @property
    def output_type(self) -> str:
        return "json"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, metadata=None, filename='battle_test_results.json') -> Path:
        """Export Battle Test results."""
        return self._reporter.export_battle_test(results, metadata, filename)

    def export_monte_carlo(self, results, metadata=None, filename='monte_carlo_results.json') -> Path:
        """Export Monte Carlo results."""
        return self._reporter.export_monte_carlo(results, metadata, filename)

    def export_validation(self, report, filename='validation_report.json') -> Path:
        """Export validation report."""
        return self._reporter.export_validation(report, filename)


@OutputRegistry.register("csv")
class CSVOutputFormatter(OutputFormatter):
    """
    Wrapper for CSVReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.csv_reporter import CSVReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = CSVReporter(output_dir=Path(output_dir)) if output_dir else CSVReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as CSV.

        Args:
            data: Data to format (list of results with to_dict())
            config: Optional config

        Returns:
            CSV string
        """
        import io
        import csv

        if isinstance(data, list) and data:
            if hasattr(data[0], 'to_dict'):
                rows = [item.to_dict() for item in data]
            else:
                rows = data

            if rows:
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                return output.getvalue()

        return ""

    @property
    def output_type(self) -> str:
        return "csv"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, filename='battle_test_results.csv') -> Path:
        """Export Battle Test results."""
        return self._reporter.export_battle_test(results, filename)

    def export_monte_carlo(self, results, filename='monte_carlo_results.csv') -> Path:
        """Export Monte Carlo results."""
        return self._reporter.export_monte_carlo(results, filename)


@OutputRegistry.register("markdown")
class MarkdownOutputFormatter(OutputFormatter):
    """
    Wrapper for MarkdownReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.markdown_reporter import MarkdownReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = MarkdownReporter(output_dir=Path(output_dir)) if output_dir else MarkdownReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as Markdown.

        Args:
            data: Data to format
            config: Optional config with:
                - title: Report title
                - include_summary: Whether to include summary section

        Returns:
            Markdown string
        """
        from datetime import datetime

        config = config or {}
        title = config.get('title', 'Results Report')

        lines = [
            f"# {title}",
            "",
            f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            "",
        ]

        # Handle different data types
        if isinstance(data, list) and data:
            if hasattr(data[0], 'to_dict'):
                rows = [item.to_dict() for item in data]
            else:
                rows = data

            if rows:
                # Create table
                headers = list(rows[0].keys())
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

                for row in rows:
                    values = [str(row.get(h, '')) for h in headers]
                    lines.append("| " + " | ".join(values) + " |")

        elif hasattr(data, 'to_dict'):
            for key, value in data.to_dict().items():
                lines.append(f"**{key}**: {value}")

        elif isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"**{key}**: {value}")

        return "\n".join(lines)

    @property
    def output_type(self) -> str:
        return "markdown"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, metadata=None, filename='battle_test_report.md') -> Path:
        """Export Battle Test report."""
        # MarkdownReporter uses generate_* methods
        # Extract scenario from metadata if available
        scenario = 'A'
        if metadata and hasattr(metadata, 'scenario'):
            scenario = metadata.scenario
        return self._reporter.generate_battle_test_report(results, scenario, filename)

    def export_monte_carlo(self, results, metadata=None, filename='monte_carlo_report.md') -> Path:
        """Export Monte Carlo report."""
        # MarkdownReporter uses generate_* methods
        return self._reporter.generate_monte_carlo_report(results, filename)


# =============================================================================
# Adelaide Formatters - Multi-Channel Output
# =============================================================================

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
        from datetime import datetime

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

    5-7 tweets, each ≤280 characters.

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
        lines.append("**[Read the full Adelaide Daily →]**")

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
            lines.append(f"Crypto Markets Move {abs(btc_change):.1f}% — Here's the Context")
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
        lines.append("• Daily moves are normal — focus on your timeframe")
        lines.append("• Sentiment indicators help, but don't predict")
        lines.append("• Your strategy should match your goals")
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
