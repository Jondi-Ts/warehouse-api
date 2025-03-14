from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud.stock_crud import StockCRUD
from app.crud.products_crud import ProductCRUD


class StockRouter:
    def __init__(self):
        self.router = APIRouter()
        self.stock_crud_class = StockCRUD  # ✅ Store only the class, not an instance
        self.product_crud_class = ProductCRUD  # ✅ Store only the class, not an instance

        self.router.add_api_route("/stock/", self.create_stock, methods=["POST"])
        self.router.add_api_route("/stock/", self.get_stock, methods=["GET"])
        self.router.add_api_route("/stock/{product_id}", self.get_stock_by_product_id, methods=["GET"])
        self.router.add_api_route("/stock/{stock_id}/reduce", self.reduce_stock, methods=["PUT"])
        self.router.add_api_route("/stock/{stock_id}", self.delete_stock, methods=["DELETE"])
        self.router.add_api_route("/stock/below-threshold/", self.get_low_stock_products, methods=["GET"])

    def create_stock(self, stock: schemas.StockCreate, db: Session = Depends(database.get_db)):
        product_crud = self.product_crud_class(db)  # ✅ Inject fresh session per request
        stock_crud = self.stock_crud_class(db)

        db_product = product_crud.get_product_by_id(stock.product_id)
        if not db_product:
            raise HTTPException(status_code=400, detail="Product does not exist")

        return stock_crud.create_stock(stock)

    def get_stock(self, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
        return self.stock_crud_class(db).get_stock(skip, limit)

    def get_stock_by_product_id(self, product_id: int, db: Session = Depends(database.get_db)):
        db_stock = self.stock_crud_class(db).get_stock_by_product_id(product_id)
        if db_stock is None:
            raise HTTPException(status_code=404, detail="Stock entry not found")
        return db_stock

    def reduce_stock(self, stock_id: int, quantity: int, db: Session = Depends(database.get_db)):
        stock_crud = self.stock_crud_class(db)
        db_stock = stock_crud.get_stock_by_id(stock_id)

        if not db_stock:
            raise HTTPException(status_code=404, detail="Stock entry not found")

        if db_stock.quantity < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        db_stock.quantity -= quantity
        db.commit()
        db.refresh(db_stock)
        return db_stock

    def delete_stock(self, stock_id: int, db: Session = Depends(database.get_db)):
        db_stock = self.stock_crud_class(db).delete_stock(stock_id)
        if db_stock is None:
            raise HTTPException(status_code=404, detail="Stock entry not found")
        return db_stock

    def get_low_stock_products(self, minimum_quantity: int = 10, db: Session = Depends(database.get_db)):
        return self.stock_crud_class(db).get_products_below_threshold(minimum_quantity)


def get_stock_router():
    return StockRouter().router
