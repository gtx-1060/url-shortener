import os
import sys
from typing import Optional

from dotenv import load_dotenv


def load_env_variables(path: Optional[str] = None):
    if path:
        path = os.path.abspath(path)
        load_dotenv(path)
        return
    load_dotenv()


def get_db_variables() -> dict:
    env = os.environ
    my_vars = \
        {
            'USER': env.get('DB_USER'),
            'PASSWORD': env.get('DB_PASSWORD'),
            'HOST': env.get('DB_HOST'),
            'NAME': env.get('DB_NAME')
        }
    return my_vars
