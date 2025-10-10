"""Consultation service for consultation-related operations."""
import logging
from typing import Optional, List
from datetime import datetime
import uuid
from src.models.consultation import Consultation, ConsultationCreate
from src.services.dynamodb_service import DynamoDBService
from src.config import get_settings

logger = logging.getLogger(__name__)


class ConsultationService:
    """Service for consultation operations."""

    def __init__(self):
        """Initialize consultation service."""
        self.db_service = DynamoDBService()
        self.settings = get_settings()
        self.table_name = self.settings.dynamodb_consultations_table

    def create_consultation(self, consultation_data: ConsultationCreate) -> Consultation:
        """Create a new consultation."""
        consultation_id = f"CONS-{uuid.uuid4().hex[:8].upper()}"

        consultation = Consultation(
            consultation_id=consultation_id, **consultation_data.model_dump()
        )

        self.db_service.put_item(self.table_name, consultation.model_dump())
        logger.info(f"Created consultation {consultation_id}")
        return consultation

    def get_consultation(self, consultation_id: str) -> Optional[Consultation]:
        """Get a consultation by ID."""
        item = self.db_service.get_item(self.table_name, {"consultation_id": consultation_id})
        if item:
            return Consultation(**item)
        return None

    def get_patient_consultations(self, patient_id: str) -> List[Consultation]:
        """Get all consultations for a patient."""
        items = self.db_service.query_by_index(
            self.table_name, "patient_id-index", "patient_id", patient_id
        )
        return [Consultation(**item) for item in items]

    def update_consultation_status(
        self, consultation_id: str, status: str, notes: Optional[str] = None
    ) -> Optional[Consultation]:
        """Update consultation status."""
        updates = {"status": status, "updated_at": datetime.utcnow().isoformat()}

        if notes:
            updates["doctor_notes"] = notes

        if status == "completed":
            updates["completed_at"] = datetime.utcnow().isoformat()

        success = self.db_service.update_item(
            self.table_name, {"consultation_id": consultation_id}, updates
        )

        if success:
            return self.get_consultation(consultation_id)
        return None
