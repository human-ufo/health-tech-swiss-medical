"""Triage data models."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class TriageLevel(str, Enum):
    """Triage priority levels based on medical standards."""

    CRITICAL = "critical"  # Immediate attention - life-threatening
    URGENT = "urgent"  # Within 15-30 minutes
    SEMI_URGENT = "semi_urgent"  # Within 1-2 hours
    NON_URGENT = "non_urgent"  # Within 2-4 hours
    ROUTINE = "routine"  # Can wait, schedule appointment


class Symptom(BaseModel):
    """Individual symptom model."""

    name: str = Field(..., description="Symptom name")
    severity: int = Field(..., ge=1, le=10, description="Severity from 1 (mild) to 10 (severe)")
    duration_hours: Optional[int] = Field(None, description="Duration in hours")
    description: Optional[str] = Field(None, description="Additional details")


class TriageRequest(BaseModel):
    """Request model for triage assessment."""

    patient_id: str = Field(..., description="Patient identifier")
    symptoms: List[Symptom] = Field(..., min_length=1, description="List of symptoms")
    vital_signs: Optional[dict] = Field(
        None,
        description="Vital signs (temperature, blood_pressure, heart_rate, respiratory_rate, oxygen_saturation)",
    )
    additional_context: Optional[str] = Field(None, description="Additional context or concerns")

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "PAT-001",
                "symptoms": [
                    {"name": "Dolor de pecho", "severity": 8, "duration_hours": 2},
                    {"name": "Dificultad para respirar", "severity": 7, "duration_hours": 1},
                ],
                "vital_signs": {
                    "temperature": 37.2,
                    "blood_pressure": "140/90",
                    "heart_rate": 95,
                    "respiratory_rate": 22,
                    "oxygen_saturation": 94,
                },
                "additional_context": "El paciente tiene antecedentes de hipertensión",
            }
        }


class TriageResponse(BaseModel):
    """Response model for triage assessment."""

    triage_id: str = Field(..., description="Unique triage identifier")
    patient_id: str
    triage_level: TriageLevel
    priority_score: int = Field(..., ge=0, le=100, description="Priority score (0-100)")
    
    # Assessment Results
    assessment_summary: str = Field(..., description="Summary of the assessment")
    recommended_action: str = Field(..., description="Recommended immediate action")
    recommended_specialty: Optional[str] = Field(None, description="Recommended medical specialty")
    recommended_tests: List[str] = Field(default_factory=list, description="Recommended tests")
    
    # Risk Factors
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    warning_signs: List[str] = Field(default_factory=list, description="Warning signs to monitor")
    
    # Timing
    estimated_wait_time: Optional[str] = Field(None, description="Estimated wait time")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Agent Information
    agent_reasoning: Optional[str] = Field(None, description="Agent's reasoning process")

    class Config:
        json_schema_extra = {
            "example": {
                "triage_id": "TRI-001",
                "patient_id": "PAT-001",
                "triage_level": "urgent",
                "priority_score": 85,
                "assessment_summary": "Paciente con dolor torácico y disnea, requiere evaluación inmediata",
                "recommended_action": "Derivar a emergencias para evaluación cardiológica inmediata",
                "recommended_specialty": "Cardiología",
                "recommended_tests": ["ECG", "Troponinas", "Radiografía de tórax"],
                "risk_factors": ["Hipertensión", "Dolor torácico agudo"],
                "warning_signs": ["Aumento del dolor", "Pérdida de conciencia", "Sudoración profusa"],
                "estimated_wait_time": "15-30 minutos",
            }
        }
