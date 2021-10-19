from datetime import datetime

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Configuration


class UrlConfigurationDAL(ObjectDAL):

    def get_expired_url_ids(self):
        tnow = datetime.now()
        ids = self.session.query(Configuration.owner_id).join(Configuration.live_until_date) \
            .filter(Configuration.live_until_date < tnow).all()
        if ids is None:
            return []
        return ids
