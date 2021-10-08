from sqlalchemy import create_engine

from app import utils


def load_env_data():
    utils.load_env_variables('app/.env')


def create_tables():
    load_env_data()

    from app.data.db.db import Base, SQLALCHEMY_DATABASE_URL
    from app.data.models import User, Url, Statistics, Configuration

    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
    Base.metadata.create_all(engine)


def drop_tables():
    load_env_data()

    from app.data.db.db import Base, SQLALCHEMY_DATABASE_URL
    from app.data.models import User, Url, Statistics, Configuration

    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
    Base.metadata.drop_all(engine)
