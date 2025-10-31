# Project Rename: wsg_mcp → wsg_courses_mcp

**Date:** November 1, 2025  
**Status:** ✅ Complete

## Overview
The project has been renamed from `wsg_mcp` to `wsg_courses_mcp` to better reflect its purpose as an MCP server specifically for WSG course data.

## What Changed

### Service Names
- **Old:** `wsg-mcp-server`
- **New:** `wsg-courses-mcp-server`

### Conda Environments
- **Old:** `wsg-mcp`, `wsg-mcp-dev`
- **New:** `wsg-courses-mcp`, `wsg-courses-mcp-dev`

### Docker Services
- **Old:** `wsg-mcp` container → `wsg-mcp-server`
- **New:** `wsg-courses-mcp` container → `wsg-courses-mcp-server`

### Cloud Run Service
- **Old:** `wsg-mcp-server`
- **New:** `wsg-courses-mcp-server`

## Files Updated

### Configuration Files
- ✅ `main.py` - Health check service name
- ✅ `docker-compose.yml` - Service and container names
- ✅ `environment.yml` - Conda environment name
- ✅ `environment-dev.yml` - Dev environment name
- ✅ `.env` - K_SERVICE variable
- ✅ `.env.example` - K_SERVICE variable

### Scripts
- ✅ `start.bat` - Conda environment activation
- ✅ `start.ps1` - Conda environment check and activation
- ✅ `start_server.py` - Conda run command
- ✅ `test_setup.py` - Environment instructions

### Tests
- ✅ `tests/test_integration_mcp.py` - Service name assertion

### Documentation
- ✅ `README_PRODUCTION.md` - All references
- ✅ `CONDA_SETUP.md` - Environment names

### Still Using Old Names (Workspace Level)
- ⚠️ Folder name: `wsg_mcp` (can be renamed manually if desired)
- ⚠️ Git repository name (if applicable)

## Migration Steps for Users

### If You Have an Existing Installation:

**Option 1: Create New Environment (Recommended)**
```powershell
# Create new environment with new name
conda create -n wsg-courses-mcp-dev --clone wsg-mcp-dev

# Activate new environment
conda activate wsg-courses-mcp-dev

# Verify it works
python test_setup.py

# Remove old environment (optional)
conda env remove -n wsg-mcp-dev
```

**Option 2: Rename Existing Environment**
```powershell
# Create clone with new name
conda create -n wsg-courses-mcp-dev --clone wsg-mcp-dev

# Remove old environment
conda env remove -n wsg-mcp-dev
```

### Update Docker Containers
```powershell
# Stop old containers
docker-compose down

# Rebuild with new names
docker-compose build

# Start new containers
docker-compose up -d
```

### Update Cloud Run Deployment
```powershell
# Build with new name
gcloud builds submit --tag gcr.io/job-rec-repo/wsg-courses-mcp-server

# Deploy with new name
gcloud run deploy wsg-courses-mcp-server \
  --image gcr.io/job-rec-repo/wsg-courses-mcp-server \
  --region us-central1

# Optional: Delete old service
gcloud run services delete wsg-mcp-server --region us-central1
```

## Current Deployment

### ✅ New Service (Active)
- **Service Name:** wsg-courses-mcp-server
- **URL:** https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app
- **Status:** ✅ Operational
- **Region:** us-central1
- **Project:** job-rec-repo

### 🔄 Old Service (Deprecated)
- **Service Name:** wsg-mcp-server
- **URL:** https://wsg-mcp-server-236255620233.us-central1.run.app
- **Status:** Can be deleted

To remove old service:
```powershell
gcloud run services delete wsg-mcp-server --region us-central1
```

## Notes
- All code references have been updated
- Health check now returns `"service": "wsg-courses-mcp-server"`
- No breaking changes to API endpoints or functionality
- Only naming/branding changes
