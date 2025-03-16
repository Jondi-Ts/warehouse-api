from fastapi import FastAPI, Request, Response
import time
from app.database import engine, Base
from app.routes.products_route import get_product_router
from app.routes.stock_route import get_stock_router
from app.routes.taks_route import get_task_router
from app.routes.warehouse_route import get_warehouse_router
from app.logging_config import logger

# ✅ Ensure database tables are created before starting
Base.metadata.create_all(bind=engine)

# ✅ Create FastAPI app
app = FastAPI(title="Warehouse API")


@app.middleware("http")
async def log_request(request: Request, call_next):
    """Middleware to log API requests and responses properly."""
    start_time = time.time()

    # Read request body safely
    try:
        body = await request.body()
        body = body.decode("utf-8") if body else "No Body"
    except Exception:
        body = "Could not decode body"

    logger.info(f"REQUEST: {request.client.host} {request.method} {request.url.path} | Body: {body}")

    # Process the request and capture response
    response: Response = await call_next(request)
    duration = round(time.time() - start_time, 4)

    # ✅ Explicitly use ERROR for 4xx and 5xx responses
    if response.status_code >= 400:
        logger.error(
            f"RESPONSE: {request.client.host} {request.method} {request.url.path} | Status: {response.status_code} | Time: {duration}s")
    else:
        logger.info(
            f"RESPONSE: {request.client.host} {request.method} {request.url.path} | Status: {response.status_code} | Time: {duration}s")

    return response


app.include_router(get_product_router())
app.include_router(get_stock_router())
app.include_router(get_warehouse_router())
app.include_router(get_task_router())
logger.info("Warehouse API started successfully!")
