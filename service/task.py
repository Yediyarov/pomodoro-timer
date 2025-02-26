from dataclasses import dataclass
from repository.task import TaskRepository
from repository.cache_task import TaskCache
from schema.task import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_all_tasks(self) -> list[TaskSchema]:
        if task_cache := await self.task_cache.get_tasks():
            return task_cache
        else:
            tasks = await self.task_repository.get_all_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
        
    async def get_task_by_category(self, category_name: str) -> list[TaskSchema]:
        if task_cache := await self.task_cache.get_tasks_by_category(category_name):
            return task_cache
        else:
            tasks = await self.task_repository.get_task_by_category(category_name)
            await self.task_cache.set_tasks(tasks)
            return tasks
        
    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        # Create task in database
        created_task = await self.task_repository.create_task(body, user_id)
        
        # Update cache with new task list
        tasks = await self.task_repository.get_all_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)
        
        return created_task
        
    async def update_task(self, task_id: int, task: TaskSchema) -> TaskSchema:
        # Update task in database
        updated_task = await self.task_repository.update_task(task_id, task)
        
        # Update cache with new task list
        tasks = await self.task_repository.get_all_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)
        
        return updated_task
    
    async def delete_task(self, task_id: int) -> TaskSchema:
        # Delete task and get the deleted task data
        deleted_task = await self.task_repository.delete_task(task_id)
        
        # Update cache with new task list
        tasks = await self.task_repository.get_all_tasks()
        await self.task_cache.set_tasks(tasks)
        
        return deleted_task
