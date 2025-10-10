"""Patient management endpoints."""
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query
from src.models.patient import Patient, PatientCreate, PatientUpdate
from src.services.patient_service import PatientService

logger = logging.getLogger(__name__)
router = APIRouter()
patient_service = PatientService()


@router.post("/", response_model=Patient, status_code=201)
async def create_patient(patient_data: PatientCreate):
    """Create a new patient."""
    try:
        patient = patient_service.create_patient(patient_data)
        return patient
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get a patient by ID."""
    patient = patient_service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, updates: PatientUpdate):
    """Update a patient."""
    patient = patient_service.update_patient(patient_id, updates)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/", response_model=List[Patient])
async def list_patients(limit: int = Query(50, ge=1, le=100)):
    """List all patients."""
    try:
        patients = patient_service.list_patients(limit=limit)
        return patients
    except Exception as e:
        logger.error(f"Error listing patients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """Get patient medical history."""
    history = patient_service.get_patient_medical_history(patient_id)
    if not history:
        raise HTTPException(status_code=404, detail="Patient not found")
    return history
