"""Data models for the application."""
from .patient import Patient, PatientCreate, PatientUpdate
from .consultation import Consultation, ConsultationCreate, TriageResult
from .triage import TriageLevel, Symptom, TriageRequest, TriageResponse

__all__ = [
    "Patient",
    "PatientCreate",
    "PatientUpdate",
    "Consultation",
    "ConsultationCreate",
    "TriageResult",
    "TriageLevel",
    "Symptom",
    "TriageRequest",
    "TriageResponse",
]
