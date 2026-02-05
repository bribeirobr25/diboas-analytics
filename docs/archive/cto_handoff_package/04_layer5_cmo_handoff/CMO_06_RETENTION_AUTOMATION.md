# CMO_06: Retention Automation
## User Engagement & Win-Back System

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P1 (Required within 30 days of launch)

---

## 1. Purpose

The Retention Automation system maintains user engagement through automated sequences triggered by behavior patterns, milestones, and inactivity signals.

### Key Objectives

| Objective | Target | Measurement |
|-----------|--------|-------------|
| Reduce churn | <5% monthly | Users who withdraw 100% |
| Increase engagement | >60% Adelaide open rate | Email opens |
| Celebrate milestones | 100% coverage | All milestones acknowledged |
| Win back inactive | >20% reactivation | Inactive users returning |

---

## 2. Trigger Framework

### 2.1 Trigger Categories

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime, timedelta

class TriggerCategory(Enum):
    INACTIVITY = "inactivity"      # User hasn't engaged
    MILESTONE = "milestone"         # User achieved something
    BEHAVIOR = "behavior"           # Specific action pattern
    LIFECYCLE = "lifecycle"         # Time-based lifecycle
    RISK = "risk"                   # Churn risk detected

class TriggerType(Enum):
    # Inactivity triggers
    INACTIVE_7_DAYS = "inactive_7_days"
    INACTIVE_14_DAYS = "inactive_14_days"
    INACTIVE_30_DAYS = "inactive_30_days"
    NO_ADELAIDE_OPEN_7_DAYS = "no_adelaide_open_7_days"
    
    # Milestone triggers
    FIRST_DEPOSIT = "first_deposit"
    FIRST_YIELD_EARNED = "first_yield_earned"
    FIRST_MONTH_ANNIVERSARY = "first_month_anniversary"
    STRATEGY_OUTPERFORMANCE = "strategy_outperformance"
    DEPOSIT_MILESTONE = "deposit_milestone"  # â‚¬1K, â‚¬5K, â‚¬10K, etc.
    
    # Behavior triggers
    VIEWED_EXIT_PAGE = "viewed_exit_page"
    PARTIAL_WITHDRAWAL = "partial_withdrawal"
    MULTIPLE_SUPPORT_TICKETS = "multiple_support_tickets"
    
    # Lifecycle triggers
    TRIAL_ENDING = "trial_ending"
    ACCOUNT_ANNIVERSARY = "account_anniversary"
    
    # Risk triggers
    HIGH_CHURN_RISK = "high_churn_risk"
    NEGATIVE_SENTIMENT = "negative_sentiment"

@dataclass
class RetentionTrigger:
    """Definition of a retention trigger."""
    trigger_type: TriggerType
    category: TriggerCategory
    condition: Callable  # Function that returns True if triggered
    sequence_id: str     # Which sequence to trigger
    priority: int        # Higher = more urgent
    cooldown_days: int   # Min days between triggers
    max_per_user: int    # Max times this can trigger per user
```

### 2.2 Trigger Definitions

```python
RETENTION_TRIGGERS = {
    # === INACTIVITY TRIGGERS ===
    TriggerType.INACTIVE_7_DAYS: RetentionTrigger(
        trigger_type=TriggerType.INACTIVE_7_DAYS,
        category=TriggerCategory.INACTIVITY,
        condition=lambda user: user.days_since_login >= 7,
        sequence_id='gentle_nudge',
        priority=3,
        cooldown_days=30,
        max_per_user=3
    ),
    
    TriggerType.INACTIVE_14_DAYS: RetentionTrigger(
        trigger_type=TriggerType.INACTIVE_14_DAYS,
        category=TriggerCategory.INACTIVITY,
        condition=lambda user: user.days_since_login >= 14,
        sequence_id='miss_you',
        priority=4,
        cooldown_days=30,
        max_per_user=2
    ),
    
    TriggerType.INACTIVE_30_DAYS: RetentionTrigger(
        trigger_type=TriggerType.INACTIVE_30_DAYS,
        category=TriggerCategory.INACTIVITY,
        condition=lambda user: user.days_since_login >= 30,
        sequence_id='win_back_campaign',
        priority=5,
        cooldown_days=60,
        max_per_user=2
    ),
    
    TriggerType.NO_ADELAIDE_OPEN_7_DAYS: RetentionTrigger(
        trigger_type=TriggerType.NO_ADELAIDE_OPEN_7_DAYS,
        category=TriggerCategory.INACTIVITY,
        condition=lambda user: user.days_since_adelaide_open >= 7,
        sequence_id='adelaide_reengagement',
        priority=2,
        cooldown_days=14,
        max_per_user=4
    ),
    
    # === MILESTONE TRIGGERS ===
    TriggerType.FIRST_DEPOSIT: RetentionTrigger(
        trigger_type=TriggerType.FIRST_DEPOSIT,
        category=TriggerCategory.MILESTONE,
        condition=lambda user: user.total_deposits > 0 and user.deposit_count == 1,
        sequence_id='welcome_depositor',
        priority=5,
        cooldown_days=0,  # Only triggers once
        max_per_user=1
    ),
    
    TriggerType.FIRST_YIELD_EARNED: RetentionTrigger(
        trigger_type=TriggerType.FIRST_YIELD_EARNED,
        category=TriggerCategory.MILESTONE,
        condition=lambda user: user.total_yield_earned > 0 and not user.first_yield_celebrated,
        sequence_id='first_yield_celebration',
        priority=5,
        cooldown_days=0,
        max_per_user=1
    ),
    
    TriggerType.FIRST_MONTH_ANNIVERSARY: RetentionTrigger(
        trigger_type=TriggerType.FIRST_MONTH_ANNIVERSARY,
        category=TriggerCategory.MILESTONE,
        condition=lambda user: user.account_age_days == 30,
        sequence_id='one_month_anniversary',
        priority=4,
        cooldown_days=0,
        max_per_user=1
    ),
    
    TriggerType.STRATEGY_OUTPERFORMANCE: RetentionTrigger(
        trigger_type=TriggerType.STRATEGY_OUTPERFORMANCE,
        category=TriggerCategory.MILESTONE,
        condition=lambda user: any(s.vs_benchmark > 1.0 for s in user.strategies),
        sequence_id='outperformance_celebration',
        priority=3,
        cooldown_days=30,
        max_per_user=12  # Monthly
    ),
    
    TriggerType.DEPOSIT_MILESTONE: RetentionTrigger(
        trigger_type=TriggerType.DEPOSIT_MILESTONE,
        category=TriggerCategory.MILESTONE,
        condition=lambda user: user.crossed_deposit_milestone,
        sequence_id='deposit_milestone_celebration',
        priority=4,
        cooldown_days=0,
        max_per_user=10  # Multiple milestones
    ),
    
    # === BEHAVIOR TRIGGERS ===
    TriggerType.VIEWED_EXIT_PAGE: RetentionTrigger(
        trigger_type=TriggerType.VIEWED_EXIT_PAGE,
        category=TriggerCategory.BEHAVIOR,
        condition=lambda user: user.viewed_withdraw_page_recently,
        sequence_id='exit_prevention',
        priority=5,
        cooldown_days=7,
        max_per_user=3
    ),
    
    TriggerType.PARTIAL_WITHDRAWAL: RetentionTrigger(
        trigger_type=TriggerType.PARTIAL_WITHDRAWAL,
        category=TriggerCategory.BEHAVIOR,
        condition=lambda user: user.recent_withdrawal and user.remaining_balance > 0,
        sequence_id='post_withdrawal_check',
        priority=4,
        cooldown_days=14,
        max_per_user=5
    ),
    
    # === RISK TRIGGERS ===
    TriggerType.HIGH_CHURN_RISK: RetentionTrigger(
        trigger_type=TriggerType.HIGH_CHURN_RISK,
        category=TriggerCategory.RISK,
        condition=lambda user: user.churn_risk_score >= 0.7,
        sequence_id='high_risk_intervention',
        priority=5,
        cooldown_days=14,
        max_per_user=3
    ),
}
```

---

## 3. Retention Sequences

### 3.1 Sequence Definitions

```python
@dataclass
class SequenceStep:
    """Single step in a retention sequence."""
    step_number: int
    delay_hours: int        # Hours after previous step
    channel: str            # 'email', 'push', 'in_app'
    template_id: str
    condition: Optional[Callable]  # Skip if condition returns False

@dataclass
class RetentionSequence:
    """Multi-step retention sequence."""
    sequence_id: str
    name: str
    description: str
    steps: List[SequenceStep]
    exit_conditions: List[Callable]  # Stop sequence if any returns True

RETENTION_SEQUENCES = {
    # === GENTLE NUDGE (7 days inactive) ===
    'gentle_nudge': RetentionSequence(
        sequence_id='gentle_nudge',
        name='Gentle Nudge',
        description='Soft reminder for users inactive 7 days',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='nudge_checking_in',
                condition=None
            ),
        ],
        exit_conditions=[
            lambda user: user.logged_in_since_sequence_start,
        ]
    ),
    
    # === WIN BACK CAMPAIGN (30 days inactive) ===
    'win_back_campaign': RetentionSequence(
        sequence_id='win_back_campaign',
        name='Win Back Campaign',
        description='Multi-touch campaign for 30-day inactive users',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='winback_miss_you',
                condition=None
            ),
            SequenceStep(
                step_number=2,
                delay_hours=72,  # 3 days later
                channel='email',
                template_id='winback_whats_new',
                condition=lambda user: not user.logged_in_since_sequence_start
            ),
            SequenceStep(
                step_number=3,
                delay_hours=168,  # 7 days after start
                channel='email',
                template_id='winback_final',
                condition=lambda user: not user.logged_in_since_sequence_start
            ),
        ],
        exit_conditions=[
            lambda user: user.logged_in_since_sequence_start,
            lambda user: user.made_deposit_since_sequence_start,
        ]
    ),
    
    # === FIRST YIELD CELEBRATION ===
    'first_yield_celebration': RetentionSequence(
        sequence_id='first_yield_celebration',
        name='First Yield Celebration',
        description='Celebrate user earning their first yield',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='celebration_first_yield',
                condition=None
            ),
            SequenceStep(
                step_number=2,
                delay_hours=0,
                channel='push',
                template_id='push_first_yield',
                condition=lambda user: user.push_enabled
            ),
            SequenceStep(
                step_number=3,
                delay_hours=24,
                channel='email',
                template_id='education_compound_growth',
                condition=None
            ),
        ],
        exit_conditions=[]
    ),
    
    # === EXIT PREVENTION ===
    'exit_prevention': RetentionSequence(
        sequence_id='exit_prevention',
        name='Exit Prevention',
        description='Intervention when user views withdrawal page',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=1,  # 1 hour after viewing
                channel='in_app',
                template_id='exit_survey_prompt',
                condition=lambda user: not user.completed_withdrawal
            ),
            SequenceStep(
                step_number=2,
                delay_hours=24,
                channel='email',
                template_id='exit_reconsider',
                condition=lambda user: not user.completed_withdrawal
            ),
        ],
        exit_conditions=[
            lambda user: user.completed_withdrawal,
            lambda user: user.made_deposit_since_sequence_start,
        ]
    ),
    
    # === WELCOME DEPOSITOR ===
    'welcome_depositor': RetentionSequence(
        sequence_id='welcome_depositor',
        name='Welcome Depositor',
        description='Onboarding sequence for first deposit',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='welcome_first_deposit',
                condition=None
            ),
            SequenceStep(
                step_number=2,
                delay_hours=24,
                channel='email',
                template_id='education_how_yields_work',
                condition=None
            ),
            SequenceStep(
                step_number=3,
                delay_hours=72,
                channel='email',
                template_id='education_strategy_selection',
                condition=lambda user: len(user.strategies) == 0
            ),
            SequenceStep(
                step_number=4,
                delay_hours=168,  # 7 days
                channel='email',
                template_id='checkin_first_week',
                condition=None
            ),
        ],
        exit_conditions=[]
    ),
    
    # === ONE MONTH ANNIVERSARY ===
    'one_month_anniversary': RetentionSequence(
        sequence_id='one_month_anniversary',
        name='One Month Anniversary',
        description='Celebrate one month with diBoaS',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='anniversary_one_month',
                condition=None
            ),
        ],
        exit_conditions=[]
    ),
    
    # === ADELAIDE RE-ENGAGEMENT ===
    'adelaide_reengagement': RetentionSequence(
        sequence_id='adelaide_reengagement',
        name='Adelaide Re-engagement',
        description='Re-engage users not opening Adelaide',
        steps=[
            SequenceStep(
                step_number=1,
                delay_hours=0,
                channel='email',
                template_id='adelaide_miss_you',
                condition=None
            ),
        ],
        exit_conditions=[
            lambda user: user.opened_adelaide_since_sequence_start,
        ]
    ),
}
```

---

## 4. Email Templates

### 4.1 Template Library

```python
RETENTION_TEMPLATES = {
    # === NUDGE TEMPLATES ===
    'nudge_checking_in': {
        'subject': {
            'en': "Just checking in ðŸ‘‹",
            'pt-br': "SÃ³ passando para ver como vocÃª estÃ¡ ðŸ‘‹",
        },
        'body_template': 'retention/nudge_checking_in_{locale}.html',
        'persona_variations': False,
        'tone': 'warm',
    },
    
    # === WIN BACK TEMPLATES ===
    'winback_miss_you': {
        'subject': {
            'en': "We miss you at diBoaS",
            'pt-br': "Sentimos sua falta na diBoaS",
        },
        'body_template': 'retention/winback_miss_you_{locale}.html',
        'persona_variations': True,  # Different for Ana/Maria/Felipe
        'tone': 'warm',
    },
    'winback_whats_new': {
        'subject': {
            'en': "Here's what you've missed",
            'pt-br': "Veja o que vocÃª perdeu",
        },
        'body_template': 'retention/winback_whats_new_{locale}.html',
        'persona_variations': False,
        'tone': 'informative',
    },
    'winback_final': {
        'subject': {
            'en': "Your strategies are waiting",
            'pt-br': "Suas estratÃ©gias estÃ£o esperando",
        },
        'body_template': 'retention/winback_final_{locale}.html',
        'persona_variations': True,
        'tone': 'gentle_urgency',
    },
    
    # === CELEBRATION TEMPLATES ===
    'celebration_first_yield': {
        'subject': {
            'en': "ðŸŽ‰ You earned your first yield!",
            'pt-br': "ðŸŽ‰ VocÃª ganhou seu primeiro rendimento!",
        },
        'body_template': 'retention/celebration_first_yield_{locale}.html',
        'persona_variations': True,
        'tone': 'celebratory',
        'data_required': ['yield_amount', 'strategy_name'],
    },
    'anniversary_one_month': {
        'subject': {
            'en': "ðŸŽ‚ Happy 1 month with diBoaS!",
            'pt-br': "ðŸŽ‚ Feliz 1 mÃªs com a diBoaS!",
        },
        'body_template': 'retention/anniversary_one_month_{locale}.html',
        'persona_variations': False,
        'tone': 'celebratory',
        'data_required': ['total_yield', 'strategies_used'],
    },
    
    # === WELCOME TEMPLATES ===
    'welcome_first_deposit': {
        'subject': {
            'en': "Welcome to diBoaS! Your money is working",
            'pt-br': "Bem-vindo Ã  diBoaS! Seu dinheiro estÃ¡ trabalhando",
        },
        'body_template': 'retention/welcome_first_deposit_{locale}.html',
        'persona_variations': True,
        'tone': 'warm_welcoming',
        'data_required': ['deposit_amount', 'selected_strategy'],
    },
    
    # === EDUCATION TEMPLATES ===
    'education_how_yields_work': {
        'subject': {
            'en': "How your money earns while you sleep",
            'pt-br': "Como seu dinheiro rende enquanto vocÃª dorme",
        },
        'body_template': 'retention/education_yields_{locale}.html',
        'persona_variations': True,
        'tone': 'educational',
    },
    'education_compound_growth': {
        'subject': {
            'en': "The magic of compound growth",
            'pt-br': "A mÃ¡gica dos juros compostos",
        },
        'body_template': 'retention/education_compound_{locale}.html',
        'persona_variations': True,
        'tone': 'educational',
    },
    
    # === EXIT TEMPLATES ===
    'exit_reconsider': {
        'subject': {
            'en': "Before you go...",
            'pt-br': "Antes de vocÃª ir...",
        },
        'body_template': 'retention/exit_reconsider_{locale}.html',
        'persona_variations': False,
        'tone': 'understanding',
    },
    
    # === ADELAIDE RE-ENGAGEMENT ===
    'adelaide_miss_you': {
        'subject': {
            'en': "Adelaide misses you â˜•",
            'pt-br': "Adelaide sente sua falta â˜•",
        },
        'body_template': 'retention/adelaide_miss_you_{locale}.html',
        'persona_variations': False,
        'tone': 'warm',
    },
}
```

### 4.2 Template Content Examples

```html
<!-- retention/celebration_first_yield_en.html -->

<h1>ðŸŽ‰ Congratulations, {user_name}!</h1>

<p>You just earned your first yield with diBoaS.</p>

<div class="highlight-box">
    <p class="yield-amount">+{yield_amount}</p>
    <p class="yield-strategy">from {strategy_name}</p>
</div>

<p>
    Your grandmother would say: "The first fruits are always the sweetest."
</p>

<p>
    This is just the beginning. Your money is now working for you, 
    earning while you sleep, eat, and live your life.
</p>

<p>
    Here's what happens next: your yield will be automatically 
    reinvested (unless you choose otherwise), which means your 
    earnings will start earning too. That's the power of compound growth.
</p>

<div class="cta-section">
    <a href="{app_url}" class="button">See Your Progress</a>
</div>

<p class="signature">
    Cheering you on,<br>
    Adelaide ðŸ’š
</p>
```

```html
<!-- retention/winback_miss_you_pt-br.html (Ana persona) -->

<h1>Oi, {user_name} ðŸ‘‹</h1>

<p>
    Faz um tempinho que a gente nÃ£o se vÃª. Tudo bem com vocÃª?
</p>

<p>
    Seu dinheiro continua seguro aqui na diBoaS. 
    {if balance > 0}
    Inclusive, enquanto vocÃª estava fora, suas estratÃ©gias 
    renderam {yield_since_last_login}.
    {/if}
</p>

<p>
    A vovÃ³ sempre dizia: "Dinheiro guardado Ã© dinheiro cuidado."
    O seu estÃ¡ bem cuidado aqui.
</p>

<p>
    Se tiver alguma dÃºvida ou preocupaÃ§Ã£o, pode falar com a gente.
    Estamos aqui pra ajudar.
</p>

<div class="cta-section">
    <a href="{app_url}" class="button">Ver Minha Conta</a>
</div>

<p class="signature">
    Com carinho,<br>
    Adelaide ðŸ’š
</p>
```

---

## 5. Churn Risk Scoring

### 5.1 Risk Model

```python
class ChurnRiskScorer:
    """Calculate churn risk score for users."""
    
    # Feature weights (sum to 1.0)
    WEIGHTS = {
        'days_since_login': 0.25,
        'days_since_deposit': 0.15,
        'adelaide_open_rate': 0.15,
        'withdrawal_signals': 0.20,
        'support_tickets': 0.10,
        'strategy_performance': 0.10,
        'engagement_trend': 0.05,
    }
    
    def calculate_risk(self, user: User) -> float:
        """
        Calculate churn risk score (0-1).
        
        0 = No risk
        1 = Highest risk
        """
        scores = {}
        
        # Days since login (0-90 days mapped to 0-1)
        scores['days_since_login'] = min(user.days_since_login / 90, 1.0)
        
        # Days since deposit (0-180 days mapped to 0-1)
        scores['days_since_deposit'] = min(user.days_since_last_deposit / 180, 1.0)
        
        # Adelaide open rate (inverted: high open = low risk)
        scores['adelaide_open_rate'] = 1 - user.adelaide_open_rate_30d
        
        # Withdrawal signals
        withdrawal_score = 0
        if user.viewed_withdraw_page_last_7d:
            withdrawal_score += 0.5
        if user.made_withdrawal_last_30d:
            withdrawal_score += 0.5
        scores['withdrawal_signals'] = withdrawal_score
        
        # Support tickets (more tickets = higher risk)
        scores['support_tickets'] = min(user.support_tickets_last_30d / 5, 1.0)
        
        # Strategy performance (negative = higher risk)
        avg_performance = sum(s.ytd_return for s in user.strategies) / len(user.strategies) if user.strategies else 0
        scores['strategy_performance'] = max(0, -avg_performance / 10)  # -10% = 1.0 risk
        
        # Engagement trend (declining = higher risk)
        scores['engagement_trend'] = max(0, user.engagement_trend_30d * -1)  # Negative trend = risk
        
        # Weighted sum
        total_risk = sum(
            scores[feature] * weight 
            for feature, weight in self.WEIGHTS.items()
        )
        
        return min(total_risk, 1.0)
    
    def get_risk_factors(self, user: User) -> List[str]:
        """Get human-readable risk factors."""
        factors = []
        
        if user.days_since_login > 14:
            factors.append(f"Haven't logged in for {user.days_since_login} days")
        
        if user.adelaide_open_rate_30d < 0.3:
            factors.append("Low Adelaide engagement")
        
        if user.viewed_withdraw_page_last_7d:
            factors.append("Recently viewed withdrawal page")
        
        if user.support_tickets_last_30d >= 3:
            factors.append("Multiple support tickets")
        
        return factors
```

---

## 6. Sequence Engine

### 6.1 Execution Engine

```python
from datetime import datetime, timedelta
import asyncio

class SequenceEngine:
    """Execute retention sequences."""
    
    def __init__(self, db, email_service, push_service):
        self.db = db
        self.email = email_service
        self.push = push_service
    
    async def run_trigger_check(self):
        """Check all users for trigger conditions."""
        users = await self.db.get_active_users()
        
        for user in users:
            await self._check_triggers_for_user(user)
    
    async def _check_triggers_for_user(self, user: User):
        """Check all triggers for a single user."""
        for trigger_type, trigger in RETENTION_TRIGGERS.items():
            # Check if trigger condition is met
            if not trigger.condition(user):
                continue
            
            # Check cooldown
            if await self._is_in_cooldown(user.id, trigger_type, trigger.cooldown_days):
                continue
            
            # Check max triggers
            if await self._exceeded_max_triggers(user.id, trigger_type, trigger.max_per_user):
                continue
            
            # Start sequence
            await self._start_sequence(user, trigger)
    
    async def _start_sequence(self, user: User, trigger: RetentionTrigger):
        """Start a retention sequence for user."""
        sequence = RETENTION_SEQUENCES.get(trigger.sequence_id)
        if not sequence:
            return
        
        # Create sequence instance
        instance = await self.db.create_sequence_instance(
            user_id=user.id,
            sequence_id=sequence.sequence_id,
            trigger_type=trigger.trigger_type,
            started_at=datetime.utcnow()
        )
        
        # Execute first step immediately
        await self._execute_step(user, sequence, sequence.steps[0], instance.id)
        
        # Schedule remaining steps
        for step in sequence.steps[1:]:
            await self._schedule_step(user, sequence, step, instance.id)
    
    async def _execute_step(
        self, 
        user: User, 
        sequence: RetentionSequence, 
        step: SequenceStep,
        instance_id: str
    ):
        """Execute a single sequence step."""
        
        # Check exit conditions
        for exit_condition in sequence.exit_conditions:
            if exit_condition(user):
                await self._end_sequence(instance_id, 'exit_condition_met')
                return
        
        # Check step condition
        if step.condition and not step.condition(user):
            return  # Skip this step
        
        # Get template
        template = RETENTION_TEMPLATES.get(step.template_id)
        if not template:
            return
        
        # Render content
        content = await self._render_template(template, user)
        
        # Send via appropriate channel
        if step.channel == 'email':
            await self.email.send(
                to=user.email,
                subject=content['subject'],
                body=content['body']
            )
        elif step.channel == 'push':
            await self.push.send(
                user_id=user.id,
                title=content['title'],
                body=content['body']
            )
        elif step.channel == 'in_app':
            await self.db.create_in_app_message(
                user_id=user.id,
                content=content
            )
        
        # Record delivery
        await self.db.record_step_delivery(
            instance_id=instance_id,
            step_number=step.step_number,
            channel=step.channel,
            delivered_at=datetime.utcnow()
        )
    
    async def _schedule_step(
        self, 
        user: User, 
        sequence: RetentionSequence, 
        step: SequenceStep,
        instance_id: str
    ):
        """Schedule a future step."""
        execute_at = datetime.utcnow() + timedelta(hours=step.delay_hours)
        
        await self.db.schedule_sequence_step(
            instance_id=instance_id,
            step_number=step.step_number,
            execute_at=execute_at
        )
    
    async def process_scheduled_steps(self):
        """Process all scheduled steps that are due."""
        due_steps = await self.db.get_due_sequence_steps()
        
        for scheduled in due_steps:
            user = await self.db.get_user(scheduled.user_id)
            sequence = RETENTION_SEQUENCES.get(scheduled.sequence_id)
            step = sequence.steps[scheduled.step_number - 1]
            
            await self._execute_step(user, sequence, step, scheduled.instance_id)
```

---

## 7. Database Schema

```sql
-- Sequence instances (active sequences for users)
CREATE TABLE retention_sequence_instances (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    sequence_id VARCHAR(50) NOT NULL,
    trigger_type VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    end_reason VARCHAR(50),  -- 'completed', 'exit_condition_met', 'cancelled'
    current_step INT DEFAULT 1,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Step deliveries (audit trail)
CREATE TABLE retention_step_deliveries (
    id SERIAL PRIMARY KEY,
    instance_id UUID NOT NULL,
    step_number INT NOT NULL,
    channel VARCHAR(20) NOT NULL,
    template_id VARCHAR(50),
    delivered_at TIMESTAMP NOT NULL,
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP,
    
    FOREIGN KEY (instance_id) REFERENCES retention_sequence_instances(id)
);

-- Scheduled steps (future executions)
CREATE TABLE retention_scheduled_steps (
    id SERIAL PRIMARY KEY,
    instance_id UUID NOT NULL,
    step_number INT NOT NULL,
    execute_at TIMESTAMP NOT NULL,
    executed BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (instance_id) REFERENCES retention_sequence_instances(id)
);

-- Trigger history (for cooldowns)
CREATE TABLE retention_trigger_history (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    trigger_type VARCHAR(50) NOT NULL,
    triggered_at TIMESTAMP NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Churn risk scores
CREATE TABLE user_churn_risk (
    user_id UUID PRIMARY KEY,
    risk_score DECIMAL(4,3) NOT NULL,
    risk_factors JSONB,
    calculated_at TIMESTAMP NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_sequences_user ON retention_sequence_instances(user_id);
CREATE INDEX idx_scheduled_execute ON retention_scheduled_steps(execute_at) WHERE NOT executed;
CREATE INDEX idx_trigger_history_user ON retention_trigger_history(user_id, trigger_type);
CREATE INDEX idx_churn_risk_score ON user_churn_risk(risk_score DESC);
```

---

## 8. Configuration

```yaml
# config/retention.yaml

retention:
  enabled: true
  
  # Trigger checking
  trigger_check_frequency: "0 */4 * * *"  # Every 4 hours
  
  # Churn risk
  churn_risk:
    high_threshold: 0.7
    medium_threshold: 0.4
    recalculate_frequency: "0 0 * * *"  # Daily
    
  # Sequences
  sequences:
    max_active_per_user: 3
    global_cooldown_hours: 24  # Min hours between any sequences
    
  # Channels
  channels:
    email:
      enabled: true
      max_per_week: 5
    push:
      enabled: true
      max_per_day: 2
    in_app:
      enabled: true
      
  # Milestones
  deposit_milestones:
    - 1000
    - 5000
    - 10000
    - 25000
    - 50000
    - 100000
```

---

## 9. Implementation Checklist

- [ ] Trigger framework implemented
- [ ] All trigger conditions working
- [ ] Sequence engine functional
- [ ] All sequences defined
- [ ] All email templates created (EN + PT-BR)
- [ ] Churn risk scorer implemented
- [ ] Database schema created
- [ ] Scheduled job runner working
- [ ] Cooldown logic working
- [ ] Analytics tracking integrated
- [ ] Admin dashboard for monitoring

---

**Document End**

**Next:** CMO_07_GATE4_CMO_VALIDATIONS.md
