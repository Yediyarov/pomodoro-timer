from sqlalchemy.orm import Session
from sqlalchemy import select

from schema.task import TaskSchema
from database.models import Task, Category

class TaskRepository:

    def __init__(self, db_session:Session):
        self.db_session = db_session

    def get_task(self, task_id:int) -> TaskSchema:
        with self.db_session as session:
            task: Task = session.execute(select(Task).where(Task.id == task_id)).scalar_one()
        return TaskSchema.model_validate(task)

    def get_all_tasks(self) -> list[TaskSchema]:
        with self.db_session as session:
            tasks: list[Task] = session.execute(select(Task)).scalars().all()
        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, task: TaskSchema) -> TaskSchema:
        task_model = Task(**task.model_dump())
        with self.db_session as session:
            session.add(task_model)
            session.commit()
        return TaskSchema.model_validate(task_model)

    def update_task(self, task_id:int, task: TaskSchema) -> TaskSchema:
        with self.db_session as session:
            existing_task = session.get(Task, task_id)
            if not existing_task:
                raise ValueError(f"Task with id {task_id} not found")
            
            for field, value in task.model_dump().items():
                setattr(existing_task, field, value)

            session.commit()
            session.refresh(existing_task)

        return TaskSchema.model_validate(existing_task)
        
    def delete_task(self, task_id:int) -> None:
        with self.db_session as session:
            task = session.get(Task, task_id)
            if not task:
                raise ValueError(f"Task with id {task_id} not found")
            session.delete(task)
            session.commit()

    def get_task_by_category(self, category_name: str) -> list[TaskSchema]:
        query = select(Task).join(Category, Task.category_id == Category.id).where(Category.name == category_name)
        with self.db_session as session:
            tasks: list[Task] = session.execute(query).scalars().all()
            return tasks