from fastapi import APIRouter, Depends
from schema import TaskSchema, TaskCreateSchema
from dependency import get_task_service
from service import TaskService
from typing import Annotated

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.get_all_tasks()


@router.post("/", response_model=TaskSchema)
async def create_task(
    task: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.create_task(task)


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task: TaskSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.update_task(task_id, task)


@router.delete("/{task_id}", response_model=TaskSchema)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.delete_task(task_id)