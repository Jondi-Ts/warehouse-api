# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def test_client():
    """Provides a TestClient instance for API testing."""
    return TestClient(app)
