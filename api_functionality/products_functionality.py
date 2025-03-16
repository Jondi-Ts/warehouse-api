def create_product(client, base_url, product_data):
    response = client.post(f"{base_url}/products", json=product_data)
    return response
