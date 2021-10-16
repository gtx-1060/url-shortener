from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.env_variables_loader import env_variables as v


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{v["DB_USER"]}:{v["DB_PASSWORD"]}@{v["DB_HOST"]}/{v["DB_NAME"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SyncBase = declarative_base()
