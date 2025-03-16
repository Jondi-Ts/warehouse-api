import pytest

from app.api_functionality.products_functionality import ProductsFunctionality
from helpers import helpers


class TestProducts:
    BASE_URL = "http://127.0.0.1:8000"

    @pytest.fixture(autouse=True)
    def setup_class(self, clients_request):
        self.client = clients_request
        self.product_functionality = ProductsFunctionality(self.client, self.BASE_URL)

    @pytest.mark.parametrize("product_data", helpers.load_yaml_data("external_Files/products_data.yml"))
    def test_create_product_success(self, product_data):
        response = self.product_functionality.create_product(product_data)
        assert response.status_code == 200
        assert response.json()["name"] == product_data["name"]
        assert response.json()["manufacturer"] == product_data["manufacturer"]

    def test_get_products_list(self):
        response = self.product_functionality.get_product_list()
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_product_by_invalid_id(self):
        response = self.product_functionality.get_product_by_id(100000)
        assert response.status_code == 404

    def test_update_product_success(self):
        update_data = {"name": "Updated Product", "price": 19.99, "manufacturer": "Updated Manufacturer",
                       "category": "Updated Category"}
        response = self.product_functionality.update_product_by_id(2, update_data)
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]

    def test_update_nonexistent_product(self):
        update_data = {"name": "Nonexistent Product", "price": 29.99, "manufacturer": "None", "category": "None"}
        response = self.product_functionality.update_product_by_id(1, update_data)
        assert response.status_code == 404

    def test_delete_product_success(self):
        response = self.product_functionality.delete_product_by_id(1)
        assert response.status_code == 200

    def test_delete_nonexistent_product(self):
        response = self.product_functionality.delete_product_by_id(49879)
        assert response.status_code == 404
