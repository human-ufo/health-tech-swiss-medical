"""Patient management page."""
import streamlit as st
from src.services.patient_service import PatientService
from src.models.patient import PatientCreate, Gender, BloodType


def show():
    """Display patient management page."""
    st.title("👤 Gestión de Pacientes")
    
    patient_service = PatientService()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["➕ Nuevo Paciente", "🔍 Buscar Paciente", "📋 Lista de Pacientes"])
    
    # Tab 1: Create new patient
    with tab1:
        st.subheader("Registrar Nuevo Paciente")
        
        with st.form("new_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("Nombre *", placeholder="Juan")
                last_name = st.text_input("Apellido *", placeholder="Pérez")
                date_of_birth = st.date_input("Fecha de Nacimiento *")
                gender = st.selectbox("Género *", options=[g.value for g in Gender])
                blood_type = st.selectbox(
                    "Tipo de Sangre",
                    options=[""] + [bt.value for bt in BloodType],
                    index=0,
                )
            
            with col2:
                phone = st.text_input("Teléfono *", placeholder="+541145678900")
                email = st.text_input("Email", placeholder="juan.perez@email.com")
                address = st.text_area("Dirección", placeholder="Calle 123, CABA")
            
            st.markdown("---")
            st.subheader("Información Médica")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                allergies = st.text_area(
                    "Alergias (una por línea)",
                    placeholder="Penicilina\nMariscos",
                    height=100,
                )
            
            with col2:
                chronic_conditions = st.text_area(
                    "Condiciones Crónicas (una por línea)",
                    placeholder="Hipertensión\nDiabetes",
                    height=100,
                )
            
            with col3:
                current_medications = st.text_area(
                    "Medicamentos Actuales (uno por línea)",
                    placeholder="Enalapril 10mg\nMetformina 500mg",
                    height=100,
                )
            
            submitted = st.form_submit_button("Registrar Paciente", use_container_width=True)
            
            if submitted:
                try:
                    patient_data = PatientCreate(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=str(date_of_birth),
                        gender=Gender(gender),
                        blood_type=BloodType(blood_type) if blood_type else None,
                        phone=phone,
                        email=email if email else None,
                        address=address if address else None,
                        allergies=[a.strip() for a in allergies.split("\n") if a.strip()],
                        chronic_conditions=[
                            c.strip() for c in chronic_conditions.split("\n") if c.strip()
                        ],
                        current_medications=[
                            m.strip() for m in current_medications.split("\n") if m.strip()
                        ],
                    )
                    
                    patient = patient_service.create_patient(patient_data)
                    st.success(f"✅ Paciente registrado exitosamente! ID: {patient.patient_id}")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error al registrar paciente: {str(e)}")
    
    # Tab 2: Search patient
    with tab2:
        st.subheader("Buscar Paciente")
        
        patient_id = st.text_input("ID del Paciente", placeholder="PAT-XXXXXXXX")
        
        if st.button("🔍 Buscar", use_container_width=True):
            if patient_id:
                try:
                    patient = patient_service.get_patient(patient_id)
                    
                    if patient:
                        st.success(f"✅ Paciente encontrado: {patient.first_name} {patient.last_name}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Información Personal**")
                            st.write(f"**ID:** {patient.patient_id}")
                            st.write(f"**Nombre:** {patient.first_name} {patient.last_name}")
                            st.write(f"**Fecha de Nacimiento:** {patient.date_of_birth}")
                            st.write(f"**Género:** {patient.gender}")
                            st.write(f"**Tipo de Sangre:** {patient.blood_type or 'No especificado'}")
                            st.write(f"**Teléfono:** {patient.phone}")
                            st.write(f"**Email:** {patient.email or 'No especificado'}")
                        
                        with col2:
                            st.markdown("**Información Médica**")
                            st.write(f"**Alergias:** {', '.join(patient.allergies) or 'Ninguna'}")
                            st.write(
                                f"**Condiciones Crónicas:** {', '.join(patient.chronic_conditions) or 'Ninguna'}"
                            )
                            st.write(
                                f"**Medicamentos:** {', '.join(patient.current_medications) or 'Ninguno'}"
                            )
                    else:
                        st.warning("⚠️ Paciente no encontrado")
                
                except Exception as e:
                    st.error(f"❌ Error al buscar paciente: {str(e)}")
            else:
                st.warning("⚠️ Por favor ingrese un ID de paciente")
    
    # Tab 3: List patients
    with tab3:
        st.subheader("Lista de Pacientes")
        
        try:
            patients = patient_service.list_patients(limit=20)
            
            if patients:
                st.write(f"**Total de pacientes:** {len(patients)}")
                
                for patient in patients:
                    with st.expander(
                        f"👤 {patient.first_name} {patient.last_name} - {patient.patient_id}"
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Fecha de Nacimiento:** {patient.date_of_birth}")
                            st.write(f"**Género:** {patient.gender}")
                            st.write(f"**Teléfono:** {patient.phone}")
                        
                        with col2:
                            st.write(f"**Alergias:** {', '.join(patient.allergies) or 'Ninguna'}")
                            st.write(
                                f"**Condiciones:** {', '.join(patient.chronic_conditions) or 'Ninguna'}"
                            )
            else:
                st.info("ℹ️ No hay pacientes registrados")
        
        except Exception as e:
            st.error(f"❌ Error al listar pacientes: {str(e)}")
