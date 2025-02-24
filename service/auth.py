from schema.user import UserLoginSchema
from dataclasses import dataclass
from repository import UserRepository
from exeptions import UserNotFound, InvalidCredentials
from repository.user import UserProfile

@dataclass
class AuthService:
    user_repository: UserRepository
    
    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFound
        if user.password != password:
            raise InvalidCredentials