from faker import Faker
import random

fake = Faker()


def generate_mock_product():
    return {
        "name": fake.word().capitalize(),
        "price": round(random.uniform(10.0, 1000.0), 2),
        "category": fake.random_element(elements=["Electronics", "Clothing", "Food", "Furniture", "Toys"]),
        "manufacturer": fake.company()
    }

# Generate a single mock record
