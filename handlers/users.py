from fastapi import APIRouter
from schema import UserLoginSchema, UserRegisterSchema
from service import UserService
from dependency import get_user_service
from typing import Annotated
from fastapi import Depends


router = APIRouter(prefix="/user", tags=["users"])

@router.post("/", response_model=UserLoginSchema)
def register(body: UserRegisterSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)