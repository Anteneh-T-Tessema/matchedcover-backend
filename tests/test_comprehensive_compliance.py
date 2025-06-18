"""
Comprehensive Regulatory Compliance Integration Tests

This module tests the complete regulatory compliance system including
federal, state, AML/BSA, AI, and blockchain compliance components.
"""

import pytest
import pytest_asyncio
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

from src.compliance.regulatory_compliance import get_compliance_manager, ComplianceRegulation
from src.compliance.aml_bsa_compliance import get_aml_bsa_manager, AMLRiskLevel
from src.compliance.state_specific_compliance import get_state_compliance_manager, State


class TestComprehensiveCompliance:
    """Test suite for comprehensive regulatory compliance."""
    
    @pytest_asyncio.fixture
    async def compliance_managers(self):
        """Set up all compliance managers."""
        federal_manager = await get_compliance_manager()
        aml_manager = await get_aml_bsa_manager()
        state_manager = await get_state_compliance_manager()
        
        return {
            "federal": federal_manager,
            "aml": aml_manager,
            "state": state_manager
        }
    
    @pytest.mark.asyncio
    async def test_federal_compliance_integration(self, compliance_managers):
        """Test federal compliance components integration."""
        federal_manager = compliance_managers["federal"]
        
        # Test AI model compliance
        model_data = {
            "name": "fraud_detection_model_v1",
            "version": "1.0.0",
            "development_documentation": True,
            "validation_documentation": True,
            "monitoring_procedures": True,
            "bias_testing_results": True,
            "performance_benchmarks": True,
            "bias_metrics": {
                "demographic_parity": 0.85,
                "equal_opportunity": 0.82,
                "calibration": 0.88
            },
            "explainability_score": 0.75,
            "performance_metrics": {
                "accuracy": 0.92,
                "precision": 0.85,
                "recall": 0.88
            }
        }
        
        result = await federal_manager.validate_ai_model_compliance(
            "fraud_model_001", model_data
        )
        
        assert result["compliance_passed"] is True
        assert result["documentation_complete"] is True
        assert result["fairness_passed"] is True
        assert result["explainability_passed"] is True
        assert result["performance_passed"] is True
        
        # Test blockchain compliance
        blockchain_data = {
            "network_id": "fabric-network-001",
            "chaincode_version": "1.0.0",
            "audit_trail_enabled": True,
            "data_retention_policy": "2555_days",
            "immutability_verified": True,
            "access_controls": {
                "role_based_access": True,
                "audit_logging": True,
                "regulatory_access": True,
                "data_encryption": True
            },
            "regulatory_access_enabled": True,
            "backup_procedures_tested": True
        }
        
        blockchain_result = await federal_manager.validate_blockchain_compliance(
            blockchain_data
        )
        
        assert blockchain_result["compliance_passed"] is True
        assert blockchain_result["audit_trail_enabled"] is True
        assert blockchain_result["regulatory_access_enabled"] is True
        
        # Test adverse action requirements
        decision_data = {
            "customer_id": "customer_001",
            "application_denied": True,
            "credit_report_used": True,
            "decision_type": "underwriting",
            "data_sources": ["credit_bureau", "external_data"]
        }
        
        adverse_action_result = await federal_manager.check_adverse_action_requirements(
            decision_data
        )
        
        assert adverse_action_result["adverse_action_required"] is True
        assert "Nature of adverse action" in adverse_action_result["required_disclosures"]
    
    @pytest.mark.asyncio
    async def test_aml_bsa_compliance_integration(self, compliance_managers):
        """Test AML/BSA compliance components integration."""
        aml_manager = compliance_managers["aml"]
        
        # Test customer identification program
        customer_data = {
            "customer_id": "customer_002",
            "name": "John Doe",
            "date_of_birth": "1980-01-15",
            "id_type": "SSN",
            "id_number": "123-45-6789",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            },
            "phone": "555-123-4567",
            "email": "john.doe@email.com",
            "country": "US"
        }
        
        cip_result = await aml_manager.conduct_customer_identification(customer_data)
        
        assert cip_result["compliance_passed"] is True
        assert cip_result["verification_status"] == "verified"
        assert cip_result["sanctions_clear"] is True
        assert cip_result["risk_level"] in ["low", "medium", "high"]
        
        # Test OFAC sanctions screening
        sanctions_result = await aml_manager.screen_ofac_sanctions(customer_data)
        
        assert "screening_id" in sanctions_result
        assert "ofac_match" in sanctions_result
        assert "screening_date" in sanctions_result
        
        # Test suspicious activity monitoring
        transaction_data = {
            "customer_id": "customer_002",
            "amount": 15000.0,
            "type": "cash_deposit",
            "transaction_date": datetime.now(timezone.utc).isoformat()
        }
        
        suspicious_result = await aml_manager.monitor_suspicious_activity(transaction_data)
        
        assert "suspicious_activity_detected" in suspicious_result
        assert "sar_required" in suspicious_result
        assert "risk_score" in suspicious_result
        
        # Test CTR requirements
        ctr_result = await aml_manager.check_ctr_requirements({
            **transaction_data,
            "is_cash": True
        })
        
        assert "ctr_required" in ctr_result
    
    @pytest.mark.asyncio
    async def test_state_compliance_integration(self, compliance_managers):
        """Test state-specific compliance integration."""
        state_manager = compliance_managers["state"]
        
        # Test California compliance
        business_data = {
            "licenses": ["property_casualty", "life_health"],
            "ai_systems": ["fraud_detection", "underwriting"],
            "cybersecurity_program": True,
            "data_privacy_program": True,
            "claims_data": {
                "total_claims": 1000,
                "settled_claims": 950,
                "average_settlement_time_days": 25
            },
            "complaints": {
                "total_complaints": 15,
                "resolved_complaints": 14
            }
        }
        
        ca_result = await state_manager.check_state_compliance(
            State.CALIFORNIA, business_data
        )
        
        assert ca_result["state"] == "CA"
        assert "overall_compliance_score" in ca_result
        assert "compliance_details" in ca_result
        assert "recommended_actions" in ca_result
        
        # Test New York compliance
        ny_result = await state_manager.check_state_compliance(
            State.NEW_YORK, business_data
        )
        
        assert ny_result["state"] == "NY"
        assert "regulator" in ny_result
        
        # Test rate filing management
        filing_data = {
            "filing_id": "RF_CA_001",
            "product_name": "Auto Insurance Premium",
            "filing_type": "revision",
            "effective_date": (datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
            "rate_change_percentage": 5.2,
            "justification": "Increased claims costs and regulatory changes",
            "actuarial_memorandum": "Detailed actuarial analysis attached",
            "supporting_documents": ["actuarial_analysis.pdf", "claims_data.xlsx"]
        }
        
        filing_result = await state_manager.manage_rate_filing(
            State.CALIFORNIA, filing_data
        )
        
        assert filing_result["status"] == "submitted"
        assert "expected_decision_date" in filing_result
        assert "tracking_number" in filing_result
        
        # Test market conduct compliance
        market_metrics = {
            "complaints": 50,
            "policies_in_force": 10000,
            "claims_settled": 4500,
            "total_claims": 4700,
            "written_premiums": 50000000,
            "surplus": 20000000
        }
        
        market_result = await state_manager.track_market_conduct_compliance(
            State.CALIFORNIA, market_metrics
        )
        
        assert "market_conduct_score" in market_result
        assert "exam_risk_level" in market_result
        assert "metrics" in market_result
    
    @pytest.mark.asyncio
    async def test_cross_system_compliance_integration(self, compliance_managers):
        """Test integration across all compliance systems."""
        federal_manager = compliance_managers["federal"]
        aml_manager = compliance_managers["aml"]
        state_manager = compliance_managers["state"]
        
        # Simulate comprehensive business assessment
        business_scenario = {
            "company_info": {
                "name": "TestCover Insurance",
                "states_operating": ["CA", "NY", "TX"],
                "business_lines": ["auto", "property", "life"]
            },
            "ai_systems": [
                {
                    "model_id": "fraud_detector_v2",
                    "name": "Fraud Detection Model",
                    "version": "2.0.0",
                    "performance_metrics": {"accuracy": 0.94, "precision": 0.87, "recall": 0.89},
                    "bias_metrics": {"demographic_parity": 0.83, "equal_opportunity": 0.85},
                    "explainability_score": 0.78,
                    "development_documentation": True,
                    "validation_documentation": True,
                    "monitoring_procedures": True,
                    "bias_testing_results": True,
                    "performance_benchmarks": True
                }
            ],
            "blockchain_config": {
                "network_id": "production-fabric-network",
                "audit_trail_enabled": True,
                "data_retention_policy": "2555_days",
                "immutability_verified": True,
                "access_controls": {
                    "role_based_access": True,
                    "audit_logging": True,
                    "regulatory_access": True,
                    "data_encryption": True
                },
                "regulatory_access_enabled": True,
                "backup_procedures_tested": True
            },
            "customers": [
                {
                    "customer_id": "cust_001",
                    "name": "Customer One",
                    "risk_level": "low",
                    "verification_status": "verified"
                }
            ]
        }
        
        # Test federal compliance
        ai_model = business_scenario["ai_systems"][0]
        federal_ai_result = await federal_manager.validate_ai_model_compliance(
            ai_model["model_id"], ai_model
        )
        
        federal_blockchain_result = await federal_manager.validate_blockchain_compliance(
            business_scenario["blockchain_config"]
        )
        
        # Test AML compliance
        customer = business_scenario["customers"][0]
        aml_customer_result = await aml_manager.conduct_customer_identification({
            **customer,
            "date_of_birth": "1985-03-20",
            "id_type": "SSN",
            "id_number": "987-65-4321",
            "address": {"street": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "zip": "90210"},
            "phone": "555-987-6543",
            "email": "customer.one@email.com",
            "country": "US"
        })
        
        # Test state compliance for multiple states
        state_results = {}
        for state_code in business_scenario["company_info"]["states_operating"]:
            try:
                state_enum = State(state_code)
                state_result = await state_manager.check_state_compliance(
                    state_enum, {
                        "licenses": business_scenario["company_info"]["business_lines"],
                        "ai_systems": [ai["name"] for ai in business_scenario["ai_systems"]],
                        "cybersecurity_program": True,
                        "data_privacy_program": True
                    }
                )
                state_results[state_code] = state_result
            except ValueError:
                continue
        
        # Generate comprehensive compliance report
        end_date = datetime.now(timezone.utc).isoformat()
        start_date = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
        
        federal_report = await federal_manager.generate_compliance_report(
            start_date, end_date
        )
        
        aml_report = await aml_manager.generate_aml_report(
            start_date, end_date
        )
        
        # Assertions for comprehensive integration
        assert federal_ai_result["compliance_passed"] is True
        assert federal_blockchain_result["compliance_passed"] is True
        assert aml_customer_result["compliance_passed"] is True
        
        assert len(state_results) > 0
        for state_code, state_result in state_results.items():
            assert state_result["state"] == state_code
            assert "overall_compliance_score" in state_result
        
        assert "report_period" in federal_report
        assert "executive_summary" in aml_report
        
        # Calculate overall compliance score
        scores = []
        scores.append(100 if federal_ai_result["compliance_passed"] else 0)
        scores.append(100 if federal_blockchain_result["compliance_passed"] else 0)
        scores.append(100 if aml_customer_result["compliance_passed"] else 0)
        
        for state_result in state_results.values():
            scores.append(state_result.get("overall_compliance_score", 0))
        
        overall_score = sum(scores) / len(scores) if scores else 0
        
        # Assert minimum compliance threshold
        assert overall_score >= 85.0, f"Overall compliance score {overall_score} below threshold"
        
        print(f"✅ Comprehensive compliance integration test passed!")
        print(f"📊 Overall compliance score: {overall_score:.1f}%")
        print(f"🏛️ Federal compliance: {'✅ PASS' if federal_ai_result['compliance_passed'] else '❌ FAIL'}")
        print(f"🚨 AML/BSA compliance: {'✅ PASS' if aml_customer_result['compliance_passed'] else '❌ FAIL'}")
        print(f"🗺️ State compliance: {len(state_results)} states assessed")
        
    @pytest.mark.asyncio
    async def test_compliance_dashboard_integration(self, compliance_managers):
        """Test compliance dashboard integration."""
        federal_manager = compliance_managers["federal"]
        
        dashboard_data = await federal_manager.get_compliance_dashboard()
        
        assert "overall_status" in dashboard_data
        assert "recent_events_count" in dashboard_data
        assert "next_reviews" in dashboard_data
        
        print("✅ Compliance dashboard integration test passed!")
    
    @pytest.mark.asyncio
    async def test_regulatory_change_monitoring(self, compliance_managers):
        """Test regulatory change monitoring capabilities."""
        # This would test real-time monitoring of regulatory changes
        # For now, we'll test the structure and basic functionality
        
        federal_manager = compliance_managers["federal"]
        
        # Test compliance event logging
        await federal_manager._log_compliance_event({
            "event_id": "test_event_001",
            "regulation": ComplianceRegulation.NAIC_AI_GOVERNANCE,
            "event_type": "check",
            "severity": "low",
            "description": "Test compliance check",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": {"test": True},
            "remediation_required": False
        })
        
        # Verify event was logged
        assert len(federal_manager.compliance_events) > 0
        
        print("✅ Regulatory change monitoring test passed!")


if __name__ == "__main__":
    # Run the integration tests
    pytest.main([__file__, "-v", "--tb=short"])
