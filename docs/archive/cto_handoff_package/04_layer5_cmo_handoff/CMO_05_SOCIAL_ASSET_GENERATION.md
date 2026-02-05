# CMO_05: Social Asset Generation
## Newsletter â†’ Social Media Transformation

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P2 (Post-Launch Enhancement)

---

## 1. Purpose

The Social Asset Generation system transforms each Adelaide newsletter into 8-10 platform-optimized social media posts, enabling consistent multi-platform presence with minimal manual effort.

### Output Targets

| Platform | Posts per Newsletter | Format |
|----------|---------------------|--------|
| Twitter/X | 3-4 | Short text + optional image |
| LinkedIn | 2 | Professional long-form |
| Instagram | 2 | Visual-first + caption |
| Threads | 2 | Conversational text |

---

## 2. Architecture

### 2.1 Transformation Flow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    SOCIAL ASSET GENERATION                                  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚  Adelaide Newsletter                                                        â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              CONTENT EXTRACTOR                                       â”‚   â”‚
â”‚  â”‚  Extract: Headlines, Key Stats, Insights, Quotes, Data Points       â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              PLATFORM ROUTER                                         â”‚   â”‚
â”‚  â”‚  Route content types to appropriate platforms                        â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚    â”Œâ”€â”€â”€â”€â”¼â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                                         â”‚
â”‚    â”‚    â”‚    â”‚        â”‚          â”‚                                         â”‚
â”‚    â–¼    â–¼    â–¼        â–¼          â–¼                                         â”‚
â”‚ Twitter LinkedIn Instagram Threads                                          â”‚
â”‚    â”‚    â”‚    â”‚        â”‚          â”‚                                         â”‚
â”‚    â–¼    â–¼    â–¼        â–¼          â–¼                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              PLATFORM FORMATTERS                                     â”‚   â”‚
â”‚  â”‚  Apply platform-specific formatting, hashtags, CTAs                  â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              VISUAL ASSET GENERATOR                                  â”‚   â”‚
â”‚  â”‚  Generate charts, stat cards, quote graphics                         â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              APPROVAL QUEUE                                          â”‚   â”‚
â”‚  â”‚  Human review before posting (required)                              â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 3. Content Extraction

### 3.1 Extractable Elements

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ContentType(Enum):
    HEADLINE = "headline"
    KEY_STAT = "key_stat"
    INSIGHT = "insight"
    WHALE_MOVEMENT = "whale_movement"
    STRATEGY_PERFORMANCE = "strategy_performance"
    MARKET_SUMMARY = "market_summary"
    QUOTE = "quote"  # Adelaide's grandmother wisdom
    EDUCATIONAL = "educational"

@dataclass
class ExtractedContent:
    """Content extracted from newsletter for social."""
    content_type: ContentType
    text: str
    data: Optional[dict]  # Numeric data if applicable
    visual_potential: bool  # Can be turned into graphic
    platform_fit: List[str]  # Which platforms this fits

class ContentExtractor:
    """Extract social-ready content from Adelaide newsletter."""
    
    def extract_all(self, newsletter: AdelaideContent) -> List[ExtractedContent]:
        """Extract all social-worthy content from newsletter."""
        extracted = []
        
        # 1. Extract headline
        extracted.append(self._extract_headline(newsletter))
        
        # 2. Extract key statistics
        extracted.extend(self._extract_key_stats(newsletter))
        
        # 3. Extract insight/wisdom
        extracted.append(self._extract_insight(newsletter))
        
        # 4. Extract whale movements (if notable)
        if newsletter.whale_section:
            extracted.extend(self._extract_whale_content(newsletter))
        
        # 5. Extract strategy highlights
        extracted.extend(self._extract_strategy_highlights(newsletter))
        
        # 6. Extract educational nuggets
        extracted.extend(self._extract_educational(newsletter))
        
        return extracted
    
    def _extract_headline(self, newsletter: AdelaideContent) -> ExtractedContent:
        """Extract main headline."""
        return ExtractedContent(
            content_type=ContentType.HEADLINE,
            text=newsletter.headline,
            data=None,
            visual_potential=False,
            platform_fit=['twitter', 'linkedin', 'threads']
        )
    
    def _extract_key_stats(self, newsletter: AdelaideContent) -> List[ExtractedContent]:
        """Extract key statistics."""
        stats = []
        
        market = newsletter.market_snapshot
        
        # BTC movement
        if abs(market.btc_change_24h) >= 2:
            stats.append(ExtractedContent(
                content_type=ContentType.KEY_STAT,
                text=f"BTC {'ðŸ“ˆ' if market.btc_change_24h > 0 else 'ðŸ“‰'} {market.btc_change_24h:+.1f}% in 24h",
                data={'asset': 'BTC', 'change': market.btc_change_24h},
                visual_potential=True,
                platform_fit=['twitter', 'instagram', 'threads']
            ))
        
        # Strategy performance
        top_strategy = max(newsletter.strategy_performance.items(), key=lambda x: x[1])
        stats.append(ExtractedContent(
            content_type=ContentType.STRATEGY_PERFORMANCE,
            text=f"Top performing strategy: {top_strategy[0]} at {top_strategy[1]:.1f}% APY",
            data={'strategy': top_strategy[0], 'apy': top_strategy[1]},
            visual_potential=True,
            platform_fit=['twitter', 'linkedin', 'instagram']
        ))
        
        return stats
    
    def _extract_insight(self, newsletter: AdelaideContent) -> ExtractedContent:
        """Extract Adelaide's insight/wisdom."""
        return ExtractedContent(
            content_type=ContentType.INSIGHT,
            text=newsletter.insight_block.core_message,
            data=None,
            visual_potential=True,  # Quote graphic
            platform_fit=['twitter', 'linkedin', 'instagram', 'threads']
        )
    
    def _extract_whale_content(self, newsletter: AdelaideContent) -> List[ExtractedContent]:
        """Extract whale movement content."""
        whale = newsletter.whale_section
        extracted = []
        
        if abs(whale.net_flow) >= 50_000_000:  # $50M+
            direction = "into" if whale.net_flow > 0 else "out of"
            extracted.append(ExtractedContent(
                content_type=ContentType.WHALE_MOVEMENT,
                text=f"ðŸ‹ ${abs(whale.net_flow)/1_000_000:.0f}M moved {direction} exchanges in 24h",
                data={'net_flow': whale.net_flow},
                visual_potential=True,
                platform_fit=['twitter', 'threads']
            ))
        
        return extracted
    
    def _extract_strategy_highlights(self, newsletter: AdelaideContent) -> List[ExtractedContent]:
        """Extract strategy performance highlights."""
        extracted = []
        
        # Find strategies beating benchmark
        for strategy_id, performance in newsletter.strategy_vs_benchmark.items():
            if performance > 0.5:  # Beating by 0.5%+
                extracted.append(ExtractedContent(
                    content_type=ContentType.STRATEGY_PERFORMANCE,
                    text=f"Strategy {strategy_id} outperforming benchmark by {performance:.1f}%",
                    data={'strategy': strategy_id, 'outperformance': performance},
                    visual_potential=True,
                    platform_fit=['linkedin', 'twitter']
                ))
        
        return extracted[:2]  # Max 2
    
    def _extract_educational(self, newsletter: AdelaideContent) -> List[ExtractedContent]:
        """Extract educational content."""
        if not newsletter.educational_note:
            return []
        
        return [ExtractedContent(
            content_type=ContentType.EDUCATIONAL,
            text=newsletter.educational_note,
            data=None,
            visual_potential=False,
            platform_fit=['linkedin', 'threads']
        )]
```

---

## 4. Platform Formatters

### 4.1 Twitter/X Formatter

```python
class TwitterFormatter:
    """Format content for Twitter/X."""
    
    MAX_LENGTH = 280
    HASHTAGS = ['#diBoaS', '#DeFi', '#Crypto', '#WhileYouSlept']
    
    def format(self, content: ExtractedContent, context: dict) -> dict:
        """Format content for Twitter."""
        
        text = content.text
        
        # Add relevant hashtags (max 3)
        hashtags = self._select_hashtags(content)
        hashtag_str = ' '.join(hashtags[:3])
        
        # Calculate available space
        available = self.MAX_LENGTH - len(hashtag_str) - 1
        
        # Truncate if needed
        if len(text) > available:
            text = text[:available-3] + '...'
        
        full_text = f"{text}\n\n{hashtag_str}"
        
        return {
            'platform': 'twitter',
            'text': full_text,
            'character_count': len(full_text),
            'media': self._get_media(content),
            'thread': self._should_thread(content),
        }
    
    def _select_hashtags(self, content: ExtractedContent) -> List[str]:
        """Select relevant hashtags."""
        hashtags = ['#diBoaS']
        
        if content.content_type == ContentType.WHALE_MOVEMENT:
            hashtags.extend(['#WhaleWatch', '#Crypto'])
        elif content.content_type == ContentType.KEY_STAT:
            hashtags.extend(['#Bitcoin', '#CryptoMarkets'])
        elif content.content_type == ContentType.INSIGHT:
            hashtags.extend(['#WhileYouSlept', '#DeFi'])
        
        return hashtags
    
    def _get_media(self, content: ExtractedContent) -> Optional[dict]:
        """Determine if media should be attached."""
        if content.visual_potential:
            return {
                'type': 'image',
                'generate': True,
                'template': self._get_visual_template(content)
            }
        return None
    
    def _get_visual_template(self, content: ExtractedContent) -> str:
        """Get visual template for content type."""
        templates = {
            ContentType.KEY_STAT: 'stat_card',
            ContentType.INSIGHT: 'quote_card',
            ContentType.WHALE_MOVEMENT: 'whale_alert_card',
            ContentType.STRATEGY_PERFORMANCE: 'performance_chart',
        }
        return templates.get(content.content_type, 'generic_card')
    
    def _should_thread(self, content: ExtractedContent) -> bool:
        """Determine if content should be a thread."""
        return len(content.text) > 500  # Long content = thread
```

### 4.2 LinkedIn Formatter

```python
class LinkedInFormatter:
    """Format content for LinkedIn."""
    
    MAX_LENGTH = 3000
    
    def format(self, content: ExtractedContent, context: dict) -> dict:
        """Format content for LinkedIn (professional tone)."""
        
        # LinkedIn needs more professional framing
        text = self._professionalize(content)
        
        # Add CTA
        cta = "\n\n---\nðŸ’¡ Want institutional-grade yields without the complexity? Learn more at diboas.com"
        
        full_text = text + cta
        
        return {
            'platform': 'linkedin',
            'text': full_text[:self.MAX_LENGTH],
            'character_count': len(full_text),
            'media': self._get_media(content),
        }
    
    def _professionalize(self, content: ExtractedContent) -> str:
        """Adjust tone for LinkedIn's professional audience."""
        text = content.text
        
        # Add professional framing based on content type
        if content.content_type == ContentType.KEY_STAT:
            text = f"ðŸ“Š Market Update\n\n{text}\n\nWhat this means for DeFi investors:"
        elif content.content_type == ContentType.INSIGHT:
            text = f"ðŸ’¡ Perspective from Adelaide\n\n\"{text}\"\n\nIn volatile markets, long-term thinking wins."
        elif content.content_type == ContentType.STRATEGY_PERFORMANCE:
            text = f"ðŸ“ˆ Performance Highlight\n\n{text}\n\nConsistent returns through systematic DeFi strategies."
        
        return text
    
    def _get_media(self, content: ExtractedContent) -> Optional[dict]:
        """LinkedIn prefers professional visuals."""
        if content.visual_potential:
            return {
                'type': 'image',
                'generate': True,
                'template': 'linkedin_professional_card',
                'style': 'clean_minimal'
            }
        return None
```

### 4.3 Instagram Formatter

```python
class InstagramFormatter:
    """Format content for Instagram."""
    
    MAX_CAPTION_LENGTH = 2200
    
    def format(self, content: ExtractedContent, context: dict) -> dict:
        """Format content for Instagram (visual-first)."""
        
        # Instagram requires visual content
        if not content.visual_potential:
            return None  # Skip non-visual content
        
        caption = self._create_caption(content)
        hashtags = self._get_hashtags(content)
        
        return {
            'platform': 'instagram',
            'caption': caption,
            'hashtags': hashtags,
            'media': {
                'type': 'image',
                'generate': True,
                'template': self._get_template(content),
                'style': 'instagram_bold',
                'aspect_ratio': '1:1',  # Square for feed
            },
            'carousel_option': self._should_carousel(content),
        }
    
    def _create_caption(self, content: ExtractedContent) -> str:
        """Create Instagram caption."""
        
        # Start with hook
        hooks = {
            ContentType.KEY_STAT: "The numbers don't lie ðŸ“Š",
            ContentType.INSIGHT: "Adelaide wisdom ðŸ’¡",
            ContentType.WHALE_MOVEMENT: "The whales are moving ðŸ‹",
            ContentType.STRATEGY_PERFORMANCE: "Performance update ðŸ“ˆ",
        }
        
        hook = hooks.get(content.content_type, "Market update")
        
        caption = f"{hook}\n\n{content.text}\n\n"
        caption += "ðŸ‘‡ What do you think? Drop a comment below.\n\n"
        caption += "Follow @diboas for daily market insights"
        
        return caption
    
    def _get_hashtags(self, content: ExtractedContent) -> List[str]:
        """Get Instagram hashtags (hidden in first comment)."""
        base = ['#diBoaS', '#DeFi', '#Crypto', '#PassiveIncome', '#CryptoInvesting']
        
        if content.content_type == ContentType.WHALE_MOVEMENT:
            base.extend(['#WhaleWatch', '#CryptoWhales', '#BitcoinWhales'])
        elif content.content_type == ContentType.STRATEGY_PERFORMANCE:
            base.extend(['#YieldFarming', '#CryptoYield', '#DeFiYield'])
        
        return base[:30]  # Instagram allows max 30
    
    def _get_template(self, content: ExtractedContent) -> str:
        """Get Instagram visual template."""
        return 'instagram_bold_stat'
    
    def _should_carousel(self, content: ExtractedContent) -> bool:
        """Determine if carousel format is better."""
        return content.content_type == ContentType.STRATEGY_PERFORMANCE
```

### 4.4 Threads Formatter

```python
class ThreadsFormatter:
    """Format content for Threads."""
    
    MAX_LENGTH = 500
    
    def format(self, content: ExtractedContent, context: dict) -> dict:
        """Format content for Threads (conversational)."""
        
        # Threads is conversational like Twitter but longer
        text = self._make_conversational(content)
        
        return {
            'platform': 'threads',
            'text': text[:self.MAX_LENGTH],
            'character_count': len(text),
            'media': self._get_media(content) if content.visual_potential else None,
        }
    
    def _make_conversational(self, content: ExtractedContent) -> str:
        """Make content conversational for Threads."""
        
        # Add conversational framing
        openers = [
            "Here's what caught my attention this morning:",
            "Interesting market move:",
            "Adelaide's take:",
            "Something to think about:",
        ]
        
        import random
        opener = random.choice(openers)
        
        return f"{opener}\n\n{content.text}"
    
    def _get_media(self, content: ExtractedContent) -> dict:
        """Threads media settings."""
        return {
            'type': 'image',
            'generate': True,
            'template': 'threads_minimal',
        }
```

---

## 5. Visual Asset Generator

### 5.1 Visual Templates

```python
from dataclasses import dataclass
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

@dataclass
class VisualTemplate:
    """Template for generating social visuals."""
    name: str
    size: Tuple[int, int]
    background_color: str
    text_color: str
    accent_color: str
    font_family: str
    logo_position: str

VISUAL_TEMPLATES = {
    'stat_card': VisualTemplate(
        name='stat_card',
        size=(1200, 675),  # Twitter optimal
        background_color='#0A1628',  # Dark blue
        text_color='#FFFFFF',
        accent_color='#00D4AA',  # diBoaS teal
        font_family='Inter',
        logo_position='bottom_right'
    ),
    'quote_card': VisualTemplate(
        name='quote_card',
        size=(1200, 675),
        background_color='#1A1A2E',
        text_color='#FFFFFF',
        accent_color='#FFD700',  # Gold for wisdom
        font_family='Playfair Display',
        logo_position='bottom_center'
    ),
    'whale_alert_card': VisualTemplate(
        name='whale_alert_card',
        size=(1200, 675),
        background_color='#0D47A1',  # Deep blue
        text_color='#FFFFFF',
        accent_color='#4FC3F7',  # Light blue
        font_family='Inter',
        logo_position='bottom_right'
    ),
    'instagram_bold_stat': VisualTemplate(
        name='instagram_bold_stat',
        size=(1080, 1080),  # Square
        background_color='#0A1628',
        text_color='#FFFFFF',
        accent_color='#00D4AA',
        font_family='Inter',
        logo_position='bottom_center'
    ),
    'linkedin_professional_card': VisualTemplate(
        name='linkedin_professional_card',
        size=(1200, 627),  # LinkedIn optimal
        background_color='#FFFFFF',
        text_color='#1A1A1A',
        accent_color='#0077B5',  # LinkedIn blue
        font_family='Inter',
        logo_position='bottom_right'
    ),
}

class VisualAssetGenerator:
    """Generate visual assets for social posts."""
    
    def __init__(self, assets_dir: str):
        self.assets_dir = assets_dir
        self.templates = VISUAL_TEMPLATES
    
    def generate(
        self, 
        content: ExtractedContent, 
        template_name: str
    ) -> str:
        """
        Generate visual asset and return file path.
        
        Returns path to generated image.
        """
        template = self.templates.get(template_name)
        if not template:
            template = self.templates['stat_card']  # Fallback
        
        # Create image
        img = Image.new('RGB', template.size, template.background_color)
        draw = ImageDraw.Draw(img)
        
        # Add content based on type
        if content.content_type == ContentType.KEY_STAT:
            self._draw_stat_card(draw, content, template)
        elif content.content_type == ContentType.INSIGHT:
            self._draw_quote_card(draw, content, template)
        elif content.content_type == ContentType.WHALE_MOVEMENT:
            self._draw_whale_card(draw, content, template)
        else:
            self._draw_generic_card(draw, content, template)
        
        # Add logo
        self._add_logo(img, template)
        
        # Save and return path
        filename = f"social_{content.content_type.value}_{hash(content.text)}.png"
        filepath = f"{self.assets_dir}/{filename}"
        img.save(filepath)
        
        return filepath
    
    def _draw_stat_card(
        self, 
        draw: ImageDraw, 
        content: ExtractedContent, 
        template: VisualTemplate
    ):
        """Draw a stat card visual."""
        # Large stat number
        if content.data:
            stat_value = content.data.get('change', content.data.get('apy', ''))
            if isinstance(stat_value, (int, float)):
                stat_text = f"{stat_value:+.1f}%"
                # Draw large stat
                font_large = ImageFont.truetype(f"{template.font_family}.ttf", 120)
                draw.text(
                    (template.size[0]//2, template.size[1]//3),
                    stat_text,
                    fill=template.accent_color,
                    font=font_large,
                    anchor='mm'
                )
        
        # Description below
        font_small = ImageFont.truetype(f"{template.font_family}.ttf", 36)
        draw.text(
            (template.size[0]//2, template.size[1]*2//3),
            content.text[:100],
            fill=template.text_color,
            font=font_small,
            anchor='mm'
        )
    
    def _draw_quote_card(
        self, 
        draw: ImageDraw, 
        content: ExtractedContent, 
        template: VisualTemplate
    ):
        """Draw a quote card visual."""
        # Large quotation mark
        font_quote = ImageFont.truetype(f"{template.font_family}.ttf", 200)
        draw.text(
            (100, 50),
            '"',
            fill=template.accent_color,
            font=font_quote
        )
        
        # Quote text
        font_text = ImageFont.truetype(f"{template.font_family}.ttf", 42)
        # Wrap text
        wrapped = self._wrap_text(content.text, 40)
        draw.multiline_text(
            (template.size[0]//2, template.size[1]//2),
            wrapped,
            fill=template.text_color,
            font=font_text,
            anchor='mm',
            align='center'
        )
        
        # Attribution
        font_attr = ImageFont.truetype(f"{template.font_family}.ttf", 28)
        draw.text(
            (template.size[0]//2, template.size[1] - 100),
            "â€” Adelaide, diBoaS",
            fill=template.accent_color,
            font=font_attr,
            anchor='mm'
        )
    
    def _draw_whale_card(
        self, 
        draw: ImageDraw, 
        content: ExtractedContent, 
        template: VisualTemplate
    ):
        """Draw whale alert card."""
        # Whale emoji (or icon)
        font_emoji = ImageFont.truetype("NotoColorEmoji.ttf", 100)
        draw.text(
            (template.size[0]//2, 100),
            "ðŸ‹",
            font=font_emoji,
            anchor='mm'
        )
        
        # Alert text
        font_text = ImageFont.truetype(f"{template.font_family}.ttf", 48)
        draw.text(
            (template.size[0]//2, template.size[1]//2),
            content.text,
            fill=template.text_color,
            font=font_text,
            anchor='mm'
        )
    
    def _draw_generic_card(
        self, 
        draw: ImageDraw, 
        content: ExtractedContent, 
        template: VisualTemplate
    ):
        """Draw generic content card."""
        font = ImageFont.truetype(f"{template.font_family}.ttf", 42)
        wrapped = self._wrap_text(content.text, 45)
        draw.multiline_text(
            (template.size[0]//2, template.size[1]//2),
            wrapped,
            fill=template.text_color,
            font=font,
            anchor='mm',
            align='center'
        )
    
    def _add_logo(self, img: Image, template: VisualTemplate):
        """Add diBoaS logo to image."""
        logo = Image.open(f"{self.assets_dir}/logo.png")
        logo = logo.resize((150, 50))
        
        if template.logo_position == 'bottom_right':
            pos = (template.size[0] - 170, template.size[1] - 70)
        elif template.logo_position == 'bottom_center':
            pos = (template.size[0]//2 - 75, template.size[1] - 70)
        else:
            pos = (20, template.size[1] - 70)
        
        img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)
    
    def _wrap_text(self, text: str, width: int) -> str:
        """Wrap text to specified width."""
        import textwrap
        return '\n'.join(textwrap.wrap(text, width))
```

---

## 6. Approval Workflow

### 6.1 Approval Queue

```python
from enum import Enum
from datetime import datetime

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    POSTED = "posted"

@dataclass
class SocialPost:
    """Social post awaiting approval."""
    post_id: str
    platform: str
    content: dict
    visual_path: Optional[str]
    generated_at: datetime
    status: ApprovalStatus
    scheduled_for: Optional[datetime]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]

class ApprovalQueue:
    """Manage social post approval workflow."""
    
    def __init__(self, db):
        self.db = db
    
    def add_to_queue(self, posts: List[SocialPost]):
        """Add generated posts to approval queue."""
        for post in posts:
            self.db.social_posts.insert(post)
        
        # Notify CMO lead
        self._notify_pending_approvals(len(posts))
    
    def approve(self, post_id: str, approver: str, schedule_time: datetime) -> bool:
        """Approve a post for publishing."""
        post = self.db.social_posts.get(post_id)
        if not post:
            return False
        
        post.status = ApprovalStatus.SCHEDULED
        post.approved_by = approver
        post.approved_at = datetime.utcnow()
        post.scheduled_for = schedule_time
        
        self.db.social_posts.update(post)
        return True
    
    def reject(self, post_id: str, reason: str) -> bool:
        """Reject a post."""
        post = self.db.social_posts.get(post_id)
        if not post:
            return False
        
        post.status = ApprovalStatus.REJECTED
        post.rejection_reason = reason
        
        self.db.social_posts.update(post)
        return True
    
    def get_pending(self) -> List[SocialPost]:
        """Get all pending posts."""
        return self.db.social_posts.find({'status': ApprovalStatus.PENDING})
    
    def _notify_pending_approvals(self, count: int):
        """Send notification about pending approvals."""
        # Slack notification
        slack_message = f"ðŸ“± {count} social posts ready for approval\n"
        slack_message += f"Review at: https://admin.diboas.com/social/queue"
        # Send to #social-content channel
```

---

## 7. Scheduling System

### 7.1 Optimal Posting Times

```python
OPTIMAL_POSTING_TIMES = {
    'twitter': {
        'weekday': ['08:00', '12:00', '17:00'],  # UTC
        'weekend': ['10:00', '14:00'],
    },
    'linkedin': {
        'weekday': ['07:30', '12:00'],  # Business hours
        'weekend': [],  # Don't post weekends
    },
    'instagram': {
        'weekday': ['11:00', '19:00'],
        'weekend': ['10:00', '18:00'],
    },
    'threads': {
        'weekday': ['08:00', '13:00', '18:00'],
        'weekend': ['11:00', '17:00'],
    },
}

class SocialScheduler:
    """Schedule social posts for optimal times."""
    
    def __init__(self):
        self.times = OPTIMAL_POSTING_TIMES
    
    def get_next_slot(self, platform: str, after: datetime) -> datetime:
        """Get next available posting slot for platform."""
        is_weekend = after.weekday() >= 5
        day_type = 'weekend' if is_weekend else 'weekday'
        
        slots = self.times.get(platform, {}).get(day_type, [])
        if not slots:
            # Fallback to next weekday
            return self._next_weekday(after)
        
        # Find next available slot
        for slot in slots:
            hour, minute = map(int, slot.split(':'))
            candidate = after.replace(hour=hour, minute=minute, second=0)
            if candidate > after:
                return candidate
        
        # Next day's first slot
        next_day = after + timedelta(days=1)
        return self.get_next_slot(platform, next_day.replace(hour=0, minute=0))
    
    def _next_weekday(self, dt: datetime) -> datetime:
        """Get next weekday."""
        days_ahead = 0 - dt.weekday()  # Monday
        if days_ahead <= 0:
            days_ahead += 7
        return dt + timedelta(days=days_ahead)
```

---

## 8. Configuration

```yaml
# config/social_generation.yaml

social_generation:
  enabled: true
  
  # Platforms
  platforms:
    twitter:
      enabled: true
      posts_per_newsletter: 4
      max_length: 280
      hashtags_enabled: true
      
    linkedin:
      enabled: true
      posts_per_newsletter: 2
      max_length: 3000
      professional_tone: true
      
    instagram:
      enabled: true
      posts_per_newsletter: 2
      requires_visual: true
      hashtags_in_comment: true
      
    threads:
      enabled: true
      posts_per_newsletter: 2
      max_length: 500
  
  # Visual generation
  visuals:
    assets_dir: "assets/social"
    logo_path: "assets/logo.png"
    default_template: "stat_card"
    
  # Approval
  approval:
    required: true
    auto_approve_types: []  # None auto-approved
    notification_channel: "#social-content"
    
  # Scheduling
  scheduling:
    timezone: "UTC"
    min_gap_minutes: 120  # 2 hours between posts
```

---

## 9. Implementation Checklist

- [ ] Content Extractor implemented
- [ ] Twitter Formatter working
- [ ] LinkedIn Formatter working
- [ ] Instagram Formatter working
- [ ] Threads Formatter working
- [ ] Visual Asset Generator functional
- [ ] All visual templates created
- [ ] Approval Queue implemented
- [ ] Scheduling system working
- [ ] Admin UI for approvals
- [ ] Platform API integrations (posting)

---

**Document End**

**Next:** CMO_06_RETENTION_AUTOMATION.md
