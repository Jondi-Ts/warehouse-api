from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud.products_crud import ProductCRUD


class ProductRouter:
    def __init__(self):
        self.router = APIRouter()
        self.product_crud_class = ProductCRUD

        self.router.add_api_route("/products/", self.create_product, methods=["POST"])
        self.router.add_api_route("/products/", self.get_products, methods=["GET"])
        self.router.add_api_route("/products/{product_id}", self.get_product_by_id, methods=["GET"])
        self.router.add_api_route("/products/{product_id}", self.update_product, methods=["PUT"])
        self.router.add_api_route("/products/{product_id}", self.delete_product, methods=["DELETE"])

    def create_product(self, product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
        """✅ Creates a new product, ensuring no duplicates."""
        existing_product = self.product_crud_class(db).get_product_by_name(product.name)
        if existing_product:
            raise HTTPException(status_code=400, detail=f"Product '{product.name}' already exists.")

        return self.product_crud_class(db).create_product(product)

    def get_products(self, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
        products = self.product_crud_class(db).get_products(skip, limit)
        if not products:
            raise HTTPException(status_code=404, detail="No products found in the warehouse.")
        return products

    def get_product_by_id(self, product_id: int, db: Session = Depends(database.get_db)):
        product = self.product_crud_class(db).get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
        return product

    def update_product(self, product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
        updated_product = self.product_crud_class(db).update_product(product_id, product_update)
        if not updated_product:
            raise HTTPException(status_code=404, detail=f"Cannot update: Product ID {product_id} not found.")
        return updated_product

    def delete_product(self, product_id: int, db: Session = Depends(database.get_db)):

        deleted_product = self.product_crud_class(db).delete_product(product_id)
        if not deleted_product:
            raise HTTPException(status_code=404, detail=f"Cannot delete: Product ID {product_id} not found.")
        return deleted_product


# ✅ Cleaner router import
def get_product_router():
    return ProductRouter().router
