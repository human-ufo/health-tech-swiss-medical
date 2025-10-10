"""Triage agent for medical assessment."""
import logging
import json
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.agents.base_agent import BaseAgent
from src.models.triage import TriageLevel, TriageRequest, TriageResponse
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class TriageAgent(BaseAgent):
    """Agent specialized in medical triage assessment."""

    def __init__(self):
        """Initialize triage agent."""
        super().__init__(temperature=0.3)  # Lower temperature for more consistent medical advice
        self.setup_prompt()

    def setup_prompt(self):
        """Setup the triage prompt template."""
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Eres un asistente médico experto en triaje de emergencias para Swiss Medical Group.
Tu tarea es evaluar los síntomas del paciente y asignar un nivel de prioridad según protocolos médicos estándar.

NIVELES DE TRIAJE:
- CRITICAL (Crítico): Situación que amenaza la vida, requiere atención inmediata
- URGENT (Urgente): Requiere atención en 15-30 minutos
- SEMI_URGENT (Semi-urgente): Requiere atención en 1-2 horas
- NON_URGENT (No urgente): Puede esperar 2-4 horas
- ROUTINE (Rutina): Puede programarse una cita

CRITERIOS DE EVALUACIÓN:
1. Severidad de síntomas (escala 1-10)
2. Duración de los síntomas
3. Signos vitales
4. Condiciones crónicas preexistentes
5. Factores de riesgo

Debes proporcionar:
- Nivel de triaje apropiado
- Puntuación de prioridad (0-100)
- Resumen de evaluación
- Acción recomendada
- Especialidad médica recomendada
- Estudios recomendados
- Factores de riesgo identificados
- Señales de alerta a monitorear
- Tiempo estimado de espera

Responde SIEMPRE en formato JSON válido con esta estructura:
{{
    "triage_level": "critical|urgent|semi_urgent|non_urgent|routine",
    "priority_score": 0-100,
    "assessment_summary": "resumen detallado",
    "recommended_action": "acción inmediata recomendada",
    "recommended_specialty": "especialidad médica",
    "recommended_tests": ["estudio1", "estudio2"],
    "risk_factors": ["factor1", "factor2"],
    "warning_signs": ["señal1", "señal2"],
    "estimated_wait_time": "tiempo estimado",
    "agent_reasoning": "razonamiento del agente"
}}""",
                ),
                ("human", "{input}"),
            ]
        )

    def assess_triage(self, request: TriageRequest, patient_history: Dict[str, Any]) -> TriageResponse:
        """Perform triage assessment."""
        try:
            # Build context
            symptoms_text = "\n".join(
                [
                    f"- {s.name}: Severidad {s.severity}/10, Duración: {s.duration_hours or 'desconocida'} horas"
                    for s in request.symptoms
                ]
            )

            vital_signs_text = ""
            if request.vital_signs:
                vital_signs_text = "\n".join(
                    [f"- {k}: {v}" for k, v in request.vital_signs.items()]
                )

            patient_context = f"""
Historial del paciente:
- Edad: {patient_history.get('age', 'desconocida')} años
- Tipo de sangre: {patient_history.get('blood_type', 'desconocido')}
- Alergias: {', '.join(patient_history.get('allergies', [])) or 'ninguna'}
- Condiciones crónicas: {', '.join(patient_history.get('chronic_conditions', [])) or 'ninguna'}
- Medicamentos actuales: {', '.join(patient_history.get('current_medications', [])) or 'ninguno'}
"""

            input_text = f"""
EVALUACIÓN DE TRIAJE

{patient_context}

SÍNTOMAS ACTUALES:
{symptoms_text}

SIGNOS VITALES:
{vital_signs_text if vital_signs_text else "No proporcionados"}

CONTEXTO ADICIONAL:
{request.additional_context or "Ninguno"}

Por favor, realiza una evaluación completa de triaje y proporciona tu respuesta en formato JSON.
"""

            # Invoke LLM
            prompt = self.prompt_template.format_messages(input=input_text)
            response = self.llm.invoke(prompt)
            
            # Parse response
            response_text = response.content.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)

            # Create TriageResponse
            triage_response = TriageResponse(
                triage_id=f"TRI-{uuid.uuid4().hex[:8].upper()}",
                patient_id=request.patient_id,
                triage_level=TriageLevel(result["triage_level"]),
                priority_score=result["priority_score"],
                assessment_summary=result["assessment_summary"],
                recommended_action=result["recommended_action"],
                recommended_specialty=result.get("recommended_specialty"),
                recommended_tests=result.get("recommended_tests", []),
                risk_factors=result.get("risk_factors", []),
                warning_signs=result.get("warning_signs", []),
                estimated_wait_time=result.get("estimated_wait_time"),
                agent_reasoning=result.get("agent_reasoning"),
                created_at=datetime.utcnow().isoformat(),
            )

            logger.info(
                f"Triage assessment completed for patient {request.patient_id}: {triage_response.triage_level}"
            )
            return triage_response

        except Exception as e:
            logger.error(f"Error in triage assessment: {e}")
            # Return a safe default response
            return TriageResponse(
                triage_id=f"TRI-{uuid.uuid4().hex[:8].upper()}",
                patient_id=request.patient_id,
                triage_level=TriageLevel.URGENT,
                priority_score=50,
                assessment_summary="Error en la evaluación automática. Se requiere evaluación manual.",
                recommended_action="Contactar con personal médico para evaluación manual.",
                agent_reasoning=f"Error del sistema: {str(e)}",
            )
