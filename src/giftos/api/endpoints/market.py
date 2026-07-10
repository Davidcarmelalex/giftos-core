"""Market intelligence endpoints with database integration."""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, desc, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from giftos.database import get_db
from giftos.models.gift_card import PriceRecord
from giftos.schemas import PriceResponse, SpreadResponse

router = APIRouter()


@router.get("/prices", response_model=List[PriceResponse])
async def get_prices(
    brand: Optional[str] = Query(None, description="Gift card brand"),
    region: Optional[str] = Query(None, description="Region code (US, UK, CA, etc.)"),
    source: Optional[str] = Query(None, description="Price source (noones, manual)"),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Get current gift card market prices from database."""
    stmt = select(PriceRecord).order_by(desc(PriceRecord.recorded_at))

    if brand:
        stmt = stmt.where(PriceRecord.brand.ilike(brand))
    if region:
        stmt = stmt.where(PriceRecord.region.ilike(region))
    if source:
        stmt = stmt.where(PriceRecord.source == source)

    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    records = result.scalars().all()

    if not records:
        return []

    return [PriceResponse(**r.to_dict()).model_dump() for r in records]


@router.get("/spreads")
async def get_spreads(
    brand: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    min_arbitrage: float = Query(1.0, ge=0, description="Minimum arbitrage %"),
    db: AsyncSession = Depends(get_db),
):
    """Get arbitrage spreads across markets — buy low, sell high opportunities."""
    stmt = (
        select(
            PriceRecord.brand,
            PriceRecord.region,
            PriceRecord.denomination,
            func.min(PriceRecord.sell_price).label("lowest_sell"),
            func.max(PriceRecord.buy_price).label("highest_buy"),
            PriceRecord.currency,
        )
        .where(
            and_(
                PriceRecord.sell_price.is_not(None),
                PriceRecord.buy_price.is_not(None),
            )
        )
        .group_by(PriceRecord.brand, PriceRecord.region, PriceRecord.denomination, PriceRecord.currency)
    )

    if brand:
        stmt = stmt.where(PriceRecord.brand.ilike(brand))
    if region:
        stmt = stmt.where(PriceRecord.region.ilike(region))

    result = await db.execute(stmt)
    rows = result.all()

    spreads = []
    for row in rows:
        if row.lowest_sell and row.highest_buy:
            arb_pct = ((row.highest_buy - row.lowest_sell) / row.lowest_sell) * 100
            if arb_pct >= min_arbitrage:
                spreads.append({
                    "brand": row.brand,
                    "region": row.region,
                    "denomination": row.denomination,
                    "lowest_sell": round(row.lowest_sell, 2),
                    "highest_buy": round(row.highest_buy, 2),
                    "arbitrage_percent": round(arb_pct, 2),
                    "currency": row.currency,
                })

    spreads.sort(key=lambda x: x["arbitrage_percent"], reverse=True)
    return {"status": "success", "count": len(spreads), "data": spreads}


@router.get("/brands")
async def get_brands(db: AsyncSession = Depends(get_db)):
    """Get all tracked gift card brands."""
    stmt = select(PriceRecord.brand).distinct().order_by(PriceRecord.brand)
    result = await db.execute(stmt)
    brands = [row[0] for row in result.all()]
    return {"status": "success", "data": brands}


@router.get("/regions")
async def get_regions(db: AsyncSession = Depends(get_db)):
    """Get all tracked regions."""
    stmt = select(PriceRecord.region).distinct().order_by(PriceRecord.region)
    result = await db.execute(stmt)
    regions = [row[0] for row in result.all()]
    return {"status": "success", "data": regions}


@router.get("/history/{brand}")
async def get_price_history(
    brand: str,
    region: Optional[str] = None,
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
):
    """Get historical price data for a brand."""
    from datetime import datetime, timedelta

    cutoff = datetime.utcnow() - timedelta(days=days)
    stmt = (
        select(PriceRecord)
        .where(
            and_(
                PriceRecord.brand.ilike(brand),
                PriceRecord.recorded_at >= cutoff,
            )
        )
        .order_by(PriceRecord.recorded_at)
    )

    if region:
        stmt = stmt.where(PriceRecord.region.ilike(region))

    result = await db.execute(stmt)
    records = result.scalars().all()

    return {
        "status": "success",
        "brand": brand,
        "days": days,
        "count": len(records),
        "data": [r.to_dict() for r in records],
    }
