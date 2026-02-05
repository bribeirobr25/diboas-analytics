# CMO_08: Analytics & A/B Testing
## Performance Tracking & Experimentation Framework

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P1 (Required within 30 days of launch)

---

## 1. Purpose

The Analytics & A/B Testing system tracks Adelaide content performance and enables data-driven optimization through controlled experiments.

### Key Objectives

| Objective | Metric | Target |
|-----------|--------|--------|
| Track email engagement | Open rate | >50% |
| Track email engagement | Click rate | >10% |
| Measure content effectiveness | Adelaide â†’ deposit correlation | Positive |
| Optimize content | A/B test velocity | 2 tests/month |
| Understand user behavior | Segment analysis | 3 persona segments |

---

## 2. Analytics Architecture

### 2.1 Data Flow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         ANALYTICS ARCHITECTURE                              â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚  CONTENT DELIVERY                   USER INTERACTIONS                       â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                         â”‚
â”‚  â”‚ Email Sent  â”‚                   â”‚ Email Open  â”‚                         â”‚
â”‚  â”‚ Push Sent   â”‚                   â”‚ Link Click  â”‚                         â”‚
â”‚  â”‚ WhatsApp    â”‚                   â”‚ App Visit   â”‚                         â”‚
â”‚  â”‚ Telegram    â”‚                   â”‚ Deposit     â”‚                         â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜                   â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜                         â”‚
â”‚         â”‚                                 â”‚                                 â”‚
â”‚         â–¼                                 â–¼                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚                    EVENT COLLECTOR                                   â”‚   â”‚
â”‚  â”‚   ConvertKit Webhooks â”‚ Firebase â”‚ Mixpanel â”‚ Custom Events         â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                 â”‚                                           â”‚
â”‚                                 â–¼                                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚                    EVENT PROCESSOR                                   â”‚   â”‚
â”‚  â”‚   - Enrich with user data                                            â”‚   â”‚
â”‚  â”‚   - Add content metadata                                             â”‚   â”‚
â”‚  â”‚   - Calculate derived metrics                                        â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                 â”‚                                           â”‚
â”‚                                 â–¼                                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚                    DATA WAREHOUSE                                    â”‚   â”‚
â”‚  â”‚   PostgreSQL â”‚ Analytics Tables â”‚ Aggregations                       â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                 â”‚                                           â”‚
â”‚                                 â–¼                                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚                    DASHBOARDS & REPORTS                              â”‚   â”‚
â”‚  â”‚   Real-time â”‚ Daily â”‚ Weekly â”‚ Monthly                               â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 3. Event Tracking

### 3.1 Event Schema

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class EventType(Enum):
    # Delivery events
    CONTENT_GENERATED = "content_generated"
    EMAIL_SENT = "email_sent"
    PUSH_SENT = "push_sent"
    WHATSAPP_SENT = "whatsapp_sent"
    TELEGRAM_SENT = "telegram_sent"
    
    # Engagement events
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    PUSH_OPENED = "push_opened"
    APP_OPENED_FROM_CONTENT = "app_opened_from_content"
    
    # Conversion events
    DEPOSIT_AFTER_CONTENT = "deposit_after_content"
    STRATEGY_SELECTED_AFTER_CONTENT = "strategy_selected_after_content"
    
    # Retention events
    UNSUBSCRIBED = "unsubscribed"
    RESUBSCRIBED = "resubscribed"
    MARKED_SPAM = "marked_spam"

@dataclass
class AnalyticsEvent:
    """Base analytics event."""
    event_id: str
    event_type: EventType
    timestamp: datetime
    
    # User context
    user_id: str
    persona: str
    locale: str
    
    # Content context
    content_id: str
    edition_type: str
    template_used: str
    
    # Channel context
    channel: str
    
    # Additional properties
    properties: Dict[str, Any]
    
    # A/B test context (if applicable)
    ab_test_id: Optional[str]
    ab_variant: Optional[str]
```

### 3.2 Event Collector

```python
from typing import List
import httpx
from datetime import datetime
import json

class EventCollector:
    """Collect analytics events from various sources."""
    
    def __init__(self, db, queue):
        self.db = db
        self.queue = queue
    
    async def track(self, event: AnalyticsEvent):
        """Track a single event."""
        # Enrich event with additional context
        enriched = await self._enrich_event(event)
        
        # Store immediately
        await self.db.insert_event(enriched)
        
        # Queue for batch processing
        await self.queue.push('analytics_events', enriched)
    
    async def track_batch(self, events: List[AnalyticsEvent]):
        """Track multiple events."""
        for event in events:
            await self.track(event)
    
    async def _enrich_event(self, event: AnalyticsEvent) -> AnalyticsEvent:
        """Enrich event with additional context."""
        # Get user data
        user = await self.db.get_user(event.user_id)
        if user:
            event.properties['user_deposit_total'] = user.total_deposits
            event.properties['user_account_age_days'] = user.account_age_days
            event.properties['user_strategies_count'] = len(user.strategies)
        
        # Get content data
        content = await self.db.get_content(event.content_id)
        if content:
            event.properties['content_insight_used'] = content.insight_used
            event.properties['content_size_bytes'] = content.size_bytes
            event.properties['content_generation_time_ms'] = content.generation_time_ms
        
        return event

class ConvertKitWebhookHandler:
    """Handle ConvertKit webhooks for email events."""
    
    def __init__(self, collector: EventCollector):
        self.collector = collector
    
    async def handle_webhook(self, payload: dict):
        """Process ConvertKit webhook."""
        event_type_map = {
            'subscriber.subscriber_activate': None,  # Ignore
            'subscriber.subscriber_unsubscribe': EventType.UNSUBSCRIBED,
            'subscriber.subscriber_bounce': None,
            'subscriber.subscriber_complain': EventType.MARKED_SPAM,
            'broadcast.broadcast_send': EventType.EMAIL_SENT,
        }
        
        ck_event = payload.get('event')
        our_event_type = event_type_map.get(ck_event)
        
        if not our_event_type:
            return
        
        # Extract user and content IDs from tags/custom fields
        subscriber = payload.get('subscriber', {})
        user_id = subscriber.get('fields', {}).get('user_id')
        content_id = subscriber.get('fields', {}).get('last_content_id')
        
        event = AnalyticsEvent(
            event_id=f"ck_{payload.get('id')}",
            event_type=our_event_type,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            persona=subscriber.get('fields', {}).get('persona', 'unknown'),
            locale=subscriber.get('fields', {}).get('locale', 'en'),
            content_id=content_id,
            edition_type=subscriber.get('fields', {}).get('last_edition_type', 'unknown'),
            template_used=subscriber.get('fields', {}).get('last_template', 'unknown'),
            channel='email',
            properties={
                'email': subscriber.get('email_address'),
                'source': 'convertkit_webhook',
            },
            ab_test_id=subscriber.get('fields', {}).get('ab_test_id'),
            ab_variant=subscriber.get('fields', {}).get('ab_variant'),
        )
        
        await self.collector.track(event)
```

---

## 4. Metrics Definitions

### 4.1 Core Metrics

```python
@dataclass
class MetricDefinition:
    """Definition of a metric."""
    name: str
    description: str
    formula: str
    unit: str
    target: float
    warning_threshold: float
    critical_threshold: float

CORE_METRICS = {
    # === DELIVERY METRICS ===
    'email_delivery_rate': MetricDefinition(
        name='Email Delivery Rate',
        description='Percentage of emails successfully delivered',
        formula='(emails_delivered / emails_sent) * 100',
        unit='%',
        target=99.0,
        warning_threshold=97.0,
        critical_threshold=95.0
    ),
    
    # === ENGAGEMENT METRICS ===
    'adelaide_open_rate': MetricDefinition(
        name='Adelaide Open Rate',
        description='Percentage of Adelaide emails opened',
        formula='(unique_opens / emails_delivered) * 100',
        unit='%',
        target=50.0,
        warning_threshold=40.0,
        critical_threshold=30.0
    ),
    'adelaide_click_rate': MetricDefinition(
        name='Adelaide Click Rate',
        description='Percentage of Adelaide emails with clicks',
        formula='(unique_clicks / emails_delivered) * 100',
        unit='%',
        target=10.0,
        warning_threshold=5.0,
        critical_threshold=3.0
    ),
    'adelaide_click_to_open': MetricDefinition(
        name='Click-to-Open Rate',
        description='Clicks as percentage of opens',
        formula='(unique_clicks / unique_opens) * 100',
        unit='%',
        target=20.0,
        warning_threshold=15.0,
        critical_threshold=10.0
    ),
    
    # === RETENTION METRICS ===
    'unsubscribe_rate': MetricDefinition(
        name='Unsubscribe Rate',
        description='Percentage who unsubscribed',
        formula='(unsubscribes / emails_delivered) * 100',
        unit='%',
        target=0.5,  # Lower is better
        warning_threshold=1.0,
        critical_threshold=2.0
    ),
    'spam_complaint_rate': MetricDefinition(
        name='Spam Complaint Rate',
        description='Percentage marked as spam',
        formula='(spam_complaints / emails_delivered) * 100',
        unit='%',
        target=0.01,  # Lower is better
        warning_threshold=0.05,
        critical_threshold=0.1
    ),
    
    # === CONVERSION METRICS ===
    'content_to_deposit_rate': MetricDefinition(
        name='Content-to-Deposit Rate',
        description='Users who deposited within 24h of opening Adelaide',
        formula='(deposits_24h_after_open / unique_opens) * 100',
        unit='%',
        target=2.0,
        warning_threshold=1.0,
        critical_threshold=0.5
    ),
    
    # === SEGMENT METRICS ===
    'ana_engagement_score': MetricDefinition(
        name='Ana Segment Engagement',
        description='Engagement score for Ana persona',
        formula='weighted_avg(open_rate, click_rate, app_visits)',
        unit='score',
        target=70.0,
        warning_threshold=50.0,
        critical_threshold=30.0
    ),
    'maria_engagement_score': MetricDefinition(
        name='Maria Segment Engagement',
        description='Engagement score for Maria persona',
        formula='weighted_avg(open_rate, click_rate, app_visits)',
        unit='score',
        target=70.0,
        warning_threshold=50.0,
        critical_threshold=30.0
    ),
    'felipe_engagement_score': MetricDefinition(
        name='Felipe Segment Engagement',
        description='Engagement score for Felipe persona',
        formula='weighted_avg(open_rate, click_rate, app_visits)',
        unit='score',
        target=70.0,
        warning_threshold=50.0,
        critical_threshold=30.0
    ),
}
```

### 4.2 Metrics Calculator

```python
from datetime import datetime, timedelta
from typing import Dict

class MetricsCalculator:
    """Calculate metrics from raw events."""
    
    def __init__(self, db):
        self.db = db
    
    async def calculate_daily_metrics(self, date: datetime) -> Dict[str, float]:
        """Calculate all metrics for a given day."""
        start = date.replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)
        
        # Get event counts
        events = await self.db.get_events_in_range(start, end)
        
        # Group by type
        sent = len([e for e in events if e.event_type == EventType.EMAIL_SENT])
        opens = len([e for e in events if e.event_type == EventType.EMAIL_OPENED])
        clicks = len([e for e in events if e.event_type == EventType.EMAIL_CLICKED])
        unsubs = len([e for e in events if e.event_type == EventType.UNSUBSCRIBED])
        spam = len([e for e in events if e.event_type == EventType.MARKED_SPAM])
        deposits = len([e for e in events if e.event_type == EventType.DEPOSIT_AFTER_CONTENT])
        
        # Calculate metrics
        metrics = {}
        
        if sent > 0:
            metrics['email_delivery_rate'] = (sent / sent) * 100  # Simplified
            metrics['adelaide_open_rate'] = (opens / sent) * 100
            metrics['adelaide_click_rate'] = (clicks / sent) * 100
            metrics['unsubscribe_rate'] = (unsubs / sent) * 100
            metrics['spam_complaint_rate'] = (spam / sent) * 100
        
        if opens > 0:
            metrics['adelaide_click_to_open'] = (clicks / opens) * 100
            metrics['content_to_deposit_rate'] = (deposits / opens) * 100
        
        return metrics
    
    async def calculate_segment_metrics(
        self, 
        persona: str, 
        start: datetime, 
        end: datetime
    ) -> Dict[str, float]:
        """Calculate metrics for a specific persona segment."""
        events = await self.db.get_events_in_range(start, end, persona=persona)
        
        # Calculate same metrics but for segment
        # ... similar to above
        
        return {}
    
    async def compare_to_target(
        self, 
        metrics: Dict[str, float]
    ) -> Dict[str, dict]:
        """Compare metrics to targets and thresholds."""
        results = {}
        
        for metric_name, value in metrics.items():
            definition = CORE_METRICS.get(metric_name)
            if not definition:
                continue
            
            status = 'good'
            if metric_name in ['unsubscribe_rate', 'spam_complaint_rate']:
                # Lower is better
                if value > definition.critical_threshold:
                    status = 'critical'
                elif value > definition.warning_threshold:
                    status = 'warning'
            else:
                # Higher is better
                if value < definition.critical_threshold:
                    status = 'critical'
                elif value < definition.warning_threshold:
                    status = 'warning'
            
            results[metric_name] = {
                'value': value,
                'target': definition.target,
                'status': status,
                'unit': definition.unit,
            }
        
        return results
```

---

## 5. A/B Testing Framework

### 5.1 Test Definition

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum
from datetime import datetime

class TestStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TestType(Enum):
    SUBJECT_LINE = "subject_line"
    INSIGHT = "insight"
    TEMPLATE = "template"
    SEND_TIME = "send_time"
    PERSONALIZATION = "personalization"

@dataclass
class ABTestVariant:
    """A single variant in an A/B test."""
    variant_id: str  # 'A', 'B', 'C'
    name: str
    description: str
    config: Dict  # Variant-specific configuration
    weight: float  # Traffic allocation (0-1)

@dataclass
class ABTest:
    """A/B test definition."""
    test_id: str
    name: str
    description: str
    test_type: TestType
    
    # Variants
    variants: List[ABTestVariant]
    control_variant: str  # Which variant is control
    
    # Targeting
    target_segment: Optional[str]  # None = all users
    target_percentage: float  # 0-1, percentage of segment to include
    
    # Timing
    start_date: datetime
    end_date: Optional[datetime]  # None = run until manually stopped
    
    # Success criteria
    primary_metric: str  # e.g., 'adelaide_open_rate'
    secondary_metrics: List[str]
    minimum_sample_size: int
    significance_level: float  # e.g., 0.95 for 95%
    
    # Status
    status: TestStatus
    winner: Optional[str]  # Variant ID if determined
    
    # Metadata
    created_at: datetime
    created_by: str
```

### 5.2 Test Manager

```python
import random
import hashlib
from scipy import stats
import numpy as np

class ABTestManager:
    """Manage A/B tests."""
    
    def __init__(self, db):
        self.db = db
    
    async def create_test(self, test: ABTest) -> str:
        """Create a new A/B test."""
        # Validate test configuration
        self._validate_test(test)
        
        # Store test
        await self.db.insert_test(test)
        
        return test.test_id
    
    def _validate_test(self, test: ABTest):
        """Validate test configuration."""
        # Check weights sum to 1
        total_weight = sum(v.weight for v in test.variants)
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(f"Variant weights must sum to 1, got {total_weight}")
        
        # Check control variant exists
        if test.control_variant not in [v.variant_id for v in test.variants]:
            raise ValueError(f"Control variant {test.control_variant} not in variants")
        
        # Check minimum sample size is reasonable
        if test.minimum_sample_size < 100:
            raise ValueError("Minimum sample size should be at least 100")
    
    async def assign_variant(self, user_id: str, test_id: str) -> Optional[str]:
        """Assign user to a variant for a test."""
        test = await self.db.get_test(test_id)
        
        if not test or test.status != TestStatus.RUNNING:
            return None
        
        # Check if user already assigned
        existing = await self.db.get_user_variant(user_id, test_id)
        if existing:
            return existing.variant_id
        
        # Check if user is in target segment
        if test.target_segment:
            user = await self.db.get_user(user_id)
            if user.persona != test.target_segment:
                return None  # User not in segment
        
        # Deterministic assignment based on user_id + test_id
        # This ensures same user always gets same variant
        hash_input = f"{user_id}:{test_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        random_value = (hash_value % 10000) / 10000  # 0-1
        
        # Check if user is in test (based on target_percentage)
        if random_value > test.target_percentage:
            return None  # User not in test
        
        # Assign to variant based on weights
        cumulative = 0
        variant_random = (hash_value % 100000) / 100000  # Different hash portion
        
        for variant in test.variants:
            cumulative += variant.weight
            if variant_random < cumulative:
                # Record assignment
                await self.db.record_variant_assignment(
                    user_id=user_id,
                    test_id=test_id,
                    variant_id=variant.variant_id
                )
                return variant.variant_id
        
        # Fallback to last variant
        return test.variants[-1].variant_id
    
    async def get_variant_config(
        self, 
        user_id: str, 
        test_id: str
    ) -> Optional[Dict]:
        """Get configuration for user's assigned variant."""
        variant_id = await self.assign_variant(user_id, test_id)
        if not variant_id:
            return None
        
        test = await self.db.get_test(test_id)
        for variant in test.variants:
            if variant.variant_id == variant_id:
                return variant.config
        
        return None
    
    async def analyze_test(self, test_id: str) -> dict:
        """Analyze A/B test results."""
        test = await self.db.get_test(test_id)
        
        if not test:
            raise ValueError(f"Test {test_id} not found")
        
        # Get metrics for each variant
        variant_results = {}
        for variant in test.variants:
            metrics = await self._get_variant_metrics(test_id, variant.variant_id)
            variant_results[variant.variant_id] = metrics
        
        # Calculate statistical significance
        control = variant_results[test.control_variant]
        
        analysis = {
            'test_id': test_id,
            'status': test.status.value,
            'variants': {},
            'winner': None,
            'significance_reached': False,
        }
        
        for variant_id, metrics in variant_results.items():
            is_control = variant_id == test.control_variant
            
            if not is_control:
                # Calculate significance vs control
                significance = self._calculate_significance(
                    control_data=control,
                    treatment_data=metrics,
                    metric=test.primary_metric
                )
            else:
                significance = None
            
            analysis['variants'][variant_id] = {
                'is_control': is_control,
                'sample_size': metrics['sample_size'],
                'primary_metric': metrics[test.primary_metric],
                'significance_vs_control': significance,
                'is_winner': False,
            }
        
        # Determine winner
        if self._can_determine_winner(analysis, test):
            winner = self._determine_winner(analysis, test)
            analysis['winner'] = winner
            analysis['significance_reached'] = True
            analysis['variants'][winner]['is_winner'] = True
        
        return analysis
    
    async def _get_variant_metrics(
        self, 
        test_id: str, 
        variant_id: str
    ) -> Dict:
        """Get metrics for a specific variant."""
        events = await self.db.get_variant_events(test_id, variant_id)
        
        sent = len([e for e in events if e.event_type == EventType.EMAIL_SENT])
        opens = len([e for e in events if e.event_type == EventType.EMAIL_OPENED])
        clicks = len([e for e in events if e.event_type == EventType.EMAIL_CLICKED])
        
        return {
            'sample_size': sent,
            'adelaide_open_rate': (opens / sent * 100) if sent > 0 else 0,
            'adelaide_click_rate': (clicks / sent * 100) if sent > 0 else 0,
            'adelaide_click_to_open': (clicks / opens * 100) if opens > 0 else 0,
            'raw_opens': opens,
            'raw_clicks': clicks,
            'raw_sent': sent,
        }
    
    def _calculate_significance(
        self, 
        control_data: Dict, 
        treatment_data: Dict,
        metric: str
    ) -> dict:
        """Calculate statistical significance between control and treatment."""
        # Use z-test for proportions
        n1 = control_data['raw_sent']
        n2 = treatment_data['raw_sent']
        
        if metric == 'adelaide_open_rate':
            x1 = control_data['raw_opens']
            x2 = treatment_data['raw_opens']
        elif metric == 'adelaide_click_rate':
            x1 = control_data['raw_clicks']
            x2 = treatment_data['raw_clicks']
        else:
            return {'p_value': 1.0, 'significant': False}
        
        # Calculate pooled proportion
        p_pool = (x1 + x2) / (n1 + n2)
        
        # Calculate z-score
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
        if se == 0:
            return {'p_value': 1.0, 'significant': False}
        
        p1 = x1 / n1
        p2 = x2 / n2
        z = (p2 - p1) / se
        
        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        return {
            'z_score': z,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'lift': ((p2 - p1) / p1 * 100) if p1 > 0 else 0,
        }
    
    def _can_determine_winner(self, analysis: dict, test: ABTest) -> bool:
        """Check if we have enough data to determine winner."""
        # Check minimum sample size
        for variant_data in analysis['variants'].values():
            if variant_data['sample_size'] < test.minimum_sample_size:
                return False
        
        # Check if any variant has significant lift
        for variant_id, variant_data in analysis['variants'].items():
            if variant_data['is_control']:
                continue
            
            sig = variant_data.get('significance_vs_control', {})
            if sig and sig.get('significant') and sig.get('p_value', 1) < (1 - test.significance_level):
                return True
        
        return False
    
    def _determine_winner(self, analysis: dict, test: ABTest) -> str:
        """Determine winning variant."""
        best_variant = None
        best_metric = -float('inf')
        
        for variant_id, variant_data in analysis['variants'].items():
            metric_value = variant_data['primary_metric']
            
            # Only consider if significant or is control
            if variant_data['is_control']:
                is_valid = True
            else:
                sig = variant_data.get('significance_vs_control', {})
                is_valid = sig and sig.get('significant', False)
            
            if is_valid and metric_value > best_metric:
                best_metric = metric_value
                best_variant = variant_id
        
        return best_variant
```

### 5.3 Test Examples

```python
# Example: Subject Line Test
subject_line_test = ABTest(
    test_id='test_subject_001',
    name='Adelaide Daily Subject Line Test',
    description='Test emoji vs no emoji in subject line',
    test_type=TestType.SUBJECT_LINE,
    variants=[
        ABTestVariant(
            variant_id='A',
            name='Control - With Emoji',
            description='Current subject line with emoji',
            config={'subject_prefix': 'ðŸ“Š'},
            weight=0.5
        ),
        ABTestVariant(
            variant_id='B',
            name='Treatment - No Emoji',
            description='Subject line without emoji',
            config={'subject_prefix': ''},
            weight=0.5
        ),
    ],
    control_variant='A',
    target_segment=None,  # All users
    target_percentage=1.0,  # 100% of users
    start_date=datetime.utcnow(),
    end_date=None,
    primary_metric='adelaide_open_rate',
    secondary_metrics=['adelaide_click_rate'],
    minimum_sample_size=500,
    significance_level=0.95,
    status=TestStatus.RUNNING,
    winner=None,
    created_at=datetime.utcnow(),
    created_by='cmo_board'
)

# Example: Insight Variation Test
insight_test = ABTest(
    test_id='test_insight_001',
    name='Grandmother Voice Intensity Test',
    description='Test stronger vs softer grandmother voice in insights',
    test_type=TestType.INSIGHT,
    variants=[
        ABTestVariant(
            variant_id='A',
            name='Control - Standard Voice',
            description='Current grandmother voice level',
            config={'grandmother_intensity': 'moderate'},
            weight=0.5
        ),
        ABTestVariant(
            variant_id='B',
            name='Treatment - Strong Voice',
            description='More prominent grandmother references',
            config={'grandmother_intensity': 'strong'},
            weight=0.5
        ),
    ],
    control_variant='A',
    target_segment='ana',  # Only Ana persona
    target_percentage=1.0,
    start_date=datetime.utcnow(),
    end_date=None,
    primary_metric='adelaide_click_to_open',
    secondary_metrics=['content_to_deposit_rate'],
    minimum_sample_size=300,
    significance_level=0.95,
    status=TestStatus.DRAFT,
    winner=None,
    created_at=datetime.utcnow(),
    created_by='cmo_board'
)
```

---

## 6. Dashboards

### 6.1 Dashboard Specifications

```python
DASHBOARD_SPECS = {
    'adelaide_daily_overview': {
        'name': 'Adelaide Daily Overview',
        'refresh_interval': 300,  # 5 minutes
        'widgets': [
            {
                'type': 'metric_card',
                'metric': 'adelaide_open_rate',
                'comparison': 'previous_day',
            },
            {
                'type': 'metric_card',
                'metric': 'adelaide_click_rate',
                'comparison': 'previous_day',
            },
            {
                'type': 'line_chart',
                'metrics': ['adelaide_open_rate', 'adelaide_click_rate'],
                'timeframe': '7_days',
            },
            {
                'type': 'segment_breakdown',
                'metric': 'adelaide_open_rate',
                'segments': ['ana', 'maria', 'felipe'],
            },
        ],
    },
    
    'ab_test_results': {
        'name': 'A/B Test Results',
        'refresh_interval': 3600,  # 1 hour
        'widgets': [
            {
                'type': 'test_list',
                'status_filter': ['running', 'completed'],
            },
            {
                'type': 'test_detail',
                'test_id': 'dynamic',  # Selected test
            },
            {
                'type': 'significance_chart',
                'test_id': 'dynamic',
            },
        ],
    },
    
    'retention_health': {
        'name': 'Retention Health',
        'refresh_interval': 3600,
        'widgets': [
            {
                'type': 'metric_card',
                'metric': 'unsubscribe_rate',
                'comparison': 'previous_week',
            },
            {
                'type': 'metric_card',
                'metric': 'spam_complaint_rate',
                'comparison': 'previous_week',
            },
            {
                'type': 'funnel',
                'steps': ['sent', 'delivered', 'opened', 'clicked', 'converted'],
            },
        ],
    },
}
```

---

## 7. Database Schema

```sql
-- Analytics events
CREATE TABLE analytics_events (
    event_id VARCHAR(100) PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    
    -- User context
    user_id UUID,
    persona VARCHAR(20),
    locale VARCHAR(10),
    
    -- Content context
    content_id UUID,
    edition_type VARCHAR(20),
    template_used VARCHAR(100),
    
    -- Channel
    channel VARCHAR(20),
    
    -- Properties (JSON)
    properties JSONB,
    
    -- A/B test
    ab_test_id VARCHAR(100),
    ab_variant VARCHAR(10),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily metrics (aggregated)
CREATE TABLE daily_metrics (
    date DATE NOT NULL,
    segment VARCHAR(50) DEFAULT 'all',  -- 'all', 'ana', 'maria', 'felipe'
    
    -- Counts
    emails_sent INT DEFAULT 0,
    emails_opened INT DEFAULT 0,
    emails_clicked INT DEFAULT 0,
    unsubscribes INT DEFAULT 0,
    spam_complaints INT DEFAULT 0,
    deposits INT DEFAULT 0,
    
    -- Calculated rates
    open_rate DECIMAL(5,2),
    click_rate DECIMAL(5,2),
    unsubscribe_rate DECIMAL(5,4),
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (date, segment)
);

-- A/B tests
CREATE TABLE ab_tests (
    test_id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    test_type VARCHAR(50) NOT NULL,
    
    -- Variants (JSON array)
    variants JSONB NOT NULL,
    control_variant VARCHAR(10) NOT NULL,
    
    -- Targeting
    target_segment VARCHAR(50),
    target_percentage DECIMAL(3,2) NOT NULL,
    
    -- Timing
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    
    -- Success criteria
    primary_metric VARCHAR(50) NOT NULL,
    secondary_metrics JSONB,
    minimum_sample_size INT NOT NULL,
    significance_level DECIMAL(3,2) NOT NULL,
    
    -- Status
    status VARCHAR(20) NOT NULL,
    winner VARCHAR(10),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100)
);

-- A/B test assignments
CREATE TABLE ab_test_assignments (
    user_id UUID NOT NULL,
    test_id VARCHAR(100) NOT NULL,
    variant_id VARCHAR(10) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (user_id, test_id),
    FOREIGN KEY (test_id) REFERENCES ab_tests(test_id)
);

-- Indexes
CREATE INDEX idx_events_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_events_user ON analytics_events(user_id);
CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_ab ON analytics_events(ab_test_id, ab_variant);
CREATE INDEX idx_daily_metrics_date ON daily_metrics(date);
CREATE INDEX idx_tests_status ON ab_tests(status);
```

---

## 8. Configuration

```yaml
# config/analytics.yaml

analytics:
  enabled: true
  
  # Event collection
  collection:
    batch_size: 100
    flush_interval_seconds: 30
    
  # Metrics calculation
  metrics:
    calculation_schedule: "0 * * * *"  # Hourly
    retention_days: 365
    
  # A/B testing
  ab_testing:
    enabled: true
    default_significance_level: 0.95
    default_minimum_sample: 500
    auto_stop_on_significance: false
    
  # Dashboards
  dashboards:
    refresh_interval_seconds: 300
    
  # Alerting
  alerts:
    enabled: true
    channels:
      - slack: "#analytics-alerts"
      - email: "cmo@diboas.com"
    thresholds:
      open_rate_critical: 30
      unsubscribe_rate_critical: 2.0
```

---

## 9. Implementation Checklist

- [ ] Event schema defined
- [ ] Event collector implemented
- [ ] ConvertKit webhook handler working
- [ ] Core metrics defined
- [ ] Metrics calculator implemented
- [ ] Daily aggregation job running
- [ ] A/B test manager implemented
- [ ] Variant assignment working (deterministic)
- [ ] Statistical significance calculator working
- [ ] Test analysis reports generating
- [ ] Dashboard specifications complete
- [ ] Dashboard UI implemented
- [ ] Alerting system working
- [ ] Historical data backfill complete

---

**Document End**

**CMO Board CTO Handoff Complete**
