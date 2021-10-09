from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import utils

v = utils.get_db_variables()
SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{v["USER"]}:{v["PASSWORD"]}@{v["HOST"]}/{v["NAME"]}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(expire_on_commit=False, bind=engine, class_=AsyncSession)

AsyncBase = declarative_base()
