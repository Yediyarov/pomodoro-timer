from database import get_db_session
from cache import get_redis_connection
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService, AuthService
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from settings import Settings
from fastapi import security
from exeptions import InvalidToken, TokenExpired
from client.google import GoogleClient
import httpx

async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session=db_session)

async def get_tasks_cache() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

async def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository), 
        task_cache: TaskCache = Depends(get_tasks_cache)
        ) -> TaskService:
    return TaskService(task_repository, task_cache)

async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)

async  def get_settings() -> Settings:
    return Settings()

async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

async def get_google_client(
        settings: Settings = Depends(get_settings),
        async_client: httpx.AsyncClient = Depends(get_async_client)
        ) -> GoogleClient:
    return GoogleClient(settings, async_client)

async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        settings: Settings = Depends(get_settings),
        google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(user_repository, settings, google_client)

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository, auth_service)


reuseable_oauth2 = security.HTTPBearer()

async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service), 
        token: str = Depends(reuseable_oauth2)
        ) -> int:
    try:
        user_id = auth_service.get_user_id_from_token(token.credentials)
    except InvalidToken as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
