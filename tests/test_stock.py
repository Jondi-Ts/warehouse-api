import pytest

from app.api_functionality.products_functionality import ProductsFunctionality
from app.api_functionality.stock_functionality import StockFunctionality
from helpers import helpers
from helpers.config import Urls
from helpers.mock_generator import generate_mock_product


class TestStocks:
    @pytest.fixture(autouse=True)
    def setup_class(self, clients_request):
        self.client = clients_request
        self.base_url = Urls.BASE_URL
        self.product_functionality = ProductsFunctionality(self.client, self.base_url)
        self.stock_functionality = StockFunctionality(self.client, self.base_url)

    def test_create_stock(self):
        product_response = self.product_functionality.create_product(generate_mock_product())
        product_id = product_response.json()["id"]
        stock_response = self.stock_functionality.create_stock(product_id)
        assert stock_response.json()["quantity"] == 50
