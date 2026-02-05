# CMO_04: Localization Pipeline
## Multi-Language Support Specification

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P0 (EN + PT-BR for Launch; DE + ES Phase 2)

---

## 1. Purpose

The Localization Pipeline ensures Adelaide content is properly adapted for each supported language and region, including tone adjustments, cultural context, and regulatory requirements.

### Supported Locales

| Locale | Language | Region | Priority | Launch Phase |
|--------|----------|--------|----------|--------------|
| **en** | English | Global | P0 | Phase 1 |
| **pt-br** | Portuguese | Brazil | P0 | Phase 1 |
| **de** | German | DACH | P1 | Phase 2 |
| **es** | Spanish | LATAM/Spain | P1 | Phase 2 |

---

## 2. Localization Architecture

### 2.1 Pipeline Flow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      LOCALIZATION PIPELINE                                  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚  Assembled Content (EN default)                                             â”‚
â”‚           â”‚                                                                 â”‚
â”‚           â–¼                                                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              LOCALE ROUTER                                           â”‚   â”‚
â”‚  â”‚  Determine user's locale â†’ Route to appropriate localizer            â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚           â”‚                                                                 â”‚
â”‚     â”Œâ”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                                      â”‚
â”‚     â”‚     â”‚     â”‚         â”‚         â”‚                                      â”‚
â”‚     â–¼     â–¼     â–¼         â–¼         â–¼                                      â”‚
â”‚   [EN]  [PT-BR] [DE]     [ES]   [Fallback]                                 â”‚
â”‚     â”‚     â”‚     â”‚         â”‚         â”‚                                      â”‚
â”‚     â–¼     â–¼     â–¼         â–¼         â–¼                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              TONE ADAPTER                                            â”‚   â”‚
â”‚  â”‚  Adjust tone per locale (formal/informal, grandmother voice)         â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚           â”‚                                                                 â”‚
â”‚           â–¼                                                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              CULTURAL ADAPTER                                        â”‚   â”‚
â”‚  â”‚  Date/number formats, currency, cultural references                  â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚           â”‚                                                                 â”‚
â”‚           â–¼                                                                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚              REGULATORY ADAPTER                                      â”‚   â”‚
â”‚  â”‚  Add jurisdiction-specific disclaimers and warnings                  â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚           â”‚                                                                 â”‚
â”‚           â–¼                                                                 â”‚
â”‚  Localized Content                                                          â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 3. Locale Configuration

### 3.1 Locale Profiles

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class LocaleProfile:
    """Complete locale configuration."""
    code: str  # 'en', 'pt-br', 'de', 'es'
    language: str
    region: str
    
    # Formatting
    date_format: str
    time_format: str
    number_decimal: str
    number_thousands: str
    currency_symbol: str
    currency_position: str  # 'before' or 'after'
    
    # Tone
    formality: str  # 'formal', 'informal', 'balanced'
    grandmother_voice: str  # Strength of Adelaide's grandmother persona
    emoji_preference: str  # 'heavy', 'moderate', 'minimal'
    
    # Cultural
    greeting_time_based: bool  # Different greetings for morning/evening
    cultural_references: List[str]  # Allowed cultural references
    
    # Regulatory
    jurisdiction: str  # 'EU', 'BR', 'US', etc.
    required_disclaimers: List[str]

LOCALE_PROFILES = {
    'en': LocaleProfile(
        code='en',
        language='English',
        region='Global',
        date_format='%B %d, %Y',  # January 23, 2026
        time_format='%I:%M %p',   # 07:00 AM
        number_decimal='.',
        number_thousands=',',
        currency_symbol='$',
        currency_position='before',
        formality='balanced',
        grandmother_voice='moderate',
        emoji_preference='moderate',
        greeting_time_based=True,
        cultural_references=['global'],
        jurisdiction='EU',  # Default to EU
        required_disclaimers=['past_performance', 'capital_risk']
    ),
    'pt-br': LocaleProfile(
        code='pt-br',
        language='Portuguese',
        region='Brazil',
        date_format='%d de %B de %Y',  # 23 de Janeiro de 2026
        time_format='%H:%M',           # 07:00
        number_decimal=',',
        number_thousands='.',
        currency_symbol='R$',
        currency_position='before',
        formality='informal',  # Brazilian Portuguese is warmer
        grandmother_voice='strong',  # Grandmother voice strongest here
        emoji_preference='heavy',
        greeting_time_based=True,
        cultural_references=['brazil', 'latin_america'],
        jurisdiction='BR',
        required_disclaimers=['rentabilidade_passada', 'riscos_investimento']
    ),
    'de': LocaleProfile(
        code='de',
        language='German',
        region='DACH',
        date_format='%d. %B %Y',  # 23. Januar 2026
        time_format='%H:%M Uhr',  # 07:00 Uhr
        number_decimal=',',
        number_thousands='.',
        currency_symbol='â‚¬',
        currency_position='after',
        formality='formal',  # German is more formal
        grandmother_voice='moderate',
        emoji_preference='minimal',  # Germans prefer less emojis in finance
        greeting_time_based=True,
        cultural_references=['dach', 'europe'],
        jurisdiction='EU',
        required_disclaimers=['past_performance', 'capital_risk', 'mifid']
    ),
    'es': LocaleProfile(
        code='es',
        language='Spanish',
        region='LATAM/Spain',
        date_format='%d de %B de %Y',  # 23 de Enero de 2026
        time_format='%H:%M',            # 07:00
        number_decimal=',',
        number_thousands='.',
        currency_symbol='â‚¬',  # Default to Euro
        currency_position='after',
        formality='balanced',
        grandmother_voice='moderate',
        emoji_preference='moderate',
        greeting_time_based=True,
        cultural_references=['spain', 'latin_america'],
        jurisdiction='EU',  # Default to EU (Spain)
        required_disclaimers=['past_performance', 'capital_risk']
    ),
}
```

---

## 4. Translation System

### 4.1 Static Translations (i18n)

```python
# Structured translations for static UI elements and common phrases

TRANSLATIONS = {
    'greetings': {
        'en': {
            'morning': "Good morning!",
            'afternoon': "Good afternoon!",
            'evening': "Good evening!",
            'generic': "Hello!",
        },
        'pt-br': {
            'morning': "Bom dia!",
            'afternoon': "Boa tarde!",
            'evening': "Boa noite!",
            'generic': "OlÃ¡!",
        },
        'de': {
            'morning': "Guten Morgen!",
            'afternoon': "Guten Tag!",
            'evening': "Guten Abend!",
            'generic': "Hallo!",
        },
        'es': {
            'morning': "Â¡Buenos dÃ­as!",
            'afternoon': "Â¡Buenas tardes!",
            'evening': "Â¡Buenas noches!",
            'generic': "Â¡Hola!",
        },
    },
    'section_headers': {
        'en': {
            'market_snapshot': "ðŸ“Š Market Snapshot",
            'whale_watch': "ðŸ‹ Whale Watch",
            'your_strategies': "ðŸ“ˆ Your Strategies",
            'adelaide_insight': "ðŸ’¡ Adelaide's Insight",
            'estate_watch': "âš ï¸ Estate Watch",
        },
        'pt-br': {
            'market_snapshot': "ðŸ“Š Resumo do Mercado",
            'whale_watch': "ðŸ‹ ObservaÃ§Ã£o de Baleias",
            'your_strategies': "ðŸ“ˆ Suas EstratÃ©gias",
            'adelaide_insight': "ðŸ’¡ Conselho da Adelaide",
            'estate_watch': "âš ï¸ Alerta de PatrimÃ´nios",
        },
        'de': {
            'market_snapshot': "ðŸ“Š MarktÃ¼bersicht",
            'whale_watch': "ðŸ‹ Wal-Beobachtung",
            'your_strategies': "ðŸ“ˆ Ihre Strategien",
            'adelaide_insight': "ðŸ’¡ Adelaides Einblick",
            'estate_watch': "âš ï¸ Estate-Warnung",
        },
        'es': {
            'market_snapshot': "ðŸ“Š Resumen del Mercado",
            'whale_watch': "ðŸ‹ Vigilancia de Ballenas",
            'your_strategies': "ðŸ“ˆ Tus Estrategias",
            'adelaide_insight': "ðŸ’¡ Consejo de Adelaide",
            'estate_watch': "âš ï¸ Alerta de Patrimonio",
        },
    },
    'common_phrases': {
        'en': {
            'while_you_slept': "Here's what happened while you slept.",
            'your_money_is_safe': "Your funds are safe.",
            'no_action_needed': "No action needed from you.",
            'consider_your_options': "Consider your options.",
            'read_more': "Read more",
            'unsubscribe': "Unsubscribe",
        },
        'pt-br': {
            'while_you_slept': "Aqui estÃ¡ o que aconteceu enquanto vocÃª dormia.",
            'your_money_is_safe': "Seu dinheiro estÃ¡ seguro.",
            'no_action_needed': "Nenhuma aÃ§Ã£o necessÃ¡ria.",
            'consider_your_options': "Considere suas opÃ§Ãµes.",
            'read_more': "Leia mais",
            'unsubscribe': "Cancelar inscriÃ§Ã£o",
        },
        'de': {
            'while_you_slept': "Das ist passiert, wÃ¤hrend Sie geschlafen haben.",
            'your_money_is_safe': "Ihr Geld ist sicher.",
            'no_action_needed': "Keine Handlung erforderlich.",
            'consider_your_options': "Betrachten Sie Ihre Optionen.",
            'read_more': "Mehr lesen",
            'unsubscribe': "Abmelden",
        },
        'es': {
            'while_you_slept': "Esto es lo que pasÃ³ mientras dormÃ­as.",
            'your_money_is_safe': "Tu dinero estÃ¡ seguro.",
            'no_action_needed': "No se necesita ninguna acciÃ³n.",
            'consider_your_options': "Considera tus opciones.",
            'read_more': "Leer mÃ¡s",
            'unsubscribe': "Cancelar suscripciÃ³n",
        },
    },
}
```

### 4.2 Dynamic Content Localization

```python
from datetime import datetime
from typing import Dict, Optional

class ContentLocalizer:
    """Localize dynamic Adelaide content."""
    
    def __init__(self, locale: str):
        self.locale = locale
        self.profile = LOCALE_PROFILES.get(locale, LOCALE_PROFILES['en'])
        self.translations = TRANSLATIONS
    
    def localize(self, content: str, context: dict) -> str:
        """
        Localize content for this locale.
        
        Steps:
        1. Replace translation keys
        2. Format dates and numbers
        3. Adapt tone
        4. Add cultural context
        5. Add regulatory requirements
        """
        
        # Step 1: Replace translation keys
        content = self._replace_translations(content)
        
        # Step 2: Format dates and numbers
        content = self._format_dates(content, context)
        content = self._format_numbers(content)
        content = self._format_currency(content)
        
        # Step 3: Adapt tone
        content = self._adapt_tone(content)
        
        # Step 4: Cultural adaptation
        content = self._adapt_cultural(content, context)
        
        # Step 5: Regulatory requirements
        content = self._add_regulatory(content)
        
        return content
    
    def _replace_translations(self, content: str) -> str:
        """Replace {{t:key}} placeholders with translations."""
        import re
        
        def replace_match(match):
            key_path = match.group(1).split('.')
            trans = self.translations
            
            for key in key_path:
                if isinstance(trans, dict):
                    trans = trans.get(key, {})
                else:
                    return match.group(0)  # Return original if not found
            
            if isinstance(trans, dict):
                return trans.get(self.locale, trans.get('en', match.group(0)))
            return str(trans)
        
        return re.sub(r'\{\{t:([a-z_.]+)\}\}', replace_match, content)
    
    def _format_dates(self, content: str, context: dict) -> str:
        """Format dates according to locale."""
        import re
        from datetime import datetime
        
        # Format main date
        if 'date' in context:
            date_obj = context['date']
            if isinstance(date_obj, str):
                date_obj = datetime.fromisoformat(date_obj)
            
            formatted_date = self._format_date(date_obj)
            content = content.replace('{DATE}', formatted_date)
        
        # Format any ISO dates in content
        def replace_iso_date(match):
            try:
                dt = datetime.fromisoformat(match.group(1))
                return self._format_date(dt)
            except:
                return match.group(0)
        
        content = re.sub(r'\{date:(\d{4}-\d{2}-\d{2})\}', replace_iso_date, content)
        
        return content
    
    def _format_date(self, dt: datetime) -> str:
        """Format a date according to locale."""
        # Month names per locale
        months = {
            'en': ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'],
            'pt-br': ['Janeiro', 'Fevereiro', 'MarÃ§o', 'Abril', 'Maio', 'Junho',
                      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            'de': ['Januar', 'Februar', 'MÃ¤rz', 'April', 'Mai', 'Juni',
                   'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
            'es': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        }
        
        month_name = months.get(self.locale, months['en'])[dt.month - 1]
        
        format_str = self.profile.date_format
        format_str = format_str.replace('%B', month_name)
        
        return dt.strftime(format_str).replace('%B', month_name)
    
    def _format_numbers(self, content: str) -> str:
        """Format numbers according to locale."""
        import re
        
        def format_number(match):
            num_str = match.group(0)
            try:
                num = float(num_str.replace(',', ''))
                
                # Format with locale separators
                if num == int(num):
                    formatted = f"{int(num):,}"
                else:
                    formatted = f"{num:,.2f}"
                
                # Replace separators
                if self.profile.number_decimal == ',':
                    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
                
                return formatted
            except:
                return num_str
        
        # Match numbers (but not percentages which have their own format)
        return re.sub(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![%])', format_number, content)
    
    def _format_currency(self, content: str) -> str:
        """Format currency according to locale."""
        import re
        
        def format_currency_match(match):
            symbol = match.group(1)
            amount = match.group(2)
            
            # Use locale's currency symbol
            local_symbol = self.profile.currency_symbol
            
            if self.profile.currency_position == 'after':
                return f"{amount} {local_symbol}"
            else:
                return f"{local_symbol}{amount}"
        
        # Match $123.45 or â‚¬123,45 patterns
        return re.sub(r'([$â‚¬Â£R\$])\s*(\d+[.,]?\d*)', format_currency_match, content)
    
    def _adapt_tone(self, content: str) -> str:
        """Adapt tone according to locale profile."""
        
        if self.profile.formality == 'formal':
            content = self._formalize(content)
        elif self.profile.formality == 'informal':
            content = self._informalize(content)
        
        if self.profile.grandmother_voice == 'strong':
            content = self._strengthen_grandmother_voice(content)
        
        return content
    
    def _formalize(self, content: str) -> str:
        """Make content more formal (German)."""
        if self.locale == 'de':
            # Use formal "Sie" instead of informal "du"
            content = content.replace(' du ', ' Sie ')
            content = content.replace(' dein ', ' Ihr ')
            content = content.replace(' deine ', ' Ihre ')
        return content
    
    def _informalize(self, content: str) -> str:
        """Make content more informal (Brazilian Portuguese)."""
        if self.locale == 'pt-br':
            # Brazilian Portuguese is naturally warmer
            # Add personal touches
            replacements = {
                'Prezado usuÃ¡rio': 'Oi!',
                'Caro cliente': 'OlÃ¡!',
            }
            for formal, informal in replacements.items():
                content = content.replace(formal, informal)
        return content
    
    def _strengthen_grandmother_voice(self, content: str) -> str:
        """Strengthen Adelaide's grandmother voice for Brazilian Portuguese."""
        if self.locale == 'pt-br':
            # Add characteristic grandmother phrases
            grandmother_phrases = {
                'O mercado caiu': 'Olha, o mercado caiu um pouquinho',
                'Considere': 'Pense com calma sobre',
                'recomendamos': 'a vovÃ³ sugere',
            }
            for standard, grandmother in grandmother_phrases.items():
                content = content.replace(standard, grandmother)
        return content
    
    def _adapt_cultural(self, content: str, context: dict) -> str:
        """Adapt cultural references."""
        # Remove or adapt culturally inappropriate references
        # This is a placeholder for more complex cultural adaptation
        return content
    
    def _add_regulatory(self, content: str) -> str:
        """Add jurisdiction-specific regulatory requirements."""
        # Disclaimers are added at the template level
        # This adds any inline regulatory requirements
        
        if self.profile.jurisdiction == 'BR':
            # CVM compliance notes
            content = self._add_cvm_compliance(content)
        elif self.profile.jurisdiction == 'EU':
            # MiCA compliance notes
            content = self._add_mica_compliance(content)
        
        return content
    
    def _add_cvm_compliance(self, content: str) -> str:
        """Add CVM compliance for Brazil."""
        # Brazilian securities regulator requirements
        return content
    
    def _add_mica_compliance(self, content: str) -> str:
        """Add MiCA compliance for EU."""
        # EU crypto regulation requirements
        return content
```

---

## 5. Grandmother Voice Templates

### 5.1 Voice Calibration by Locale

```python
GRANDMOTHER_VOICE_TEMPLATES = {
    'en': {
        'market_down_calm': """
The market dipped today. That's normal â€” like the weather, it changes. 
Your grandmother would say: "Don't check your garden every hour. Let it grow."
Your strategies are designed for the long haul.
""",
        'market_up_celebrate': """
Good news today! The market is up, and so is your balance.
But remember what grandma always said: "Don't count your chickens before they hatch."
Stay steady.
""",
        'exit_with_dignity': """
If you need to take your money out, that's okay. Life comes first.
There's no shame in it. Your grandmother would understand.
""",
    },
    
    'pt-br': {
        'market_down_calm': """
O mercado caiu um pouquinho hoje. Isso Ã© normal â€” igual o tempo, muda todo dia.
Sua avÃ³ diria: "NÃ£o fica olhando a planta toda hora. Deixa ela crescer."
Suas estratÃ©gias foram feitas pra longo prazo.
""",
        'market_up_celebrate': """
Boas notÃ­cias hoje! O mercado subiu, e seu saldo tambÃ©m.
Mas lembra o que a vovÃ³ sempre dizia: "NÃ£o conta com o ovo dentro da galinha."
MantÃ©m a calma.
""",
        'exit_with_dignity': """
Se vocÃª precisa tirar seu dinheiro, tudo bem. A vida vem primeiro.
NÃ£o tem vergonha nisso. Sua avÃ³ entenderia.
""",
    },
    
    'de': {
        'market_down_calm': """
Der Markt ist heute etwas gefallen. Das ist normal â€” wie das Wetter, es Ã¤ndert sich.
Ihre GroÃŸmutter wÃ¼rde sagen: "Schau nicht jede Stunde in deinen Garten. Lass ihn wachsen."
Ihre Strategien sind fÃ¼r die lange Sicht konzipiert.
""",
        'market_up_celebrate': """
Gute Nachrichten heute! Der Markt ist gestiegen, und Ihr Guthaben auch.
Aber denken Sie daran, was GroÃŸmutter immer sagte: "Man soll den Tag nicht vor dem Abend loben."
Bleiben Sie besonnen.
""",
        'exit_with_dignity': """
Wenn Sie Ihr Geld abheben mÃ¼ssen, ist das in Ordnung. Das Leben geht vor.
Daran ist nichts Verwerfliches. Ihre GroÃŸmutter wÃ¼rde das verstehen.
""",
    },
    
    'es': {
        'market_down_calm': """
El mercado bajÃ³ un poco hoy. Es normal â€” como el clima, cambia.
Tu abuela dirÃ­a: "No revises tu jardÃ­n cada hora. DÃ©jalo crecer."
Tus estrategias estÃ¡n diseÃ±adas para el largo plazo.
""",
        'market_up_celebrate': """
Â¡Buenas noticias hoy! El mercado subiÃ³, y tu saldo tambiÃ©n.
Pero recuerda lo que la abuela siempre decÃ­a: "No vendas la piel del oso antes de cazarlo."
MantÃ©n la calma.
""",
        'exit_with_dignity': """
Si necesitas retirar tu dinero, estÃ¡ bien. La vida es primero.
No hay vergÃ¼enza en eso. Tu abuela lo entenderÃ­a.
""",
    },
}
```

---

## 6. Disclaimer Templates

### 6.1 Localized Disclaimers

```python
DISCLAIMER_TEMPLATES = {
    'en': {
        'standard': """
---

**Disclaimer:** This content is for educational purposes only and does not constitute financial advice. 
Past performance does not guarantee future results. Your capital is at risk. 
Consult a licensed financial advisor before making investment decisions.

diBoaS is not responsible for investment decisions made based on this content.
""",
        'crisis': """
---

**âš ï¸ Important Notice:** Market conditions are volatile. This update is for informational purposes only.
Do not make financial decisions based solely on this message. Your funds remain accessible.
Past performance does not guarantee future results. Consult a financial advisor.
""",
    },
    
    'pt-br': {
        'standard': """
---

**Aviso:** Este conteÃºdo Ã© apenas para fins educacionais e nÃ£o constitui aconselhamento financeiro.
Rentabilidade passada nÃ£o Ã© garantia de rentabilidade futura. Investimentos envolvem riscos.
Consulte um consultor financeiro licenciado antes de tomar decisÃµes de investimento.

A diBoaS nÃ£o se responsabiliza por decisÃµes de investimento baseadas neste conteÃºdo.
""",
        'crisis': """
---

**âš ï¸ Aviso Importante:** O mercado estÃ¡ volÃ¡til. Esta atualizaÃ§Ã£o Ã© apenas informativa.
NÃ£o tome decisÃµes financeiras baseadas apenas nesta mensagem. Seus fundos continuam acessÃ­veis.
Rentabilidade passada nÃ£o Ã© garantia de rentabilidade futura. Consulte um consultor financeiro.
""",
    },
    
    'de': {
        'standard': """
---

**Haftungsausschluss:** Dieser Inhalt dient nur zu Bildungszwecken und stellt keine Finanzberatung dar.
Die Wertentwicklung der Vergangenheit ist keine Garantie fÃ¼r zukÃ¼nftige Ergebnisse. Ihr Kapital ist gefÃ¤hrdet.
Konsultieren Sie einen lizenzierten Finanzberater, bevor Sie Anlageentscheidungen treffen.

diBoaS haftet nicht fÃ¼r Anlageentscheidungen, die auf diesem Inhalt basieren.
""",
        'crisis': """
---

**âš ï¸ Wichtiger Hinweis:** Die Marktbedingungen sind volatil. Dieses Update dient nur zu Informationszwecken.
Treffen Sie keine finanziellen Entscheidungen allein auf Grundlage dieser Nachricht.
Die Wertentwicklung der Vergangenheit ist keine Garantie fÃ¼r zukÃ¼nftige Ergebnisse.
""",
    },
    
    'es': {
        'standard': """
---

**Descargo de responsabilidad:** Este contenido es solo para fines educativos y no constituye asesoramiento financiero.
El rendimiento pasado no garantiza resultados futuros. Su capital estÃ¡ en riesgo.
Consulte a un asesor financiero autorizado antes de tomar decisiones de inversiÃ³n.

diBoaS no es responsable de las decisiones de inversiÃ³n basadas en este contenido.
""",
        'crisis': """
---

**âš ï¸ Aviso Importante:** Las condiciones del mercado son volÃ¡tiles. Esta actualizaciÃ³n es solo informativa.
No tome decisiones financieras basÃ¡ndose Ãºnicamente en este mensaje. Sus fondos siguen accesibles.
El rendimiento pasado no garantiza resultados futuros. Consulte a un asesor financiero.
""",
    },
}
```

---

## 7. Configuration

```yaml
# config/localization.yaml

localization:
  # Supported locales
  supported_locales:
    - en
    - pt-br
    - de
    - es
  
  # Default locale (fallback)
  default_locale: en
  
  # Locale detection priority
  detection_priority:
    - user_preference
    - browser_language
    - ip_geolocation
    - default
  
  # Locale-specific settings
  locales:
    en:
      enabled: true
      date_format: "%B %d, %Y"
      number_decimal: "."
      number_thousands: ","
      formality: "balanced"
      grandmother_strength: "moderate"
    
    pt-br:
      enabled: true
      date_format: "%d de %B de %Y"
      number_decimal: ","
      number_thousands: "."
      formality: "informal"
      grandmother_strength: "strong"
    
    de:
      enabled: false  # Phase 2
      date_format: "%d. %B %Y"
      number_decimal: ","
      number_thousands: "."
      formality: "formal"
      grandmother_strength: "moderate"
    
    es:
      enabled: false  # Phase 2
      date_format: "%d de %B de %Y"
      number_decimal: ","
      number_thousands: "."
      formality: "balanced"
      grandmother_strength: "moderate"
  
  # Translation file paths
  translation_files:
    base: "translations/"
    format: "{locale}.json"
  
  # Fallback behavior
  fallback:
    missing_translation: "use_key"  # or "use_default_locale"
    log_missing: true
```

---

## 8. Database Schema

```sql
-- User locale preferences
CREATE TABLE user_locale_preferences (
    user_id UUID PRIMARY KEY,
    locale VARCHAR(10) NOT NULL DEFAULT 'en',
    timezone VARCHAR(50),
    date_format_override VARCHAR(50),
    currency_override VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Translation cache (for dynamic translations)
CREATE TABLE translation_cache (
    id SERIAL PRIMARY KEY,
    locale VARCHAR(10) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    original_content TEXT NOT NULL,
    translated_content TEXT NOT NULL,
    translator VARCHAR(50),  -- 'manual', 'ai', 'api'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    UNIQUE(locale, content_hash)
);

CREATE INDEX idx_translation_cache_lookup ON translation_cache(locale, content_hash);
```

---

## 9. Implementation Checklist

### Phase 1 (Launch)
- [ ] EN locale fully implemented
- [ ] PT-BR locale fully implemented
- [ ] Date formatting working for both
- [ ] Number formatting working for both
- [ ] Grandmother voice templates complete
- [ ] Disclaimers localized
- [ ] Locale router working

### Phase 2
- [ ] DE locale implemented
- [ ] ES locale implemented
- [ ] All templates translated
- [ ] Cultural adaptations complete
- [ ] Regulatory adaptations complete

---

**Document End**

**Next:** CMO_05_SOCIAL_ASSET_GENERATION.md
