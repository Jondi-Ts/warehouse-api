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

    def get_stock_list(self):
        response = self.client.get(f"{self.base_url}{Endpoints.STOCK_ENDPOINT}")
        print(response.json())
        return response

    def reduce_stock_quantity(self, stock_id, reduce_amount, delay=5):
        params = {"quantity": reduce_amount, "delay": delay}
        reduce_response = self.client.put(f"{self.base_url}{Endpoints.STOCK_ENDPOINT}/{stock_id}/reduce", params=params)
        return reduce_response

    def get_stock_by_product_id(self, product_id):
        response = self.client.get(f"{self.base_url}{Endpoints.STOCK_ENDPOINT}/{product_id}")
        return response
