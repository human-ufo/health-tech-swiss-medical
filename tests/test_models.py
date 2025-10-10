"""Tests for data models."""
import pytest
from datetime import datetime
from src.models.patient import Patient, PatientCreate, Gender, BloodType
from src.models.triage import TriageRequest, Symptom, TriageLevel


class TestPatientModels:
    """Test patient models."""

    def test_patient_create(self):
        """Test patient creation model."""
        patient_data = PatientCreate(
            first_name="Juan",
            last_name="Pérez",
            date_of_birth="1985-05-15",
            gender=Gender.MALE,
            blood_type=BloodType.O_POSITIVE,
            phone="+541145678900",
            email="juan.perez@email.com",
            allergies=["Penicilina"],
            chronic_conditions=["Hipertensión"],
            current_medications=["Enalapril 10mg"],
        )

        assert patient_data.first_name == "Juan"
        assert patient_data.gender == Gender.MALE
        assert len(patient_data.allergies) == 1

    def test_patient_model(self):
        """Test patient model."""
        patient = Patient(
            patient_id="PAT-001",
            first_name="Juan",
            last_name="Pérez",
            date_of_birth="1985-05-15",
            gender=Gender.MALE,
            phone="+541145678900",
        )

        assert patient.patient_id == "PAT-001"
        assert patient.is_active is True


class TestTriageModels:
    """Test triage models."""

    def test_symptom_model(self):
        """Test symptom model."""
        symptom = Symptom(
            name="Dolor de pecho",
            severity=8,
            duration_hours=2,
            description="Dolor opresivo",
        )

        assert symptom.name == "Dolor de pecho"
        assert symptom.severity == 8
        assert 1 <= symptom.severity <= 10

    def test_triage_request(self):
        """Test triage request model."""
        request = TriageRequest(
            patient_id="PAT-001",
            symptoms=[
                Symptom(name="Dolor de pecho", severity=8, duration_hours=2),
                Symptom(name="Dificultad para respirar", severity=7, duration_hours=1),
            ],
            vital_signs={
                "temperature": 37.2,
                "blood_pressure": "140/90",
                "heart_rate": 95,
            },
        )

        assert request.patient_id == "PAT-001"
        assert len(request.symptoms) == 2
        assert request.vital_signs["heart_rate"] == 95

    def test_triage_levels(self):
        """Test triage level enum."""
        assert TriageLevel.CRITICAL.value == "critical"
        assert TriageLevel.URGENT.value == "urgent"
        assert TriageLevel.ROUTINE.value == "routine"
