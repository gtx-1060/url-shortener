from datetime import datetime

from pydantic import BaseModel

from app.dtos.privacy_modes import PrivacyModes


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode=True


class Configuration(BaseModel):
    privacy: PrivacyModes
    bots_protect: bool
    live_until_date: datetime
    live_until_visits: int = None

    class Config:
        orm_mode = True


class Url(BaseModel):
    original_url: str
    shorted_url: str

    class Config:
        orm_mode = True


class Statistics(BaseModel):
    visits: int
    last_visit: datetime
    creation: datetime
    url: 'Url'

    class Config:
        orm_mode = True


class UrlComplete(Url):
    configuration: Configuration
    statistics: Statistics

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: int
