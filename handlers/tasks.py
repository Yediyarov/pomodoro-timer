from fastapi import APIRouter, Depends
from schema import TaskSchema
from dependency import get_task_service
from service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_all_tasks()