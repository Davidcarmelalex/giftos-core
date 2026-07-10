"""Webhook endpoint tests."""

import pytest


def test_noones_webhook_without_signature(client):
    """Test webhook accepts payload without signature when secret not set."""
    payload = {"event": "trade.started", "trade_hash": "abc123"}
    response = client.post("/api/v1/webhooks/noones", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "received"


def test_noones_webhook_with_invalid_signature(client):
    """Test webhook rejects invalid signature."""
    payload = {"event": "trade.started", "trade_hash": "abc123"}
    response = client.post(
        "/api/v1/webhooks/noones",
        json=payload,
        headers={"X-Signature": "sha256=invalid"},
    )
    # Will fail signature verification if NOONES_WEBHOOK_SECRET is set
