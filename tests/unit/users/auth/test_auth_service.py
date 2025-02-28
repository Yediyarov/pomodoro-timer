from app.settings import Settings
from app.users.auth.service import AuthService
from jose import jwt
from datetime import datetime as dt, timedelta, timezone
from app.users.user_profile.models import UserProfile
from app.users.auth.schema import UserLoginSchema

async def test_get_google_redirect_url__success(auth_service:AuthService, settings:Settings):
    setting_google_redirect_url = settings.get_google_redirect_url
    auth_google_redirect_url = auth_service.get_google_redirect_url()
    
    assert auth_google_redirect_url == setting_google_redirect_url
    
    
async def test_get_google_redirect_url__fail(auth_service:AuthService):
    setting_google_redirect_url = 'https://google.com/'
    auth_google_redirect_url = auth_service.get_google_redirect_url()
    
    assert auth_google_redirect_url != setting_google_redirect_url
    

async def test_generate_access_token__success(auth_service:AuthService, settings:Settings):
    user_id = 1
    access_token = auth_service.generate_access_token(user_id)
    decode_access_token =  jwt.decode(access_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    decoded_user_id = decode_access_token.get('user_id')
    decoded_token_exp = dt.fromtimestamp(decode_access_token.get('exp'), tz=timezone.utc)
    
    assert decoded_user_id == user_id
    assert (decoded_token_exp - dt.now(tz=timezone.utc)) > timedelta(days=6)
    
    
async def test_get_user_id_from_token__success(auth_service:AuthService):
    user_id = str(1)
    access_token = auth_service.generate_access_token(user_id)
    decoded_user_id = auth_service.get_user_id_from_token(access_token)
    
    assert decoded_user_id == user_id
    
    
    
async def test_google_auth__success(auth_service:AuthService, user_profile:UserProfile):
    code = 'fake_code'
    user = await auth_service.google_auth(code=code)
    decoded_user_id = auth_service.get_user_id_from_token(user.access_token)

    assert isinstance(user, UserLoginSchema)
    assert user.id == decoded_user_id