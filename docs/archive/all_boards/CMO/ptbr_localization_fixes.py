"""
PT-BR Localization Fixes for Adelaide

These fixes address:
1. English phrase leakage in Ana persona
2. Missing UTF-8 accents (ASCII approximations)
3. Missing PT-BR phrases

CMO Board Session 010 - February 4, 2026

INSTRUCTIONS:
1. Replace TRANSLATIONS['pt-br'] in src/adelaide/localization.py with FIXED_PTBR_TRANSLATIONS below
2. Replace REGIONAL_DISCLAIMERS['pt-br'] with FIXED_PTBR_DISCLAIMER below
3. Add AI_DISCLOSURES dict to localization.py
4. Update AnaPersona.PHRASES['pt-br'] in persona_registry.py with FIXED_ANA_PTBR_PHRASES below
5. Fix _build_market_bullets() method in AnaPersona class
"""

# =============================================================================
# 1. FIXED PT-BR TRANSLATIONS (src/adelaide/localization.py)
# =============================================================================

FIXED_PTBR_TRANSLATIONS = {
    # Greetings - with proper accents
    'good_morning': 'Bom dia',
    'good_afternoon': 'Boa tarde',
    'good_evening': 'Boa noite',

    # Common phrases - with proper accents
    'dear': 'Querido(a)',
    'friend': 'amigo(a)',
    'with_care': 'Com carinho',
    'you_decide': 'Você decide o que é melhor para sua situação.',

    # Market terms - with proper accents
    'market_snapshot': 'Panorama do Mercado',
    'fear_greed_index': 'Índice de Medo e Ganância',
    'whale_watch': 'Monitoramento de Baleias',
    'strategy_overview': 'Visão das Estratégias',

    # Labels - with proper accents
    'conservative': 'Conservador',
    'balanced': 'Equilibrado',
    'growth': 'Crescimento',
    'status': 'Status',
    'performance': 'Desempenho',

    # Status - with proper accents
    'normal': 'Normal',
    'elevated': 'Elevado',
    'warning': 'Atenção',

    # Sentiments - with proper accents
    'extreme_fear': 'Medo Extremo',
    'fear': 'Medo',
    'neutral': 'Neutro',
    'greed': 'Ganância',
    'extreme_greed': 'Ganância Extrema',

    # Disclaimers - with proper accents
    'disclaimer_header': 'Avisos Importantes',
    'not_financial_advice': 'Este é conteúdo educacional apenas, não aconselhamento financeiro.',
    'past_performance': 'Desempenho passado não garante resultados futuros.',
    'consult_adviser': 'Considere consultar um assessor financeiro licenciado para orientação personalizada.',

    # Ana-specific - with proper accents
    'dont_worry': 'Não se preocupe, querido(a)',
    'take_a_breath': 'Vamos respirar juntos',
    'youre_doing_great': 'Você está indo muito bem',
    'slow_and_steady': 'Devagar e sempre',

    # MiCA/CVM warning - with proper accents
    'mica_warning': 'AVISO: Criptoativos NÃO são protegidos por esquemas de garantia de depósitos da UE. Stablecoins podem perder paridade. Você pode perder todo o capital.',
    
    # AI Disclosure (California SB 942) - NEW
    'ai_disclosure': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
    
    # Table headers - NEW
    'table_asset': 'Ativo',
    'table_price': 'Preço',
    'table_change': 'Variação 24h',
    'table_who': 'Quem',
    'table_what': 'O Que Têm',
    'table_happening': 'O Que Está Acontecendo',
    
    # Section titles - NEW
    'whats_next': 'O Que Vem a Seguir',
    'heres_what_numbers_say': 'Veja o que os números dizem:',
}


# =============================================================================
# 2. FIXED PT-BR REGIONAL DISCLAIMER (src/adelaide/localization.py)
# =============================================================================

FIXED_PTBR_DISCLAIMER = """**Avisos Importantes de Conformidade**

**AVISO 1 - PROTEÇÃO AO INVESTIDOR:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos ou fundos de compensação ao investidor.

**AVISO 2 - RISCO DE PERDA:** O valor dos seus investimentos pode diminuir ou aumentar. Você pode perder parte ou todo o capital investido.

**AVISO 3 - ORIENTAÇÃO PROFISSIONAL:** Considere consultar um assessor financeiro ou profissional habilitado pela CVM para orientação específica à sua situação.

Este conteúdo é apenas para fins educacionais e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.

Desempenho passado não é indicativo de resultados futuros.

**Direito de reclamação:** [contato@diboas.com]

*Você decide o que é melhor para sua situação.*"""


# =============================================================================
# 3. AI DISCLOSURES (add to src/adelaide/localization.py)
# =============================================================================

AI_DISCLOSURES = {
    'en': '🤖 This content was generated with artificial intelligence assistance.',
    'pt-br': '🤖 Este conteúdo foi gerado com assistência de inteligência artificial.',
    'de': '🤖 Dieser Inhalt wurde mit Unterstützung künstlicher Intelligenz erstellt.',
    'es': '🤖 Este contenido fue generado con asistencia de inteligencia artificial.',
}


# =============================================================================
# 4. FIXED ANA PT-BR PHRASES (src/registries/persona_registry.py)
# =============================================================================

FIXED_ANA_PTBR_PHRASES = {
    # Greetings
    'greeting_morning': 'Bom dia, querido(a)!',
    'greeting_afternoon': 'Boa tarde, querido(a)!',
    'greeting_evening': 'Boa noite, querido(a)!',
    
    # Intro messages
    'intro_calm': 'Adelaide aqui com sua atualização de {day}. Tudo calmo hoje — respire fundo e aproveite sua {time}. Seu dinheiro está trabalhando direitinho.',
    'intro_down': 'Adelaide aqui com sua atualização de {day}. Os mercados estão um pouco nublados hoje, mas não se preocupe — isso é apenas clima temporário. Suas economias ainda estão seguras.',
    'intro_up': 'Adelaide aqui com sua atualização de {day}. Os mercados estão ensolarados hoje! Mas lembre-se, não nos animamos com o clima de curto prazo.',
    
    # Section titles
    'market_section': 'O Que Está Acontecendo nos Mercados',
    'market_intro_calm': 'Pense como o clima: hoje está ensolarado com uma leve brisa. Nada com que se preocupar!',
    'market_intro_down': 'Pense como o clima: hoje está um pouco nublado. Mas lembre-se, as nuvens sempre passam!',
    'market_intro_up': 'Pense como o clima: hoje está brilhante e ensolarado! Mas sabemos que o clima muda.',
    
    # Market meaning
    'market_meaning': '**O que isso significa para você?**\n\nQuando a vovó via todo mundo entrando em pânico no mercado, ela sabia que esse é frequentemente o melhor momento para ficar calmo. As grandes empresas não estão preocupadas — só as pessoas nervosas estão.\n\n**Suas economias:** Todas seguras e trabalhando conforme planejado. Não precisa fazer nada!',
    
    # Whale section
    'whale_section': '🐋 Monitorando as Grandes Carteiras',
    'whale_intro': 'Lembra daquelas grandes empresas de cripto que faliram? Estamos de olho nelas para você.',
    'whale_summary_calm': '**Nada grande se moveu esta semana.** Tudo está acontecendo devagar e com cuidado — o que é bom!',
    'whale_disclaimer': 'Movimentos de grandes carteiras não são sinais de negociação. Monitoramos apenas para informação.',
    
    # Strategy section
    'strategy_section': 'Status da Sua Estratégia',
    'strategy_col1': 'Sua Estratégia',
    'strategy_col2': 'Como Está?',
    'strategy_col3': 'O Que Fazer',
    'strategy_note': 'Seu dinheiro está exatamente onde deveria estar. A abordagem devagar-e-sempre está funcionando.',
    
    # Insight section
    'insight_section': '💡 Sabedoria da Vovó',
    'wisdom_note': 'Isso não significa que você precisa mudar nada! É apenas uma observação. Pessoas pacientes que ficaram calmas durante momentos assustadores frequentemente se saíram bem no longo prazo.\n\nSua estratégia foi construída para momentos como este. Continue no curso, ou faça uma mudança — **é sempre sua escolha, querido(a).** 💙',
    
    # Closing
    'closing': 'Cuide-se primeiro',
    'signature': 'Com carinho,\n**Adelaide** | diBoaS 💙\n*Construindo seu futuro, um dia de cada vez*',
    'footer': '📧 Dúvidas? Responda este email — estou aqui para ajudar! 💌\n⚙️ [Alterar Configurações](link) | 🚪 [Cancelar inscrição](link)',
    
    # VIX phrases
    'vix_low': 'O "medidor de preocupação" (VIX) está em {vix:.0f} — isso é baixo! Como um mar calmo. ⛵',
    'vix_high': 'O "medidor de preocupação" (VIX) está em {vix:.0f} — um pouco elevado. Mas tudo bem, já vimos isso antes.',
    
    # Credit health - FIX FOR ENGLISH LEAKAGE
    'credit_healthy': 'Bancos e grandes empresas estão emprestando dinheiro livremente — um bom sinal! 💚',
    
    # Fear/Greed phrases
    'fear_extreme': 'Muitas pessoas estão se sentindo muito assustadas agora — mas é frequentemente quando as coisas estão na verdade bem. 🤔',
    'fear_greed': 'Muitas pessoas estão se sentindo assustadas agora — mas é frequentemente quando as coisas estão na verdade bem. 🤔',
    'fear_neutral': 'As pessoas estão se sentindo bem calmas sobre os mercados agora. 😊',
    'greed': 'As pessoas estão se sentindo animadas sobre os mercados — hora de ficar estável! 🧘',
    'greed_extreme': 'As pessoas estão muito animadas sobre os mercados — a vovó diz que é quando devemos ter mais cuidado! 🤔',
    
    # Grandma wisdom
    'grandma_wisdom_fear': 'Sabe o que a vovó sempre dizia? *"Quando todo mundo tem medo de comprar tomates na feira, é frequentemente quando os preços estão melhores."* 🍅',
    'grandma_wisdom_calm': 'Sabe o que a vovó sempre dizia? *"Devagar e sempre vence a corrida."* O jardineiro paciente tem a melhor colheita.',
    'grandma_wisdom_greed': 'Sabe o que a vovó sempre dizia? *"Quando todo mundo está correndo para comprar, é quando eu dou uma caminhada em vez disso."* 🚶‍♀️',
    
    # Status
    'status_good': '✅ Tudo certo!',
    'action_relax': 'Nada — relaxe!',
    
    # Disclaimer (full CVM compliance)
    'disclaimer': """**Avisos Importantes de Conformidade**

**AVISO 1 - PROTEÇÃO AO INVESTIDOR:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos ou fundos de compensação ao investidor.

**AVISO 2 - RISCO DE PERDA:** O valor dos seus investimentos pode diminuir ou aumentar. Você pode perder parte ou todo o capital investido.

**AVISO 3 - ORIENTAÇÃO PROFISSIONAL:** Considere consultar um assessor financeiro ou profissional habilitado pela CVM para orientação específica à sua situação.

Este conteúdo é apenas para fins educacionais e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.

Desempenho passado não é indicativo de resultados futuros.

**Direito de reclamação:** [contato@diboas.com]

*Você decide o que é melhor para sua situação.*""",
}


# =============================================================================
# 5. FIXED _build_market_bullets() METHOD (src/registries/persona_registry.py)
# =============================================================================

def fixed_build_market_bullets(self, content: dict, phrases: dict) -> str:
    """
    Build market bullet points for Ana - FIXED VERSION.
    
    Replaces the original method in AnaPersona class.
    Now uses localized phrases for all content.
    """
    bullets = []
    
    # VIX bullet - localized
    vix = content.get('vix', 20)
    if vix < 20:
        vix_phrase = phrases.get('vix_low', 'The "worry meter" (VIX) is at {vix:.0f} — that\'s low! Like a calm sea. ⛵')
    else:
        vix_phrase = phrases.get('vix_high', 'The "worry meter" (VIX) is at {vix:.0f} — a bit elevated. But that\'s okay, we\'ve seen this before.')
    bullets.append("- " + vix_phrase.format(vix=vix))
    
    # Credit health bullet - NOW LOCALIZED (was hardcoded English before)
    credit_phrase = phrases.get('credit_healthy', 'Banks and big companies are lending money freely — a good sign! 💚')
    bullets.append("- " + credit_phrase)
    
    # Fear/Greed bullet - localized
    fg = content.get('fear_greed_index', 50)
    if fg <= 25:
        fg_phrase = phrases.get('fear_extreme', 'Many people feel very scared right now — but that\'s often when things are actually fine. 🤔')
    elif fg <= 45:
        fg_phrase = phrases.get('fear_greed', 'Many people feel scared right now — but that\'s often when things are actually fine. 🤔')
    elif fg <= 55:
        fg_phrase = phrases.get('fear_neutral', 'People are feeling pretty calm about markets right now. 😊')
    elif fg <= 75:
        fg_phrase = phrases.get('greed', 'People are feeling excited about markets — time to stay steady! 🧘')
    else:
        fg_phrase = phrases.get('greed_extreme', 'People are very excited about markets — grandma says that\'s when to be most careful! 🤔')
    bullets.append("- " + fg_phrase)
    
    return '\n'.join(bullets)


# =============================================================================
# IMPLEMENTATION INSTRUCTIONS
# =============================================================================

IMPLEMENTATION_INSTRUCTIONS = """
STEP-BY-STEP IMPLEMENTATION:

1. src/adelaide/localization.py:
   - Replace TRANSLATIONS['pt-br'] with FIXED_PTBR_TRANSLATIONS
   - Replace REGIONAL_DISCLAIMERS['pt-br'] with FIXED_PTBR_DISCLAIMER
   - Add AI_DISCLOSURES dict at module level
   - Add method to LocalizationEngine:
     
     def get_ai_disclosure(self, locale: str = None) -> str:
         locale = locale or self.default_locale
         return AI_DISCLOSURES.get(locale, AI_DISCLOSURES['en'])

2. src/registries/persona_registry.py:
   - Replace AnaPersona.PHRASES['pt-br'] with FIXED_ANA_PTBR_PHRASES
   - Replace AnaPersona._build_market_bullets() with fixed_build_market_bullets()

3. src/adelaide/templates/*.md:
   - Add {{ai_disclosure}} placeholder after {{signature}} in all templates:
     
     {{signature}}
     
     ---
     
     {{ai_disclosure}}
     
     {{footer}}

4. src/adelaide/generator.py:
   - In _prepare_content_data(), add:
     
     # AI Disclosure (California SB 942 compliance)
     data['ai_disclosure'] = self.localization.get_ai_disclosure(locale)

5. Test all combinations:
   - python main.py adelaide --persona=ana --locale=pt-br
   - python main.py adelaide --persona=maria --locale=pt-br
   - python main.py adelaide --persona=felipe --locale=pt-br
   - Verify NO English phrases appear in PT-BR output
   - Verify all accents render correctly (não, você, situação, etc.)
   - Verify AI disclosure appears in all outputs
"""

if __name__ == "__main__":
    print(IMPLEMENTATION_INSTRUCTIONS)
