import os
import sys
from datetime import datetime
from typing import Optional
from jose import jwt, JWTError

from dotenv import load_dotenv
from passlib.context import CryptContext
from starlette.requests import Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"


def load_env_variables(path: Optional[str] = None):
    if path:
        path = os.path.abspath(path)
        load_dotenv(path)
        return
    load_dotenv()


def get_db_variables() -> dict:
    env = os.environ
    my_vars = \
        {
            'USER': env.get('DB_USER'),
            'PASSWORD': env.get('DB_PASSWORD'),
            'HOST': env.get('DB_HOST'),
            'NAME': env.get('DB_NAME')
        }
    return my_vars


def get_db(request: Request):
    return request.state.db


def data_from_jwt(token: str) -> Optional[dict]:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except JWTError:
        return None


def get_str_hash(string: str) -> str:
    return pwd_context.hash(string)


def verify_hashed(string_hash: str, string: str) -> bool:
    return pwd_context.verify(string, string_hash)


def generate_jwt(payload: dict, expires_delta) -> str:
    expire = datetime.utcnow() + expires_delta
    payload['exp'] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)