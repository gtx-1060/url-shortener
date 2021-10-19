from sqlalchemy.orm import Session

from app.data.dals.url_configuration_dal import UrlConfigurationDAL
from app.data.dals.url_dal import UrlDAL
from app.data.db.db import SyncSessionLocal
from app.data.models import Url
from app.services.schedule_service import _MyScheduler

TASK_ID = "url_expire_tacking"


def remove_all_urls_expired():
    db = SyncSessionLocal()
    conf_dal = UrlConfigurationDAL(db)
    url_ids_to_remove = conf_dal.get_expired_url_ids()
    urls_dal = UrlDAL(db)
    urls_dal.remove_urls(url_ids_to_remove)
    db.close()


def check_url_visits_remained(url: Url, db: Session):
    if url.configuration.live_until_visits is None:
        return
    if url.statistics.visits >= url.configuration.live_until_visits:
        dal = UrlDAL(db)
        dal.remove_url(url.shorted_url)


def start_expire_tracking(scheduler: _MyScheduler):
    if not scheduler.task_exists(TASK_ID):
        scheduler.plan_periodic_task(TASK_ID, 3600, remove_all_urls_expired, [])
