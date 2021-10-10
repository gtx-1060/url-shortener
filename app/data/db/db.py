from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import utils

utils.load_env_variables()
v = utils.get_db_variables()
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{v["USER"]}:{v["PASSWORD"]}@{v["HOST"]}/{v["NAME"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SyncBase = declarative_base()
