"""FastAPI application with MCP integration for WSG Courses API."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from routers import courses
from config import settings
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="WSG Courses API MCP Server",
    description="MCP server for Singapore SkillsFuture WSG Courses API with certificate authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware if configured
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {settings.cors_origins_list}")

# Include routers
app.include_router(courses.router)
logger.info("Courses router registered")

# Initialize MCP server
mcp = FastApiMCP(
    app,
    name="WSG Courses MCP",
    description="AI-accessible tools for Singapore course directory search and discovery"
)

# Mount MCP endpoint
mcp.mount_http(mount_path="/mcp")
logger.info("MCP endpoint mounted at /mcp")


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("="*60)
    logger.info("WSG Courses API MCP Server Starting")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Base URL: {settings.base_url}")
    logger.info(f"Certificate: {settings.cert_path}")
    logger.info(f"Cloud Run: {settings.is_cloud_run}")
    logger.info("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("WSG Courses API MCP Server Shutting Down")


@app.get("/")
async def root():
    """API information and available endpoints."""
    return {
        "name": "WSG Courses API MCP Server",
        "version": "1.0.0",
        "description": "AI-accessible Singapore SkillsFuture course directory",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "mcp": "/mcp",
            "health": "/health",
            "api": "/courses"
        },
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and Cloud Run."""
    return {
        "status": "healthy",
        "service": "wsg-courses-mcp-server",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "cloud_run": settings.is_cloud_run
    }


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to check configuration."""
    from pathlib import Path
    return {
        "base_url": settings.base_url,
        "cert_path": settings.cert_path,
        "key_path": settings.key_path,
        "cert_exists": Path(settings.cert_path).exists(),
        "key_exists": Path(settings.key_path).exists(),
        "environment": settings.environment
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower()
    )
