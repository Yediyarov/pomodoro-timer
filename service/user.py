from dataclasses import dataclass
from repository import UserRepository
from schema import UserLoginSchema
from service import AuthService

@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username, password) -> UserLoginSchema:
        user = self.user_repository.create_user(username, password)
        access_token = self.auth_service.generate_access_token(user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)

    


