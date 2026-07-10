"""Portfolio and inventory endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_portfolio():
    """Get complete portfolio overview."""
    return {
        "status": "success",
        "data": {
            "total_value_usd": 0.0,
            "holdings": [],
            "pnl": {"realized": 0, "unrealized": 0},
        },
    }


@router.get("/inventory")
async def get_inventory():
    """Get gift card inventory."""
    return {"status": "success", "data": []}
