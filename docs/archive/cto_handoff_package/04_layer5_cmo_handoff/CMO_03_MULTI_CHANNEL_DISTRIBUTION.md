# CMO_03: Multi-Channel Distribution
## Channel Integration & Delivery Specification

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P0 (Launch-Critical for Email; P1 for others)

---

## 1. Purpose

The Multi-Channel Distribution system delivers Adelaide content across multiple channels, formatting content appropriately for each platform.

### Supported Channels

| Channel | Priority | Launch Phase | Integration |
|---------|----------|--------------|-------------|
| **Email** | P0 | Phase 1 | ConvertKit |
| **WhatsApp** | P1 | Phase 2 | WhatsApp Business API |
| **Telegram** | P1 | Phase 2 | Telegram Bot API |
| **Substack** | P1 | Phase 2 | Substack API |
| **SMS** | P2 | Phase 3 | Twilio |
| **Push** | P2 | Phase 3 | Firebase/OneSignal |

---

## 2. Channel Architecture

### 2.1 Distribution Flow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    MULTI-CHANNEL DISTRIBUTION                               â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚  Assembled Content (from CMO_01)                                            â”‚
â”‚           â”‚                                                                 â”‚
â”‚           â–¼                                                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              CHANNEL FORMATTER                                       â”‚   â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”  â”‚   â”‚
â”‚  â”‚  â”‚  Email  â”‚ â”‚WhatsApp â”‚ â”‚Telegram â”‚ â”‚Substack â”‚ â”‚ SMS â”‚ â”‚ Push â”‚  â”‚   â”‚
â”‚  â”‚  â”‚Formatterâ”‚ â”‚Formatterâ”‚ â”‚Formatterâ”‚ â”‚Formatterâ”‚ â”‚Fmt  â”‚ â”‚ Fmt  â”‚  â”‚   â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”¬â”€â”€â”˜ â””â”€â”€â”¬â”€â”€â”€â”˜  â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚          â”‚          â”‚          â”‚          â”‚         â”‚        â”‚           â”‚
â”‚          â–¼          â–¼          â–¼          â–¼         â–¼        â–¼           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              CHANNEL DISPATCHERS                                     â”‚   â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”  â”‚   â”‚
â”‚  â”‚  â”‚Convert- â”‚ â”‚WhatsApp â”‚ â”‚Telegram â”‚ â”‚Substack â”‚ â”‚Twilioâ”‚ â”‚FCM/  â”‚  â”‚   â”‚
â”‚  â”‚  â”‚  Kit    â”‚ â”‚  API    â”‚ â”‚Bot API  â”‚ â”‚  API    â”‚ â”‚     â”‚ â”‚Signalâ”‚  â”‚   â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”˜  â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 2.2 Channel Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum

class ChannelType(Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    SUBSTACK = "substack"
    SMS = "sms"
    PUSH = "push"

@dataclass
class ChannelContent:
    """Content formatted for a specific channel."""
    channel: ChannelType
    formatted_content: str
    metadata: Dict
    size_bytes: int
    
    # Channel-specific
    subject: Optional[str] = None  # Email/Push
    preview_text: Optional[str] = None  # Email
    buttons: Optional[List[Dict]] = None  # WhatsApp/Telegram
    media_url: Optional[str] = None  # WhatsApp/Telegram

@dataclass
class DeliveryResult:
    """Result of channel delivery."""
    success: bool
    channel: ChannelType
    recipient_id: str
    message_id: Optional[str]
    error: Optional[str]
    timestamp: str

class ChannelFormatter(ABC):
    """Base class for channel formatters."""
    
    @abstractmethod
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format content for this channel."""
        pass
    
    @abstractmethod
    def get_max_length(self) -> int:
        """Get maximum content length for channel."""
        pass

class ChannelDispatcher(ABC):
    """Base class for channel dispatchers."""
    
    @abstractmethod
    async def send(self, content: ChannelContent, recipient: str) -> DeliveryResult:
        """Send content to recipient."""
        pass
    
    @abstractmethod
    async def send_bulk(self, content: ChannelContent, recipients: List[str]) -> List[DeliveryResult]:
        """Send content to multiple recipients."""
        pass
```

---

## 3. Email Channel (ConvertKit)

### 3.1 ConvertKit Integration

```python
import httpx
from typing import List, Optional

class ConvertKitConfig:
    """ConvertKit configuration."""
    api_key: str
    api_secret: str
    base_url: str = "https://api.convertkit.com/v3"
    
    # Adelaide-specific
    adelaide_daily_sequence_id: int
    adelaide_weekly_sequence_id: int
    adelaide_crisis_broadcast_id: int
    
    # Tags
    tag_ids: dict = {
        'ana': 12345,
        'maria': 12346,
        'felipe': 12347,
        'locale_en': 12348,
        'locale_de': 12349,
        'locale_pt_br': 12350,
        'locale_es': 12351,
    }

class EmailFormatter(ChannelFormatter):
    """Format content for email delivery."""
    
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
    
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format Adelaide content for email."""
        
        # Load email template
        template = self._load_template(context.get('edition_type', 'daily'))
        
        # Build HTML version
        html_content = self._build_html(content, template, context)
        
        # Build plain text version
        text_content = self._build_plain_text(content)
        
        # Generate subject line
        subject = self._generate_subject(context)
        
        # Generate preview text
        preview = self._generate_preview(content)
        
        return ChannelContent(
            channel=ChannelType.EMAIL,
            formatted_content=html_content,
            metadata={
                'plain_text': text_content,
                'template_used': template,
            },
            size_bytes=len(html_content.encode('utf-8')),
            subject=subject,
            preview_text=preview
        )
    
    def get_max_length(self) -> int:
        return 102400  # 100KB for email
    
    def _build_html(self, content: str, template: str, context: dict) -> str:
        """Build HTML email from markdown content."""
        import markdown
        
        # Convert markdown to HTML
        html_body = markdown.markdown(content, extensions=['tables', 'fenced_code'])
        
        # Wrap in email template
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{context.get('subject', 'Adelaide Daily')}</title>
            <style>
                {self._get_email_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://diboas.com/logo.png" alt="diBoaS" width="120">
                </div>
                <div class="content">
                    {html_body}
                </div>
                <div class="footer">
                    <p>Â© 2026 diBoaS. All rights reserved.</p>
                    <p><a href="{{{{unsubscribe_url}}}}">Unsubscribe</a> | <a href="https://diboas.com/preferences">Preferences</a></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _build_plain_text(self, content: str) -> str:
        """Build plain text version of email."""
        # Strip markdown formatting
        import re
        
        text = content
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # Italic
        text = re.sub(r'#{1,6}\s*', '', text)  # Headers
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
        
        return text
    
    def _generate_subject(self, context: dict) -> str:
        """Generate email subject line."""
        edition = context.get('edition_type', 'daily')
        date = context.get('date', '')
        locale = context.get('locale', 'en')
        
        subjects = {
            'en': {
                'daily': f"Adelaide Daily â€” {date}",
                'weekly': f"Adelaide Weekly Review â€” {date}",
                'monthly': f"Adelaide Monthly Report â€” {date}",
                'crisis': "âš ï¸ Adelaide Alert â€” Market Update",
            },
            'pt-br': {
                'daily': f"Adelaide DiÃ¡rio â€” {date}",
                'weekly': f"Adelaide Resumo Semanal â€” {date}",
                'monthly': f"Adelaide RelatÃ³rio Mensal â€” {date}",
                'crisis': "âš ï¸ Alerta Adelaide â€” AtualizaÃ§Ã£o do Mercado",
            },
        }
        
        return subjects.get(locale, subjects['en']).get(edition, f"Adelaide â€” {date}")
    
    def _generate_preview(self, content: str) -> str:
        """Generate email preview text (first 100 chars)."""
        # Get first paragraph
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                preview = line.strip()[:100]
                if len(line) > 100:
                    preview += '...'
                return preview
        return "Your daily market update from Adelaide"
    
    def _get_email_styles(self) -> str:
        """Get email CSS styles."""
        return """
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                   line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; padding: 20px 0; border-bottom: 1px solid #eee; }
            .content { padding: 20px 0; }
            .footer { text-align: center; padding: 20px 0; border-top: 1px solid #eee; 
                      font-size: 12px; color: #666; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f5f5f5; }
            h1, h2, h3 { color: #1a1a1a; }
            a { color: #0066cc; }
        """

class ConvertKitDispatcher(ChannelDispatcher):
    """Dispatch emails via ConvertKit."""
    
    def __init__(self, config: ConvertKitConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={'Content-Type': 'application/json'}
        )
    
    async def send(self, content: ChannelContent, recipient: str) -> DeliveryResult:
        """Send email to single recipient."""
        try:
            # Get subscriber ID
            subscriber = await self._get_or_create_subscriber(recipient)
            
            # Send broadcast
            response = await self.client.post(
                f"/broadcasts",
                json={
                    'api_secret': self.config.api_secret,
                    'subject': content.subject,
                    'content': content.formatted_content,
                    'subscriber_ids': [subscriber['id']],
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return DeliveryResult(
                    success=True,
                    channel=ChannelType.EMAIL,
                    recipient_id=recipient,
                    message_id=data.get('broadcast', {}).get('id'),
                    error=None,
                    timestamp=datetime.utcnow().isoformat()
                )
            else:
                return DeliveryResult(
                    success=False,
                    channel=ChannelType.EMAIL,
                    recipient_id=recipient,
                    message_id=None,
                    error=response.text,
                    timestamp=datetime.utcnow().isoformat()
                )
        
        except Exception as e:
            return DeliveryResult(
                success=False,
                channel=ChannelType.EMAIL,
                recipient_id=recipient,
                message_id=None,
                error=str(e),
                timestamp=datetime.utcnow().isoformat()
            )
    
    async def send_bulk(
        self, 
        content: ChannelContent, 
        recipients: List[str],
        segment: Optional[str] = None
    ) -> List[DeliveryResult]:
        """Send email to segment or list of recipients."""
        
        # For bulk, use ConvertKit broadcast to segment
        try:
            payload = {
                'api_secret': self.config.api_secret,
                'subject': content.subject,
                'content': content.formatted_content,
            }
            
            if segment:
                payload['segment_id'] = segment
            
            response = await self.client.post("/broadcasts", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return [DeliveryResult(
                    success=True,
                    channel=ChannelType.EMAIL,
                    recipient_id=f"segment:{segment}",
                    message_id=data.get('broadcast', {}).get('id'),
                    error=None,
                    timestamp=datetime.utcnow().isoformat()
                )]
            else:
                return [DeliveryResult(
                    success=False,
                    channel=ChannelType.EMAIL,
                    recipient_id=f"segment:{segment}",
                    message_id=None,
                    error=response.text,
                    timestamp=datetime.utcnow().isoformat()
                )]
        
        except Exception as e:
            return [DeliveryResult(
                success=False,
                channel=ChannelType.EMAIL,
                recipient_id=f"segment:{segment}",
                message_id=None,
                error=str(e),
                timestamp=datetime.utcnow().isoformat()
            )]
    
    async def _get_or_create_subscriber(self, email: str) -> dict:
        """Get or create subscriber in ConvertKit."""
        response = await self.client.get(
            f"/subscribers",
            params={'api_secret': self.config.api_secret, 'email_address': email}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('subscribers'):
                return data['subscribers'][0]
        
        # Create new subscriber
        response = await self.client.post(
            f"/subscribers",
            json={
                'api_secret': self.config.api_secret,
                'email_address': email,
            }
        )
        return response.json().get('subscriber', {})
    
    async def tag_subscriber(self, email: str, tag_id: int) -> bool:
        """Add tag to subscriber."""
        response = await self.client.post(
            f"/tags/{tag_id}/subscribe",
            json={
                'api_secret': self.config.api_secret,
                'email': email,
            }
        )
        return response.status_code == 200
```

---

## 4. WhatsApp Channel

### 4.1 WhatsApp Business API Integration

```python
class WhatsAppConfig:
    """WhatsApp Business API configuration."""
    phone_number_id: str
    access_token: str
    base_url: str = "https://graph.facebook.com/v17.0"
    
    # Template IDs (pre-approved by Meta)
    template_ids: dict = {
        'adelaide_daily': 'adelaide_daily_v1',
        'adelaide_weekly': 'adelaide_weekly_v1',
        'adelaide_crisis': 'adelaide_crisis_v1',
    }

class WhatsAppFormatter(ChannelFormatter):
    """Format content for WhatsApp delivery."""
    
    # WhatsApp limits
    MAX_MESSAGE_LENGTH = 4096
    MAX_BUTTONS = 3
    
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format Adelaide content for WhatsApp."""
        
        # WhatsApp uses plain text with limited formatting
        formatted = self._format_for_whatsapp(content)
        
        # Truncate if needed
        if len(formatted) > self.MAX_MESSAGE_LENGTH:
            formatted = self._truncate_with_link(formatted, context)
        
        # Add quick reply buttons
        buttons = self._generate_buttons(context)
        
        return ChannelContent(
            channel=ChannelType.WHATSAPP,
            formatted_content=formatted,
            metadata={
                'template_id': context.get('template_id'),
            },
            size_bytes=len(formatted.encode('utf-8')),
            buttons=buttons
        )
    
    def get_max_length(self) -> int:
        return self.MAX_MESSAGE_LENGTH
    
    def _format_for_whatsapp(self, content: str) -> str:
        """Convert markdown to WhatsApp formatting."""
        import re
        
        text = content
        
        # Convert markdown bold to WhatsApp bold
        text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)
        
        # Convert headers to bold with emoji
        text = re.sub(r'^## (.+)$', r'*\1*', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'*\1*', text, flags=re.MULTILINE)
        
        # Convert tables to simple lists
        text = self._convert_tables_to_lists(text)
        
        # Remove HTML if any
        text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    
    def _convert_tables_to_lists(self, text: str) -> str:
        """Convert markdown tables to WhatsApp-friendly lists."""
        import re
        
        # Find tables
        table_pattern = r'\|(.+)\|[\r\n]+\|[-:| ]+\|[\r\n]+((?:\|.+\|[\r\n]*)+)'
        
        def replace_table(match):
            headers = [h.strip() for h in match.group(1).split('|') if h.strip()]
            rows = match.group(2).strip().split('\n')
            
            result = []
            for row in rows:
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    result.append(' | '.join(cells))
            
            return '\n'.join(result)
        
        return re.sub(table_pattern, replace_table, text)
    
    def _truncate_with_link(self, text: str, context: dict) -> str:
        """Truncate and add link to full version."""
        max_len = self.MAX_MESSAGE_LENGTH - 100  # Reserve space for link
        truncated = text[:max_len]
        
        # Find last sentence
        last_period = truncated.rfind('.')
        if last_period > 0:
            truncated = truncated[:last_period + 1]
        
        link = f"https://diboas.com/adelaide/{context.get('edition_id', '')}"
        truncated += f"\n\nðŸ“– *Read full update:* {link}"
        
        return truncated
    
    def _generate_buttons(self, context: dict) -> List[Dict]:
        """Generate WhatsApp quick reply buttons."""
        edition = context.get('edition_type', 'daily')
        
        if edition == 'crisis':
            return [
                {'type': 'reply', 'reply': {'id': 'view_options', 'title': 'ðŸ“Š View Options'}},
                {'type': 'reply', 'reply': {'id': 'contact_support', 'title': 'ðŸ’¬ Talk to Us'}},
            ]
        else:
            return [
                {'type': 'reply', 'reply': {'id': 'view_portfolio', 'title': 'ðŸ“ˆ My Portfolio'}},
                {'type': 'reply', 'reply': {'id': 'read_more', 'title': 'ðŸ“– Full Report'}},
            ]

class WhatsAppDispatcher(ChannelDispatcher):
    """Dispatch messages via WhatsApp Business API."""
    
    def __init__(self, config: WhatsAppConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={
                'Authorization': f'Bearer {config.access_token}',
                'Content-Type': 'application/json',
            }
        )
    
    async def send(self, content: ChannelContent, recipient: str) -> DeliveryResult:
        """Send WhatsApp message to single recipient."""
        try:
            payload = {
                'messaging_product': 'whatsapp',
                'to': recipient,
                'type': 'text',
                'text': {'body': content.formatted_content}
            }
            
            # Add buttons if present
            if content.buttons:
                payload['type'] = 'interactive'
                payload['interactive'] = {
                    'type': 'button',
                    'body': {'text': content.formatted_content},
                    'action': {'buttons': content.buttons}
                }
            
            response = await self.client.post(
                f"/{self.config.phone_number_id}/messages",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return DeliveryResult(
                    success=True,
                    channel=ChannelType.WHATSAPP,
                    recipient_id=recipient,
                    message_id=data.get('messages', [{}])[0].get('id'),
                    error=None,
                    timestamp=datetime.utcnow().isoformat()
                )
            else:
                return DeliveryResult(
                    success=False,
                    channel=ChannelType.WHATSAPP,
                    recipient_id=recipient,
                    message_id=None,
                    error=response.text,
                    timestamp=datetime.utcnow().isoformat()
                )
        
        except Exception as e:
            return DeliveryResult(
                success=False,
                channel=ChannelType.WHATSAPP,
                recipient_id=recipient,
                message_id=None,
                error=str(e),
                timestamp=datetime.utcnow().isoformat()
            )
    
    async def send_bulk(self, content: ChannelContent, recipients: List[str]) -> List[DeliveryResult]:
        """Send WhatsApp message to multiple recipients."""
        # WhatsApp requires individual sends
        import asyncio
        tasks = [self.send(content, r) for r in recipients]
        return await asyncio.gather(*tasks)
```

---

## 5. Telegram Channel

### 5.1 Telegram Bot Integration

```python
class TelegramConfig:
    """Telegram Bot configuration."""
    bot_token: str
    channel_id: str  # @diboas_adelaide
    base_url: str = "https://api.telegram.org"

class TelegramFormatter(ChannelFormatter):
    """Format content for Telegram delivery."""
    
    MAX_MESSAGE_LENGTH = 4096
    
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format Adelaide content for Telegram."""
        
        # Telegram supports HTML or Markdown
        formatted = self._format_for_telegram(content)
        
        # Truncate if needed
        if len(formatted) > self.MAX_MESSAGE_LENGTH:
            formatted = self._truncate(formatted)
        
        return ChannelContent(
            channel=ChannelType.TELEGRAM,
            formatted_content=formatted,
            metadata={
                'parse_mode': 'HTML',
            },
            size_bytes=len(formatted.encode('utf-8'))
        )
    
    def get_max_length(self) -> int:
        return self.MAX_MESSAGE_LENGTH
    
    def _format_for_telegram(self, content: str) -> str:
        """Convert markdown to Telegram HTML."""
        import re
        
        text = content
        
        # Convert bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Convert italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        # Convert headers to bold
        text = re.sub(r'^## (.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
        
        # Convert links
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Convert code blocks
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        return text.strip()
    
    def _truncate(self, text: str) -> str:
        """Truncate to max length."""
        if len(text) <= self.MAX_MESSAGE_LENGTH:
            return text
        
        truncated = text[:self.MAX_MESSAGE_LENGTH - 50]
        last_newline = truncated.rfind('\n')
        if last_newline > 0:
            truncated = truncated[:last_newline]
        
        return truncated + '\n\n<i>...continued in next message</i>'

class TelegramDispatcher(ChannelDispatcher):
    """Dispatch messages via Telegram Bot API."""
    
    def __init__(self, config: TelegramConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=f"{config.base_url}/bot{config.bot_token}"
        )
    
    async def send(self, content: ChannelContent, recipient: str) -> DeliveryResult:
        """Send Telegram message."""
        try:
            response = await self.client.post(
                "/sendMessage",
                json={
                    'chat_id': recipient,
                    'text': content.formatted_content,
                    'parse_mode': content.metadata.get('parse_mode', 'HTML'),
                    'disable_web_page_preview': False,
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return DeliveryResult(
                    success=True,
                    channel=ChannelType.TELEGRAM,
                    recipient_id=recipient,
                    message_id=str(data.get('result', {}).get('message_id')),
                    error=None,
                    timestamp=datetime.utcnow().isoformat()
                )
            else:
                return DeliveryResult(
                    success=False,
                    channel=ChannelType.TELEGRAM,
                    recipient_id=recipient,
                    message_id=None,
                    error=response.text,
                    timestamp=datetime.utcnow().isoformat()
                )
        
        except Exception as e:
            return DeliveryResult(
                success=False,
                channel=ChannelType.TELEGRAM,
                recipient_id=recipient,
                message_id=None,
                error=str(e),
                timestamp=datetime.utcnow().isoformat()
            )
    
    async def send_to_channel(self, content: ChannelContent) -> DeliveryResult:
        """Send to public Telegram channel."""
        return await self.send(content, self.config.channel_id)
    
    async def send_bulk(self, content: ChannelContent, recipients: List[str]) -> List[DeliveryResult]:
        """Send to multiple chat IDs."""
        import asyncio
        tasks = [self.send(content, r) for r in recipients]
        return await asyncio.gather(*tasks)
```

---

## 6. SMS Channel

### 6.1 SMS Integration (Twilio)

```python
class SMSFormatter(ChannelFormatter):
    """Format content for SMS delivery."""
    
    MAX_LENGTH = 160  # Single SMS
    MAX_CONCAT = 480  # 3 concatenated SMS
    
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format Adelaide content for SMS."""
        
        # SMS needs extreme brevity
        formatted = self._compress_for_sms(content, context)
        
        return ChannelContent(
            channel=ChannelType.SMS,
            formatted_content=formatted,
            metadata={
                'segments': self._count_segments(formatted),
            },
            size_bytes=len(formatted.encode('utf-8'))
        )
    
    def get_max_length(self) -> int:
        return self.MAX_CONCAT
    
    def _compress_for_sms(self, content: str, context: dict) -> str:
        """Compress Adelaide to SMS-friendly format."""
        
        # Extract only critical info
        edition = context.get('edition_type', 'daily')
        
        if edition == 'crisis':
            # Crisis gets priority content
            return self._crisis_sms(context)
        else:
            return self._daily_sms(context)
    
    def _daily_sms(self, context: dict) -> str:
        """Generate daily SMS summary."""
        market = context.get('market_data', {})
        
        btc = market.get('btc_change_24h', 0)
        btc_emoji = 'ðŸ“ˆ' if btc >= 0 else 'ðŸ“‰'
        
        return f"Adelaide Daily: BTC {btc_emoji}{btc:+.1f}% | Your strategies: On track | diboas.com/app"
    
    def _crisis_sms(self, context: dict) -> str:
        """Generate crisis SMS alert."""
        level = context.get('crisis_level', 1)
        
        if level >= 3:
            return f"âš ï¸ Adelaide Alert: Market volatility. Check app for details. Your funds are safe. diboas.com/app"
        else:
            return f"ðŸ“Š Adelaide: Market update available. diboas.com/app"
    
    def _count_segments(self, text: str) -> int:
        """Count SMS segments."""
        length = len(text)
        if length <= 160:
            return 1
        elif length <= 306:
            return 2
        else:
            return 3
```

---

## 7. Push Notifications

### 7.1 Push Integration (Firebase/OneSignal)

```python
class PushFormatter(ChannelFormatter):
    """Format content for push notifications."""
    
    MAX_TITLE = 65
    MAX_BODY = 240
    
    def format(self, content: str, context: dict) -> ChannelContent:
        """Format Adelaide content for push notification."""
        
        title = self._generate_title(context)
        body = self._generate_body(content, context)
        
        return ChannelContent(
            channel=ChannelType.PUSH,
            formatted_content=body,
            metadata={
                'title': title,
                'data': context.get('push_data', {}),
            },
            size_bytes=len(body.encode('utf-8')),
            subject=title
        )
    
    def get_max_length(self) -> int:
        return self.MAX_BODY
    
    def _generate_title(self, context: dict) -> str:
        """Generate push notification title."""
        edition = context.get('edition_type', 'daily')
        
        titles = {
            'daily': "ðŸ“Š Adelaide Daily",
            'weekly': "ðŸ“ˆ Adelaide Weekly",
            'crisis': "âš ï¸ Market Alert",
        }
        
        return titles.get(edition, "Adelaide Update")[:self.MAX_TITLE]
    
    def _generate_body(self, content: str, context: dict) -> str:
        """Generate push notification body."""
        # Extract first meaningful sentence
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#') and not line.startswith('|'):
                body = line.strip()[:self.MAX_BODY]
                if len(line) > self.MAX_BODY:
                    body = body[:self.MAX_BODY-3] + '...'
                return body
        
        return "Your daily market update is ready."
```

---

## 8. Distribution Orchestrator

### 8.1 Main Orchestrator

```python
class DistributionOrchestrator:
    """Orchestrate content delivery across all channels."""
    
    def __init__(self, config: dict):
        self.channels = {}
        self._init_channels(config)
    
    def _init_channels(self, config: dict):
        """Initialize all channel formatters and dispatchers."""
        
        # Email (always enabled)
        self.channels[ChannelType.EMAIL] = {
            'formatter': EmailFormatter(config['templates_dir']),
            'dispatcher': ConvertKitDispatcher(config['convertkit']),
            'enabled': True,
        }
        
        # WhatsApp (if configured)
        if config.get('whatsapp'):
            self.channels[ChannelType.WHATSAPP] = {
                'formatter': WhatsAppFormatter(),
                'dispatcher': WhatsAppDispatcher(config['whatsapp']),
                'enabled': config['whatsapp'].get('enabled', False),
            }
        
        # Telegram (if configured)
        if config.get('telegram'):
            self.channels[ChannelType.TELEGRAM] = {
                'formatter': TelegramFormatter(),
                'dispatcher': TelegramDispatcher(config['telegram']),
                'enabled': config['telegram'].get('enabled', False),
            }
        
        # SMS (if configured)
        if config.get('twilio'):
            self.channels[ChannelType.SMS] = {
                'formatter': SMSFormatter(),
                'dispatcher': TwilioDispatcher(config['twilio']),
                'enabled': config['twilio'].get('enabled', False),
            }
        
        # Push (if configured)
        if config.get('push'):
            self.channels[ChannelType.PUSH] = {
                'formatter': PushFormatter(),
                'dispatcher': PushDispatcher(config['push']),
                'enabled': config['push'].get('enabled', False),
            }
    
    async def distribute(
        self,
        content: str,
        context: dict,
        user_preferences: dict
    ) -> Dict[ChannelType, DeliveryResult]:
        """
        Distribute content to all user's preferred channels.
        
        Args:
            content: Assembled Adelaide content
            context: Context including edition_type, locale, etc.
            user_preferences: User's channel preferences and IDs
        
        Returns:
            Dict of channel -> delivery result
        """
        results = {}
        
        for channel_type, channel_config in self.channels.items():
            # Skip disabled channels
            if not channel_config['enabled']:
                continue
            
            # Skip if user hasn't enabled this channel
            if not user_preferences.get(f'{channel_type.value}_enabled', False):
                continue
            
            # Format content for channel
            formatter = channel_config['formatter']
            formatted = formatter.format(content, context)
            
            # Get recipient ID for this channel
            recipient = user_preferences.get(f'{channel_type.value}_id')
            if not recipient:
                continue
            
            # Dispatch
            dispatcher = channel_config['dispatcher']
            result = await dispatcher.send(formatted, recipient)
            results[channel_type] = result
        
        return results
    
    async def broadcast(
        self,
        content: str,
        context: dict,
        channel: ChannelType,
        segment: Optional[str] = None
    ) -> List[DeliveryResult]:
        """
        Broadcast content to a segment via specific channel.
        
        Used for Adelaide Daily to all subscribers.
        """
        if channel not in self.channels:
            raise ValueError(f"Channel {channel} not configured")
        
        channel_config = self.channels[channel]
        
        # Format
        formatted = channel_config['formatter'].format(content, context)
        
        # Broadcast
        dispatcher = channel_config['dispatcher']
        if hasattr(dispatcher, 'send_bulk'):
            return await dispatcher.send_bulk(formatted, [], segment=segment)
        
        raise ValueError(f"Channel {channel} doesn't support bulk send")
```

---

## 9. Configuration

```yaml
# config/distribution.yaml

distribution:
  # Email (ConvertKit)
  convertkit:
    enabled: true
    api_key: "${CONVERTKIT_API_KEY}"
    api_secret: "${CONVERTKIT_API_SECRET}"
    sequences:
      adelaide_daily: 12345
      adelaide_weekly: 12346
    segments:
      all_users: "segment_all"
      ana_users: "segment_ana"
      maria_users: "segment_maria"
      felipe_users: "segment_felipe"
      locale_en: "segment_en"
      locale_pt_br: "segment_pt_br"
  
  # WhatsApp
  whatsapp:
    enabled: false  # Phase 2
    phone_number_id: "${WHATSAPP_PHONE_ID}"
    access_token: "${WHATSAPP_TOKEN}"
    templates:
      adelaide_daily: "adelaide_daily_v1"
      adelaide_crisis: "adelaide_crisis_v1"
  
  # Telegram
  telegram:
    enabled: false  # Phase 2
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    channel_id: "@diboas_adelaide"
  
  # SMS (Twilio)
  twilio:
    enabled: false  # Phase 3
    account_sid: "${TWILIO_SID}"
    auth_token: "${TWILIO_TOKEN}"
    from_number: "+1234567890"
  
  # Push Notifications
  push:
    enabled: false  # Phase 3
    provider: "firebase"  # or "onesignal"
    firebase_credentials: "${FIREBASE_CREDS}"
  
  # Delivery settings
  delivery:
    retry_attempts: 3
    retry_delay_seconds: 5
    batch_size: 100
    rate_limit_per_second: 50
```

---

## 10. Testing Requirements

### 10.1 Unit Tests

```python
class TestEmailFormatter:
    def test_html_generation(self):
        """Test HTML email is generated correctly."""
        # ... implementation
    
    def test_subject_localization(self):
        """Test subject lines are localized."""
        # ... implementation

class TestWhatsAppFormatter:
    def test_truncation(self):
        """Test content is truncated for WhatsApp limits."""
        # ... implementation
    
    def test_button_generation(self):
        """Test quick reply buttons are generated."""
        # ... implementation

class TestDistributionOrchestrator:
    def test_respects_user_preferences(self):
        """Test only preferred channels are used."""
        # ... implementation
```

---

## 11. Implementation Checklist

### Phase 1 (Launch)
- [ ] EmailFormatter implemented
- [ ] ConvertKitDispatcher working
- [ ] Segment-based broadcasting working
- [ ] Unsubscribe handling compliant

### Phase 2
- [ ] WhatsAppFormatter implemented
- [ ] WhatsApp Business API integrated
- [ ] TelegramFormatter implemented
- [ ] Telegram Bot working
- [ ] SubstackFormatter implemented

### Phase 3
- [ ] SMSFormatter implemented
- [ ] Twilio integration working
- [ ] PushFormatter implemented
- [ ] Firebase/OneSignal integrated
- [ ] DistributionOrchestrator complete

---

**Document End**

**Next:** CMO_04_LOCALIZATION_PIPELINE.md
