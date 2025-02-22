from database import get_db_session
from cache import get_redis_connection
from repository import TaskRepository, TaskCache
from service import TaskService
from fastapi import Depends

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)

def get_tasks_cache() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository), 
        task_cache: TaskCache = Depends(get_tasks_cache)
        ) -> TaskService:
    return TaskService(task_repository, task_cache)