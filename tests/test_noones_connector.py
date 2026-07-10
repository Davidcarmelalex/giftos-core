"""NoOnes connector unit tests."""

import pytest
from unittest.mock import AsyncMock, patch

from giftos.connectors.noones import NoOnesClient, NoOnesAPIError


@pytest.fixture
def client():
    """Create NoOnes client with test credentials."""
    return NoOnesClient()


@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initializes correctly."""
    client = NoOnesClient()
    assert client.api_base == "https://api.noones.com"


@pytest.mark.asyncio
async def test_token_refresh(client):
    """Test token is obtained on first request."""
    with patch.object(client._client, "post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={
            "access_token": "test_token",
            "expires_in": 864000,
            "scope": "read write",
        })
        mock_post.return_value = mock_response
        
        token = await client._get_token()
        assert token == "test_token"
