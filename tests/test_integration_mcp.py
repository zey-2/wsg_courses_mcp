"""Tests for application health and configuration."""

import pytest
from fastapi.testclient import TestClient

from main import app
from config import settings


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""
    
    def test_health_check_success(self):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "wsg-courses-mcp-server"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        assert "environment" in data
    
    def test_health_check_structure(self):
        """Test health endpoint response structure."""
        response = client.get("/health")
        data = response.json()
        
        required_fields = ["status", "service", "version", "timestamp", "environment"]
        for field in required_fields:
            assert field in data


class TestRootEndpoint:
    """Tests for / root endpoint."""
    
    def test_root_success(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "WSG Courses API MCP Server"
        assert data["version"] == "1.0.0"
        assert data["status"] == "operational"
    
    def test_root_endpoints_info(self):
        """Test root endpoint includes endpoints information."""
        response = client.get("/")
        data = response.json()
        
        assert "endpoints" in data
        endpoints = data["endpoints"]
        assert endpoints["docs"] == "/docs"
        assert endpoints["health"] == "/health"
        assert endpoints["mcp"] == "/mcp"


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""
    
    def test_openapi_schema(self):
        """Test OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "WSG Courses API MCP Server"
    
    def test_swagger_ui(self):
        """Test Swagger UI is accessible."""
        response = client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc(self):
        """Test ReDoc is accessible."""
        response = client.get("/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestConfiguration:
    """Tests for application configuration."""
    
    def test_settings_loaded(self):
        """Test settings are properly loaded."""
        assert settings.base_url == "https://api.ssg-wsg.sg"
        assert settings.cert_path is not None
        assert settings.key_path is not None
    
    def test_cors_origins_parsing(self):
        """Test CORS origins parsing."""
        origins = settings.cors_origins_list
        assert isinstance(origins, list)
    
    def test_cloud_run_detection(self):
        """Test Cloud Run detection."""
        is_cloud_run = settings.is_cloud_run
        assert isinstance(is_cloud_run, bool)
