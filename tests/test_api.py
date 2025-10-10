"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from src.api.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_readiness_check(self):
        """Test readiness check endpoint."""
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"


class TestPatientEndpoints:
    """Test patient endpoints."""

    @patch('src.api.routes.patients.patient_service')
    def test_create_patient(self, mock_service):
        """Test create patient endpoint."""
        # Setup mock
        mock_patient = Mock()
        mock_patient.model_dump.return_value = {
            "patient_id": "PAT-001",
            "first_name": "Juan",
            "last_name": "Pérez",
            "date_of_birth": "1985-05-15",
            "gender": "male",
            "phone": "+541145678900",
            "allergies": [],
            "chronic_conditions": [],
            "current_medications": [],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "is_active": True,
        }
        mock_service.create_patient.return_value = mock_patient

        # Make request
        response = client.post(
            "/api/v1/patients/",
            json={
                "first_name": "Juan",
                "last_name": "Pérez",
                "date_of_birth": "1985-05-15",
                "gender": "male",
                "phone": "+541145678900",
            },
        )

        # Assertions
        assert response.status_code == 201


class TestTriageEndpoints:
    """Test triage endpoints."""

    def test_get_workflow(self):
        """Test get workflow endpoint."""
        response = client.get("/api/v1/triage/workflow")
        assert response.status_code == 200
        data = response.json()
        assert "workflow" in data
        assert "description" in data
