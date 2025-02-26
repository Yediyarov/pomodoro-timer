from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from schema.task import TaskSchema, TaskCreateSchema
from models import Task, Category
from dataclasses import dataclass

@dataclass
class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int) -> TaskSchema:
        task: Task = (await self.db_session.execute(
            select(Task).where(Task.id == task_id)
        )).scalar_one()
        return TaskSchema.model_validate(task)

    async def get_all_tasks(self) -> list[TaskSchema]:
        tasks: list[Task] = (await self.db_session.execute(select(Task))).scalars().all()
        return [TaskSchema.model_validate(task) for task in tasks]

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = (
            insert(Task)
            .values(title=task.title, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id)
            .returning(Task.id)
        )
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return task_id

    async def update_task(self, task_id: int, task: TaskSchema) -> TaskSchema:
        existing_task = await self.db_session.get(Task, task_id)
        if not existing_task:
            raise ValueError(f"Task with id {task_id} not found")
        
        for field, value in task.model_dump().items():
            setattr(existing_task, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(existing_task)
        return TaskSchema.model_validate(existing_task)
        
    async def delete_task(self, task_id: int) -> TaskSchema:
        task = await self.db_session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        # Create TaskSchema before deletion
        task_schema = TaskSchema.model_validate(task)
        
        await self.db_session.delete(task)
        await self.db_session.commit()
        
        return task_schema

    async def get_task_by_category(self, category_name: str) -> list[TaskSchema]:
        query = select(Task).join(Category, Task.category_id == Category.id).where(Category.name == category_name)
        async with self.db_session as session:
            tasks: list[Task] = (await session.execute(query)).scalars().all()
            return tasks