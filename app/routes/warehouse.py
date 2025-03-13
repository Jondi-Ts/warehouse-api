from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, crud

router = APIRouter()

#
@router.get("/warehouse/stats")
def get_warehouse_statistics(
    db: Session = Depends(database.get_db),
    low_stock_threshold: int = 10  # Default low stock threshold
):
    total_products = crud.get_total_products(db)
    total_stock = crud.get_total_stock(db)
    low_stock_count = crud.get_low_stock_count(db, low_stock_threshold)
    out_of_stock_count = crud.get_out_of_stock_count(db)

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock_products": low_stock_count,
        "out_of_stock_products": out_of_stock_count
    }
