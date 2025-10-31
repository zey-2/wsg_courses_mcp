"""Tests for error handling and edge cases."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, Mock
import httpx

from main import app


client = TestClient(app)


class TestErrorHandling:
    """Tests for error handling scenarios."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_http_error_404(self, mock_get_client):
        """Test handling of 404 errors from WSG API."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_http_client.get.return_value = mock_response
        
        # Simulate HTTPStatusError
        error = httpx.HTTPStatusError(
            "Not found", 
            request=Mock(), 
            response=mock_response
        )
        mock_response.raise_for_status.side_effect = error
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory/INVALID-REF")
        
        assert response.status_code == 404
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_http_error_500(self, mock_get_client):
        """Test handling of 500 errors from WSG API."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_http_client.get.return_value = mock_response
        
        error = httpx.HTTPStatusError(
            "Server error", 
            request=Mock(), 
            response=mock_response
        )
        mock_response.raise_for_status.side_effect = error
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=test")
        
        assert response.status_code == 500
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_network_timeout(self, mock_get_client):
        """Test handling of network timeout errors."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_http_client.get.side_effect = httpx.TimeoutException("Request timeout")
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=python")
        
        assert response.status_code == 500
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_unexpected_exception(self, mock_get_client):
        """Test handling of unexpected exceptions."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_http_client.get.side_effect = Exception("Unexpected error")
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=python")
        
        assert response.status_code == 500


class TestInputValidation:
    """Tests for input validation."""
    
    def test_invalid_page_size(self):
        """Test validation of page_size parameter."""
        # Too large
        response = client.get("/courses/directory?keyword=python&page_size=1000")
        assert response.status_code == 422
        
        # Too small
        response = client.get("/courses/directory?keyword=python&page_size=0")
        assert response.status_code == 422
    
    def test_invalid_page_number(self):
        """Test validation of page parameter."""
        response = client.get("/courses/directory?keyword=python&page=-1")
        assert response.status_code == 422
    
    def test_missing_required_params(self):
        """Test missing required parameters."""
        response = client.get("/courses/directory")
        assert response.status_code == 422  # Missing keyword
    
    @patch('routers.courses.get_cert_client')
    def test_tagging_search_delta_without_last_update(self, mock_get_client):
        """Test tagging search with DELTA but no last_update_date."""
        response = client.post(
            "/courses/directory/search-by-tagging",
            params={
                "tagging_codes": ["1"],
                "support_end_date": "20250101",
                "retrieve_type": "DELTA"
                # Missing last_update_date
            }
        )
        assert response.status_code == 400


class TestEdgeCases:
    """Tests for edge cases."""
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_empty_search_results(self, mock_get_client):
        """Test handling of empty search results."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "courses": [],
            "totalResults": 0
        }
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=xyzabc123notfound")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []
    
    @patch('routers.courses.get_cert_client')
    @pytest.mark.asyncio
    async def test_special_characters_in_keyword(self, mock_get_client, sample_search_response):
        """Test search with special characters."""
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_search_response
        mock_response.raise_for_status = AsyncMock()
        mock_http_client.get.return_value = mock_response
        mock_get_client.return_value = mock_http_client
        
        response = client.get("/courses/directory?keyword=C%2B%2B")  # C++
        
        assert response.status_code == 200
