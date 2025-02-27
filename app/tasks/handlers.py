from fastapi import APIRouter, Depends
from app.tasks.schema import TaskSchema, TaskCreateSchema
from app.dependency import get_task_service, get_request_user_id
from app.tasks.service import TaskService
from typing import Annotated

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return await task_service.get_all_tasks()


@router.post("/", response_model=TaskSchema)
async def create_task(
    body : TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: Annotated[int, Depends(get_request_user_id)]
):
    return await task_service.create_task(body=body, user_id=user_id)


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task: TaskSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return await task_service.update_task(task_id, task)


@router.delete("/{task_id}", response_model=TaskSchema)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return await task_service.delete_task(task_id)