from schema.user import UserLoginSchema
from dataclasses import dataclass
from repository import UserRepository
from exeptions import UserNotFound, InvalidCredentials
from repository.user import UserProfile
import uuid
@dataclass
class AuthService:
    user_repository: UserRepository
    
    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFound
        if user.password != password:
            raise InvalidCredentials
        
    @staticmethod
    def generate_access_token(user_id: int) -> str:
        return str(uuid.uuid4())
