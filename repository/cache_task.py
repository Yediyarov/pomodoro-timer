from redis import Redis
from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            task_json = redis.lrange("tasks", 0, -1)
            return [TaskSchema.model_validate_json(task) for task in task_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        # First, clear existing tasks
        with self.redis as redis:
            redis.delete("tasks")
            # Convert tasks to JSON and push them one by one
            for task in tasks:
                redis.rpush("tasks", task.model_dump_json())
