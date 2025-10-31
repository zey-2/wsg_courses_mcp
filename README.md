# WSG Courses API MCP Server

> MCP (Model Context Protocol) server providing AI agents access to Singapore's SkillsFuture WSG Courses API

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

- **10 Course API Endpoints**: Complete access to Singapore's course directory
- **Certificate Authentication**: Secure mTLS authentication with WSG API
- **MCP Protocol Support**: Native integration with AI agents via Model Context Protocol
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Type Safety**: Full Pydantic validation for requests and responses
- **Cloud-Ready**: Docker and Google Cloud Run deployment support
- **Production Grade**: Comprehensive testing, monitoring, and error handling
- **Auto-scaling**: Zero to millions of requests with Cloud Run

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [MCP Tools](#mcp-tools)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security](#security)
- [Contributing](#contributing)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/wsg-courses-mcp.git
cd wsg-courses-mcp

# Create conda environment
conda env create -f environment.yml
conda activate wsg-courses-mcp-dev

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Place your certificates in certificates/
# - certificates/cert.pem
# - certificates/key.pem

# Run the server
python main.py

# Access the API documentation
# Open http://localhost:8000/docs
```

## 📦 Prerequisites

- **Python 3.12+** (or Python 3.10+)
- **WSG API Certificates**: `cert.pem` and `key.pem`
  - Obtain from [SSG-WSG Developer Portal](https://developer.ssg-wsg.gov.sg)
- **Git** for version control
- **Docker** (optional, for containerized deployment)
- **Google Cloud SDK** (optional, for Cloud Run deployment)

### System Requirements

- **Memory**: 512MB minimum, 1GB recommended
- **CPU**: 1 core minimum, 2+ cores recommended
- **Storage**: 100MB for application + dependencies
- **Network**: HTTPS connectivity to api.ssg-wsg.sg

## 🔧 Installation

### Local Development

#### Option 1: Conda (Recommended)

```bash
# Create conda environment
conda env create -f environment-dev.yml

# Activate environment
conda activate wsg-courses-mcp-dev

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

#### Option 2: Virtual Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

### Docker Installation

```bash
# Build image
docker build -t wsg-courses-mcp:latest .

# Run container
docker run -p 8080:8080 `
  -v ${PWD}/certificates:/app/certificates:ro `
  --env-file .env `
  wsg-courses-mcp:latest

# Or use Docker Compose
docker-compose up -d
```

## ⚙️ Configuration

Create `.env` file:

```env
BASE_URL=https://api.ssg-wsg.sg
CERT_PATH=certificates/cert.pem
KEY_PATH=certificates/key.pem
ENVIRONMENT=development
LOG_LEVEL=INFO
PORT=8000
```

### Certificate Setup

1. Obtain certificates from WSG Developer Portal
2. Create `certificates/` directory
3. Copy `cert.pem` and `key.pem` to certificates/
4. Ensure certificates are not committed to version control

## 💻 Usage

### Starting the Server

```bash
# Development (with auto-reload)
python main.py

# Production with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Production with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### API Endpoints

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **MCP Endpoint**: http://localhost:8000/mcp
- **Health Check**: http://localhost:8000/health

### Example Requests

```bash
# Search courses
curl "http://localhost:8000/courses/directory?keyword=python&page_size=5"

# Get categories
curl "http://localhost:8000/courses/categories?keyword=training"

# Get popular courses
curl "http://localhost:8000/courses/directory/popular?page_size=10"

# Get course details
curl "http://localhost:8000/courses/directory/TGS-2020500330"
```

## 📚 API Endpoints

| Endpoint | Method | Description | Version |
|----------|--------|-------------|---------|
| `/courses/categories` | GET | Retrieve course categories | v1 |
| `/courses/tags` | GET | Get course tags | v1 |
| `/courses/directory` | GET | Search courses by keyword | v2.2 |
| `/courses/directory/search-by-tagging` | POST | Search by tagging codes | v2.2 |
| `/courses/directory/autocomplete` | GET | Autocomplete suggestions | v1.2 |
| `/courses/directory/popular` | GET | Popular courses | v1.2 |
| `/courses/directory/featured` | GET | Featured courses | v1.2 |
| `/courses/directory/{refNumber}` | GET | Course details | v1.2 |
| `/courses/directory/{refNumber}/related` | GET | Related courses | v1 |
| `/courses/categories/{id}/subCategories` | GET | Subcategories | v1 |

## 🤖 MCP Tools

AI agents can access these tools through the MCP protocol:

1. **get_course_categories** - Search and browse categories
2. **get_course_tags** - Retrieve available tags
3. **search_courses_by_keyword** - Find courses by keyword
4. **search_courses_by_tagging** - Filter courses by tags
5. **get_course_autocomplete** - Get search suggestions
6. **get_course_subcategories** - Browse subcategories
7. **get_course_details** - Get detailed course information
8. **get_related_courses** - Find similar courses
9. **get_popular_courses** - Discover trending courses
10. **get_featured_courses** - View featured courses

## 🛠️ Development

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8 .

# Run all checks
black . ; isort . ; flake8 . ; mypy .
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific test file
pytest tests/test_unit_endpoints.py -v

# Integration tests
pytest tests/test_integration_mcp.py -v

# View coverage report
# Open htmlcov/index.html in browser
```

## 🚀 Deployment

### Local Deployment

```bash
python main.py
```

### Docker Deployment

```bash
docker-compose up -d
```

### Google Cloud Run

**Current Deployment:** https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/job-rec-repo/wsg-courses-mcp-server

gcloud run deploy wsg-courses-mcp-server \
  --image gcr.io/job-rec-repo/wsg-courses-mcp-server \
  --region us-central1 \
  --allow-unauthenticated \
  --update-secrets="WSG_CERT_PATH=wsg-cert:latest,WSG_KEY_PATH=wsg-key:latest" \
  --set-env-vars="ENVIRONMENT=production,BASE_URL=https://api.ssg-wsg.sg"
```

See the implementation plan for detailed deployment instructions.

## 📊 Monitoring

- **Health Endpoint**: `/health` for uptime monitoring
- **Logs**: Structured logging with timestamps
- **Metrics**: Request count, latency, errors (in Cloud Run)
- **Alerts**: Configure Cloud Monitoring for production

## 🔒 Security

- Never commit certificates to version control (`.pem` files in `.gitignore`)
- Use Secret Manager for cloud deployments
- Certificates are mounted as read-only volumes
- All API requests use HTTPS with mTLS
- Input validation with Pydantic models
- Comprehensive error handling

**Report security issues**: Create a private security advisory on GitHub

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Make changes and add tests
4. Run tests: `pytest tests/ -v`
5. Format code: `black . ; isort .`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing`
8. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Singapore SkillsFuture Singapore (SSG) and Workforce Singapore (WSG)
- FastAPI and fastapi_mcp communities
- Model Context Protocol community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/wsg-courses-mcp/issues)
- **Live API**: https://wsg-courses-mcp-server-c2tuon4crq-uc.a.run.app/docs
- **Documentation**: See implementation plan in `.github/prompts/`

---

**Built with ❤️ for Singapore's education and training community**
