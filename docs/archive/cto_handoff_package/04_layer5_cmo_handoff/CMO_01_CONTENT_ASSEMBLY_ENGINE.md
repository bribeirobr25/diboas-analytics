# CMO_01: Content Assembly Engine
## Data â†’ Content Transformation Specification

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P0 (Launch-Critical)

---

## 1. Purpose

The Content Assembly Engine transforms Layer 4 alert objects into formatted Adelaide newsletter content. It is the core of Layer 5 and the first step in the presentation pipeline.

### Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Template Selection | Choose appropriate template based on market conditions |
| Insight Selection | Select relevant insight from 20+ categories |
| Section Population | Fill template sections with data |
| Content Budget | Enforce size limits (100KB daily, 250KB weekly) |
| Fallback Handling | Gracefully handle missing data |

---

## 2. Template Selection System

### 2.1 Template Categories

| Category | Templates | Trigger Condition |
|----------|-----------|-------------------|
| **Daily** | calm_day, down_day, up_day | Market conditions |
| **Weekly** | review_standard, review_volatile | Week volatility |
| **Monthly** | performance_report | 1st of month |
| **Quarterly** | comprehensive_review | Q1/Q2/Q3/Q4 |
| **Crisis** | level_1 through level_5 | Crisis triggers |

### 2.2 Daily Template Selection Logic

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional

class DailyTemplate(Enum):
    CALM_DAY = "daily_calm"
    DOWN_DAY = "daily_down"
    UP_DAY = "daily_up"

class MarketCondition(Enum):
    CALM = "calm"
    SIGNIFICANT_DOWN = "significant_down"
    MODERATE_DOWN = "moderate_down"
    MODERATE_UP = "moderate_up"
    SIGNIFICANT_UP = "significant_up"

@dataclass
class MarketData:
    btc_change_24h: float
    eth_change_24h: float
    sp500_change_24h: float
    vix: float
    whale_net_flow: float
    estate_alerts_count: int

class TemplateSelector:
    """Select appropriate template based on market conditions."""
    
    # Thresholds for market condition classification
    THRESHOLDS = {
        'significant_down': -5.0,    # BTC down >5%
        'moderate_down': -2.0,       # BTC down 2-5%
        'moderate_up': 2.0,          # BTC up 2-5%
        'significant_up': 5.0,       # BTC up >5%
        'high_vix': 25.0,            # VIX above 25
        'whale_significant': 100_000_000,  # $100M whale movement
    }
    
    def classify_market(self, data: MarketData) -> MarketCondition:
        """Classify current market conditions."""
        btc = data.btc_change_24h
        
        # Check for significant movements first
        if btc <= self.THRESHOLDS['significant_down']:
            return MarketCondition.SIGNIFICANT_DOWN
        elif btc >= self.THRESHOLDS['significant_up']:
            return MarketCondition.SIGNIFICANT_UP
        elif btc <= self.THRESHOLDS['moderate_down']:
            return MarketCondition.MODERATE_DOWN
        elif btc >= self.THRESHOLDS['moderate_up']:
            return MarketCondition.MODERATE_UP
        else:
            return MarketCondition.CALM
    
    def select_daily_template(self, data: MarketData) -> DailyTemplate:
        """Select daily template based on market conditions."""
        condition = self.classify_market(data)
        
        # Template mapping
        template_map = {
            MarketCondition.CALM: DailyTemplate.CALM_DAY,
            MarketCondition.SIGNIFICANT_DOWN: DailyTemplate.DOWN_DAY,
            MarketCondition.MODERATE_DOWN: DailyTemplate.DOWN_DAY,
            MarketCondition.MODERATE_UP: DailyTemplate.UP_DAY,
            MarketCondition.SIGNIFICANT_UP: DailyTemplate.UP_DAY,
        }
        
        return template_map[condition]
    
    def select_template(
        self, 
        edition_type: str, 
        data: MarketData,
        crisis_level: Optional[int] = None
    ) -> str:
        """Select template for any edition type."""
        
        # Crisis overrides everything
        if crisis_level:
            return f"crisis_level_{crisis_level}"
        
        if edition_type == "daily":
            return self.select_daily_template(data).value
        elif edition_type == "weekly":
            # Weekly template based on week volatility
            avg_volatility = abs(data.btc_change_24h)  # Simplified; use 7-day in prod
            if avg_volatility > 10:
                return "weekly_volatile"
            return "weekly_standard"
        elif edition_type == "monthly":
            return "monthly_performance"
        elif edition_type == "quarterly":
            return "quarterly_comprehensive"
        
        return "daily_calm"  # Fallback
```

### 2.3 Template Selection Decision Tree

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    TEMPLATE SELECTION                           â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  Is Crisis Active?                                              â”‚
â”‚       â”‚                                                         â”‚
â”‚   Yes â”‚ No                                                      â”‚
â”‚   â–¼   â”‚                                                         â”‚
â”‚ crisis_level_N                                                  â”‚
â”‚       â”‚                                                         â”‚
â”‚       â–¼                                                         â”‚
â”‚  What Edition Type?                                             â”‚
â”‚       â”‚                                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”¼â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                               â”‚
â”‚  â”‚    â”‚    â”‚        â”‚          â”‚                               â”‚
â”‚  â–¼    â–¼    â–¼        â–¼          â–¼                               â”‚
â”‚ Daily Weekly Monthly Quarterly                                  â”‚
â”‚  â”‚     â”‚     â”‚        â”‚                                        â”‚
â”‚  â–¼     â–¼     â–¼        â–¼                                        â”‚
â”‚ BTC    Week  Always   Always                                    â”‚
â”‚ Change Vol   Same     Same                                      â”‚
â”‚  â”‚     â”‚                                                        â”‚
â”‚ â”Œâ”´â”€â”€â”€â”€â”€â”´â”                                                       â”‚
â”‚ â”‚ <-5%  â”‚ â†’ daily_down                                         â”‚
â”‚ â”‚ -5~-2%â”‚ â†’ daily_down                                         â”‚
â”‚ â”‚ -2~+2%â”‚ â†’ daily_calm                                         â”‚
â”‚ â”‚ +2~+5%â”‚ â†’ daily_up                                           â”‚
â”‚ â”‚ >+5%  â”‚ â†’ daily_up                                           â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”˜                                                       â”‚
â”‚                                                                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 3. Insight Selection Algorithm

### 3.1 Insight Categories

Adelaide has 20+ insight templates organized into categories:

```python
INSIGHT_CATEGORIES = {
    # Market Context (5 templates)
    'market_context': [
        'accumulation_signal',      # Whales buying
        'distribution_signal',      # Whales selling
        'correlation_breakdown',    # Unusual market behavior
        'volatility_context',       # VIX explanation
        'macro_headwind',          # Fed/rates context
    ],
    
    # Strategy Education (5 templates)
    'strategy_education': [
        'yield_explanation',        # How APY works
        'risk_reward_tradeoff',     # Risk vs return
        'diversification_benefit',  # Multiple strategies
        'time_horizon_reminder',    # Long-term focus
        'compound_growth',          # Power of compounding
    ],
    
    # Behavioral (5 templates)
    'behavioral': [
        'stay_calm_down_market',    # Don't panic sell
        'avoid_fomo_up_market',     # Don't chase pumps
        'automation_benefit',       # Set and forget
        'dca_reminder',             # Dollar cost averaging
        'exit_dignity',             # OK to exit if needed
    ],
    
    # Protocol/Technical (5 templates)
    'technical': [
        'protocol_health_good',     # TVL/utilization healthy
        'protocol_health_warning',  # TVL/utilization concern
        'estate_context',           # Bankruptcy wallet explanation
        'whale_context',            # What whale movements mean
        'stablecoin_health',        # USDS/USDC status
    ],
    
    # Milestone/Celebration (3+ templates)
    'celebration': [
        'first_yield_earned',       # Congrats on first return
        'strategy_outperformance',  # Beat benchmark
        'consistent_returns',       # N months positive
    ],
}

# Total: 23 insight templates
```

### 3.2 Insight Selection Logic

```python
from typing import List, Tuple
import random

class InsightSelector:
    """Select appropriate insight based on market context and user history."""
    
    def __init__(self, insight_history_days: int = 14):
        self.history_days = insight_history_days
        self.used_insights: List[Tuple[str, str]] = []  # (date, insight_id)
    
    def select_insight(
        self,
        market_data: MarketData,
        user_context: dict,
        recent_insights: List[str]
    ) -> str:
        """
        Select insight based on:
        1. Market conditions (primary driver)
        2. User context (personalization)
        3. Recent insight history (avoid repetition)
        """
        
        # Step 1: Determine eligible categories based on market
        eligible_categories = self._get_eligible_categories(market_data)
        
        # Step 2: Score insights within eligible categories
        scored_insights = self._score_insights(
            eligible_categories, 
            market_data, 
            user_context,
            recent_insights
        )
        
        # Step 3: Select top insight (with some randomization)
        return self._select_from_scored(scored_insights)
    
    def _get_eligible_categories(self, data: MarketData) -> List[str]:
        """Determine which insight categories are relevant."""
        categories = []
        
        # Market context always eligible
        categories.append('market_context')
        
        # Add behavioral based on conditions
        if data.btc_change_24h < -5:
            categories.append('behavioral')  # stay_calm_down_market
        elif data.btc_change_24h > 5:
            categories.append('behavioral')  # avoid_fomo_up_market
        
        # Add technical if protocol/whale activity
        if data.whale_net_flow != 0 or data.estate_alerts_count > 0:
            categories.append('technical')
        
        # Strategy education always available (low priority)
        categories.append('strategy_education')
        
        return categories
    
    def _score_insights(
        self,
        categories: List[str],
        market_data: MarketData,
        user_context: dict,
        recent_insights: List[str]
    ) -> List[Tuple[str, float]]:
        """Score insights based on relevance."""
        scores = []
        
        for category in categories:
            for insight_id in INSIGHT_CATEGORIES.get(category, []):
                score = 0.0
                
                # Base score by category priority
                category_priority = {
                    'market_context': 1.0,
                    'behavioral': 0.9,
                    'technical': 0.8,
                    'strategy_education': 0.6,
                    'celebration': 0.5,
                }
                score += category_priority.get(category, 0.5)
                
                # Bonus for market-specific relevance
                score += self._calculate_relevance_bonus(insight_id, market_data)
                
                # Penalty for recent use
                if insight_id in recent_insights:
                    days_since = self._days_since_used(insight_id)
                    score -= max(0, (self.history_days - days_since) / self.history_days)
                
                scores.append((insight_id, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def _calculate_relevance_bonus(self, insight_id: str, data: MarketData) -> float:
        """Calculate bonus for market-specific relevance."""
        bonus = 0.0
        
        # Specific insight â†’ market condition mappings
        if insight_id == 'stay_calm_down_market' and data.btc_change_24h < -5:
            bonus += 0.5
        elif insight_id == 'avoid_fomo_up_market' and data.btc_change_24h > 5:
            bonus += 0.5
        elif insight_id == 'whale_context' and abs(data.whale_net_flow) > 50_000_000:
            bonus += 0.4
        elif insight_id == 'estate_context' and data.estate_alerts_count > 0:
            bonus += 0.6  # Estate alerts are important
        elif insight_id == 'volatility_context' and data.vix > 25:
            bonus += 0.3
        
        return bonus
    
    def _select_from_scored(self, scored: List[Tuple[str, float]]) -> str:
        """Select from top insights with weighted randomization."""
        if not scored:
            return 'time_horizon_reminder'  # Safe default
        
        # Take top 3 and randomly select (weighted by score)
        top_3 = scored[:3]
        total_score = sum(s[1] for s in top_3)
        
        if total_score == 0:
            return top_3[0][0]
        
        # Weighted random selection
        r = random.uniform(0, total_score)
        cumulative = 0
        for insight_id, score in top_3:
            cumulative += score
            if r <= cumulative:
                return insight_id
        
        return top_3[0][0]
    
    def _days_since_used(self, insight_id: str) -> int:
        """Calculate days since insight was last used."""
        # Implementation would check database
        return 7  # Placeholder
```

### 3.3 Insight Selection Rules

| Rule | Description | Priority |
|------|-------------|----------|
| **No Repeat < 7 Days** | Same insight not used within 7 days | HIGH |
| **Market Match** | Insight matches market conditions | HIGH |
| **Persona Fit** | Insight appropriate for user persona | MEDIUM |
| **Crisis Override** | Crisis insights override all others | CRITICAL |
| **Celebration Trigger** | Milestones trigger celebration insights | MEDIUM |

---

## 4. Section Population

### 4.1 Template Structure

All Adelaide templates follow a consistent section structure:

```markdown
# Adelaide {EDITION_TYPE} â€” {DATE}

{GREETING}

## ðŸ“Š Market Snapshot
{MARKET_SNAPSHOT_TABLE}

## ðŸ‹ Whale Watch
{WHALE_SECTION}

## ðŸ“ˆ Your Strategies
{STRATEGY_TABLE}

## ðŸ’¡ Adelaide's Insight
{INSIGHT_BLOCK}

## âš ï¸ Estate Watch (if applicable)
{ESTATE_ALERTS}

---

{DISCLAIMER_BLOCK}

{FOOTER}
```

### 4.2 Section Populator Implementation

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import jinja2

@dataclass
class PopulatedSection:
    """A populated template section."""
    section_id: str
    content: str
    size_bytes: int
    priority: int  # For trimming (1 = never trim, 5 = trim first)

class SectionPopulator:
    """Populate template sections with data."""
    
    def __init__(self, template_dir: str):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
    
    def populate_all_sections(
        self,
        template_name: str,
        alert_data: dict,
        user_context: dict,
        locale: str
    ) -> Dict[str, PopulatedSection]:
        """Populate all sections for a template."""
        
        sections = {}
        
        # 1. Greeting
        sections['greeting'] = self._populate_greeting(
            alert_data, user_context, locale
        )
        
        # 2. Market Snapshot
        sections['market_snapshot'] = self._populate_market_snapshot(
            alert_data.get('market_data', {}), locale
        )
        
        # 3. Whale Watch
        sections['whale_section'] = self._populate_whale_section(
            alert_data.get('whale_data', {}), locale
        )
        
        # 4. Strategy Table
        sections['strategy_table'] = self._populate_strategy_table(
            alert_data.get('strategy_yields', {}),
            alert_data.get('strategy_vs_benchmark', {}),
            user_context.get('user_strategies', []),
            locale
        )
        
        # 5. Insight Block
        sections['insight_block'] = self._populate_insight(
            alert_data.get('selected_insight', ''),
            alert_data,
            locale
        )
        
        # 6. Estate Alerts (optional)
        if alert_data.get('estate_alerts'):
            sections['estate_alerts'] = self._populate_estate_alerts(
                alert_data['estate_alerts'], locale
            )
        
        # 7. Disclaimer (always present)
        sections['disclaimer'] = self._populate_disclaimer(
            user_context.get('jurisdiction', 'EU'), locale
        )
        
        # 8. Footer
        sections['footer'] = self._populate_footer(locale)
        
        return sections
    
    def _populate_greeting(
        self, 
        data: dict, 
        user: dict, 
        locale: str
    ) -> PopulatedSection:
        """Populate greeting section."""
        
        # Get greeting template based on locale
        greetings = {
            'en': "Good morning! Here's what happened while you slept.",
            'de': "Guten Morgen! Hier ist, was passiert ist, wÃ¤hrend Sie geschlafen haben.",
            'pt-br': "Bom dia! Aqui estÃ¡ o que aconteceu enquanto vocÃª dormia.",
            'es': "Â¡Buenos dÃ­as! Esto es lo que pasÃ³ mientras dormÃ­as.",
        }
        
        content = greetings.get(locale, greetings['en'])
        
        return PopulatedSection(
            section_id='greeting',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=1  # Never trim
        )
    
    def _populate_market_snapshot(
        self, 
        market_data: dict, 
        locale: str
    ) -> PopulatedSection:
        """Populate market snapshot table."""
        
        template = self.env.get_template(f'sections/market_snapshot_{locale}.md')
        
        content = template.render(
            btc_price=market_data.get('btc_price', 0),
            btc_change=market_data.get('btc_change_24h', 0),
            eth_price=market_data.get('eth_price', 0),
            eth_change=market_data.get('eth_change_24h', 0),
            sol_price=market_data.get('sol_price', 0),
            sol_change=market_data.get('sol_change_24h', 0),
            sp500_price=market_data.get('sp500_price', 0),
            sp500_change=market_data.get('sp500_change_24h', 0),
        )
        
        return PopulatedSection(
            section_id='market_snapshot',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=2
        )
    
    def _populate_whale_section(
        self, 
        whale_data: dict, 
        locale: str
    ) -> PopulatedSection:
        """Populate whale watch section."""
        
        # Skip if no whale activity
        if not whale_data or whale_data.get('net_flow', 0) == 0:
            content = self._get_no_whale_activity_message(locale)
        else:
            template = self.env.get_template(f'sections/whale_watch_{locale}.md')
            content = template.render(
                net_flow=whale_data.get('net_flow', 0),
                signal=whale_data.get('signal', 'neutral'),
                notable_movements=whale_data.get('movements', [])[:3],  # Top 3
            )
        
        return PopulatedSection(
            section_id='whale_section',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=3
        )
    
    def _populate_strategy_table(
        self,
        yields: dict,
        benchmarks: dict,
        user_strategies: List[int],
        locale: str
    ) -> PopulatedSection:
        """Populate strategy performance table."""
        
        template = self.env.get_template(f'sections/strategy_table_{locale}.md')
        
        # Build strategy rows
        rows = []
        for strategy_id in user_strategies:
            if strategy_id in yields:
                rows.append({
                    'id': strategy_id,
                    'name': self._get_strategy_name(strategy_id, locale),
                    'apy': yields[strategy_id],
                    'vs_benchmark': benchmarks.get(strategy_id, 0),
                })
        
        content = template.render(strategies=rows)
        
        return PopulatedSection(
            section_id='strategy_table',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=2
        )
    
    def _populate_insight(
        self,
        insight_id: str,
        alert_data: dict,
        locale: str
    ) -> PopulatedSection:
        """Populate insight block."""
        
        template = self.env.get_template(f'insights/{insight_id}_{locale}.md')
        
        content = template.render(
            market_data=alert_data.get('market_data', {}),
            whale_data=alert_data.get('whale_data', {}),
            risk_metrics=alert_data.get('risk_metrics', {}),
        )
        
        return PopulatedSection(
            section_id='insight_block',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=4  # Can be trimmed if over budget
        )
    
    def _populate_estate_alerts(
        self,
        alerts: List[dict],
        locale: str
    ) -> PopulatedSection:
        """Populate estate wallet alerts."""
        
        template = self.env.get_template(f'sections/estate_alerts_{locale}.md')
        
        content = template.render(alerts=alerts[:5])  # Max 5 alerts
        
        return PopulatedSection(
            section_id='estate_alerts',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=2  # Important - don't trim easily
        )
    
    def _populate_disclaimer(
        self,
        jurisdiction: str,
        locale: str
    ) -> PopulatedSection:
        """Populate jurisdiction-specific disclaimer."""
        
        # Disclaimers are pre-approved by CLO Board
        template = self.env.get_template(f'disclaimers/{jurisdiction}_{locale}.md')
        content = template.render()
        
        return PopulatedSection(
            section_id='disclaimer',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=1  # NEVER trim disclaimers
        )
    
    def _populate_footer(self, locale: str) -> PopulatedSection:
        """Populate footer."""
        
        template = self.env.get_template(f'sections/footer_{locale}.md')
        content = template.render(
            unsubscribe_url="{{UNSUBSCRIBE_URL}}",  # Placeholder for channel
            year=datetime.now().year,
        )
        
        return PopulatedSection(
            section_id='footer',
            content=content,
            size_bytes=len(content.encode('utf-8')),
            priority=1  # Never trim
        )
    
    def _get_no_whale_activity_message(self, locale: str) -> str:
        """Get message for no whale activity."""
        messages = {
            'en': "ðŸ‹ **Whale Watch**: No significant whale activity in the last 24 hours. Markets are calm.",
            'de': "ðŸ‹ **Wal-Beobachtung**: Keine signifikante Wal-AktivitÃ¤t in den letzten 24 Stunden.",
            'pt-br': "ðŸ‹ **ObservaÃ§Ã£o de Baleias**: Nenhuma atividade significativa nas Ãºltimas 24 horas.",
            'es': "ðŸ‹ **Vigilancia de Ballenas**: Sin actividad significativa en las Ãºltimas 24 horas.",
        }
        return messages.get(locale, messages['en'])
    
    def _get_strategy_name(self, strategy_id: int, locale: str) -> str:
        """Get localized strategy name."""
        # Would load from strategies.json with locale
        strategy_names = {
            1: {'en': 'Conservative USD', 'pt-br': 'USD Conservador'},
            2: {'en': 'Conservative EUR', 'pt-br': 'EUR Conservador'},
            # ... etc
        }
        return strategy_names.get(strategy_id, {}).get(locale, f'Strategy {strategy_id}')
```

---

## 5. Content Budget Enforcement

### 5.1 Budget Limits

| Edition | Max Size | Enforcement |
|---------|----------|-------------|
| Daily | 100KB (102,400 bytes) | Hard limit |
| Weekly | 250KB (256,000 bytes) | Hard limit |
| Monthly | 500KB (512,000 bytes) | Soft limit (warning) |
| Crisis | 50KB (51,200 bytes) | Hard limit |

### 5.2 Budget Enforcer Implementation

```python
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class BudgetResult:
    """Result of budget enforcement."""
    within_budget: bool
    original_size: int
    final_size: int
    trimmed_sections: List[str]
    warnings: List[str]

class ContentBudgetEnforcer:
    """Enforce content size limits."""
    
    LIMITS = {
        'daily': 102_400,      # 100KB
        'weekly': 256_000,     # 250KB
        'monthly': 512_000,    # 500KB (soft)
        'quarterly': 512_000,  # 500KB (soft)
        'crisis': 51_200,      # 50KB
    }
    
    # Sections that can NEVER be trimmed
    PROTECTED_SECTIONS = {'disclaimer', 'footer', 'greeting', 'crisis_message'}
    
    def enforce_budget(
        self,
        edition_type: str,
        sections: Dict[str, PopulatedSection]
    ) -> Tuple[Dict[str, PopulatedSection], BudgetResult]:
        """Enforce content budget, trimming if necessary."""
        
        limit = self.LIMITS.get(edition_type, self.LIMITS['daily'])
        original_size = sum(s.size_bytes for s in sections.values())
        
        result = BudgetResult(
            within_budget=True,
            original_size=original_size,
            final_size=original_size,
            trimmed_sections=[],
            warnings=[]
        )
        
        # Check if within budget
        if original_size <= limit:
            return sections, result
        
        # Need to trim
        result.within_budget = False
        result.warnings.append(
            f"Content exceeds budget: {original_size} > {limit} bytes"
        )
        
        # Sort sections by priority (highest priority = trim first)
        trimmable = [
            (name, section) 
            for name, section in sections.items()
            if name not in self.PROTECTED_SECTIONS
        ]
        trimmable.sort(key=lambda x: x[1].priority, reverse=True)
        
        # Trim sections until within budget
        current_size = original_size
        for name, section in trimmable:
            if current_size <= limit:
                break
            
            # Try to trim this section
            trimmed = self._trim_section(section, limit - current_size + section.size_bytes)
            
            if trimmed.size_bytes < section.size_bytes:
                savings = section.size_bytes - trimmed.size_bytes
                current_size -= savings
                sections[name] = trimmed
                result.trimmed_sections.append(name)
                result.warnings.append(
                    f"Trimmed {name}: saved {savings} bytes"
                )
        
        # If still over budget, remove lowest priority sections entirely
        for name, section in trimmable:
            if current_size <= limit:
                break
            
            if section.priority >= 4:  # Only remove priority 4+ sections
                current_size -= section.size_bytes
                del sections[name]
                result.trimmed_sections.append(f"{name} (removed)")
                result.warnings.append(f"Removed {name} entirely")
        
        result.final_size = current_size
        result.within_budget = current_size <= limit
        
        if not result.within_budget:
            result.warnings.append(
                f"CRITICAL: Still over budget after trimming: {current_size} > {limit}"
            )
        
        return sections, result
    
    def _trim_section(
        self, 
        section: PopulatedSection, 
        target_size: int
    ) -> PopulatedSection:
        """Trim a section to target size."""
        
        if section.size_bytes <= target_size:
            return section
        
        content = section.content
        
        # Strategy 1: Truncate with ellipsis
        if target_size > 100:
            # Find last complete sentence within limit
            truncated = content[:target_size - 20]  # Leave room for ellipsis
            last_period = truncated.rfind('.')
            if last_period > 0:
                truncated = truncated[:last_period + 1] + "\n\n*[Content trimmed for length]*"
            else:
                truncated = truncated + "..."
            
            return PopulatedSection(
                section_id=section.section_id,
                content=truncated,
                size_bytes=len(truncated.encode('utf-8')),
                priority=section.priority
            )
        
        # Strategy 2: Remove section entirely (return empty)
        return PopulatedSection(
            section_id=section.section_id,
            content="",
            size_bytes=0,
            priority=section.priority
        )
```

---

## 6. Content Assembler (Main Class)

### 6.1 Complete Implementation

```python
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

@dataclass
class AssembledContent:
    """Fully assembled Adelaide content."""
    edition_type: str
    template_used: str
    locale: str
    
    # Assembled content
    full_content: str
    sections: Dict[str, PopulatedSection]
    
    # Metadata
    generated_at: datetime
    insight_used: str
    size_bytes: int
    
    # Budget info
    budget_result: BudgetResult
    
    # Validation ready
    ready_for_gate4: bool

class ContentAssemblyEngine:
    """
    Main content assembly engine.
    
    Transforms Layer 4 alerts into formatted Adelaide content.
    """
    
    def __init__(self, config: dict):
        self.template_selector = TemplateSelector()
        self.insight_selector = InsightSelector()
        self.section_populator = SectionPopulator(config['template_dir'])
        self.budget_enforcer = ContentBudgetEnforcer()
        self.config = config
    
    def assemble(
        self,
        alert_data: dict,
        user_context: dict,
        edition_type: str = 'daily'
    ) -> AssembledContent:
        """
        Assemble complete Adelaide content.
        
        Args:
            alert_data: Alert object from Strategy Board (Layer 4)
            user_context: User information (persona, locale, jurisdiction)
            edition_type: 'daily', 'weekly', 'monthly', 'quarterly', 'crisis'
        
        Returns:
            AssembledContent ready for Gate 4 validation
        """
        
        locale = user_context.get('locale', 'en')
        
        # Step 1: Select template
        template_name = self.template_selector.select_template(
            edition_type=edition_type,
            data=MarketData(**alert_data.get('market_data', {})),
            crisis_level=alert_data.get('crisis_level')
        )
        
        # Step 2: Select insight
        recent_insights = self._get_recent_insights(user_context.get('user_id'))
        insight_id = self.insight_selector.select_insight(
            market_data=MarketData(**alert_data.get('market_data', {})),
            user_context=user_context,
            recent_insights=recent_insights
        )
        
        # Add insight to alert data for population
        alert_data['selected_insight'] = insight_id
        
        # Step 3: Populate sections
        sections = self.section_populator.populate_all_sections(
            template_name=template_name,
            alert_data=alert_data,
            user_context=user_context,
            locale=locale
        )
        
        # Step 4: Enforce content budget
        sections, budget_result = self.budget_enforcer.enforce_budget(
            edition_type=edition_type,
            sections=sections
        )
        
        # Step 5: Assemble final content
        full_content = self._assemble_sections(sections, template_name)
        
        return AssembledContent(
            edition_type=edition_type,
            template_used=template_name,
            locale=locale,
            full_content=full_content,
            sections=sections,
            generated_at=datetime.utcnow(),
            insight_used=insight_id,
            size_bytes=len(full_content.encode('utf-8')),
            budget_result=budget_result,
            ready_for_gate4=budget_result.within_budget
        )
    
    def _assemble_sections(
        self, 
        sections: Dict[str, PopulatedSection],
        template_name: str
    ) -> str:
        """Assemble sections into final content."""
        
        # Section order
        order = [
            'greeting',
            'market_snapshot',
            'whale_section',
            'strategy_table',
            'insight_block',
            'estate_alerts',
            'disclaimer',
            'footer',
        ]
        
        parts = []
        for section_id in order:
            if section_id in sections and sections[section_id].content:
                parts.append(sections[section_id].content)
        
        return "\n\n---\n\n".join(parts)
    
    def _get_recent_insights(self, user_id: str) -> List[str]:
        """Get recently used insights for user."""
        # Would query database
        return []  # Placeholder
```

---

## 7. Configuration

### 7.1 YAML Configuration

```yaml
# config/content_assembly.yaml

content_assembly:
  template_dir: "templates/adelaide"
  insight_history_days: 14
  
  # Template selection thresholds
  thresholds:
    significant_down: -5.0
    moderate_down: -2.0
    moderate_up: 2.0
    significant_up: 5.0
    high_vix: 25.0
    whale_significant: 100000000
  
  # Content budgets (bytes)
  budgets:
    daily: 102400
    weekly: 256000
    monthly: 512000
    quarterly: 512000
    crisis: 51200
  
  # Section priorities (1=never trim, 5=trim first)
  section_priorities:
    greeting: 1
    disclaimer: 1
    footer: 1
    crisis_message: 1
    market_snapshot: 2
    strategy_table: 2
    estate_alerts: 2
    whale_section: 3
    insight_block: 4
    educational_note: 5

  # Protected sections (never removed)
  protected_sections:
    - disclaimer
    - footer
    - greeting
    - crisis_message
```

---

## 8. Testing Requirements

### 8.1 Unit Tests

```python
# tests/test_content_assembly.py

class TestTemplateSelector:
    def test_calm_day_selection(self):
        """Test calm day template is selected for flat market."""
        selector = TemplateSelector()
        data = MarketData(btc_change_24h=0.5, ...)
        assert selector.select_daily_template(data) == DailyTemplate.CALM_DAY
    
    def test_down_day_selection(self):
        """Test down day template for negative market."""
        selector = TemplateSelector()
        data = MarketData(btc_change_24h=-6.0, ...)
        assert selector.select_daily_template(data) == DailyTemplate.DOWN_DAY
    
    def test_crisis_overrides_daily(self):
        """Test crisis template overrides daily selection."""
        selector = TemplateSelector()
        data = MarketData(btc_change_24h=0.5, ...)
        template = selector.select_template('daily', data, crisis_level=3)
        assert template == "crisis_level_3"

class TestInsightSelector:
    def test_no_repeat_within_7_days(self):
        """Test same insight not repeated within 7 days."""
        selector = InsightSelector()
        # ... implementation
    
    def test_market_match_priority(self):
        """Test market-matching insights get higher priority."""
        # ... implementation

class TestContentBudgetEnforcer:
    def test_within_budget_no_trim(self):
        """Test content within budget is not trimmed."""
        # ... implementation
    
    def test_over_budget_trims_low_priority(self):
        """Test over-budget content trims low priority sections first."""
        # ... implementation
    
    def test_protected_sections_never_trimmed(self):
        """Test protected sections are never trimmed."""
        # ... implementation
```

### 8.2 Integration Tests

| Test | Description | Frequency |
|------|-------------|-----------|
| Full assembly | End-to-end daily generation | Every deploy |
| Template coverage | All templates can be selected | Weekly |
| Insight rotation | Insights rotate properly | Weekly |
| Budget enforcement | All editions stay within budget | Every deploy |

---

## 9. Error Codes

| Code | Description | Handling |
|------|-------------|----------|
| CMO-ASM-001 | Template not found | Use fallback template |
| CMO-ASM-002 | Insight selection failed | Use generic insight |
| CMO-ASM-003 | Content budget exceeded | Trim per priority |
| CMO-ASM-004 | Section population failed | Use placeholder |
| CMO-ASM-005 | Market data missing | Skip market-dependent sections |

---

## 10. Implementation Checklist

- [ ] Template selection logic implemented
- [ ] All template files created (daily_calm, daily_down, daily_up, etc.)
- [ ] Insight selection algorithm working
- [ ] All 23 insight templates created
- [ ] Section populator functional
- [ ] All section templates created (4 locales)
- [ ] Content budget enforcement active
- [ ] Fallback handling implemented
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing

---

**Document End**

**Next:** CMO_02_PERSONA_SEGMENTATION_ENGINE.md
