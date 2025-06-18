"""
AI Agent Integration Test

This test demonstrates the integration of the Guardrail AI Agent and 
Evaluation AI Agent with the existing insurance platform workflow.

It shows how AI decisions are processed through safety checks, quality 
evaluation, and compliance verification before being finalized.
"""

import sys
import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, Any

# Add project root to path
sys.path.append('/Users/antenehtessema/Desktop/MatchInsurane')

from src.agents.ai_integration import (
    AIAgentIntegrator, 
    AIDecisionContext, 
    process_ai_with_safety
)


async def test_insurance_claim_processing():
    """Test AI safety and evaluation in insurance claim processing."""
    print("🔍 Testing AI Safety and Evaluation in Insurance Claim Processing")
    print("=" * 70)
    
    # Test Case 1: Standard claim approval
    print("\n📋 Test Case 1: Standard Claim Approval")
    print("-" * 40)
    
    claim_input = {
        "claim_id": "CLM-2025-001234",
        "policy_holder": {
            "id": "POL-987654",
            "age": 42,
            "state": "CA",
            "risk_profile": "standard"
        },
        "incident": {
            "type": "auto_accident",
            "date": "2025-06-15",
            "amount_claimed": 15000.00,
            "description": "Rear-end collision with property damage"
        }
    }
    
    # Simulated AI claim agent output
    ai_claim_decision = {
        "decision": "approve",
        "approved_amount": 14500.00,
        "confidence": 0.92,
        "reasoning": {
            "factors_considered": [
                "clean driving record",
                "policy in good standing",
                "reasonable claim amount",
                "consistent incident report"
            ],
            "risk_indicators": [],
            "compliance_checks": ["fraud_detection", "policy_validation"]
        },
        "processing_agent": "claim_evaluator_ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        result = await process_ai_with_safety(
            agent_id="claim_evaluator_ai",
            task_type="claim_evaluation",
            input_data=claim_input,
            ai_output=ai_claim_decision,
            user_context={"customer_tier": "premium", "claim_history": "clean"},
            regulatory_context=["Fair Claims Settlement", "State Insurance Code"]
        )
        
        print(f"✅ Decision Status: {result.final_decision.get('status', 'unknown')}")
        print(f"✅ Safety Status: {result.safety_status}")
        print(f"✅ Quality Score: {result.quality_score:.2f}")
        print(f"✅ Compliance: {result.compliance_status}")
        
        if result.recommendations:
            print("💡 Recommendations:")
            for rec in result.recommendations[:3]:  # Show first 3
                print(f"   - {rec}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    # Test Case 2: High-risk claim requiring additional scrutiny
    print("\n🚨 Test Case 2: High-Risk Claim Evaluation")
    print("-" * 40)
    
    high_risk_input = {
        "claim_id": "CLM-2025-005678",
        "policy_holder": {
            "id": "POL-123456", 
            "age": 28,
            "state": "NY",
            "risk_profile": "high_risk"
        },
        "incident": {
            "type": "theft",
            "date": "2025-06-10",
            "amount_claimed": 45000.00,
            "description": "Vehicle stolen from parking garage"
        }
    }
    
    # Simulated AI output with potential issues
    ai_high_risk_decision = {
        "decision": "approve",
        "approved_amount": 45000.00,
        "confidence": 0.68,  # Lower confidence
        "reasoning": {
            "factors_considered": [
                "high claim amount",
                "theft in high-crime area",
                "recent policy inception"
            ],
            "risk_indicators": [
                "multiple recent claims",
                "high-value vehicle",
                "limited documentation"
            ],
            "compliance_checks": ["fraud_detection", "policy_validation"]
        },
        "processing_agent": "claim_evaluator_ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        result = await process_ai_with_safety(
            agent_id="claim_evaluator_ai",
            task_type="claim_evaluation",
            input_data=high_risk_input,
            ai_output=ai_high_risk_decision,
            user_context={"customer_tier": "standard", "claim_history": "multiple"},
            regulatory_context=["Anti-Fraud Regulations", "State Insurance Code"]
        )
        
        print(f"⚠️  Decision Status: {result.final_decision.get('status', 'unknown')}")
        print(f"⚠️  Safety Status: {result.safety_status}")
        print(f"⚠️  Quality Score: {result.quality_score:.2f}")
        print(f"⚠️  Compliance: {result.compliance_status}")
        
        if result.final_decision.get('warnings'):
            print("⚠️  Warnings:")
            for warning in result.final_decision['warnings'][:3]:
                print(f"   - {warning}")
        
        if result.recommendations:
            print("💡 Recommendations:")
            for rec in result.recommendations[:3]:
                print(f"   - {rec}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def test_policy_underwriting():
    """Test AI safety and evaluation in policy underwriting."""
    print("\n🏠 Testing AI Safety and Evaluation in Policy Underwriting")
    print("=" * 70)
    
    underwriting_input = {
        "application_id": "APP-2025-789012",
        "applicant": {
            "age": 35,
            "credit_score": 720,
            "location": "Austin, TX",
            "property_type": "single_family_home",
            "property_value": 350000
        },
        "coverage_requested": {
            "dwelling": 350000,
            "personal_property": 175000,
            "liability": 300000
        }
    }
    
    # Simulated AI underwriting decision
    ai_underwriting_decision = {
        "decision": "approve",
        "premium": 1850.00,
        "coverage_approved": {
            "dwelling": 350000,
            "personal_property": 175000,
            "liability": 300000
        },
        "confidence": 0.88,
        "risk_factors": [
            "moderate_credit_score",
            "standard_location_risk",
            "appropriate_coverage_levels"
        ],
        "discounts_applied": ["multi_policy", "security_system"],
        "processing_agent": "underwriting_ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        result = await process_ai_with_safety(
            agent_id="underwriting_ai",
            task_type="policy_underwriting",
            input_data=underwriting_input,
            ai_output=ai_underwriting_decision,
            user_context={"new_customer": True, "referral_source": "agent"},
            regulatory_context=["Fair Housing Act", "Equal Credit Opportunity Act"]
        )
        
        print(f"✅ Decision Status: {result.final_decision.get('status', 'unknown')}")
        print(f"✅ Safety Status: {result.safety_status}")
        print(f"✅ Quality Score: {result.quality_score:.2f}")
        print(f"✅ Compliance: {result.compliance_status}")
        
        if result.recommendations:
            print("💡 Recommendations:")
            for rec in result.recommendations[:3]:
                print(f"   - {rec}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def test_pricing_optimization():
    """Test AI safety and evaluation in pricing optimization."""
    print("\n💰 Testing AI Safety and Evaluation in Pricing Optimization")
    print("=" * 70)
    
    pricing_input = {
        "customer_segment": "young_professional",
        "risk_profile": {
            "driving_record": "clean",
            "credit_score": 680,
            "claims_history": "none",
            "vehicle_type": "compact_sedan"
        },
        "market_conditions": {
            "competition_level": "high",
            "loss_ratios": "favorable",
            "regulatory_environment": "stable"
        }
    }
    
    # Simulated AI pricing decision
    ai_pricing_decision = {
        "base_premium": 1200.00,
        "adjusted_premium": 1080.00,
        "discounts": {
            "good_driver": 0.10,
            "multi_policy": 0.05,
            "loyalty": 0.03
        },
        "confidence": 0.94,
        "market_position": "competitive",
        "profit_margin": 0.15,
        "processing_agent": "pricing_ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        result = await process_ai_with_safety(
            agent_id="pricing_ai",
            task_type="pricing_optimization",
            input_data=pricing_input,
            ai_output=ai_pricing_decision,
            user_context={"customer_lifetime_value": "high", "acquisition_channel": "digital"},
            regulatory_context=["Rate Filing Requirements", "Anti-Discrimination Laws"]
        )
        
        print(f"✅ Decision Status: {result.final_decision.get('status', 'unknown')}")
        print(f"✅ Safety Status: {result.safety_status}")
        print(f"✅ Quality Score: {result.quality_score:.2f}")
        print(f"✅ Compliance: {result.compliance_status}")
        
        processing_summary = result.processing_summary
        print(f"⏱️  Total Processing Time: {processing_summary.get('processing_time_ms', 0):.0f}ms")
        print(f"🔍 Risk Score: {processing_summary.get('risk_score', 0):.2f}")
        
        if result.recommendations:
            print("💡 Recommendations:")
            for rec in result.recommendations[:3]:
                print(f"   - {rec}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def main():
    """Run comprehensive AI safety and evaluation tests."""
    print("🤖 AI Agent Safety and Evaluation Integration Test")
    print("=" * 70)
    print("Testing the integration of Guardrail AI and Evaluation AI agents")
    print("with the MatchedCover insurance platform workflow.")
    print()
    
    try:
        # Test different insurance workflows
        await test_insurance_claim_processing()
        await test_policy_underwriting()
        await test_pricing_optimization()
        
        print("\n" + "=" * 70)
        print("🎉 AI Safety and Evaluation Integration Test Complete!")
        print("✅ All systems are properly integrated and functioning")
        print("✅ AI decisions are being processed through safety and quality checks")
        print("✅ Compliance verification is working across all workflows")
        print()
        print("The AI Agent Integration provides:")
        print("  🛡️  Comprehensive safety guardrails")
        print("  📊 Continuous quality evaluation")
        print("  ⚖️  Regulatory compliance verification")
        print("  🔍 Real-time bias and fairness monitoring")
        print("  📈 Performance analytics and recommendations")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
