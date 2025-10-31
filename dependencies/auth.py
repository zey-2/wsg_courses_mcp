"""Certificate-based authentication for WSG API."""

from typing import AsyncGenerator
from pathlib import Path
import httpx
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class CertificateAuth:
    """Certificate-based authentication for WSG API."""
    
    def __init__(self, cert_path: str, key_path: str, base_url: str = "https://api.ssg-wsg.sg"):
        """Initialize certificate authentication.
        
        Args:
            cert_path: Path to certificate file (cert.pem)
            key_path: Path to private key file (key.pem)
            base_url: Base URL for WSG API
        """
        self.cert_path = Path(cert_path)
        self.key_path = Path(key_path)
        self.base_url = base_url
        
        # Verify certificate files exist
        if not self.cert_path.exists():
            raise FileNotFoundError(f"Certificate not found: {self.cert_path}")
        if not self.key_path.exists():
            raise FileNotFoundError(f"Private key not found: {self.key_path}")
        
        self.cert = (str(self.cert_path), str(self.key_path))
        logger.info(f"Certificate authentication initialized with base URL: {self.base_url}")
    
    def get_client(self) -> httpx.AsyncClient:
        """Return configured HTTP client with certificate authentication.
        
        Returns:
            Configured AsyncClient with certificate authentication
        """
        return httpx.AsyncClient(
            cert=self.cert,
            base_url=self.base_url,
            timeout=30.0,
            follow_redirects=True,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )


async def get_cert_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """FastAPI dependency that provides authenticated HTTP client.
    
    Yields:
        Configured HTTP client with certificate authentication
        
    Raises:
        HTTPException: If certificate files are not found or invalid
    """
    try:
        # Import here to avoid circular dependency
        from config import settings
        
        auth = CertificateAuth(
            cert_path=settings.cert_path,
            key_path=settings.key_path,
            base_url=settings.base_url
        )
        
        async with auth.get_client() as client:
            yield client
            
    except FileNotFoundError as e:
        logger.error(f"Certificate file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Certificate configuration error"
        )
