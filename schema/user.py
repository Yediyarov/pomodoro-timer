from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    id: int
    access_token: str


class UserRegisterSchema(BaseModel):
    username: str
    password: str
