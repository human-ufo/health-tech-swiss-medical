"""Consultation history page."""
import streamlit as st
from src.services.consultation_service import ConsultationService
from src.services.dynamodb_service import DynamoDBService
from src.config import get_settings


def show():
    """Display consultation history page."""
    st.title("📋 Historial de Consultas y Triajes")
    
    consultation_service = ConsultationService()
    db_service = DynamoDBService()
    settings = get_settings()
    
    tab1, tab2 = st.tabs(["🩺 Historial de Triajes", "📋 Consultas"])
    
    # Tab 1: Triage history
    with tab1:
        st.subheader("Historial de Evaluaciones de Triaje")
        
        # Search by patient
        patient_id = st.text_input("Buscar por ID de Paciente", placeholder="PAT-XXXXXXXX")
        
        if st.button("🔍 Buscar Triajes", use_container_width=True):
            if patient_id:
                try:
                    triages = db_service.query_by_index(
                        settings.dynamodb_triage_table,
                        "patient_id-index",
                        "patient_id",
                        patient_id,
                    )
                    
                    if triages:
                        st.success(f"✅ Se encontraron {len(triages)} evaluaciones de triaje")
                        
                        for triage in sorted(
                            triages, key=lambda x: x.get("created_at", ""), reverse=True
                        ):
                            with st.expander(
                                f"🩺 {triage.get('triage_id')} - {triage.get('triage_level', 'N/A').upper()} - {triage.get('created_at', 'N/A')}"
                            ):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Nivel de Triaje:** {triage.get('triage_level', 'N/A')}")
                                    st.write(
                                        f"**Puntuación:** {triage.get('priority_score', 'N/A')}/100"
                                    )
                                    st.write(
                                        f"**Especialidad:** {triage.get('recommended_specialty', 'N/A')}"
                                    )
                                    st.write(
                                        f"**Tiempo de Espera:** {triage.get('estimated_wait_time', 'N/A')}"
                                    )
                                
                                with col2:
                                    st.write("**Resumen:**")
                                    st.write(triage.get("assessment_summary", "N/A"))
                                
                                st.markdown("---")
                                st.write("**Acción Recomendada:**")
                                st.info(triage.get("recommended_action", "N/A"))
                                
                                if triage.get("recommended_tests"):
                                    st.write("**Estudios Recomendados:**")
                                    for test in triage.get("recommended_tests", []):
                                        st.write(f"- {test}")
                    else:
                        st.warning("⚠️ No se encontraron evaluaciones de triaje para este paciente")
                
                except Exception as e:
                    st.error(f"❌ Error al buscar triajes: {str(e)}")
            else:
                st.warning("⚠️ Por favor ingrese un ID de paciente")
        
        # Show recent triages
        st.markdown("---")
        st.subheader("Evaluaciones Recientes")
        
        try:
            recent_triages = db_service.scan_table(settings.dynamodb_triage_table, limit=10)
            
            if recent_triages:
                for triage in sorted(
                    recent_triages, key=lambda x: x.get("created_at", ""), reverse=True
                ):
                    level_emoji = {
                        "critical": "🔴",
                        "urgent": "🟠",
                        "semi_urgent": "🟡",
                        "non_urgent": "🟢",
                        "routine": "🔵",
                    }
                    
                    emoji = level_emoji.get(triage.get("triage_level", ""), "⚪")
                    
                    st.markdown(
                        f"{emoji} **{triage.get('triage_id')}** - Paciente: {triage.get('patient_id')} - "
                        f"Nivel: {triage.get('triage_level', 'N/A').upper()} - "
                        f"Fecha: {triage.get('created_at', 'N/A')}"
                    )
            else:
                st.info("ℹ️ No hay evaluaciones de triaje registradas")
        
        except Exception as e:
            st.error(f"❌ Error al cargar triajes recientes: {str(e)}")
    
    # Tab 2: Consultations
    with tab2:
        st.subheader("Historial de Consultas")
        
        patient_id = st.text_input(
            "Buscar consultas por ID de Paciente",
            placeholder="PAT-XXXXXXXX",
            key="consultation_search",
        )
        
        if st.button("🔍 Buscar Consultas", use_container_width=True):
            if patient_id:
                try:
                    consultations = consultation_service.get_patient_consultations(patient_id)
                    
                    if consultations:
                        st.success(f"✅ Se encontraron {len(consultations)} consultas")
                        
                        for consultation in consultations:
                            with st.expander(
                                f"📋 {consultation.consultation_id} - {consultation.status} - {consultation.created_at}"
                            ):
                                st.write(f"**Motivo de Consulta:** {consultation.chief_complaint}")
                                st.write(f"**Descripción:** {consultation.symptoms_description}")
                                st.write(f"**Estado:** {consultation.status}")
                                
                                if consultation.assigned_doctor:
                                    st.write(f"**Médico Asignado:** {consultation.assigned_doctor}")
                                
                                if consultation.assigned_specialty:
                                    st.write(
                                        f"**Especialidad:** {consultation.assigned_specialty}"
                                    )
                                
                                if consultation.doctor_notes:
                                    st.markdown("**Notas del Médico:**")
                                    st.info(consultation.doctor_notes)
                    else:
                        st.warning("⚠️ No se encontraron consultas para este paciente")
                
                except Exception as e:
                    st.error(f"❌ Error al buscar consultas: {str(e)}")
            else:
                st.warning("⚠️ Por favor ingrese un ID de paciente")
