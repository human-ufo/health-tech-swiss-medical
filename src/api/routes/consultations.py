"""Consultation endpoints."""
import logging
from typing import List
from fastapi import APIRouter, HTTPException
from src.models.consultation import Consultation, ConsultationCreate
from src.services.consultation_service import ConsultationService

logger = logging.getLogger(__name__)
router = APIRouter()
consultation_service = ConsultationService()


@router.post("/", response_model=Consultation, status_code=201)
async def create_consultation(consultation_data: ConsultationCreate):
    """Create a new consultation."""
    try:
        consultation = consultation_service.create_consultation(consultation_data)
        return consultation
    except Exception as e:
        logger.error(f"Error creating consultation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{consultation_id}", response_model=Consultation)
async def get_consultation(consultation_id: str):
    """Get a consultation by ID."""
    consultation = consultation_service.get_consultation(consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation


@router.get("/patient/{patient_id}", response_model=List[Consultation])
async def get_patient_consultations(patient_id: str):
    """Get all consultations for a patient."""
    try:
        consultations = consultation_service.get_patient_consultations(patient_id)
        return consultations
    except Exception as e:
        logger.error(f"Error getting patient consultations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{consultation_id}/status")
async def update_consultation_status(
    consultation_id: str, status: str, notes: str = None
):
    """Update consultation status."""
    consultation = consultation_service.update_consultation_status(
        consultation_id, status, notes
    )
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation
