from fastapi import APIRouter

from app.dtos.schemas import User

router = APIRouter(
    prefix="/user/",
    tags=["url"],
    responses={404: {"description": "Not found"}},
)


@router.post('')
def login_user():
    pass


# NEED AUTH
@router.post('me', response_model=User)
def get_me():
    pass
