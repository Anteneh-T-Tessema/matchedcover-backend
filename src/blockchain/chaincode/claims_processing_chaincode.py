"""
Claims Processing Chaincode for Hyperledger Fabric

This chaincode manages automated claims processing and smart contract payouts.
It provides transparent, auditable claim workflows with AI agent integration.

Key Functions:
- Submit and track insurance claims
- Execute automated payouts based on conditions
- Multi-party approval workflows
- Integration with external oracles for parametric insurance"""

import json
from datetime import datetime


class ClaimsProcessingChaincode:"""
Chaincode for claims processing and automated payouts.

    This chaincode provides functions to:
    1. Submit insurance claims for processing
2. Execute automated payouts based on conditions
3. Track claim status and approvals
4. Implement multi-party approval workflows"""

    def init_ledger(self, stub) -> str:
        """Initialize the claims processing ledger."""
    try:
            initial_state = {
            "initialized": True,
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "total_claims": 0,
            "total_payouts": 0.0,
        }

            stub.put_state("CLAIMS_REGISTRY", json.dumps(initial_state))
        return json.dumps(
            {"status": "success", "message": "Claims ledger initialized"}
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def submit_claim(self, stub, claim_record_json: str) -> str:"""
    Submit an insurance claim to the blockchain.

        Args:
            stub: Chaincode stub for blockchain interaction
        claim_record_json: JSON string of claim record

        Returns:
            Transaction result JSON"""
    try:
            claim_record = json.loads(claim_record_json)

            # Validate required fields
        required_fields = [
            "claim_id",
            "policy_id",
            "claim_amount",
            "ai_assessment",
        ]

            for field in required_fields:
                if field not in claim_record:
                    return json.dumps(
                    {
                        "status": "error",
                        "message": f"Missing required field: {field}",
                    }
                )

            claim_id = claim_record["claim_id"]

            # Check if claim already exists
        existing_claim = stub.get_state(f"CLAIM_{claim_id}")
        if existing_claim:
                return json.dumps(
                {"status": "error", "message": "Claim already exists"}
            )

            # Set initial status and metadata
        claim_record["status"] = "submitted"
        claim_record["submission_timestamp"] = (
            datetime.utcnow().isoformat()
        )
        claim_record["tx_id"] = stub.get_tx_id()
        claim_record["approval_signatures"] = []
        claim_record["status_history"] = [
            {
                "status": "submitted",
                "timestamp": datetime.utcnow().isoformat(),
                "tx_id": stub.get_tx_id(),
            }
        ]

            # Store claim
        stub.put_state(f"CLAIM_{claim_id}", json.dumps(claim_record))

            # Update registry
        registry_json = stub.get_state("CLAIMS_REGISTRY")
        if registry_json:
                registry = json.loads(registry_json)
            registry["total_claims"] = registry.get("total_claims", 0) + 1
            registry["last_update"] = datetime.utcnow().isoformat()
            stub.put_state("CLAIMS_REGISTRY", json.dumps(registry))

            # Emit event
        stub.set_event(
            "ClaimSubmitted",
            json.dumps(
                {
                    "claim_id": claim_id,
                    "policy_id": claim_record["policy_id"],
                    "claim_amount": claim_record["claim_amount"],
                    "timestamp": claim_record["submission_timestamp"],
                }
            ),
        )

            return json.dumps(
            {
                "status": "success",
                "message": "Claim submitted successfully",
                "claim_id": claim_id,
                "tx_id": stub.get_tx_id(),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def approve_payout(self, stub, payout_data_json: str) -> str:"""
    Approve claim payout through smart contract.

        Args:
            stub: Chaincode stub for blockchain interaction
        payout_data_json: JSON string of payout approval data

        Returns:
            Transaction result JSON"""
    try:
            payout_data = json.loads(payout_data_json)

            claim_id = payout_data.get("claim_id")
        if not claim_id:
                return json.dumps(
                {"status": "error", "message": "Missing claim_id"}
            )

            # Get existing claim
        claim_json = stub.get_state(f"CLAIM_{claim_id}")
        if not claim_json:
                return json.dumps(
                {"status": "error", "message": "Claim not found"}
            )

            claim = json.loads(claim_json)

            # Validate payout conditions
        if claim.get("status") not in ["submitted", "under_review"]:
                return json.dumps(
                {
                    "status": "error",
                    "message": f"Invalid claim status for payout: {claim"
                        .get('status')}","
                }
            )

            # Update claim with payout information
        claim["status"] = "approved"
        claim["payout_amount"] = payout_data.get("payout_amount")
        claim["payout_timestamp"] = datetime.utcnow().isoformat()
        claim["approver_signatures"] = payout_data.get(
            "approver_signatures", []
        )
        claim["payout_tx_id"] = stub.get_tx_id()

            # Add to status history
        claim["status_history"].append(
            {
                "status": "approved",
                "timestamp": datetime.utcnow().isoformat(),
                "tx_id": stub.get_tx_id(),
                "payout_amount": payout_data.get("payout_amount"),
            }
        )

            # Store updated claim
        stub.put_state(f"CLAIM_{claim_id}", json.dumps(claim))

            # Update registry with payout total
        registry_json = stub.get_state("CLAIMS_REGISTRY")
        if registry_json:
                registry = json.loads(registry_json)
            registry["total_payouts"] = registry.get(
                "total_payouts", 0
            ) + float(payout_data.get("payout_amount", 0))
            registry["last_update"] = datetime.utcnow().isoformat()
            stub.put_state("CLAIMS_REGISTRY", json.dumps(registry))

            # Emit payout event
        stub.set_event(
            "PayoutApproved",
            json.dumps(
                {
                    "claim_id": claim_id,
                    "payout_amount": payout_data.get("payout_amount"),
                    "timestamp": claim["payout_timestamp"],
                }
            ),
        )

            return json.dumps(
            {
                "status": "success",
                "message": "Payout approved successfully",
                "claim_id": claim_id,
                "payout_amount": payout_data.get("payout_amount"),
                "tx_id": stub.get_tx_id(),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def update_claim_status(
        self, stub, claim_id: str, new_status: str, notes: str = ""
) -> str:"""
    Update claim status with audit trail.

        Args:
            stub: Chaincode stub for blockchain interaction
        claim_id: Claim identifier
        new_status: New status value
        notes: Optional notes for status update

        Returns:
            Transaction result JSON"""
    try:
            # Get existing claim
        claim_json = stub.get_state(f"CLAIM_{claim_id}")
        if not claim_json:
                return json.dumps(
                {"status": "error", "message": "Claim not found"}
            )

            claim = json.loads(claim_json)

            # Valid status transitions
        valid_statuses = [
            "submitted",
            "under_review",
            "approved",
            "rejected",
            "paid",
            "cancelled",
            "investigating",
        ]

            if new_status not in valid_statuses:
                return json.dumps(
                {
                    "status": "error",
                    "message": f"Invalid status: {new_status}",
                }
            )

            # Update claim status
        old_status = claim.get("status")
        claim["status"] = new_status
        claim["last_updated"] = datetime.utcnow().isoformat()

            # Add to status history
        status_update = {
            "status": new_status,
            "previous_status": old_status,
            "timestamp": datetime.utcnow().isoformat(),
            "tx_id": stub.get_tx_id(),
            "notes": notes,
        }

            if "status_history" not in claim:
                claim["status_history"] = []

            claim["status_history"].append(status_update)

            # Store updated claim
        stub.put_state(f"CLAIM_{claim_id}", json.dumps(claim))

            # Emit status update event
        stub.set_event(
            "ClaimStatusUpdated",
            json.dumps(
                {
                    "claim_id": claim_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "timestamp": status_update["timestamp"],
                }
            ),
        )

            return json.dumps(
            {
                "status": "success",
                "message": "Claim status updated successfully",
                "claim_id": claim_id,
                "new_status": new_status,
                "tx_id": stub.get_tx_id(),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def query_claim_history(self, stub, claim_id: str) -> str:"""
    Query complete claim processing history.

        Args:
            stub: Chaincode stub for blockchain interaction
        claim_id: Claim identifier

        Returns:
            Claim history JSON"""
    try:
            claim_json = stub.get_state(f"CLAIM_{claim_id}")
        if not claim_json:
                return json.dumps(
                {"status": "error", "message": "Claim not found"}
            )

            claim = json.loads(claim_json)

            return json.dumps(
            {
                "status": "success",
                "claim_id": claim_id,
                "claim_data": claim,
                "status_history": claim.get("status_history", []),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def execute_parametric_payout(
        self, stub, parametric_data_json: str
) -> str:"""
    Execute automated parametric insurance payout based on oracle data.

        Args:
            stub: Chaincode stub for blockchain interaction
        parametric_data_json: JSON string of parametric trigger data

        Returns:
            Transaction result JSON"""
    try:
            parametric_data = json.loads(parametric_data_json)

            required_fields = [
            "policy_id",
            "trigger_event",
            "oracle_data",
            "payout_amount",
        ]
        for field in required_fields:
                if field not in parametric_data:
                    return json.dumps(
                    {
                        "status": "error",
                        "message": f"Missing required field: {field}",
                    }
                )

            # Create automatic claim for parametric payout
        claim_id = f"PARAMETRIC_{parametric_data['policy_id']}_{int("
            datetime.utcnow().timestamp())}""

            parametric_claim = {
            "claim_id": claim_id,
            "policy_id": parametric_data["policy_id"],
            "claim_type": "parametric",
            "trigger_event": parametric_data["trigger_event"],
            "oracle_data": parametric_data["oracle_data"],
            "claim_amount": parametric_data["payout_amount"],
            "status": "auto_approved",
            "submission_timestamp": datetime.utcnow().isoformat(),
            "payout_timestamp": datetime.utcnow().isoformat(),
            "tx_id": stub.get_tx_id(),
            "automated": True,
        }

            # Store parametric claim
        stub.put_state(f"CLAIM_{claim_id}", json.dumps(parametric_claim))

            # Update registry
        registry_json = stub.get_state("CLAIMS_REGISTRY")
        if registry_json:
                registry = json.loads(registry_json)
            registry["total_claims"] = registry.get("total_claims", 0) + 1
            registry["total_payouts"] = registry.get(
                "total_payouts", 0
            ) + float(parametric_data["payout_amount"])
            registry["last_update"] = datetime.utcnow().isoformat()
            stub.put_state("CLAIMS_REGISTRY", json.dumps(registry))

            # Emit parametric payout event
        stub.set_event(
            "ParametricPayoutExecuted",
            json.dumps(
                {
                    "claim_id": claim_id,
                    "policy_id": parametric_data["policy_id"],
                    "trigger_event": parametric_data["trigger_event"],
                    "payout_amount": parametric_data["payout_amount"],
                    "timestamp": parametric_claim["payout_timestamp"],
                }
            ),
        )

            return json.dumps(
            {
                "status": "success",
                "message": "Parametric payout executed successfully",
                "claim_id": claim_id,
                "payout_amount": parametric_data["payout_amount"],
                "tx_id": stub.get_tx_id(),
            }
        )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def get_claims_statistics(self, stub) -> str:"""
    Get claims processing statistics.

        Args:
            stub: Chaincode stub for blockchain interaction

        Returns:
            Claims statistics JSON"""
    try:
            registry_json = stub.get_state("CLAIMS_REGISTRY")
        if not registry_json:
                return json.dumps(
                {
                    "status": "error",
                    "message": "Claims registry not initialized",
                }
            )

            registry = json.loads(registry_json)

            # Query all claims for detailed statistics
        results_iterator = stub.get_state_by_range("CLAIM_", "CLAIM_~")

            status_counts = {}
        claim_types = {}
        total_claim_amount = 0.0

            for result in results_iterator:
                value_json = result.value.decode("utf-8")

                if value_json:
                    claim = json.loads(value_json)

                    # Count by status
                status = claim.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1

                    # Count by type
                claim_type = claim.get("claim_type", "standard")
                claim_types[claim_type] = (
                    claim_types.get(claim_type, 0) + 1
                )

                    # Sum claim amounts
                claim_amount = float(claim.get("claim_amount", 0))
                total_claim_amount += claim_amount

            statistics = {
            "registry_info": registry,
            "status_distribution": status_counts,
            "claim_type_distribution": claim_types,
            "total_claim_amount": total_claim_amount,
            "average_claim_amount": total_claim_amount
            / registry.get("total_claims", 1),
            "payout_ratio": (
                registry.get("total_payouts", 0) / total_claim_amount
                if total_claim_amount > 0
                    else 0
            ),
        }

            return json.dumps({"status": "success", "statistics": statistics})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# Chaincode entry points for Hyperledger Fabric
def invoke(stub):
    """Main chaincode invoke function."""
function_name, args = stub.get_function_and_parameters()
chaincode = ClaimsProcessingChaincode()

    if function_name == "initLedger":
        return chaincode.init_ledger(stub)
elif function_name == "submitClaim":
        return chaincode.submit_claim(stub, args[0])
elif function_name == "approvePayout":
        return chaincode.approve_payout(stub, args[0])
elif function_name == "updateClaimStatus":
        return chaincode.update_claim_status(
        stub, args[0], args[1], args[2] if len(args) > 2 else ""
    )
elif function_name == "queryClaimHistory":
        return chaincode.query_claim_history(stub, args[0])
elif function_name == "executeParametricPayout":
        return chaincode.execute_parametric_payout(stub, args[0])
elif function_name == "getClaimsStatistics":
        return chaincode.get_claims_statistics(stub)
else:
        return json.dumps(
        {
            "status": "error",
            "message": f"Unknown function: {function_name}",
        }
    )
