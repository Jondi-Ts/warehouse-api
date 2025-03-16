# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as test_client:
        yield test_client
