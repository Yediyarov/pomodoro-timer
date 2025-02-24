from dataclasses import dataclass
from repository import UserRepository
from schema import UserLoginSchema
import uuid

@dataclass
class UserService:
    user_repository: UserRepository
    
    def create_user(self, username, password) -> UserLoginSchema:
        access_token = self._generate_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(id=user.id, access_token=user.access_token)

    def _generate_access_token(self) -> str:
        return str(uuid.uuid4())



