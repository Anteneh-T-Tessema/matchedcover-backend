#!/usr/bin/env python3
"""
Simple Integration Test for Enhanced Fraud Detection System

This script performs basic integration testing to ensure the enhanced fraud
detection system components work together correctly.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any
import uuid

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_test_claim() -> Dict[str, Any]:
    """Create a sample claim for testing."""
    return {
        "claim_id": str(uuid.uuid4()),
        "policy_number": "POL12345",
        "claim_amount": 15000.0,
        "incident_date": "2024-01-10T10:00:00",
        "reported_date": "2024-01-12T09:00:00",
        "claim_type": "auto",
        "description": "Vehicle collision on highway",
        "location": "Los Angeles, CA",
        "claimant": {
            "name": "John Smith",
            "phone": "555-0123",
            "email": "john.smith@email.com",
            "address": "123 Main St, Los Angeles, CA 90210"
        },
        "vehicle": {
            "make": "Toyota",
            "model": "Camry",
            "year": 2020,
            "vin": "1HGBH41JXMN109186"
        }
    }


async def test_agent_imports():
    """Test that all agent modules can be imported."""
    logger.info("Testing agent imports...")
    
    try:
        from src.agents.enhanced_fraud_detection_agent import EnhancedFraudDetectionAgent
        from src.agents.compliance_agent import ComplianceAgent
        from src.agents.audit_agent import AuditAgent
        
        logger.info("✅ All agent modules imported successfully")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False


async def test_api_import():
    """Test that the API module can be imported."""
    logger.info("Testing API import...")
    
    try:
        from src.api.enhanced_fraud_detection import router
        logger.info("✅ API module imported successfully")
        return True
        
    except ImportError as e:
        logger.error(f"❌ API import error: {e}")
        return False


async def test_dependencies():
    """Test that all required dependencies are available."""
    logger.info("Testing dependencies...")
    
    required_packages = [
        "fastapi",
        "pydantic", 
        "uvicorn",
        "httpx",
        "pandas",
        "numpy",
        "sklearn"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} available")
        except ImportError:
            logger.error(f"❌ {package} not available")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        return False
    
    logger.info("✅ All required dependencies available")
    return True


async def test_enhanced_dependencies():
    """Test enhanced ML and compliance dependencies."""
    logger.info("Testing enhanced dependencies...")
    
    enhanced_packages = [
        ("shap", "SHAP for explainable AI"),
        ("lime", "LIME for model explanations"),
        ("mlflow", "MLflow for model tracking"),
        ("evidently", "Evidently for data drift detection"),
        ("cryptography", "Cryptography for security"),
    ]
    
    available_count = 0
    
    for package, description in enhanced_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} available - {description}")
            available_count += 1
        except ImportError:
            logger.warning(f"⚠️ {package} not available - {description}")
    
    logger.info(f"Enhanced packages available: {available_count}/{len(enhanced_packages)}")
    return available_count > 0


async def test_file_structure():
    """Test that all required files exist."""
    logger.info("Testing file structure...")
    
    required_files = [
        "src/agents/enhanced_fraud_detection_agent.py",
        "src/agents/compliance_agent.py", 
        "src/agents/audit_agent.py",
        "src/api/enhanced_fraud_detection.py",
        "requirements.txt",
        "docs/ENTERPRISE_FRAUD_DETECTION.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            logger.info(f"✅ {file_path} exists")
        else:
            logger.error(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"Missing files: {missing_files}")
        return False
    
    logger.info("✅ All required files present")
    return True


async def test_basic_functionality():
    """Test basic functionality without full initialization."""
    logger.info("Testing basic functionality...")
    
    try:
        # Test claim data creation
        claim = create_test_claim()
        assert "claim_id" in claim
        assert "policy_number" in claim
        assert "claim_amount" in claim
        logger.info("✅ Test claim data creation works")
        
        # Test JSON serialization
        json_str = json.dumps(claim)
        parsed_claim = json.loads(json_str)
        assert parsed_claim["claim_id"] == claim["claim_id"]
        logger.info("✅ JSON serialization/deserialization works")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Basic functionality test failed: {e}")
        return False


async def test_configuration():
    """Test configuration and environment setup."""
    logger.info("Testing configuration...")
    
    try:
        # Check if .env.example exists
        if os.path.exists(".env.example"):
            logger.info("✅ .env.example file found")
        else:
            logger.warning("⚠️ .env.example file not found")
        
        # Check if environment variables can be set
        os.environ["TEST_VAR"] = "test_value"
        if os.environ.get("TEST_VAR") == "test_value":
            logger.info("✅ Environment variables work")
            del os.environ["TEST_VAR"]
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {e}")
        return False


async def run_integration_tests():
    """Run all integration tests."""
    logger.info("="*60)
    logger.info("ENHANCED FRAUD DETECTION SYSTEM - INTEGRATION TESTS")
    logger.info("="*60)
    
    tests = [
        ("Dependencies", test_dependencies()),
        ("Enhanced Dependencies", test_enhanced_dependencies()),
        ("File Structure", test_file_structure()),
        ("Agent Imports", test_agent_imports()),
        ("API Import", test_api_import()),
        ("Basic Functionality", test_basic_functionality()),
        ("Configuration", test_configuration())
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        logger.info(f"\nRunning: {test_name}")
        logger.info("-" * 40)
        
        try:
            result = await test_coro
            results.append((test_name, result))
            
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
                
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{status:<5} | {test_name}")
    
    logger.info("-" * 60)
    logger.info(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! System ready for next phase.")
    else:
        logger.warning("⚠️ Some tests failed. Review issues before proceeding.")
    
    return passed, total


async def main():
    """Main function."""
    try:
        passed, total = await run_integration_tests()
        
        # Write simple report
        with open("integration_test_results.txt", "w") as f:
            f.write(f"Enhanced Fraud Detection System - Integration Test Results\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write(f"Results: {passed}/{total} tests passed\n")
            f.write(f"Success Rate: {passed/total*100:.1f}%\n")
        
        print(f"\nResults written to: integration_test_results.txt")
        
        # Exit with appropriate code
        sys.exit(0 if passed == total else 1)
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
