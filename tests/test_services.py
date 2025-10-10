"""Tests for services."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.patient_service import PatientService
from src.models.patient import PatientCreate, Gender, BloodType


class TestPatientService:
    """Test patient service."""

    @patch('src.services.patient_service.DynamoDBService')
    def test_create_patient(self, mock_db_service):
        """Test patient creation."""
        # Setup mock
        mock_db = Mock()
        mock_db.put_item.return_value = True
        mock_db_service.return_value = mock_db

        # Create service
        service = PatientService()

        # Create patient data
        patient_data = PatientCreate(
            first_name="Juan",
            last_name="Pérez",
            date_of_birth="1985-05-15",
            gender=Gender.MALE,
            phone="+541145678900",
        )

        # Create patient
        patient = service.create_patient(patient_data)

        # Assertions
        assert patient.first_name == "Juan"
        assert patient.last_name == "Pérez"
        assert patient.patient_id.startswith("PAT-")
        mock_db.put_item.assert_called_once()

    @patch('src.services.patient_service.DynamoDBService')
    def test_get_patient(self, mock_db_service):
        """Test get patient."""
        # Setup mock
        mock_db = Mock()
        mock_db.get_item.return_value = {
            "patient_id": "PAT-001",
            "first_name": "Juan",
            "last_name": "Pérez",
            "date_of_birth": "1985-05-15",
            "gender": "male",
            "phone": "+541145678900",
            "allergies": [],
            "chronic_conditions": [],
            "current_medications": [],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "is_active": True,
        }
        mock_db_service.return_value = mock_db

        # Create service
        service = PatientService()

        # Get patient
        patient = service.get_patient("PAT-001")

        # Assertions
        assert patient is not None
        assert patient.patient_id == "PAT-001"
        assert patient.first_name == "Juan"
        mock_db.get_item.assert_called_once()

    @patch('src.services.patient_service.DynamoDBService')
    def test_calculate_age(self, mock_db_service):
        """Test age calculation."""
        service = PatientService()
        age = service._calculate_age("1985-05-15")
        assert age > 0
        assert isinstance(age, int)
