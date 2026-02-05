# CMO_07: Gate 4 CMO Validations
## Tone, Brand & Personalization Validation

**Document Version:** 1.0  
**Date:** January 23, 2026  
**Parent Document:** CMO_BOARD_CTO_HANDOFF.md  
**Priority:** P0 (Launch-Critical)

---

## 1. Purpose

Gate 4 has two components:
- **CLO Validations:** Legal compliance (see CLO_BOARD_CTO_HANDOFF.md)
- **CMO Validations:** Tone, brand consistency, personalization completeness

This document specifies the **CMO portion** of Gate 4.

### CMO Gate 4 Responsibilities

| Validation | Description | Blocking? |
|------------|-------------|-----------|
| Tone Appropriateness | Content matches edition type | Yes |
| Personalization Complete | No unfilled placeholders | Yes |
| Length Limits | Channel-specific limits respected | Yes |
| Brand Voice | Adelaide's voice maintained | Warning |
| Emoji Usage | Appropriate for persona/locale | Warning |
| Grandmother Tone | Adelaide's warmth present | Warning |

---

## 2. Validation Architecture

### 2.1 Validation Pipeline

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         CMO GATE 4 VALIDATION                               â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                             â”‚
â”‚  Content from Layer 5                                                       â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚ 1. STRUCTURAL VALIDATION                                             â”‚   â”‚
â”‚  â”‚    - Personalization placeholders filled                             â”‚   â”‚
â”‚  â”‚    - Required sections present                                       â”‚   â”‚
â”‚  â”‚    - Length within limits                                            â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚ 2. TONE VALIDATION                                                   â”‚   â”‚
â”‚  â”‚    - Edition-appropriate tone                                        â”‚   â”‚
â”‚  â”‚    - Persona-appropriate language                                    â”‚   â”‚
â”‚  â”‚    - Crisis content checks (if applicable)                           â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚ 3. BRAND VALIDATION                                                  â”‚   â”‚
â”‚  â”‚    - Adelaide voice present                                          â”‚   â”‚
â”‚  â”‚    - Grandmother warmth check                                        â”‚   â”‚
â”‚  â”‚    - No prohibited phrases                                           â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚ 4. FORMATTING VALIDATION                                             â”‚   â”‚
â”‚  â”‚    - Emoji appropriateness                                           â”‚   â”‚
â”‚  â”‚    - Channel-specific formatting                                     â”‚   â”‚
â”‚  â”‚    - Localization completeness                                       â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚         â”‚                                                                   â”‚
â”‚         â–¼                                                                   â”‚
â”‚  Pass / Warn / Fail â†’ Route accordingly                                    â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 3. Validation Rules

### 3.1 Structural Validations (BLOCKING)

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import re

class ValidationResult(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"

@dataclass
class ValidationIssue:
    """A single validation issue."""
    rule_id: str
    severity: ValidationResult
    message: str
    location: Optional[str]  # Where in content
    suggestion: Optional[str]

class StructuralValidator:
    """Validate content structure."""
    
    # Placeholder patterns to detect
    PLACEHOLDER_PATTERNS = [
        r'\{[a-z_]+\}',           # {user_name}
        r'\{\{[a-z_]+\}\}',       # {{user_name}}
        r'\[PLACEHOLDER\]',       # [PLACEHOLDER]
        r'\[TODO\]',              # [TODO]
        r'__[A-Z_]+__',           # __USER_NAME__
    ]
    
    # Required sections by edition type
    REQUIRED_SECTIONS = {
        'daily': ['greeting', 'market_snapshot', 'disclaimer'],
        'weekly': ['greeting', 'market_summary', 'strategy_review', 'disclaimer'],
        'crisis': ['crisis_alert', 'safety_message', 'disclaimer'],
        'monthly': ['greeting', 'performance_summary', 'disclaimer'],
    }
    
    # Length limits by channel (characters)
    LENGTH_LIMITS = {
        'email': 100_000,      # 100KB
        'whatsapp': 4_096,
        'telegram': 4_096,
        'sms': 160,
        'push': 200,
    }
    
    def validate(self, content: str, context: dict) -> List[ValidationIssue]:
        """Run all structural validations."""
        issues = []
        
        # 1. Check for unfilled placeholders
        issues.extend(self._check_placeholders(content))
        
        # 2. Check required sections
        issues.extend(self._check_required_sections(
            content, 
            context.get('edition_type', 'daily')
        ))
        
        # 3. Check length limits
        issues.extend(self._check_length(
            content, 
            context.get('channel', 'email')
        ))
        
        return issues
    
    def _check_placeholders(self, content: str) -> List[ValidationIssue]:
        """Check for unfilled placeholders."""
        issues = []
        
        for pattern in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content)
            for match in matches:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-001',
                    severity=ValidationResult.FAIL,
                    message=f"Unfilled placeholder found: {match}",
                    location=match,
                    suggestion=f"Fill placeholder {match} with actual value"
                ))
        
        return issues
    
    def _check_required_sections(
        self, 
        content: str, 
        edition_type: str
    ) -> List[ValidationIssue]:
        """Check that required sections are present."""
        issues = []
        required = self.REQUIRED_SECTIONS.get(edition_type, [])
        
        for section in required:
            # Check for section markers or headers
            section_patterns = [
                f'## {section}',
                f'### {section}',
                f'[{section}]',
                section.upper(),
            ]
            
            found = any(p.lower() in content.lower() for p in section_patterns)
            
            if not found and section == 'disclaimer':
                # Disclaimer is CRITICAL
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-002',
                    severity=ValidationResult.FAIL,
                    message=f"Required section missing: {section}",
                    location=None,
                    suggestion=f"Add {section} section to content"
                ))
            elif not found:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-003',
                    severity=ValidationResult.WARN,
                    message=f"Expected section may be missing: {section}",
                    location=None,
                    suggestion=f"Consider adding {section} section"
                ))
        
        return issues
    
    def _check_length(self, content: str, channel: str) -> List[ValidationIssue]:
        """Check content length for channel."""
        issues = []
        limit = self.LENGTH_LIMITS.get(channel, 100_000)
        actual = len(content)
        
        if actual > limit:
            issues.append(ValidationIssue(
                rule_id='CMO-G4-004',
                severity=ValidationResult.FAIL,
                message=f"Content exceeds {channel} limit: {actual} > {limit} chars",
                location=None,
                suggestion=f"Trim content to under {limit} characters"
            ))
        elif actual > limit * 0.9:
            issues.append(ValidationIssue(
                rule_id='CMO-G4-005',
                severity=ValidationResult.WARN,
                message=f"Content approaching {channel} limit: {actual}/{limit} chars",
                location=None,
                suggestion="Consider trimming content for buffer"
            ))
        
        return issues
```

### 3.2 Tone Validations

```python
class ToneValidator:
    """Validate content tone appropriateness."""
    
    # Panic-inducing phrases to avoid
    PANIC_PHRASES = [
        'crash imminent',
        'sell everything',
        'emergency',
        'disaster',
        'catastrophe',
        'meltdown',
        'collapse',
        'plummet',
        'free fall',
        'blood bath',
        'wipe out',
    ]
    
    # FOMO phrases to avoid
    FOMO_PHRASES = [
        'don\'t miss out',
        'limited time',
        'act now',
        'last chance',
        'hurry',
        'before it\'s too late',
        'exclusive opportunity',
        'once in a lifetime',
    ]
    
    # Overly casual phrases (inappropriate for crisis)
    CASUAL_PHRASES = [
        'lol',
        'omg',
        'btw',
        'tbh',
        'ngl',
        'bruh',
    ]
    
    # Formal phrases (inappropriate for Ana persona)
    OVERLY_FORMAL = [
        'pursuant to',
        'notwithstanding',
        'hereinafter',
        'aforementioned',
        'henceforth',
    ]
    
    def validate(self, content: str, context: dict) -> List[ValidationIssue]:
        """Run all tone validations."""
        issues = []
        
        edition_type = context.get('edition_type', 'daily')
        persona = context.get('persona', 'maria')
        crisis_level = context.get('crisis_level', 0)
        
        # 1. Check for panic-inducing language
        issues.extend(self._check_panic_language(content))
        
        # 2. Check for FOMO language
        issues.extend(self._check_fomo_language(content))
        
        # 3. Check tone matches edition type
        issues.extend(self._check_edition_tone(content, edition_type, crisis_level))
        
        # 4. Check tone matches persona
        issues.extend(self._check_persona_tone(content, persona))
        
        return issues
    
    def _check_panic_language(self, content: str) -> List[ValidationIssue]:
        """Check for panic-inducing language."""
        issues = []
        content_lower = content.lower()
        
        for phrase in self.PANIC_PHRASES:
            if phrase in content_lower:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-010',
                    severity=ValidationResult.FAIL,
                    message=f"Panic-inducing language detected: '{phrase}'",
                    location=phrase,
                    suggestion="Replace with calmer, more measured language"
                ))
        
        return issues
    
    def _check_fomo_language(self, content: str) -> List[ValidationIssue]:
        """Check for FOMO-inducing language."""
        issues = []
        content_lower = content.lower()
        
        for phrase in self.FOMO_PHRASES:
            if phrase in content_lower:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-011',
                    severity=ValidationResult.WARN,
                    message=f"FOMO language detected: '{phrase}'",
                    location=phrase,
                    suggestion="Adelaide doesn't create urgency; replace with educational tone"
                ))
        
        return issues
    
    def _check_edition_tone(
        self, 
        content: str, 
        edition_type: str,
        crisis_level: int
    ) -> List[ValidationIssue]:
        """Check tone matches edition type."""
        issues = []
        content_lower = content.lower()
        
        if edition_type == 'crisis' or crisis_level >= 3:
            # Crisis content should not have casual language
            for phrase in self.CASUAL_PHRASES:
                if phrase in content_lower:
                    issues.append(ValidationIssue(
                        rule_id='CMO-G4-012',
                        severity=ValidationResult.FAIL,
                        message=f"Casual language in crisis content: '{phrase}'",
                        location=phrase,
                        suggestion="Crisis content requires serious tone"
                    ))
            
            # Check for appropriate crisis markers
            crisis_markers = ['âš ï¸', 'important', 'alert', 'update']
            has_marker = any(m in content_lower for m in crisis_markers)
            if not has_marker:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-013',
                    severity=ValidationResult.WARN,
                    message="Crisis content lacks urgency markers",
                    location=None,
                    suggestion="Add appropriate crisis markers (âš ï¸, 'Important Update', etc.)"
                ))
        
        return issues
    
    def _check_persona_tone(self, content: str, persona: str) -> List[ValidationIssue]:
        """Check tone matches target persona."""
        issues = []
        content_lower = content.lower()
        
        if persona == 'ana':
            # Ana needs simple, warm language
            for phrase in self.OVERLY_FORMAL:
                if phrase in content_lower:
                    issues.append(ValidationIssue(
                        rule_id='CMO-G4-014',
                        severity=ValidationResult.WARN,
                        message=f"Overly formal language for Ana persona: '{phrase}'",
                        location=phrase,
                        suggestion="Simplify language for Ana persona"
                    ))
            
            # Check for technical terms
            technical_terms = ['APY', 'TVL', 'liquidity', 'protocol', 'smart contract']
            for term in technical_terms:
                if term.lower() in content_lower:
                    issues.append(ValidationIssue(
                        rule_id='CMO-G4-015',
                        severity=ValidationResult.WARN,
                        message=f"Technical term for Ana persona: '{term}'",
                        location=term,
                        suggestion=f"Replace '{term}' with plain language"
                    ))
        
        elif persona == 'felipe':
            # Felipe expects more detail - warn if too simplified
            simplifications = ['your money', 'savings', 'earnings']
            simple_count = sum(1 for s in simplifications if s in content_lower)
            
            if simple_count > 5:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-016',
                    severity=ValidationResult.WARN,
                    message="Content may be oversimplified for Felipe persona",
                    location=None,
                    suggestion="Felipe prefers technical terms; consider using APY, returns, etc."
                ))
        
        return issues
```

### 3.3 Brand Validations

```python
class BrandValidator:
    """Validate brand voice consistency."""
    
    # Adelaide's voice markers
    GRANDMOTHER_MARKERS = [
        'grandmother',
        'grandma',
        'vovÃ³',
        'avÃ³',
        'oma',
        'abuela',
        'would say',
        'diria',
        'wÃ¼rde sagen',
        'patience',
        'time',
        'long-term',
        'sleep',
        'while you slept',
    ]
    
    # Prohibited brand phrases
    PROHIBITED_PHRASES = [
        'guaranteed returns',
        'risk-free',
        'no risk',
        'can\'t lose',
        'sure thing',
        'get rich quick',
        'financial advice',
        'investment advice',
        'you should buy',
        'you should sell',
    ]
    
    # Required brand elements
    BRAND_ELEMENTS = {
        'daily': ['Adelaide', 'diBoaS'],
        'weekly': ['Adelaide', 'diBoaS'],
        'monthly': ['Adelaide', 'diBoaS'],
        'crisis': ['diBoaS'],  # Adelaide less prominent in crisis
    }
    
    def validate(self, content: str, context: dict) -> List[ValidationIssue]:
        """Run all brand validations."""
        issues = []
        
        edition_type = context.get('edition_type', 'daily')
        
        # 1. Check for prohibited phrases
        issues.extend(self._check_prohibited(content))
        
        # 2. Check brand elements present
        issues.extend(self._check_brand_elements(content, edition_type))
        
        # 3. Check grandmother voice (non-crisis only)
        if edition_type != 'crisis':
            issues.extend(self._check_grandmother_voice(content))
        
        return issues
    
    def _check_prohibited(self, content: str) -> List[ValidationIssue]:
        """Check for prohibited phrases."""
        issues = []
        content_lower = content.lower()
        
        for phrase in self.PROHIBITED_PHRASES:
            if phrase in content_lower:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-020',
                    severity=ValidationResult.FAIL,
                    message=f"Prohibited phrase detected: '{phrase}'",
                    location=phrase,
                    suggestion="Remove or rephrase; this language is not permitted"
                ))
        
        return issues
    
    def _check_brand_elements(
        self, 
        content: str, 
        edition_type: str
    ) -> List[ValidationIssue]:
        """Check brand elements are present."""
        issues = []
        required = self.BRAND_ELEMENTS.get(edition_type, ['diBoaS'])
        
        for element in required:
            if element.lower() not in content.lower():
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-021',
                    severity=ValidationResult.WARN,
                    message=f"Brand element missing: '{element}'",
                    location=None,
                    suggestion=f"Include '{element}' somewhere in content"
                ))
        
        return issues
    
    def _check_grandmother_voice(self, content: str) -> List[ValidationIssue]:
        """Check Adelaide's grandmother voice is present."""
        issues = []
        content_lower = content.lower()
        
        # Check for any grandmother markers
        has_grandmother = any(m in content_lower for m in self.GRANDMOTHER_MARKERS)
        
        if not has_grandmother:
            issues.append(ValidationIssue(
                rule_id='CMO-G4-022',
                severity=ValidationResult.WARN,
                message="Adelaide's grandmother voice not detected",
                location=None,
                suggestion="Add grandmother wisdom or long-term perspective references"
            ))
        
        return issues
```

### 3.4 Formatting Validations

```python
class FormattingValidator:
    """Validate content formatting."""
    
    # Emoji limits by persona
    EMOJI_LIMITS = {
        'ana': {'min': 3, 'max': 15},
        'maria': {'min': 2, 'max': 10},
        'felipe': {'min': 0, 'max': 5},
    }
    
    # Emoji limits by locale
    LOCALE_EMOJI_ADJUSTMENT = {
        'de': -3,  # Germans prefer fewer emojis
        'pt-br': +3,  # Brazilians like more emojis
    }
    
    def validate(self, content: str, context: dict) -> List[ValidationIssue]:
        """Run all formatting validations."""
        issues = []
        
        persona = context.get('persona', 'maria')
        locale = context.get('locale', 'en')
        channel = context.get('channel', 'email')
        
        # 1. Check emoji usage
        issues.extend(self._check_emojis(content, persona, locale))
        
        # 2. Check channel-specific formatting
        issues.extend(self._check_channel_formatting(content, channel))
        
        # 3. Check localization completeness
        issues.extend(self._check_localization(content, locale))
        
        return issues
    
    def _check_emojis(
        self, 
        content: str, 
        persona: str, 
        locale: str
    ) -> List[ValidationIssue]:
        """Check emoji usage is appropriate."""
        issues = []
        
        # Count emojis
        import emoji
        emoji_count = len([c for c in content if c in emoji.EMOJI_DATA])
        
        # Get limits for persona
        limits = self.EMOJI_LIMITS.get(persona, self.EMOJI_LIMITS['maria'])
        adjustment = self.LOCALE_EMOJI_ADJUSTMENT.get(locale, 0)
        
        min_emojis = max(0, limits['min'] + adjustment)
        max_emojis = limits['max'] + adjustment
        
        if emoji_count < min_emojis:
            issues.append(ValidationIssue(
                rule_id='CMO-G4-030',
                severity=ValidationResult.WARN,
                message=f"Too few emojis for {persona} persona: {emoji_count} < {min_emojis}",
                location=None,
                suggestion=f"Add more emojis; {persona} persona expects more visual warmth"
            ))
        elif emoji_count > max_emojis:
            issues.append(ValidationIssue(
                rule_id='CMO-G4-031',
                severity=ValidationResult.WARN,
                message=f"Too many emojis for {persona} persona: {emoji_count} > {max_emojis}",
                location=None,
                suggestion=f"Reduce emoji usage; {persona} persona prefers cleaner content"
            ))
        
        return issues
    
    def _check_channel_formatting(
        self, 
        content: str, 
        channel: str
    ) -> List[ValidationIssue]:
        """Check channel-specific formatting."""
        issues = []
        
        if channel == 'sms':
            # SMS should not have markdown
            if '**' in content or '##' in content or '*' in content:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-032',
                    severity=ValidationResult.FAIL,
                    message="SMS content contains markdown formatting",
                    location=None,
                    suggestion="Remove markdown; SMS is plain text only"
                ))
        
        elif channel == 'whatsapp':
            # WhatsApp has specific formatting
            if '<b>' in content or '<i>' in content:
                issues.append(ValidationIssue(
                    rule_id='CMO-G4-033',
                    severity=ValidationResult.FAIL,
                    message="WhatsApp content contains HTML formatting",
                    location=None,
                    suggestion="Use *bold* and _italic_ for WhatsApp"
                ))
        
        return issues
    
    def _check_localization(self, content: str, locale: str) -> List[ValidationIssue]:
        """Check localization is complete."""
        issues = []
        
        # Check for mixed language (e.g., English in PT-BR content)
        if locale == 'pt-br':
            english_words = ['the', 'and', 'your', 'while you slept']
            for word in english_words:
                if f' {word} ' in content.lower():
                    issues.append(ValidationIssue(
                        rule_id='CMO-G4-034',
                        severity=ValidationResult.WARN,
                        message=f"English word in PT-BR content: '{word}'",
                        location=word,
                        suggestion="Translate all content to Portuguese"
                    ))
                    break  # One warning is enough
        
        elif locale == 'de':
            english_words = ['the', 'and', 'your']
            for word in english_words:
                if f' {word} ' in content.lower():
                    issues.append(ValidationIssue(
                        rule_id='CMO-G4-035',
                        severity=ValidationResult.WARN,
                        message=f"English word in German content: '{word}'",
                        location=word,
                        suggestion="Translate all content to German"
                    ))
                    break
        
        return issues
```

---

## 4. Main Validator

### 4.1 Gate 4 CMO Validator

```python
@dataclass
class Gate4CMOResult:
    """Result of CMO Gate 4 validation."""
    passed: bool
    has_warnings: bool
    issues: List[ValidationIssue]
    blocking_issues: List[ValidationIssue]
    warning_issues: List[ValidationIssue]
    validation_time_ms: int

class Gate4CMOValidator:
    """Main CMO Gate 4 validator."""
    
    def __init__(self):
        self.structural = StructuralValidator()
        self.tone = ToneValidator()
        self.brand = BrandValidator()
        self.formatting = FormattingValidator()
    
    def validate(self, content: str, context: dict) -> Gate4CMOResult:
        """
        Run complete CMO Gate 4 validation.
        
        Args:
            content: Content to validate
            context: Dict containing:
                - edition_type: 'daily', 'weekly', 'crisis', etc.
                - persona: 'ana', 'maria', 'felipe'
                - locale: 'en', 'pt-br', 'de', 'es'
                - channel: 'email', 'whatsapp', etc.
                - crisis_level: 0-5
        
        Returns:
            Gate4CMOResult with pass/fail and issues
        """
        import time
        start = time.time()
        
        all_issues = []
        
        # Run all validators
        all_issues.extend(self.structural.validate(content, context))
        all_issues.extend(self.tone.validate(content, context))
        all_issues.extend(self.brand.validate(content, context))
        all_issues.extend(self.formatting.validate(content, context))
        
        # Separate blocking vs warning
        blocking = [i for i in all_issues if i.severity == ValidationResult.FAIL]
        warnings = [i for i in all_issues if i.severity == ValidationResult.WARN]
        
        elapsed_ms = int((time.time() - start) * 1000)
        
        return Gate4CMOResult(
            passed=len(blocking) == 0,
            has_warnings=len(warnings) > 0,
            issues=all_issues,
            blocking_issues=blocking,
            warning_issues=warnings,
            validation_time_ms=elapsed_ms
        )
    
    def validate_and_fix(
        self, 
        content: str, 
        context: dict
    ) -> Tuple[str, Gate4CMOResult]:
        """
        Validate and attempt to auto-fix issues.
        
        Some issues can be auto-fixed:
        - Emoji count adjustments
        - Simple placeholder fills (if default available)
        - Formatting corrections
        """
        # First validation
        result = self.validate(content, context)
        
        if result.passed and not result.has_warnings:
            return content, result
        
        # Attempt auto-fixes for warnings
        fixed_content = content
        for issue in result.warning_issues:
            fixed_content = self._attempt_fix(fixed_content, issue, context)
        
        # Re-validate
        final_result = self.validate(fixed_content, context)
        
        return fixed_content, final_result
    
    def _attempt_fix(
        self, 
        content: str, 
        issue: ValidationIssue, 
        context: dict
    ) -> str:
        """Attempt to auto-fix an issue."""
        
        # Emoji count fixes
        if issue.rule_id == 'CMO-G4-031':  # Too many emojis
            # Remove some emojis
            import emoji
            emojis_in_content = [c for c in content if c in emoji.EMOJI_DATA]
            # Remove every other emoji after the max
            persona = context.get('persona', 'maria')
            max_emojis = self.formatting.EMOJI_LIMITS.get(persona, {}).get('max', 10)
            
            for e in emojis_in_content[max_emojis:]:
                content = content.replace(e, '', 1)
        
        # Markdown in SMS fix
        if issue.rule_id == 'CMO-G4-032':
            content = content.replace('**', '').replace('##', '').replace('*', '')
        
        return content
```

---

## 5. Error Codes

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| CMO-G4-001 | Unfilled placeholder | FAIL | Block until fixed |
| CMO-G4-002 | Missing required section (disclaimer) | FAIL | Block until fixed |
| CMO-G4-003 | Expected section may be missing | WARN | Log, proceed |
| CMO-G4-004 | Content exceeds channel limit | FAIL | Block, trim content |
| CMO-G4-005 | Approaching channel limit | WARN | Log, proceed |
| CMO-G4-010 | Panic-inducing language | FAIL | Block until rewritten |
| CMO-G4-011 | FOMO language detected | WARN | Log, suggest change |
| CMO-G4-012 | Casual language in crisis | FAIL | Block until fixed |
| CMO-G4-013 | Crisis lacks urgency markers | WARN | Log, proceed |
| CMO-G4-014 | Overly formal for Ana | WARN | Log, suggest simplification |
| CMO-G4-015 | Technical term for Ana | WARN | Log, suggest plain language |
| CMO-G4-016 | Oversimplified for Felipe | WARN | Log, proceed |
| CMO-G4-020 | Prohibited phrase | FAIL | Block until removed |
| CMO-G4-021 | Brand element missing | WARN | Log, proceed |
| CMO-G4-022 | Grandmother voice missing | WARN | Log, proceed |
| CMO-G4-030 | Too few emojis | WARN | Auto-fix or proceed |
| CMO-G4-031 | Too many emojis | WARN | Auto-fix or proceed |
| CMO-G4-032 | Markdown in SMS | FAIL | Auto-fix or block |
| CMO-G4-033 | HTML in WhatsApp | FAIL | Auto-fix or block |
| CMO-G4-034 | Incomplete localization | WARN | Log, proceed |

---

## 6. Configuration

```yaml
# config/gate4_cmo.yaml

gate4_cmo:
  enabled: true
  
  # Validation settings
  validation:
    structural:
      enabled: true
      require_disclaimer: true
      
    tone:
      enabled: true
      block_panic_language: true
      warn_fomo_language: true
      
    brand:
      enabled: true
      require_adelaide_mention: true
      require_grandmother_voice: true
      
    formatting:
      enabled: true
      check_emojis: true
      check_localization: true
  
  # Auto-fix settings
  auto_fix:
    enabled: true
    fix_emoji_count: true
    fix_markdown_sms: true
    fix_html_whatsapp: true
    
  # Escalation
  escalation:
    fail_threshold: 1  # Any fail = block
    warn_threshold: 5  # 5+ warnings = notify CMO lead
    notification_channel: "#content-quality"
```

---

## 7. Testing Requirements

```python
class TestGate4CMO:
    """Tests for CMO Gate 4 validations."""
    
    def test_unfilled_placeholder_fails(self):
        """Unfilled placeholders should fail validation."""
        content = "Hello {user_name}, your balance is {balance}"
        result = validator.validate(content, {'edition_type': 'daily'})
        assert not result.passed
        assert any(i.rule_id == 'CMO-G4-001' for i in result.blocking_issues)
    
    def test_panic_language_fails(self):
        """Panic-inducing language should fail."""
        content = "CRASH IMMINENT! Sell everything now!"
        result = validator.validate(content, {'edition_type': 'daily'})
        assert not result.passed
        assert any(i.rule_id == 'CMO-G4-010' for i in result.blocking_issues)
    
    def test_fomo_language_warns(self):
        """FOMO language should warn but not fail."""
        content = "Don't miss out on these yields!"
        result = validator.validate(content, {'edition_type': 'daily'})
        assert result.passed  # Warnings don't fail
        assert any(i.rule_id == 'CMO-G4-011' for i in result.warning_issues)
    
    def test_crisis_requires_serious_tone(self):
        """Crisis content should not have casual language."""
        content = "lol the market is down btw"
        result = validator.validate(content, {'edition_type': 'crisis'})
        assert not result.passed
    
    def test_ana_avoids_technical_terms(self):
        """Ana persona should avoid technical jargon."""
        content = "Your APY is 5% with low TVL risk"
        result = validator.validate(content, {'persona': 'ana', 'edition_type': 'daily'})
        assert result.has_warnings
        assert any(i.rule_id == 'CMO-G4-015' for i in result.warning_issues)
```

---

## 8. Implementation Checklist

- [ ] StructuralValidator implemented
- [ ] ToneValidator implemented
- [ ] BrandValidator implemented
- [ ] FormattingValidator implemented
- [ ] Gate4CMOValidator orchestrator working
- [ ] Auto-fix functionality implemented
- [ ] All error codes documented
- [ ] Integration with Layer 5 pipeline
- [ ] Integration with CLO Gate 4
- [ ] Logging and monitoring
- [ ] Unit tests passing (>95% coverage)

---

**Document End**

**Next:** CMO_08_ANALYTICS_AB_TESTING.md
