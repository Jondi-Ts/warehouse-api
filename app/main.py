from fastapi import FastAPI, Request
import time
from app.database import engine, Base
from app.routes.products_route import get_product_router
from app.routes.stock_route import get_stock_router
from app.routes.warehouse_route import get_warehouse_router
from app.logging_config import logger
from fastapi import BackgroundTasks
from app.celery_worker import process_long_task
from celery.result import AsyncResult
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
        f"REQUEST: {request.client.host} {request.method} {request.url.path} - Body: {request_body.decode('utf-8') if request_body else 'No Body'}"
    )

    response = await call_next(request)

    duration = round(time.time() - start_time, 4)
    logger.info(
        f"RESPONSE: {request.client.host} {request.method} {request.url.path} - {response.status_code} ({duration}s)")

    return response


app.include_router(get_product_router())
app.include_router(get_stock_router())
app.include_router(get_warehouse_router())


@app.post("/start-task/{seconds}")
@app.post("/start-task/{seconds}")
async def start_task(seconds: int, background_tasks: BackgroundTasks):
    """Starts a long-running task asynchronously."""
    task = process_long_task.apply_async(args=[seconds])
    return {"task_id": task.id, "status": "Task started"}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """Checks the status of a Celery task."""
    result = AsyncResult(task_id)  # Correct usage
    return {"task_id": task_id, "status": result.status, "result": result.result}

logger.info("Warehouse API started successfully!")
