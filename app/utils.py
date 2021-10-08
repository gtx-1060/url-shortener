import os

from dotenv import load_dotenv


def load_env_variables():
    load_dotenv()


def get_db_variables() -> dict:
    with os.environ as env:
        my_vars = \
            {
                'USER': env.get('DB_USER'),
                'PASSWORD': env.get('DB_PASSWORD'),
                'HOST': env.get('DB_HOST'),
                'NAME': env.get('DB_NAME')
            }
    return my_vars
