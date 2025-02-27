from fastapi import APIRouter
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserRegisterSchema
from app.users.user_profile.service import UserService
from app.dependency import get_user_service
from typing import Annotated
from fastapi import Depends


router = APIRouter(prefix="/user", tags=["users"])

@router.post("/", response_model=UserLoginSchema)
async def register(body: UserRegisterSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body.username, body.password)