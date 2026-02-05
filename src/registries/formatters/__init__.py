"""
Output Formatters Package.

Contains all output formatters organized by category:
- base: Base classes and registry
- legacy: Wrappers for existing reporters (JSON, CSV, Markdown)
- newsletter: Full newsletter formatters
- social: Social media formatters (WhatsApp, Telegram, Twitter, LinkedIn, Substack)
"""

from src.registries.formatters.base import OutputFormatter, OutputRegistry
from src.registries.formatters.legacy import (
    JSONOutputFormatter,
    CSVOutputFormatter,
    MarkdownOutputFormatter,
)
from src.registries.formatters.newsletter import (
    NewsletterMarkdownFormatter,
    TwitterThreadFormatter,
    WebsiteTeaserFormatter,
    LinkedInPostFormatter,
)
from src.registries.formatters.social import (
    WhatsAppFormatter,
    TelegramFormatter,
    TwitterFormatter,
    SubstackFormatter,
)

__all__ = [
    # Base
    'OutputFormatter',
    'OutputRegistry',
    # Legacy
    'JSONOutputFormatter',
    'CSVOutputFormatter',
    'MarkdownOutputFormatter',
    # Newsletter
    'NewsletterMarkdownFormatter',
    'TwitterThreadFormatter',
    'WebsiteTeaserFormatter',
    'LinkedInPostFormatter',
    # Social
    'WhatsAppFormatter',
    'TelegramFormatter',
    'TwitterFormatter',
    'SubstackFormatter',
]
