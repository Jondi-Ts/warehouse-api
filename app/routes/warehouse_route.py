from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database
from app.crud.warehouse_crud import WarehouseCRUD


class WarehouseRouter:
    def __init__(self):
        self.router = APIRouter()
        self.warehouse_crud_class = WarehouseCRUD

        self.router.add_api_route("/warehouse/stats", self.get_warehouse_statistics, methods=["GET"])
        self.router.add_api_route("/warehouse/report/", self.generate_report, methods=["GET"])

    def get_warehouse_statistics(self, db: Session = Depends(database.get_db)):
        warehouse_crud = self.warehouse_crud_class(db)

        total_products = warehouse_crud.get_total_products()
        total_stock = warehouse_crud.get_total_stock()
        low_stock_count = warehouse_crud.get_low_stock_count()
        low_stock_alerts = warehouse_crud.get_low_stock_alerts()
        out_of_stock_products = warehouse_crud.get_out_of_stock_products()

        return {
            "total_products": total_products,
            "total_stock": total_stock,
            "low_stock_products": low_stock_count,
            "out_of_stock_products": len(out_of_stock_products),
            "low_stock_alerts": low_stock_alerts,
            "out_of_stock_list": out_of_stock_products
        }

    def generate_report(self, db: Session = Depends(database.get_db)):
        return self.warehouse_crud_class(db).get_all_stock_data()



def get_warehouse_router():
    return WarehouseRouter().router
