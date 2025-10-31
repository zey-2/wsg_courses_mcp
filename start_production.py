"""Production server startup script."""

import os
import sys
from pathlib import Path

# Ensure we're in the right directory
os.chdir(Path(__file__).parent)

# Verify certificates exist
cert_path = os.getenv("WSG_CERT_PATH", "certificates/cert.pem")
key_path = os.getenv("WSG_KEY_PATH", "certificates/key.pem")

cert_path = cert_path if os.path.isabs(cert_path) else os.path.join(os.getcwd(), cert_path)
key_path = key_path if os.path.isabs(key_path) else os.path.join(os.getcwd(), key_path)

if not os.path.exists(cert_path):
    print(f"❌ ERROR: Certificate not found at {cert_path}")
    sys.exit(1)

if not os.path.exists(key_path):
    print(f"❌ ERROR: Private key not found at {key_path}")
    sys.exit(1)

print("✅ Certificates verified")
print(f"   Cert: {cert_path}")
print(f"   Key:  {key_path}")

# Import and verify app
try:
    from main import app
    print("✅ Application imported successfully")
except Exception as e:
    print(f"❌ ERROR: Failed to import application: {e}")
    sys.exit(1)

# Start server
import uvicorn

port = int(os.getenv("PORT", "8080"))
host = os.getenv("HOST", "0.0.0.0")
workers = int(os.getenv("WORKERS", "4"))

print(f"\n🚀 Starting production server...")
print(f"   Host: {host}")
print(f"   Port: {port}")
print(f"   Workers: {workers}")
print(f"   Environment: {os.getenv('ENVIRONMENT', 'production')}")
print(f"\n   Health check: http://{host}:{port}/health")
print(f"   API docs: http://{host}:{port}/docs")
print(f"\n")

uvicorn.run(
    "main:app",
    host=host,
    port=port,
    workers=workers,
    log_level=os.getenv("LOG_LEVEL", "info").lower(),
    access_log=True,
    proxy_headers=True,
    forwarded_allow_ips="*"
)
