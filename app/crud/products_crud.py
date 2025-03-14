from sqlalchemy.orm import Session
from app import models, schemas


class ProductCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: schemas.ProductCreate):
        db_product = models.Product(
            name=product.name,
            price=product.price,
            category=product.category,
            manufacturer=product.manufacturer
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_products(self, skip: int = 0, limit: int = 10):
        return self.db.query(models.Product).offset(skip).limit(limit).all()

    def get_product_by_id(self, product_id: int):
        return self.db.query(models.Product).filter(models.Product.id == product_id).first()

    def update_product(self, product_id: int, product_update: schemas.ProductUpdate):
        db_product = self.get_product_by_id(product_id)
        if not db_product:
            return None
        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int):
        db_product = self.get_product_by_id(product_id)
        if not db_product:
            return None
        self.db.delete(db_product)
        self.db.commit()
        return db_product
