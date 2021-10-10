from datetime import datetime
from typing import List

from app.data.dals.object_dal import ObjectDAL
from app.data.models import Statistics


class UrlStatsDAL(ObjectDAL):

    def get_url_stats_of_user(self, user_id: int) -> List[Statistics]:
        stats = self.session.query(Statistics).first(Statistics.owner_id == user_id).all()
        if stats is None:
            return []
        return stats

    def update_stats(self, url_id: int, new_visits: int = None, last_visit: datetime = None):
        stats = self.session.query(Statistics).filter(Statistics.url_id == url_id).first()
        UrlStatsDAL.chk_val(stats)
        if new_visits:
            stats.visits += new_visits
        if last_visit:
            stats.last_visit = last_visit
        self.session.add(stats)
        self.session.commit()
