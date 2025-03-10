from fastapi import APIRouter
from app.users.user_profile.schema import UserRegisterSchema 
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.dependency import get_auth_service
from typing import Annotated
from fastapi import Depends
from app.exeptions import UserNotFound, InvalidCredentials
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginSchema)
async def login(body: UserRegisterSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFound:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = await auth_service.get_google_redirect_url()
    return RedirectResponse(url=redirect_url)

@router.get("/google")
async def google_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str):
    return await auth_service.google_auth(code)