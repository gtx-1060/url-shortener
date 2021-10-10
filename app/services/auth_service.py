from datetime import timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.dals.user_dal import UserDAL
from app.data.models import User
from app.dtos.schemas import TokenData as TokenDataSchema, TokenData
from app.exceptions import BaseHTTPException
from app.services.bearer_oauth_service import MyOAuth2PasswordBearer
from app.utils import generate_jwt, data_from_jwt, verify_hashed, get_str_hash

oauth2_scheme = MyOAuth2PasswordBearer(tokenUrl='/user')


def create_jwt_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    if not expires_delta:
        expires_delta = timedelta(days=30)
    payload = {'id': user.id, 'scope': 'user'}
    encoded_jwt = generate_jwt(payload, expires_delta)
    return encoded_jwt


def decode_token(token: str) -> TokenDataSchema:
    payload = data_from_jwt(token)
    if payload is None:
        raise BaseHTTPException(403, 'access token is wrong or expired')
    user_id: int = int(payload.get("id"))
    if user_id is None:
        raise BaseHTTPException(405, 'wrong access token')
    return TokenData(user_id=user_id)


def try_auth_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[TokenDataSchema]:
    if token is None:
        return None
    return decode_token(token)


def auth_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenDataSchema:
    if token is None:
        raise BaseHTTPException(403, 'token header is empty')
    return decode_token(token)


def login_or_reg_user(db: Session, username: str, password: str) -> str:
    dal = UserDAL(db)
    exited_user = dal.get_user_by_name_or_null(username)
    if exited_user:
        if not verify_hashed(exited_user.password, password):
            raise BaseHTTPException(403, 'wrong password')
        return create_jwt_token(exited_user)
    user = dal.create_user(username, get_str_hash(password))
    return create_jwt_token(user)
