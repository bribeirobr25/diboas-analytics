"""
HTML Email Formatter for Adelaide newsletters.

Uses inline CSS for maximum email client compatibility.
Registered with OutputRegistry as 'html_email'.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.registries.output_registry import OutputRegistry, OutputFormatter


@dataclass
class EmailSection:
    """Represents a section in the email."""
    title: str
    content: str
    icon: str = "📊"


@OutputRegistry.register("html_email")
class AdelaideHtmlEmailFormatter(OutputFormatter):
    """
    Formats Adelaide content as HTML email.

    Features:
    - Inline CSS (no external stylesheets)
    - Mobile-responsive design
    - Dark mode support via prefers-color-scheme
    - Preheader text for email preview
    - MSO conditional comments for Outlook
    """

    # Brand colors
    PRIMARY_COLOR = "#0066CC"
    SECONDARY_COLOR = "#00A86B"
    TEXT_COLOR = "#333333"
    BACKGROUND_COLOR = "#F5F5F5"
    CARD_COLOR = "#FFFFFF"

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @property
    def output_type(self) -> str:
        return "html_email"

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format Adelaide content as HTML email.

        Args:
            data: Adelaide content dict with keys:
                - edition: {type, date, persona, locale}
                - content: {greeting, market_snapshot, insight, etc.}

        Returns:
            Complete HTML email string
        """
        config = config or {}
        sections = self._build_sections(data)
        content = data.get("content", data) if isinstance(data, dict) else {}
        edition = data.get("edition", {}) if isinstance(data, dict) else {}

        return self._render_template(
            subject=content.get("subject", "Adelaide Daily Market Update"),
            preheader=content.get("preheader", "Your daily market intelligence"),
            greeting=content.get("greeting_message", content.get("greeting", "Good morning")),
            sections=sections,
            signature=self._get_signature(edition.get("persona", "ana")),
            date=datetime.utcnow().strftime("%B %d, %Y"),
            disclaimer=self._get_disclaimer(edition.get("locale", "en"))
        )

    def _build_sections(self, data: Any) -> List[EmailSection]:
        """Build email sections from content."""
        sections = []
        content = data.get("content", data) if isinstance(data, dict) else {}

        if content.get("market_snapshot"):
            sections.append(EmailSection(
                title="Market Overview",
                content=self._format_market_snapshot(content["market_snapshot"]),
                icon="📈"
            ))

        if content.get("alerts") or content.get("triggered_alerts"):
            alerts = content.get("alerts") or content.get("triggered_alerts", "")
            sections.append(EmailSection(
                title="Important Alerts",
                content=str(alerts),
                icon="⚠️"
            ))

        if content.get("insight_content"):
            sections.append(EmailSection(
                title="Adelaide's Insight",
                content=content["insight_content"],
                icon="💡"
            ))

        if content.get("strategy_summary"):
            sections.append(EmailSection(
                title="Strategy Updates",
                content=content["strategy_summary"],
                icon="📊"
            ))

        return sections

    def _format_market_snapshot(self, snapshot: Dict[str, Any]) -> str:
        """Format market snapshot as HTML table."""
        rows = []

        assets = [
            ("BTC", "btc_price", "btc_24h_change"),
            ("ETH", "eth_price", "eth_24h_change"),
            ("SOL", "sol_price", "sol_24h_change"),
        ]

        for label, price_key, change_key in assets:
            if price_key in snapshot:
                price = snapshot.get(price_key, 0)
                change = snapshot.get(change_key, 0)
                color = "#00A86B" if change >= 0 else "#DC3545"
                rows.append(
                    f'<tr><td style="padding:8px;border-bottom:1px solid #eee;">{label}</td>'
                    f'<td style="padding:8px;border-bottom:1px solid #eee;">${price:,.2f}</td>'
                    f'<td style="padding:8px;border-bottom:1px solid #eee;color:{color}">{change:+.2f}%</td></tr>'
                )

        if not rows:
            return "<p>Market data unavailable</p>"

        table = f'''
        <table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#f8f9fa;">
                <th style="padding:8px;text-align:left;">Asset</th>
                <th style="padding:8px;text-align:left;">Price</th>
                <th style="padding:8px;text-align:left;">24h</th>
            </tr>
            {"".join(rows)}
        </table>
        '''

        fg = snapshot.get("fear_greed_index")
        if fg is not None:
            label = snapshot.get("fear_greed_label", "Neutral")
            table += f'<p style="margin-top:15px;"><strong>Fear & Greed Index:</strong> {fg} ({label})</p>'

        return table

    def _render_template(
        self,
        subject: str,
        preheader: str,
        greeting: str,
        sections: List[EmailSection],
        signature: str,
        date: str,
        disclaimer: str
    ) -> str:
        """Render the full HTML email."""
        sections_html = "\n".join([self._render_section(s) for s in sections])

        return f'''<!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="color-scheme" content="light dark">
    <meta name="supported-color-schemes" content="light dark">
    <title>{subject}</title>
    <!--[if mso]>
    <style type="text/css">
        table {{border-collapse: collapse;}}
        .fallback-font {{font-family: Arial, sans-serif;}}
    </style>
    <![endif]-->
    <style>
        @media (prefers-color-scheme: dark) {{
            .email-bg {{ background-color: #1a1a1a !important; }}
            .email-card {{ background-color: #2d2d2d !important; }}
            .email-text {{ color: #e0e0e0 !important; }}
        }}
        @media only screen and (max-width: 600px) {{
            .email-container {{ width: 100% !important; }}
            .email-padding {{ padding: 20px !important; }}
        }}
    </style>
</head>
<body style="margin:0;padding:0;background-color:{self.BACKGROUND_COLOR};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;" class="email-bg">

    <!-- Preheader -->
    <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
        {preheader}
        &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
    </div>

    <!-- Email Container -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{self.BACKGROUND_COLOR};" class="email-bg">
        <tr>
            <td align="center" style="padding:20px 10px;">

                <!-- Content Card -->
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" class="email-container" style="background-color:{self.CARD_COLOR};border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">

                    <!-- Header -->
                    <tr>
                        <td style="padding:30px 40px;background-color:{self.PRIMARY_COLOR};border-radius:8px 8px 0 0;" class="email-padding">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <h1 style="margin:0;color:#FFFFFF;font-size:24px;font-weight:600;">
                                            &#127796; Adelaide
                                        </h1>
                                        <p style="margin:5px 0 0;color:rgba(255,255,255,0.8);font-size:14px;">
                                            {date}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Greeting -->
                    <tr>
                        <td style="padding:30px 40px 20px;" class="email-padding">
                            <p style="margin:0;color:{self.TEXT_COLOR};font-size:16px;line-height:1.6;" class="email-text">
                                {greeting}
                            </p>
                        </td>
                    </tr>

                    <!-- Sections -->
                    {sections_html}

                    <!-- Signature -->
                    <tr>
                        <td style="padding:20px 40px 30px;" class="email-padding">
                            <p style="margin:0;color:{self.TEXT_COLOR};font-size:16px;line-height:1.6;" class="email-text">
                                {signature}
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding:20px 40px;background-color:#F9F9F9;border-radius:0 0 8px 8px;border-top:1px solid #EEEEEE;" class="email-padding">
                            <p style="margin:0;color:#888888;font-size:12px;line-height:1.5;">
                                {disclaimer}
                            </p>
                            <p style="margin:10px 0 0;color:#888888;font-size:12px;">
                                <a href="{{{{unsubscribe_url}}}}" style="color:{self.PRIMARY_COLOR};text-decoration:none;">Unsubscribe</a> &#183;
                                <a href="https://diboas.com/preferences" style="color:{self.PRIMARY_COLOR};text-decoration:none;">Preferences</a>
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>'''

    def _render_section(self, section: EmailSection) -> str:
        """Render a single section."""
        return f'''
                    <tr>
                        <td style="padding:10px 40px 20px;" class="email-padding">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#F9F9F9;border-radius:8px;border-left:4px solid {self.PRIMARY_COLOR};">
                                <tr>
                                    <td style="padding:20px;">
                                        <h2 style="margin:0 0 10px;color:{self.TEXT_COLOR};font-size:18px;font-weight:600;" class="email-text">
                                            {section.icon} {section.title}
                                        </h2>
                                        <div style="color:{self.TEXT_COLOR};font-size:15px;line-height:1.6;" class="email-text">
                                            {section.content}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>'''

    def _get_signature(self, persona: str) -> str:
        """Get signature based on persona."""
        signatures = {
            "ana": "Stay informed,<br><strong>Ana</strong> &#127796;",
            "maria": "See you tomorrow,<br><strong>Maria</strong> &#128156;",
            "felipe": "Keep building,<br><strong>Felipe</strong> &#128640;",
        }
        return signatures.get(persona, signatures["ana"])

    def _get_disclaimer(self, locale: str) -> str:
        """Get disclaimer based on locale."""
        disclaimers = {
            "en": "This is not financial advice. Past performance does not guarantee future results. Your capital is at risk.",
            "pt-BR": "Isto n&atilde;o &eacute; aconselhamento financeiro. Rentabilidade passada n&atilde;o &eacute; garantia de rentabilidade futura. Seu capital est&aacute; em risco.",
            "pt-br": "Isto n&atilde;o &eacute; aconselhamento financeiro. Rentabilidade passada n&atilde;o &eacute; garantia de rentabilidade futura. Seu capital est&aacute; em risco.",
        }
        return disclaimers.get(locale, disclaimers["en"])
