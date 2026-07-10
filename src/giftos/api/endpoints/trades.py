"""Trade lifecycle endpoints with database integration."""

import hashlib
import time
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from giftos.database import get_db
from giftos.models.trade import Trade, Offer, TradeStatus
from giftos.schemas import TradeCreate, TradeResponse

router = APIRouter()


def _generate_trade_hash() -> str:
    return hashlib.sha256(f"trade-{time.time()}".encode()).hexdigest()[:16]


@router.get("", response_model=List[TradeResponse])
async def list_trades(
    status: Optional[str] = Query(None, description="Filter by status"),
    brand: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List trades with filtering."""
    stmt = select(Trade).order_by(desc(Trade.created_at))

    if status:
        stmt = stmt.where(Trade.status == status.lower())
    if brand:
        stmt = stmt.where(Trade.gift_card_brand.ilike(brand))

    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    trades = result.scalars().all()

    return [TradeResponse(**t.to_dict()).model_dump() for t in trades]


@router.post("", response_model=TradeResponse, status_code=201)
async def create_trade(trade: TradeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new trade from an offer."""
    stmt = select(Offer).where(Offer.id == trade.offer_id)
    result = await db.execute(stmt)
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    if not offer.is_active:
        raise HTTPException(status_code=400, detail="Offer is not active")

    db_trade = Trade(
        trade_hash=_generate_trade_hash(),
        offer_id=trade.offer_id,
        status=TradeStatus.PENDING.value,
        amount_usd=trade.amount_usd,
        quantity=trade.quantity,
        buyer_username=trade.buyer_username,
        seller_username=trade.seller_username,
        gift_card_brand=trade.gift_card_brand,
        denomination=trade.denomination,
        payment_method=trade.payment_method or offer.payment_method,
    )

    db.add(db_trade)
    await db.commit()
    await db.refresh(db_trade)

    return TradeResponse(**db_trade.to_dict()).model_dump()


@router.get("/{trade_hash}", response_model=TradeResponse)
async def get_trade(trade_hash: str, db: AsyncSession = Depends(get_db)):
    """Get trade details."""
    stmt = select(Trade).where(Trade.trade_hash == trade_hash)
    result = await db.execute(stmt)
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    return TradeResponse(**trade.to_dict()).model_dump()


@router.post("/{trade_hash}/pay")
async def mark_paid(trade_hash: str, db: AsyncSession = Depends(get_db)):
    """Mark trade as paid (buyer has sent payment)."""
    stmt = select(Trade).where(Trade.trade_hash == trade_hash)
    result = await db.execute(stmt)
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    if trade.status != TradeStatus.PENDING.value:
        raise HTTPException(status_code=400, detail=f"Trade is {trade.status}, cannot mark as paid")

    trade.status = TradeStatus.PAID.value
    trade.paid_at = datetime.utcnow()
    await db.commit()

    return {"status": "success", "trade_hash": trade_hash, "status": trade.status}


@router.post("/{trade_hash}/release")
async def release_trade(trade_hash: str, db: AsyncSession = Depends(get_db)):
    """Release escrow for completed trade (seller releases gift card)."""
    stmt = select(Trade).where(Trade.trade_hash == trade_hash)
    result = await db.execute(stmt)
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    if trade.status != TradeStatus.PAID.value:
        raise HTTPException(status_code=400, detail=f"Trade is {trade.status}, cannot release")

    trade.status = TradeStatus.COMPLETED.value
    trade.released_at = datetime.utcnow()
    trade.completed_at = datetime.utcnow()
    await db.commit()

    return {"status": "success", "trade_hash": trade_hash, "released": True}


@router.post("/{trade_hash}/dispute")
async def dispute_trade(
    trade_hash: str,
    reason: str = "Disputed by user",
    db: AsyncSession = Depends(get_db),
):
    """Raise a dispute on a trade."""
    stmt = select(Trade).where(Trade.trade_hash == trade_hash)
    result = await db.execute(stmt)
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    if trade.status in [TradeStatus.COMPLETED.value, TradeStatus.CANCELLED.value]:
        raise HTTPException(status_code=400, detail="Cannot dispute completed/cancelled trade")

    trade.status = TradeStatus.DISPUTED.value
    await db.commit()

    return {"status": "success", "trade_hash": trade_hash, "status": "disputed", "reason": reason}


@router.post("/{trade_hash}/cancel")
async def cancel_trade(trade_hash: str, db: AsyncSession = Depends(get_db)):
    """Cancel a pending trade."""
    stmt = select(Trade).where(Trade.trade_hash == trade_hash)
    result = await db.execute(stmt)
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    if trade.status not in [TradeStatus.PENDING.value, TradeStatus.ACTIVE.value]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel trade with status: {trade.status}")

    trade.status = TradeStatus.CANCELLED.value
    trade.cancelled_at = datetime.utcnow()
    await db.commit()

    return {"status": "success", "trade_hash": trade_hash, "status": "cancelled"}
