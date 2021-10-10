from typing import List

from fastapi import APIRouter, Depends, Path

from app.dtos.schemas import Url, Configuration, Statistics
from app.services.auth_service import try_auth_user, auth_user

router = APIRouter(
    prefix="/s",
    tags=["url"],
    responses={404: {"description": "Not found"}},
)


@router.post('', response_model=Url)
def create_short_url(url: str, configuration: Configuration, auth_data=Depends(try_auth_user)):
    # RETURN SHORT URL AND SMTH ABOUT IT
    pass


@router.delete('/{short_url}')
def delete_short_url(short_url: str = Path(...,), auth_data=Depends(auth_user)):
    pass


# REDIRECT
@router.get('/{short_url}')
def follow_link(short_url: str = Path(...,)):
    pass


@router.get('/{short_url}/stats', response_model=Statistics)
def get_all_stats(short_url: str, auth_data=Depends(auth_user)):
    pass
