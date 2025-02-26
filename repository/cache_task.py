from redis import asyncio as Redis
from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.redis as redis:
            task_json = await redis.lrange("tasks", 0, -1)
            return [TaskSchema.model_validate_json(task) for task in task_json]

    async  def set_tasks(self, tasks: list[TaskSchema]):
        # First, clear existing tasks
        async with self.redis as redis:
            await redis.delete("tasks")
            # Convert tasks to JSON and push them one by one
            for task in tasks:
                await redis.rpush("tasks", task.model_dump_json())
