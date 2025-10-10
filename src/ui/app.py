"""Streamlit UI for Swiss Medical Triage System."""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ui.pages import home, patient_management, triage_assessment, consultation_history

# Page configuration
st.set_page_config(
    page_title="Swiss Medical - Sistema de Triaje",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/200x80/1f77b4/FFFFFF?text=Swiss+Medical", use_container_width=True)
st.sidebar.title("🏥 Navegación")

pages = {
    "🏠 Inicio": home,
    "👤 Gestión de Pacientes": patient_management,
    "🩺 Evaluación de Triaje": triage_assessment,
    "📋 Historial de Consultas": consultation_history,
}

selection = st.sidebar.radio("Ir a:", list(pages.keys()))

# Display selected page
page = pages[selection]
page.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Swiss Medical Group**  
    Sistema de Triaje Inteligente v1.0  
    Powered by AI Agents 🤖
    """
)
