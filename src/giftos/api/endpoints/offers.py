"""Offer management endpoints with database integration."""

import hashlib
import time

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from giftos.database import get_db
from giftos.models.trade import Offer
from giftos.schemas import OfferCreate, OfferResponse

router = APIRouter()


def _generate_hash() -> str:
    """Generate unique offer hash."""
    return hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:12]


@router.get("", response_model=List[OfferResponse])
async def list_offers(
    brand: Optional[str] = Query(None, description="Filter by gift card brand"),
    offer_type: Optional[str] = Query(None, description="buy or sell"),
    is_active: Optional[bool] = Query(True),
    source: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List offers with filtering."""
    stmt = select(Offer).order_by(desc(Offer.created_at))

    if brand:
        stmt = stmt.where(Offer.gift_card_brand.ilike(brand))
    if offer_type:
        stmt = stmt.where(Offer.offer_type == offer_type.lower())
    if is_active is not None:
        stmt = stmt.where(Offer.is_active == is_active)
    if source:
        stmt = stmt.where(Offer.source == source)

    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    offers = result.scalars().all()

    return [OfferResponse(**o.to_dict()).model_dump() for o in offers]


@router.post("", response_model=OfferResponse, status_code=201)
async def create_offer(offer: OfferCreate, db: AsyncSession = Depends(get_db)):
    """Create a new offer."""
    db_offer = Offer(
        offer_hash=_generate_hash(),
        offer_type=offer.offer_type.lower(),
        gift_card_brand=offer.gift_card_brand.lower(),
        denomination=offer.denomination,
        price=offer.price,
        currency=offer.currency.upper(),
        payment_method=offer.payment_method,
        terms=offer.terms,
        margin=offer.margin,
        source=offer.source,
        is_active=True,
    )

    db.add(db_offer)
    await db.commit()
    await db.refresh(db_offer)

    return OfferResponse(**db_offer.to_dict()).model_dump()


@router.get("/{offer_hash}", response_model=OfferResponse)
async def get_offer(offer_hash: str, db: AsyncSession = Depends(get_db)):
    """Get a single offer by hash."""
    stmt = select(Offer).where(Offer.offer_hash == offer_hash)
    result = await db.execute(stmt)
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    return OfferResponse(**offer.to_dict()).model_dump()


@router.patch("/{offer_hash}/deactivate")
async def deactivate_offer(offer_hash: str, db: AsyncSession = Depends(get_db)):
    """Deactivate an offer."""
    stmt = select(Offer).where(Offer.offer_hash == offer_hash)
    result = await db.execute(stmt)
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    offer.is_active = False
    await db.commit()

    return {"status": "success", "message": "Offer deactivated", "offer_hash": offer_hash}


@router.delete("/{offer_hash}")
async def delete_offer(offer_hash: str, db: AsyncSession = Depends(get_db)):
    """Delete an offer permanently."""
    stmt = select(Offer).where(Offer.offer_hash == offer_hash)
    result = await db.execute(stmt)
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    await db.delete(offer)
    await db.commit()

    return {"status": "success", "message": "Offer deleted", "offer_hash": offer_hash}
