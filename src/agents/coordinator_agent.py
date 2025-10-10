"""Coordinator agent using LangGraph for multi-agent orchestration."""
import logging
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
from src.agents.base_agent import BaseAgent
from src.agents.triage_agent import TriageAgent
from src.models.triage import TriageRequest, TriageResponse
from src.services.patient_service import PatientService
from src.services.dynamodb_service import DynamoDBService
from src.config import get_settings

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for the agent graph."""

    messages: Annotated[Sequence[BaseMessage], operator.add]
    triage_request: TriageRequest
    patient_history: dict
    triage_result: TriageResponse
    next_action: str


class CoordinatorAgent:
    """Coordinator agent that orchestrates multiple specialized agents using LangGraph."""

    def __init__(self):
        """Initialize coordinator agent."""
        self.settings = get_settings()
        self.patient_service = PatientService()
        self.triage_agent = TriageAgent()
        self.db_service = DynamoDBService()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("fetch_patient_history", self._fetch_patient_history)
        workflow.add_node("perform_triage", self._perform_triage)
        workflow.add_node("save_results", self._save_results)

        # Define edges
        workflow.set_entry_point("fetch_patient_history")
        workflow.add_edge("fetch_patient_history", "perform_triage")
        workflow.add_edge("perform_triage", "save_results")
        workflow.add_edge("save_results", END)

        return workflow.compile()

    def _fetch_patient_history(self, state: AgentState) -> AgentState:
        """Node: Fetch patient medical history."""
        logger.info(f"Fetching history for patient {state['triage_request'].patient_id}")

        try:
            patient_history = self.patient_service.get_patient_medical_history(
                state["triage_request"].patient_id
            )

            if not patient_history:
                # Create a default history if patient not found
                patient_history = {
                    "patient_id": state["triage_request"].patient_id,
                    "name": "Paciente Desconocido",
                    "age": 0,
                    "allergies": [],
                    "chronic_conditions": [],
                    "current_medications": [],
                }
                logger.warning(f"Patient {state['triage_request'].patient_id} not found, using defaults")

            state["patient_history"] = patient_history
            state["messages"].append(
                AIMessage(content=f"Historial del paciente recuperado: {patient_history.get('name')}")
            )

        except Exception as e:
            logger.error(f"Error fetching patient history: {e}")
            state["patient_history"] = {}
            state["messages"].append(AIMessage(content=f"Error al recuperar historial: {str(e)}"))

        return state

    def _perform_triage(self, state: AgentState) -> AgentState:
        """Node: Perform triage assessment."""
        logger.info("Performing triage assessment")

        try:
            triage_result = self.triage_agent.assess_triage(
                state["triage_request"], state["patient_history"]
            )

            state["triage_result"] = triage_result
            state["messages"].append(
                AIMessage(
                    content=f"Triaje completado: Nivel {triage_result.triage_level.value}, Prioridad {triage_result.priority_score}"
                )
            )

        except Exception as e:
            logger.error(f"Error performing triage: {e}")
            state["messages"].append(AIMessage(content=f"Error en triaje: {str(e)}"))

        return state

    def _save_results(self, state: AgentState) -> AgentState:
        """Node: Save triage results to database."""
        logger.info("Saving triage results")

        try:
            triage_data = state["triage_result"].model_dump()
            success = self.db_service.put_item(
                self.settings.dynamodb_triage_table, triage_data
            )

            if success:
                state["messages"].append(
                    AIMessage(content=f"Resultados guardados: {state['triage_result'].triage_id}")
                )
            else:
                state["messages"].append(AIMessage(content="Error al guardar resultados"))

        except Exception as e:
            logger.error(f"Error saving results: {e}")
            state["messages"].append(AIMessage(content=f"Error al guardar: {str(e)}"))

        return state

    def process_triage(self, triage_request: TriageRequest) -> TriageResponse:
        """Process a triage request through the agent graph."""
        logger.info(f"Processing triage request for patient {triage_request.patient_id}")

        # Initialize state
        initial_state = AgentState(
            messages=[HumanMessage(content="Iniciar proceso de triaje")],
            triage_request=triage_request,
            patient_history={},
            triage_result=None,
            next_action="",
        )

        # Execute graph
        final_state = self.graph.invoke(initial_state)

        logger.info("Triage process completed")
        return final_state["triage_result"]

    def get_workflow_visualization(self) -> str:
        """Get a text representation of the workflow."""
        return """
        Flujo de Trabajo del Sistema de Triaje:
        
        1. [INICIO] → Recibir solicitud de triaje
        2. [fetch_patient_history] → Recuperar historial médico del paciente
        3. [perform_triage] → Evaluar síntomas y asignar prioridad
        4. [save_results] → Guardar resultados en DynamoDB
        5. [FIN] → Retornar resultado de triaje
        
        Agentes involucrados:
        - TriageAgent: Especializado en evaluación médica
        - PatientService: Gestión de datos del paciente
        - DynamoDBService: Persistencia de datos
        """
