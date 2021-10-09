from typing import List

from fastapi import APIRouter

from app.dtos.schemas import Url, Configuration, Statistics

router = APIRouter(
    prefix="/",
    tags=["url"],
    responses={404: {"description": "Not found"}},
)


@router.post('', response_model=Url)
def create_short_url(url: str, configuration: Configuration):
    # RETURN SHORT URL AND SMTH ABOUT IT
    pass


# NEED AUTH
@router.delete('/{short_url}')
def delete_short_url(short_url: str):
    pass


# REDIRECT
@router.get('/{short_url}')
def follow_link(short_url: str):
    pass


# NEED AUTH
@router.get('/{short_url}/stats', response_model=List[Statistics])
def get_all_stats(short_url: str):
    pass
