"""Integration tests for certificate authentication."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from fastapi import HTTPException

from dependencies.auth import CertificateAuth, get_cert_client


class TestCertificateAuth:
    """Tests for CertificateAuth class."""
    
    def test_init_success(self, tmp_path):
        """Test successful CertificateAuth initialization."""
        # Create temporary certificate files
        cert_file = tmp_path / "cert.pem"
        key_file = tmp_path / "key.pem"
        cert_file.write_text("fake cert")
        key_file.write_text("fake key")
        
        auth = CertificateAuth(
            cert_path=str(cert_file),
            key_path=str(key_file)
        )
        
        assert auth.base_url == "https://api.ssg-wsg.sg"
        assert auth.cert_path == cert_file
        assert auth.key_path == key_file
    
    def test_init_missing_cert(self, tmp_path):
        """Test initialization fails with missing certificate."""
        key_file = tmp_path / "key.pem"
        key_file.write_text("fake key")
        
        with pytest.raises(FileNotFoundError, match="Certificate not found"):
            CertificateAuth(
                cert_path=str(tmp_path / "nonexistent.pem"),
                key_path=str(key_file)
            )
    
    def test_init_missing_key(self, tmp_path):
        """Test initialization fails with missing private key."""
        cert_file = tmp_path / "cert.pem"
        cert_file.write_text("fake cert")
        
        with pytest.raises(FileNotFoundError, match="Private key not found"):
            CertificateAuth(
                cert_path=str(cert_file),
                key_path=str(tmp_path / "nonexistent.pem")
            )
    
    def test_get_client(self, tmp_path):
        """Test HTTP client creation."""
        cert_file = tmp_path / "cert.pem"
        key_file = tmp_path / "key.pem"
        cert_file.write_text("fake cert")
        key_file.write_text("fake key")
        
        auth = CertificateAuth(
            cert_path=str(cert_file),
            key_path=str(key_file)
        )
        
        client = auth.get_client()
        assert client.base_url == "https://api.ssg-wsg.sg"


class TestGetCertClient:
    """Tests for get_cert_client dependency."""
    
    @pytest.mark.asyncio
    @patch('dependencies.auth.settings')
    async def test_get_cert_client_success(self, mock_settings, tmp_path):
        """Test successful client dependency injection."""
        # Create temporary certificate files
        cert_file = tmp_path / "cert.pem"
        key_file = tmp_path / "key.pem"
        cert_file.write_text("fake cert")
        key_file.write_text("fake key")
        
        mock_settings.cert_path = str(cert_file)
        mock_settings.key_path = str(key_file)
        mock_settings.base_url = "https://api.ssg-wsg.sg"
        
        # Test the generator
        async for client in get_cert_client():
            assert client is not None
            break
    
    @pytest.mark.asyncio
    @patch('dependencies.auth.settings')
    async def test_get_cert_client_missing_cert(self, mock_settings):
        """Test client dependency with missing certificate."""
        mock_settings.cert_path = "nonexistent.pem"
        mock_settings.key_path = "nonexistent.pem"
        
        with pytest.raises(HTTPException) as exc_info:
            async for _ in get_cert_client():
                pass
        
        assert exc_info.value.status_code == 500
