"""Market intelligence endpoint tests."""

import pytest


def test_get_prices(client):
    """Test prices endpoint returns price data."""
    response = client.get("/api/v1/market/prices")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data


def test_get_prices_with_filters(client):
    """Test prices endpoint with brand filter."""
    response = client.get("/api/v1/market/prices?brand=Apple&region=US")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_get_spreads(client):
    """Test spreads endpoint."""
    response = client.get("/api/v1/market/spreads")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
