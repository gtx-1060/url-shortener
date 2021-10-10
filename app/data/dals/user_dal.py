from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Url, Configuration, Statistics, User
from app.dtos.schemas import Configuration as ConfSchema, Url as UrlSchema
from app.exceptions import BaseHTTPException


class UserDAL(ObjectDAL):

    def get_user(self, user_id: int) -> User:
        user = self.session.query(User).filter(User.id == user_id).first()
        return await UserDAL.chk_val(user)

    def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

