"""
Localization constants and compliance disclosures.

Contains locale-independent constants, AI disclosure, TradFi gap disclosures,
regional disclaimers, and hypothetical performance disclaimers.

Note: REGIONAL_DISCLAIMERS and HYPOTHETICAL_DISCLAIMERS are imported from
src/shared/disclaimers.py to avoid cross-domain coupling (DDD Principle 1).
They are re-exported here for backward compatibility within the Adelaide domain.
"""

# Import shared disclaimers (DDD Principle 1: avoid cross-domain coupling)
from src.shared.disclaimers import (
    REGIONAL_DISCLAIMERS,
    HYPOTHETICAL_DISCLAIMERS,
)

# Supported locales
SUPPORTED_LOCALES = ['en', 'pt-br', 'de', 'es']


# AI Disclosure translations (California SB 942 compliance)
AI_DISCLOSURE = {
    'en': "🤖 This content was generated with artificial intelligence assistance.",
    'pt-br': "🤖 Este conteúdo foi gerado com assistência de inteligência artificial.",
    'de': "🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.",
    'es': "🤖 Este contenido fue generado con asistencia de inteligencia artificial.",
}


# Weekend/Holiday TradFi Gap Disclosure translations
TRADFI_GAP_DISCLOSURE = {
    'weekend': {
        'en': "📅 Note: US stock markets were closed. TradFi data reflects the last trading day.",
        'pt-br': "📅 Nota: Os mercados de ações dos EUA estavam fechados. Dados TradFi refletem o último dia de negociação.",
        'de': "📅 Hinweis: Die US-Aktienmärkte waren geschlossen. TradFi-Daten spiegeln den letzten Handelstag wider.",
        'es': "📅 Nota: Los mercados bursátiles de EE.UU. estaban cerrados. Los datos TradFi reflejan el último día de negociación.",
    },
    'holiday': {
        'en': "📅 Note: US stock markets were closed for a holiday. TradFi data reflects the last trading day.",
        'pt-br': "📅 Nota: Os mercados de ações dos EUA estavam fechados por feriado. Dados TradFi refletem o último dia de negociação.",
        'de': "📅 Hinweis: Die US-Aktienmärkte waren aufgrund eines Feiertags geschlossen. TradFi-Daten spiegeln den letzten Handelstag wider.",
        'es': "📅 Nota: Los mercados bursátiles de EE.UU. estaban cerrados por feriado. Los datos TradFi reflejan el último día de negociación.",
    },
    'pre_market_close': {
        'en': "📅 Note: TradFi data reflects yesterday's close. Today's data will be available after 4PM ET.",
        'pt-br': "📅 Nota: Dados TradFi refletem o fechamento de ontem. Os dados de hoje estarão disponíveis após 17h (horário de Brasília).",
        'de': "📅 Hinweis: TradFi-Daten spiegeln den gestrigen Schlusskurs wider. Die heutigen Daten werden nach 22 Uhr MEZ verfügbar sein.",
        'es': "📅 Nota: Los datos TradFi reflejan el cierre de ayer. Los datos de hoy estarán disponibles después de las 5PM hora del este.",
    },
}


# Note: REGIONAL_DISCLAIMERS and HYPOTHETICAL_DISCLAIMERS are imported
# from src/shared/disclaimers.py at the top of this file.
# They are re-exported for backward compatibility.
