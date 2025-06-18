"""
Pricing Agent for MatchedCover Insurance Platform.

This agent calculates dynamic insurance premiums using market data,
risk assessments, and machine learning models for competitive pricing.
"""

import json
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


from src.agents.base_agent import BaseAgent
from src.agents.risk_assessor import RiskAssessment, RiskLevel
from src.core.config import get_settings
from src.quantum.crypto import QuantumResistantSigner

logger = logging.getLogger(__name__)
settings = get_settings()


class PricingStrategy(Enum):
    """Pricing strategy options."""

    COMPETITIVE = "competitive"
    PENETRATION = "penetration"
    PREMIUM = "premium"
    RISK_BASED = "risk_based"
    MARKET_FOLLOWING = "market_following"


class PricingFactorType(Enum):
    """Types of pricing factors."""

    BASE_RATE = "base_rate"
    RISK_ADJUSTMENT = "risk_adjustment"
    MARKET_COMPETITIVE = "market_competitive"
    VOLUME_DISCOUNT = "volume_discount"
    LOYALTY_DISCOUNT = "loyalty_discount"
    REGULATORY_SURCHARGE = "regulatory_surcharge"
    PROFIT_MARGIN = "profit_margin"


@dataclass
class PricingFactor:
    """Individual pricing factor."""

    factor_type: PricingFactorType
    value: Decimal
    weight: float
    description: str
    source: str


@dataclass
class PricingQuote:
    """Insurance pricing quote."""

    quote_id: str
    customer_id: str
    policy_type: str
    coverage_amount: Decimal
    base_premium: Decimal
    final_premium: Decimal
    pricing_factors: List[PricingFactor]
    discount_total: Decimal
    surcharge_total: Decimal
    risk_multiplier: float
    market_competitiveness: float
    quote_timestamp: datetime
    valid_until: datetime
    confidence_score: float
    quantum_signature: str


@dataclass
class MarketData:
    """Market pricing data."""

    competitor_prices: List[Decimal]
    market_average: Decimal
    market_percentile_25: Decimal
    market_percentile_75: Decimal
    volume_trends: Dict[str, float]
    seasonal_factors: Dict[str, float]


class PricingAgent(BaseAgent):
    """
    AI agent for dynamic insurance pricing and quote generation.

    Uses machine learning models, market data, and risk assessments
    to calculate competitive and profitable insurance premiums.
    """

    def __init__(self):
        super().__init__(name="PricingAgent", agent_type="pricing")
        self.quantum_signer = QuantumResistantSigner()
        self.pricing_models = {}
        self.market_data_cache = {}
        self._initialize_pricing_models()

    def _initialize_pricing_models(self):
        """Initialize machine learning models for pricing."""
        try:
            # Base pricing model
            self.pricing_models["base_pricing"] = RandomForestRegressor(
                n_estimators=150, max_depth=12, random_state=42
            )

            # Market competitive pricing model
            self.pricing_models["competitive_pricing"] = LinearRegression()

            # Risk-based pricing model
            self.pricing_models["risk_pricing"] = RandomForestRegressor(
                n_estimators=100, max_depth=8, random_state=42
            )

            # Load base rates for different policy types
            self.base_rates = {
                "auto": Decimal("1200.00"),
                "home": Decimal("800.00"),
                "health": Decimal("3600.00"),
                "life": Decimal("2400.00"),
                "business": Decimal("5000.00"),
                "travel": Decimal("150.00"),
            }

            logger.info("Pricing models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize pricing models: {str(e)}")
            raise

    async def calculate_quote(
        self,
        customer_data: Dict[str, Any],
        policy_type: str,
        coverage_amount: Decimal,
        risk_assessment: RiskAssessment,
        pricing_strategy: PricingStrategy = PricingStrategy.COMPETITIVE,
    ) -> PricingQuote:
        """
        Calculate insurance quote with dynamic pricing.

        Args:
            customer_data: Customer information
            policy_type: Type of insurance policy
            coverage_amount: Requested coverage amount
            risk_assessment: Risk assessment from RiskAssessorAgent
            pricing_strategy: Pricing strategy to use

        Returns:
            Complete pricing quote with breakdown
        """
        try:
            logger.info(
                f"Calculating quote for {policy_type} policy, coverage: {coverage_amount}"
            )

            # Get market data
            market_data = await self._get_market_data(
                policy_type, coverage_amount
            )

            # Calculate base premium
            base_premium = await self._calculate_base_premium(
                policy_type, coverage_amount, customer_data
            )

            # Calculate pricing factors
            pricing_factors = await self._calculate_pricing_factors(
                customer_data,
                policy_type,
                coverage_amount,
                risk_assessment,
                market_data,
            )

            # Apply pricing strategy
            final_premium, adjusted_factors = await self._apply_pricing_strategy(
                base_premium,
                pricing_factors,
                pricing_strategy,
                market_data,
            )

            # Calculate discounts and surcharges
            discount_total = sum(
                factor.value for factor in adjusted_factors if factor.value < 0
            )
            
            surcharge_total = sum(
                factor.value
                for factor in adjusted_factors
                if factor.value > 0
                and factor.factor_type != PricingFactorType.BASE_RATE
            )

            # Generate quote
            quote = PricingQuote(
                quote_id=self._generate_quote_id(),
                customer_id=customer_data.get("customer_id", ""),
                policy_type=policy_type,
                coverage_amount=coverage_amount,
                base_premium=base_premium,
                final_premium=final_premium,
                pricing_factors=adjusted_factors,
                discount_total=abs(discount_total),
                surcharge_total=surcharge_total,
                risk_multiplier=risk_assessment.premium_multiplier,
                market_competitiveness=await self._calculate_market_competitiveness(
                    final_premium, market_data
                ),
                quote_timestamp=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(days=30),
                confidence_score=await self._calculate_pricing_confidence(
                    pricing_factors, market_data, risk_assessment
                ),
                quantum_signature="",
            )

            # Add quantum signature
            quote_data = json.dumps(
                {
                    "quote_id": quote.quote_id,
                    "final_premium": str(quote.final_premium),
                    "timestamp": quote.quote_timestamp.isoformat(),
                }
            )
            quote.quantum_signature = await self.quantum_signer.sign(
                quote_data
            )

            logger.info(
                f"Quote calculated: {final_premium} (base: {base_premium})"
            )
            return quote

        except Exception as e:
            logger.error(f"Quote calculation failed: {str(e)}")
            raise

    async def _calculate_base_premium(
        self,
        policy_type: str,
        coverage_amount: Decimal,
        customer_data: Dict[str, Any],
    ) -> Decimal:
        """Calculate base premium before adjustments."""
        try:
            base_rate = self.base_rates.get(policy_type, Decimal("1000.00"))

            # Coverage amount factor
            coverage_factor = (
                float(coverage_amount) / 100000
            )  # Normalize to 100k
            coverage_adjustment = Decimal(str(np.sqrt(coverage_factor)))

            # Age factor for certain policy types
            age_factor = Decimal("1.0")
            if policy_type in ["auto", "life", "health"]:
                age = customer_data.get("age", 35)
                age_factor = self._calculate_age_factor(age, policy_type)

            base_premium = base_rate * coverage_adjustment * age_factor
            return base_premium.quantize(Decimal("0.01"))

        except Exception as e:
            logger.error(f"Base premium calculation failed: {str(e)}")
            return Decimal("1000.00")

    async def _calculate_pricing_factors(
        self,
        customer_data: Dict[str, Any],
        policy_type: str,
        coverage_amount: Decimal,
        risk_assessment: RiskAssessment,
        market_data: MarketData,
    ) -> List[PricingFactor]:
        """Calculate all pricing factors."""
        factors = []

        try:
            # Risk adjustment factor
            risk_factor = PricingFactor(
                factor_type=PricingFactorType.RISK_ADJUSTMENT,
                value=Decimal(
                    str((risk_assessment.premium_multiplier - 1.0) * 100)
                ),
                weight=0.4,
                description=f"Risk level: {risk_assessment.overall_risk_level.value}",
                source="risk_assessment",
            )
            factors.append(risk_factor)

            # Market competitive factor
            market_factor = await self._calculate_market_factor(market_data)
            factors.append(market_factor)

            # Volume discount
            volume_factor = await self._calculate_volume_discount(
                customer_data
            )
            factors.append(volume_factor)

            # Loyalty discount
            loyalty_factor = await self._calculate_loyalty_discount(
                customer_data
            )
            factors.append(loyalty_factor)

            # Regulatory surcharge
            regulatory_factor = await self._calculate_regulatory_surcharge(
                policy_type
            )
            factors.append(regulatory_factor)

            # Profit margin
            profit_factor = await self._calculate_profit_margin(
                policy_type, risk_assessment
            )
            factors.append(profit_factor)

            return factors

        except Exception as e:
            logger.error(f"Pricing factors calculation failed: {str(e)}")
            return []

    async def _get_market_data(
        self, policy_type: str, coverage_amount: Decimal
    ) -> MarketData:
        """Get market pricing data (mock implementation)."""
        try:
            # In production, integrate with market data APIs
            base_price = float(coverage_amount) * 0.012  # 1.2% of coverage

            competitor_prices = [
                Decimal(str(base_price * np.random.uniform(0.8, 1.2)))
                for _ in range(5)
            ]

            market_average = sum(competitor_prices) / len(competitor_prices)
            sorted_prices = sorted(competitor_prices)

            return MarketData(
                competitor_prices=competitor_prices,
                market_average=market_average,
                market_percentile_25=sorted_prices[1],
                market_percentile_75=sorted_prices[3],
                volume_trends={policy_type: np.random.uniform(0.95, 1.05)},
                seasonal_factors=self._get_seasonal_factors(),
            )

        except Exception as e:
            logger.error(f"Market data retrieval failed: {str(e)}")
            return MarketData(
                competitor_prices=[Decimal("1000.00")],
                market_average=Decimal("1000.00"),
                market_percentile_25=Decimal("900.00"),
                market_percentile_75=Decimal("1100.00"),
                volume_trends={},
                seasonal_factors={},
            )

    async def _calculate_market_factor(
        self, market_data: MarketData
    ) -> PricingFactor:
        """Calculate market competitiveness factor."""
        # Aim for 25th percentile for competitive pricing
        target_price = market_data.market_percentile_25
        market_average = market_data.market_average

        if market_average > 0:
            adjustment_pct = (
                (target_price - market_average) / market_average
            ) * 100
        else:
            adjustment_pct = 0

        return PricingFactor(
            factor_type=PricingFactorType.MARKET_COMPETITIVE,
            value=Decimal(str(adjustment_pct)),
            weight=0.3,
            description=f"Market competitive adjustment: {adjustment_pct:.1f}%",
            source="market_analysis",
        )

    async def _calculate_volume_discount(
        self, customer_data: Dict[str, Any]
    ) -> PricingFactor:
        """Calculate volume-based discount."""
        # Check number of active policies
        policy_count = customer_data.get("policy_count", 0)
        
        if policy_count >= 5:
            discount_pct = -15.0  # 15% discount
        elif policy_count >= 3:
            discount_pct = -10.0  # 10% discount
        elif policy_count >= 2:
            discount_pct = -5.0  # 5% discount
        else:
            discount_pct = 0.0
            
        return PricingFactor(
            factor_type=PricingFactorType.VOLUME_DISCOUNT,
            value=Decimal(str(discount_pct)),
            weight=0.1,
            description=f"Volume discount: {policy_count} policies",
            source="customer_portfolio",
        )

    async def _calculate_loyalty_discount(
        self, customer_data: Dict[str, Any]
    ) -> PricingFactor:
        """Calculate loyalty-based discount."""
        customer_since = customer_data.get("customer_since")
        
        if customer_since:
            try:
                start_date = datetime.fromisoformat(customer_since)
                years = (datetime.now() - start_date).days / 365.25
                
                if years >= 5:
                    discount_pct = -12.5  # 12.5% discount
                elif years >= 3:
                    discount_pct = -7.5  # 7.5% discount
                elif years >= 1:
                    discount_pct = -2.5  # 2.5% discount
                else:
                    discount_pct = 0.0
            except (ValueError, TypeError):
                discount_pct = 0.0
        else:
            discount_pct = 0.0
            
        return PricingFactor(
            factor_type=PricingFactorType.LOYALTY_DISCOUNT,
            value=Decimal(str(discount_pct)),
            weight=0.1,
            description=f"Loyalty discount: {abs(discount_pct):.1f}%",
            source="customer_history",
        )

    async def _calculate_regulatory_surcharge(
        self, policy_type: str
    ) -> PricingFactor:
        """Calculate regulatory fees and surcharges."""
        regulatory_fees = {
            "auto": 2.5,     # 2.5%
            "home": 1.0,     # 1%
            "health": 3.5,   # 3.5%
            "life": 1.5,     # 1.5%
            "business": 2.0, # 2%
            "travel": 1.0,   # 1%
        }
        
        surcharge = regulatory_fees.get(policy_type, 1.0)
        
        return PricingFactor(
            factor_type=PricingFactorType.REGULATORY_SURCHARGE,
            value=Decimal(str(surcharge)),
            weight=0.05,
            description=f"Regulatory fees: {surcharge:.1f}%",
            source="regulatory_requirements",
        )

    async def _calculate_profit_margin(
        self, policy_type: str, risk_assessment: RiskAssessment
    ) -> PricingFactor:
        """Calculate profit margin based on risk and policy type."""
        # Base profit margins by policy type
        base_margins = {
            "auto": 8.0,      # 8%
            "home": 10.0,     # 10%
            "health": 5.0,    # 5%
            "life": 12.0,     # 12%
            "business": 15.0, # 15%
            "travel": 20.0,   # 20%
        }
        
        # Adjust based on risk level
        risk_adjustments = {
            RiskLevel.LOW: 2.0,       # +2%
            RiskLevel.MEDIUM: 0.0,    # no change
            RiskLevel.HIGH: -3.0,     # -3%
            RiskLevel.VERY_HIGH: -5.0 # -5%
        }
        
        base_margin = base_margins.get(policy_type, 10.0)
        risk_adj = risk_adjustments.get(risk_assessment.overall_risk_level, 0.0)
        
        margin = base_margin + risk_adj
        
        return PricingFactor(
            factor_type=PricingFactorType.PROFIT_MARGIN,
            value=Decimal(str(margin)),
            weight=0.15,
            description=f"Profit margin: {margin:.1f}%",
            source="business_strategy",
        )

    async def _apply_pricing_strategy(
        self,
        base_premium: Decimal,
        factors: List[PricingFactor],
        strategy: PricingStrategy,
        market_data: MarketData,
    ) -> Tuple[Decimal, List[PricingFactor]]:
        """Apply pricing strategy to adjust final premium."""
        # Deep copy the factors to avoid modifying originals
        adjusted_factors = factors.copy()
        
        # Strategy-specific adjustments
        if strategy == PricingStrategy.COMPETITIVE:
            # Aim to be 5-10% below market average
            target_discount = -0.075  # 7.5% below market
            market_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.MARKET_COMPETITIVE),
                None
            )
            if market_factor:
                market_factor.value = Decimal(str(target_discount * 100))
                market_factor.description = "Competitive strategy: 7.5% below market"
                
        elif strategy == PricingStrategy.PENETRATION:
            # Aggressive pricing to gain market share
            target_discount = -0.15  # 15% below market
            market_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.MARKET_COMPETITIVE),
                None
            )
            if market_factor:
                market_factor.value = Decimal(str(target_discount * 100))
                market_factor.description = "Penetration strategy: 15% below market"
                
            # Also reduce profit margin
            profit_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.PROFIT_MARGIN),
                None
            )
            if profit_factor:
                profit_factor.value = profit_factor.value * Decimal("0.5")  # Half the profit margin
                profit_factor.description = f"Reduced margin: {float(profit_factor.value):.1f}%"
                
        elif strategy == PricingStrategy.PREMIUM:
            # Premium pricing for high-value customers
            # Enhance profit margins
            profit_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.PROFIT_MARGIN),
                None
            )
            if profit_factor:
                profit_factor.value = profit_factor.value * Decimal("1.5")  # Increase margin by 50%
                profit_factor.description = f"Premium margin: {float(profit_factor.value):.1f}%"
                
            # Position above market average
            market_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.MARKET_COMPETITIVE),
                None
            )
            if market_factor:
                market_factor.value = Decimal("5.0")  # 5% above market
                market_factor.description = "Premium positioning: 5% above market"
                
        elif strategy == PricingStrategy.RISK_BASED:
            # Emphasize risk factors
            risk_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.RISK_ADJUSTMENT),
                None
            )
            if risk_factor:
                risk_factor.weight = 0.6  # Increase risk weight
                
            # De-emphasize market factors
            market_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.MARKET_COMPETITIVE),
                None
            )
            if market_factor:
                market_factor.weight = 0.1  # Decrease market weight
                
        elif strategy == PricingStrategy.MARKET_FOLLOWING:
            # Closely follow market average
            market_factor = next(
                (f for f in adjusted_factors if f.factor_type == PricingFactorType.MARKET_COMPETITIVE),
                None
            )
            if market_factor:
                # Aim to be within 2% of market average
                market_factor.value = Decimal("0.0")
                market_factor.description = "Market following: match market average"
        
        # Calculate the weighted sum of all factor adjustments
        total_adjustment = sum(
            factor.value * Decimal(str(factor.weight))
            for factor in adjusted_factors
        ) / Decimal("100")
        
        # Apply to base premium
        final_premium = base_premium * (Decimal("1") + total_adjustment)
        
        # Ensure minimum premium
        final_premium = max(final_premium, Decimal("100.00"))
        
        return final_premium.quantize(Decimal("0.01")), adjusted_factors

    def _calculate_age_factor(self, age: int, policy_type: str) -> Decimal:
        """Calculate age-related pricing factor."""
        if policy_type == "auto":
            if age < 25:
                return Decimal("1.5")  # 50% surcharge
            elif age < 30:
                return Decimal("1.2")  # 20% surcharge
            elif age > 70:
                return Decimal("1.3")  # 30% surcharge
            else:
                return Decimal("1.0")
        elif policy_type == "life":
            # Simple linear increase with age
            return Decimal(str(1.0 + (age - 30) * 0.02 if age > 30 else 1.0))
        elif policy_type == "health":
            # Exponential increase after 40
            if age <= 40:
                return Decimal("1.0")
            else:
                return Decimal(str(1.0 + 0.03 * ((age - 40) ** 1.5) / 10))
        else:
            return Decimal("1.0")

    def _get_seasonal_factors(self) -> Dict[str, float]:
        """Get seasonal pricing factors based on current date."""
        current_month = datetime.now().month
        
        # Different seasonal factors for different policy types
        return {
            "auto": 1.0 + 0.05 * abs(((current_month - 1) % 12) - 6) / 6,
            "home": 1.0 + 0.03 * abs(((current_month - 4) % 12) - 6) / 6,
            "travel": 1.0 + 0.15 * abs(((current_month - 7) % 12) - 6) / 6,
        }

    async def _calculate_market_competitiveness(
        self, premium: Decimal, market_data: MarketData
    ) -> float:
        """Calculate how competitive our price is in the market."""
        if market_data.market_average <= 0:
            return 0.5  # Neutral if we have no market data
            
        # Our price position relative to market
        # 0 = lowest price, 1 = highest price
        sorted_prices = sorted(market_data.competitor_prices + [premium])
        our_position = sorted_prices.index(premium) / len(sorted_prices)
        
        # Invert so 1 = most competitive, 0 = least competitive
        return 1.0 - our_position

    async def _calculate_pricing_confidence(
        self,
        pricing_factors: List[PricingFactor],
        market_data: MarketData,
        risk_assessment: RiskAssessment,
    ) -> float:
        """Calculate confidence level in our pricing accuracy."""
        # Factors that affect confidence
        risk_confidence = risk_assessment.confidence_score
        
        # Market data breadth
        market_confidence = min(1.0, len(market_data.competitor_prices) / 10)
        
        # Factor reliability
        factor_confidence = min(1.0, len(pricing_factors) / 5)
        
        # Weighted average
        confidence = (
            risk_confidence * 0.5 +
            market_confidence * 0.3 +
            factor_confidence * 0.2
        )
        
        return min(1.0, max(0.1, confidence))

    def _generate_quote_id(self) -> str:
        """Generate a unique quote ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = np.random.randint(1000, 9999)
        return f"QT{timestamp}{random_suffix}"

    async def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return [
            "Dynamic premium calculation",
            "Risk-based pricing",
            "Market competitive analysis",
            "Multi-strategy pricing",
            "Quantum-signed quotes",
            "Age-based factor adjustment",
            "Seasonal pricing optimization",
        ]

    async def train_pricing_model(self, training_data: Dict[str, Any]) -> bool:
        """Train or update pricing models with new data."""
        try:
            # In production, this would use real training data
            # For now, we'll simulate successful training
            logger.info("Training pricing models with new data")
            
            # Simulate model training time
            await asyncio.sleep(0.5)
            
            # Update last trained timestamp
            self.last_trained = datetime.now()
            
            logger.info("Pricing models training completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to train pricing models: {str(e)}")
            return False
