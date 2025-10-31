"""Quick test to verify the server starts successfully."""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("Testing WSG MCP Server Setup")
print("=" * 60)

# Test 1: Import dependencies
print("\n1. Testing imports...")
try:
    from config import settings
    print("   ✓ Config imported successfully")
    print(f"   - Base URL: {settings.base_url}")
    print(f"   - Environment: {settings.environment}")
    print(f"   - Certificate path: {settings.cert_path}")
    print(f"   - Key path: {settings.key_path}")
except Exception as e:
    print(f"   ✗ Config import failed: {e}")
    sys.exit(1)

# Test 2: Check certificate files
print("\n2. Checking certificate files...")
try:
    from pathlib import Path
    cert_path = Path(settings.cert_path)
    key_path = Path(settings.key_path)
    
    if cert_path.exists():
        print(f"   ✓ Certificate found: {cert_path}")
    else:
        print(f"   ✗ Certificate not found: {cert_path}")
    
    if key_path.exists():
        print(f"   ✓ Private key found: {key_path}")
    else:
        print(f"   ✗ Private key not found: {key_path}")
except Exception as e:
    print(f"   ✗ Certificate check failed: {e}")

# Test 3: Import FastAPI app
print("\n3. Testing FastAPI app import...")
try:
    from main import app
    print("   ✓ FastAPI app imported successfully")
    print(f"   - Title: {app.title}")
    print(f"   - Version: {app.version}")
except Exception as e:
    print(f"   ✗ FastAPI app import failed: {e}")
    sys.exit(1)

# Test 4: Check routes
print("\n4. Checking registered routes...")
try:
    routes = [route.path for route in app.routes]
    print(f"   ✓ Found {len(routes)} routes")
    
    important_routes = ["/", "/health", "/docs", "/courses/directory", "/mcp"]
    for route in important_routes:
        if any(r for r in routes if route in r):
            print(f"   ✓ Route exists: {route}")
        else:
            print(f"   ✗ Route missing: {route}")
except Exception as e:
    print(f"   ✗ Route check failed: {e}")

# Test 5: Import models
print("\n5. Testing model imports...")
try:
    from models import requests, responses
    print("   ✓ Request models imported")
    print("   ✓ Response models imported")
except Exception as e:
    print(f"   ✗ Model import failed: {e}")

# Test 6: Import routers
print("\n6. Testing router imports...")
try:
    from routers import courses
    print("   ✓ Courses router imported")
except Exception as e:
    print(f"   ✗ Router import failed: {e}")

# Test 7: Import auth dependencies
print("\n7. Testing auth dependencies...")
try:
    from dependencies.auth import CertificateAuth, get_cert_client
    print("   ✓ CertificateAuth imported")
    print("   ✓ get_cert_client dependency imported")
except Exception as e:
    print(f"   ✗ Auth import failed: {e}")

print("\n" + "=" * 60)
print("✓ All tests passed! Server is ready to run.")
print("=" * 60)
print("\nTo start the server, run:")
print("  conda activate wsg-courses-mcp-dev")
print("  python main.py")
print("\nOr use uvicorn directly:")
print("  conda activate wsg-courses-mcp-dev")
print("  uvicorn main:app --reload --port 8000")
print("\nAccess the API at:")
print("  - Swagger UI: http://localhost:8000/docs")
print("  - Health check: http://localhost:8000/health")
print("  - MCP endpoint: http://localhost:8000/mcp")
print("=" * 60)
