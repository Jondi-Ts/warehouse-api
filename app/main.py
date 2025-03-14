from fastapi import FastAPI

from app.database import engine, Base
from app.routes.products_route import product_router
from app.routes.stock_route import stock_router
from app.routes.warehouse_route import warehouse_router

#  Ensure database tables are created before starting


Base.metadata.create_all(bind=engine)

#  Initialize FastAPI app
app = FastAPI(title="Warehouse API")

#  Register product routes
app.include_router(product_router)
app.include_router(stock_router)
app.include_router(warehouse_router)
