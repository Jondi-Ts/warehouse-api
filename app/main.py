from fastapi import FastAPI, Request
import time
from app.database import engine, Base
from app.routes.products_route import get_product_router
from app.routes.stock_route import get_stock_router
from app.routes.warehouse_route import get_warehouse_router
from app.logging_config import logger

# ✅ Ensure database tables are created before starting
Base.metadata.create_all(bind=engine)

# ✅ Create FastAPI app
app = FastAPI(title="Warehouse API")


@app.middleware("http")
async def log_request(request: Request, call_next):
    """Logs detailed API requests and responses."""
    start_time = time.time()  

    request_body = await request.body()
    logger.info(
        f"REQUEST: {request.client.host} {request.method} {request.url.path} - Body: {request_body.decode('utf-8') if request_body else 'No Body'} "
    )

    response = await call_next(request)

    duration = round(time.time() - start_time, 4)
    logger.info(f"📤 RESPONSE: {request.client.host} {request.method} {request.url.path} - {response.status_code} ({duration}s)")

    return response


app.include_router(get_product_router())
app.include_router(get_stock_router())
app.include_router(get_warehouse_router())


logger.info("🚀 Warehouse API started successfully!")
