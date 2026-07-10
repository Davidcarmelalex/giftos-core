"""Trade lifecycle endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_trades():
    """List trades."""
    return {"status": "success", "data": []}


@router.get("/{trade_hash}")
async def get_trade(trade_hash: str):
    """Get trade details."""
    return {"status": "success", "data": {"trade_hash": trade_hash}}


@router.post("/{trade_hash}/release")
async def release_trade(trade_hash: str):
    """Release escrow for completed trade."""
    return {"status": "success", "data": {"released": True}}
