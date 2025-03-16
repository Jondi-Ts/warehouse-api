import uuid
import asyncio
import logging

# Initialize Logger
logger = logging.getLogger("api_logger")

# In-memory task store
task_store = {}


def create_task():
    """Generates a unique task ID and sets initial status to 'processing'."""
    task_id = str(uuid.uuid4())
    task_store[task_id] = "processing"
    logger.info(f"Task {task_id} created and set to 'processing'.")
    return task_id


def update_task_status(task_id: str, status: str):
    """Updates the task status to 'completed' or 'failed'."""
    if task_id in task_store:
        task_store[task_id] = status
        logger.info(f"Task {task_id} updated to '{status}'.")
    else:
        logger.warning(f"Attempted to update non-existent task {task_id}.")


def get_task_status(task_id: str):
    """Retrieves the status of a background task."""
    status = task_store.get(task_id, "not found")
    logger.info(f"Task {task_id} status checked: {status}")
    return status


async def run_background_task(task_id: str, task_func, *args, **kwargs):
    """
    Runs any async function as a background task.

    :param task_id: Unique task identifier.
    :param task_func: The async function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    """
    logger.info(f"Starting background task {task_id} with function {task_func.__name__}.")

    try:
        await task_func(*args, **kwargs)
        update_task_status(task_id, "completed")
        logger.info(f"Task {task_id} completed successfully.")
    except Exception as e:
        update_task_status(task_id, "failed")
        logger.error(f"Task {task_id} failed due to error: {str(e)}")
