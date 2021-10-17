from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Path
from starlette.responses import Response, RedirectResponse

from app.data.dals.stats_dal import UrlStatsDAL
from app.data.dals.url_dal import UrlDAL
from app.dtos.privacy_modes import PrivacyModes
from app.dtos.schemas import Url, Configuration, Statistics
from app.exceptions import BaseHTTPException
from app.services.auth_service import try_auth_user, auth_user
from app.services.url_shorter_sevice import UrlShorter
from app.utils import get_db

router = APIRouter(
    prefix="/s",
    tags=["url"],
    responses={404: {"description": "Not found"}},
)


@router.post('', response_model=Url)
def create_short_url(url: str, configuration: Configuration, auth_data=Depends(try_auth_user), db=Depends(get_db)):
    if configuration and not auth_data:
        raise BaseHTTPException(403, "Auth to use your own custom url configuration")
    dal = UrlDAL(db)
    shorter = UrlShorter()
    short_url = shorter.get_short_url_part()
    owner_id = None
    if auth_data:
        owner_id = auth_data.user_id
    return dal.create_url(url, short_url, owner_id, configuration)


@router.delete('/{short_url}')
def delete_short_url(short_url: str = Path(..., ), auth_data=Depends(auth_user), db=Depends(get_db)):
    dal = UrlDAL(db)
    dal.remove_url(short_url)
    return Response(status_code=200)


# REDIRECT
@router.get('/{short_url}')
def follow_link(short_url: str = Path(..., regex='^$'), db=Depends(get_db)):
    url_dal = UrlDAL(db)
    url = url_dal.get_url(short_url)
    stats_dal = UrlStatsDAL(db)
    stats_dal.update_stats(url.id, 1, datetime.now())
    print(url.original_url)
    return RedirectResponse(url=url.original_url)


@router.get('/{short_url}/stats', response_model=Statistics)
def get_all_stats(short_url: str, auth_data=Depends(auth_user), db=Depends(get_db)):
    url_dal = UrlDAL(db)
    url = url_dal.get_url(short_url)
    if url.configuration.privacy != PrivacyModes.PUBLIC and url.statistics.owner_id != auth_data.user_id:
        raise BaseHTTPException(403, "not enough permissions")
    return url.statistics
