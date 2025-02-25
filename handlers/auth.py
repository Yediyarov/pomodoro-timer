from fastapi import APIRouter
from schema import UserRegisterSchema, UserLoginSchema
from service import AuthService
from dependency import get_auth_service
from typing import Annotated
from fastapi import Depends
from exeptions import UserNotFound, InvalidCredentials
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginSchema)
def login(body: UserRegisterSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFound:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(url=redirect_url)

@router.get("/google")
async def google_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str):
    return auth_service.google_auth(code)