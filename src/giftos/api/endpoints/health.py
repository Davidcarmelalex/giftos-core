"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health():
    """Service health status."""
    return {"status": "healthy", "service": "giftos-core", "version": "0.1.0"}
