"""Patient data models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class BloodType(str, Enum):
    """Blood type enumeration."""

    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class Gender(str, Enum):
    """Gender enumeration."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Patient(BaseModel):
    """Patient model."""

    patient_id: str = Field(..., description="Unique patient identifier")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    gender: Gender
    blood_type: Optional[BloodType] = None
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: Optional[str] = None
    address: Optional[str] = None
    
    # Medical Information
    allergies: List[str] = Field(default_factory=list)
    chronic_conditions: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "PAT-001",
                "first_name": "Juan",
                "last_name": "Pérez",
                "date_of_birth": "1985-05-15",
                "gender": "male",
                "blood_type": "O+",
                "phone": "+541145678900",
                "email": "juan.perez@email.com",
                "allergies": ["Penicilina"],
                "chronic_conditions": ["Hipertensión"],
                "current_medications": ["Enalapril 10mg"],
            }
        }


class PatientCreate(BaseModel):
    """Patient creation model."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str
    gender: Gender
    blood_type: Optional[BloodType] = None
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    allergies: List[str] = Field(default_factory=list)
    chronic_conditions: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)


class PatientUpdate(BaseModel):
    """Patient update model."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    is_active: Optional[bool] = None
