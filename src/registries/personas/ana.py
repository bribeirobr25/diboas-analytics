"""
Ana Persona - Warm Grandmother Voice.

Characteristics:
- Warm and reassuring tone ("grandmother voice")
- High emoji usage (8-15 per newsletter)
- Focus on stability and safety
- Simple explanations, avoids jargon
- Weather metaphors and grandma wisdom
- Targets strategies 1, 3, 5, 7, 9 (0% crypto)

Sign-off: "With care, Adelaide | diBoaS 💙"
"""

import re
from datetime import datetime
from typing import Any, Dict

from src.registries.personas.base import Persona, EmojiLevel, TECHNICAL_TERMS


class AnaPersona(Persona):
    """Ana - Conservative persona with warm grandmother voice."""

    # Ana's emoji palette
    EMOJIS = {
        'title': '💙',
        'greeting_morning': '☕✨',
        'greeting_afternoon': '☀️✨',
        'greeting_evening': '🌙✨',
        'market_calm': '🌤️',
        'market_down': '🌧️',
        'market_up': '☀️',
        'positive': ['✨', '💪', '🎉', '🌸', '💚'],
        'reassuring': ['🙏', '💙', '🤗', '🌺', '💚'],
        'whale': '🐋',
        'strategy': '💚',
        'insight': '💡',
        'closing': ['💚', '🌸', '✨', '🙏', '💙'],
        'caution': ['💭', '🤔'],
        'calm_sea': '⛵',
        'checkmark': '✅',
        'tomato': '🍅',
        'email': '📧',
        'settings': '⚙️',
        'door': '🚪',
        'letter': '💌',
        'clipboard': '📋',
    }

    # Ana's warm phrases by locale
    PHRASES = {
        'en': {
            'greeting_morning': "Good morning, dear!",
            'greeting_afternoon': "Good afternoon, dear!",
            'greeting_evening': "Good evening, dear!",
            'intro_calm': "Adelaide here with your {day} update. Everything is calm today — take a deep breath and enjoy your {time}. Your money is working just fine.",
            'intro_down': "Adelaide here with your {day} update. Markets are a bit cloudy today, but don't worry — this is just temporary weather. Your savings are still safe.",
            'intro_up': "Adelaide here with your {day} update. Markets are sunny today! But remember, we don't get excited about short-term weather.",
            'market_section': "What's Happening in the Markets",
            'market_intro_calm': "Think of it like weather: today is sunny with a slight breeze. Nothing to worry about!",
            'market_intro_down': "Think of it like weather: today is a bit cloudy. But remember, clouds always pass!",
            'market_intro_up': "Think of it like weather: today is bright and sunny! But we know weather changes.",
            'market_meaning': "**What does this mean for you?**\n\nWhen grandma used to see everyone panicking at the market, she knew that's often the best time to stay calm. The big companies aren't worried — only the nervous folks are.\n\n**Your savings:** All safe and working as planned. No need to do anything!",
            'whale_section': "🐋 Watching the Big Wallets",
            'whale_intro': "Remember those big crypto companies that went bankrupt? We're keeping an eye on them so you don't have to.",
            'whale_summary_calm': "**Nothing big moved this week.** Everything is happening slowly and carefully — which is good!",
            'whale_disclaimer': "Large wallet movements are not trading signals. We track them for awareness only.",
            'strategy_section': "Your Strategy Status",
            'strategy_col1': "Your Strategy",
            'strategy_col2': "How's It Doing?",
            'strategy_col3': "What To Do",
            'strategy_note': "Your money is exactly where it should be. The slow-and-steady approach is working.",
            'insight_section': "💡 Grandma's Wisdom",
            'wisdom_note': "This doesn't mean you need to change anything! It's just an observation. Patient people who stayed calm through scary times often did well in the long run.\n\nYour strategy was built for moments like this. Stay the course, or make a change — **it's always your choice, dear.** 💙",
            'closing': "Take care of yourself first",
            'signature': "With care,\n**Adelaide** | diBoaS 💙\n*Building your future, one day at a time*",
            'footer': "📧 Questions? Just reply to this email — I'm here to help! 💌\n⚙️ [Change Your Settings](link) | 🚪 [Unsubscribe](link)",
            'disclaimer': "**Important Notice** 📋\n\n*Remember: Past results don't guarantee future results. Your money can go up or down. This is information, not advice — all decisions are yours. If you're unsure, talk to a financial adviser.*\n\n**You decide what's best for your situation.**",
            'vix_low': "The \"worry meter\" (VIX) is at {vix:.0f} — that's low! Like a calm sea. ⛵",
            'vix_high': "The \"worry meter\" (VIX) is at {vix:.0f} — a bit elevated. But that's okay, we've seen this before.",
            'fear_extreme': "Many people feel very scared right now — but that's often when things are actually fine. 🤔",
            'fear_greed': "Many people feel scared right now — but that's often when things are actually fine. 🤔",
            'fear_neutral': "People are feeling pretty calm about markets right now. 😊",
            'greed': "People are feeling excited about markets — time to stay steady! 🧘",
            'greed_extreme': "People are very excited about markets — grandma says that's when to be most careful! 🤔",
            'grandma_wisdom_fear': "You know what grandma always said? *\"When everyone else is afraid to buy tomatoes at the market, that's often when the prices are best.\"* 🍅",
            'grandma_wisdom_calm': "You know what grandma always said? *\"Slow and steady wins the race.\"* The patient gardener gets the best harvest.",
            'grandma_wisdom_greed': "You know what grandma always said? *\"When everyone's rushing to buy, that's when I take a walk instead.\"* 🚶‍♀️",
            'status_good': "✅ Right on track!",
            'action_relax': "Nothing — relax!",
            'credit_healthy': "Banks and big companies are lending money freely — a good sign! 💚",
        },
        'pt-br': {
            'greeting_morning': "Bom dia, querido(a)!",
            'greeting_afternoon': "Boa tarde, querido(a)!",
            'greeting_evening': "Boa noite, querido(a)!",
            'intro_calm': "Adelaide aqui com sua atualização de {day}. Tudo calmo hoje — respire fundo e aproveite sua {time}. Seu dinheiro está trabalhando direitinho.",
            'intro_down': "Adelaide aqui com sua atualização de {day}. Os mercados estão um pouco nublados hoje, mas não se preocupe — isso é apenas clima temporário. Suas economias ainda estão seguras.",
            'intro_up': "Adelaide aqui com sua atualização de {day}. Os mercados estão ensolarados hoje! Mas lembre-se, não nos animamos com o clima de curto prazo.",
            'market_section': "O Que Está Acontecendo nos Mercados",
            'market_intro_calm': "Pense como o clima: hoje está ensolarado com uma leve brisa. Nada com que se preocupar!",
            'market_intro_down': "Pense como o clima: hoje está um pouco nublado. Mas lembre-se, as nuvens sempre passam!",
            'market_intro_up': "Pense como o clima: hoje está brilhante e ensolarado! Mas sabemos que o clima muda.",
            'market_meaning': "**O que isso significa para você?**\n\nQuando a vovó via todo mundo entrando em pânico no mercado, ela sabia que esse é frequentemente o melhor momento para ficar calmo. As grandes empresas não estão preocupadas — só as pessoas nervosas estão.\n\n**Suas economias:** Todas seguras e trabalhando conforme planejado. Não precisa fazer nada!",
            'whale_section': "🐋 Monitorando as Grandes Carteiras",
            'whale_intro': "Lembra daquelas grandes empresas de cripto que faliram? Estamos de olho nelas para você.",
            'whale_summary_calm': "**Nada grande se moveu esta semana.** Tudo está acontecendo devagar e com cuidado — o que é bom!",
            'whale_disclaimer': "Movimentos de grandes carteiras não são sinais de negociação. Monitoramos apenas para informação.",
            'strategy_section': "Status da Sua Estratégia",
            'strategy_col1': "Sua Estratégia",
            'strategy_col2': "Como Está?",
            'strategy_col3': "O Que Fazer",
            'strategy_note': "Seu dinheiro está exatamente onde deveria estar. A abordagem devagar-e-sempre está funcionando.",
            'insight_section': "💡 Sabedoria da Vovó",
            'wisdom_note': "Isso não significa que você precisa mudar nada! É apenas uma observação. Pessoas pacientes que ficaram calmas durante momentos assustadores frequentemente se saíram bem no longo prazo.\n\nSua estratégia foi construída para momentos como este. Continue no curso, ou faça uma mudança — **é sempre sua escolha, querido(a).** 💙",
            'closing': "Cuide-se primeiro",
            'signature': "Com carinho,\n**Adelaide** | diBoaS 💙\n*Construindo seu futuro, um dia de cada vez*",
            'footer': "📧 Dúvidas? Responda este email — estou aqui para ajudar! 💌\n⚙️ [Alterar Configurações](link) | 🚪 [Cancelar inscrição](link)",
            'disclaimer': "**Aviso Importante** 📋\n\n**AVISO MiCA/CVM:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos. Stablecoins podem perder paridade. Você pode perder todo o capital.\n\n*Lembre-se: Resultados passados não garantem resultados futuros. Seu dinheiro pode subir ou descer. Isto é informação, não aconselhamento — todas as decisões são suas. Se tiver dúvidas, fale com um assessor financeiro.*\n\n**Você decide o que é melhor para sua situação.**",
            'vix_low': "O \"medidor de preocupação\" (VIX) está em {vix:.0f} — isso é baixo! Como um mar calmo. ⛵",
            'vix_high': "O \"medidor de preocupação\" (VIX) está em {vix:.0f} — um pouco elevado. Mas tudo bem, já vimos isso antes.",
            'fear_extreme': "Muitas pessoas estão se sentindo muito assustadas agora — mas é frequentemente quando as coisas estão na verdade bem. 🤔",
            'fear_greed': "Muitas pessoas estão se sentindo assustadas agora — mas é frequentemente quando as coisas estão na verdade bem. 🤔",
            'fear_neutral': "As pessoas estão se sentindo bem calmas sobre os mercados agora. 😊",
            'greed': "As pessoas estão se sentindo animadas sobre os mercados — hora de ficar estável! 🧘",
            'greed_extreme': "As pessoas estão muito animadas sobre os mercados — a vovó diz que é quando devemos ter mais cuidado! 🤔",
            'grandma_wisdom_fear': "Sabe o que a vovó sempre dizia? *\"Quando todo mundo tem medo de comprar tomates na feira, é frequentemente quando os preços estão melhores.\"* 🍅",
            'grandma_wisdom_calm': "Sabe o que a vovó sempre dizia? *\"Devagar e sempre vence a corrida.\"* O jardineiro paciente tem a melhor colheita.",
            'grandma_wisdom_greed': "Sabe o que a vovó sempre dizia? *\"Quando todo mundo está correndo para comprar, é quando eu dou uma caminhada em vez disso.\"* 🚶‍♀️",
            'status_good': "✅ Tudo certo!",
            'action_relax': "Nada — relaxe!",
            'credit_healthy': "Bancos e grandes empresas estão emprestando dinheiro livremente — um bom sinal! 💚",
        },
        'de': {
            'greeting_morning': "Guten Morgen!",
            'greeting_afternoon': "Guten Tag!",
            'greeting_evening': "Guten Abend!",
            'intro_calm': "Adelaide hier mit Ihrem {day}-Update. Heute ist alles ruhig — atmen Sie tief durch und genießen Sie Ihren {time}. Ihr Geld arbeitet einwandfrei.",
            'intro_down': "Adelaide hier mit Ihrem {day}-Update. Die Märkte sind heute etwas bewölkt, aber keine Sorge — das ist nur vorübergehendes Wetter. Ihre Ersparnisse sind noch sicher.",
            'intro_up': "Adelaide hier mit Ihrem {day}-Update. Die Märkte sind heute sonnig! Aber denken Sie daran, wir werden nicht aufgeregt über kurzfristiges Wetter.",
            'market_section': "Was auf den Märkten passiert",
            'market_intro_calm': "Denken Sie an das Wetter: Heute ist es sonnig mit einer leichten Brise. Nichts, worüber Sie sich Sorgen machen müssen!",
            'market_intro_down': "Denken Sie an das Wetter: Heute ist es etwas bewölkt. Aber denken Sie daran, Wolken ziehen immer vorbei!",
            'market_intro_up': "Denken Sie an das Wetter: Heute ist es hell und sonnig! Aber wir wissen, das Wetter ändert sich.",
            'market_meaning': "**Was bedeutet das für Sie?**\n\nWenn Oma alle am Markt in Panik sah, wusste sie, dass das oft der beste Zeitpunkt ist, ruhig zu bleiben. Die großen Unternehmen sind nicht besorgt — nur die nervösen Leute.\n\n**Ihre Ersparnisse:** Alle sicher und arbeiten wie geplant. Sie müssen nichts tun!",
            'whale_section': "🐋 Große Wallets beobachten",
            'whale_intro': "Erinnern Sie sich an die großen Krypto-Unternehmen, die bankrott gingen? Wir behalten sie für Sie im Auge.",
            'whale_summary_calm': "**Diese Woche hat sich nichts Großes bewegt.** Alles passiert langsam und vorsichtig — was gut ist!",
            'whale_disclaimer': "Große Wallet-Bewegungen sind keine Handelssignale. Wir verfolgen sie nur zur Information.",
            'strategy_section': "Status Ihrer Strategie",
            'strategy_col1': "Ihre Strategie",
            'strategy_col2': "Wie geht es?",
            'strategy_col3': "Was zu tun ist",
            'strategy_note': "Ihr Geld ist genau dort, wo es sein sollte. Der langsame und stetige Ansatz funktioniert.",
            'insight_section': "💡 Omas Weisheit",
            'wisdom_note': "Das bedeutet nicht, dass Sie etwas ändern müssen! Es ist nur eine Beobachtung. Geduldige Menschen, die in beängstigenden Zeiten ruhig blieben, haben langfristig oft gut abgeschnitten.\n\nIhre Strategie wurde für Momente wie diesen entwickelt. Bleiben Sie auf Kurs oder machen Sie eine Änderung — **es ist immer Ihre Wahl.** 💙",
            'closing': "Passen Sie zuerst auf sich auf",
            'signature': "Mit freundlichen Grüßen,\n**Adelaide** | diBoaS 💙\n*Wir bauen Ihre Zukunft, einen Tag nach dem anderen*",
            'footer': "📧 Fragen? Antworten Sie einfach auf diese E-Mail — ich bin hier, um zu helfen! 💌\n⚙️ [Einstellungen ändern](link) | 🚪 [Abmelden](link)",
            'disclaimer': "**Wichtiger Hinweis** 📋\n\n**MiCA-HINWEIS:** Kryptowerte werden NICHT durch EU-Einlagensicherungssysteme geschützt. Stablecoins können ihre Bindung verlieren. Sie können Ihr gesamtes Kapital verlieren.\n\n*Denken Sie daran: Vergangene Ergebnisse garantieren keine zukünftigen Ergebnisse. Ihr Geld kann steigen oder fallen. Dies sind Informationen, keine Beratung — alle Entscheidungen liegen bei Ihnen. Wenn Sie unsicher sind, sprechen Sie mit einem Finanzberater.*\n\n**Sie entscheiden, was für Ihre Situation am besten ist.**",
            'vix_low': "Das \"Sorgenbarometer\" (VIX) steht bei {vix:.0f} — das ist niedrig! Wie ein ruhiges Meer. ⛵",
            'vix_high': "Das \"Sorgenbarometer\" (VIX) steht bei {vix:.0f} — etwas erhöht. Aber das ist in Ordnung, wir haben das schon gesehen.",
            'fear_extreme': "Viele Menschen fühlen sich gerade sehr ängstlich — aber das ist oft der Zeitpunkt, wenn alles eigentlich in Ordnung ist. 🤔",
            'fear_greed': "Viele Menschen fühlen sich gerade ängstlich — aber das ist oft der Zeitpunkt, wenn alles eigentlich in Ordnung ist. 🤔",
            'fear_neutral': "Die Menschen fühlen sich ziemlich ruhig bezüglich der Märkte. 😊",
            'greed': "Die Menschen fühlen sich aufgeregt bezüglich der Märkte — Zeit, stabil zu bleiben! 🧘",
            'greed_extreme': "Die Menschen sind sehr aufgeregt bezüglich der Märkte — Oma sagt, das ist der Zeitpunkt für Vorsicht! 🤔",
            'grandma_wisdom_fear': "Wissen Sie, was Oma immer sagte? *\"Wenn alle Angst haben, Tomaten auf dem Markt zu kaufen, sind die Preise oft am besten.\"* 🍅",
            'grandma_wisdom_calm': "Wissen Sie, was Oma immer sagte? *\"Langsam und stetig gewinnt das Rennen.\"* Der geduldige Gärtner hat die beste Ernte.",
            'grandma_wisdom_greed': "Wissen Sie, was Oma immer sagte? *\"Wenn alle eilen, um zu kaufen, mache ich stattdessen einen Spaziergang.\"* 🚶‍♀️",
            'status_good': "✅ Auf Kurs!",
            'action_relax': "Nichts — entspannen Sie sich!",
            'credit_healthy': "Banken und große Unternehmen verleihen Geld frei — ein gutes Zeichen! 💚",
        },
        'es': {
            'greeting_morning': "¡Buenos días, querido(a)!",
            'greeting_afternoon': "¡Buenas tardes, querido(a)!",
            'greeting_evening': "¡Buenas noches, querido(a)!",
            'intro_calm': "Adelaide aquí con su actualización de {day}. Todo tranquilo hoy — respire profundo y disfrute de su {time}. Su dinero está trabajando bien.",
            'intro_down': "Adelaide aquí con su actualización de {day}. Los mercados están un poco nublados hoy, pero no se preocupe — esto es solo clima temporal. Sus ahorros siguen seguros.",
            'intro_up': "Adelaide aquí con su actualización de {day}. ¡Los mercados están soleados hoy! Pero recuerde, no nos emocionamos por el clima a corto plazo.",
            'market_section': "Lo Que Está Pasando en los Mercados",
            'market_intro_calm': "Piense en el clima: hoy está soleado con una brisa ligera. ¡Nada de qué preocuparse!",
            'market_intro_down': "Piense en el clima: hoy está un poco nublado. ¡Pero recuerde, las nubes siempre pasan!",
            'market_intro_up': "Piense en el clima: ¡hoy está brillante y soleado! Pero sabemos que el clima cambia.",
            'market_meaning': "**¿Qué significa esto para usted?**\n\nCuando la abuela veía a todos entrando en pánico en el mercado, sabía que ese es frecuentemente el mejor momento para mantener la calma. Las grandes empresas no están preocupadas — solo los nerviosos lo están.\n\n**Sus ahorros:** Todos seguros y trabajando según lo planeado. ¡No necesita hacer nada!",
            'whale_section': "🐋 Observando las Grandes Carteras",
            'whale_intro': "¿Recuerda esas grandes empresas de cripto que quebraron? Las estamos vigilando por usted.",
            'whale_summary_calm': "**Nada grande se movió esta semana.** Todo está sucediendo despacio y con cuidado — ¡lo cual es bueno!",
            'whale_disclaimer': "Los movimientos de grandes carteras no son señales de trading. Los monitoreamos solo para información.",
            'strategy_section': "Estado de Su Estrategia",
            'strategy_col1': "Su Estrategia",
            'strategy_col2': "¿Cómo Está?",
            'strategy_col3': "Qué Hacer",
            'strategy_note': "Su dinero está exactamente donde debe estar. El enfoque lento y constante está funcionando.",
            'insight_section': "💡 Sabiduría de la Abuela",
            'wisdom_note': "¡Esto no significa que necesite cambiar nada! Es solo una observación. Las personas pacientes que se mantuvieron tranquilas durante momentos aterradores frecuentemente les fue bien a largo plazo.\n\nSu estrategia fue construida para momentos como este. Continúe el curso, o haga un cambio — **siempre es su elección, querido(a).** 💙",
            'closing': "Cuídese primero",
            'signature': "Con cariño,\n**Adelaide** | diBoaS 💙\n*Construyendo su futuro, un día a la vez*",
            'footer': "📧 ¿Preguntas? ¡Responda a este correo — estoy aquí para ayudar! 💌\n⚙️ [Cambiar Configuración](link) | 🚪 [Cancelar suscripción](link)",
            'disclaimer': "**Aviso Importante** 📋\n\n**AVISO MiCA:** Los criptoactivos NO están protegidos por sistemas de garantía de depósitos de la UE. Las stablecoins pueden perder paridad. Usted puede perder todo su capital.\n\n*Recuerde: Los resultados pasados no garantizan resultados futuros. Su dinero puede subir o bajar. Esto es información, no asesoramiento — todas las decisiones son suyas. Si tiene dudas, hable con un asesor financiero.*\n\n**Usted decide lo que es mejor para su situación.**",
            'vix_low': "El \"medidor de preocupación\" (VIX) está en {vix:.0f} — ¡eso es bajo! Como un mar en calma. ⛵",
            'vix_high': "El \"medidor de preocupación\" (VIX) está en {vix:.0f} — un poco elevado. Pero está bien, ya hemos visto esto antes.",
            'fear_extreme': "Muchas personas se sienten muy asustadas ahora — pero frecuentemente es cuando las cosas están en realidad bien. 🤔",
            'fear_greed': "Muchas personas se sienten asustadas ahora — pero frecuentemente es cuando las cosas están en realidad bien. 🤔",
            'fear_neutral': "Las personas se sienten bastante tranquilas sobre los mercados ahora. 😊",
            'greed': "Las personas se sienten emocionadas sobre los mercados — ¡hora de mantenerse estable! 🧘",
            'greed_extreme': "Las personas están muy emocionadas sobre los mercados — ¡la abuela dice que es cuando hay que tener más cuidado! 🤔",
            'grandma_wisdom_fear': "¿Sabe lo que la abuela siempre decía? *\"Cuando todos tienen miedo de comprar tomates en el mercado, frecuentemente es cuando los precios están mejores.\"* 🍅",
            'grandma_wisdom_calm': "¿Sabe lo que la abuela siempre decía? *\"Lento y constante gana la carrera.\"* El jardinero paciente tiene la mejor cosecha.",
            'grandma_wisdom_greed': "¿Sabe lo que la abuela siempre decía? *\"Cuando todos corren a comprar, es cuando doy un paseo.\"* 🚶‍♀️",
            'status_good': "✅ ¡Todo bien!",
            'action_relax': "Nada — ¡relájese!",
            'credit_healthy': "Bancos y grandes empresas están prestando dinero libremente — ¡una buena señal! 💚",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """
        Adapt content to Ana's warm, reassuring voice.

        Transformations:
        - Add emojis throughout (8-15 total)
        - Simplify technical terms
        - Add warm greetings and closings
        - Add grandma wisdom
        - Use weather metaphors
        - Shorten sentences (15 words max)
        """
        adapted = content.copy()
        adapted['persona'] = 'ana'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        # Get locale-specific phrases
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # Determine time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_of_day = 'morning'
            time_word = 'morning'
        elif 12 <= hour < 18:
            time_of_day = 'afternoon'
            time_word = 'afternoon'
        else:
            time_of_day = 'evening'
            time_word = 'evening'

        # Get day of week
        day_name = datetime.now().strftime('%A')

        # Title emoji
        adapted['title_emoji'] = self.EMOJIS['title']

        # Persona greeting with emojis
        greeting = phrases[f'greeting_{time_of_day}']
        emoji = self.EMOJIS[f'greeting_{time_of_day}']
        adapted['persona_greeting'] = f"{greeting} {emoji}"

        # Market regime affects intro
        btc_change = content.get('btc_24h_change', 0)
        if btc_change < -3:
            intro_key = 'intro_down'
            market_emoji = self.EMOJIS['market_down']
            market_intro = phrases.get('market_intro_down', phrases['market_intro_calm'])
        elif btc_change > 3:
            intro_key = 'intro_up'
            market_emoji = self.EMOJIS['market_up']
            market_intro = phrases.get('market_intro_up', phrases['market_intro_calm'])
        else:
            intro_key = 'intro_calm'
            market_emoji = self.EMOJIS['market_calm']
            market_intro = phrases['market_intro_calm']

        adapted['greeting_message'] = phrases[intro_key].format(day=day_name, time=time_word) + " 💪"
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = market_emoji
        adapted['market_intro'] = market_intro

        # Build market bullets based on data
        bullets = self._build_market_bullets(content, phrases)
        adapted['market_bullets'] = bullets

        # Fear & Greed emoji
        fg = content.get('fear_greed_index', 50)
        if fg <= 25:
            adapted['fear_greed_emoji'] = '😰'
        elif fg <= 45:
            adapted['fear_greed_emoji'] = '😟'
        elif fg <= 55:
            adapted['fear_greed_emoji'] = '😐'
        elif fg <= 75:
            adapted['fear_greed_emoji'] = '😊'
        else:
            adapted['fear_greed_emoji'] = '🤑'

        # Market meaning section
        adapted['market_meaning'] = phrases['market_meaning'] + " " + self.EMOJIS['checkmark']

        # Whale section
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary_calm'] + " " + self.EMOJIS['reassuring'][0]
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = self.EMOJIS['strategy']
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Your Strategy')
        adapted['strategy_col2'] = phrases.get('strategy_col2', "How's It Doing?")
        adapted['strategy_col3'] = phrases.get('strategy_col3', 'What To Do')
        adapted['conservative_status'] = phrases.get('status_good', '✅ On track')
        adapted['conservative_action'] = phrases.get('action_relax', 'Nothing — relax!')
        adapted['balanced_status'] = phrases.get('status_good', '✅ On track')
        adapted['balanced_action'] = phrases.get('action_relax', 'Nothing — relax!')
        adapted['growth_status'] = phrases.get('status_good', '✅ On track')
        adapted['growth_action'] = phrases.get('action_relax', 'Nothing — relax!')
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section with grandma wisdom
        adapted['insight_section_title'] = phrases['insight_section']

        # Add grandma wisdom based on market sentiment
        if fg <= 25:
            wisdom = phrases.get('grandma_wisdom_fear', '')
        elif fg >= 75:
            wisdom = phrases.get('grandma_wisdom_greed', '')
        else:
            wisdom = phrases.get('grandma_wisdom_calm', '')

        adapted['wisdom_note'] = phrases['wisdom_note']

        # If insight_content exists, prepend with wisdom
        if 'insight_content' in adapted and wisdom:
            adapted['insight_content'] = self._simplify_text(adapted.get('insight_content', ''))
            adapted['insight_content'] = f"{wisdom}\n\n{adapted['insight_content']}"

        # Closing
        adapted['closing_wisdom'] = f"{phrases['closing']} {self.EMOJIS['closing'][0]}"

        # Disclaimer
        adapted['disclaimer'] = phrases['disclaimer']

        # Footer
        adapted['footer'] = phrases['footer']

        # Signature
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_market_bullets(self, content: Dict, phrases: Dict) -> str:
        """Build market bullet points for Ana."""
        bullets = []

        vix = content.get('vix', 20)
        if vix < 20:
            bullets.append("- " + phrases.get('vix_low', '').format(vix=vix))
        else:
            bullets.append("- " + phrases.get('vix_high', '').format(vix=vix))

        # Use localized credit health phrase
        credit_healthy = phrases.get('credit_healthy', "Banks and big companies are lending money freely — a good sign! 💚")
        bullets.append("- " + credit_healthy)

        fg = content.get('fear_greed_index', 50)
        if fg <= 25:
            bullets.append("- " + phrases.get('fear_extreme', ''))
        elif fg <= 45:
            bullets.append("- " + phrases.get('fear_greed', ''))
        elif fg <= 55:
            bullets.append("- " + phrases.get('fear_neutral', ''))
        elif fg <= 75:
            bullets.append("- " + phrases.get('greed', ''))
        else:
            bullets.append("- " + phrases.get('greed_extreme', ''))

        return '\n'.join(bullets)

    def _simplify_text(self, text: str) -> str:
        """Replace technical terms with simple language."""
        result = text
        for technical, simple in TECHNICAL_TERMS.items():
            result = re.sub(
                rf'\b{technical}\b',
                simple,
                result,
                flags=re.IGNORECASE
            )
        return result

    @property
    def name(self) -> str:
        return "Ana"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.HIGH

    @property
    def risk_profile(self) -> str:
        return "conservative"

    def get_signature(self, locale: str = "en") -> str:
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        return phrases.get('signature', "With care,\n**Adelaide** | diBoaS 💙")
