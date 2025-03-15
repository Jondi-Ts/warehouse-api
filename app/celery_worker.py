from celery import Celery

celery = Celery(
    "warehouse_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def process_long_task(duration: int):
    import time
    time.sleep(duration)
    return f"Task completed after {duration} seconds"
