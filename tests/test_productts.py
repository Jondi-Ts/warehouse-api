import pytest

from api_functionality.products_functionality import create_product
from app.schemas import ProductCreate, ProductUpdate
from helpers import helpers


class TestProducts:
    BASE_URL = "http://127.0.0.1:8000"

    @pytest.fixture(autouse=True)
    def setup_class(self, clients_request):
        self.client = clients_request

    @pytest.mark.parametrize("product_data", helpers.load_yaml_data("external_Files/products_data.yml"))
    def test_create_product_success(self, product_data):
        response = create_product(self.client, self.BASE_URL, product_data)
        assert response.status_code == 200
        assert response.json()["name"] == product_data["name"]
        assert response.json()["manufacturer"] == product_data["manufacturer"]

    def test_create_duplicate_product(self, product_data):
        self.client.post(f"{self.BASE_URL}/products", json=product_data)
        response = self.client.post(f"{self.BASE_URL}/products", json=product_data)
        assert response.status_code == 400

    def test_get_products_list(self):
        response = self.client.get(f"{self.BASE_URL}/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_product_by_valid_id(self):
        response = self.client.get(f"{self.BASE_URL}/products/1")
        assert response.status_code == 200
        assert "name" in response.json()

    def test_get_product_by_invalid_id(self):
        response = self.client.get(f"{self.BASE_URL}/products/999")
        assert response.status_code == 404

    def test_update_product_success(self):
        update_data = {"name": "Updated Product", "price": 19.99, "manufacturer": "Updated Manufacturer",
                       "category": "Updated Category"}
        response = self.client.put(f"{self.BASE_URL}/products/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]

    def test_update_nonexistent_product(self):
        update_data = {"name": "Nonexistent Product", "price": 29.99, "manufacturer": "None", "category": "None"}
        response = self.client.put(f"{self.BASE_URL}/products/999", json=update_data)
        assert response.status_code == 404

    def test_delete_product_success(self):
        response = self.client.delete(f"{self.BASE_URL}/products/1")
        assert response.status_code == 200

    def test_delete_nonexistent_product(self):
        response = self.client.delete(f"{self.BASE_URL}/products/999")
        assert response.status_code == 404
