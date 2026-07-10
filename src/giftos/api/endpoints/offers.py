"""Offer management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class OfferCreate(BaseModel):
    gift_card_brand: str
    denomination: float
    price: float
    currency: str = "USD"
    payment_method: str
    terms: Optional[str] = None


@router.get("")
async def list_offers(
    brand: Optional[str] = None,
    limit: int = 50,
):
    """List active offers (from connected exchanges)."""
    return {"status": "success", "data": []}


@router.post("")
async def create_offer(offer: OfferCreate):
    """Create a new offer on connected exchanges."""
    return {"status": "success", "data": {"offer_hash": "placeholder"}}
