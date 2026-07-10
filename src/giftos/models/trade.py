"""Trade and offer data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from giftos.database import Base
import enum


class TradeStatus(str, enum.Enum):
    """Trade lifecycle statuses."""
    PENDING = "pending"
    ACTIVE = "active"
    PAID = "paid"
    DISPUTED = "disputed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class OfferType(str, enum.Enum):
    """Offer direction."""
    BUY = "buy"
    SELL = "sell"


class Offer(Base):
    """Gift card offer."""

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    offer_hash = Column(String, unique=True, index=True)
    offer_type = Column(String, nullable=False)
    gift_card_brand = Column(String, nullable=False, index=True)
    denomination = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    payment_method = Column(String, nullable=False)
    terms = Column(Text, nullable=True)
    margin = Column(Float, nullable=True)
    source = Column(String, nullable=False, default="noones")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    trades = relationship("Trade", back_populates="offer")

    def to_dict(self):
        return {
            "id": self.id,
            "offer_hash": self.offer_hash,
            "offer_type": self.offer_type,
            "gift_card_brand": self.gift_card_brand,
            "denomination": self.denomination,
            "price": self.price,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "terms": self.terms,
            "margin": self.margin,
            "source": self.source,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Trade(Base):
    """Gift card trade transaction."""

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    trade_hash = Column(String, unique=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=True)
    status = Column(String, nullable=False, default=TradeStatus.PENDING.value)
    amount_usd = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    buyer_username = Column(String, nullable=True)
    seller_username = Column(String, nullable=True)
    gift_card_brand = Column(String, nullable=False)
    denomination = Column(Float, nullable=False)
    payment_method = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    released_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    offer = relationship("Offer", back_populates="trades")

    def to_dict(self):
        return {
            "id": self.id,
            "trade_hash": self.trade_hash,
            "offer_id": self.offer_id,
            "status": self.status,
            "amount_usd": self.amount_usd,
            "quantity": self.quantity,
            "buyer_username": self.buyer_username,
            "seller_username": self.seller_username,
            "gift_card_brand": self.gift_card_brand,
            "denomination": self.denomination,
            "payment_method": self.payment_method,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "released_at": self.released_at.isoformat() if self.released_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
        }


class WalletBalance(Base):
    """Wallet balance snapshot."""

    __tablename__ = "wallet_balances"

    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0.0)
    available = Column(Float, nullable=False, default=0.0)
    frozen = Column(Float, nullable=False, default=0.0)
    source = Column(String, nullable=False, default="noones")
    snapshot_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "currency": self.currency,
            "balance": self.balance,
            "available": self.available,
            "frozen": self.frozen,
            "source": self.source,
            "snapshot_at": self.snapshot_at.isoformat() if self.snapshot_at else None,
        }
