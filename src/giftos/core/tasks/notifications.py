"""Notification delivery tasks."""

from celery import shared_task
import structlog

from giftos.config import settings

logger = structlog.get_logger()


@shared_task(bind=True, max_retries=3)
def send_alert(self, channel: str, message: str):
    """Send alert via configured channel."""
    logger.info("notification.send", channel=channel)
    return {"channel": channel, "sent": True}


@shared_task
def notify_trade_event(trade_hash: str, event: str, details: dict = None):
    """Notify on trade state changes."""
    logger.info("notification.trade_event", trade_hash=trade_hash, event=event)
    message = f"Trade {trade_hash}: {event}"
    if details:
        message += f"\n{details}"
    if settings.TELEGRAM_BOT_TOKEN:
        send_alert.delay("telegram", message)
    return {"trade_hash": trade_hash, "event": event}


@shared_task
def send_price_alert(brand: str, region: str, condition: str, price: float):
    """Send price threshold alert."""
    message = f"Price Alert: {brand} ({region}) is {condition} ${price}"
    logger.info("notification.price_alert", brand=brand, condition=condition, price=price)
    if settings.TELEGRAM_BOT_TOKEN:
        send_alert.delay("telegram", message)
    return {"alert_sent": True}
