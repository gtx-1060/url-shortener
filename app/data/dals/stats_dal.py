from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Url, Configuration, Statistics
from app.dtos.schemas import Configuration as ConfSchema, Url as UrlSchema
from app.exceptions import BaseHTTPException


class UrlStatsDAL(ObjectDAL):

    async def get_url_stats_of_user(self, user_id: int) -> List[Statistics]:
        query = select(Statistics).where(Statistics.owner_id == user_id)
        result = (await self.session.execute(query)).scalars().all()
        if result is None:
            return []
        return result
