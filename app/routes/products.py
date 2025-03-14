from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud.products_crud import ProductCRUD


class ProductRouter:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.router = APIRouter()
        self.db = db
        self.product_crud = ProductCRUD(self.db)
        self.router.add_api_route("/products/", self.create_product, methods=["POST"])
        self.router.add_api_route("/products/", self.get_products, methods=["GET"])
        self.router.add_api_route("/products/{product_id}", self.get_product_by_id, methods=["GET"])
        self.router.add_api_route("/products/{product_id}", self.update_product, methods=["PUT"])
        self.router.add_api_route("/products/{product_id}", self.delete_product, methods=["DELETE"])

    def create_product(self, product: schemas.ProductCreate):
        return self.product_crud.create_product(product)

    def get_products(self, skip: int = 0, limit: int = 10):
        return self.product_crud.get_products(skip, limit)

    def get_product_by_id(self, product_id: int):
        product = self.product_crud.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def update_product(self, product_id: int, product_update: schemas.ProductUpdate):
        updated_product = self.product_crud.update_product(product_id, product_update)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product

    def delete_product(self, product_id: int):
        deleted_product = self.product_crud.delete_product(product_id)
        if not deleted_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return deleted_product


product_router = ProductRouter().router
