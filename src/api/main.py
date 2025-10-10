"""FastAPI main application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import get_settings
from src.api.routes import patients, triage, consultations, health
from src.services.dynamodb_service import DynamoDBService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application."""
    # Startup
    logger.info("Starting Swiss Medical Triage System API")
    settings = get_settings()
    
    # Initialize DynamoDB tables
    try:
        db_service = DynamoDBService()
        db_service.create_tables()
        logger.info("DynamoDB tables initialized")
    except Exception as e:
        logger.error(f"Error initializing DynamoDB: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Swiss Medical Triage System API")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de Triaje Médico Inteligente con Agentes de IA",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(triage.router, prefix="/api/v1/triage", tags=["Triage"])
app.include_router(consultations.router, prefix="/api/v1/consultations", tags=["Consultations"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Swiss Medical Triage System API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )
