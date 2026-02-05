# CMO_02: Persona Segmentation Engine
## User Classification & Content Adaptation Specification

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P0 (Launch-Critical)

---

## 1. Purpose

The Persona Segmentation Engine classifies users into personas and adapts content accordingly. diBoaS uses three primary personas representing different user archetypes.

### Responsibilities

| Responsibility | Description |
|----------------|-------------|
| User Classification | Classify users into Ana, Maria, or Felipe |
| Content Adaptation | Adjust content depth, tone, and complexity |
| Risk Language Calibration | Calibrate risk messaging per persona |
| Communication Frequency | Adjust contact frequency per persona |
| Strategy Recommendations | Surface appropriate strategies |

---

## 2. Persona Definitions

### 2.1 The Three Personas

| Persona | Archetype | Risk Tolerance | Deposit Range | Primary Goal |
|---------|-----------|----------------|---------------|--------------|
| **Ana** | Conservative Saver | Low | â‚¬50 - â‚¬1,000 | Preserve capital, beat bank |
| **Maria** | Balanced Investor | Medium | â‚¬1,000 - â‚¬10,000 | Grow wealth steadily |
| **Felipe** | Sophisticated Investor | High | â‚¬10,000+ | Maximize returns |

### 2.2 Detailed Persona Profiles

```python
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class PersonaType(Enum):
    ANA = "ana"
    MARIA = "maria"
    FELIPE = "felipe"

@dataclass
class PersonaProfile:
    """Complete persona profile definition."""
    persona_type: PersonaType
    
    # Demographics
    typical_age_range: tuple  # (min, max)
    financial_literacy: str   # "low", "medium", "high"
    
    # Investment Behavior
    risk_tolerance: str       # "low", "medium", "high"
    deposit_range: tuple      # (min_eur, max_eur)
    preferred_strategies: List[int]
    
    # Communication Preferences
    content_depth: str        # "simple", "moderate", "detailed"
    communication_style: str  # "reassuring", "balanced", "direct"
    emoji_usage: str          # "heavy", "moderate", "minimal"
    technical_terms: bool     # Whether to use DeFi jargon
    
    # Engagement Patterns
    check_frequency: str      # "daily", "weekly", "monthly"
    notification_tolerance: str  # "minimal", "moderate", "full"
    
    # Risk Language
    loss_framing: str         # How to discuss potential losses

PERSONA_PROFILES = {
    PersonaType.ANA: PersonaProfile(
        persona_type=PersonaType.ANA,
        typical_age_range=(35, 65),
        financial_literacy="low",
        risk_tolerance="low",
        deposit_range=(50, 1000),
        preferred_strategies=[1, 2, 3],  # Conservative strategies
        content_depth="simple",
        communication_style="reassuring",
        emoji_usage="heavy",
        technical_terms=False,
        check_frequency="weekly",
        notification_tolerance="minimal",
        loss_framing="protective"
    ),
    PersonaType.MARIA: PersonaProfile(
        persona_type=PersonaType.MARIA,
        typical_age_range=(28, 50),
        financial_literacy="medium",
        risk_tolerance="medium",
        deposit_range=(1000, 10000),
        preferred_strategies=[4, 5, 6, 7],  # Moderate strategies
        content_depth="moderate",
        communication_style="balanced",
        emoji_usage="moderate",
        technical_terms=False,  # Still avoid jargon
        check_frequency="weekly",
        notification_tolerance="moderate",
        loss_framing="educational"
    ),
    PersonaType.FELIPE: PersonaProfile(
        persona_type=PersonaType.FELIPE,
        typical_age_range=(25, 45),
        financial_literacy="high",
        risk_tolerance="high",
        deposit_range=(10000, float('inf')),
        preferred_strategies=[8, 9, 10],  # Aggressive strategies
        content_depth="detailed",
        communication_style="direct",
        emoji_usage="minimal",
        technical_terms=True,  # Can use DeFi terms
        check_frequency="daily",
        notification_tolerance="full",
        loss_framing="analytical"
    ),
}
```

---

## 3. User Classification

### 3.1 Classification Signals

Users are classified based on multiple signals:

| Signal | Weight | Source |
|--------|--------|--------|
| **Initial deposit size** | 30% | First deposit amount |
| **Strategy selections** | 25% | Which strategies chosen |
| **Questionnaire answers** | 20% | Onboarding quiz |
| **Engagement behavior** | 15% | App usage patterns |
| **Content interactions** | 10% | Adelaide open/click rates |

### 3.2 Classification Engine

```python
from typing import Optional, Dict, Tuple

class PersonaClassifier:
    """Classify users into personas based on signals."""
    
    # Strategy to persona mapping
    STRATEGY_PERSONA_MAP = {
        1: PersonaType.ANA,    # Conservative USD
        2: PersonaType.ANA,    # Conservative EUR
        3: PersonaType.ANA,    # Conservative BRL
        4: PersonaType.MARIA,  # Moderate USD
        5: PersonaType.MARIA,  # Moderate EUR
        6: PersonaType.MARIA,  # Moderate BRL
        7: PersonaType.MARIA,  # Balanced Multi
        8: PersonaType.FELIPE, # Aggressive USD
        9: PersonaType.FELIPE, # Aggressive Multi
        10: PersonaType.FELIPE, # Maximum Yield
    }
    
    # Deposit thresholds (EUR)
    DEPOSIT_THRESHOLDS = {
        'ana_max': 1000,
        'maria_max': 10000,
        # Above maria_max = Felipe
    }
    
    def classify(self, user_data: dict) -> Tuple[PersonaType, float]:
        """
        Classify user into persona.
        
        Returns:
            Tuple of (PersonaType, confidence_score)
        """
        scores = {
            PersonaType.ANA: 0.0,
            PersonaType.MARIA: 0.0,
            PersonaType.FELIPE: 0.0,
        }
        
        # Signal 1: Deposit size (30%)
        deposit_score = self._score_deposit(user_data.get('total_deposits', 0))
        for persona, score in deposit_score.items():
            scores[persona] += score * 0.30
        
        # Signal 2: Strategy selections (25%)
        strategy_score = self._score_strategies(user_data.get('strategies', []))
        for persona, score in strategy_score.items():
            scores[persona] += score * 0.25
        
        # Signal 3: Questionnaire (20%)
        quiz_score = self._score_questionnaire(user_data.get('quiz_answers', {}))
        for persona, score in quiz_score.items():
            scores[persona] += score * 0.20
        
        # Signal 4: Engagement behavior (15%)
        engagement_score = self._score_engagement(user_data.get('engagement', {}))
        for persona, score in engagement_score.items():
            scores[persona] += score * 0.15
        
        # Signal 5: Content interactions (10%)
        content_score = self._score_content(user_data.get('content_interactions', {}))
        for persona, score in content_score.items():
            scores[persona] += score * 0.10
        
        # Determine winner
        best_persona = max(scores, key=scores.get)
        confidence = scores[best_persona]
        
        return best_persona, confidence
    
    def _score_deposit(self, amount: float) -> Dict[PersonaType, float]:
        """Score based on deposit amount."""
        if amount <= self.DEPOSIT_THRESHOLDS['ana_max']:
            return {PersonaType.ANA: 1.0, PersonaType.MARIA: 0.3, PersonaType.FELIPE: 0.0}
        elif amount <= self.DEPOSIT_THRESHOLDS['maria_max']:
            return {PersonaType.ANA: 0.1, PersonaType.MARIA: 1.0, PersonaType.FELIPE: 0.3}
        else:
            return {PersonaType.ANA: 0.0, PersonaType.MARIA: 0.3, PersonaType.FELIPE: 1.0}
    
    def _score_strategies(self, strategies: List[int]) -> Dict[PersonaType, float]:
        """Score based on strategy selections."""
        if not strategies:
            return {PersonaType.ANA: 0.33, PersonaType.MARIA: 0.34, PersonaType.FELIPE: 0.33}
        
        persona_counts = {p: 0 for p in PersonaType}
        for strategy_id in strategies:
            mapped = self.STRATEGY_PERSONA_MAP.get(strategy_id, PersonaType.MARIA)
            persona_counts[mapped] += 1
        
        total = sum(persona_counts.values())
        return {p: count/total for p, count in persona_counts.items()}
    
    def _score_questionnaire(self, answers: dict) -> Dict[PersonaType, float]:
        """Score based on onboarding questionnaire."""
        scores = {p: 0.33 for p in PersonaType}  # Default equal
        
        # Risk tolerance question
        risk = answers.get('risk_tolerance')
        if risk == 'low':
            scores[PersonaType.ANA] += 0.4
        elif risk == 'medium':
            scores[PersonaType.MARIA] += 0.4
        elif risk == 'high':
            scores[PersonaType.FELIPE] += 0.4
        
        # Investment horizon question
        horizon = answers.get('investment_horizon')
        if horizon == 'short':  # < 1 year
            scores[PersonaType.ANA] += 0.2
        elif horizon == 'medium':  # 1-5 years
            scores[PersonaType.MARIA] += 0.2
        elif horizon == 'long':  # > 5 years
            scores[PersonaType.FELIPE] += 0.2
        
        # Financial literacy question
        literacy = answers.get('financial_literacy')
        if literacy == 'beginner':
            scores[PersonaType.ANA] += 0.2
        elif literacy == 'intermediate':
            scores[PersonaType.MARIA] += 0.2
        elif literacy == 'advanced':
            scores[PersonaType.FELIPE] += 0.2
        
        # Normalize
        total = sum(scores.values())
        return {p: s/total for p, s in scores.items()}
    
    def _score_engagement(self, engagement: dict) -> Dict[PersonaType, float]:
        """Score based on app engagement patterns."""
        scores = {p: 0.33 for p in PersonaType}
        
        # Check frequency
        daily_opens = engagement.get('daily_opens_avg', 0)
        if daily_opens >= 3:  # Power user
            scores[PersonaType.FELIPE] += 0.4
        elif daily_opens >= 1:
            scores[PersonaType.MARIA] += 0.3
        else:
            scores[PersonaType.ANA] += 0.3
        
        # Feature usage
        advanced_features = engagement.get('advanced_features_used', 0)
        if advanced_features >= 5:
            scores[PersonaType.FELIPE] += 0.3
        elif advanced_features >= 2:
            scores[PersonaType.MARIA] += 0.2
        
        # Normalize
        total = sum(scores.values())
        return {p: s/total for p, s in scores.items()}
    
    def _score_content(self, interactions: dict) -> Dict[PersonaType, float]:
        """Score based on content interactions."""
        scores = {p: 0.33 for p in PersonaType}
        
        # Which content types they engage with
        technical_clicks = interactions.get('technical_content_clicks', 0)
        educational_clicks = interactions.get('educational_content_clicks', 0)
        
        if technical_clicks > educational_clicks:
            scores[PersonaType.FELIPE] += 0.4
        elif educational_clicks > technical_clicks:
            scores[PersonaType.ANA] += 0.3
        
        # Normalize
        total = sum(scores.values())
        return {p: s/total for p, s in scores.items()}
```

### 3.3 Classification Rules

| Rule | Description | Override? |
|------|-------------|-----------|
| **New User Default** | Default to Maria until signals accumulate | Yes |
| **Explicit Selection** | User can manually select persona | Yes |
| **Minimum Signals** | Need 2+ signals for confident classification | No |
| **Reclassification** | Re-evaluate monthly or on major deposit | Yes |

---

## 4. Content Adaptation

### 4.1 Adaptation Dimensions

Content is adapted across multiple dimensions per persona:

```python
@dataclass
class ContentAdaptation:
    """Content adaptation rules for a persona."""
    
    # Text complexity
    max_sentence_length: int
    max_paragraph_length: int
    use_technical_terms: bool
    explanation_depth: str  # "brief", "moderate", "detailed"
    
    # Tone
    formality: str  # "casual", "balanced", "formal"
    encouragement_level: str  # "high", "medium", "low"
    directness: str  # "gentle", "balanced", "direct"
    
    # Visual elements
    emoji_frequency: str  # "heavy", "moderate", "minimal"
    chart_complexity: str  # "simple", "moderate", "detailed"
    
    # Risk communication
    loss_language: str  # How to describe potential losses
    upside_language: str  # How to describe gains
    
    # Call to action
    cta_urgency: str  # "soft", "moderate", "direct"

CONTENT_ADAPTATIONS = {
    PersonaType.ANA: ContentAdaptation(
        max_sentence_length=15,
        max_paragraph_length=3,
        use_technical_terms=False,
        explanation_depth="brief",
        formality="casual",
        encouragement_level="high",
        directness="gentle",
        emoji_frequency="heavy",
        chart_complexity="simple",
        loss_language="Your money might go down temporarily, like the weather changing.",
        upside_language="Your money is working for you, slowly but surely.",
        cta_urgency="soft"
    ),
    PersonaType.MARIA: ContentAdaptation(
        max_sentence_length=20,
        max_paragraph_length=4,
        use_technical_terms=False,
        explanation_depth="moderate",
        formality="balanced",
        encouragement_level="medium",
        directness="balanced",
        emoji_frequency="moderate",
        chart_complexity="moderate",
        loss_language="Markets can be volatile; your portfolio may decrease in value.",
        upside_language="Your investments are performing well against benchmarks.",
        cta_urgency="moderate"
    ),
    PersonaType.FELIPE: ContentAdaptation(
        max_sentence_length=25,
        max_paragraph_length=5,
        use_technical_terms=True,
        explanation_depth="detailed",
        formality="formal",
        encouragement_level="low",
        directness="direct",
        emoji_frequency="minimal",
        chart_complexity="detailed",
        loss_language="Current drawdown: -X%. VaR 95: Y%. Max historical: Z%.",
        upside_language="Strategy outperforming benchmark by X bps. Sharpe: Y.",
        cta_urgency="direct"
    ),
}
```

### 4.2 Content Adapter Implementation

```python
class ContentAdapter:
    """Adapt content for specific personas."""
    
    def __init__(self):
        self.adaptations = CONTENT_ADAPTATIONS
    
    def adapt(self, content: str, persona: PersonaType) -> str:
        """
        Adapt content for persona.
        
        This is the main entry point for content adaptation.
        """
        adaptation = self.adaptations[persona]
        
        # Step 1: Simplify/complexify language
        content = self._adapt_complexity(content, adaptation)
        
        # Step 2: Adjust tone
        content = self._adapt_tone(content, adaptation)
        
        # Step 3: Handle technical terms
        content = self._adapt_technical_terms(content, adaptation)
        
        # Step 4: Adjust emoji usage
        content = self._adapt_emojis(content, adaptation)
        
        return content
    
    def _adapt_complexity(self, content: str, adaptation: ContentAdaptation) -> str:
        """Adapt text complexity."""
        
        # Split into sentences
        sentences = content.split('. ')
        adapted_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            
            # If sentence too long for persona, split it
            if len(words) > adaptation.max_sentence_length:
                # Find natural break point
                midpoint = len(words) // 2
                adapted_sentences.append(' '.join(words[:midpoint]) + '.')
                adapted_sentences.append(' '.join(words[midpoint:]))
            else:
                adapted_sentences.append(sentence)
        
        return '. '.join(adapted_sentences)
    
    def _adapt_tone(self, content: str, adaptation: ContentAdaptation) -> str:
        """Adapt tone based on persona."""
        
        # Tone word replacements
        if adaptation.formality == "casual":
            replacements = {
                "However": "But",
                "Therefore": "So",
                "Additionally": "Also",
                "Furthermore": "Plus",
                "Nevertheless": "Still",
                "portfolio": "your money",
                "investment": "savings",
            }
        elif adaptation.formality == "formal":
            replacements = {
                "But": "However",
                "So": "Therefore",
                "Also": "Additionally",
                "Plus": "Furthermore",
                "your money": "your portfolio",
            }
        else:
            replacements = {}
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def _adapt_technical_terms(
        self, 
        content: str, 
        adaptation: ContentAdaptation
    ) -> str:
        """Handle technical terms based on persona."""
        
        if adaptation.use_technical_terms:
            return content  # Keep technical terms
        
        # Replace technical terms with plain language
        replacements = {
            "APY": "yearly return",
            "TVL": "total money in the protocol",
            "liquidity": "available funds",
            "yield": "return",
            "protocol": "platform",
            "DeFi": "crypto savings",
            "smart contract": "automated system",
            "staking": "earning rewards",
            "impermanent loss": "temporary value changes",
            "slippage": "price difference",
            "gas fees": "transaction costs",
            "wallet": "account",
            "on-chain": "on the blockchain",
            "off-chain": "outside the blockchain",
            "VaR": "potential loss",
            "Sharpe ratio": "risk-adjusted return",
            "drawdown": "decline from peak",
            "volatility": "price swings",
            "correlation": "how things move together",
            "rebalancing": "adjusting your mix",
        }
        
        for term, plain in replacements.items():
            # Case-insensitive replacement
            content = content.replace(term, plain)
            content = content.replace(term.lower(), plain)
        
        return content
    
    def _adapt_emojis(self, content: str, adaptation: ContentAdaptation) -> str:
        """Adapt emoji usage."""
        
        # Emoji mappings for different contexts
        EMOJI_CONTEXTS = {
            'positive': ['ðŸ“ˆ', 'âœ…', 'ðŸŽ‰', 'ðŸ’ª', 'ðŸŒŸ'],
            'negative': ['ðŸ“‰', 'âš ï¸', 'ðŸ˜Ÿ', 'ðŸ”»'],
            'neutral': ['ðŸ“Š', 'ðŸ“‹', 'ðŸ”', 'ðŸ’¡'],
            'money': ['ðŸ’°', 'ðŸ’µ', 'ðŸ¦', 'ðŸ’Ž'],
        }
        
        if adaptation.emoji_frequency == "heavy":
            # Ensure emojis are present, add if missing
            if not any(emoji in content for emojis in EMOJI_CONTEXTS.values() for emoji in emojis):
                # Add contextual emoji based on content
                if "up" in content.lower() or "positive" in content.lower():
                    content = "ðŸ“ˆ " + content
                elif "down" in content.lower() or "negative" in content.lower():
                    content = "ðŸ“‰ " + content
                else:
                    content = "ðŸ’¡ " + content
        
        elif adaptation.emoji_frequency == "minimal":
            # Remove most emojis, keep only essential ones
            import re
            # Keep only warning emojis for important alerts
            essential = ['âš ï¸', 'ðŸš¨', 'âŒ', 'âœ…']
            for emojis in EMOJI_CONTEXTS.values():
                for emoji in emojis:
                    if emoji not in essential:
                        content = content.replace(emoji, '')
            
            # Clean up extra spaces
            content = re.sub(r'\s+', ' ', content).strip()
        
        return content
```

---

## 5. Risk Language Calibration

### 5.1 Loss Framing by Persona

```python
class RiskLanguageCalibrator:
    """Calibrate risk language for different personas."""
    
    # Loss scenario templates by persona
    LOSS_TEMPLATES = {
        PersonaType.ANA: {
            'minor_loss': "Your savings dipped a little today â€” like prices going up and down at the store. Nothing to worry about.",
            'moderate_loss': "The market had a rough day, and your balance went down. This happens sometimes. Adelaide is watching.",
            'significant_loss': "There's been a bigger drop today. Your grandmother would say: 'Don't make decisions when you're worried.' Let's talk about your options.",
            'exit_option': "If you need your money, you can always take it out. There's no shame in that. Your life comes first.",
        },
        PersonaType.MARIA: {
            'minor_loss': "Markets are down slightly today. Your portfolio decreased by {loss_pct}%. This is within normal fluctuation.",
            'moderate_loss': "Today saw a notable market correction. Your portfolio is down {loss_pct}%. Historical data shows similar periods recovered within {recovery_time}.",
            'significant_loss': "Significant market downturn: {loss_pct}% decrease. Review your risk settings if this level of volatility is uncomfortable.",
            'exit_option': "You can adjust your strategy or withdraw at any time. Consider your time horizon before making changes.",
        },
        PersonaType.FELIPE: {
            'minor_loss': "Daily return: {loss_pct}%. Within 1 standard deviation. No action required.",
            'moderate_loss': "Drawdown: {loss_pct}%. VaR 95 breach: No. Current Sharpe: {sharpe}. Historical recovery: {recovery_time}.",
            'significant_loss': "Significant drawdown: {loss_pct}%. VaR 99 breach: {var_breach}. Strategy {strategy_id} most affected. Correlation spike detected.",
            'exit_option': "Exit liquidity available. Estimated slippage at current volume: {slippage}%. Consider rebalancing or partial exit.",
        },
    }
    
    def get_loss_message(
        self,
        persona: PersonaType,
        loss_pct: float,
        context: dict
    ) -> str:
        """Get appropriate loss message for persona."""
        
        templates = self.LOSS_TEMPLATES[persona]
        
        # Determine severity
        if abs(loss_pct) < 2:
            template_key = 'minor_loss'
        elif abs(loss_pct) < 10:
            template_key = 'moderate_loss'
        else:
            template_key = 'significant_loss'
        
        template = templates[template_key]
        
        # Fill in variables
        return template.format(
            loss_pct=f"{loss_pct:.1f}",
            recovery_time=context.get('recovery_time', '3-6 months'),
            sharpe=context.get('sharpe', 'N/A'),
            var_breach=context.get('var_breach', 'No'),
            strategy_id=context.get('most_affected_strategy', 'N/A'),
            slippage=context.get('slippage', '0.1'),
        )
```

### 5.2 Gain Framing by Persona

```python
GAIN_TEMPLATES = {
    PersonaType.ANA: {
        'minor_gain': "Your money grew a little today! ðŸŒ± Every bit counts.",
        'moderate_gain': "Good news! Your savings are up. Adelaide is happy for you! ðŸŽ‰",
        'significant_gain': "Wonderful! Your patience is paying off. But remember, markets go up and down. Enjoy this moment.",
        'milestone': "ðŸŽŠ Congratulations! You've earned your first {milestone}. Your grandmother would be proud.",
    },
    PersonaType.MARIA: {
        'minor_gain': "Positive day: your portfolio gained {gain_pct}%.",
        'moderate_gain': "Strong performance today. Portfolio up {gain_pct}%, outperforming {benchmark} by {outperform}%.",
        'significant_gain': "Excellent returns: {gain_pct}%. YTD performance: {ytd_pct}%. Consider if rebalancing is appropriate.",
        'milestone': "Milestone reached: {milestone}. You've been invested for {duration}. Well done.",
    },
    PersonaType.FELIPE: {
        'minor_gain': "Daily: +{gain_pct}%. MTD: {mtd_pct}%. Alpha vs benchmark: {alpha} bps.",
        'moderate_gain': "Return: +{gain_pct}%. Sharpe: {sharpe}. Strategy {top_strategy} leading at +{top_return}%.",
        'significant_gain': "Exceptional return: +{gain_pct}%. Consider taking partial profits. Current risk/reward: {risk_reward}.",
        'milestone': "Performance milestone: {milestone}. Compound return since inception: {compound_return}%.",
    },
}
```

---

## 6. Communication Frequency

### 6.1 Frequency Rules by Persona

```python
NOTIFICATION_RULES = {
    PersonaType.ANA: {
        'daily_adelaide': True,  # Opt-in
        'weekly_adelaide': True,  # Default
        'monthly_adelaide': True,
        'crisis_alerts': True,  # Always
        'milestone_alerts': True,
        'promotional': False,  # Never
        'max_per_week': 3,
    },
    PersonaType.MARIA: {
        'daily_adelaide': True,  # Default
        'weekly_adelaide': True,
        'monthly_adelaide': True,
        'crisis_alerts': True,
        'milestone_alerts': True,
        'promotional': True,  # Occasional
        'max_per_week': 7,
    },
    PersonaType.FELIPE: {
        'daily_adelaide': True,  # Default
        'weekly_adelaide': True,
        'monthly_adelaide': True,
        'quarterly_adelaide': True,
        'crisis_alerts': True,
        'milestone_alerts': True,
        'promotional': True,
        'whale_alerts': True,  # Felipe only
        'max_per_week': 14,
    },
}
```

### 6.2 Frequency Manager

```python
class CommunicationFrequencyManager:
    """Manage communication frequency per persona."""
    
    def __init__(self):
        self.rules = NOTIFICATION_RULES
    
    def should_send(
        self,
        persona: PersonaType,
        notification_type: str,
        notifications_this_week: int
    ) -> bool:
        """Determine if notification should be sent."""
        
        rules = self.rules[persona]
        
        # Check if notification type is enabled
        if not rules.get(notification_type, False):
            return False
        
        # Check weekly limit (except crisis)
        if notification_type != 'crisis_alerts':
            if notifications_this_week >= rules['max_per_week']:
                return False
        
        return True
    
    def get_digest_preference(self, persona: PersonaType) -> str:
        """Get digest preference for persona."""
        
        if persona == PersonaType.ANA:
            return 'weekly'  # Prefer weekly digest
        elif persona == PersonaType.MARIA:
            return 'daily'  # Daily is fine
        else:
            return 'realtime'  # Felipe wants everything
```

---

## 7. Strategy Surfacing

### 7.1 Strategy Recommendations by Persona

```python
class StrategySurfacer:
    """Surface appropriate strategies for personas."""
    
    PERSONA_STRATEGIES = {
        PersonaType.ANA: {
            'primary': [1, 2, 3],  # Conservative
            'secondary': [4],      # One moderate option
            'never_show': [8, 9, 10],  # Too risky
        },
        PersonaType.MARIA: {
            'primary': [4, 5, 6, 7],  # Moderate
            'secondary': [1, 2, 3, 8],  # Conservative + one aggressive
            'never_show': [10],  # Max yield too risky
        },
        PersonaType.FELIPE: {
            'primary': [8, 9, 10],  # Aggressive
            'secondary': [4, 5, 6, 7],  # Moderate as diversification
            'never_show': [],  # Show everything
        },
    }
    
    def get_strategies_for_persona(
        self,
        persona: PersonaType,
        context: str = 'default'
    ) -> dict:
        """Get strategies to show for persona."""
        
        config = self.PERSONA_STRATEGIES[persona]
        
        return {
            'highlight': config['primary'],
            'available': config['secondary'],
            'hidden': config['never_show'],
        }
    
    def should_show_strategy(
        self,
        persona: PersonaType,
        strategy_id: int
    ) -> bool:
        """Check if strategy should be shown to persona."""
        
        config = self.PERSONA_STRATEGIES[persona]
        return strategy_id not in config['never_show']
```

---

## 8. Database Schema

```sql
-- User persona classification
CREATE TABLE user_personas (
    user_id UUID PRIMARY KEY,
    persona_type VARCHAR(20) NOT NULL DEFAULT 'maria',
    confidence_score DECIMAL(4,3),
    classification_method VARCHAR(50), -- 'auto', 'explicit', 'default'
    classified_at TIMESTAMP NOT NULL,
    signals_used JSONB,
    
    -- Override
    explicit_override BOOLEAN DEFAULT FALSE,
    override_at TIMESTAMP,
    override_reason TEXT,
    
    -- History
    previous_persona VARCHAR(20),
    reclassification_count INT DEFAULT 0,
    
    CONSTRAINT valid_persona CHECK (persona_type IN ('ana', 'maria', 'felipe'))
);

-- Classification signals history
CREATE TABLE persona_signals (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    signal_type VARCHAR(50) NOT NULL,
    signal_value JSONB,
    persona_contribution JSONB, -- {"ana": 0.3, "maria": 0.5, "felipe": 0.2}
    recorded_at TIMESTAMP NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Communication preferences (persona-derived + overrides)
CREATE TABLE user_comm_preferences (
    user_id UUID PRIMARY KEY,
    
    -- Derived from persona
    daily_adelaide BOOLEAN DEFAULT TRUE,
    weekly_adelaide BOOLEAN DEFAULT TRUE,
    monthly_adelaide BOOLEAN DEFAULT TRUE,
    crisis_alerts BOOLEAN DEFAULT TRUE,
    milestone_alerts BOOLEAN DEFAULT TRUE,
    whale_alerts BOOLEAN DEFAULT FALSE,
    promotional BOOLEAN DEFAULT FALSE,
    
    -- User overrides
    overrides JSONB DEFAULT '{}',
    
    -- Tracking
    notifications_this_week INT DEFAULT 0,
    week_start DATE,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_user_personas_type ON user_personas(persona_type);
CREATE INDEX idx_persona_signals_user ON persona_signals(user_id, recorded_at DESC);
```

---

## 9. API Specification

### 9.1 Classification Endpoint

```yaml
# POST /api/v1/persona/classify
request:
  user_id: string (required)
  signals:
    deposits: number
    strategies: array[int]
    quiz_answers: object
    engagement: object
    content_interactions: object

response:
  persona: "ana" | "maria" | "felipe"
  confidence: number (0-1)
  signals_used: array[string]
  recommendations:
    strategies: array[int]
    communication_frequency: string
```

### 9.2 Adaptation Endpoint

```yaml
# POST /api/v1/persona/adapt
request:
  user_id: string (required)
  content: string (required)
  content_type: "adelaide" | "notification" | "email"

response:
  adapted_content: string
  adaptations_applied:
    - type: string
      description: string
  persona_used: string
```

---

## 10. Configuration

```yaml
# config/persona_engine.yaml

persona_engine:
  # Default persona for new users
  default_persona: "maria"
  
  # Minimum signals for confident classification
  min_signals_for_classification: 2
  
  # Signal weights
  signal_weights:
    deposit_size: 0.30
    strategy_selections: 0.25
    questionnaire: 0.20
    engagement: 0.15
    content_interactions: 0.10
  
  # Reclassification triggers
  reclassification:
    frequency_days: 30
    on_major_deposit: true
    major_deposit_threshold: 5000
  
  # Content adaptation
  adaptation:
    ana:
      max_sentence_length: 15
      max_paragraph_length: 3
      emoji_frequency: "heavy"
    maria:
      max_sentence_length: 20
      max_paragraph_length: 4
      emoji_frequency: "moderate"
    felipe:
      max_sentence_length: 25
      max_paragraph_length: 5
      emoji_frequency: "minimal"
  
  # Strategy surfacing
  strategy_visibility:
    ana:
      show: [1, 2, 3, 4]
      highlight: [1, 2, 3]
    maria:
      show: [1, 2, 3, 4, 5, 6, 7, 8]
      highlight: [4, 5, 6, 7]
    felipe:
      show: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      highlight: [8, 9, 10]
```

---

## 11. Testing Requirements

### 11.1 Unit Tests

```python
class TestPersonaClassifier:
    def test_low_deposit_classifies_as_ana(self):
        """Test low deposit users classify as Ana."""
        classifier = PersonaClassifier()
        user_data = {'total_deposits': 500}
        persona, _ = classifier.classify(user_data)
        assert persona == PersonaType.ANA
    
    def test_high_deposit_classifies_as_felipe(self):
        """Test high deposit users classify as Felipe."""
        classifier = PersonaClassifier()
        user_data = {'total_deposits': 50000}
        persona, _ = classifier.classify(user_data)
        assert persona == PersonaType.FELIPE
    
    def test_explicit_override_respected(self):
        """Test explicit persona override is respected."""
        # ... implementation

class TestContentAdapter:
    def test_ana_removes_technical_terms(self):
        """Test Ana persona removes technical terms."""
        adapter = ContentAdapter()
        content = "Your APY is 5% with low TVL risk."
        adapted = adapter.adapt(content, PersonaType.ANA)
        assert "APY" not in adapted
        assert "TVL" not in adapted
    
    def test_felipe_keeps_technical_terms(self):
        """Test Felipe persona keeps technical terms."""
        adapter = ContentAdapter()
        content = "Your APY is 5% with low TVL risk."
        adapted = adapter.adapt(content, PersonaType.FELIPE)
        assert "APY" in adapted or "yearly return" in adapted
```

---

## 12. Implementation Checklist

- [ ] PersonaClassifier implemented
- [ ] All 5 signal scorers working
- [ ] ContentAdapter implemented
- [ ] Technical term replacement dictionary complete
- [ ] RiskLanguageCalibrator implemented
- [ ] All loss/gain templates created (3 personas Ã— 4 scenarios)
- [ ] CommunicationFrequencyManager working
- [ ] StrategySurfacer working
- [ ] Database tables created
- [ ] API endpoints functional
- [ ] Unit tests passing (>85% coverage)
- [ ] Integration tests passing

---

**Document End**

**Next:** CMO_03_MULTI_CHANNEL_DISTRIBUTION.md
