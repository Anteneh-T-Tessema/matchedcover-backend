#!/usr/bin/env python3
"""
Integration Test Suite for Enhanced Fraud Detection System

This script tests the integration of all enhanced fraud detection components
including the agent, API endpoints, and enterprise features.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid

import httpx
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.enhanced_fraud_detection_agent import EnhancedFraudDetectionAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.audit_agent import AuditAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegrationTestSuite:
    """Integration test suite for enhanced fraud detection system."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize test suite."""
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.fraud_endpoint = f"{self.api_base}/fraud-detection"
        self.test_results: List[Dict[str, Any]] = []
        
    async def setup(self):
        """Set up test environment."""
        logger.info("Setting up integration test environment...")
        
        # Initialize agents for direct testing
        self.fraud_agent = EnhancedFraudDetectionAgent()
        self.compliance_agent = ComplianceAgent()
        self.audit_agent = AuditAgent()
        
        # Initialize agents
        await self.fraud_agent.initialize()
        await self.compliance_agent.initialize()
        await self.audit_agent.initialize()
        
        logger.info("Test environment setup complete")
        
    async def teardown(self):
        """Clean up test environment."""
        logger.info("Cleaning up test environment...")
        # Add cleanup logic here if needed
        logger.info("Test environment cleanup complete")
    
    def create_sample_claim_data(self, risk_level: str = "medium") -> Dict[str, Any]:
        """Create sample claim data for testing."""
        base_claim = {
            "claim_id": str(uuid.uuid4()),
            "policy_number": f"POL{uuid.uuid4().hex[:8].upper()}",
            "claim_amount": 15000.0,
            "incident_date": (datetime.now() - timedelta(days=5)).isoformat(),
            "reported_date": (datetime.now() - timedelta(days=3)).isoformat(),
            "claim_type": "auto",
            "description": "Vehicle collision on highway",
            "location": "Los Angeles, CA",
            "claimant": {
                "name": "John Smith",
                "phone": "555-0123",
                "email": "john.smith@email.com",
                "address": "123 Main St, Los Angeles, CA 90210",
                "ssn_last_four": "1234"
            },
            "vehicle": {
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "vin": "1HGBH41JXMN109186"
            },
            "incident_details": {
                "weather": "clear",
                "time_of_day": "14:30",
                "traffic_conditions": "moderate",
                "police_report": True,
                "injuries": False
            }
        }
        
        # Modify data based on risk level
        if risk_level == "high":
            base_claim.update({
                "claim_amount": 85000.0,
                "incident_details": {
                    **base_claim["incident_details"],
                    "injuries": True,
                    "weather": "heavy rain",
                    "time_of_day": "02:30"
                },
                "reported_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "description": "Major collision with total loss and injuries"
            })
        elif risk_level == "low":
            base_claim.update({
                "claim_amount": 2500.0,
                "description": "Minor fender bender in parking lot"
            })
            
        return base_claim
    
    async def test_agent_initialization(self) -> Dict[str, Any]:
        """Test that all agents initialize properly."""
        logger.info("Testing agent initialization...")
        
        try:
            # Test fraud detection agent
            assert self.fraud_agent is not None
            assert hasattr(self.fraud_agent, 'model_manager')
            assert hasattr(self.fraud_agent, 'compliance_checker')
            assert hasattr(self.fraud_agent, 'explainer')
            
            # Test compliance agent
            assert self.compliance_agent is not None
            
            # Test audit agent
            assert self.audit_agent is not None
            
            result = {
                "test": "agent_initialization",
                "status": "PASSED",
                "message": "All agents initialized successfully",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "agent_initialization",
                "status": "FAILED",
                "message": f"Agent initialization failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_fraud_detection_analysis(self) -> Dict[str, Any]:
        """Test fraud detection analysis functionality."""
        logger.info("Testing fraud detection analysis...")
        
        try:
            # Test with different risk levels
            test_claims = [
                ("low_risk", self.create_sample_claim_data("low")),
                ("medium_risk", self.create_sample_claim_data("medium")),
                ("high_risk", self.create_sample_claim_data("high"))
            ]
            
            analysis_results = []
            
            for risk_level, claim_data in test_claims:
                logger.info(f"Analyzing {risk_level} claim...")
                
                analysis = await self.fraud_agent.analyze_claim(claim_data)
                
                # Validate analysis structure
                assert "fraud_score" in analysis
                assert "risk_level" in analysis
                assert "confidence" in analysis
                assert "explanation" in analysis
                assert "recommendations" in analysis
                assert "compliance_status" in analysis
                
                # Validate fraud score range
                assert 0 <= analysis["fraud_score"] <= 1
                assert 0 <= analysis["confidence"] <= 1
                
                analysis_results.append({
                    "risk_level": risk_level,
                    "fraud_score": analysis["fraud_score"],
                    "detected_risk": analysis["risk_level"],
                    "confidence": analysis["confidence"]
                })
            
            result = {
                "test": "fraud_detection_analysis",
                "status": "PASSED",
                "message": "Fraud detection analysis completed successfully",
                "details": analysis_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "fraud_detection_analysis",
                "status": "FAILED",
                "message": f"Fraud detection analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_compliance_checking(self) -> Dict[str, Any]:
        """Test compliance checking functionality."""
        logger.info("Testing compliance checking...")
        
        try:
            claim_data = self.create_sample_claim_data("medium")
            
            # Test GLBA compliance
            glba_result = await self.compliance_agent.check_glba_compliance(claim_data)
            assert "compliant" in glba_result
            assert "violations" in glba_result
            assert "recommendations" in glba_result
            
            # Test FCRA compliance
            fcra_result = await self.compliance_agent.check_fcra_compliance(claim_data)
            assert "compliant" in fcra_result
            assert "violations" in fcra_result
            
            # Test NAIC compliance
            naic_result = await self.compliance_agent.check_naic_compliance(claim_data)
            assert "compliant" in naic_result
            assert "violations" in naic_result
            
            result = {
                "test": "compliance_checking",
                "status": "PASSED",
                "message": "Compliance checking completed successfully",
                "details": {
                    "glba_compliant": glba_result["compliant"],
                    "fcra_compliant": fcra_result["compliant"],
                    "naic_compliant": naic_result["compliant"]
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "compliance_checking",
                "status": "FAILED",
                "message": f"Compliance checking failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_audit_trail(self) -> Dict[str, Any]:
        """Test audit trail functionality."""
        logger.info("Testing audit trail...")
        
        try:
            # Create audit entries
            audit_data = {
                "user_id": "test_user",
                "action": "fraud_analysis",
                "resource": "claim_123",
                "details": {"test": "integration"},
                "timestamp": datetime.now().isoformat()
            }
            
            # Log audit entry
            await self.audit_agent.log_audit_entry(audit_data)
            
            # Retrieve audit trail
            trail = await self.audit_agent.get_audit_trail(
                start_date=datetime.now() - timedelta(hours=1),
                end_date=datetime.now() + timedelta(hours=1)
            )
            
            assert isinstance(trail, list)
            
            result = {
                "test": "audit_trail",
                "status": "PASSED",
                "message": "Audit trail functionality working",
                "details": {"entries_found": len(trail)},
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "audit_trail",
                "status": "FAILED",
                "message": f"Audit trail test failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_api_endpoints(self) -> Dict[str, Any]:
        """Test API endpoints (requires server to be running)."""
        logger.info("Testing API endpoints...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test health endpoint
                health_response = await client.get(f"{self.fraud_endpoint}/health")
                assert health_response.status_code == 200
                
                # Test analyze endpoint
                claim_data = self.create_sample_claim_data("medium")
                analyze_response = await client.post(
                    f"{self.fraud_endpoint}/analyze",
                    json=claim_data,
                    timeout=30.0
                )
                
                if analyze_response.status_code == 200:
                    analysis = analyze_response.json()
                    assert "fraud_score" in analysis
                    assert "risk_level" in analysis
                    
                    api_test_passed = True
                    message = "API endpoints working correctly"
                else:
                    api_test_passed = False
                    message = f"API test failed with status {analyze_response.status_code}"
                
            result = {
                "test": "api_endpoints",
                "status": "PASSED" if api_test_passed else "FAILED",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "api_endpoints",
                "status": "FAILED",
                "message": f"API endpoint test failed: {str(e)} (Server may not be running)",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_human_in_the_loop(self) -> Dict[str, Any]:
        """Test human-in-the-loop workflow."""
        logger.info("Testing human-in-the-loop workflow...")
        
        try:
            claim_data = self.create_sample_claim_data("high")
            
            # Analyze claim (should trigger HITL for high risk)
            analysis = await self.fraud_agent.analyze_claim(claim_data)
            
            # Check if HITL was triggered
            hitl_triggered = analysis.get("requires_human_review", False)
            
            if hitl_triggered:
                # Simulate human review
                review_data = {
                    "reviewer_id": "test_reviewer",
                    "decision": "approved",
                    "notes": "Reviewed and approved after investigation",
                    "confidence": 0.9
                }
                
                # Submit human review
                final_decision = await self.fraud_agent.process_human_review(
                    claim_data["claim_id"], 
                    review_data
                )
                
                assert "final_decision" in final_decision
                assert "human_override" in final_decision
                
            result = {
                "test": "human_in_the_loop",
                "status": "PASSED",
                "message": "HITL workflow completed successfully",
                "details": {"hitl_triggered": hitl_triggered},
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "human_in_the_loop",
                "status": "FAILED",
                "message": f"HITL test failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def test_model_monitoring(self) -> Dict[str, Any]:
        """Test model monitoring functionality."""
        logger.info("Testing model monitoring...")
        
        try:
            # Get model metrics
            metrics = await self.fraud_agent.model_manager.get_model_metrics()
            
            assert "accuracy" in metrics
            assert "precision" in metrics
            assert "recall" in metrics
            assert "f1_score" in metrics
            
            # Test drift detection
            drift_status = await self.fraud_agent.model_manager.check_model_drift()
            assert "drift_detected" in drift_status
            assert "drift_score" in drift_status
            
            result = {
                "test": "model_monitoring",
                "status": "PASSED",
                "message": "Model monitoring working correctly",
                "details": {
                    "accuracy": metrics.get("accuracy", 0),
                    "drift_detected": drift_status.get("drift_detected", False)
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result = {
                "test": "model_monitoring",
                "status": "FAILED",
                "message": f"Model monitoring test failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
        self.test_results.append(result)
        return result
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""
        logger.info("Starting comprehensive integration test suite...")
        
        await self.setup()
        
        try:
            # Run all tests
            tests = [
                self.test_agent_initialization(),
                self.test_fraud_detection_analysis(),
                self.test_compliance_checking(),
                self.test_audit_trail(),
                self.test_api_endpoints(),
                self.test_human_in_the_loop(),
                self.test_model_monitoring()
            ]
            
            # Execute tests
            results = await asyncio.gather(*tests, return_exceptions=True)
            
            # Process results
            passed_tests = sum(1 for r in self.test_results if r["status"] == "PASSED")
            total_tests = len(self.test_results)
            
            summary = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
                "test_results": self.test_results,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Integration tests completed: {passed_tests}/{total_tests} passed")
            
            return summary
            
        finally:
            await self.teardown()
    
    def generate_test_report(self, summary: Dict[str, Any]) -> str:
        """Generate a formatted test report."""
        report = f"""
# Enhanced Fraud Detection System - Integration Test Report

**Test Execution Date:** {summary['timestamp']}
**Total Tests:** {summary['total_tests']}
**Passed:** {summary['passed_tests']}
**Failed:** {summary['failed_tests']}
**Success Rate:** {summary['success_rate']:.1f}%

## Test Results Summary

"""
        
        for result in summary['test_results']:
            status_emoji = "✅" if result['status'] == "PASSED" else "❌"
            report += f"{status_emoji} **{result['test'].replace('_', ' ').title()}**\n"
            report += f"   - Status: {result['status']}\n"
            report += f"   - Message: {result['message']}\n"
            if 'details' in result:
                report += f"   - Details: {json.dumps(result['details'], indent=2)}\n"
            report += "\n"
        
        report += f"""
## Overall Assessment

{'🎉 All tests passed! The enhanced fraud detection system is ready for production.' if summary['success_rate'] == 100 else '⚠️ Some tests failed. Please review the failures before deploying to production.'}

## Next Steps

1. Address any failed tests
2. Set up continuous monitoring
3. Configure production environment
4. Train staff on new features
5. Plan gradual rollout

---
*This report was generated automatically by the integration test suite.*
"""
        
        return report


async def main():
    """Main test execution function."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Run integration tests for enhanced fraud detection system")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for API testing")
    parser.add_argument("--output", default="integration_test_report.md", help="Output file for test report")
    args = parser.parse_args()
    
    # Run tests
    test_suite = IntegrationTestSuite(base_url=args.base_url)
    summary = await test_suite.run_all_tests()
    
    # Generate and save report
    report = test_suite.generate_test_report(summary)
    
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"\nIntegration test completed!")
    print(f"Results: {summary['passed_tests']}/{summary['total_tests']} tests passed")
    print(f"Report saved to: {args.output}")
    
    # Print summary to console
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for result in summary['test_results']:
        status = "PASS" if result['status'] == "PASSED" else "FAIL"
        print(f"{status:<5} | {result['test'].replace('_', ' ').title()}")
    
    print("="*60)
    print(f"Overall: {summary['success_rate']:.1f}% success rate")
    
    # Exit with error code if tests failed
    if summary['success_rate'] < 100:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
