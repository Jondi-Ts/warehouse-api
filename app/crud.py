from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas


def create_product(db: Session, product: schemas.ProductCreate):
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
        return None  # ❌ Stock entry not found

    # ✅ Ensure stock does not go negative
    if db_stock.quantity < quantity:
        return "Not enough stock"  # ❌ Not enough stock available

    db_stock.quantity -= quantity
    db.commit()
    db.refresh(db_stock)
    return db_stock


def delete_stock(db: Session, stock_id: int):
    db_stock = get_stock_by_id(db, stock_id)
    if db_stock is None:
        return None  # ❌ Stock entry not found

    db.delete(db_stock)
    db.commit()
    return db_stock


def get_products_below_threshold(db: Session, minimum_quantity: int):
    return db.query(models.Stock).filter(models.Stock.quantity < minimum_quantity).all()


def get_total_products(db: Session):
    return db.query(models.Product).count()


def get_total_stock(db: Session):
    return db.query(func.sum(models.Stock.quantity)).scalar() or 0


def get_low_stock_count(db: Session, threshold: int):
    return db.query(models.Stock).filter(models.Stock.quantity < threshold).count()


def get_out_of_stock_count(db: Session):
    return db.query(models.Stock).filter(models.Stock.quantity == 0).count()
