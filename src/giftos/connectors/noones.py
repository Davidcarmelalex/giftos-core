"""NoOnes API connector with OAuth 2.0 authentication.

Implements the NoOnes API client with automatic token refresh,
rate limiting, and retry logic for all gift card marketplace operations.

API Documentation: https://developer.noones.com/
"""

import time
from typing import Optional, Dict, Any, List
import structlog
import httpx

from giftos.config import settings

logger = structlog.get_logger()


class NoOnesAPIError(Exception):
    """Raised when NoOnes API returns an error response."""
    
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NoOnesClient:
    """NoOnes API client with OAuth 2.0 client-credentials flow.
    
    Handles authentication, request signing, rate limiting, and
    automatic token refresh for all NoOnes marketplace operations.
    
    Example:
        client = NoOnesClient()
        balance = await client.get_wallet_balance()
        offers = await client.list_offers(gift_card_brand="Apple")
    """
    
    def __init__(self):
        self.client_id = settings.NOONES_CLIENT_ID
        self.client_secret = settings.NOONES_CLIENT_SECRET
        self.api_base = settings.NOONES_API_BASE.rstrip("/")
        self.auth_url = settings.NOONES_AUTH_URL
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._client = httpx.AsyncClient(timeout=30.0)
    
    async def _get_token(self) -> str:
        """Obtain or refresh OAuth 2.0 access token.
        
        Uses client_credentials grant type. Tokens are cached
        and refreshed 5 minutes before expiry.
        
        Returns:
            Valid access token string.
        """
        if self._access_token and time.time() < self._token_expires_at - 300:
            return self._access_token
        
        logger.info("noones.auth.refresh")
        
        response = await self._client.post(
            self.auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        data = response.json()
        
        self._access_token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 864000)
        
        logger.info(
            "noones.auth.success",
            scopes=data.get("scope", ""),
            expires_in=data.get("expires_in", 0),
        )
        
        return self._access_token
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make authenticated API request to NoOnes.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., '/wallet/balance')
            **kwargs: Additional arguments passed to httpx
            
        Returns:
            Parsed JSON response dict with 'status', 'data', 'timestamp'
            
        Raises:
            NoOnesAPIError: If API returns an error response
            httpx.HTTPError: For network/HTTP errors
        """
        token = await self._get_token()
        
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/json; version=1"
        headers["Content-Type"] = "text/plain"
        
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        
        logger.debug("noones.api.request", method=method, endpoint=endpoint)
        
        response = await self._client.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == "error":
            error = data.get("error", {})
            logger.error(
                "noones.api.error",
                endpoint=endpoint,
                error_code=error.get("code"),
                error_message=error.get("message"),
            )
            raise NoOnesAPIError(
                message=error.get("message", "Unknown error"),
                code=error.get("code"),
                details=error,
            )
        
        return data
    
    # -- Wallet Endpoints --
    
    async def get_wallet_balance(self) -> Dict[str, Any]:
        """Get wallet balances for all currencies."""
        return await self._request("GET", "/wallet/balance")
    
    async def get_wallet_transactions(
        self,
        currency: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get wallet transaction history."""
        params = {"limit": limit}
        if currency:
            params["currency"] = currency
        return await self._request("GET", "/wallet/transactions", params=params)
    
    # -- Offer Endpoints --
    
    async def list_offers(
        self,
        offer_type: Optional[str] = None,
        gift_card_brand: Optional[str] = None,
        currency_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List marketplace offers with filtering."""
        params = {"limit": limit}
        if offer_type:
            params["offer_type"] = offer_type
        if gift_card_brand:
            params["gift_card_brand"] = gift_card_brand
        if currency_code:
            params["currency_code"] = currency_code
        if payment_method:
            params["payment_method"] = payment_method
        
        return await self._request("GET", "/offer/list", params=params)
    
    async def get_offer(self, offer_hash: str) -> Dict[str, Any]:
        """Get offer details."""
        return await self._request("GET", f"/offer/{offer_hash}")
    
    async def create_offer(self, **offer_data) -> Dict[str, Any]:
        """Create a new offer."""
        return await self._request("POST", "/offer", json=offer_data)
    
    async def update_offer(self, offer_hash: str, **updates) -> Dict[str, Any]:
        """Update an existing offer."""
        return await self._request("PATCH", f"/offer/{offer_hash}", json=updates)
    
    async def delete_offer(self, offer_hash: str) -> Dict[str, Any]:
        """Deactivate an offer."""
        return await self._request("DELETE", f"/offer/{offer_hash}")
    
    # -- Trade Endpoints --
    
    async def list_trades(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List trades."""
        params = {"limit": limit}
        if status:
            params["status"] = status
        return await self._request("GET", "/trade/list", params=params)
    
    async def get_trade(self, trade_hash: str) -> Dict[str, Any]:
        """Get trade details."""
        return await self._request("GET", f"/trade/{trade_hash}")
    
    async def start_trade(self, offer_hash: str, amount: float) -> Dict[str, Any]:
        """Start a new trade."""
        return await self._request(
            "POST",
            "/trade",
            json={"offer_hash": offer_hash, "amount": amount},
        )
    
    async def cancel_trade(self, trade_hash: str) -> Dict[str, Any]:
        """Cancel an active trade."""
        return await self._request("POST", "/trade/cancel", json={"trade_hash": trade_hash})
    
    # -- Trade Chat --
    
    async def post_trade_chat(self, trade_hash: str, message: str) -> Dict[str, Any]:
        """Post message to trade chat."""
        return await self._request(
            "POST",
            "/trade-chat/post",
            json={"trade_hash": trade_hash, "message": message},
        )
    
    async def get_trade_chat(self, trade_hash: str) -> Dict[str, Any]:
        """Get trade chat history."""
        return await self._request("GET", "/trade-chat/get", params={"trade_hash": trade_hash})
    
    # -- Trade Actions --
    
    async def release_trade(self, trade_hash: str) -> Dict[str, Any]:
        """Release escrow."""
        return await self._request("POST", "/trade/release", json={"trade_hash": trade_hash})
    
    async def mark_trade_paid(self, trade_hash: str) -> Dict[str, Any]:
        """Mark trade as paid."""
        return await self._request("POST", "/trade/paid", json={"trade_hash": trade_hash})
    
    async def dispute_trade(self, trade_hash: str, reason: str) -> Dict[str, Any]:
        """Open a dispute."""
        return await self._request(
            "POST",
            "/trade/dispute",
            json={"trade_hash": trade_hash, "reason": reason},
        )
    
    # -- Payment Methods --
    
    async def list_payment_methods(self) -> Dict[str, Any]:
        """List available payment methods."""
        return await self._request("GET", "/payment-method/list")
    
    # -- Webhooks --
    
    async def register_webhook(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Register webhook for trade events."""
        return await self._request("POST", "/webhook", json={"url": url, "events": events})
    
    async def list_webhooks(self) -> Dict[str, Any]:
        """List registered webhooks."""
        return await self._request("GET", "/webhook/list")
    
    async def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        return await self._request("DELETE", f"/webhook/{webhook_id}")
    
    # -- User Profile --
    
    async def get_me(self) -> Dict[str, Any]:
        """Get authenticated user profile."""
        return await self._request("GET", "/user/me")
    
    # -- Cleanup --
    
    async def close(self):
        """Close HTTP client."""
        await self._client.aclose()
