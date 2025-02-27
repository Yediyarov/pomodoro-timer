from dataclasses import dataclass
from app.settings import Settings
import httpx
from app.users.auth.schema import GoogleAuthSchema

@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleAuthSchema :
        access_token = await self._get_access_token(code)
        async with self.async_client as client:
            user_info = await client.get(
                self.settings.GOOGLE_USER_INFO_URL, 
                headers={"Authorization": f"Bearer {access_token}"})
        return GoogleAuthSchema(**user_info.json(), access_token=access_token)
    
    async def _get_access_token(self, code: str) -> str:
        data ={
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with self.async_client as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]
    
   