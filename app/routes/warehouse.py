
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, crud
from app.crud import warehouse_crud as crud

router = APIRouter()


#
@router.get("/warehouse/stats")
def get_warehouse_statistics(db: Session = Depends(database.get_db)):
    total_products = crud.get_total_products(db)
    total_stock = crud.get_total_stock(db)
    low_stock_count = crud.get_low_stock_count(db)
    low_stock_alerts = crud.get_low_stock_alerts(db)
    out_of_stock_products = crud.get_out_of_stock_products(db)  # ✅ Include out-of-stock details

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock_products": low_stock_count,
        "out_of_stock_products": len(out_of_stock_products),  # ✅ Keep count for summary
        "low_stock_alerts": low_stock_alerts,
        "out_of_stock_list": out_of_stock_products  # ✅ Include list of out-of-stock products
    }


@router.get("/warehouse/report/")
def generate_report(db: Session = Depends(database.get_db)):
    stock_data = crud.get_all_stock_data(db)
    return stock_data
