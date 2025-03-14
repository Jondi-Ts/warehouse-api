from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database
from app.crud.warehouse_crud import WarehouseCRUD


class WarehouseRouter:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.router = APIRouter()
        self.db = db
        self.warehouse_crud = WarehouseCRUD(self.db)

        self.router.add_api_route("/warehouse/stats", self.get_warehouse_statistics, methods=["GET"])
        self.router.add_api_route("/warehouse/report/", self.generate_report, methods=["GET"])

    def get_warehouse_statistics(self):
        total_products = self.warehouse_crud.get_total_products()
        total_stock = self.warehouse_crud.get_total_stock()
        low_stock_count = self.warehouse_crud.get_low_stock_count()
        low_stock_alerts = self.warehouse_crud.get_low_stock_alerts()
        out_of_stock_products = self.warehouse_crud.get_out_of_stock_products()

        return {
            "total_products": total_products,
            "total_stock": total_stock,
            "low_stock_products": low_stock_count,
            "out_of_stock_products": len(out_of_stock_products),
            "low_stock_alerts": low_stock_alerts,
            "out_of_stock_list": out_of_stock_products
        }

    def generate_report(self):
        return self.warehouse_crud.get_all_stock_data()


warehouse_router = WarehouseRouter().router
