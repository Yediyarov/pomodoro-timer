from sqlalchemy.orm import Session
from sqlalchemy import select

from schema.task import TaskSchema, TaskCreateSchema
from database.models import Task, Category

class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> TaskSchema:
        task: Task = self.db_session.execute(
            select(Task).where(Task.id == task_id)
        ).scalar_one()
        return TaskSchema.model_validate(task)

    def get_all_tasks(self) -> list[TaskSchema]:
        tasks: list[Task] = self.db_session.execute(select(Task)).scalars().all()
        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, task: TaskCreateSchema) -> TaskSchema:
        task_model = Task(**task.model_dump())
        self.db_session.add(task_model)
        self.db_session.commit()
        return TaskSchema.model_validate(task_model)

    def update_task(self, task_id: int, task: TaskSchema) -> TaskSchema:
        existing_task = self.db_session.get(Task, task_id)
        if not existing_task:
            raise ValueError(f"Task with id {task_id} not found")
        
        for field, value in task.model_dump().items():
            setattr(existing_task, field, value)

        self.db_session.commit()
        self.db_session.refresh(existing_task)
        return TaskSchema.model_validate(existing_task)
        
    def delete_task(self, task_id: int) -> TaskSchema:
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        # Create TaskSchema before deletion
        task_schema = TaskSchema.model_validate(task)
        
        self.db_session.delete(task)
        self.db_session.commit()
        
        return task_schema

    def get_task_by_category(self, category_name: str) -> list[TaskSchema]:
        query = select(Task).join(Category, Task.category_id == Category.id).where(Category.name == category_name)
        with self.db_session as session:
            tasks: list[Task] = session.execute(query).scalars().all()
            return tasks