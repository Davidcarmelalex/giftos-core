"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PriceResponse(BaseModel):
    brand: str
    region: str
    denomination: float
    buy_price: Optional[float]
    sell_price: Optional[float]
    currency: str = "USD"
    spread_percent: Optional[float]
    source: str
    updated_at: Optional[str]


class SpreadResponse(BaseModel):
    brand: str
    region: str
    denomination: float
    lowest_sell: float
    highest_buy: float
    arbitrage_percent: float
    currency: str = "USD"


class OfferCreate(BaseModel):
    offer_type: str = Field(..., pattern="^(buy|sell)$")
    gift_card_brand: str
    denomination: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str
    terms: Optional[str] = None
    margin: Optional[float] = None
    source: str = "manual"


class OfferResponse(BaseModel):
    id: int
    offer_hash: str
    offer_type: str
    gift_card_brand: str
    denomination: float
    price: float
    currency: str
    payment_method: str
    terms: Optional[str]
    margin: Optional[float]
    source: str
    is_active: bool
    created_at: Optional[str]


class TradeCreate(BaseModel):
    offer_id: int
    amount_usd: float = Field(..., gt=0)
    quantity: float = Field(default=1.0, gt=0)
    buyer_username: Optional[str] = None
    seller_username: Optional[str] = None
    gift_card_brand: str
    denomination: float
    payment_method: Optional[str] = None


class TradeResponse(BaseModel):
    id: int
    trade_hash: str
    offer_id: Optional[int]
    status: str
    amount_usd: float
    quantity: float
    buyer_username: Optional[str]
    seller_username: Optional[str]
    gift_card_brand: str
    denomination: float
    payment_method: Optional[str]
    started_at: Optional[str]
    paid_at: Optional[str]
    released_at: Optional[str]
    completed_at: Optional[str]


class PortfolioHolding(BaseModel):
    gift_card_brand: str
    total_quantity: float
    avg_buy_price: float
    current_value: float
    unrealized_pnl: float


class PortfolioResponse(BaseModel):
    total_value_usd: float
    holdings: List[PortfolioHolding]
    pnl: dict
    wallet_balances: List[dict]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
