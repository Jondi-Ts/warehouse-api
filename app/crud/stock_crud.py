from sqlalchemy.orm import Session
from app import models, schemas


class StockCRUD:
    def __init__(self, db: Session):
        self.db = db  #

    def create_stock(self, stock: schemas.StockCreate):
        db_stock = models.Stock(**stock.dict())
        self.db.add(db_stock)
        self.db.commit()
        self.db.refresh(db_stock)
        return db_stock

    def get_stock(self, skip: int = 0, limit: int = 10):
        return self.db.query(models.Stock).offset(skip).limit(limit).all()

    def get_stock_by_product_id(self, product_id: int):
        return self.db.query(models.Stock).filter(models.Stock.product_id == product_id).first()

    def get_stock_by_id(self, stock_id: int):
        return self.db.query(models.Stock).filter(models.Stock.id == stock_id).first()

    def reduce_stock(self, stock_id: int, quantity: int):
        db_stock = self.get_stock_by_id(stock_id)
        if db_stock is None:
            return None

        if db_stock.quantity < quantity:
            return "Not enough stock"

        db_stock.quantity -= quantity
        self.db.commit()
        self.db.refresh(db_stock)
        return db_stock

    def delete_stock(self, stock_id: int):
        db_stock = self.get_stock_by_id(stock_id)
        if db_stock is None:
            return None

        self.db.delete(db_stock)
        self.db.commit()
        return db_stock

    def get_products_below_threshold(self, minimum_quantity: int):
        return self.db.query(models.Stock).filter(models.Stock.quantity < minimum_quantity).all()
