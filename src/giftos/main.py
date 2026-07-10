"""FastAPI application entry point."""

import structlog
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from giftos.config import settings
from giftos.database import init_db
from giftos.api.routes import router as api_router
from giftos.celery_app import celery_app

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("giftos.startup", version="0.1.0", env=settings.APP_ENV)
    await init_db()
    yield
    logger.info("giftos.shutdown")


app = FastAPI(
    title="GiftOS Core API",
    description="Open infrastructure for digital gift card markets.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("giftos.error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "giftos-core", "version": "0.1.0"}


@app.get("/", tags=["System"])
async def root():
    """Root endpoint."""
    return {
        "name": "GiftOS Core",
        "version": "0.1.0",
        "documentation": "/docs",
    }
