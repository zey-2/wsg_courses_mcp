"""Test production deployment locally."""

import subprocess
import time
import httpx
import sys


def test_production_server():
    """Test the production server setup."""
    
    print("=" * 70)
    print("PRODUCTION DEPLOYMENT TEST")
    print("=" * 70)
    
    # Test 1: Certificate verification
    print("\n1. Testing certificate files...")
    try:
        import os
        from pathlib import Path
        
        cert_path = Path("certificates/cert.pem")
        key_path = Path("certificates/key.pem")
        
        assert cert_path.exists(), f"Certificate not found: {cert_path}"
        assert key_path.exists(), f"Key not found: {key_path}"
        assert cert_path.stat().st_size > 0, "Certificate is empty"
        assert key_path.stat().st_size > 0, "Key is empty"
        
        print(f"   ✓ Certificate: {cert_path} ({cert_path.stat().st_size} bytes)")
        print(f"   ✓ Private Key: {key_path} ({key_path.stat().st_size} bytes)")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    # Test 2: Configuration loading
    print("\n2. Testing configuration...")
    try:
        from config import settings
        
        assert settings.cert_path, "Certificate path not configured"
        assert settings.key_path, "Key path not configured"
        assert settings.base_url, "Base URL not configured"
        
        print(f"   ✓ Base URL: {settings.base_url}")
        print(f"   ✓ Environment: {settings.environment}")
        print(f"   ✓ Port: {settings.port}")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    # Test 3: Application import
    print("\n3. Testing application import...")
    try:
        from main import app
        
        print(f"   ✓ FastAPI app: {app.title}")
        print(f"   ✓ Version: {app.version}")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    # Test 4: Dependencies check
    print("\n4. Testing required dependencies...")
    try:
        import fastapi
        import httpx
        import pydantic
        import uvicorn
        import gunicorn
        import mcp
        
        print(f"   ✓ FastAPI: {fastapi.__version__}")
        print(f"   ✓ Uvicorn: {uvicorn.__version__}")
        print(f"   ✓ Gunicorn: {gunicorn.__version__}")
        print(f"   ✓ HTTPX: {httpx.__version__}")
        print(f"   ✓ Pydantic: {pydantic.__version__}")
    except ImportError as e:
        print(f"   ✗ FAILED: Missing dependency - {e}")
        return False
    
    # Test 5: Docker build (optional)
    print("\n5. Checking Docker configuration...")
    try:
        from pathlib import Path
        
        dockerfile = Path("Dockerfile")
        dockercompose = Path("docker-compose.yml")
        dockerignore = Path(".dockerignore")
        
        if dockerfile.exists():
            print(f"   ✓ Dockerfile present")
        if dockercompose.exists():
            print(f"   ✓ docker-compose.yml present")
        if dockerignore.exists():
            print(f"   ✓ .dockerignore present")
    except Exception as e:
        print(f"   ⚠ Warning: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ALL PRODUCTION CHECKS PASSED")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Local test: python start_production.py")
    print("2. Docker test: docker-compose up")
    print("3. Deploy to Cloud Run: See PRODUCTION_DEPLOYMENT.md")
    print()
    
    return True


if __name__ == "__main__":
    success = test_production_server()
    sys.exit(0 if success else 1)
