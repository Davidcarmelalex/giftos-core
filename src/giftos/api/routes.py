"""Main API router aggregation."""

from fastapi import APIRouter

from giftos.api.endpoints import health, market, offers, trades, portfolio, webhooks

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(market.router, prefix="/market", tags=["Market Intelligence"])
router.include_router(offers.router, prefix="/offers", tags=["Offers"])
router.include_router(trades.router, prefix="/trades", tags=["Trades"])
router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
