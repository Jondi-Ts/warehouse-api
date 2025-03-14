from sqlalchemy.orm import Session
from app import models, schemas


def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stock(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Stock).offset(skip).limit(limit).all()


def get_stock_by_product_id(db: Session, product_id: int):
    return db.query(models.Stock).filter(models.Stock.product_id == product_id).first()


def get_stock_by_id(db: Session, stock_id: int):
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()


def reduce_stock(db: Session, stock_id: int, quantity: int):
    db_stock = get_stock_by_id(db, stock_id)
    if db_stock is None:
        return None

    if db_stock.quantity < quantity:
        return "Not enough stock"

    db_stock.quantity -= quantity
    db.commit()
    db.refresh(db_stock)
    return db_stock


def delete_stock(db: Session, stock_id: int):
    db_stock = get_stock_by_id(db, stock_id)
    if db_stock is None:
        return None

    db.delete(db_stock)
    db.commit()
    return db_stock


def get_products_below_threshold(db: Session, minimum_quantity: int):
    return db.query(models.Stock).filter(models.Stock.quantity < minimum_quantity).all()
