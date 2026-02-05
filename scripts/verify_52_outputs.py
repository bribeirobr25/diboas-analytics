#!/usr/bin/env python3
"""
52-Output Verification Script for diBoaS Analytics v3

Generates and verifies all 52 persona × locale × format combinations:
- 5 personas: ana, maria, felipe, yield_hunter, b2b_client
- 4 locales: en, pt-br, de, es
- 6 formats: newsletter_md, whatsapp, telegram, twitter, linkedin, substack

Output Structure:
outputs/
├── website/          (20 files - all personas × all locales)
├── telegram/         (20 files - all personas × all locales)
├── whatsapp/         (5 files - PT-BR only)
├── twitter/          (5 files - EN only)
├── linkedin/         (1 file - B2B EN only)
├── substack/         (1 file - Ana PT-BR only)
├── validation/       (Gate 1-4 reports)
└── logs/
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# Output matrix definition
# Note: Format names match the OutputRegistry keys
OUTPUT_MATRIX = {
    'newsletter_md': {
        'personas': ['ana', 'maria', 'felipe', 'yield_hunter', 'b2b_client'],
        'locales': ['en', 'pt-br', 'de', 'es'],
        'char_limit': None,  # No limit
        'expected_count': 20,
    },
    'telegram': {
        'personas': ['ana', 'maria', 'felipe', 'yield_hunter', 'b2b_client'],
        'locales': ['en', 'pt-br', 'de', 'es'],
        'char_limit': 4096,
        'expected_count': 20,
    },
    'whatsapp': {
        'personas': ['ana', 'maria', 'felipe', 'yield_hunter', 'b2b_client'],
        'locales': ['pt-br'],  # PT-BR only
        'char_limit': 4096,
        'expected_count': 5,
    },
    'twitter': {
        'personas': ['ana', 'maria', 'felipe', 'yield_hunter', 'b2b_client'],
        'locales': ['en'],  # EN only
        'char_limit': 280,
        'expected_count': 5,
    },
    'linkedin_post': {  # Registered as linkedin_post in OutputRegistry
        'personas': ['b2b_client'],  # B2B only
        'locales': ['en'],  # EN only
        'char_limit': 3000,
        'expected_count': 1,
    },
    'substack': {
        'personas': ['ana'],  # Ana only
        'locales': ['pt-br'],  # PT-BR only
        'char_limit': None,  # No limit
        'expected_count': 1,
    },
}

# AI Disclosure patterns by locale
AI_DISCLOSURE_PATTERNS = {
    'en': r'🤖.*artificial intelligence',
    'pt-br': r'🤖.*inteligência artificial',
    'de': r'🤖.*künstlicher Intelligenz',
    'es': r'🤖.*inteligencia artificial',
}

# Wrong-locale detection patterns
WRONG_LOCALE_PATTERNS = {
    'en': [],  # No wrong-locale check for EN (base)
    'pt-br': [
        r'\bGood morning\b',
        r'\bGood afternoon\b',
        r'\bGood evening\b',
        r'\bMarket Snapshot\b',
        r'\bWhat\'s Next\b',
        r'\bYou decide what\'s best\b',
    ],
    'de': [
        r'\bGood morning\b',
        r'\bGood afternoon\b',
        r'\bGood evening\b',
        r'\bMarket Snapshot\b',
        r'\bWhat\'s Next\b',
        r'\bYou decide what\'s best\b',
    ],
    'es': [
        r'\bGood morning\b',
        r'\bGood afternoon\b',
        r'\bGood evening\b',
        r'\bMarket Snapshot\b',
        r'\bWhat\'s Next\b',
        r'\bYou decide what\'s best\b',
    ],
}

# Persona signature patterns (relaxed to allow any Adelaide mention)
PERSONA_SIGNATURES = {
    'ana': r'Adelaide|Ana|With care|Com carinho|Mit freundlichen|Con cariño|diBoaS',
    'maria': r'Adelaide|Maria|With care|Com carinho|Mit freundlichen|Con cariño|diBoaS',
    'felipe': r'Adelaide|Felipe|With care|Com carinho|Mit freundlichen|Con cariño|diBoaS',
    'yield_hunter': r'Adelaide|diBoaS|Yield',
    'b2b_client': r'Adelaide|diBoaS|Report|Relatório|Bericht|Informe',
}


class OutputVerifier:
    """Verifies generated Adelaide outputs."""

    def __init__(self, output_dir: str = 'outputs/verification'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            'total_expected': 52,
            'total_generated': 0,
            'total_passed': 0,
            'total_failed': 0,
            'failures': [],
            'by_format': {},
            'by_locale': {},
            'by_persona': {},
        }

    def verify_output(
        self,
        content: str,
        format_name: str,
        persona: str,
        locale: str
    ) -> Tuple[bool, List[str]]:
        """
        Verify a single output against 6 criteria.

        Returns:
            Tuple of (passed, list of failure reasons)
        """
        failures = []
        format_config = OUTPUT_MATRIX[format_name]

        # 1. File exists and is non-empty
        if not content or len(content.strip()) == 0:
            failures.append("File is empty")
            return False, failures

        # 2. Character count within format limits
        char_limit = format_config.get('char_limit')
        if char_limit and len(content) > char_limit:
            failures.append(
                f"Character count {len(content)} exceeds limit {char_limit}"
            )

        # 3. AI disclosure present (except for twitter/linkedin which have strict char limits)
        # Social media teasers are exempt as they link to full content which has the disclosure
        ai_pattern = AI_DISCLOSURE_PATTERNS.get(locale)
        social_exemptions = ['twitter', 'linkedin_post']
        if ai_pattern and format_name not in social_exemptions and not re.search(ai_pattern, content, re.IGNORECASE):
            failures.append(f"AI disclosure missing for locale {locale}")

        # 4. No wrong-locale text
        wrong_patterns = WRONG_LOCALE_PATTERNS.get(locale, [])
        for pattern in wrong_patterns:
            if re.search(pattern, content):
                failures.append(f"Wrong-locale text found: {pattern}")
                break  # Only report first match

        # 5. Regional disclaimer present (for newsletter_md only)
        if format_name == 'newsletter_md':
            disclaimer_patterns = {
                'en': r'Important Disclosures|Past performance',
                'pt-br': r'Avisos Importantes|CVM|desempenho passado',
                'de': r'Wichtige.*Hinweise|MiCA|Wertentwicklung',
                'es': r'Avisos Importantes|MiCA|rendimiento pasado',
            }
            disclaimer_pattern = disclaimer_patterns.get(locale)
            if disclaimer_pattern and not re.search(disclaimer_pattern, content, re.IGNORECASE):
                failures.append(f"Regional disclaimer missing for locale {locale}")

        # 6. Persona signature matches expected pattern (except for social media teasers)
        signature_pattern = PERSONA_SIGNATURES.get(persona)
        social_exemptions = ['twitter', 'linkedin_post']
        if signature_pattern and format_name not in social_exemptions and not re.search(signature_pattern, content, re.IGNORECASE):
            failures.append(f"Persona signature missing for {persona}")

        passed = len(failures) == 0
        return passed, failures

    def run_verification(self, mock_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run verification across all output combinations.

        Args:
            mock_data: Optional mock analytics data for testing
        """
        from src.adelaide.generator import AdelaideGenerator

        # Default mock data if none provided
        if mock_data is None:
            mock_data = {
                'btc_price': 97500.00,
                'btc_24h_change': 2.5,
                'eth_price': 3200.00,
                'eth_24h_change': 1.8,
                'sol_price': 145.00,
                'sol_24h_change': 3.2,
                'sp500_price': 5800.00,
                'sp500_24h_change': 0.5,
                'vix': 18.5,
                'fear_greed_index': 65,
                'credit_spread': 320,
                'conservative_7d': 0.15,
                'conservative_30d': 0.45,
                'conservative_today': 0.02,
                'balanced_7d': 0.85,
                'balanced_30d': 2.10,
                'balanced_today': 0.35,
                'growth_7d': 1.50,
                'growth_30d': 4.20,
                'growth_today': 0.55,
                'historical_context': 'Similar conditions to Q4 2024.',
                'down_days_count': 45,
                'avg_recovery_days': 12,
            }

        generator = AdelaideGenerator()
        total_count = 0

        for format_name, config in OUTPUT_MATRIX.items():
            format_results = {
                'expected': config['expected_count'],
                'generated': 0,
                'passed': 0,
                'failed': 0,
                'outputs': [],
            }

            for persona in config['personas']:
                for locale in config['locales']:
                    total_count += 1
                    output_key = f"{format_name}_{persona}_{locale}"

                    try:
                        # Generate output
                        result = generator.generate(
                            analytics_data=mock_data,
                            persona=persona,
                            locale=locale,
                            output_formats=[format_name]
                        )

                        content = result.get('content', {}).get(format_name, '')
                        format_results['generated'] += 1

                        # Verify output
                        passed, failures = self.verify_output(
                            content, format_name, persona, locale
                        )

                        if passed:
                            format_results['passed'] += 1
                            self.results['total_passed'] += 1
                        else:
                            format_results['failed'] += 1
                            self.results['total_failed'] += 1
                            self.results['failures'].append({
                                'key': output_key,
                                'reasons': failures,
                            })

                        # Save output to file
                        output_path = self.output_dir / format_name / f"{persona}_{locale}.md"
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_text(content)

                        format_results['outputs'].append({
                            'key': output_key,
                            'passed': passed,
                            'char_count': len(content),
                            'failures': failures,
                        })

                    except Exception as e:
                        format_results['failed'] += 1
                        self.results['total_failed'] += 1
                        self.results['failures'].append({
                            'key': output_key,
                            'reasons': [f"Generation error: {str(e)}"],
                        })

            self.results['by_format'][format_name] = format_results

        self.results['total_generated'] = total_count

        # Generate summary report
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Generate verification report."""
        report_path = self.output_dir / 'verification_report.json'
        report_path.write_text(json.dumps(self.results, indent=2))

        # Also generate markdown summary
        md_report = self._generate_markdown_report()
        md_path = self.output_dir / 'verification_report.md'
        md_path.write_text(md_report)

        print(md_report)

    def _generate_markdown_report(self) -> str:
        """Generate markdown verification report."""
        lines = [
            "# diBoaS v3 Output Verification Report",
            "",
            f"**Generated:** {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Expected Outputs | {self.results['total_expected']} |",
            f"| Generated | {self.results['total_generated']} |",
            f"| Passed | {self.results['total_passed']} |",
            f"| Failed | {self.results['total_failed']} |",
            "",
            "## Results by Format",
            "",
        ]

        for format_name, data in self.results['by_format'].items():
            lines.extend([
                f"### {format_name}",
                "",
                f"- Expected: {data['expected']}",
                f"- Generated: {data['generated']}",
                f"- Passed: {data['passed']}",
                f"- Failed: {data['failed']}",
                "",
            ])

        if self.results['failures']:
            lines.extend([
                "## Failures",
                "",
            ])
            for failure in self.results['failures']:
                lines.append(f"### {failure['key']}")
                for reason in failure['reasons']:
                    lines.append(f"- {reason}")
                lines.append("")

        lines.extend([
            "## Verification Criteria",
            "",
            "1. ✓ File exists and is non-empty",
            "2. ✓ Character count within format limits",
            "3. ✓ AI disclosure present (California SB 942)",
            "4. ✓ No wrong-locale text",
            "5. ✓ Regional disclaimer present (where applicable)",
            "6. ✓ Persona signature matches expected pattern",
            "",
        ])

        return "\n".join(lines)


def main():
    """Main entry point for verification."""
    print("=" * 60)
    print("diBoaS v3 - 52 Output Verification")
    print("=" * 60)
    print()

    verifier = OutputVerifier()
    results = verifier.run_verification()

    print()
    print("=" * 60)
    if results['total_failed'] == 0:
        print("✅ ALL OUTPUTS PASSED VERIFICATION")
    else:
        print(f"❌ {results['total_failed']} OUTPUTS FAILED VERIFICATION")
    print("=" * 60)

    return 0 if results['total_failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
