"""Market intelligence scraper tasks."""

from celery import shared_task
import structlog

from giftos.database import AsyncSessionLocal
from giftos.models.gift_card import PriceRecord
from giftos.config import settings

logger = structlog.get_logger()


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def scrape_gift_card_prices(self, brand: str, region: str):
    """Scrape gift card prices from marketplace."""
    logger.info("scraper.start", brand=brand, region=region)
    return {"brand": brand, "region": region, "prices": [], "status": "placeholder"}


@shared_task
def calculate_spreads():
    """Calculate arbitrage spreads across all price sources."""
    logger.info("scraper.spreads.calculate")
    return {"spreads_calculated": 0}


@shared_task
def sync_noones_offers():
    """Sync active offers from NoOnes marketplace."""
    logger.info("scraper.noones.offers.sync")
    return {"offers_synced": 0}
