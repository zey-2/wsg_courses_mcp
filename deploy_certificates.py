"""Deploy certificates to existing WSG MCP Cloud Run service."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and handle output."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()
    
    result = subprocess.run(cmd, shell=True, text=True)
    
    if result.returncode != 0 and check:
        print(f"\n❌ FAILED: {description}")
        return False
    elif result.returncode == 0:
        print(f"\n✅ SUCCESS: {description}")
    else:
        print(f"\n⚠️  WARNING: {description} (non-critical)")
    
    return True


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("Checking prerequisites...")
    
    # Check gcloud
    result = subprocess.run("gcloud --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("❌ ERROR: gcloud CLI not found")
        return False
    print("✅ gcloud CLI found")
    
    # Check certificates exist
    cert_path = Path("certificates/cert.pem")
    key_path = Path("certificates/key.pem")
    
    if not cert_path.exists():
        print(f"❌ ERROR: Certificate not found at {cert_path}")
        return False
    print("✅ Certificate file found")
    
    if not key_path.exists():
        print(f"❌ ERROR: Private key not found at {key_path}")
        return False
    print("✅ Private key file found")
    
    # Check gcloud authentication
    result = subprocess.run("gcloud config get-value account", 
                          shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("❌ ERROR: No active gcloud authentication")
        print("Run: gcloud auth login")
        return False
    
    active_account = result.stdout.strip()
    print(f"✅ Authenticated as: {active_account}")
    
    # Check project is set
    result = subprocess.run("gcloud config get-value project", 
                          shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("❌ ERROR: No active gcloud project")
        print("Run: gcloud config set project PROJECT_ID")
        return False
    
    project_id = result.stdout.strip()
    print(f"✅ Active project: {project_id}")
    
    return True


def update_secrets():
    """Update certificate secrets in Secret Manager."""
    print("\n" + "="*60)
    print("UPDATING CERTIFICATE SECRETS")
    print("="*60)
    
    # Update certificate secret
    success = run_command(
        "gcloud secrets versions add wsg-cert --data-file=certificates/cert.pem",
        "Updating WSG certificate secret"
    )
    if not success:
        return False
    
    # Update private key secret
    success = run_command(
        "gcloud secrets versions add wsg-key --data-file=certificates/key.pem",
        "Updating WSG private key secret"
    )
    if not success:
        return False
    
    return True


def deploy_service():
    """Deploy the service with certificates."""
    print("\n" + "="*60)
    print("DEPLOYING SERVICE WITH CERTIFICATES")
    print("="*60)
    
    # Get current project info
    result = subprocess.run("gcloud config get-value project", 
                          shell=True, capture_output=True, text=True)
    project_id = result.stdout.strip()
    
    service_name = "wsg-courses-mcp-server"
    region = "us-central1"
    image_url = f"gcr.io/{project_id}/{service_name}"
    
    print(f"Project: {project_id}")
    print(f"Service: {service_name}")
    print(f"Region: {region}")
    
    # Build and submit new image
    success = run_command(
        f"gcloud builds submit --tag {image_url}",
        "Building updated container image"
    )
    if not success:
        return False
    
    # Deploy service with secrets
    deploy_cmd = f"""gcloud run deploy {service_name} --image {image_url} --platform managed --region {region} --allow-unauthenticated --memory 1Gi --cpu 1 --timeout 300 --max-instances 10 --port 8080 --set-env-vars ENVIRONMENT=production,LOG_LEVEL=INFO,BASE_URL=https://api.ssg-wsg.sg,CERT_PATH=/app/secrets/cert.pem,KEY_PATH=/app/secrets/key.pem --update-secrets /app/secrets/cert.pem=wsg-cert:latest,/app/secrets/key.pem=wsg-key:latest"""
    
    success = run_command(deploy_cmd, "Deploying service with certificates")
    if not success:
        return False
    
    return True


def test_deployment():
    """Test the deployed service with certificates."""
    print("\n" + "="*60)
    print("TESTING DEPLOYMENT")
    print("="*60)
    
    service_url = "https://wsg-courses-mcp-server-236255620233.us-central1.run.app"
    
    try:
        import httpx
        import asyncio
        
        async def run_tests():
            async with httpx.AsyncClient(timeout=30.0) as client:
                
                # Test health
                print("\n🔍 Testing health endpoint...")
                try:
                    response = await client.get(f"{service_url}/health")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Health: {data.get('status')} (Environment: {data.get('environment')})")
                    else:
                        print(f"❌ Health check failed: {response.status_code}")
                        return False
                except Exception as e:
                    print(f"❌ Health check error: {e}")
                    return False
                
                # Test configuration
                print("\n🔍 Testing certificate configuration...")
                try:
                    response = await client.get(f"{service_url}/debug/config")
                    if response.status_code == 200:
                        data = response.json()
                        cert_exists = data.get('cert_exists', False)
                        key_exists = data.get('key_exists', False)
                        
                        if cert_exists and key_exists:
                            print("✅ Certificates: Successfully deployed and accessible")
                        else:
                            print(f"❌ Certificates: cert_exists={cert_exists}, key_exists={key_exists}")
                            return False
                    else:
                        print(f"❌ Config check failed: {response.status_code}")
                        return False
                except Exception as e:
                    print(f"❌ Config check error: {e}")
                    return False
                
                # Test WSG API call
                print("\n🔍 Testing WSG API integration...")
                try:
                    response = await client.get(f"{service_url}/courses/tags")
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and len(data.get('data', [])) > 0:
                            print(f"✅ WSG API: Successfully retrieved {len(data['data'])} tags")
                            print(f"   Sample tag: {data['data'][0].get('text', 'N/A')}")
                        else:
                            print("❌ WSG API: No data returned")
                            return False
                    else:
                        print(f"❌ WSG API test failed: {response.status_code}")
                        response_text = await response.aread()
                        print(f"   Response: {response_text[:200]}...")
                        return False
                except Exception as e:
                    print(f"❌ WSG API test error: {e}")
                    return False
                
                # Test course search
                print("\n🔍 Testing course search...")
                try:
                    response = await client.get(f"{service_url}/courses/directory?keyword=python&page_size=3")
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and len(data.get('data', [])) > 0:
                            print(f"✅ Course Search: Found {len(data['data'])} Python courses")
                            print(f"   Sample: {data['data'][0].get('title', 'N/A')[:60]}...")
                        else:
                            print("❌ Course Search: No courses found")
                            return False
                    else:
                        print(f"❌ Course search failed: {response.status_code}")
                        return False
                except Exception as e:
                    print(f"❌ Course search error: {e}")
                    return False
                
                return True
        
        return asyncio.run(run_tests())
        
    except ImportError:
        print("❌ httpx not available for testing")
        print("Install with: pip install httpx")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main deployment function."""
    print("\n" + "="*60)
    print("WSG MCP SERVER - CERTIFICATE DEPLOYMENT")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please resolve issues above.")
        return False
    
    # Confirm deployment
    print(f"\nThis will:")
    print(f"  ✅ Update certificate secrets in Secret Manager")
    print(f"  ✅ Rebuild and redeploy the WSG MCP service")
    print(f"  ✅ Test the deployment with WSG API calls")
    
    confirm = input("\nContinue with certificate deployment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Certificate deployment cancelled")
        return False
    
    # Update secrets
    if not update_secrets():
        print("\n❌ Failed to update secrets")
        return False
    
    # Deploy service
    if not deploy_service():
        print("\n❌ Failed to deploy service")
        return False
    
    # Test deployment
    print("\nWaiting for service to be ready...")
    import time
    time.sleep(10)  # Give service time to start
    
    if test_deployment():
        print("\n" + "="*60)
        print("🎉 CERTIFICATE DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print(f"\n✅ WSG MCP Server with certificates is now live!")
        print(f"   Service URL: https://wsg-courses-mcp-server-236255620233.us-central1.run.app")
        print(f"   Health Check: https://wsg-courses-mcp-server-236255620233.us-central1.run.app/health")
        print(f"   API Docs: https://wsg-courses-mcp-server-236255620233.us-central1.run.app/docs")
        print(f"   MCP Endpoint: https://wsg-courses-mcp-server-236255620233.us-central1.run.app/mcp")
        print(f"\n🚀 The server can now access WSG API with certificates!")
        return True
    else:
        print("\n" + "="*60)
        print("⚠️  DEPLOYMENT COMPLETED BUT TESTS FAILED")
        print("="*60)
        print("The service was deployed but some tests failed.")
        print("Check the service logs for more details:")
        print("gcloud run services logs tail wsg-courses-mcp-server --region us-central1")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ DEPLOYMENT ERROR: {e}")
        sys.exit(1)