"""
Market Regime Classifier for Adelaide.

Classifies market conditions into regimes that determine
which template and tone to use for newsletter generation.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """Market regime classifications."""
    RISK_ON_BULL = "risk_on_bull"      # Markets up, risk appetite high
    RISK_ON_BEAR = "risk_on_bear"      # Markets down but still risk-taking
    RISK_OFF_BULL = "risk_off_bull"    # Markets up but defensive
    RISK_OFF_BEAR = "risk_off_bear"    # Markets down, defensive
    TRANSITION = "transition"           # Uncertain, mixed signals
    CRISIS = "crisis"                   # Emergency situation


@dataclass
class RegimeSignals:
    """Market signals used for regime classification."""
    btc_24h_change: float       # BTC 24h price change (%)
    eth_24h_change: float       # ETH 24h price change (%)
    sp500_24h_change: float     # S&P 500 24h change (%)
    vix_level: float            # VIX index level
    fear_greed_index: int       # Fear & Greed (0-100)
    credit_spread: float        # High-yield credit spread (bps)

    # Optional crisis signals
    protocol_exploit: bool = False
    exploit_amount_usd: float = 0
    stablecoin_depeg: bool = False


class RegimeClassifier:
    """
    Classifies market regime from analytics data.

    The regime determines which template to use and the
    overall tone of the Adelaide newsletter.

    Usage:
        classifier = RegimeClassifier()
        regime = classifier.classify(analytics_data)
    """

    # Crisis thresholds
    CRISIS_BTC_DROP = -20.0         # -20% triggers crisis consideration
    CRISIS_EXPLOIT_THRESHOLD = 10_000_000  # $10M exploit

    # Regime thresholds
    BULL_THRESHOLD = 2.0            # +2% considered bullish
    BEAR_THRESHOLD = -2.0           # -2% considered bearish
    STRONG_BULL = 5.0               # +5% strong rally
    STRONG_BEAR = -5.0              # -5% significant decline

    VIX_LOW = 20                    # Low volatility
    VIX_HIGH = 25                   # High volatility
    VIX_CRISIS = 30                 # Crisis-level volatility

    FG_GREED = 60                   # Greed territory
    FG_FEAR = 40                    # Fear territory
    FG_EXTREME_FEAR = 25            # Extreme fear

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize classifier with optional config overrides."""
        self.config = config or {}

    def classify(self, analytics_data: Dict[str, Any]) -> MarketRegime:
        """
        Classify market regime from analytics data.

        Args:
            analytics_data: Dictionary containing market data
                - btc_24h_change: BTC 24h change (%)
                - eth_24h_change: ETH 24h change (%)
                - sp500_24h_change: S&P 500 24h change (%)
                - vix: VIX level
                - fear_greed_index: Fear & Greed (0-100)
                - credit_spread: HY credit spread (bps)
                - protocol_exploit: bool (optional)
                - exploit_amount_usd: float (optional)
                - stablecoin_depeg: bool (optional)

        Returns:
            MarketRegime enum value
        """
        # Extract signals
        signals = self._extract_signals(analytics_data)

        # Check for crisis conditions first
        if self._is_crisis(signals):
            return MarketRegime.CRISIS

        # Classify based on market signals
        return self._classify_regime(signals)

    def _extract_signals(self, data: Dict[str, Any]) -> RegimeSignals:
        """Extract regime signals from analytics data."""
        return RegimeSignals(
            btc_24h_change=data.get('btc_24h_change', 0.0),
            eth_24h_change=data.get('eth_24h_change', 0.0),
            sp500_24h_change=data.get('sp500_24h_change', 0.0),
            vix_level=data.get('vix', 20.0),
            fear_greed_index=data.get('fear_greed_index', 50),
            credit_spread=data.get('credit_spread', 350),
            protocol_exploit=data.get('protocol_exploit', False),
            exploit_amount_usd=data.get('exploit_amount_usd', 0),
            stablecoin_depeg=data.get('stablecoin_depeg', False),
        )

    def _is_crisis(self, signals: RegimeSignals) -> bool:
        """Check if crisis conditions are met."""
        # Major market crash
        if signals.btc_24h_change <= self.CRISIS_BTC_DROP:
            logger.warning(f"Crisis: BTC down {signals.btc_24h_change}%")
            return True

        # Significant protocol exploit
        if signals.protocol_exploit and signals.exploit_amount_usd >= self.CRISIS_EXPLOIT_THRESHOLD:
            logger.warning(f"Crisis: Protocol exploit ${signals.exploit_amount_usd:,.0f}")
            return True

        # Stablecoin depeg
        if signals.stablecoin_depeg:
            logger.warning("Crisis: Stablecoin depeg detected")
            return True

        # Extreme market stress
        if signals.vix_level >= self.VIX_CRISIS and signals.fear_greed_index <= self.FG_EXTREME_FEAR:
            logger.warning(f"Crisis: VIX {signals.vix_level}, F&G {signals.fear_greed_index}")
            return True

        return False

    def _classify_regime(self, signals: RegimeSignals) -> MarketRegime:
        """Classify non-crisis market regime."""
        btc_change = signals.btc_24h_change
        vix = signals.vix_level
        fg = signals.fear_greed_index

        # Calculate risk appetite score
        risk_on = self._is_risk_on(signals)

        # Determine bull/bear
        if btc_change >= self.STRONG_BULL:
            # Strong rally
            return MarketRegime.RISK_ON_BULL if risk_on else MarketRegime.RISK_OFF_BULL

        elif btc_change >= self.BULL_THRESHOLD:
            # Moderate up
            if risk_on and fg >= self.FG_GREED:
                return MarketRegime.RISK_ON_BULL
            elif not risk_on or vix >= self.VIX_HIGH:
                return MarketRegime.RISK_OFF_BULL
            else:
                return MarketRegime.TRANSITION

        elif btc_change <= self.STRONG_BEAR:
            # Significant decline
            return MarketRegime.RISK_OFF_BEAR

        elif btc_change <= self.BEAR_THRESHOLD:
            # Moderate down
            if not risk_on or fg <= self.FG_FEAR:
                return MarketRegime.RISK_OFF_BEAR
            else:
                return MarketRegime.RISK_ON_BEAR

        else:
            # Flat market (-2% to +2%)
            return MarketRegime.TRANSITION

    def _is_risk_on(self, signals: RegimeSignals) -> bool:
        """Determine if market sentiment is risk-on."""
        score = 0

        # Fear & Greed
        if signals.fear_greed_index >= self.FG_GREED:
            score += 2
        elif signals.fear_greed_index >= 50:
            score += 1
        elif signals.fear_greed_index <= self.FG_FEAR:
            score -= 2
        else:
            score -= 1

        # VIX
        if signals.vix_level <= self.VIX_LOW:
            score += 1
        elif signals.vix_level >= self.VIX_HIGH:
            score -= 1

        # Credit spreads (wider = risk-off)
        if signals.credit_spread <= 300:
            score += 1
        elif signals.credit_spread >= 400:
            score -= 1

        return score > 0

    def get_template_name(self, regime: MarketRegime) -> str:
        """Get template name for a regime."""
        template_map = {
            MarketRegime.RISK_ON_BULL: "daily_up",
            MarketRegime.RISK_ON_BEAR: "daily_calm",
            MarketRegime.RISK_OFF_BULL: "daily_calm",
            MarketRegime.RISK_OFF_BEAR: "daily_down",
            MarketRegime.TRANSITION: "daily_calm",
            MarketRegime.CRISIS: "crisis",
        }
        return template_map.get(regime, "daily_calm")

    def get_regime_description(self, regime: MarketRegime) -> str:
        """Get human-readable regime description."""
        descriptions = {
            MarketRegime.RISK_ON_BULL: "Markets are up with strong risk appetite",
            MarketRegime.RISK_ON_BEAR: "Markets are down but sentiment remains resilient",
            MarketRegime.RISK_OFF_BULL: "Markets are up but investors are cautious",
            MarketRegime.RISK_OFF_BEAR: "Markets are down with defensive positioning",
            MarketRegime.TRANSITION: "Markets are mixed with uncertain direction",
            MarketRegime.CRISIS: "Emergency market conditions detected",
        }
        return descriptions.get(regime, "Unknown market conditions")
