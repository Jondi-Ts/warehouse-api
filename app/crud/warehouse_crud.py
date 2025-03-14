from sqlalchemy.orm import Session
from app import models
from sqlalchemy import func


def get_total_products(db: Session):
    return db.query(models.Product).count()


def get_total_stock(db: Session):
    return db.query(func.sum(models.Stock.quantity)).scalar() or 0


def get_low_stock_count(db: Session, threshold: int = 10):
    return (
        db.query(models.Stock.product_id)
            .join(models.Product, models.Stock.product_id == models.Product.id)
            .group_by(models.Stock.product_id)
            .having(func.sum(models.Stock.quantity) < threshold)
            .having(func.sum(models.Stock.quantity) > 0)
            .count()
    )


def get_out_of_stock_products(db: Session):
    out_of_stock_data = (
        db.query(
            models.Product.id.label("product_id"),
            models.Product.name.label("product_name"),
            models.Product.manufacturer.label("manufacturer")
        )
            .outerjoin(models.Stock, models.Product.id == models.Stock.product_id)
            .group_by(models.Product.id, models.Product.name, models.Product.manufacturer)
            .having(func.coalesce(func.sum(models.Stock.quantity), 0) == 0)
            .all()
    )

    return [
        {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "manufacturer": product.manufacturer
        }
        for product in out_of_stock_data
    ]


# stock data for reports


def get_all_stock_data(db: Session, low_stock_threshold: int = 10):
    stock_data = (
        db.query(
            models.Product.id.label("product_id"),
            models.Product.name.label("product_name"),
            models.Product.manufacturer.label("manufacturer"),
            func.sum(models.Stock.quantity).label("total_stock"),
            func.count(models.Stock.id).label("stock_entries"),
            func.sum(models.Stock.quantity * models.Product.price).label("total_stock_value")
        )
            .join(models.Stock, models.Product.id == models.Stock.product_id)
            .group_by(models.Product.id, models.Product.name, models.Product.manufacturer, models.Product.price)
            .all()
    )

    return [
        {
            "product_id": stock.product_id,
            "product_name": stock.product_name,
            "manufacturer": stock.manufacturer,
            "total_stock": stock.total_stock or 0,  # ✅ Ensure it doesn't return null
            "stock_entries": stock.stock_entries,
            "low_stock_alert": (stock.total_stock or 0) < low_stock_threshold,  # ✅ Fix null issue
            "total_stock_value": stock.total_stock_value or 0  # ✅ Show stock value
        }
        for stock in stock_data
    ]


def get_low_stock_alerts(db: Session, threshold: int = 10):
    low_stock_data = (
        db.query(
            models.Stock.product_id,
            models.Product.name,
            models.Product.manufacturer,
            func.sum(models.Stock.quantity).label("total_stock")
        )
            .join(models.Product, models.Product.id == models.Stock.product_id)
            .group_by(models.Stock.product_id, models.Product.name, models.Product.manufacturer)
            .having(func.sum(models.Stock.quantity) < threshold)
            .having(func.sum(models.Stock.quantity) > 0)
            .all()
    )

    return [
        {
            "product_id": stock.product_id,
            "product_name": stock.name,
            "manufacturer": stock.manufacturer,
            "total_stock": stock.total_stock
        }
        for stock in low_stock_data
    ]
