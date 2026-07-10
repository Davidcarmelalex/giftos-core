"""Market intelligence endpoints."""

from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()


@router.get("/prices")
async def get_prices(
    brand: Optional[str] = Query(None, description="Gift card brand"),
    region: Optional[str] = Query(None, description="Region code"),
):
    """Get current gift card market prices."""
    return {
        "status": "success",
        "timestamp": 1720600000,
        "data": [
            {
                "brand": "Apple",
                "region": "US",
                "denomination": 100,
                "buy_price": 85.50,
                "sell_price": 92.00,
                "currency": "USD",
                "spread_percent": 7.09,
                "source": "noones",
                "updated_at": "2026-07-10T08:00:00Z",
            }
        ],
    }


@router.get("/spreads")
async def get_spreads():
    """Get arbitrage spreads across markets."""
    return {"status": "success", "data": []}
