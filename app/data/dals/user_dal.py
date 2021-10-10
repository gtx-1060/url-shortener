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
        return UserDAL.chk_val(user)

    def get_user_by_name_or_null(self, username: str) -> Optional[User]:
        user = self.session.query(User).filter(User.username == username).first()
        return user

    def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password=password_hash)
        if self.session.query(User).filter(User.username == username).first():
            raise BaseHTTPException(400, "user with the same name already registered")
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

