# Mine Detector OS -- Addendum B: Social Sentiment

> Social media sentiment analysis for early warning detection. Monitors Twitter/X, Reddit, StockTwits for unusual activity patterns.

**Version:** 2026-01-30-r9

**Cross-References:**
- Core OS: mine-detector-os.md (interface contract, Event Risk category, RiskCategory enum)
- Addendum E: mine-detector-addendum-e-maintenance-operations.md (API rate limits, data freshness)

---

## Overview

Social sentiment provides leading indicators of:

1. **Retail positioning changes** - Crowd behavior before price moves
2. **Information leakage** - Unusual chatter before news
3. **Manipulation attempts** - Coordinated pump/dump activity
4. **Sentiment extremes** - Contrarian indicators at peaks/troughs

This addendum also defines the **mapping from social sentiment to Event Risk**, ensuring social signals integrate properly into the Core OS scoring framework.

---

## Interface Contract

Implements the Core OS Social Sentiment interface:

```python
def compute_social_sentiment(ticker: str, 
                              time_window_hours: int = 24) -> Dict:
    """
    Compute social sentiment score for a ticker.
    
    Returns:
        {
            'score': float,                   # -100 to +100 (raw sentiment)
            'event_risk_contribution': float, # 0 to 100 (mapped to Event Risk)
            'confidence': str,                # HIGH, MEDIUM, LOW, VERY_LOW
            'volume': int,                    # Number of posts analyzed
            'sources': Dict,                  # Breakdown by platform
            'alerts': List[str]               # Anomaly alerts
        }
    """
```

---

## Imports and Dependencies

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
from functools import wraps
import time
import math

# Import from shared module (Core OS)
from mine_detector_shared import utc_now, to_utc, format_timestamp, RiskCategory
```

---

## Data Sources

```python
class Platform(Enum):
    """Supported social media platforms."""
    TWITTER = "twitter"
    REDDIT = "reddit"
    STOCKTWITS = "stocktwits"
    DISCORD = "discord"
    TELEGRAM = "telegram"


@dataclass
class SocialPost:
    """Normalized social media post."""
    platform: Platform
    post_id: str
    timestamp: datetime
    author_id: str
    content: str
    
    # Engagement metrics
    likes: int = 0
    replies: int = 0
    shares: int = 0
    
    # Author metrics
    author_followers: int = 0
    author_account_age_days: int = 0
    author_post_frequency: float = 0.0  # Posts per day
    
    # Computed fields
    sentiment_score: Optional[float] = None  # -1 to +1
    bot_probability: float = 0.0
    is_verified: bool = False


@dataclass
class PlatformConfig:
    """Configuration for each platform."""
    platform: Platform
    weight: float  # Relative importance in final score
    min_posts_for_signal: int
    max_age_hours: int
    api_rate_limit: int  # Requests per minute


PLATFORM_CONFIGS = {
    Platform.TWITTER: PlatformConfig(
        platform=Platform.TWITTER,
        weight=0.35,
        min_posts_for_signal=50,
        max_age_hours=24,
        api_rate_limit=300
    ),
    Platform.REDDIT: PlatformConfig(
        platform=Platform.REDDIT,
        weight=0.30,
        min_posts_for_signal=20,
        max_age_hours=48,
        api_rate_limit=60
    ),
    Platform.STOCKTWITS: PlatformConfig(
        platform=Platform.STOCKTWITS,
        weight=0.25,
        min_posts_for_signal=30,
        max_age_hours=24,
        api_rate_limit=200
    ),
    Platform.DISCORD: PlatformConfig(
        platform=Platform.DISCORD,
        weight=0.05,
        min_posts_for_signal=10,
        max_age_hours=12,
        api_rate_limit=50
    ),
    Platform.TELEGRAM: PlatformConfig(
        platform=Platform.TELEGRAM,
        weight=0.05,
        min_posts_for_signal=10,
        max_age_hours=12,
        api_rate_limit=30
    )
}
```

---

## Bot Detection

```python
class BotDetector:
    """
    Detect bot accounts to filter out manipulation.
    
    Uses multiple signals:
    1. Account age
    2. Posting frequency
    3. Content patterns (repetitive)
    4. Engagement ratios
    5. Timing patterns
    6. Coordinated behavior
    """
    
    BOT_SIGNALS = {
        'new_account': {'threshold_days': 30, 'weight': 0.15},
        'high_frequency': {'threshold_posts_per_day': 50, 'weight': 0.20},
        'low_engagement_ratio': {'threshold': 0.01, 'weight': 0.15},
        'repetitive_content': {'threshold_similarity': 0.8, 'weight': 0.20},
        'suspicious_timing': {'threshold_variance': 0.1, 'weight': 0.15},
        'coordinated_behavior': {'threshold_correlation': 0.9, 'weight': 0.15}
    }
    
    def __init__(self):
        self.known_bots: set = set()
        self.content_cache: Dict[str, List[str]] = {}
    
    def compute_bot_probability(self, post: SocialPost, 
                                 recent_posts: List[SocialPost] = None) -> float:
        """
        Compute probability that a post is from a bot.
        
        Returns:
            Float 0.0 to 1.0 (higher = more likely bot)
        """
        recent_posts = recent_posts or []
        signals = {}
        weights_used = 0.0
        
        # Signal 1: New account
        cfg = self.BOT_SIGNALS['new_account']
        if post.author_account_age_days < cfg['threshold_days']:
            signals['new_account'] = 1.0 - (post.author_account_age_days / cfg['threshold_days'])
        else:
            signals['new_account'] = max(0, 1.0 - post.author_account_age_days / 365)
        weights_used += cfg['weight']
        
        # Signal 2: High posting frequency
        cfg = self.BOT_SIGNALS['high_frequency']
        if post.author_post_frequency > cfg['threshold_posts_per_day']:
            signals['high_frequency'] = min(1.0, post.author_post_frequency / (cfg['threshold_posts_per_day'] * 2))
        else:
            signals['high_frequency'] = post.author_post_frequency / cfg['threshold_posts_per_day']
        weights_used += cfg['weight']
        
        # Signal 3: Low engagement ratio
        cfg = self.BOT_SIGNALS['low_engagement_ratio']
        if post.author_followers > 0:
            engagement = (post.likes + post.replies + post.shares) / post.author_followers
            if engagement < cfg['threshold']:
                signals['low_engagement_ratio'] = 1.0 - (engagement / cfg['threshold'])
            else:
                signals['low_engagement_ratio'] = 0.0
        else:
            signals['low_engagement_ratio'] = 0.5
        weights_used += cfg['weight']
        
        # Signal 4: Repetitive content (requires recent posts from same author)
        cfg = self.BOT_SIGNALS['repetitive_content']
        author_posts = [p for p in recent_posts if p.author_id == post.author_id]
        if author_posts:
            similarity = self._compute_max_similarity(post.content, 
                                                       [p.content for p in author_posts[-10:]])
            signals['repetitive_content'] = min(1.0, similarity / cfg['threshold_similarity'])
            weights_used += cfg['weight']
        
        # Signal 5: Suspicious timing (low variance in posting intervals)
        cfg = self.BOT_SIGNALS['suspicious_timing']
        if len(author_posts) >= 5:
            timing_cv = self._compute_timing_cv(author_posts)
            if timing_cv < cfg['threshold_variance']:
                signals['suspicious_timing'] = 1.0 - (timing_cv / cfg['threshold_variance'])
            else:
                signals['suspicious_timing'] = 0.0
            weights_used += cfg['weight']
        
        # Signal 6: Coordinated behavior (many accounts posting same content)
        cfg = self.BOT_SIGNALS['coordinated_behavior']
        if recent_posts:
            similar_posts = sum(1 for p in recent_posts 
                               if p.author_id != post.author_id 
                               and self._content_similarity(post.content, p.content) > 0.8)
            if similar_posts > 3:
                signals['coordinated_behavior'] = min(1.0, similar_posts / 10)
                weights_used += cfg['weight']
        
        # Compute weighted probability
        if weights_used == 0:
            return 0.0
        
        weighted_sum = sum(
            signals.get(name, 0) * config['weight']
            for name, config in self.BOT_SIGNALS.items()
            if name in signals
        )
        
        return round(weighted_sum / weights_used, 3)
    
    def _compute_max_similarity(self, content: str, other_contents: List[str]) -> float:
        """Compute maximum similarity to any other content."""
        if not other_contents:
            return 0.0
        return max(self._content_similarity(content, other) for other in other_contents)
    
    def _content_similarity(self, a: str, b: str) -> float:
        """Simple word overlap similarity."""
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        if not words_a or not words_b:
            return 0.0
        overlap = len(words_a & words_b)
        union = len(words_a | words_b)
        return overlap / union if union > 0 else 0.0
    
    def _compute_timing_cv(self, posts: List[SocialPost]) -> float:
        """Compute coefficient of variation of posting intervals."""
        if len(posts) < 3:
            return 1.0
        
        sorted_posts = sorted(posts, key=lambda p: p.timestamp)
        intervals = []
        for i in range(1, len(sorted_posts)):
            delta = (sorted_posts[i].timestamp - sorted_posts[i-1].timestamp).total_seconds()
            intervals.append(delta)
        
        if not intervals:
            return 1.0
        
        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        std = math.sqrt(variance)
        return min(1.0, std / mean)
    
    def filter_posts(self, posts: List[SocialPost], threshold: float = 0.7) -> List[SocialPost]:
        """Filter out likely bot posts."""
        filtered = []
        for post in posts:
            bot_prob = self.compute_bot_probability(post, posts)
            post.bot_probability = bot_prob
            if bot_prob < threshold:
                filtered.append(post)
        return filtered
```

---

## Sentiment Analysis

```python
class SentimentAnalyzer:
    """
    Analyze sentiment of social posts using keyword and pattern matching.
    """
    
    BULLISH_KEYWORDS = [
        'buy', 'long', 'bullish', 'moon', 'rocket', 'breakout', 'undervalued',
        'accumulate', 'strong', 'growth', 'beat', 'upgrade', 'buy the dip',
        'calls', 'bull', 'rip', 'pump', 'green', 'winner', 'gem'
    ]
    
    BEARISH_KEYWORDS = [
        'sell', 'short', 'bearish', 'crash', 'dump', 'overvalued', 'avoid',
        'weak', 'decline', 'miss', 'downgrade', 'red flag', 'warning',
        'puts', 'bear', 'fade', 'tank', 'red', 'loser', 'scam', 'fraud'
    ]
    
    INTENSIFIERS = ['very', 'extremely', 'super', 'absolutely', 'definitely']
    NEGATIONS = ['not', "don't", "doesn't", "won't", "never", "no"]
    
    def analyze(self, post: SocialPost) -> float:
        """
        Analyze sentiment of a post.
        
        Returns:
            Score from -1.0 (very bearish) to +1.0 (very bullish)
        """
        content_lower = post.content.lower()
        words = content_lower.split()
        
        # Check for negation context (simple approach)
        has_negation = any(neg in content_lower for neg in self.NEGATIONS)
        
        # Keyword scoring
        bullish_count = sum(1 for kw in self.BULLISH_KEYWORDS if kw in content_lower)
        bearish_count = sum(1 for kw in self.BEARISH_KEYWORDS if kw in content_lower)
        
        # Intensifier bonus
        intensifier_count = sum(1 for word in words if word in self.INTENSIFIERS)
        
        # Calculate base score
        total_keywords = bullish_count + bearish_count
        if total_keywords == 0:
            return 0.0
        
        base_score = (bullish_count - bearish_count) / total_keywords
        
        # Apply intensifier
        if intensifier_count > 0 and abs(base_score) > 0:
            base_score *= (1 + 0.1 * min(intensifier_count, 3))
        
        # Flip if negation detected (simple heuristic)
        if has_negation and total_keywords <= 2:
            base_score *= -0.5
        
        return max(-1.0, min(1.0, base_score))
    
    def analyze_batch(self, posts: List[SocialPost]) -> Dict:
        """Analyze a batch of posts and return aggregate metrics."""
        if not posts:
            return {
                'mean_sentiment': 0.0,
                'sentiment_std': 0.0,
                'bullish_count': 0,
                'bearish_count': 0,
                'neutral_count': 0,
                'total_posts': 0
            }
        
        sentiments = []
        for post in posts:
            score = self.analyze(post)
            post.sentiment_score = score
            sentiments.append(score)
        
        mean_sentiment = sum(sentiments) / len(sentiments)
        variance = sum((s - mean_sentiment) ** 2 for s in sentiments) / len(sentiments)
        std = math.sqrt(variance)
        
        bullish = sum(1 for s in sentiments if s > 0.2)
        bearish = sum(1 for s in sentiments if s < -0.2)
        neutral = len(sentiments) - bullish - bearish
        
        return {
            'mean_sentiment': round(mean_sentiment, 3),
            'sentiment_std': round(std, 3),
            'bullish_count': bullish,
            'bearish_count': bearish,
            'neutral_count': neutral,
            'total_posts': len(posts)
        }
```

---

## Confidence Calculation

```python
def calculate_confidence(volume: int, 
                          platforms_with_data: int,
                          bot_filtered_pct: float,
                          sentiment_std: float) -> str:
    """
    Calculate confidence level for sentiment score.
    
    Factors:
    1. Volume - More posts = higher confidence
    2. Platform diversity - Multiple platforms = higher confidence
    3. Bot filtering - High bot % = lower confidence
    4. Sentiment variance - High variance = lower confidence
    
    Returns:
        One of: HIGH, MEDIUM, LOW, VERY_LOW
    """
    score = 0
    
    # Volume scoring (0-30 points)
    if volume >= 200:
        score += 30
    elif volume >= 100:
        score += 20
    elif volume >= 50:
        score += 10
    elif volume >= 20:
        score += 5
    
    # Platform diversity (0-25 points)
    if platforms_with_data >= 4:
        score += 25
    elif platforms_with_data >= 3:
        score += 20
    elif platforms_with_data >= 2:
        score += 10
    elif platforms_with_data >= 1:
        score += 5
    
    # Bot filtering penalty (0-25 points, inverted)
    if bot_filtered_pct <= 10:
        score += 25
    elif bot_filtered_pct <= 25:
        score += 15
    elif bot_filtered_pct <= 50:
        score += 5
    
    # Sentiment consistency (0-20 points)
    if sentiment_std <= 0.2:
        score += 20
    elif sentiment_std <= 0.4:
        score += 12
    elif sentiment_std <= 0.6:
        score += 5
    
    # Convert score to confidence level (max 100)
    if score >= 70:
        return 'HIGH'
    elif score >= 45:
        return 'MEDIUM'
    elif score >= 25:
        return 'LOW'
    else:
        return 'VERY_LOW'
```

---

## Sentiment to Event Risk Mapping

This section defines how raw social sentiment maps to the Event Risk category in the Core OS:

```python
def map_sentiment_to_event_risk(sentiment_score: float,
                                 confidence: str,
                                 volume: int,
                                 volume_change_pct: float = 0.0) -> Dict:
    """
    Map social sentiment to Event Risk contribution.
    
    The mapping considers:
    1. Sentiment extremes (both positive and negative) indicate risk
    2. Volume spikes indicate something is happening
    3. Confidence level scales the contribution
    
    MAPPING LOGIC:
    - Extreme bullishness (>70) = elevated risk (crowded trade, pump risk)
    - Extreme bearishness (<-70) = elevated risk (information leakage, panic)
    - Volume spike (>200% normal) = elevated risk (unusual activity)
    - Neutral sentiment with normal volume = low risk
    
    Returns:
        {
            'event_risk_contribution': float,  # 0-100
            'risk_type': str,                   # 'bullish_extreme', 'bearish_extreme', etc.
            'explanation': str
        }
    """
    # Confidence scaling
    confidence_multipliers = {
        'HIGH': 1.0,
        'MEDIUM': 0.7,
        'LOW': 0.4,
        'VERY_LOW': 0.2
    }
    conf_mult = confidence_multipliers.get(confidence, 0.5)
    
    # Base contribution from sentiment extremes
    abs_sentiment = abs(sentiment_score)
    
    if abs_sentiment >= 80:
        base_contribution = 70
        risk_type = 'bullish_extreme' if sentiment_score > 0 else 'bearish_extreme'
    elif abs_sentiment >= 60:
        base_contribution = 50
        risk_type = 'elevated_bullish' if sentiment_score > 0 else 'elevated_bearish'
    elif abs_sentiment >= 40:
        base_contribution = 30
        risk_type = 'moderate_sentiment'
    else:
        base_contribution = 10
        risk_type = 'neutral'
    
    # Volume spike bonus
    volume_bonus = 0
    if volume_change_pct > 300:
        volume_bonus = 25
        risk_type = 'volume_spike_' + risk_type
    elif volume_change_pct > 200:
        volume_bonus = 15
    elif volume_change_pct > 100:
        volume_bonus = 5
    
    # Calculate final contribution
    raw_contribution = base_contribution + volume_bonus
    scaled_contribution = raw_contribution * conf_mult
    final_contribution = min(100, max(0, scaled_contribution))
    
    # Generate explanation
    explanations = {
        'bullish_extreme': 'Extreme bullish sentiment suggests crowded trade or pump activity',
        'bearish_extreme': 'Extreme bearish sentiment suggests information leakage or panic',
        'elevated_bullish': 'Elevated bullish sentiment indicates increasing crowd participation',
        'elevated_bearish': 'Elevated bearish sentiment indicates growing concern',
        'moderate_sentiment': 'Moderate sentiment levels, monitoring for changes',
        'neutral': 'Neutral sentiment, no significant social risk detected'
    }
    
    base_explanation = explanations.get(risk_type.replace('volume_spike_', ''), 'Unknown')
    if 'volume_spike' in risk_type:
        base_explanation = f'VOLUME SPIKE: {base_explanation}'
    
    return {
        'event_risk_contribution': round(final_contribution, 1),
        'risk_type': risk_type,
        'explanation': base_explanation,
        'confidence_applied': confidence,
        'confidence_multiplier': conf_mult
    }
```

---

## Error Handling & Retries

```python
class SocialAPIError(Exception):
    """Base exception for social API errors."""
    pass

class RateLimitError(SocialAPIError):
    """Rate limit exceeded."""
    pass

class AuthenticationError(SocialAPIError):
    """Authentication failed."""
    pass

class TemporaryError(SocialAPIError):
    """Temporary error - retry may succeed."""
    pass


def with_retry(max_attempts: int = 3, 
               base_delay: float = 1.0,
               exponential_backoff: bool = True):
    """Decorator for retry logic with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                
                except RateLimitError as e:
                    delay = base_delay * (4 ** attempt) if exponential_backoff else base_delay * 4
                    last_exception = e
                    
                except TemporaryError as e:
                    delay = base_delay * (2 ** attempt) if exponential_backoff else base_delay
                    last_exception = e
                    
                except AuthenticationError:
                    raise  # Don't retry auth errors
                
                except Exception as e:
                    delay = base_delay * (2 ** attempt)
                    last_exception = e
                
                if attempt < max_attempts - 1:
                    time.sleep(delay)
            
            raise last_exception or SocialAPIError("All retry attempts failed")
        
        return wrapper
    return decorator


class SocialDataFetcher:
    """Fetch social data with consistent error handling."""
    
    def __init__(self):
        self.api_clients: Dict[Platform, object] = {}
        self.historical_volumes: Dict[str, float] = {}  # ticker -> avg daily volume
    
    @with_retry(max_attempts=3, base_delay=1.0)
    def fetch_posts(self, platform: Platform, 
                    ticker: str,
                    hours: int = 24) -> List[SocialPost]:
        """
        Fetch posts for a ticker from a platform.
        
        In production, implement actual API calls here.
        """
        # Placeholder - would call actual APIs
        return []
    
    def fetch_all_platforms(self, ticker: str, 
                            hours: int = 24) -> Tuple[Dict[Platform, List[SocialPost]], Dict]:
        """
        Fetch from all platforms with graceful degradation.
        """
        results = {}
        errors = {}
        
        for platform in Platform:
            try:
                posts = self.fetch_posts(platform, ticker, hours)
                results[platform] = posts
            except Exception as e:
                errors[platform] = str(e)
                results[platform] = []
        
        return results, errors
    
    def get_volume_change_pct(self, ticker: str, current_volume: int) -> float:
        """Calculate volume change vs historical average."""
        avg_volume = self.historical_volumes.get(ticker, 0)
        if avg_volume <= 0:
            return 0.0
        return ((current_volume - avg_volume) / avg_volume) * 100
```

---

## Main Sentiment Function

```python
def compute_social_sentiment(ticker: str, 
                              time_window_hours: int = 24) -> Dict:
    """
    Compute social sentiment score for a ticker.
    
    Implements the Core OS interface contract.
    """
    fetcher = SocialDataFetcher()
    bot_detector = BotDetector()
    sentiment_analyzer = SentimentAnalyzer()
    
    # Fetch from all platforms
    platform_posts, fetch_errors = fetcher.fetch_all_platforms(ticker, time_window_hours)
    
    # Aggregate all posts
    all_posts = []
    for posts in platform_posts.values():
        all_posts.extend(posts)
    
    if not all_posts:
        return {
            'score': 0.0,
            'event_risk_contribution': 0.0,
            'confidence': 'VERY_LOW',
            'volume': 0,
            'sources': {},
            'alerts': ['No social data available'],
            'errors': fetch_errors
        }
    
    # Filter bots
    original_count = len(all_posts)
    filtered_posts = bot_detector.filter_posts(all_posts, threshold=0.7)
    bot_filtered_pct = ((original_count - len(filtered_posts)) / original_count) * 100 if original_count > 0 else 0
    
    # Analyze sentiment
    sentiment_result = sentiment_analyzer.analyze_batch(filtered_posts)
    
    # Calculate per-platform breakdown with weights
    sources = {}
    weighted_sentiment = 0.0
    total_weight = 0.0
    
    for platform in Platform:
        config = PLATFORM_CONFIGS[platform]
        platform_filtered = [p for p in filtered_posts if p.platform == platform]
        
        if len(platform_filtered) >= config.min_posts_for_signal:
            platform_sentiment = sentiment_analyzer.analyze_batch(platform_filtered)
            sources[platform.value] = {
                'count': len(platform_filtered),
                'sentiment': platform_sentiment['mean_sentiment'],
                'weight': config.weight
            }
            weighted_sentiment += platform_sentiment['mean_sentiment'] * config.weight
            total_weight += config.weight
    
    # Final weighted sentiment
    if total_weight > 0:
        final_sentiment = weighted_sentiment / total_weight
    else:
        final_sentiment = sentiment_result['mean_sentiment']
    
    # Calculate confidence
    platforms_with_data = len([s for s in sources.values() if s['count'] > 0])
    confidence = calculate_confidence(
        volume=len(filtered_posts),
        platforms_with_data=platforms_with_data,
        bot_filtered_pct=bot_filtered_pct,
        sentiment_std=sentiment_result['sentiment_std']
    )
    
    # Map to Event Risk
    volume_change = fetcher.get_volume_change_pct(ticker, len(filtered_posts))
    event_risk_mapping = map_sentiment_to_event_risk(
        sentiment_score=final_sentiment * 100,  # Convert to -100 to +100 scale
        confidence=confidence,
        volume=len(filtered_posts),
        volume_change_pct=volume_change
    )
    
    # Generate alerts
    alerts = []
    if bot_filtered_pct > 50:
        alerts.append(f'High bot activity detected ({bot_filtered_pct:.0f}% filtered)')
    if sentiment_result['sentiment_std'] > 0.6:
        alerts.append('Highly polarized sentiment')
    if volume_change > 200:
        alerts.append(f'Unusual volume spike (+{volume_change:.0f}% vs normal)')
    if abs(final_sentiment) > 0.7:
        direction = 'bullish' if final_sentiment > 0 else 'bearish'
        alerts.append(f'Extreme {direction} sentiment detected')
    
    # Convert sentiment to -100 to +100 scale
    score = final_sentiment * 100
    
    return {
        'score': round(score, 1),
        'event_risk_contribution': event_risk_mapping['event_risk_contribution'],
        'confidence': confidence,
        'volume': len(filtered_posts),
        'sources': sources,
        'alerts': alerts,
        'event_risk_details': event_risk_mapping,
        'metadata': {
            'original_post_count': original_count,
            'bot_filtered_pct': round(bot_filtered_pct, 1),
            'sentiment_std': sentiment_result['sentiment_std'],
            'volume_change_pct': round(volume_change, 1),
            'fetch_errors': fetch_errors
        }
    }
```

---

## API Scarcity Fallback Mode

When social APIs are unavailable (rate limits, cost, access restrictions), the system can fall back to alternative signals:

```python
class SocialScarcityFallback:
    """
    Fallback mode when social APIs are unavailable.
    
    Uses alternative signals:
    1. Options flow (unusual activity)
    2. News sentiment (via news APIs)
    3. Google Trends data
    """
    
    def __init__(self):
        self.fallback_sources = ['options_flow', 'news_sentiment', 'google_trends']
    
    def compute_fallback_sentiment(self, ticker: str) -> Dict:
        """
        Compute sentiment using fallback sources.
        Returns a lower-confidence result.
        """
        # Placeholder - would implement actual fallback logic
        return {
            'score': 0.0,
            'event_risk_contribution': 15.0,  # Base uncertainty penalty
            'confidence': 'VERY_LOW',
            'volume': 0,
            'sources': {},
            'alerts': ['Using fallback mode - primary social APIs unavailable'],
            'fallback_mode': True
        }
```

---

## Dashboard Output

```
================================================================================
                        SOCIAL SENTIMENT ANALYSIS
                        Ticker: XYZ | 2026-01-30 10:00 UTC
================================================================================

SENTIMENT SCORE: +42.5 / 100 [BULLISH]
EVENT RISK CONTRIBUTION: 21/100 (moderate_sentiment)
Confidence: MEDIUM

VOLUME: 847 posts analyzed (1,203 raw, 30% bot-filtered)
Volume Change: +85% vs 30-day average

PLATFORM BREAKDOWN
--------------------------------------------------------------------------------
Platform      Posts    Sentiment    Weight    Contribution
----------    -----    ---------    ------    ------------
Twitter       412      +0.48        0.35      +0.17
Reddit        156      +0.35        0.30      +0.11
StockTwits    245      +0.41        0.25      +0.10
Discord       24       +0.52        0.05      +0.03
Telegram      10       +0.38        0.05      +0.02

SENTIMENT DISTRIBUTION
--------------------------------------------------------------------------------
Bullish:     423 (50%)  █████████████████████░░░░░░░░░░░░░░░░░░░░
Neutral:     298 (35%)  ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░
Bearish:     126 (15%)  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

ALERTS
--------------------------------------------------------------------------------
[WARNING] High bot activity detected (30% filtered)
[INFO]    Sentiment consistency: moderate (std=0.42)

EVENT RISK MAPPING
--------------------------------------------------------------------------------
Type: elevated_bullish
Explanation: Elevated bullish sentiment indicates increasing crowd participation
Confidence Multiplier: 0.7

================================================================================
```

---

---

## Future Enhancements to be Evaluated

The following topics have been identified for potential future development:

- **Async/concurrency:** Implement asyncio-based parallel fetching for social media APIs. Current sequential fetching across 5 platforms creates latency bottlenecks. Use `asyncio.gather()` with proper rate limiting per platform.

---

*Addendum B - Mine Detector OS v2026-01-30-r9*
