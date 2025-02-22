from dataclasses import dataclass
from repository.task import TaskRepository
from repository.cache_task import TaskCache
from schema.task import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_all_tasks(self) -> list[TaskSchema]:
        if task_cache := self.task_cache.get_tasks():
            return task_cache
        else:
            tasks = self.task_repository.get_all_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
        
    def get_task_by_category(self, category_name: str) -> list[TaskSchema]:
        if task_cache := self.task_cache.get_tasks_by_category(category_name):
            return task_cache
        else:
            tasks = self.task_repository.get_task_by_category(category_name)
            self.task_cache.set_tasks(tasks)
            return tasks
        
    def create_task(self, task: TaskCreateSchema) -> TaskSchema:
        # Create task in database
        created_task = self.task_repository.create_task(task)
        
        # Update cache with new task list
        tasks = self.task_repository.get_all_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_schema)
        
        return created_task
        
        