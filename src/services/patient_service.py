"""Patient service for patient-related operations."""
import logging
from typing import Optional, List
from datetime import datetime
import uuid
from src.models.patient import Patient, PatientCreate, PatientUpdate
from src.services.dynamodb_service import DynamoDBService
from src.config import get_settings

logger = logging.getLogger(__name__)


class PatientService:
    """Service for patient operations."""

    def __init__(self):
        """Initialize patient service."""
        self.db_service = DynamoDBService()
        self.settings = get_settings()
        self.table_name = self.settings.dynamodb_patients_table

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        """Create a new patient."""
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        patient = Patient(
            patient_id=patient_id,
            **patient_data.model_dump(),
        )

        self.db_service.put_item(self.table_name, patient.model_dump())
        logger.info(f"Created patient {patient_id}")
        return patient

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get a patient by ID."""
        item = self.db_service.get_item(self.table_name, {"patient_id": patient_id})
        if item:
            return Patient(**item)
        return None

    def update_patient(self, patient_id: str, updates: PatientUpdate) -> Optional[Patient]:
        """Update a patient."""
        update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow().isoformat()

        success = self.db_service.update_item(
            self.table_name, {"patient_id": patient_id}, update_data
        )

        if success:
            return self.get_patient(patient_id)
        return None

    def list_patients(self, limit: Optional[int] = 50) -> List[Patient]:
        """List all patients."""
        items = self.db_service.scan_table(self.table_name, limit=limit)
        return [Patient(**item) for item in items]

    def get_patient_medical_history(self, patient_id: str) -> dict:
        """Get patient's medical history summary."""
        patient = self.get_patient(patient_id)
        if not patient:
            return {}

        return {
            "patient_id": patient.patient_id,
            "name": f"{patient.first_name} {patient.last_name}",
            "age": self._calculate_age(patient.date_of_birth),
            "blood_type": patient.blood_type,
            "allergies": patient.allergies,
            "chronic_conditions": patient.chronic_conditions,
            "current_medications": patient.current_medications,
        }

    @staticmethod
    def _calculate_age(date_of_birth: str) -> int:
        """Calculate age from date of birth."""
        from datetime import datetime

        dob = datetime.fromisoformat(date_of_birth.replace("Z", "+00:00"))
        today = datetime.utcnow()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
