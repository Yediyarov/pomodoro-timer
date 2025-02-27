from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None 
    email: str | None = None
    name: str | None = None
    google_access_token: str | None = None