"""Triage assessment page."""
import streamlit as st
from src.agents.coordinator_agent import CoordinatorAgent
from src.models.triage import TriageRequest, Symptom, TriageLevel
from src.services.patient_service import PatientService


def show():
    """Display triage assessment page."""
    st.title("🩺 Evaluación de Triaje")
    
    coordinator = CoordinatorAgent()
    patient_service = PatientService()
    
    st.markdown(
        """
        Este sistema utiliza **Agentes de IA** para evaluar síntomas y asignar prioridad médica.
        Complete el formulario a continuación para iniciar la evaluación.
        """
    )
    
    st.markdown("---")
    
    with st.form("triage_form"):
        # Patient selection
        st.subheader("1️⃣ Identificación del Paciente")
        patient_id = st.text_input(
            "ID del Paciente *",
            placeholder="PAT-XXXXXXXX",
            help="Ingrese el ID del paciente registrado",
        )
        
        # Verify patient
        if patient_id:
            try:
                patient = patient_service.get_patient(patient_id)
                if patient:
                    st.success(f"✅ Paciente: {patient.first_name} {patient.last_name}")
                else:
                    st.warning("⚠️ Paciente no encontrado. Verifique el ID.")
            except:
                pass
        
        st.markdown("---")
        
        # Symptoms
        st.subheader("2️⃣ Síntomas")
        
        num_symptoms = st.number_input(
            "Número de síntomas a reportar",
            min_value=1,
            max_value=10,
            value=2,
        )
        
        symptoms = []
        for i in range(int(num_symptoms)):
            st.markdown(f"**Síntoma {i+1}**")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                symptom_name = st.text_input(
                    f"Nombre del síntoma {i+1}",
                    key=f"symptom_name_{i}",
                    placeholder="Ej: Dolor de pecho",
                )
            
            with col2:
                severity = st.slider(
                    f"Severidad {i+1}",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key=f"severity_{i}",
                )
            
            with col3:
                duration = st.number_input(
                    f"Duración (horas) {i+1}",
                    min_value=0,
                    max_value=720,
                    value=2,
                    key=f"duration_{i}",
                )
            
            if symptom_name:
                symptoms.append(
                    {
                        "name": symptom_name,
                        "severity": severity,
                        "duration_hours": duration,
                    }
                )
        
        st.markdown("---")
        
        # Vital signs
        st.subheader("3️⃣ Signos Vitales (Opcional)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temperature = st.number_input(
                "Temperatura (°C)",
                min_value=35.0,
                max_value=42.0,
                value=37.0,
                step=0.1,
            )
            heart_rate = st.number_input(
                "Frecuencia Cardíaca (lpm)",
                min_value=40,
                max_value=200,
                value=75,
            )
        
        with col2:
            blood_pressure_sys = st.number_input(
                "Presión Sistólica",
                min_value=60,
                max_value=250,
                value=120,
            )
            blood_pressure_dia = st.number_input(
                "Presión Diastólica",
                min_value=40,
                max_value=150,
                value=80,
            )
        
        with col3:
            respiratory_rate = st.number_input(
                "Frecuencia Respiratoria (rpm)",
                min_value=8,
                max_value=60,
                value=16,
            )
            oxygen_saturation = st.number_input(
                "Saturación de O₂ (%)",
                min_value=70,
                max_value=100,
                value=98,
            )
        
        vital_signs = {
            "temperature": temperature,
            "blood_pressure": f"{blood_pressure_sys}/{blood_pressure_dia}",
            "heart_rate": heart_rate,
            "respiratory_rate": respiratory_rate,
            "oxygen_saturation": oxygen_saturation,
        }
        
        st.markdown("---")
        
        # Additional context
        st.subheader("4️⃣ Contexto Adicional")
        additional_context = st.text_area(
            "Información adicional o preocupaciones",
            placeholder="Ej: El paciente tiene antecedentes de hipertensión...",
            height=100,
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Iniciar Evaluación de Triaje", use_container_width=True)
        
        if submitted:
            if not patient_id:
                st.error("❌ Por favor ingrese el ID del paciente")
            elif not symptoms:
                st.error("❌ Por favor ingrese al menos un síntoma")
            else:
                try:
                    with st.spinner("🤖 Los agentes de IA están evaluando al paciente..."):
                        # Create triage request
                        triage_request = TriageRequest(
                            patient_id=patient_id,
                            symptoms=[Symptom(**s) for s in symptoms],
                            vital_signs=vital_signs,
                            additional_context=additional_context if additional_context else None,
                        )
                        
                        # Process triage
                        result = coordinator.process_triage(triage_request)
                        
                        # Display results
                        st.success("✅ Evaluación completada!")
                        st.markdown("---")
                        
                        # Triage level with color coding
                        level_colors = {
                            TriageLevel.CRITICAL: "🔴",
                            TriageLevel.URGENT: "🟠",
                            TriageLevel.SEMI_URGENT: "🟡",
                            TriageLevel.NON_URGENT: "🟢",
                            TriageLevel.ROUTINE: "🔵",
                        }
                        
                        st.markdown(
                            f"## {level_colors.get(result.triage_level, '⚪')} Nivel de Triaje: {result.triage_level.value.upper()}"
                        )
                        st.metric("Puntuación de Prioridad", f"{result.priority_score}/100")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📋 Resumen de Evaluación")
                            st.write(result.assessment_summary)
                            
                            st.subheader("🎯 Acción Recomendada")
                            st.info(result.recommended_action)
                            
                            if result.recommended_specialty:
                                st.subheader("👨‍⚕️ Especialidad Recomendada")
                                st.write(result.recommended_specialty)
                        
                        with col2:
                            if result.recommended_tests:
                                st.subheader("🔬 Estudios Recomendados")
                                for test in result.recommended_tests:
                                    st.write(f"- {test}")
                            
                            if result.risk_factors:
                                st.subheader("⚠️ Factores de Riesgo")
                                for factor in result.risk_factors:
                                    st.write(f"- {factor}")
                            
                            if result.warning_signs:
                                st.subheader("🚨 Señales de Alerta")
                                for sign in result.warning_signs:
                                    st.write(f"- {sign}")
                        
                        if result.estimated_wait_time:
                            st.info(f"⏱️ **Tiempo estimado de espera:** {result.estimated_wait_time}")
                        
                        st.markdown("---")
                        st.write(f"**ID de Triaje:** {result.triage_id}")
                        st.write(f"**Fecha:** {result.created_at}")
                        
                        # Show agent reasoning if available
                        if result.agent_reasoning:
                            with st.expander("🤖 Ver Razonamiento del Agente"):
                                st.write(result.agent_reasoning)
                
                except Exception as e:
                    st.error(f"❌ Error durante la evaluación: {str(e)}")
                    st.exception(e)
