"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from giftos.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)
