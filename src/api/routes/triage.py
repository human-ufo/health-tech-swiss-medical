"""Triage endpoints."""
import logging
from fastapi import APIRouter, HTTPException
from src.models.triage import TriageRequest, TriageResponse
from src.agents.coordinator_agent import CoordinatorAgent

logger = logging.getLogger(__name__)
router = APIRouter()
coordinator = CoordinatorAgent()


@router.post("/assess", response_model=TriageResponse)
async def assess_triage(request: TriageRequest):
    """Perform triage assessment using AI agents."""
    try:
        logger.info(f"Received triage request for patient {request.patient_id}")
        result = coordinator.process_triage(request)
        return result
    except Exception as e:
        logger.error(f"Error in triage assessment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing triage: {str(e)}")


@router.get("/workflow")
async def get_workflow():
    """Get workflow visualization."""
    return {
        "workflow": coordinator.get_workflow_visualization(),
        "description": "Multi-agent workflow using LangGraph",
    }
