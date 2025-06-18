""""
Hyperledger Fabric Integration for MatchedCover Insurance Platform

This module provides a permissioned blockchain layer for:
- Immutable fraud detection audit trails
- Smart contracts for automated claims processing
- Agent decision governance and explainability
- Decentralized identity verification
- Multi-party risk sharing for reinsurance

Architecture:
- Private/Consortium network with insurance partners
- Chaincode (smart contracts) for business logic
- Certificate Authority for identity management
- Orderer service for transaction ordering
""""

import json
import logging
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import base64

# Hyperledger Fabric SDK
try:
    from hfc.fabric import Client
from hfc.fabric_network import Gateway  # Used in __init__

    # from hfc.fabric_network import Network  # Not currently used
# from hfc.fabric_ca.caservice import ca_service  # Not currently used
# from hfc.protos.common import common_pb2  # Not currently used
# from hfc.protos.peer import chaincode_pb2  # Not currently used
FABRIC_AVAILABLE = True
except ImportError:
    FABRIC_AVAILABLE = False
logging.warning(
    "Hyperledger Fabric SDK not available. Using mock implementation."
)

from src.core.config import settings
from src.quantum.crypto import QuantumResistantSigner

logger = logging.getLogger(__name__)


class ChannelType(Enum):
    """Blockchain channel types for different use cases."""

    FRAUD_AUDIT = "fraud-audit-channel"
CLAIMS_PROCESSING = "claims-channel"
IDENTITY_VERIFICATION = "identity-channel"
REINSURANCE = "reinsurance-channel"
AGENT_GOVERNANCE = "governance-channel"


class TransactionType(Enum):
    """Types of blockchain transactions."""

    FRAUD_DETECTION_LOG = "fraud_detection_log"
CLAIM_SUBMISSION = "claim_submission"
CLAIM_APPROVAL = "claim_approval"
CLAIM_PAYOUT = "claim_payout"
IDENTITY_ATTESTATION = "identity_attestation"
AGENT_DECISION = "agent_decision"
RISK_ASSESSMENT = "risk_assessment"
REINSURANCE_CONTRACT = "reinsurance_contract"


@dataclass
class FraudAuditRecord:
    """Immutable fraud detection audit record."""

    claim_id: str
fraud_score: float
risk_level: str
agent_id: str
timestamp: str
decision_hash: str
quantum_signature: str
evidence_hash: str
compliance_flags: List[str]
human_review_required: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClaimRecord:
    """Blockchain claim processing record."""

    claim_id: str
policy_id: str
claim_amount: float
status: str
ai_assessment: Dict[str, Any]
approval_conditions: List[str]
payout_address: Optional[str]
timestamp: str
approver_signatures: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IdentityAttestation:
    """Decentralized identity attestation record."""

    user_id: str
verification_type: str
attestation_hash: str
verifier_agent_id: str
timestamp: str
validity_period: int
revocation_status: bool
zero_knowledge_proof: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentDecisionRecord:
    """Agent governance and explainability record."""

    agent_id: str
decision_type: str
input_hash: str
output_hash: str
confidence_score: float
explanation_hash: str
timestamp: str
model_version: str
compliance_check: Dict[str, Any]
quantum_signature: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MockFabricClient:
    """Mock Fabric client for when SDK is not available."""

    def __init__(self):
        self.connected = False
    self.channels = {}
    self.ledger = {}

    async def connect(self, connection_profile: Dict[str, Any]) -> bool:
        """Mock connection."""
    self.connected = True
    logger.info("Mock Fabric client connected")
    return True

    async def invoke_chaincode(
        self, channel: str, chaincode: str, function: str, args: List[str]
) -> Dict[str, Any]:
        """Mock chaincode invocation."""
    tx_id = str(uuid.uuid4())
    result = {
        "tx_id": tx_id,
        "status": "success",
        "payload": {"message": f"Mock execution of {function}"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

        # Store in mock ledger
    if channel not in self.ledger:
            self.ledger[channel] = []
    self.ledger[channel].append(result)

        return result

    async def query_chaincode(
        self, channel: str, chaincode: str, function: str, args: List[str]
) -> Dict[str, Any]:
        """Mock chaincode query."""
    return {
        "status": "success",
        "payload": {"message": f"Mock query of {function}"},
        "data": [],
    }


class HyperledgerFabricManager:
    """"
Hyperledger Fabric integration manager for insurance blockchain operations.

    Provides permissioned blockchain functionality for:
    1. Fraud detection audit trails
2. Claims processing automation
3. Identity verification and attestation
4. Agent decision governance
5. Reinsurance risk sharing
""""

    def __init__(self):
        """Initialize Hyperledger Fabric manager."""
    self.client = None
    self.gateway = None
    self.networks = {}
    self.quantum_signer = QuantumResistantSigner()
    self.connection_profile = self._get_connection_profile()
    self.org_name = settings.FABRIC_ORG_NAME
    self.user_name = settings.FABRIC_USER_NAME

    def _get_connection_profile(self) -> Dict[str, Any]:
        """Get Hyperledger Fabric connection profile."""
    return {
        "name": "insurance-network",
        "version": "1.0.0",
        "client": {
            "organization": settings.FABRIC_ORG_NAME,
            "connection": {
                "timeout": {"peer": {"endorser": "300"}, "orderer": "300"}
            },
        },
        "organizations": {
            settings.FABRIC_ORG_NAME: {
                "mspid": f"{settings.FABRIC_ORG_NAME}MSP",
                "peers": [f"peer0.{settings.FABRIC_ORG_NAME}.example.com"],
                "certificateAuthorities": [
                    f"ca.{settings.FABRIC_ORG_NAME}.example.com"
                ],
            }
        },
        "orderers": {
            "orderer.example.com": {
                "url": settings.FABRIC_ORDERER_URL,
                "tlsCACerts": {"pem": settings.FABRIC_TLS_CERT},
            }
        },
        "peers": {
            f"peer0.{settings.FABRIC_ORG_NAME}.example.com": {
                "url": settings.FABRIC_PEER_URL,
                "tlsCACerts": {"pem": settings.FABRIC_TLS_CERT},
            }
        },
        "certificateAuthorities": {
            f"ca.{settings.FABRIC_ORG_NAME}.example.com": {
                "url": settings.FABRIC_CA_URL,
                "tlsCACerts": {"pem": settings.FABRIC_TLS_CERT},
            }
        },
    }

    async def initialize(self) -> bool:
        """Initialize Hyperledger Fabric connection."""
    try:
            if FABRIC_AVAILABLE:
                self.client = Client(net_profile=self.connection_profile)

                # Create gateway for network interaction
            self.gateway = Gateway()
            await self.gateway.connect(
                self.connection_profile,
                {
                    "wallet": self._get_wallet(),
                    "identity": self.user_name,
                    "discovery": {"enabled": True},
                },
            )

                # Initialize networks for different channels
            await self._initialize_networks()

                logger.info(
                "Hyperledger Fabric client initialized successfully"
            )
            return True
        else:
                # Use mock client
            self.client = MockFabricClient()
            await self.client.connect(self.connection_profile)
            logger.info("Using mock Fabric client for development")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Hyperledger Fabric: {e}")
        return False

    async def _initialize_networks(self):
        """Initialize networks for different channels."""
    for channel_type in ChannelType:
            try:
                network = await self.gateway.get_network(channel_type.value)
            self.networks[channel_type.value] = network
            logger.info(f"Connected to channel: {channel_type.value}")
        except Exception as e:
                logger.warning(
                f"Failed to connect to channel {channel_type.value}: {e}"
            )

    def _get_wallet(self) -> Dict[str, Any]:
        """Get wallet for user identity."""
    # In production, this would load from secure storage
    return {
        self.user_name: {
            "type": "X.509",
            "mspId": f"{self.org_name}MSP",
            "credentials": {
                "certificate": settings.FABRIC_USER_CERT,
                "privateKey": settings.FABRIC_USER_KEY,
            },
        }
    }

    async def log_fraud_detection(self, fraud_record: FraudAuditRecord) -> str:
        """"
    Log fraud detection results to blockchain for immutable audit trail.

        Args:
            fraud_record: Fraud detection audit record

        Returns:
            Transaction ID
    """"
    try:
            # Create quantum-resistant signature
        record_data = json.dumps(fraud_record.to_dict(), sort_keys=True)
        signature = await self.quantum_signer.sign(record_data)
        fraud_record.quantum_signature = base64.b64encode(
            signature.encode()
        ).decode()

            # Create decision hash
        fraud_record.decision_hash = hashlib.sha256(
            record_data.encode()
        ).hexdigest()

            if (
                FABRIC_AVAILABLE
            and ChannelType.FRAUD_AUDIT.value in self.networks
        ):
                network = self.networks[ChannelType.FRAUD_AUDIT.value]
            contract = network.get_contract("fraud-audit-chaincode")

                result = await contract.submit_transaction(
                "logFraudDetection", json.dumps(fraud_record.to_dict())
            )

                logger.info(f"Fraud detection logged to blockchain: {result}")
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.FRAUD_AUDIT.value,
                "fraud-audit-chaincode",
                "logFraudDetection",
                [json.dumps(fraud_record.to_dict())],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(f"Failed to log fraud detection to blockchain: {e}")
        raise

    async def submit_claim_to_blockchain(
        self, claim_record: ClaimRecord
) -> str:
        """"
    Submit claim to blockchain for transparent processing.

        Args:
            claim_record: Claim processing record

        Returns:
            Transaction ID
    """"
    try:
            if (
                FABRIC_AVAILABLE
            and ChannelType.CLAIMS_PROCESSING.value in self.networks
        ):
                network = self.networks[ChannelType.CLAIMS_PROCESSING.value]
            contract = network.get_contract("claims-chaincode")

                result = await contract.submit_transaction(
                "submitClaim", json.dumps(claim_record.to_dict())
            )

                logger.info(f"Claim submitted to blockchain: {result}")
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.CLAIMS_PROCESSING.value,
                "claims-chaincode",
                "submitClaim",
                [json.dumps(claim_record.to_dict())],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(f"Failed to submit claim to blockchain: {e}")
        raise

    async def approve_claim_payout(
        self,
    claim_id: str,
    payout_amount: float,
    approver_signatures: List[str],
) -> str:
        """"
    Approve claim payout through smart contract.

        Args:
            claim_id: Claim identifier
        payout_amount: Amount to pay out
        approver_signatures: Digital signatures from approvers

        Returns:
            Transaction ID
    """"
    try:
            payout_data = {
            "claim_id": claim_id,
            "payout_amount": payout_amount,
            "approver_signatures": approver_signatures,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "approved",
        }

            if (
                FABRIC_AVAILABLE
            and ChannelType.CLAIMS_PROCESSING.value in self.networks
        ):
                network = self.networks[ChannelType.CLAIMS_PROCESSING.value]
            contract = network.get_contract("claims-chaincode")

                result = await contract.submit_transaction(
                "approvePayout", json.dumps(payout_data)
            )

                logger.info(f"Claim payout approved on blockchain: {result}")
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.CLAIMS_PROCESSING.value,
                "claims-chaincode",
                "approvePayout",
                [json.dumps(payout_data)],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(f"Failed to approve claim payout on blockchain: {e}")
        raise

    async def create_identity_attestation(
        self, attestation: IdentityAttestation
) -> str:
        """"
    Create decentralized identity attestation on blockchain.

        Args:
            attestation: Identity attestation record

        Returns:
            Transaction ID
    """"
    try:
            if (
                FABRIC_AVAILABLE
            and ChannelType.IDENTITY_VERIFICATION.value in self.networks
        ):
                network = self.networks[
                ChannelType.IDENTITY_VERIFICATION.value
            ]
            contract = network.get_contract("identity-chaincode")

                result = await contract.submit_transaction(
                "createAttestation", json.dumps(attestation.to_dict())
            )

                logger.info(
                f"Identity attestation created on blockchain: {result}"
            )
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.IDENTITY_VERIFICATION.value,
                "identity-chaincode",
                "createAttestation",
                [json.dumps(attestation.to_dict())],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(
            f"Failed to create identity attestation on blockchain: {e}"
        )
        raise

    async def log_agent_decision(
        self, decision_record: AgentDecisionRecord
) -> str:
        """"
    Log AI agent decision to blockchain for governance and explainability.

        Args:
            decision_record: Agent decision record

        Returns:
            Transaction ID
    """"
    try:
            # Create quantum-resistant signature for decision
        record_data = json.dumps(decision_record.to_dict(), sort_keys=True)
        signature = await self.quantum_signer.sign(record_data)
        decision_record.quantum_signature = base64.b64encode(
            signature.encode()
        ).decode()

            if (
                FABRIC_AVAILABLE
            and ChannelType.AGENT_GOVERNANCE.value in self.networks
        ):
                network = self.networks[ChannelType.AGENT_GOVERNANCE.value]
            contract = network.get_contract("governance-chaincode")

                result = await contract.submit_transaction(
                "logAgentDecision", json.dumps(decision_record.to_dict())
            )

                logger.info(f"Agent decision logged to blockchain: {result}")
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.AGENT_GOVERNANCE.value,
                "governance-chaincode",
                "logAgentDecision",
                [json.dumps(decision_record.to_dict())],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(f"Failed to log agent decision to blockchain: {e}")
        raise

    async def query_fraud_audit_trail(
        self, claim_id: str
) -> List[Dict[str, Any]]:
        """"
    Query fraud detection audit trail for a claim.

        Args:
            claim_id: Claim identifier

        Returns:
            List of fraud audit records
    """"
    try:
            if (
                FABRIC_AVAILABLE
            and ChannelType.FRAUD_AUDIT.value in self.networks
        ):
                network = self.networks[ChannelType.FRAUD_AUDIT.value]
            contract = network.get_contract("fraud-audit-chaincode")

                result = await contract.evaluate_transaction(
                "queryFraudAuditTrail", claim_id
            )

                return json.loads(result)
        else:
                # Mock implementation
            result = await self.client.query_chaincode(
                ChannelType.FRAUD_AUDIT.value,
                "fraud-audit-chaincode",
                "queryFraudAuditTrail",
                [claim_id],
            )
            return result.get("data", [])

        except Exception as e:
            logger.error(f"Failed to query fraud audit trail: {e}")
        return []

    async def query_claim_history(self, claim_id: str) -> List[Dict[str, Any]]:
        """"
    Query complete claim processing history.

        Args:
            claim_id: Claim identifier

        Returns:
            List of claim processing records
    """"
    try:
            if (
                FABRIC_AVAILABLE
            and ChannelType.CLAIMS_PROCESSING.value in self.networks
        ):
                network = self.networks[ChannelType.CLAIMS_PROCESSING.value]
            contract = network.get_contract("claims-chaincode")

                result = await contract.evaluate_transaction(
                "queryClaimHistory", claim_id
            )

                return json.loads(result)
        else:
                # Mock implementation
            result = await self.client.query_chaincode(
                ChannelType.CLAIMS_PROCESSING.value,
                "claims-chaincode",
                "queryClaimHistory",
                [claim_id],
            )
            return result.get("data", [])

        except Exception as e:
            logger.error(f"Failed to query claim history: {e}")
        return []

    async def verify_identity_attestation(
        self, user_id: str, verification_type: str
) -> Optional[Dict[str, Any]]:
        """"
    Verify identity attestation from blockchain.

        Args:
            user_id: User identifier
        verification_type: Type of verification to check

        Returns:
            Identity attestation record or None
    """"
    try:
            if (
                FABRIC_AVAILABLE
            and ChannelType.IDENTITY_VERIFICATION.value in self.networks
        ):
                network = self.networks[
                ChannelType.IDENTITY_VERIFICATION.value
            ]
            contract = network.get_contract("identity-chaincode")

                result = await contract.evaluate_transaction(
                "verifyAttestation", user_id, verification_type
            )

                return json.loads(result) if result else None
        else:
                # Mock implementation
            result = await self.client.query_chaincode(
                ChannelType.IDENTITY_VERIFICATION.value,
                "identity-chaincode",
                "verifyAttestation",
                [user_id, verification_type],
            )
            return (
                result.get("data", [{}])[0] if result.get("data") else None
            )

        except Exception as e:
            logger.error(f"Failed to verify identity attestation: {e}")
        return None

    async def query_agent_decisions(
        self,
    agent_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
        """"
    Query AI agent decision history for governance and audit.

        Args:
            agent_id: Agent identifier
        start_date: Start date filter (ISO format)
        end_date: End date filter (ISO format)

        Returns:
            List of agent decision records
    """"
    try:
            query_params = [agent_id]
        if start_date:
                query_params.append(start_date)
        if end_date:
                query_params.append(end_date)

            if (
                FABRIC_AVAILABLE
            and ChannelType.AGENT_GOVERNANCE.value in self.networks
        ):
                network = self.networks[ChannelType.AGENT_GOVERNANCE.value]
            contract = network.get_contract("governance-chaincode")

                result = await contract.evaluate_transaction(
                "queryAgentDecisions", *query_params
            )

                return json.loads(result)
        else:
                # Mock implementation
            result = await self.client.query_chaincode(
                ChannelType.AGENT_GOVERNANCE.value,
                "governance-chaincode",
                "queryAgentDecisions",
                query_params,
            )
            return result.get("data", [])

        except Exception as e:
            logger.error(f"Failed to query agent decisions: {e}")
        return []

    async def create_reinsurance_contract(
        self, contract_data: Dict[str, Any]
) -> str:
        """"
    Create reinsurance contract on blockchain for multi-party risk sharing.

        Args:
            contract_data: Reinsurance contract details

        Returns:
            Transaction ID
    """"
    try:
            contract_data["timestamp"] = datetime.now(timezone.utc).isoformat()
        contract_data["contract_id"] = str(uuid.uuid4())

            if (
                FABRIC_AVAILABLE
            and ChannelType.REINSURANCE.value in self.networks
        ):
                network = self.networks[ChannelType.REINSURANCE.value]
            contract = network.get_contract("reinsurance-chaincode")

                result = await contract.submit_transaction(
                "createReinsuranceContract", json.dumps(contract_data)
            )

                logger.info(
                f"Reinsurance contract created on blockchain: {result}"
            )
            return result
        else:
                # Mock implementation
            result = await self.client.invoke_chaincode(
                ChannelType.REINSURANCE.value,
                "reinsurance-chaincode",
                "createReinsuranceContract",
                [json.dumps(contract_data)],
            )
            return result["tx_id"]

        except Exception as e:
            logger.error(
            f"Failed to create reinsurance contract on blockchain: {e}"
        )
        raise

    async def get_network_status(self) -> Dict[str, Any]:
        """"
    Get Hyperledger Fabric network status and health.

        Returns:
            Network status information
    """"
    try:
            status = {
            "connected": bool(self.client),
            "fabric_available": FABRIC_AVAILABLE,
            "channels": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

            for channel_type in ChannelType:
                channel_name = channel_type.value
            status["channels"][channel_name] = {
                "connected": channel_name in self.networks,
                "type": channel_type.name,
            }

            return status

        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
        return {"connected": False, "error": str(e)}

    async def disconnect(self):
        """Disconnect from Hyperledger Fabric network."""
    try:
            if self.gateway:
                self.gateway.disconnect()

            self.client = None
        self.gateway = None
        self.networks = {}

            logger.info("Disconnected from Hyperledger Fabric network")

        except Exception as e:
            logger.error(f"Error disconnecting from Fabric network: {e}")


# Global Hyperledger Fabric manager instance
fabric_manager = HyperledgerFabricManager()


async def get_fabric_manager() -> HyperledgerFabricManager:
    """Get the global Hyperledger Fabric manager instance."""
if not fabric_manager.client:
        await fabric_manager.initialize()
return fabric_manager
