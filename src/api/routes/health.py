"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime
from src.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Add checks for dependencies (DynamoDB, Bedrock, etc.)
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }
