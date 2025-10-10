"""Script to seed database with sample data."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.patient_service import PatientService
from src.models.patient import PatientCreate, Gender, BloodType

def seed_patients():
    """Create sample patients."""
    patient_service = PatientService()
    
    sample_patients = [
        PatientCreate(
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
        ),
        PatientCreate(
            first_name="María",
            last_name="González",
            date_of_birth="1990-08-22",
            gender=Gender.FEMALE,
            blood_type=BloodType.A_POSITIVE,
            phone="+541156789012",
            email="maria.gonzalez@email.com",
            allergies=[],
            chronic_conditions=["Diabetes Tipo 2"],
            current_medications=["Metformina 850mg"],
        ),
        PatientCreate(
            first_name="Carlos",
            last_name="Rodríguez",
            date_of_birth="1978-03-10",
            gender=Gender.MALE,
            blood_type=BloodType.B_POSITIVE,
            phone="+541167890123",
            email="carlos.rodriguez@email.com",
            allergies=["Ibuprofeno"],
            chronic_conditions=[],
            current_medications=[],
        ),
    ]
    
    print("🌱 Seeding database with sample patients...")
    
    for patient_data in sample_patients:
        try:
            patient = patient_service.create_patient(patient_data)
            print(f"✅ Created patient: {patient.patient_id} - {patient.first_name} {patient.last_name}")
        except Exception as e:
            print(f"❌ Error creating patient: {e}")
    
    print("\n✅ Database seeding completed!")

if __name__ == "__main__":
    seed_patients()
