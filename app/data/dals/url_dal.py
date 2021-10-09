from sqlalchemy.future import select

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Url
from app.dtos.schemas import Configuration
from app.exceptions import ItemNotFoundException


class UrlDAL(ObjectDAL):

    @staticmethod
    async def chk_val(val):
        if val is None:
            raise ItemNotFoundException(type(val))
        return val

    async def get_url(self, short_url: str):
        query = select(Url).where(Url.shorted_url == short_url)
        result = await self.session.execute(query)
        return await UrlDAL.chk_val(result.scalars().first())

    async def create_url(self, url: str, configuration: Configuration):
        pass

