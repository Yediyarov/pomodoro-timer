from pydantic import BaseModel, ConfigDict

class GoogleAuthSchema(BaseModel):
    id: int | None = None
    email: str | None = None
    verified_email: bool | None = None
    name: str | None = None
    access_token: str | None = None


class UserLoginSchema(BaseModel):
    id: int
    access_token: str

    model_config = ConfigDict(from_attributes=True)
