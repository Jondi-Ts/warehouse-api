
import pytest
import requests

@pytest.fixture(scope="session")
def clients_request():
    """✅ Provides a Requests session for test clients."""
    with requests.Session() as clients_request:
        yield clients_request
