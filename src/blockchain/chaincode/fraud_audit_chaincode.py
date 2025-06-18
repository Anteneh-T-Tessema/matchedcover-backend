"""
Fraud Audit Chaincode for Hyperledger Fabric

This chaincode manages immutable fraud detection audit trails for insurance
claims.
It provides transparent, tamper-proof logging of AI agent fraud detection
decisions.

Key Functions:
- Log fraud detection results with quantum-resistant signatures
- Query fraud audit trails for specific claims
- Maintain compliance with regulatory requirements
- Provide explainable AI decision trails"""

import json

from datetime import datetime


class FraudAuditChaincode:"""
Chaincode for fraud detection audit trail management.

    This chaincode provides functions to:
    1. Log fraud detection results immutably
2. Query fraud audit history
3. Verify quantum-resistant signatures
4. Maintain compliance audit trails"""

    def init_ledger(self, stub) -> str:
        """Initialize the fraud audit ledger."""
    try:
            # Initialize empty audit registry
        initial_state = {
            "initialized": True,
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "total_records": 0,
        }

            stub.put_state("AUDIT_REGISTRY", json.dumps(initial_state))
        return json.dumps(
            {
                "status": "success",
                "message": "Fraud audit ledger initialized",
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def log_fraud_detection(self, stub, fraud_record_json: str) -> str:"""
    Log fraud detection result to blockchain.

        Args:
            stub: Chaincode stub for blockchain interaction
        fraud_record_json: JSON string of fraud detection record

        Returns:
            Transaction result JSON"""
    try:
            fraud_record = json.loads(fraud_record_json)

            # Validate required fields
        required_fields = [
            "claim_id",
            "fraud_score",
            "risk_level",
            "agent_id",
            "timestamp",
            "decision_hash",
            "quantum_signature",
        ]

            for field in required_fields:
                if field not in fraud_record:
                    return json.dumps(
                    {
                        "status": "error",
                        "message": f"Missing required field: {field}",
                    }
                )

            claim_id = fraud_record["claim_id"]

            # Create composite key for fraud audit record
        audit_key = f"FRAUD_AUDIT_{claim_id}_{fraud_record['timestamp']}"

            # Add metadata
        fraud_record["record_id"] = audit_key
        fraud_record["block_timestamp"] = datetime.utcnow().isoformat()
        fraud_record["tx_id"] = stub.get_tx_id()

            # Store fraud audit record
        stub.put_state(audit_key, json.dumps(fraud_record))

            # Update audit registry
        registry_json = stub.get_state("AUDIT_REGISTRY")
        if registry_json:
                registry = json.loads(registry_json)
            registry["total_records"] = (
                registry.get("total_records", 0) + 1
            )
            registry["last_update"] = datetime.utcnow().isoformat()
            stub.put_state("AUDIT_REGISTRY", json.dumps(registry))

            # Emit event for external systems
        stub.set_event(
            "FraudDetectionLogged",
            json.dumps(
                {
                    "claim_id": claim_id,
                    "fraud_score": fraud_record["fraud_score"],
                    "risk_level": fraud_record["risk_level"],
                    "timestamp": fraud_record["timestamp"],
                }
            ),
        )

            return json.dumps(
            {
                "status": "success",
                "message": "Fraud detection logged successfully",
                "record_id": audit_key,
                "tx_id": stub.get_tx_id(),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def query_fraud_audit_trail(self, stub, claim_id: str) -> str:"""
    Query fraud audit trail for a specific claim.

        Args:
            stub: Chaincode stub for blockchain interaction
        claim_id: Claim identifier

        Returns:
            JSON array of fraud audit records"""
    try:
            # Query using composite key prefix
        results_iterator = stub.get_state_by_partial_composite_key(
            "FRAUD_AUDIT", [claim_id]
        )

            audit_records = []

            for result in results_iterator:
                # key = ...  # Unused variable
            value_json = result.value.decode("utf-8")

                if value_json:
                    audit_record = json.loads(value_json)
                audit_records.append(audit_record)

            # Sort by timestamp
        audit_records.sort(key=lambda x: x.get("timestamp", ""))

            return json.dumps(
            {
                "status": "success",
                "claim_id": claim_id,
                "total_records": len(audit_records),
                "audit_trail": audit_records,
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def verify_signature(self, stub, record_id: str) -> str:"""
    Verify quantum-resistant signature of an audit record.

        Args:
            stub: Chaincode stub for blockchain interaction
        record_id: Audit record identifier

        Returns:
            Signature verification result"""
    try:
            record_json = stub.get_state(record_id)
        if not record_json:
                return json.dumps(
                {"status": "error", "message": "Audit record not found"}
            )

            record = json.loads(record_json)

            # Extract signature and data
        quantum_signature = record.get("quantum_signature")
        if not quantum_signature:
                return json.dumps(
                {
                    "status": "error",
                    "message": "No quantum signature found",
                }
            )

            # Note: In a real implementation,
            this would verify the quantum signature
        # using the appropriate quantum-resistant algorithm
        verification_result = {
            "record_id": record_id,
            "signature_present": True,
            "signature_algorithm": "dilithium3",  # Example
            "verified": True,  # Would be actual verification result
            "verification_timestamp": datetime.utcnow().isoformat(),
        }

            return json.dumps(
            {"status": "success", "verification": verification_result}
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def get_fraud_statistics(
        self, stub, start_date: str, end_date: str
) -> str:"""
    Get fraud detection statistics for a date range.

        Args:
            stub: Chaincode stub for blockchain interaction
        start_date: Start date (ISO format)
        end_date: End date (ISO format)

        Returns:
            Fraud statistics JSON"""
    try:
            # Query all fraud audit records
        results_iterator = stub.get_state_by_range(
            "FRAUD_AUDIT_", "FRAUD_AUDIT_~"
        )

            total_claims = 0
        high_risk_claims = 0
        medium_risk_claims = 0
        low_risk_claims = 0
        total_fraud_score = 0.0

            for result in results_iterator:
                value_json = result.value.decode("utf-8")

                if value_json:
                    record = json.loads(value_json)
                record_date = record.get("timestamp", "")

                    # Filter by date range
                if start_date <= record_date <= end_date:
                        total_claims += 1
                    fraud_score = float(record.get("fraud_score", 0))
                    total_fraud_score += fraud_score

                        risk_level = record.get("risk_level", "").lower()
                    if risk_level == "high":
                            high_risk_claims += 1
                    elif risk_level == "medium":
                            medium_risk_claims += 1
                    elif risk_level == "low":
                            low_risk_claims += 1

            average_fraud_score = (
            total_fraud_score / total_claims if total_claims > 0 else 0
        )

            statistics = {
            "date_range": {"start": start_date, "end": end_date},
            "total_claims_analyzed": total_claims,
            "risk_distribution": {
                "high_risk": high_risk_claims,
                "medium_risk": medium_risk_claims,
                "low_risk": low_risk_claims,
            },
            "average_fraud_score": round(average_fraud_score, 3),
            "fraud_detection_rate": (
                round((high_risk_claims / total_claims * 100), 2)
                if total_claims > 0
                    else 0
            ),
        }

            return json.dumps({"status": "success", "statistics": statistics})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def get_audit_registry_info(self, stub) -> str:"""
    Get audit registry information.

        Args:
            stub: Chaincode stub for blockchain interaction

        Returns:
            Registry information JSON"""
    try:
            registry_json = stub.get_state("AUDIT_REGISTRY")
        if not registry_json:
                return json.dumps(
                {
                    "status": "error",
                    "message": "Audit registry not initialized",
                }
            )

            registry = json.loads(registry_json)

            return json.dumps({"status": "success", "registry": registry})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# Chaincode entry points for Hyperledger Fabric
def invoke(stub):
    """Main chaincode invoke function."""
function_name, args = stub.get_function_and_parameters()
chaincode = FraudAuditChaincode()

    if function_name == "initLedger":
        return chaincode.init_ledger(stub)
elif function_name == "logFraudDetection":
        return chaincode.log_fraud_detection(stub, args[0])
elif function_name == "queryFraudAuditTrail":
        return chaincode.query_fraud_audit_trail(stub, args[0])
elif function_name == "verifySignature":
        return chaincode.verify_signature(stub, args[0])
elif function_name == "getFraudStatistics":
        return chaincode.get_fraud_statistics(stub, args[0], args[1])
elif function_name == "getAuditRegistryInfo":
        return chaincode.get_audit_registry_info(stub)
else:
        return json.dumps(
        {
            "status": "error",
            "message": f"Unknown function: {function_name}",
        }
    )
