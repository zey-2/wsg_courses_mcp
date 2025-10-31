# 🚀 WSG Courses MCP Server - Production Ready

## Status: ✅ OPERATIONAL

**Current Version:** 1.0.0  
**Service Name:** wsg-courses-mcp-server  
**Deployed:** November 1, 2025  
**Cloud Run URL:** https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app  
**Test Coverage:** 25/35 tests passing (71%)  
**Endpoints:** 10/10 working  

---

## Quick Start

### Production Deployment

**Option 1: Local Production Server**
```powershell
python start_production.py
```

**Option 2: Docker**
```powershell
docker-compose up -d
```

**Option 3: Google Cloud Run** (Recommended)
```powershell
python deploy_cloud_run.py
```

### Development Server
```powershell
conda activate wsg-courses-mcp-dev
python main.py
# or
uvicorn main:app --reload
```

---

## Live Service

**Production URL:** https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app

- Health: https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app/health
- API Docs: https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app/docs
- Tags: https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app/courses/tags

---

## Production Files

| File | Purpose |
|------|---------|
| `PRODUCTION_DEPLOYMENT.md` | Complete deployment guide |
| `deploy_cloud_run.py` | Automated Cloud Run deployment |
| `start_production.py` | Production server startup |
| `test_production_ready.py` | Pre-deployment validation |
| `Dockerfile` | Container configuration |
| `docker-compose.yml` | Docker Compose setup |
| `.env.production.example` | Production environment template |

---

## What's Working ✅

### All 10 API Endpoints
1. ✅ `/health` - Health check
2. ✅ `/courses/categories` - Get categories
3. ✅ `/courses/tags` - Get tags  
4. ✅ `/courses/directory` - Search courses
5. ✅ `/courses/directory/autocomplete` - Autocomplete
6. ✅ `/courses/categories/{id}/subCategories` - Subcategories
7. ✅ `/courses/directory/{ref}` - Course details
8. ✅ `/courses/directory/{ref}/related` - Related courses
9. ✅ `/courses/directory/popular` - Popular courses
10. ✅ `/courses/directory/featured` - Featured courses

### Features
- ✅ Certificate-based mTLS authentication
- ✅ Nested API response parsing
- ✅ Pydantic validation
- ✅ Error handling
- ✅ OpenAPI documentation
- ✅ MCP integration
- ✅ CORS support
- ✅ Docker containerization
- ✅ Cloud Run ready

---

## Architecture

```
┌─────────────────┐
│   AI Agents     │
│  (via MCP)      │
└────────┬────────┘
         │
    ┌────▼────┐
    │  /mcp   │
    └────┬────┘
         │
┌────────▼────────────┐
│  WSG MCP Server     │
│  - FastAPI          │
│  - 10 Endpoints     │
│  - Auth Layer       │
└────────┬────────────┘
         │ mTLS
    ┌────▼──────┐
    │  WSG API  │
    │  (Gov SG) │
    └───────────┘
```

---

## Deployment Guide

### Prerequisites
- Python 3.12+
- Valid WSG API certificates
- Docker (optional)
- Google Cloud account (for Cloud Run)

### Environment Setup

1. **Copy environment template**:
```powershell
cp .env.production.example .env.production
```

2. **Update values** in `.env.production`:
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=8080
CORS_ORIGINS=https://yourdomain.com
```

3. **Place certificates** in `certificates/` directory:
   - `cert.pem` (2136 bytes)
   - `key.pem` (3324 bytes)

### Deployment Steps

#### Local Production
```powershell
# Validate setup
python test_production_ready.py

# Start server
python start_production.py
```

#### Docker
```powershell
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### Google Cloud Run
```powershell
# Interactive deployment
python deploy_cloud_run.py

# Or manual deployment
gcloud builds submit --tag gcr.io/job-rec-repo/wsg-courses-mcp-server
gcloud run deploy wsg-courses-mcp-server --image gcr.io/job-rec-repo/wsg-courses-mcp-server --region us-central1

# Current deployment
# Service: wsg-courses-mcp-server
# URL: https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app
```

---

## Testing

### Run All Tests
```powershell
pytest tests/ -v
```

### Test Production Setup
```powershell
python test_production_ready.py
```

### Test Endpoints
```powershell
python test_comprehensive.py
```

### Manual API Testing
```powershell
# Health check
curl http://localhost:8080/health

# Get tags
curl http://localhost:8080/courses/tags

# Search courses
curl "http://localhost:8080/courses/directory?keyword=python&page_size=5"
```

---

## Monitoring

### Health Check
```
GET /health
```
Returns:
```json
{
  "status": "healthy",
  "service": "wsg-courses-mcp-server",
  "version": "1.0.0",
  "timestamp": "2025-10-31T15:30:00",
  "environment": "production"
}
```

### Logs

**Local:**
```powershell
# Logs are written to stdout
```

**Docker:**
```powershell
docker-compose logs -f wsg-courses-mcp
```

**Cloud Run:**
```powershell
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=wsg-courses-mcp-server" --limit 50 --format json
```

---

## Security

### Certificate Management
- ✅ Certificates loaded from secure paths
- ✅ Read-only mounts in Docker
- ✅ Google Secret Manager for Cloud Run
- ⚠️ **Never commit certificates to git**
- ⚠️ Rotate certificates before expiration

### API Security
- ✅ mTLS authentication to WSG API
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- 📝 Optional: Add API key authentication

---

## Performance

### Current Configuration
- **Workers**: 4 (multi-process)
- **Timeout**: 120 seconds
- **Memory**: 512 MB (Cloud Run)
- **CPU**: 1 vCPU (Cloud Run)

### Expected Performance
- **Latency**: 200-500ms per request
- **Throughput**: 100-200 req/sec
- **Concurrent Connections**: 100+

### Optimization Options
- Add Redis caching
- Enable response compression
- Implement rate limiting
- Use CDN for static content

---

## Troubleshooting

### Common Issues

**Certificate Errors**
```
Solution: Verify cert.pem and key.pem exist and have correct permissions
```

**Port Already in Use**
```powershell
# Change port in .env
PORT=8081
```

**Connection Refused**
```
Solution: Check server is running and firewall allows connections
```

**404 Errors**
```
Solution: Ensure endpoint paths are correct (e.g., /courses/tags not /api/courses/tags)
```

### Debug Mode

Enable detailed logging:
```bash
LOG_LEVEL=DEBUG
```

---

## Cost Estimates

### Cloud Run (Monthly)
- **Free Tier**: 2M requests, 360k GB-seconds
- **Beyond Free**: ~$0.00002 per request
- **Estimated**: $5-20/month for moderate use

### Optimization
- Set min instances to 0 for cost savings
- Use maximum instances to control costs
- Monitor with billing alerts

---

## Documentation

- `README.md` - This file
- `PRODUCTION_DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_COMPLETE.md` - Implementation summary
- `QUICKSTART.md` - Quick start guide
- `CONDA_SETUP.md` - Conda environment setup
- `/docs` - Interactive API documentation (when server running)

---

## API Documentation

When server is running, access:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI Schema**: http://localhost:8080/openapi.json

---

## Support & Maintenance

### Update Dependencies
```powershell
conda run -n wsg-courses-mcp-dev pip install -r requirements.txt --upgrade
```

### Rebuild Docker Image
```powershell
docker-compose build --no-cache
```

### Update Cloud Run Deployment
```powershell
python deploy_cloud_run.py
```

---

## License

[Your License Here]

---

## Contact

[Your Contact Information]

---

**Status**: Ready for production deployment 🚀
