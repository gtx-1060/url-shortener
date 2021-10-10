from app import utils


def load_env_data():
    utils.load_env_variables('app/.env')


def create_tables():
    load_env_data()
    from app.data.db.db import SyncBase, engine
    from app.data.models import Url, User, Configuration, Statistics
    SyncBase.metadata.create_all(engine)


def drop_tables():
    load_env_data()
    from app.data.db.db import SyncBase, engine
    SyncBase.metadata.drop_all(engine)
