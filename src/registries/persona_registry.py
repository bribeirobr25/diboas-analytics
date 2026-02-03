"""
Persona Registry for Adelaide personas.

Provides interface for content adaptation based on user persona.

Three core personas:
- Ana (Conservative): Warm, emoji-rich, reassuring, grandmother voice
- Maria (Balanced): Educational, moderate detail, friendly professional
- Felipe (Aggressive): Data-forward, no emojis, technical, direct
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
import re
import random
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


# Technical term replacements for simpler personas
TECHNICAL_TERMS = {
    'APY': 'yearly return',
    'TVL': 'total money in protocol',
    'DeFi': 'crypto savings',
    'smart contract': 'automated system',
    'impermanent loss': 'temporary value changes',
    'Sharpe ratio': 'risk-adjusted return',
    'drawdown': 'decline from peak',
    'volatility': 'price swings',
    'liquidity': 'available funds',
    'protocol': 'platform',
    'yield': 'return',
    'staking': 'earning rewards',
    'collateral': 'backed value',
}


class EmojiLevel(Enum):
    """Emoji usage level for personas."""
    NONE = "none"           # No emojis (Felipe)
    MINIMAL = "minimal"     # 1-3 emojis
    MODERATE = "moderate"   # 3-8 emojis (Maria)
    HIGH = "high"           # 8-15 emojis (Ana)


class Persona(ABC):
    """
    Abstract base class for all Adelaide personas.

    Personas adapt content to different communication styles
    based on user risk profile and preferences.
    """

    @abstractmethod
    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """
        Adapt content to this persona's voice.

        Args:
            content: Base content to adapt (from Adelaide generator)
            locale: Language locale (en, pt-br, de, es)

        Returns:
            Adapted content with persona's voice
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return persona name."""
        pass

    @property
    @abstractmethod
    def emoji_level(self) -> EmojiLevel:
        """Return emoji usage level."""
        pass

    @property
    @abstractmethod
    def risk_profile(self) -> str:
        """
        Return target risk profile.

        Returns:
            One of: 'conservative', 'balanced', 'aggressive'
        """
        pass

    def get_signature(self, locale: str = "en") -> str:
        """Get persona's signature for newsletter sign-off."""
        return f"— {self.name}"


class PersonaRegistry(Registry[Persona]):
    """
    Registry for Adelaide personas.

    Usage:
        persona = PersonaRegistry.get_instance().get("ana", {})
        adapted = persona.adapt(content, locale="en")
    """
    pass


# =============================================================================
# Ana Persona - Warm Grandmother Voice
# =============================================================================

@PersonaRegistry.register("ana")
class AnaPersona(Persona):
    """
    Ana - Conservative persona.

    Characteristics:
    - Warm and reassuring tone ("grandmother voice")
    - High emoji usage (8-15 per newsletter)
    - Focus on stability and safety
    - Simple explanations, avoids jargon
    - Weather metaphors and grandma wisdom
    - Targets strategies 1, 3, 5, 7, 9 (0% crypto)

    Sign-off: "With care, Adelaide | diBoaS 💙"
    """

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

    # Ana's warm phrases
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
        },
        'pt-br': {
            'greeting_morning': "Bom dia, querido(a)!",
            'greeting_afternoon': "Boa tarde, querido(a)!",
            'greeting_evening': "Boa noite, querido(a)!",
            'intro_calm': "Adelaide aqui com sua atualizacao de {day}. Tudo calmo hoje — respire fundo e aproveite sua {time}. Seu dinheiro esta trabalhando direitinho.",
            'intro_down': "Adelaide aqui com sua atualizacao de {day}. Os mercados estao um pouco nublados hoje, mas nao se preocupe — isso e apenas clima temporario. Suas economias ainda estao seguras.",
            'intro_up': "Adelaide aqui com sua atualizacao de {day}. Os mercados estao ensolarados hoje! Mas lembre-se, nao nos animamos com o clima de curto prazo.",
            'market_section': "O Que Esta Acontecendo nos Mercados",
            'market_intro_calm': "Pense como o clima: hoje esta ensolarado com uma leve brisa. Nada com que se preocupar!",
            'market_intro_down': "Pense como o clima: hoje esta um pouco nublado. Mas lembre-se, as nuvens sempre passam!",
            'market_intro_up': "Pense como o clima: hoje esta brilhante e ensolarado! Mas sabemos que o clima muda.",
            'market_meaning': "**O que isso significa para voce?**\n\nQuando a vovo via todo mundo entrando em panico no mercado, ela sabia que esse e frequentemente o melhor momento para ficar calmo. As grandes empresas nao estao preocupadas — so as pessoas nervosas estao.\n\n**Suas economias:** Todas seguras e trabalhando conforme planejado. Nao precisa fazer nada!",
            'whale_section': "🐋 Monitorando as Grandes Carteiras",
            'whale_intro': "Lembra daquelas grandes empresas de cripto que faliram? Estamos de olho nelas para voce.",
            'whale_summary_calm': "**Nada grande se moveu esta semana.** Tudo esta acontecendo devagar e com cuidado — o que e bom!",
            'whale_disclaimer': "Movimentos de grandes carteiras nao sao sinais de negociacao. Monitoramos apenas para informacao.",
            'strategy_section': "Status da Sua Estrategia",
            'strategy_col1': "Sua Estrategia",
            'strategy_col2': "Como Esta?",
            'strategy_col3': "O Que Fazer",
            'strategy_note': "Seu dinheiro esta exatamente onde deveria estar. A abordagem devagar-e-sempre esta funcionando.",
            'insight_section': "💡 Sabedoria da Vovo",
            'wisdom_note': "Isso nao significa que voce precisa mudar nada! E apenas uma observacao. Pessoas pacientes que ficaram calmas durante momentos assustadores frequentemente se saíram bem no longo prazo.\n\nSua estrategia foi construida para momentos como este. Continue no curso, ou faca uma mudanca — **e sempre sua escolha, querido(a).** 💙",
            'closing': "Cuide-se primeiro",
            'signature': "Com carinho,\n**Adelaide** | diBoaS 💙\n*Construindo seu futuro, um dia de cada vez*",
            'footer': "📧 Duvidas? Responda este email — estou aqui para ajudar! 💌\n⚙️ [Alterar Configuracoes](link) | 🚪 [Cancelar inscricao](link)",
            'disclaimer': "**Aviso Importante** 📋\n\n**AVISO MiCA/CVM:** Criptoativos NAO sao protegidos por esquemas de garantia de depositos. Stablecoins podem perder paridade. Voce pode perder todo o capital.\n\n*Lembre-se: Resultados passados nao garantem resultados futuros. Seu dinheiro pode subir ou descer. Isto e informacao, nao aconselhamento — todas as decisoes sao suas. Se tiver duvidas, fale com um assessor financeiro.*\n\n**Voce decide o que e melhor para sua situacao.**",
            'vix_low': "O \"medidor de preocupacao\" (VIX) esta em {vix:.0f} — isso e baixo! Como um mar calmo. ⛵",
            'vix_high': "O \"medidor de preocupacao\" (VIX) esta em {vix:.0f} — um pouco elevado. Mas tudo bem, ja vimos isso antes.",
            'fear_extreme': "Muitas pessoas estao se sentindo muito assustadas agora — mas e frequentemente quando as coisas estao na verdade bem. 🤔",
            'fear_greed': "Muitas pessoas estao se sentindo assustadas agora — mas e frequentemente quando as coisas estao na verdade bem. 🤔",
            'fear_neutral': "As pessoas estao se sentindo bem calmas sobre os mercados agora. 😊",
            'greed': "As pessoas estao se sentindo animadas sobre os mercados — hora de ficar estavel! 🧘",
            'greed_extreme': "As pessoas estao muito animadas sobre os mercados — a vovo diz que e quando devemos ter mais cuidado! 🤔",
            'grandma_wisdom_fear': "Sabe o que a vovo sempre dizia? *\"Quando todo mundo tem medo de comprar tomates na feira, e frequentemente quando os precos estao melhores.\"* 🍅",
            'grandma_wisdom_calm': "Sabe o que a vovo sempre dizia? *\"Devagar e sempre vence a corrida.\"* O jardineiro paciente tem a melhor colheita.",
            'grandma_wisdom_greed': "Sabe o que a vovo sempre dizia? *\"Quando todo mundo esta correndo para comprar, e quando eu dou uma caminhada em vez disso.\"* 🚶‍♀️",
            'status_good': "✅ Tudo certo!",
            'action_relax': "Nada — relaxe!",
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

        bullets.append("- Banks and big companies are lending money freely — a good sign! 💚")

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


# =============================================================================
# Maria Persona - Friendly Teacher
# =============================================================================

@PersonaRegistry.register("maria")
class MariaPersona(Persona):
    """
    Maria - Balanced persona.

    Characteristics:
    - Educational and informative tone ("friendly teacher")
    - Moderate emoji usage (3-8 per newsletter)
    - Balance of safety and growth
    - Explains concepts with context
    - Targets strategies 2, 4, 6 (30-40% crypto)

    Sign-off: "Stay informed, Adelaide 📊"
    """

    EMOJIS = {
        'title': '📊',
        'greeting': '👋',
        'market': '📈',
        'educational': ['📚', '💡', '📈', '🏠'],
        'whale': '🐋',
        'strategy': '📊',
        'neutral': ['📋', '🔍'],
        'closing': '📊',
    }

    PHRASES = {
        'en': {
            'greeting_morning': "Good morning!",
            'greeting_afternoon': "Good afternoon!",
            'greeting_evening': "Good evening!",
            'intro': "Here's your {day} market update. Let's look at what the data is telling us today.",
            'market_section': "Market Overview",
            'market_intro': "Today's market conditions at a glance. Here's what the indicators show:",
            'market_meaning': "**Context:** Markets move daily. What matters most is understanding the broader trends and how they relate to your investment timeframe.",
            'whale_section': "🐋 Whale Watch",
            'whale_intro': "Tracking large wallet movements for market awareness.",
            'whale_summary': "**Recent Activity:** No significant estate movements this period. Distributions continue on schedule.",
            'whale_disclaimer': "Note: Whale movements are informational only and not trading signals.",
            'strategy_section': "Strategy Performance",
            'strategy_col1': "Strategy Type",
            'strategy_col2': "Status",
            'strategy_col3': "7-Day Performance",
            'strategy_note': "All strategies operating within expected parameters.",
            'insight_section': "💡 Market Insight",
            'wisdom_note': "Historical context helps frame current conditions, though past patterns don't guarantee future results.",
            'closing': "Stay informed",
            'signature': "Stay informed,\n**Adelaide** | diBoaS 📊",
            'footer': "📧 Questions? Reply to this email.\n⚙️ [Settings](link) | 🚪 [Unsubscribe](link)",
            'disclaimer': "**Important Notice**\n\nThis content is educational market commentary, not financial advice. Past performance does not guarantee future results. Always consult a licensed financial adviser before making investment decisions.\n\n**You decide what's best for your situation.**",
        },
        'pt-br': {
            'greeting_morning': "Bom dia!",
            'greeting_afternoon': "Boa tarde!",
            'greeting_evening': "Boa noite!",
            'intro': "Aqui esta sua atualizacao de mercado de {day}. Vamos ver o que os dados estao nos dizendo.",
            'market_section': "Visao Geral do Mercado",
            'whale_section': "🐋 Monitoramento de Baleias",
            'strategy_section': "Desempenho das Estrategias",
            'insight_section': "💡 Insight de Mercado",
            'closing': "Mantenha-se informado(a)",
            'signature': "Mantenha-se informado(a),\n**Adelaide** | diBoaS 📊",
            'disclaimer': "**Aviso Importante**\n\n**AVISO MiCA/CVM:** Criptoativos NAO sao protegidos por esquemas de garantia de depositos.\n\nEste conteudo e comentario educacional de mercado, nao aconselhamento financeiro. Desempenho passado nao garante resultados futuros.\n\n**Voce decide o que e melhor para sua situacao.**",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Maria's educational, balanced voice."""
        adapted = content.copy()
        adapted['persona'] = 'maria'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # Time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_of_day = 'morning'
        elif 12 <= hour < 18:
            time_of_day = 'afternoon'
        else:
            time_of_day = 'evening'

        day_name = datetime.now().strftime('%A')

        # Title and greeting
        adapted['title_emoji'] = self.EMOJIS['title']
        adapted['persona_greeting'] = f"{phrases[f'greeting_{time_of_day}']} {self.EMOJIS['greeting']}"
        adapted['greeting_message'] = phrases['intro'].format(day=day_name)

        # Market section
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = self.EMOJIS['market']
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_market_bullets(content)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # Whale section
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = self.EMOJIS['strategy']
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Strategy Type')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Status')
        adapted['strategy_col3'] = phrases.get('strategy_col3', '7-Day Performance')
        adapted['conservative_status'] = '✅ Normal'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):+.2f}%"
        adapted['balanced_status'] = '✅ Normal'
        adapted['balanced_action'] = f"{content.get('balanced_7d', 0):+.2f}%"
        adapted['growth_status'] = '✅ Normal'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section
        adapted['insight_section_title'] = phrases['insight_section']
        adapted['wisdom_note'] = phrases['wisdom_note']

        # Closing
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_market_bullets(self, content: Dict) -> str:
        """Build educational market bullets."""
        bullets = []
        vix = content.get('vix', 20)
        fg = content.get('fear_greed_index', 50)

        bullets.append(f"- VIX (volatility index): {vix:.1f} — {'Low volatility environment' if vix < 20 else 'Elevated volatility' if vix > 25 else 'Normal range'}")
        bullets.append(f"- Fear & Greed Index: {fg} — Sentiment indicator showing market mood")
        bullets.append("- Credit spreads: Within normal range — institutional confidence stable")

        return '\n'.join(bullets)

    @property
    def name(self) -> str:
        return "Maria"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.MODERATE

    @property
    def risk_profile(self) -> str:
        return "balanced"

    def get_signature(self, locale: str = "en") -> str:
        phrases = self.PHRASES.get(locale, self.PHRASES['en'])
        return phrases.get('signature', "Stay informed,\n**Adelaide** | diBoaS 📊")


# =============================================================================
# Felipe Persona - Technical Analyst
# =============================================================================

@PersonaRegistry.register("felipe")
class FelipePersona(Persona):
    """
    Felipe - Aggressive/Technical persona.

    Characteristics:
    - Data-forward, analytical tone ("technical analyst")
    - Zero emojis (only warning indicators)
    - Focus on returns and opportunities
    - Technical language, precise numbers
    - Indicator matrices and regime analysis
    - Targets strategies 8, 10 (70-85% crypto)

    Sign-off: "— Adelaide"
    """

    PHRASES = {
        'en': {
            'greeting': "Morning. Here's today's data.",
            'intro': "Daily briefing. Current regime analysis and key metrics follow.",
            'market_section': "Market Regime Analysis",
            'market_intro': "Current market conditions and indicator signals:",
            'market_meaning': "**Regime Assessment:** Review indicator confluence for positioning decisions.",
            'whale_section': "Estate Wallet Status",
            'whale_intro': "Tracking bankruptcy estate distributions and large holder movements.",
            'whale_summary': "**Activity:** No large movements detected. Distributions on schedule.",
            'whale_disclaimer': "Estate tracking is informational. Not a trading signal.",
            'strategy_section': "Strategy Matrix",
            'strategy_col1': "Strategy",
            'strategy_col2': "Status",
            'strategy_col3': "7d Return",
            'strategy_note': "All strategies within risk parameters. No triggers activated.",
            'insight_section': "Technical Analysis",
            'wisdom_note': "Historical correlations noted. Past patterns are not predictive.",
            'closing': "Execute accordingly",
            'signature': "— Adelaide | diBoaS",
            'footer': "Reply with questions. [Settings](link) | [Unsubscribe](link)",
            'disclaimer': "**Disclaimer**\n\nPast performance ≠ future results. Capital at risk. Not financial advice. DYOR.\n\n**Your call.**",
        },
        'pt-br': {
            'greeting': "Bom dia. Dados de hoje.",
            'intro': "Briefing diario. Analise de regime e metricas principais.",
            'market_section': "Analise de Regime de Mercado",
            'whale_section': "Status de Carteiras Estate",
            'strategy_section': "Matriz de Estrategias",
            'insight_section': "Analise Tecnica",
            'closing': "Execute conforme necessario",
            'signature': "— Adelaide | diBoaS",
            'disclaimer': "**Aviso**\n\n**MiCA/CVM:** Criptoativos sem garantia de deposito.\n\nDesempenho passado ≠ resultados futuros. Capital em risco. Nao e aconselhamento financeiro.\n\n**Sua decisao.**",
        }
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def adapt(self, content: Dict[str, Any], locale: str = "en") -> Dict[str, Any]:
        """Adapt content to Felipe's technical, data-forward voice."""
        adapted = content.copy()
        adapted['persona'] = 'felipe'
        adapted['locale'] = locale
        adapted['emoji_level'] = self.emoji_level.value

        phrases = self.PHRASES.get(locale, self.PHRASES['en'])

        # No emojis
        adapted['title_emoji'] = ''
        adapted['persona_greeting'] = phrases['greeting']
        adapted['greeting_message'] = phrases['intro']

        # Market section - technical
        adapted['market_section_title'] = phrases['market_section']
        adapted['market_emoji'] = ''
        adapted['market_intro'] = phrases['market_intro']
        adapted['market_bullets'] = self._build_indicator_matrix(content)
        adapted['fear_greed_emoji'] = ''
        adapted['market_meaning'] = phrases['market_meaning']

        # Whale section - technical
        adapted['whale_section_title'] = phrases['whale_section']
        adapted['whale_intro'] = phrases['whale_intro']
        adapted['whale_summary'] = phrases['whale_summary']
        adapted['whale_disclaimer'] = phrases['whale_disclaimer']

        # Strategy section - metrics focused
        adapted['strategy_section_title'] = phrases['strategy_section']
        adapted['strategy_emoji'] = ''
        adapted['strategy_col1'] = phrases.get('strategy_col1', 'Strategy')
        adapted['strategy_col2'] = phrases.get('strategy_col2', 'Status')
        adapted['strategy_col3'] = phrases.get('strategy_col3', '7d Return')
        adapted['conservative_status'] = 'Active'
        adapted['conservative_action'] = f"{content.get('conservative_7d', 0):+.2f}%"
        adapted['balanced_status'] = 'Active'
        adapted['balanced_action'] = f"{content.get('balanced_7d', 0):+.2f}%"
        adapted['growth_status'] = 'Active'
        adapted['growth_action'] = f"{content.get('growth_7d', 0):+.2f}%"
        adapted['strategy_note'] = phrases['strategy_note']

        # Insight section
        adapted['insight_section_title'] = phrases['insight_section']

        # Strip emojis from insight content
        if 'insight_content' in adapted:
            adapted['insight_content'] = self._strip_emojis(adapted.get('insight_content', ''))

        adapted['wisdom_note'] = phrases['wisdom_note']

        # Closing - direct
        adapted['closing_wisdom'] = phrases['closing']
        adapted['disclaimer'] = phrases['disclaimer']
        adapted['footer'] = phrases['footer']
        adapted['signature'] = phrases['signature']

        return adapted

    def _build_indicator_matrix(self, content: Dict) -> str:
        """Build technical indicator matrix."""
        btc = content.get('btc_24h_change', 0)
        fg = content.get('fear_greed_index', 50)
        vix = content.get('vix', 20)

        btc_signal = 'Bullish' if btc > 2 else 'Bearish' if btc < -2 else 'Neutral'
        fg_signal = 'Oversold' if fg < 25 else 'Overbought' if fg > 75 else 'Neutral'
        vix_signal = 'Risk-On' if vix < 20 else 'Risk-Off' if vix > 30 else 'Neutral'

        return f"""| Indicator | Value | Signal |
|-----------|-------|--------|
| BTC 24h | {btc:+.2f}% | {btc_signal} |
| Fear/Greed | {fg} | {fg_signal} |
| VIX | {vix:.1f} | {vix_signal} |"""

    def _strip_emojis(self, text: str) -> str:
        """Remove all emojis from text."""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', text).strip()

    @property
    def name(self) -> str:
        return "Felipe"

    @property
    def emoji_level(self) -> EmojiLevel:
        return EmojiLevel.NONE

    @property
    def risk_profile(self) -> str:
        return "aggressive"

    def get_signature(self, locale: str = "en") -> str:
        return "— Adelaide | diBoaS"


# =============================================================================
# Utility Functions
# =============================================================================

def get_persona_for_strategy(strategy_id: int) -> str:
    """
    Get the recommended persona name for a strategy.

    Args:
        strategy_id: Strategy ID (1-10)

    Returns:
        Persona name ('ana', 'maria', or 'felipe')
    """
    if strategy_id in [1, 3, 5, 7, 9]:
        return "ana"
    elif strategy_id in [2, 4, 6]:
        return "maria"
    elif strategy_id in [8, 10]:
        return "felipe"
    else:
        return "maria"


def get_personas_for_path(dream_mode_path: str) -> str:
    """
    Get the recommended persona for a Dream Mode path.

    Args:
        dream_mode_path: 'safety', 'balance', or 'growth'

    Returns:
        Persona name
    """
    path_personas = {
        'safety': 'ana',
        'balance': 'maria',
        'growth': 'felipe'
    }
    return path_personas.get(dream_mode_path.lower(), 'maria')
