"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    base_url: str = "https://api.ssg-wsg.sg"
    
    # Certificate paths (will be made absolute if relative)
    cert_path: str = "certificates/cert.pem"
    key_path: str = "certificates/key.pem"
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Environment
    environment: str = "development"
    
    # Logging
    log_level: str = "INFO"
    
    # CORS origins (comma-separated string or list)
    cors_origins: Optional[str] = None
    
    # Cloud Run detection
    k_service: Optional[str] = None  # Cloud Run service name
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    @property
    def is_cloud_run(self) -> bool:
        """Check if running on Google Cloud Run."""
        return self.k_service is not None
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list."""
        if not self.cors_origins:
            return []
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    def model_post_init(self, __context) -> None:
        """Convert relative certificate paths to absolute paths or handle Cloud Run secrets."""
        from pathlib import Path
        import os
        
        # Check if secrets are provided as environment variables (Cloud Run)
        wsg_cert = os.getenv("WSG_CERT_PATH")
        wsg_key = os.getenv("WSG_KEY_PATH")
        
        if wsg_cert and wsg_key:
            # Secrets are in environment variables, write them to files
            cert_dir = Path("/tmp/certificates")
            cert_dir.mkdir(exist_ok=True, parents=True)
            
            cert_file = cert_dir / "cert.pem"
            key_file = cert_dir / "key.pem"
            
            cert_file.write_text(wsg_cert)
            key_file.write_text(wsg_key)
            
            self.cert_path = str(cert_file)
            self.key_path = str(key_file)
        else:
            # Local file paths - convert to Path objects
            cert = Path(self.cert_path)
            key = Path(self.key_path)
            
            # If relative, make them absolute relative to the project root
            if not cert.is_absolute():
                project_root = Path(__file__).parent
                self.cert_path = str(project_root / cert)
            
            if not key.is_absolute():
                project_root = Path(__file__).parent
                self.key_path = str(project_root / key)


# Singleton settings instance
settings = Settings()
