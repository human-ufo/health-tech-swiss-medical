"""Home page for Streamlit UI."""
import streamlit as st
from datetime import datetime


def show():
    """Display home page."""
    st.markdown('<h1 class="main-header">🏥 Sistema de Triaje Médico Inteligente</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome message
    st.markdown(
        """
        ### Bienvenido al Sistema de Triaje de Swiss Medical Group
        
        Este sistema utiliza **Inteligencia Artificial** y **Agentes Multi-Agente** para proporcionar 
        evaluaciones de triaje médico rápidas y precisas.
        """
    )
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <h3>🤖 Agentes de IA</h3>
                <p>Sistema multi-agente con LangGraph que coordina la evaluación médica</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <h3>⚡ Evaluación Rápida</h3>
                <p>Análisis de síntomas y asignación de prioridad en segundos</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <h3>📊 Historial Completo</h3>
                <p>Acceso al historial médico y consultas previas del paciente</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    
    # System architecture
    st.subheader("🏗️ Arquitectura del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            **Stack Tecnológico:**
            - 🐍 Python 3.11+
            - ⚡ FastAPI
            - 🦜 LangChain & LangGraph
            - 🤖 AWS Bedrock (Claude)
            - 🗄️ DynamoDB
            - 📊 Streamlit
            """
        )
    
    with col2:
        st.markdown(
            """
            **Agentes Implementados:**
            - 🩺 **Triage Agent**: Evaluación de síntomas
            - 📋 **History Agent**: Consulta de historial
            - 🎯 **Coordinator Agent**: Orquestación con LangGraph
            - 💊 **Recommendation Agent**: Sugerencias médicas
            """
        )
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Acciones Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Nuevo Paciente", use_container_width=True):
            st.info("Ir a 'Gestión de Pacientes' para registrar un nuevo paciente")
    
    with col2:
        if st.button("🩺 Nueva Evaluación", use_container_width=True):
            st.info("Ir a 'Evaluación de Triaje' para iniciar una evaluación")
    
    with col3:
        if st.button("📋 Ver Consultas", use_container_width=True):
            st.info("Ir a 'Historial de Consultas' para ver el historial")
    
    st.markdown("---")
    
    # System status
    st.subheader("📊 Estado del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Estado API", "🟢 Activo", "")
    
    with col2:
        st.metric("AWS Bedrock", "🟢 Conectado", "")
    
    with col3:
        st.metric("DynamoDB", "🟢 Disponible", "")
    
    with col4:
        st.metric("Agentes IA", "🟢 Operativos", "")
    
    # Footer info
    st.markdown("---")
    st.info(
        f"""
        **Información del Sistema**  
        Versión: 1.0.0 | Ambiente: Desarrollo | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
    )
