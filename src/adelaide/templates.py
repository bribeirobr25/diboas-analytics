"""
Template Engine for Adelaide.

Handles loading, rendering, and managing newsletter templates.
Templates are deterministic (no LLM) - they use placeholder
substitution and conditional sections.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import re
import logging

logger = logging.getLogger(__name__)

# Template directory
TEMPLATE_DIR = Path(__file__).parent / "templates"


class TemplateEngine:
    """
    Template engine for Adelaide newsletter generation.

    Loads templates from files, fills placeholders with data,
    and handles conditional sections.

    Usage:
        engine = TemplateEngine()
        content = engine.render("daily_calm", data, persona="ana")
    """

    def __init__(self, template_dir: Path = None):
        """Initialize with optional custom template directory."""
        self.template_dir = template_dir or TEMPLATE_DIR
        self._cache: Dict[str, str] = {}

    def render(
        self,
        template_name: str,
        data: Dict[str, Any],
        persona: str = "ana",
        locale: str = "en"
    ) -> str:
        """
        Render a template with data.

        Args:
            template_name: Template identifier (e.g., "daily_calm")
            data: Dictionary of data to fill placeholders
            persona: Persona name for adaptation
            locale: Locale for localization

        Returns:
            Rendered template string
        """
        # Load template
        template = self._load_template(template_name)
        if not template:
            logger.error(f"Template not found: {template_name}")
            return self._get_fallback_content(data, persona)

        # Process conditional sections
        template = self._process_conditionals(template, data)

        # Fill placeholders
        content = self._fill_placeholders(template, data)

        return content

    def _load_template(self, name: str) -> Optional[str]:
        """Load template from file or cache."""
        if name in self._cache:
            return self._cache[name]

        filepath = self.template_dir / f"{name}.md"
        if not filepath.exists():
            logger.warning(f"Template file not found: {filepath}")
            return None

        try:
            content = filepath.read_text(encoding='utf-8')
            self._cache[name] = content
            return content
        except Exception as e:
            logger.error(f"Failed to load template {name}: {e}")
            return None

    def _process_conditionals(self, template: str, data: Dict[str, Any]) -> str:
        """
        Process conditional sections in template.

        Syntax:
            {{#if condition}}content{{/if}}
            {{#if condition}}content{{else}}alternative{{/if}}
        """
        # Simple if blocks: {{#if key}}...{{/if}}
        pattern = r'\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}'

        def replace_if(match):
            key = match.group(1)
            content = match.group(2)

            # Check for else clause
            if '{{else}}' in content:
                if_content, else_content = content.split('{{else}}', 1)
            else:
                if_content = content
                else_content = ''

            # Evaluate condition
            value = data.get(key)
            if value:
                return if_content
            else:
                return else_content

        return re.sub(pattern, replace_if, template, flags=re.DOTALL)

    def _fill_placeholders(self, template: str, data: Dict[str, Any]) -> str:
        """
        Fill placeholders in template.

        Syntax:
            {{key}} - Simple replacement
            {{key|format}} - With format specifier
            {{key|default:value}} - With default value
        """
        # Pattern for placeholders: {{key}}, {{key|format}}, {{key|default:value}}
        pattern = r'\{\{(\w+)(?:\|([^}]+))?\}\}'

        def replace_placeholder(match):
            key = match.group(1)
            modifier = match.group(2)

            value = data.get(key, '')

            # Handle modifiers
            if modifier:
                if modifier.startswith('default:'):
                    default = modifier[8:]
                    value = value if value else default
                elif modifier == 'percent':
                    try:
                        value = f"{float(value):+.2f}%"
                    except (ValueError, TypeError):
                        value = str(value)
                elif modifier == 'currency':
                    try:
                        value = f"${float(value):,.2f}"
                    except (ValueError, TypeError):
                        value = str(value)
                elif modifier == 'number':
                    try:
                        value = f"{float(value):,.0f}"
                    except (ValueError, TypeError):
                        value = str(value)
                elif modifier == 'date':
                    if isinstance(value, (date, datetime)):
                        value = value.strftime('%B %d, %Y')
                elif modifier == 'upper':
                    value = str(value).upper()
                elif modifier == 'lower':
                    value = str(value).lower()

            return str(value) if value is not None else ''

        return re.sub(pattern, replace_placeholder, template)

    def _get_fallback_content(self, data: Dict[str, Any], persona: str) -> str:
        """Generate fallback content when template is missing."""
        today = datetime.now().strftime('%B %d, %Y')
        return f"""# Adelaide Daily Update

**{today}**

Market data is being processed. Please check back shortly.

---

*This is educational content only, not financial advice. Past performance does not guarantee future results. You decide what's best for your situation.*
"""

    def get_available_templates(self) -> List[str]:
        """List available templates."""
        if not self.template_dir.exists():
            return []

        templates = []
        for f in self.template_dir.glob("*.md"):
            templates.append(f.stem)
        return sorted(templates)

    def clear_cache(self):
        """Clear template cache."""
        self._cache.clear()


# Insight library - 23 templates as specified
INSIGHT_LIBRARY = {
    # Market Context (5)
    "market_accumulation": {
        "title": "Accumulation Pattern",
        "content": "Large wallets have been gradually adding to positions. This doesn't predict prices, but shows long-term confidence from major holders.",
        "category": "market",
        "min_days_between": 7,
    },
    "market_distribution": {
        "title": "Distribution Pattern",
        "content": "Some large wallets are reducing positions. This could mean profit-taking, rebalancing, or other portfolio management - we can't know their reasons.",
        "category": "market",
        "min_days_between": 7,
    },
    "market_correlation": {
        "title": "Correlation Shift",
        "content": "Crypto is moving differently from stocks today. This happens periodically - correlation isn't constant.",
        "category": "market",
        "min_days_between": 7,
    },
    "market_volatility": {
        "title": "Volatility Context",
        "content": "Price swings are larger than usual. This is normal for crypto and why time horizon matters more than daily moves.",
        "category": "market",
        "min_days_between": 7,
    },
    "market_macro": {
        "title": "Macro Headwinds",
        "content": "Traditional markets are influencing crypto today. When stocks struggle, crypto often follows - at least in the short term.",
        "category": "market",
        "min_days_between": 7,
    },

    # Strategy Education (5)
    "edu_yield": {
        "title": "Understanding Yields",
        "content": "Yields come from protocol activity - lending, trading fees, or staking rewards. Higher yields usually mean more risk. There's no free lunch.",
        "category": "strategy",
        "min_days_between": 14,
    },
    "edu_risk_reward": {
        "title": "Risk and Reward",
        "content": "Higher potential returns always come with higher potential losses. Choosing your comfort level is personal - there's no wrong answer.",
        "category": "strategy",
        "min_days_between": 14,
    },
    "edu_diversification": {
        "title": "Why Diversification",
        "content": "Spreading across different strategies means no single bad day affects everything. It won't maximize gains, but it can help smooth the ride.",
        "category": "strategy",
        "min_days_between": 14,
    },
    "edu_time_horizon": {
        "title": "Time Horizon Reminder",
        "content": "Strategies work differently over days, months, and years. Short-term noise often fades in longer timeframes.",
        "category": "strategy",
        "min_days_between": 14,
    },
    "edu_compound": {
        "title": "Compound Growth",
        "content": "Yields earn yields over time. It's slow to start but can add up. The key is consistency, not timing.",
        "category": "strategy",
        "min_days_between": 14,
    },

    # Behavioral (5)
    "behav_stay_calm": {
        "title": "Staying Calm",
        "content": "Down days feel worse than up days feel good. That's human nature, not a sign you should act. Breathing room matters.",
        "category": "behavioral",
        "min_days_between": 7,
    },
    "behav_avoid_fomo": {
        "title": "Avoiding FOMO",
        "content": "Big green days tempt us to add more. History shows chasing rallies often disappoints. Your plan was made for a reason.",
        "category": "behavioral",
        "min_days_between": 7,
    },
    "behav_automation": {
        "title": "Benefits of Automation",
        "content": "Automated strategies remove emotional decisions. They won't catch every opportunity, but they won't panic-sell either.",
        "category": "behavioral",
        "min_days_between": 14,
    },
    "behav_dca": {
        "title": "Dollar Cost Averaging",
        "content": "Adding the same amount regularly means you buy more when prices are low, less when high. Simple, but effective over time.",
        "category": "behavioral",
        "min_days_between": 14,
    },
    "behav_exit_dignity": {
        "title": "It's OK to Exit",
        "content": "If your circumstances changed, or this no longer feels right, exiting is valid. Your peace of mind has value too.",
        "category": "behavioral",
        "min_days_between": 7,
    },

    # Technical (5)
    "tech_protocol_health": {
        "title": "Protocol Health Check",
        "content": "The protocols in your strategies are functioning normally. Smart contracts are doing what they're designed to do.",
        "category": "technical",
        "min_days_between": 7,
    },
    "tech_protocol_warning": {
        "title": "Protocol Update",
        "content": "One of our monitored protocols is experiencing higher than usual activity. We're watching closely. No action needed yet.",
        "category": "technical",
        "min_days_between": 3,
    },
    "tech_estate_context": {
        "title": "Estate Monitoring",
        "content": "We track bankrupt estate wallets for unusual activity. This helps anticipate potential market moves from forced selling.",
        "category": "technical",
        "min_days_between": 14,
    },
    "tech_whale_context": {
        "title": "Whale Watching",
        "content": "Large wallet movements can signal upcoming volatility. But we can't know intentions - they could be moving to cold storage, to exchanges, or between funds.",
        "category": "technical",
        "min_days_between": 7,
    },
    "tech_stablecoin": {
        "title": "Stablecoin Status",
        "content": "Major stablecoins are maintaining their pegs normally. This is the foundation that DeFi protocols rely on.",
        "category": "technical",
        "min_days_between": 14,
    },

    # Celebration (3)
    "celeb_first_yield": {
        "title": "First Yield Earned",
        "content": "Congratulations on earning your first yield! Small steps add up. Your money is working while you sleep.",
        "category": "celebration",
        "min_days_between": 30,
    },
    "celeb_outperform": {
        "title": "Strategy Outperforming",
        "content": "Your chosen strategy has been performing well recently. Remember: past performance doesn't predict the future, but it's nice to acknowledge good periods.",
        "category": "celebration",
        "min_days_between": 14,
    },
    "celeb_consistency": {
        "title": "Consistent Returns",
        "content": "Your strategy has delivered returns for multiple periods in a row. Consistency matters more than occasional big wins.",
        "category": "celebration",
        "min_days_between": 14,
    },
}


def get_insight(insight_id: str) -> Optional[Dict[str, Any]]:
    """Get insight template by ID."""
    return INSIGHT_LIBRARY.get(insight_id)


def get_insights_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all insights in a category."""
    return [
        {**v, 'id': k}
        for k, v in INSIGHT_LIBRARY.items()
        if v['category'] == category
    ]


def select_insight(
    category: str = None,
    recent_insights: List[str] = None,
    market_conditions: Dict[str, Any] = None
) -> Optional[Dict[str, Any]]:
    """
    Select an appropriate insight based on conditions.

    Args:
        category: Optional category filter
        recent_insights: List of recently used insight IDs
        market_conditions: Current market data

    Returns:
        Selected insight dict with 'id' key added
    """
    recent_insights = recent_insights or []

    # Filter by category if specified
    if category:
        candidates = get_insights_by_category(category)
    else:
        candidates = [{**v, 'id': k} for k, v in INSIGHT_LIBRARY.items()]

    # Remove recently used
    candidates = [c for c in candidates if c['id'] not in recent_insights]

    if not candidates:
        # If all used, reset
        candidates = [{**v, 'id': k} for k, v in INSIGHT_LIBRARY.items()]
        if category:
            candidates = [c for c in candidates if c['category'] == category]

    # For now, return first candidate
    # In production, would add scoring based on market_conditions
    return candidates[0] if candidates else None
