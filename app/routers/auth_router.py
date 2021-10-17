from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.data.dals.user_dal import UserDAL
from app.dtos.schemas import User
from app.services import auth_service
from app.services.auth_service import auth_user
from app.utils import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


# login if user exists or register if not
@router.post('')
def login_user(form: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    token = auth_service.login_or_reg_user(db, form.username, form.password)
    return {"access_token": token, "token_type": "bearer"}


# returns some user data
# indicates if jwt token is valid
@router.get('/me', response_model=User)
def get_me(auth_data=Depends(auth_user), db=Depends(get_db)):
    dal = UserDAL(db)
    return dal.get_user(auth_data.user_id)
