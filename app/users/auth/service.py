from app.users.auth.schema import UserLoginSchema
from dataclasses import dataclass
from app.users.user_profile.repository import UserRepository
from app.exeptions import UserNotFound, InvalidCredentials, TokenExpired, InvalidToken
from app.users.user_profile.models import UserProfile
from jose import jwt
from datetime import datetime as dt, timedelta
from datetime import timezone
from app.settings import Settings
from app.users.auth.client.google import GoogleClient
from app.users.user_profile.schema import UserCreateSchema

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    
    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFound
        if user.password != password:
            raise InvalidCredentials
        

    def generate_access_token(self,user_id: int) -> str:
        expires_data_unix = (dt.now(tz=timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expires_data_unix},
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM
            )
        return token
    
    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET, algorithms=[self.settings.JWT_ALGORITHM])
        except jwt.JWTError:
            raise InvalidToken
        if payload['exp'] < dt.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]
    
    
    def get_google_redirect_url(self) -> str:
        return self.settings.get_google_redirect_url
    
    async def google_auth(self, code: str) -> str:
        user_data = await self.google_client.get_user_info(code)
        if user := await self.user_repository.get_user_by_email(user_data.email):
            access_token = self.generate_access_token(user.id)
            return UserLoginSchema(id=user.id, access_token=access_token)

        google_user_data = UserCreateSchema(  
            email=user_data.email,
            name=user_data.name,
            google_access_token=user_data.access_token
        )
        created_user = await self.user_repository.create_user(google_user_data)
        access_token = self.generate_access_token(created_user.id)
        return UserLoginSchema(id=created_user.id, access_token=access_token)
