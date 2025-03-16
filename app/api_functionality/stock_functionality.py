from helpers.config import Endpoints


class StockFunctionality:
    def __init__(self, client, base_url):
        self.base_url = base_url
        self.client = client

    def create_stock(self, product_id, quantity=50):
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        response = self.client.post(f"{self.base_url}{Endpoints.STOCK_ENDPOINT}", json=data)
        return response
