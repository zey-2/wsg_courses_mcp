"""Unit tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import httpx

from main import app


client = TestClient(app)


class TestCategoriesEndpoint:
    """Tests for /courses/categories endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_categories_success(self, mock_get_client, sample_category_data):
        """Test successful category retrieval."""
        # Setup mock
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_category_data
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        # Make request
        response = client.get("/courses/categories?keyword=training")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_categories_empty_keyword(self, mock_get_client):
        """Test category retrieval with empty keyword."""
        response = client.get("/courses/categories?keyword=")
        assert response.status_code == 422  # Validation error


class TestTagsEndpoint:
    """Tests for /courses/tags endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_tags_success(self, mock_get_client, sample_tag_data):
        """Test successful tag retrieval."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_tag_data
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/tags")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCourseSearchEndpoint:
    """Tests for /courses/directory search endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_search_courses_success(self, mock_get_client, sample_search_response):
        """Test successful course search."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_search_response
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=python&page_size=10&page=0")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "meta" in data
        assert data["meta"]["page"] == 0
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_search_courses_keyword_too_short(self, mock_get_client):
        """Test search with keyword less than 3 characters."""
        response = client.get("/courses/directory?keyword=py")
        assert response.status_code == 422  # Validation error
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_search_courses_pagination(self, mock_get_client, sample_search_response):
        """Test course search with pagination."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_search_response
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=python&page_size=5&page=2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page_size"] == 5


class TestAutocompleteEndpoint:
    """Tests for /courses/directory/autocomplete endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_autocomplete_success(self, mock_get_client):
        """Test successful autocomplete."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["Python Programming", "Python for Data Science"]
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory/autocomplete?keyword=python")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], dict)


class TestCourseDetailEndpoint:
    """Tests for /courses/directory/{ref_number} endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_course_details_success(self, mock_get_client, sample_course_data):
        """Test successful course detail retrieval."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_course_data
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory/TGS-2020500330")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["referenceNumber"] == "TGS-2020500330"


class TestPopularCoursesEndpoint:
    """Tests for /courses/directory/popular endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_popular_courses_success(self, mock_get_client, sample_search_response):
        """Test successful popular courses retrieval."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_search_response
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory/popular?page_size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestFeaturedCoursesEndpoint:
    """Tests for /courses/directory/featured endpoint."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_get_featured_courses_success(self, mock_get_client, sample_search_response):
        """Test successful featured courses retrieval."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_search_response
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory/featured?page_size=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
