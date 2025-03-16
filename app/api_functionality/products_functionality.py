from helpers.endpoints import Endpoints


class ProductsFunctionality:
    def __init__(self, client, base_url):
        self.base_url = base_url
        self.client = client

    def create_product(self, product_data):
        response = self.client.post(f"{self.base_url}{Endpoints.PRODUCT_ENDPOINT}", json=product_data)
        return response

    def get_product_list(self):
        response = self.client.get(f"{self.base_url}{Endpoints.PRODUCT_ENDPOINT}")
        return response

    def get_product_by_id(self, id: int):
        response = self.client.get(f"{self.base_url}{Endpoints.PRODUCT_ENDPOINT}/{id}")
        return response

    def delete_product_by_id(self, id: int):
        response = self.client.delete(f"{self.base_url}{Endpoints.PRODUCT_ENDPOINT}/{id}")
        return response

    def update_product_by_id(self, id: int, product_data):
        response = self.client.put(f"{self.base_url}{Endpoints.PRODUCT_ENDPOINT}/{id}", json=product_data)
        return response