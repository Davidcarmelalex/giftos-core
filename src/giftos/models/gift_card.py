"""Gift card data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, UniqueConstraint
from sqlalchemy.sql import func
from giftos.database import Base
import enum


class GiftCardBrand(str, enum.Enum):
    """Supported gift card brands."""
    APPLE = "apple"
    AMAZON = "amazon"
    STEAM = "steam"
    GOOGLE_PLAY = "google_play"
    VISA = "visa"
    MASTERCARD = "mastercard"
    PLAYSTATION = "playstation"
    XBOX = "xbox"
    NINTENDO = "nintendo"
    NETFLIX = "netflix"
    SPOTIFY = "spotify"
    Uber = "uber"
    WALMART = "walmart"
    TARGET = "target"
    BEST_BUY = "best_buy"
    STARBUCKS = "starbucks"


class PriceRecord(Base):
    """Historical price record for gift cards."""

    __tablename__ = "price_records"
    __table_args__ = (
        UniqueConstraint("brand", "region", "denomination", "source", "recorded_at", name="uix_price_record"),
    )

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    denomination = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    source = Column(String, nullable=False, index=True)
    spread_percent = Column(Float, nullable=True)
    metadata_json = Column(String, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "region": self.region,
            "denomination": self.denomination,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "currency": self.currency,
            "source": self.source,
            "spread_percent": self.spread_percent,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
        }
