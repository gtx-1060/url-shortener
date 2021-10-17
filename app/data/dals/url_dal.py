from sqlalchemy import desc

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Url, Configuration, Statistics
from app.dtos.schemas import Configuration as ConfigurationSchema
from app.exceptions import ItemNotFoundException


class UrlDAL(ObjectDAL):

    def get_url(self, short_url: str) -> Url:
        url = self.session.query(Url).filter(Url.shorted_url == short_url).first()
        return UrlDAL.chk_val(url)

    def create_url(self, url: str, short_url: str, owner_id: int, configuration: ConfigurationSchema) -> Url:
        url = Url(shorted_url=short_url, original_url=url)
        self.session.add(url)
        self.session.commit()
        self.session.refresh(url)
        conf_model = Configuration(url_id=url.id)
        if configuration:
            conf_model.privacy = configuration.privacy
            conf_model.live_until_date = configuration.live_until_date
            conf_model.live_until_visits = configuration.live_until_visits
            conf_model.bots_protect = configuration.bots_protect
        self.session.add(conf_model)
        stats = Statistics(url_id=url.id)
        if owner_id:
            stats.owner_id = owner_id
        self.session.add(stats)
        self.session.commit()
        self.session.refresh(url)
        return url

    def remove_url(self, short_url: str):
        self.session.query(Url).filter(Url.shorted_url == short_url).delete()

    def get_last_url(self):
        return self.session.query(Url).order_by(desc(Url.id)).first()

    def get_all_short_urls(self):
        urls = self.session.query(Url.shorted_url).all()
        if not urls:
            return []
        return urls
