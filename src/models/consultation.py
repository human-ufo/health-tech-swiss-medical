"""Consultation data models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .triage import TriageLevel


class ConsultationStatus(str):
    """Consultation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TriageResult(BaseModel):
    """Triage result embedded in consultation."""

    triage_level: TriageLevel
    priority_score: int
    assessment_summary: str
    recommended_action: str


class Consultation(BaseModel):
    """Consultation model."""

    consultation_id: str = Field(..., description="Unique consultation identifier")
    patient_id: str
    triage_result: Optional[TriageResult] = None
    
    # Consultation Details
    chief_complaint: str = Field(..., description="Main reason for consultation")
    symptoms_description: str
    status: str = Field(default=ConsultationStatus.PENDING)
    
    # Medical Staff
    assigned_doctor: Optional[str] = None
    assigned_specialty: Optional[str] = None
    
    # Timing
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    
    # Notes
    doctor_notes: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    prescriptions: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "consultation_id": "CONS-001",
                "patient_id": "PAT-001",
                "chief_complaint": "Dolor de pecho",
                "symptoms_description": "Dolor opresivo en el pecho con irradiación al brazo izquierdo",
                "status": "pending",
            }
        }


class ConsultationCreate(BaseModel):
    """Consultation creation model."""

    patient_id: str
    chief_complaint: str
    symptoms_description: str
