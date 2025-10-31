"""Test configuration and shared fixtures."""

import pytest
import httpx
from pathlib import Path
from unittest.mock import AsyncMock, Mock


@pytest.fixture
def mock_cert_client():
    """Mock HTTP client with certificate authentication."""
    client = AsyncMock(spec=httpx.AsyncClient)
    client.base_url = "https://api.ssg-wsg.sg"
    return client


@pytest.fixture
def sample_course_data():
    """Sample course data for testing."""
    return {
        "referenceNumber": "TGS-2020500330",
        "title": "Python Programming for Data Science",
        "description": "Learn Python programming for data analysis",
        "category": "Information and Communications Technology",
        "subCategory": "Data Analytics",
        "provider": {
            "name": "Training Provider Ltd",
            "uen": "123456789A",
            "code": "TP001"
        },
        "courseFee": 1200.00,
        "duration": "40 hours",
        "durationHours": 40.0,
        "trainingMode": "Classroom",
        "tags": ["SkillsFuture Credit", "PSEA"],
        "url": "https://example.com/course"
    }


@pytest.fixture
def sample_category_data():
    """Sample category data for testing."""
    return [
        {
            "id": "1",
            "name": "Information Technology",
            "description": "IT courses"
        },
        {
            "id": "2",
            "name": "Business Management",
            "description": "Management courses"
        }
    ]


@pytest.fixture
def sample_tag_data():
    """Sample tag data for testing."""
    return [
        {
            "code": "SFC",
            "name": "SkillsFuture Credit",
            "description": "Eligible for SkillsFuture Credit"
        },
        {
            "code": "PSEA",
            "name": "PSEA",
            "description": "Post-Secondary Education Account"
        }
    ]


@pytest.fixture
def sample_search_response():
    """Sample search response with pagination."""
    return {
        "courses": [
            {
                "referenceNumber": "TGS-001",
                "title": "Python Basics",
                "provider": {"name": "Provider A"}
            },
            {
                "referenceNumber": "TGS-002",
                "title": "Advanced Python",
                "provider": {"name": "Provider B"}
            }
        ],
        "totalResults": 25,
        "page": 0,
        "pageSize": 10
    }


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Mock()
    settings.base_url = "https://api.ssg-wsg.sg"
    settings.cert_path = "certificates/cert.pem"
    settings.key_path = "certificates/key.pem"
    settings.environment = "testing"
    settings.log_level = "INFO"
    return settings
