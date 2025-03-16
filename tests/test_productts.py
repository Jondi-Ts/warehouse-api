from pprint import pprint

import pytest


class TestProducts:
    BASE_URL = "http://127.0.0.1:8000"

    @pytest.fixture(autouse=True)
    def setup_class(self, clients_request):
        """✅ Automatically injects the session-based HTTP client into test class."""
        self.client = clients_request

    def test_get_products(self):
        """✅ Tests retrieving all products."""
        response = self.client.get(f"{self.BASE_URL}/products/")
        pprint(response.json())  # Debugging output
