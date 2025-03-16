import uuid
import asyncio

# In-memory task store to track long-running operations
task_store = {}


def create_task():
    """Generate a new task ID and mark it as 'processing'."""
    task_id = str(uuid.uuid4())  # Generate a unique ID
    task_store[task_id] = "processing"
    return task_id


def update_task_status(task_id, status):
    """Update the task status (e.g., 'completed' or 'failed')."""
    if task_id in task_store:
        task_store[task_id] = status


async def long_running_update(task_id, seconds):
    """Simulate a long-running task."""
    await asyncio.sleep(seconds)  # Simulate delay
    update_task_status(task_id, "completed")
