import asyncio

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

    def test_create_stock_positive(self):
        product_response = self.product_functionality.create_product(generate_mock_product())
        product_id = product_response.json()["id"]
        stock_response = self.stock_functionality.create_stock(product_id)
        assert stock_response.json()["quantity"] == 50

    def test_create_stock_invalid_negative(self):
        response = self.stock_functionality.create_stock("1041451", 6549994)
        assert response.status_code == 400

    def test_get_stock_list(self):
        response = self.stock_functionality.get_stock_list()
        if response.status_code == 404:
            assert response.json()["detail"] == "No stock entries found."
        else:
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    import pytest
    import asyncio

    @pytest.mark.asyncio
    async def test_async_reduce_stock_success(self):
        product_response = self.product_functionality.create_product(generate_mock_product())
        product_id = product_response.json()["id"]

        stock_response = self.stock_functionality.create_stock(product_id, quantity=50)
        stock_id = stock_response.json()["id"]

        reduce_resp = self.stock_functionality.reduce_stock_quantity(stock_id, 10, delay=1)
        assert reduce_resp.status_code == 200
        reduce_task_id = reduce_resp.json()['task_id']

        # Wait and poll for task completion
        task_status_resp = None
        for _ in range(5):  # Retry for up to 5 seconds
            task_status_resp = self.client.get(f"{self.base_url}/tasks/{reduce_task_id}/status")
            status = task_status_resp.json()["status"]
            if status == "completed":
                break
            await asyncio.sleep(1)

        assert task_status_resp.json()["status"] == "completed"

        updated_stock_resp = self.stock_functionality.get_stock_by_product_id(product_id)
        assert updated_stock_resp.status_code == 200
        updated_stock = updated_stock_resp.json()
        assert updated_stock["quantity"] == 40

    def test_get_low_stock_products(self):
        # Setup: Create a new product
        product_response = self.product_functionality.create_product(generate_mock_product())
        product_id = product_response.json()["id"]
        low_quantity = 5  # assuming the threshold is 10
        stock_response = self.stock_functionality.create_stock(product_id, quantity=low_quantity)
        low_stock_resp = self.stock_functionality.get_low_stock_products(minimum_quantity=10)
        assert stock_response.status_code == 200
        low_stock_products = low_stock_resp.json()

        # Validate: Check the product appears in the low stock list
        assert any(item["product_id"] == product_id for item in low_stock_products)
