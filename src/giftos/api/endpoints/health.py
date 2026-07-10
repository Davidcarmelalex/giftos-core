"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from giftos.database import get_db, engine
from giftos.models.trade import Trade
from giftos.models.gift_card import PriceRecord
from giftos.config import settings

router = APIRouter()


@router.get("")
async def health(db: AsyncSession = Depends(get_db)):
    """Service health status with dependency checks."""
    health_data = {
        "status": "healthy",
        "service": "giftos-core",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.APP_ENV,
    }

    # Check database
    try:
        stmt = select(func.count(Trade.id))
        result = await db.execute(stmt)
        health_data["database"] = {"status": "connected", "trades": result.scalar() or 0}
    except Exception as e:
        health_data["database"] = {"status": "error", "message": str(e)}
        health_data["status"] = "degraded"

    # Check price records
    try:
        stmt = select(func.count(PriceRecord.id))
        result = await db.execute(stmt)
        health_data["price_records"] = result.scalar() or 0
    except Exception:
        health_data["price_records"] = 0

    return health_data


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Kubernetes readiness probe."""
    try:
        stmt = select(func.count(Trade.id))
        await db.execute(stmt)
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}


@router.get("/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"alive": True}
