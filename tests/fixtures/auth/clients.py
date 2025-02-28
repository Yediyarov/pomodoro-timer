from app.settings import Settings
from httpx import AsyncClient
from dataclasses import dataclass
import pytest

@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_access_token(code)
        return {'fake_access_token': access_token}

    async def _get_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=AsyncClient())