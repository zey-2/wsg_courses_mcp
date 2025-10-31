"""Deploy to Google Cloud Run."""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and print output."""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}")
    print()
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ FAILED: {description}")
        return False
    
    print(f"\n✅ SUCCESS: {description}")
    return True


def deploy_to_cloud_run():
    """Deploy the application to Google Cloud Run."""
    
    print("\n" + "="*70)
    print("GOOGLE CLOUD RUN DEPLOYMENT")
    print("="*70)
    
    # Check if gcloud is installed
    print("\nChecking prerequisites...")
    result = subprocess.run("gcloud --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("❌ ERROR: gcloud CLI not found")
        print("Install from: https://cloud.google.com/sdk/docs/install")
        return False
    
    print("✅ gcloud CLI found")
    
    # Get project ID
    print("\n" + "="*70)
    print("CONFIGURATION")
    print("="*70)
    
    project_id = input("\nEnter your Google Cloud Project ID: ").strip()
    if not project_id:
        print("❌ ERROR: Project ID required")
        return False
    
    region = input("Enter deployment region [us-central1]: ").strip() or "us-central1"
    service_name = input("Enter service name [wsg-mcp-server]: ").strip() or "wsg-mcp-server"
    
    print(f"\nConfiguration:")
    print(f"  Project: {project_id}")
    print(f"  Region: {region}")
    print(f"  Service: {service_name}")
    
    confirm = input("\nContinue with deployment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deployment cancelled")
        return False
    
    # Set project
    if not run_command(
        f"gcloud config set project {project_id}",
        "Setting active project"
    ):
        return False
    
    # Enable required APIs
    print("\nEnabling required APIs...")
    apis = [
        "run.googleapis.com",
        "cloudbuild.googleapis.com",
        "secretmanager.googleapis.com"
    ]
    
    for api in apis:
        if not run_command(
            f"gcloud services enable {api}",
            f"Enabling {api}"
        ):
            print(f"⚠️  Warning: Failed to enable {api} (may already be enabled)")
    
    # Create secrets for certificates
    print("\nCreating secrets for certificates...")
    
    if not run_command(
        f"gcloud secrets create wsg-cert --data-file=certificates/cert.pem --replication-policy=automatic",
        "Creating certificate secret"
    ):
        print("⚠️  Secret may already exist, continuing...")
    
    if not run_command(
        f"gcloud secrets create wsg-key --data-file=certificates/key.pem --replication-policy=automatic",
        "Creating private key secret"
    ):
        print("⚠️  Secret may already exist, continuing...")
    
    # Build and submit
    image_url = f"gcr.io/{project_id}/{service_name}"
    
    if not run_command(
        f"gcloud builds submit --tag {image_url}",
        "Building container image"
    ):
        return False
    
    # Deploy to Cloud Run
    deploy_cmd = f"""gcloud run deploy {service_name} \
        --image {image_url} \
        --platform managed \
        --region {region} \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1 \
        --timeout 60 \
        --max-instances 10 \
        --set-env-vars ENVIRONMENT=production,LOG_LEVEL=INFO,WSG_BASE_URL=https://api.ssg-wsg.sg \
        --update-secrets WSG_CERT_PATH=wsg-cert:latest,WSG_KEY_PATH=wsg-key:latest"""
    
    if not run_command(deploy_cmd, "Deploying to Cloud Run"):
        return False
    
    # Get service URL
    print("\n" + "="*70)
    print("DEPLOYMENT COMPLETE!")
    print("="*70)
    
    url_result = subprocess.run(
        f"gcloud run services describe {service_name} --region {region} --format 'value(status.url)'",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if url_result.returncode == 0:
        service_url = url_result.stdout.strip()
        print(f"\n🚀 Service deployed successfully!")
        print(f"\n   Service URL: {service_url}")
        print(f"   Health check: {service_url}/health")
        print(f"   API docs: {service_url}/docs")
        print(f"   MCP endpoint: {service_url}/mcp")
        
        # Test the deployment
        test = input("\nTest the deployment now? (yes/no): ").strip().lower()
        if test == "yes":
            import httpx
            import asyncio
            
            async def test_deployment():
                async with httpx.AsyncClient(timeout=10.0) as client:
                    print("\nTesting endpoints...")
                    
                    try:
                        response = await client.get(f"{service_url}/health")
                        if response.status_code == 200:
                            print("✅ Health check passed")
                        else:
                            print(f"⚠️  Health check returned {response.status_code}")
                    except Exception as e:
                        print(f"❌ Health check failed: {e}")
                    
                    try:
                        response = await client.get(f"{service_url}/courses/tags")
                        if response.status_code == 200:
                            data = response.json()
                            print(f"✅ API test passed - retrieved {len(data.get('data', []))} tags")
                        else:
                            print(f"⚠️  API test returned {response.status_code}")
                    except Exception as e:
                        print(f"❌ API test failed: {e}")
            
            asyncio.run(test_deployment())
    
    print("\n" + "="*70)
    print("Next steps:")
    print(f"1. Monitor logs: gcloud run services logs tail {service_name} --region {region}")
    print(f"2. Update service: gcloud run services update {service_name} --region {region}")
    print(f"3. Delete service: gcloud run services delete {service_name} --region {region}")
    print("="*70)
    
    return True


if __name__ == "__main__":
    try:
        success = deploy_to_cloud_run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
