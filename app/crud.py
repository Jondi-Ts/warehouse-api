from sqlalchemy.orm import Session
from app import models, schemas


def create_product(db: Session, product: schemas.ProuctCreate):
    db_prodcut = models.Product(
        name=product.name,
        price=product.price,
        category=product.category,
        manufacturer=product.manufacturer
    )
    db.add(db_prodcut)
    db.commit()
    db.refresh(db_prodcut)
    return db_prodcut


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product


def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(
        product_id=stock.product_id,
        quantity=stock.quantity
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stock_by_product(db: Session, product_id: int):
    return db.query(models.Stock).filter(models.Stock.product_id == product_id).first()


def update_stock(db: Session, product_id: int, quantity: int):
    db_stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not db_stock:
        return None
    db_stock.quantity = quantity
    db.commit()
    db.refresh(db_stock)
    return db_stock


def delete_stock(db: Session, stock_id: int):
    db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if not db_stock:
        return None
    db.delete(db_stock)
    db.commit()
    return db_stock
