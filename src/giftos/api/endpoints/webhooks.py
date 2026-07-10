"""Webhook receiver endpoints."""

from fastapi import APIRouter, Request, Header, HTTPException
import hmac
import hashlib

from giftos.config import settings

router = APIRouter()


@router.post("/noones")
async def noones_webhook(
    request: Request,
    x_signature: str = Header(None, alias="X-Signature"),
):
    """Receive NoOnes webhook events."""
    body = await request.body()
    
    if settings.NOONES_WEBHOOK_SECRET and x_signature:
        expected = hmac.new(
            settings.NOONES_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(f"sha256={expected}", x_signature):
            raise HTTPException(401, "Invalid signature")
    
    payload = await request.json()
    return {"status": "received"}
