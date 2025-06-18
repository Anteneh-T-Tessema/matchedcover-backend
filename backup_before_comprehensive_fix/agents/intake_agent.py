""""
Intake Agent for MatchedCover.

This agent handles customer intake, gathering initial information
and starting the insurance application process.
""""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json

from src.agents.base_agent import BaseAgent


logger = logging.getLogger(__name__)


class IntakeAgent(BaseAgent):
    """"
Intake Agent responsible for:
    - Customer information gathering
- Initial data validation
- Application initiation
- Customer verification
""""

    def __init__(self):
        super().__init__(agent_type="intake", name="Intake Agent")
    self.supported_channels = ["web", "mobile", "phone", "chat"]
    self.required_fields = {
        "personal": ["first_name", "last_name", "email", "phone"],
        "address": ["street", "city", "state", "zip_code"],
        "insurance": ["coverage_type", "coverage_amount"],
    }

    async def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration for the Intake Agent."""
    return {
        "max_retry_attempts": 3,
        "validation_timeout": 30,
        "supported_languages": ["en", "es", "fr"],
        "data_retention_days": 30,
        "auto_verification": True,
        "require_document_upload": False,
        "min_age_requirement": 18,
        "max_coverage_amount": 10000000,
        "supported_coverage_types": [
            "auto",
            "home",
            "life",
            "health",
            "business",
            "travel",
        ],
    }

    async def _initialize_resources(self) -> None:
        """Initialize Intake Agent specific resources."""
    # Initialize data validation services
    self.validation_service = DataValidationService()

        # Initialize document processing service
    self.document_processor = DocumentProcessingService()

        # Initialize communication channels
    self.communication_channels = {
        channel: ChannelHandler(channel)
        for channel in self.supported_channels
        }

        logger.info("Intake Agent resources initialized")

    async def _cleanup_resources(self) -> None:
        """Cleanup Intake Agent specific resources."""
    # Cleanup communication channels
    for handler in self.communication_channels.values():
            await handler.cleanup()

        logger.info("Intake Agent resources cleaned up")

    async def _process_task_impl(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Process intake-related tasks."""

        if task_type == "customer_intake":
            return await self._process_customer_intake(input_data, context)
    elif task_type == "document_processing":
            return await self._process_documents(input_data, context)
    elif task_type == "data_validation":
            return await self._validate_customer_data(input_data, context)
    elif task_type == "application_initiation":
            return await self._initiate_application(input_data, context)
    else:
            raise ValueError(f"Unsupported task type: {task_type}")

    async def _validate_input(
        self, task_type: str, input_data: Dict[str, Any]
) -> None:
        """Validate input data for intake tasks."""

        if task_type == "customer_intake":
            required_fields = ["customer_info", "coverage_request"]
        for field in required_fields:
                if field not in input_data:
                    raise ValueError(f"Missing required field: {field}")

        elif task_type == "document_processing":
            if "documents" not in input_data:
                raise ValueError(
                "Documents are required for document processing"
            )

        elif task_type == "data_validation":
            if "data_to_validate" not in input_data:
                raise ValueError("Data to validate is required")

    async def _process_customer_intake(
        self,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Process customer intake information."""

        customer_info = input_data["customer_info"]
    coverage_request = input_data["coverage_request"]

        # Validate customer information
    validation_result = await self._validate_customer_data(
        {"data_to_validate": customer_info}, context
    )

        if not validation_result["is_valid"]:
            return {
            "status": "validation_failed",
            "errors": validation_result["errors"],
            "customer_id": None,
        }

        # Check age requirement
    if not await self._check_age_requirement(customer_info):
            return {
            "status": "age_requirement_not_met",
            "error": "Customer does not meet minimum age requirement",
            "customer_id": None,
        }

        # Generate customer ID
    customer_id = await self._generate_customer_id(customer_info)

        # Store preliminary customer data
    await self._store_preliminary_data(
        customer_id, customer_info, coverage_request
    )

        # Initialize application
    application_result = await self._initiate_application(
        {
            "customer_id": customer_id,
            "customer_info": customer_info,
            "coverage_request": coverage_request,
        },
        context,
    )

        return {
        "status": "intake_completed",
        "customer_id": customer_id,
        "application_id": application_result.get("application_id"),
        "next_steps": [
            "risk_assessment",
            "pricing_calculation",
            "compliance_check",
        ],
        "required_documents": await self._get_required_documents(
            coverage_request
        ),
        "estimated_processing_time": "24-48 hours",
    }

    async def _process_documents(
        self,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Process uploaded documents."""

        documents = input_data["documents"]
    customer_id = input_data.get("customer_id")

        processed_documents = []

        for document in documents:
            try:
                # Process document
            processing_result = (
                await self.document_processor.process_document(document)
            )

                processed_documents.append(
                {
                    "document_id": processing_result["document_id"],
                    "type": processing_result["document_type"],
                    "status": "processed",
                    "extracted_data": processing_result["extracted_data"],
                    "confidence_score": processing_result[
                        "confidence_score"
                    ],
                }
            )

            except Exception as e:
                processed_documents.append(
                {
                    "document_id": document.get("id"),
                    "type": document.get("type"),
                    "status": "processing_failed",
                    "error": str(e),
                }
            )

        return {
        "status": "documents_processed",
        "customer_id": customer_id,
        "processed_documents": processed_documents,
        "total_documents": len(documents),
        "successful_documents": len(
            [d for d in processed_documents if d["status"] == "processed"]
        ),
    }

    async def _validate_customer_data(
        self,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Validate customer data."""

        data_to_validate = input_data["data_to_validate"]
    validation_errors = []

        # Validate required fields
    for category, fields in self.required_fields.items():
            category_data = data_to_validate.get(category, {})
        for field in fields:
                if not category_data.get(field):
                    validation_errors.append(
                    f"Missing required field: {category}.{field}"
                )

        # Validate email format
    email = data_to_validate.get("personal", {}).get("email")
    if email and not await self._validate_email_format(email):
            validation_errors.append("Invalid email format")

        # Validate phone number
    phone = data_to_validate.get("personal", {}).get("phone")
    if phone and not await self._validate_phone_format(phone):
            validation_errors.append("Invalid phone number format")

        # Validate coverage type
    coverage_type = data_to_validate.get("insurance", {}).get(
        "coverage_type"
    )
    if (
            coverage_type
        and coverage_type not in self.config["supported_coverage_types"]
    ):
            validation_errors.append(
            f"Unsupported coverage type: {coverage_type}"
        )

        # Validate coverage amount
    coverage_amount = data_to_validate.get("insurance", {}).get(
        "coverage_amount"
    )
    if coverage_amount:
            try:
                amount = float(coverage_amount)
            if amount > self.config["max_coverage_amount"]:
                    validation_errors.append(
                    "Coverage amount exceeds maximum limit"
                )
            if amount <= 0:
                    validation_errors.append(
                    "Coverage amount must be positive"
                )
        except (ValueError, TypeError):
                validation_errors.append("Invalid coverage amount format")

        return {
        "is_valid": len(validation_errors) == 0,
        "errors": validation_errors,
        "validated_data": data_to_validate,
    }

    async def _initiate_application(
        self,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Initiate insurance application."""

        customer_id = input_data["customer_id"]
    customer_info = input_data["customer_info"]
    coverage_request = input_data["coverage_request"]

        # Generate application ID
    application_id = (
        f"APP-{customer_id}-{int(asyncio.get_event_loop().time())}"
    )

        # Create application record
    application_data = {
        "application_id": application_id,
        "customer_id": customer_id,
        "customer_info": customer_info,
        "coverage_request": coverage_request,
        "status": "initiated",
        "created_at": "2024-01-01T00:00:00Z",  # Placeholder
        "workflow_stage": "intake_completed",
    }

        # Store application data (in a real implementation, this would be in
    # database)
    await self._store_application_data(application_data)

        return {
        "application_id": application_id,
        "status": "application_initiated",
        "workflow_stage": "intake_completed",
        "next_agent": "risk_assessor",
    }

    # Helper methods

    async def _check_age_requirement(
        self, customer_info: Dict[str, Any]
) -> bool:
        """Check if customer meets age requirement."""
    # Simplified age check - in real implementation would use date of birth
    return True  # Placeholder

    async def _generate_customer_id(
        self, customer_info: Dict[str, Any]
) -> str:
        """Generate unique customer ID."""
    import hashlib
    import time

        # Create a hash based on customer info and timestamp
    info_str = json.dumps(
        customer_info.get("personal", {}), sort_keys=True
    )
    hash_input = f"{info_str}_{time.time()}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:12].upper()

    async def _store_preliminary_data(
        self,
    customer_id: str,
    customer_info: Dict[str, Any],
    coverage_request: Dict[str, Any],
) -> None:
        """Store preliminary customer data."""
    # In a real implementation, this would store in database
    logger.info(f"Storing preliminary data for customer {customer_id}")

    async def _store_application_data(
        self, application_data: Dict[str, Any]
) -> None:
        """Store application data."""
    # In a real implementation, this would store in database
    logger.info(
        f"Storing application data: {application_data['application_id']}"
    )

    async def _get_required_documents(
        self, coverage_request: Dict[str, Any]
) -> List[str]:
        """Get list of required documents based on coverage type."""
    coverage_type = coverage_request.get("coverage_type", "")

        document_requirements = {
        "auto": [
            "driver_license",
            "vehicle_registration",
            "previous_insurance",
        ],
        "home": ["property_deed", "home_inspection", "previous_insurance"],
        "life": [
            "medical_records",
            "beneficiary_info",
            "financial_statements",
        ],
        "health": ["medical_records", "employment_verification"],
        "business": [
            "business_license",
            "financial_statements",
            "employee_records",
        ],
        "travel": ["passport", "travel_itinerary"],
    }

        return document_requirements.get(
        coverage_type, ["identity_verification"]
    )

    async def _validate_email_format(self, email: str) -> bool:
        """Validate email format."""
    import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

    async def _validate_phone_format(self, phone: str) -> bool:
        """Validate phone number format."""
    import re

        # Remove non-digit characters
    digits_only = re.sub(r"\D", "", phone)
    # Check if it's a valid length (10-15 digits)'
    return 10 <= len(digits_only) <= 15

    def get_capabilities(self) -> List[str]:
        """Get list of Intake Agent capabilities."""
    return [
        "customer_intake",
        "document_processing",
        "data_validation",
        "application_initiation",
        "multi_channel_communication",
        "real_time_validation",
    ]


# Helper classes (simplified implementations)


class DataValidationService:
    """Service for validating customer data."""

    async def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data and return results."""
    # Simplified implementation
    return {"is_valid": True, "errors": []}


class DocumentProcessingService:
    """Service for processing uploaded documents."""

    async def process_document(
        self, document: Dict[str, Any]
) -> Dict[str, Any]:
        """Process document and extract data."""
    # Simplified implementation
    return {
        "document_id": f"DOC_{document.get('id', 'unknown')}",
        "document_type": document.get("type", "unknown"),
        "extracted_data": {},
        "confidence_score": 0.95,
    }


class ChannelHandler:
    """Handler for different communication channels."""

    def __init__(self, channel: str):
        self.channel = channel

    async def cleanup(self) -> None:
        """Cleanup channel resources."""
    pass
