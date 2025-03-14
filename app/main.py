from fastapi import FastAPI

from app.database import engine, Base

# Ensure database tables are created before starting
from app.routes.products_route import get_product_router
from app.routes.stock_route import get_stock_router
from app.routes.warehouse_route import get_warehouse_router

Base.metadata.create_all(bind=engine)




app = FastAPI(title="Warehouse API")

# ✅ Register routes (without changing your structure)
app.include_router(get_product_router())
app.include_router(get_stock_router())
app.include_router(get_warehouse_router())
