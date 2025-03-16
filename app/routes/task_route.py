from fastapi import APIRouter, HTTPException
from app.task_manager import get_task_status


class TaskRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/tasks/{task_id}/status", self.get_task_status, methods=["GET"])

    def get_task_status(self, task_id: str):
        """Returns the status of a background task."""
        status = get_task_status(task_id)

        if status == "not found":
            raise HTTPException(status_code=404, detail="Task ID not found.")

        return {"task_id": task_id, "status": status}


def get_task_router():
    return TaskRouter().router
