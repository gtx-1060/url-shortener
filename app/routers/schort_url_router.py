from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Path, Body
from starlette.responses import Response, RedirectResponse

from app.data.dals.stats_dal import UrlStatsDAL
from app.data.dals.url_dal import UrlDAL
from app.dtos.privacy_modes import PrivacyModes
from app.dtos.schemas import Url, Configuration, Statistics
from app.exceptions import BaseHTTPException
from app.services.auth_service import try_auth_user, auth_user
from app.services.url_lifecycle_service import check_url_visits_remained
from app.services.url_shorter_sevice import UrlShorter
from app.utils import get_db

router = APIRouter(
    tags=["url"],
    responses={404: {"description": "Not found"}},
)


# creates short url
# if user was authorized, he can use his custom url configuration
@router.post('/url', response_model=Url)
def create_short_url(url: str, configuration: Optional[Configuration] = Body(None),
                     auth_data=Depends(try_auth_user), db=Depends(get_db)):
    if configuration and not auth_data:
        raise BaseHTTPException(403, "Auth to use your own custom url configuration")
    dal = UrlDAL(db)
    shorter = UrlShorter()
    short_url = shorter.get_short_url_part()
    owner_id = None
    if auth_data:
        owner_id = auth_data.user_id
    return dal.create_url(url, short_url, owner_id, configuration)


# deletes url record from database
# user can delete only his own url
@router.delete('/{short_url}')
def delete_short_url(short_url: str = Path(..., regex=r'\w{6}'), auth_data=Depends(auth_user), db=Depends(get_db)):
    dal = UrlDAL(db)
    url = dal.get_url(short_url)
    if url.statistics.owner_id != auth_data.user_id:
        raise BaseHTTPException(403, "You can delete only your own url")
    dal.remove_url(short_url)
    return Response(status_code=200)


# redirect user using short_url as path item
@router.get('/{short_url}')
def follow_link(short_url: str = Path(..., regex=r'\w{6}'), db=Depends(get_db)):
    url_dal = UrlDAL(db)
    url = url_dal.get_url(short_url)
    stats_dal = UrlStatsDAL(db)
    stats_dal.update_stats(url.id, 1, datetime.now())
    check_url_visits_remained(url, db)
    return RedirectResponse(url=url.original_url)


# returns stats of url visits depends of access mode
@router.get('/{short_url}/stats', response_model=Statistics)
def get_all_stats(short_url: str, auth_data=Depends(auth_user), db=Depends(get_db)):
    url_dal = UrlDAL(db)
    url = url_dal.get_url(short_url)
    if url.configuration.privacy != PrivacyModes.PUBLIC and url.statistics.owner_id != auth_data.user_id:
        raise BaseHTTPException(403, "not enough permissions")
    return url.statistics
