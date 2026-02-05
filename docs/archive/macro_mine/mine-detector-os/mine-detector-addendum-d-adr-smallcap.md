# Mine Detector OS -- Addendum D: ADR/Small-Cap/Web3 Overlay

> Score adjustment overlay for securities with structural risks not captured in core US equity metrics: ADRs, small-caps, and tokenized/Web3 assets.

**Version:** 2026-01-30-r9

**Cross-References:**
- Core OS: mine-detector-os.md (interface contract, 9 canonical categories, RiskCategory enum)
- Addendum C: mine-detector-addendum-c-brokerage.md (crypto exchange connectors)
- Addendum E: mine-detector-addendum-e-maintenance-operations.md (token unlock tracking)

---

## Overview

This addendum addresses structural risks in non-standard securities:

1. **ADRs:** Geopolitical, VIE (Variable Interest Entity) structure, delisting risks
2. **Small-Caps:** Liquidity, coverage, manipulation risks
3. **Tokenized/Web3:** Smart contract, bridge, oracle risks

**Acronym Reference (r8):**
- **VIE** = Variable Interest Entity (corporate structure where foreign investors hold contractual rights rather than direct equity ownership; common in China ADRs)
- **HFCAA** = Holding Foreign Companies Accountable Act (US law requiring foreign companies to allow PCAOB audit inspection or face delisting)

---

## Overlay Units: Notches vs Points

**CRITICAL: Understanding the unit conversion is essential.**

The structural overlay is measured in **notches** (0.0 to 2.5), which are then converted to **points** (0 to 25) when added to the composite score:

```
overlay_points = overlay_notches * 10
```

| Security Type | Overlay Notches | Overlay Points | Meaning |
|---------------|-----------------|----------------|---------|
| US Large-Cap | 0.0 | 0 | Baseline - no structural penalty |
| US Mid-Cap | 0.0 | 0 | Baseline |
| US Small-Cap | 0.3-0.8 | 3-8 | Liquidity/coverage concerns |
| ADR Developed | 0.2-0.5 | 2-5 | Light geopolitical risk |
| ADR Emerging | 0.5-1.0 | 5-10 | Moderate geopolitical risk |
| ADR China | 0.8-2.0 | 8-20 | High structural risk (stacking) |
| Tokenized/Web3 | 0.5-2.5 | 5-25 | Variable smart contract risk |

---

## Interface Contract

Implements the Core OS ADR/Small-Cap interface:

```python
def compute_structural_overlay(security_type: str,
                                geopolitical: Dict,
                                liquidity: Dict,
                                data_gaps: List[str]) -> Dict:
    """
    Compute structural risk overlay for ADR/small-cap/Web3.
    
    Returns:
        {
            'overlay_notches': float,    # 0.0 to 2.5 (raw overlay)
            'overlay_points': float,     # 0 to 25 (notches * 10)
            'confidence': str,           # HIGH, MEDIUM, LOW, VERY_LOW
            'reasons': List[str],        # Human-readable explanations
            'security_type': str         # Classification result
        }
    """
```

---

## Imports and Dependencies

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime, timezone

# Import from shared module (Core OS)
from mine_detector_shared import utc_now, to_utc, format_timestamp, RiskCategory
```

---

## Security Classification

```python
class SecurityType(Enum):
    """Security type classification."""
    US_LARGE_CAP = "us_large_cap"
    US_MID_CAP = "us_mid_cap"
    US_SMALL_CAP = "us_small_cap"
    US_MICRO_CAP = "us_micro_cap"
    ADR_DEVELOPED = "adr_developed"
    ADR_EMERGING = "adr_emerging"
    ADR_CHINA = "adr_china"
    ADR_RUSSIA = "adr_russia"
    TOKENIZED_EQUITY = "tokenized_equity"
    TOKENIZED_RWA = "tokenized_rwa"       # Real World Assets
    NATIVE_CRYPTO = "native_crypto"
    DEFI_TOKEN = "defi_token"
    UNKNOWN = "unknown"


# Base overlay notches by security type
BASE_OVERLAY_NOTCHES: Dict[SecurityType, float] = {
    SecurityType.US_LARGE_CAP: 0.0,
    SecurityType.US_MID_CAP: 0.0,
    SecurityType.US_SMALL_CAP: 0.3,
    SecurityType.US_MICRO_CAP: 0.6,
    SecurityType.ADR_DEVELOPED: 0.2,
    SecurityType.ADR_EMERGING: 0.5,
    SecurityType.ADR_CHINA: 0.8,      # Base only - additional stacking applies
    SecurityType.ADR_RUSSIA: 2.5,     # Sanctioned - maximum
    SecurityType.TOKENIZED_EQUITY: 0.6,
    SecurityType.TOKENIZED_RWA: 0.8,
    SecurityType.NATIVE_CRYPTO: 0.5,
    SecurityType.DEFI_TOKEN: 0.7,
    SecurityType.UNKNOWN: 1.0
}


def classify_security(ticker: str,
                      market_cap_usd: Optional[float],
                      country: Optional[str],
                      is_adr: bool,
                      chain: Optional[str] = None) -> SecurityType:
    """
    Classify a security into the appropriate type.
    """
    # Tokenized/crypto
    if chain is not None:
        if chain.lower() in ['ethereum', 'polygon', 'base', 'arbitrum', 'optimism']:
            # Check if it's a tokenized equity or RWA
            # In production: check token metadata
            return SecurityType.TOKENIZED_EQUITY
        return SecurityType.NATIVE_CRYPTO
    
    # ADRs
    if is_adr and country:
        country_upper = country.upper()
        
        # China (including HK)
        if country_upper in ['CN', 'CHN', 'CHINA', 'HK', 'HKG']:
            return SecurityType.ADR_CHINA
        
        # Russia (sanctioned)
        if country_upper in ['RU', 'RUS', 'RUSSIA']:
            return SecurityType.ADR_RUSSIA
        
        # Developed markets
        developed = ['GB', 'GBR', 'DE', 'DEU', 'FR', 'FRA', 'JP', 'JPN', 
                    'AU', 'AUS', 'CA', 'CAN', 'CH', 'CHE', 'NL', 'NLD', 
                    'SE', 'SWE', 'IE', 'IRL', 'BE', 'BEL']
        if country_upper in developed:
            return SecurityType.ADR_DEVELOPED
        
        # Everything else is emerging
        return SecurityType.ADR_EMERGING
    
    # US equities by market cap
    if market_cap_usd is not None:
        if market_cap_usd >= 10_000_000_000:  # $10B+
            return SecurityType.US_LARGE_CAP
        if market_cap_usd >= 2_000_000_000:   # $2B-$10B
            return SecurityType.US_MID_CAP
        if market_cap_usd >= 300_000_000:     # $300M-$2B
            return SecurityType.US_SMALL_CAP
        return SecurityType.US_MICRO_CAP      # <$300M
    
    return SecurityType.UNKNOWN
```

---

## Web3 Metric Translation Layer

The Core OS uses 9 TradFi risk categories. This layer maps Web3-native metrics to those categories:

```python
"""
WEB3 METRIC TRANSLATION TABLE

The Core OS risk categories assume TradFi data (options chains, SEC filings).
Tokenized assets have none of these. This table maps Web3 equivalents:

+----------------------+---------------------------+---------------------------+
| Core OS Category     | TradFi Metric             | Web3 Equivalent           |
+----------------------+---------------------------+---------------------------+
| catalyst_risk        | Earnings dates            | Token unlock schedules    |
| solvency_risk        | Altman-Z, debt ratios     | Protocol TVL, treasury    |
| crowding_risk        | Short interest            | Perp funding rates, OI    |
| liquidity_flow_risk  | ETF flows, 13F            | CEX flows, whale wallets  |
| momentum_risk        | RSI, moving averages      | Same (price-based)        |
| governance_risk      | Insider selling, auditor  | Multisig changes, DAO     |
| refinancing_risk     | Debt maturity             | Protocol runway           |
| dilution_risk        | Shelf registrations       | Token emission schedule   |
| event_risk           | M&A, litigation           | Hack risk, regulatory     |
+----------------------+---------------------------+---------------------------+
"""


@dataclass
class Web3Metrics:
    """Web3-native metrics for translation to Core OS categories."""
    
    # Token unlocks (-> catalyst_risk)
    next_unlock_date: Optional[datetime] = None
    next_unlock_pct: Optional[float] = None
    circulating_supply_pct: Optional[float] = None
    
    # Protocol health (-> solvency_risk)
    tvl_usd: Optional[float] = None
    tvl_change_30d_pct: Optional[float] = None
    treasury_usd: Optional[float] = None
    treasury_runway_months: Optional[float] = None
    
    # Derivatives positioning (-> crowding_risk)
    # UNIT: perp_funding_rate_8h is in DECIMAL form (e.g., 0.0001 = 0.01% per 8h)
    # NOT percentage form. If your feed gives 0.01 meaning 1%, divide by 100 first.
    perp_funding_rate_8h: Optional[float] = None
    perp_open_interest_usd: Optional[float] = None
    long_short_ratio: Optional[float] = None
    
    # Flow data (-> liquidity_flow_risk)
    cex_netflow_24h: Optional[float] = None
    whale_transactions_24h: Optional[int] = None
    
    # Governance (-> governance_risk)
    multisig_signers: Optional[int] = None
    multisig_threshold: Optional[int] = None
    top_holder_pct: Optional[float] = None
    
    # Security (-> event_risk)
    audit_count: Optional[int] = None
    days_since_last_audit: Optional[int] = None
    has_bug_bounty: bool = False
    previous_exploits: int = 0


class Web3MetricCalculator:
    """
    Calculate Core OS category scores from Web3 metrics.
    Each method returns a score from 0-100 or None if not calculable.
    """
    
    def catalyst_risk(self, m: Web3Metrics) -> Optional[float]:
        """Token unlock schedule -> Catalyst Risk."""
        if m.next_unlock_date is None or m.next_unlock_pct is None:
            return None
        
        days_to_unlock = (m.next_unlock_date - utc_now()).days
        
        # Large unlock approaching = high risk
        if days_to_unlock <= 7 and m.next_unlock_pct > 5:
            return 90
        if days_to_unlock <= 14 and m.next_unlock_pct > 3:
            return 70
        if days_to_unlock <= 30 and m.next_unlock_pct > 2:
            return 50
        if days_to_unlock <= 30:
            return 30
        return 15
    
    def solvency_risk(self, m: Web3Metrics) -> Optional[float]:
        """Protocol TVL and treasury -> Solvency Risk."""
        scores = []
        
        # TVL decline
        if m.tvl_change_30d_pct is not None:
            if m.tvl_change_30d_pct < -50:
                scores.append(90)
            elif m.tvl_change_30d_pct < -30:
                scores.append(70)
            elif m.tvl_change_30d_pct < -10:
                scores.append(40)
            else:
                scores.append(10)
        
        # Treasury runway
        if m.treasury_runway_months is not None:
            if m.treasury_runway_months < 6:
                scores.append(85)
            elif m.treasury_runway_months < 12:
                scores.append(50)
            elif m.treasury_runway_months < 24:
                scores.append(25)
            else:
                scores.append(10)
        
        return sum(scores) / len(scores) if scores else None
    
    def crowding_risk(self, m: Web3Metrics) -> Optional[float]:
        """
        Perp funding rates -> Crowding Risk.
        
        UNIT REQUIREMENT: perp_funding_rate_8h must be in DECIMAL form.
        Example: 0.0001 = 0.01% per 8-hour period
        
        Annualization: rate_8h * 3 (periods/day) * 365 (days) * 100 (to %)
        Example: 0.0001 * 3 * 365 * 100 = 10.95% annualized
        """
        if m.perp_funding_rate_8h is None:
            return None
        
        # Annualize funding rate (8h rate * 3 periods/day * 365 days * 100 to %)
        # ASSUMES: perp_funding_rate_8h is in decimal (0.0001 = 0.01%)
        funding_annual = abs(m.perp_funding_rate_8h) * 3 * 365 * 100
        
        if funding_annual > 100:  # >100% annualized
            return 90
        if funding_annual > 50:
            return 70
        if funding_annual > 20:
            return 45
        if funding_annual > 10:
            return 25
        return 10
    
    def governance_risk(self, m: Web3Metrics) -> Optional[float]:
        """Multisig and holder concentration -> Governance Risk."""
        score = 15  # Base
        
        # Multisig configuration
        if m.multisig_signers is not None:
            if m.multisig_signers <= 2:
                score += 40  # Very centralized
            elif m.multisig_signers <= 3:
                score += 25
            elif m.multisig_signers <= 5:
                score += 10
        
        # Holder concentration
        if m.top_holder_pct is not None:
            if m.top_holder_pct > 50:
                score += 30
            elif m.top_holder_pct > 30:
                score += 15
        
        # Audit status
        if m.audit_count is not None and m.audit_count == 0:
            score += 20
        
        return min(100, score)
    
    def dilution_risk(self, m: Web3Metrics) -> Optional[float]:
        """Token emission schedule -> Dilution Risk."""
        if m.circulating_supply_pct is None:
            return None
        
        unvested = 100 - m.circulating_supply_pct
        
        if unvested > 70:
            return 85
        if unvested > 50:
            return 65
        if unvested > 30:
            return 40
        if unvested > 15:
            return 25
        return 10
    
    def event_risk(self, m: Web3Metrics) -> Optional[float]:
        """Hack/exploit history -> Event Risk."""
        score = 10  # Base
        
        # Previous exploits
        if m.previous_exploits > 0:
            score += min(40, m.previous_exploits * 15)
        
        # No audit
        if m.audit_count is not None and m.audit_count == 0:
            score += 25
        
        # No bug bounty
        if not m.has_bug_bounty:
            score += 10
        
        # Stale audit
        if m.days_since_last_audit is not None and m.days_since_last_audit > 365:
            score += 15
        
        return min(100, score)


def translate_web3_to_core_categories(metrics: Web3Metrics) -> Dict[RiskCategory, Optional[float]]:
    """
    Convenience function to translate Web3 metrics to all Core OS categories.
    """
    calc = Web3MetricCalculator()
    
    return {
        RiskCategory.CATALYST_RISK: calc.catalyst_risk(metrics),
        RiskCategory.SOLVENCY_RISK: calc.solvency_risk(metrics),
        RiskCategory.CROWDING_RISK: calc.crowding_risk(metrics),
        RiskCategory.LIQUIDITY_FLOW_RISK: None,  # Requires flow data integration
        RiskCategory.MOMENTUM_RISK: None,        # Use standard price-based
        RiskCategory.GOVERNANCE_RISK: calc.governance_risk(metrics),
        RiskCategory.REFINANCING_RISK: None,     # Use solvency as proxy
        RiskCategory.DILUTION_RISK: calc.dilution_risk(metrics),
        RiskCategory.EVENT_RISK: calc.event_risk(metrics)
    }
```

---

## China ADR Assessment

China ADRs receive **stacked** adjustments due to compound structural risks:

```python
"""
CHINA ADR STACKING

Total overlay = Base (0.8 notches) + Additional (0.0-1.2 notches)

Minimum: 0.8 notches (8 points) - base only
Maximum: 2.0 notches (20 points) - base + all flags

The stacking is INTENTIONAL given compound structural risks:
1. VIE structure = no actual ownership of Chinese operating assets
2. HFCAA = potential forced delisting from US exchanges
3. Geopolitical = unpredictable regulatory/political actions
4. Data access = limited financial transparency for investors
"""


@dataclass
class ChinaADRRisk:
    """China ADR specific risk factors."""
    has_vie_structure: bool = True
    hfcaa_status: str = "at_risk"  # compliant, at_risk, non_compliant
    sector: str = "unknown"
    geopolitical_tension: str = "moderate"  # low, moderate, high, critical


class ChinaADRAssessor:
    """
    Assess China-specific ADR risks.
    
    NOTE: Adjustments from this assessor STACK with base ADR_CHINA of 0.8 notches.
    """
    
    SENSITIVE_SECTORS = ['technology', 'semiconductors', 'ai', 'defense', 
                         'telecommunications', 'education', 'gaming']
    
    TENSION_ADJUSTMENTS = {
        'low': 0.0,
        'moderate': 0.1,
        'high': 0.15,
        'critical': 0.2
    }
    
    def assess(self, risk: ChinaADRRisk, ticker: str = "") -> Dict:
        """
        Assess China ADR additional risks.
        
        Returns:
            {
                'additional_notches': float,  # 0.0 to 1.2
                'reasons': List[str],
                'total_notches': float        # Base (0.8) + additional
            }
        """
        additional = 0.0
        reasons = []
        
        # VIE structure (+0.0 to +0.3 notches)
        if risk.has_vie_structure:
            additional += 0.3
            reasons.append('VIE structure: +0.3 notches (no direct ownership)')
        
        # HFCAA status (+0.0 to +0.5 notches)
        if risk.hfcaa_status == 'non_compliant':
            additional += 0.5
            reasons.append('HFCAA non-compliant: +0.5 notches (delisting risk)')
        elif risk.hfcaa_status == 'at_risk':
            additional += 0.25
            reasons.append('HFCAA at-risk: +0.25 notches')
        
        # Sensitive sectors (+0.0 to +0.2 notches)
        if risk.sector.lower() in self.SENSITIVE_SECTORS:
            additional += 0.2
            reasons.append(f'Sensitive sector ({risk.sector}): +0.2 notches')
        
        # Geopolitical tension (+0.0 to +0.2 notches)
        geo_adj = self.TENSION_ADJUSTMENTS.get(risk.geopolitical_tension, 0.1)
        if geo_adj > 0:
            additional += geo_adj
            reasons.append(f'Geopolitical ({risk.geopolitical_tension}): +{geo_adj} notches')
        
        # Cap additional at 1.2 notches
        additional = min(1.2, additional)
        
        base = BASE_OVERLAY_NOTCHES[SecurityType.ADR_CHINA]
        total = base + additional
        
        return {
            'base_notches': base,
            'additional_notches': round(additional, 2),
            'total_notches': round(total, 2),
            'total_points': round(total * 10, 1),
            'reasons': reasons
        }
```

---

## Liquidity Assessor

```python
class LiquidityAssessor:
    """Assess liquidity risk for small-cap securities."""
    
    def assess(self,
               avg_daily_volume_usd: Optional[float],
               bid_ask_spread_pct: Optional[float],
               float_pct: Optional[float] = None) -> Dict:
        """
        Assess liquidity risk.
        
        Returns:
            {'additional_notches': float (0.0-0.5), 'reasons': List[str]}
        """
        additional = 0.0
        reasons = []
        
        # Volume assessment
        if avg_daily_volume_usd is not None:
            if avg_daily_volume_usd < 100_000:
                additional += 0.4
                reasons.append(f'Very low volume (${avg_daily_volume_usd/1000:.0f}K): +0.4 notches')
            elif avg_daily_volume_usd < 500_000:
                additional += 0.2
                reasons.append(f'Low volume (${avg_daily_volume_usd/1000:.0f}K): +0.2 notches')
            elif avg_daily_volume_usd < 1_000_000:
                additional += 0.1
                reasons.append(f'Below-average volume: +0.1 notches')
        
        # Spread assessment
        if bid_ask_spread_pct is not None:
            if bid_ask_spread_pct > 2.0:
                additional += 0.25
                reasons.append(f'Wide spread ({bid_ask_spread_pct:.1f}%): +0.25 notches')
            elif bid_ask_spread_pct > 1.0:
                additional += 0.1
                reasons.append(f'Elevated spread ({bid_ask_spread_pct:.1f}%): +0.1 notches')
        
        # Float assessment
        if float_pct is not None and float_pct < 30:
            additional += 0.15
            reasons.append(f'Low float ({float_pct:.0f}%): +0.15 notches')
        
        return {
            'additional_notches': min(0.5, round(additional, 2)),
            'reasons': reasons
        }
```

---

## Web3 Risk Assessor

```python
class Web3RiskAssessor:
    """Assess Web3-specific structural risks."""
    
    HIGH_RISK_FLAGS = [
        'unaudited',
        'single_admin',
        'upgradeable_no_timelock',
        'high_bridge_exposure',
        'centralized_oracle',
        'new_contract',
        'no_bug_bounty'
    ]
    
    CHAIN_RISK_NOTCHES = {
        'ethereum': 0.0,
        'arbitrum': 0.05,
        'optimism': 0.05,
        'base': 0.08,
        'polygon': 0.1,
        'avalanche': 0.12,
        'solana': 0.15,
        'bsc': 0.2,
    }
    
    def assess(self,
               audit_status: str,
               chain: str,
               tvl_usd: Optional[float],
               risk_flags: List[str],
               contract_age_days: int = 365) -> Dict:
        """
        Assess Web3-specific risks.
        
        Returns:
            {'additional_notches': float (0.0-1.5), 'reasons': List[str]}
        """
        additional = 0.0
        reasons = []
        
        # Audit status
        if audit_status == 'unaudited':
            additional += 0.5
            reasons.append('Unaudited: +0.5 notches')
        elif audit_status == 'partial':
            additional += 0.2
            reasons.append('Partial audit: +0.2 notches')
        elif audit_status == 'stale':  # >1 year old
            additional += 0.15
            reasons.append('Stale audit: +0.15 notches')
        
        # Chain risk
        chain_adj = self.CHAIN_RISK_NOTCHES.get(chain.lower(), 0.15)
        if chain_adj > 0:
            additional += chain_adj
            reasons.append(f'Chain ({chain}): +{chain_adj} notches')
        
        # Contract age
        if contract_age_days < 30:
            additional += 0.3
            reasons.append(f'New contract ({contract_age_days}d): +0.3 notches')
        elif contract_age_days < 90:
            additional += 0.15
            reasons.append(f'Young contract ({contract_age_days}d): +0.15 notches')
        
        # Risk flags
        flag_count = sum(1 for f in risk_flags if f in self.HIGH_RISK_FLAGS)
        if flag_count > 0:
            flag_adj = min(0.4, flag_count * 0.1)
            additional += flag_adj
            reasons.append(f'Risk flags ({flag_count}): +{flag_adj} notches')
        
        # Low TVL
        if tvl_usd is not None:
            if tvl_usd < 1_000_000:
                additional += 0.3
                reasons.append(f'Very low TVL (${tvl_usd/1e6:.2f}M): +0.3 notches')
            elif tvl_usd < 10_000_000:
                additional += 0.15
                reasons.append(f'Low TVL (${tvl_usd/1e6:.1f}M): +0.15 notches')
        
        return {
            'additional_notches': min(1.5, round(additional, 2)),
            'reasons': reasons
        }
```

---

## Main Interface Implementation

```python
def compute_structural_overlay(security_type: str,
                                geopolitical: Dict,
                                liquidity: Dict,
                                data_gaps: List[str]) -> Dict:
    """
    Compute structural risk overlay for ADR/small-cap/Web3.
    
    Implements the Core OS interface contract.
    """
    # Parse security type
    try:
        sec_type = SecurityType(security_type)
    except ValueError:
        sec_type = SecurityType.UNKNOWN
    
    # Start with base notches
    notches = BASE_OVERLAY_NOTCHES.get(sec_type, 0.5)
    reasons = [f'Base ({sec_type.value}): +{notches} notches']
    confidence = 'HIGH'
    
    # China ADR additional (stacking)
    if sec_type == SecurityType.ADR_CHINA:
        china_risk = ChinaADRRisk(
            has_vie_structure=geopolitical.get('has_vie', True),
            hfcaa_status=geopolitical.get('hfcaa_status', 'at_risk'),
            sector=geopolitical.get('sector', 'unknown'),
            geopolitical_tension=geopolitical.get('tension_level', 'moderate')
        )
        china_assessor = ChinaADRAssessor()
        china_result = china_assessor.assess(china_risk, geopolitical.get('ticker', ''))
        
        notches = china_result['total_notches']  # Already includes base
        reasons = [f"Base (ADR_CHINA): +{china_result['base_notches']} notches"]
        reasons.extend(china_result['reasons'])
    
    # Small-cap liquidity (additional to base)
    if sec_type in [SecurityType.US_SMALL_CAP, SecurityType.US_MICRO_CAP]:
        liq_assessor = LiquidityAssessor()
        liq_result = liq_assessor.assess(
            avg_daily_volume_usd=liquidity.get('avg_daily_volume_usd'),
            bid_ask_spread_pct=liquidity.get('bid_ask_spread_pct'),
            float_pct=liquidity.get('float_pct')
        )
        if liq_result['additional_notches'] > 0:
            notches += liq_result['additional_notches']
            reasons.extend(liq_result['reasons'])
    
    # Web3 assessment
    if sec_type in [SecurityType.NATIVE_CRYPTO, SecurityType.DEFI_TOKEN, 
                    SecurityType.TOKENIZED_EQUITY, SecurityType.TOKENIZED_RWA]:
        web3_assessor = Web3RiskAssessor()
        web3_result = web3_assessor.assess(
            audit_status=geopolitical.get('audit_status', 'unknown'),
            chain=geopolitical.get('chain', 'unknown'),
            tvl_usd=geopolitical.get('tvl_usd'),
            risk_flags=geopolitical.get('risk_flags', []),
            contract_age_days=geopolitical.get('contract_age_days', 365)
        )
        if web3_result['additional_notches'] > 0:
            notches += web3_result['additional_notches']
            reasons.extend(web3_result['reasons'])
    
    # Data gap penalty
    if len(data_gaps) > 2:
        gap_penalty = min(0.3, len(data_gaps) * 0.05)
        notches += gap_penalty
        reasons.append(f'Data gaps ({len(data_gaps)}): +{gap_penalty:.2f} notches')
        
        if len(data_gaps) > 4:
            confidence = 'LOW'
        else:
            confidence = 'MEDIUM'
    
    # Cap at 2.5 notches
    notches = min(2.5, max(0.0, notches))
    points = notches * 10
    
    return {
        'overlay_notches': round(notches, 2),
        'overlay_points': round(points, 1),
        'confidence': confidence,
        'reasons': reasons,
        'security_type': sec_type.value
    }
```

---

## Position Sizing Based on Overlay

| Overlay Notches | Overlay Points | Position Limit | Risk Level |
|-----------------|----------------|----------------|------------|
| 0.0-0.5 | 0-5 | 100% normal | Standard |
| 0.5-1.0 | 5-10 | 75% normal | Elevated structural |
| 1.0-1.5 | 10-15 | 50% normal | High structural |
| 1.5-2.0 | 15-20 | 25% normal | Very high |
| 2.0-2.5 | 20-25 | 10% or avoid | Extreme |

```python
def get_position_size_limit(overlay_notches: float) -> Dict:
    """
    Get recommended position size limit based on overlay.
    """
    if overlay_notches <= 0.5:
        return {'limit_pct': 100, 'risk_level': 'standard', 'recommendation': 'Normal sizing allowed'}
    elif overlay_notches <= 1.0:
        return {'limit_pct': 75, 'risk_level': 'elevated', 'recommendation': 'Reduce maximum position by 25%'}
    elif overlay_notches <= 1.5:
        return {'limit_pct': 50, 'risk_level': 'high', 'recommendation': 'Reduce maximum position by 50%'}
    elif overlay_notches <= 2.0:
        return {'limit_pct': 25, 'risk_level': 'very_high', 'recommendation': 'Reduce maximum position by 75%'}
    else:
        return {'limit_pct': 10, 'risk_level': 'extreme', 'recommendation': 'Avoid or minimal position only'}
```

---

## Dashboard Output

```
================================================================================
                    STRUCTURAL OVERLAY ASSESSMENT
                    Ticker: BABA | 2026-01-30 10:00 UTC
================================================================================

SECURITY CLASSIFICATION
--------------------------------------------------------------------------------
Type:                ADR_CHINA
Country:             China (CN)
Market Cap:          $185B
VIE Structure:       YES
HFCAA Status:        AT_RISK

OVERLAY CALCULATION
--------------------------------------------------------------------------------
Component                          Notches    Points
-------------------------------    -------    ------
Base (ADR_CHINA)                   +0.80      +8.0
VIE structure                      +0.30      +3.0
HFCAA at-risk                      +0.25      +2.5
Sensitive sector (Technology)     +0.20      +2.0
Geopolitical (Moderate)            +0.10      +1.0
                                   -------    ------
TOTAL OVERLAY                      +1.65      +16.5

CONFIDENCE: HIGH

POSITION SIZING RECOMMENDATION
--------------------------------------------------------------------------------
Overlay: 1.65 notches -> Position limit: 25% of normal
Risk Level: Very High Structural Risk
Recommendation: Reduce maximum position by 75%

EXPLANATION
--------------------------------------------------------------------------------
This China ADR carries significant structural risks:
- VIE structure means no direct ownership of operating assets
- HFCAA compliance remains uncertain, delisting risk exists
- Technology sector faces heightened regulatory scrutiny
- Current geopolitical tensions add uncertainty

================================================================================
```

---

---

## Future Enhancements to be Evaluated

The following topics have been identified for potential future development:

- **Web3 security model gaps:** Expand Web3RiskAssessor to include additional smart contract risk factors:
  - Reentrancy guard detection (check for nonReentrant modifiers)
  - Flash loan attack surface assessment
  - Governance participation rate tracking (voter apathy risk)
  - Oracle manipulation resistance scoring
  - Token registry integration for more accurate security classification (avoid guessing from chain alone)

- **Proxy contract risk detection (r8):** Add specialized assessment for upgradeable contracts:
  - Proxy pattern identification (Transparent, UUPS, Beacon, Diamond)
  - Implementation contract history (how many upgrades, how recently)
  - Admin/owner timelock verification (minimum 24-48h timelock recommended)
  - Multisig requirements for upgrade execution
  - Implementation slot storage analysis for tampering risks
  - Severity: MEDIUM for timelocked proxies, HIGH for instant-upgrade proxies

---

*Addendum D - Mine Detector OS v2026-01-30-r9*
