"""Health endpoint tests."""

import pytest


def test_health_check(client):
    """Test health endpoint returns OK."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "giftos-core"


def test_root_endpoint(client):
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "GiftOS Core"
    assert "documentation" in data
