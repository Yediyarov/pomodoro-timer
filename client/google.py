from dataclasses import dataclass
from settings import Settings
import requests
from schema import GoogleAuthSchema

@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> GoogleAuthSchema :
        access_token = self._get_access_token(code)
        user_info = requests.get(
            self.settings.GOOGLE_USER_INFO_URL, 
            headers={"Authorization": f"Bearer {access_token}"})
        return GoogleAuthSchema(**user_info.json(), access_token=access_token)
    
    def _get_access_token(self, code: str) -> str:
        data ={
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]
    
   