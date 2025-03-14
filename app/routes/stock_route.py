from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud.stock_crud import StockCRUD
from app.crud.products_crud import ProductCRUD


class StockRouter:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.router = APIRouter()
        self.db = db
        self.stock_crud = StockCRUD(self.db)
        self.product_crud = ProductCRUD(self.db)

        self.router.add_api_route("/stock/", self.create_stock, methods=["POST"])
        self.router.add_api_route("/stock/", self.get_stock, methods=["GET"])
        self.router.add_api_route("/stock/{product_id}", self.get_stock_by_product_id, methods=["GET"])
        self.router.add_api_route("/stock/{stock_id}/reduce", self.reduce_stock, methods=["PUT"])
        self.router.add_api_route("/stock/{stock_id}", self.delete_stock, methods=["DELETE"])
        self.router.add_api_route("/stock/below-threshold/", self.get_low_stock_products, methods=["GET"])

    def create_stock(self, stock: schemas.StockCreate):
        db_product = self.product_crud.get_product_by_id(stock.product_id)
        if not db_product:
            raise HTTPException(status_code=400, detail="Product does not exist")

        return self.stock_crud.create_stock(stock)

    def get_stock(self, skip: int = 0, limit: int = 10):
        return self.stock_crud.get_stock(skip, limit)

    def get_stock_by_product_id(self, product_id: int):
        db_stock = self.stock_crud.get_stock_by_product_id(product_id)
        if db_stock is None:
            raise HTTPException(status_code=404, detail="Stock entry not found")
        return db_stock

    def reduce_stock(self, stock_id: int, quantity: int):
        db_stock = self.stock_crud.get_stock_by_id(stock_id)
        if not db_stock:
            raise HTTPException(status_code=404, detail="Stock entry not found")

        if db_stock.quantity < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        db_stock.quantity -= quantity
        self.db.commit()
        self.db.refresh(db_stock)
        return db_stock

    def delete_stock(self, stock_id: int):
        db_stock = self.stock_crud.delete_stock(stock_id)
        if db_stock is None:
            raise HTTPException(status_code=404, detail="Stock entry not found")
        return db_stock

    def get_low_stock_products(self, minimum_quantity: int = 10):
        return self.stock_crud.get_products_below_threshold(minimum_quantity)


stock_router = StockRouter().router
