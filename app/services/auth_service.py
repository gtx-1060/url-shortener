from datetime import timedelta
from typing import Optional

from fastapi import Depends

from app.dtos.schemas import User, TokenData
from app.exceptions import BaseHTTPException
from app.services.bearer_oauth_service import MyOAuth2PasswordBearer
from app.utils import generate_jwt, data_from_jwt


oauth2_scheme = MyOAuth2PasswordBearer(tokenUrl='/user/login')


def create_jwt_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    if not expires_delta:
        expires_delta = timedelta(days=30)
    payload = {'id': user.id, 'scope': 'user'}
    encoded_jwt = generate_jwt(payload, expires_delta)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    payload = data_from_jwt(token)
    if payload is None:
        raise BaseHTTPException(403, 'access token is wrong or expired')
    user_id: int = int(payload.get("id"))
    if user_id is None:
        raise BaseHTTPException(405, 'wrong access token')
    return TokenData(user_id=user_id)


def try_auth_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[TokenData]:
    if token is None:
        return None
    return decode_token(token)


def auth_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenData:
    if token is None:
        raise BaseHTTPException(403, 'token header is empty')
    return decode_token(token)
