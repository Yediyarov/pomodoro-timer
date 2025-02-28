from app.settings import Settings
from app.users.auth.service import AuthService
import pytest


@pytest.fixture
def auth_service(google_client, user_repository):
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client , 
    )