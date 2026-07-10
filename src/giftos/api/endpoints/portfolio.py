"""Portfolio and inventory endpoints with database integration."""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from giftos.database import get_db
from giftos.models.trade import Trade, WalletBalance, TradeStatus
from giftos.models.gift_card import PriceRecord

router = APIRouter()


@router.get("")
async def get_portfolio(db: AsyncSession = Depends(get_db)):
    """Get complete portfolio overview with P&L calculation."""
    # Get completed trades grouped by brand
    stmt = (
        select(
            Trade.gift_card_brand,
            func.sum(Trade.quantity).label("total_quantity"),
            func.avg(Trade.amount_usd / Trade.quantity).label("avg_price"),
            func.sum(Trade.amount_usd).label("total_spent"),
        )
        .where(Trade.status == TradeStatus.COMPLETED.value)
        .group_by(Trade.gift_card_brand)
    )
    result = await db.execute(stmt)
    holdings_rows = result.all()

    # Get latest prices for valuation
    latest_prices = {}
    for row in holdings_rows:
        stmt = (
            select(PriceRecord)
            .where(PriceRecord.brand.ilike(row.gift_card_brand))
            .order_by(PriceRecord.recorded_at.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        price_rec = result.scalar_one_or_none()
        if price_rec:
            latest_prices[row.gift_card_brand] = price_rec.sell_price or price_rec.buy_price or 0

    # Calculate holdings with P&L
    holdings = []
    total_value = 0.0
    total_pnl = 0.0

    for row in holdings_rows:
        current_price = latest_prices.get(row.gift_card_brand, row.avg_price or 0)
        current_value = (row.total_quantity or 0) * current_price
        cost_basis = (row.total_quantity or 0) * (row.avg_price or 0)
        unrealized_pnl = current_value - cost_basis

        holdings.append({
            "gift_card_brand": row.gift_card_brand,
            "total_quantity": round(row.total_quantity or 0, 2),
            "avg_buy_price": round(row.avg_price or 0, 2),
            "current_price": round(current_price, 2),
            "current_value": round(current_value, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
        })
        total_value += current_value
        total_pnl += unrealized_pnl

    # Get wallet balances
    stmt = select(WalletBalance).order_by(WalletBalance.currency)
    result = await db.execute(stmt)
    wallets = result.scalars().all()

    # Trade counts by status
    stmt = (
        select(Trade.status, func.count(Trade.id).label("count"))
        .group_by(Trade.status)
    )
    result = await db.execute(stmt)
    trade_counts = {row.status: row.count for row in result.all()}

    return {
        "status": "success",
        "data": {
            "total_value_usd": round(total_value, 2),
            "unrealized_pnl": round(total_pnl, 2),
            "holdings": holdings,
            "wallet_balances": [w.to_dict() for w in wallets],
            "trade_summary": trade_counts,
            "trade_summary_total": sum(trade_counts.values()),
        },
    }


@router.get("/inventory")
async def get_inventory(db: AsyncSession = Depends(get_db)):
    """Get gift card inventory — aggregated by brand and denomination."""
    stmt = (
        select(
            Trade.gift_card_brand,
            Trade.denomination,
            func.sum(Trade.quantity).label("total_qty"),
            func.count(Trade.id).label("trade_count"),
        )
        .where(Trade.status == TradeStatus.COMPLETED.value)
        .group_by(Trade.gift_card_brand, Trade.denomination)
        .order_by(Trade.gift_card_brand)
    )
    result = await db.execute(stmt)
    rows = result.all()

    inventory = [
        {
            "gift_card_brand": row.gift_card_brand,
            "denomination": row.denomination,
            "total_quantity": round(row.total_qty or 0, 2),
            "trade_count": row.trade_count,
        }
        for row in rows
    ]

    return {"status": "success", "data": inventory}


@router.get("/pnl")
async def get_pnl_breakdown(db: AsyncSession = Depends(get_db)):
    """Get detailed P&L breakdown by brand."""
    stmt = (
        select(
            Trade.gift_card_brand,
            func.sum(Trade.amount_usd).label("revenue"),
            func.count(Trade.id).label("trade_count"),
            func.avg(Trade.amount_usd).label("avg_trade_size"),
        )
        .where(Trade.status == TradeStatus.COMPLETED.value)
        .group_by(Trade.gift_card_brand)
    )
    result = await db.execute(stmt)
    rows = result.all()

    return {
        "status": "success",
        "data": [
            {
                "brand": row.gift_card_brand,
                "total_revenue": round(row.revenue or 0, 2),
                "trade_count": row.trade_count,
                "avg_trade_size": round(row.avg_trade_size or 0, 2),
            }
            for row in rows
        ],
    }
