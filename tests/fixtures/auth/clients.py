from app.settings import Settings
from httpx import AsyncClient
from dataclasses import dataclass
import pytest
from app.users.auth.schema import GoogleAuthSchema
from faker import Factory as FakerFactory

faker = FakerFactory.create()

@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: AsyncClient

    async def get_user_info(self, code: str) -> GoogleAuthSchema:
        access_token = await self._get_access_token(code)
        return google_user_info_data()

    async def _get_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=AsyncClient())


def google_user_info_data() -> GoogleAuthSchema:
    return GoogleAuthSchema(
        id=faker.random_int(),
        email=faker.email(),
        verified_email=faker.boolean(),
        name=faker.name(),
        access_token=faker.sha256()
    ) 