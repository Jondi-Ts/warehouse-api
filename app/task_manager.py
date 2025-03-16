import uuid

task_store = {}


def create_task():
    """Generates a unique task ID and sets initial status to 'processing'."""
    task_id = str(uuid.uuid4())
    task_store[task_id] = "processing"
    return task_id


def update_task_status(task_id: str, status: str):
    """Updates the task status to 'completed' or 'failed'."""
    if task_id in task_store:
        task_store[task_id] = status


def get_task_status(task_id: str):
    """Retrieves the status of a background task."""
    return task_store.get(task_id, "not found")
