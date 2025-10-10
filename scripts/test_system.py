"""Script to test the complete system."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.coordinator_agent import CoordinatorAgent
from src.models.triage import TriageRequest, Symptom
from src.services.patient_service import PatientService

def test_triage_system():
    """Test the triage system end-to-end."""
    print("🧪 Testing Swiss Medical Triage System\n")
    
    # Initialize services
    patient_service = PatientService()
    coordinator = CoordinatorAgent()
    
    # Get a patient
    print("1️⃣ Fetching patient...")
    patients = patient_service.list_patients(limit=1)
    
    if not patients:
        print("❌ No patients found. Run 'python scripts/seed_data.py' first.")
        return
    
    patient = patients[0]
    print(f"✅ Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})\n")
    
    # Create triage request
    print("2️⃣ Creating triage request...")
    triage_request = TriageRequest(
        patient_id=patient.patient_id,
        symptoms=[
            Symptom(name="Dolor de pecho", severity=8, duration_hours=2),
            Symptom(name="Dificultad para respirar", severity=7, duration_hours=1),
        ],
        vital_signs={
            "temperature": 37.2,
            "blood_pressure": "140/90",
            "heart_rate": 95,
            "respiratory_rate": 22,
            "oxygen_saturation": 94,
        },
        additional_context="El paciente tiene antecedentes de hipertensión",
    )
    print("✅ Triage request created\n")
    
    # Process triage
    print("3️⃣ Processing triage with AI agents...")
    print("   (This may take 10-30 seconds...)\n")
    
    try:
        result = coordinator.process_triage(triage_request)
        
        print("✅ Triage completed!\n")
        print("=" * 60)
        print(f"🆔 Triage ID: {result.triage_id}")
        print(f"🎯 Triage Level: {result.triage_level.value.upper()}")
        print(f"📊 Priority Score: {result.priority_score}/100")
        print(f"⏱️  Estimated Wait Time: {result.estimated_wait_time}")
        print("=" * 60)
        print(f"\n📋 Assessment Summary:\n{result.assessment_summary}")
        print(f"\n🎯 Recommended Action:\n{result.recommended_action}")
        
        if result.recommended_specialty:
            print(f"\n👨‍⚕️ Recommended Specialty: {result.recommended_specialty}")
        
        if result.recommended_tests:
            print(f"\n🔬 Recommended Tests:")
            for test in result.recommended_tests:
                print(f"   - {test}")
        
        if result.risk_factors:
            print(f"\n⚠️  Risk Factors:")
            for factor in result.risk_factors:
                print(f"   - {factor}")
        
        print("\n✅ System test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during triage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_triage_system()
