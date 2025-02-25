from handlers.tasks import router as task_router
from handlers.users import router as user_router
from handlers.auth import router as auth_router

routers = [task_router, user_router, auth_router]