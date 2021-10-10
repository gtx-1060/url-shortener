from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Url, Configuration, Statistics, User
from app.dtos.schemas import Configuration as ConfSchema, Url as UrlSchema
from app.exceptions import BaseHTTPException


class UserDAL(ObjectDAL):

    async def get_user(self, user_id: int) -> User:
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)
        return await UserDAL.chk_val(result.scalars().first())

    async def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password=password_hash)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

