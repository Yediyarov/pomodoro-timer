from fastapi import APIRouter
from schema import UserRegisterSchema, UserLoginSchema
from service import AuthService
from dependency import get_auth_service
from typing import Annotated
from fastapi import Depends
from exeptions import UserNotFound, InvalidCredentials
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginSchema)
def login(body: UserRegisterSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFound:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")