import base58
from time import time

from app.data.dals.url_dal import UrlDAL
from app.data.db.db import SyncSessionLocal


class UrlShorter:
    __generated_urls = set()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UrlShorter, cls).__new__(cls)
            cls.instance.__load_short_urls()
        return cls.instance

    def get_short_url_part(self):
        short_url = UrlShorter.__generate_hash()
        extra_salt = 2
        while short_url in self.__generated_urls:
            short_url = UrlShorter.__generate_hash(extra_salt)
            extra_salt += 2
        self.__generated_urls.add(short_url)
        return short_url

    def __load_short_urls(self):
        db = SyncSessionLocal()
        dal = UrlDAL(db)
        self.__generated_urls.update(dal.get_all_short_urls())
        db.close()

    @staticmethod
    def __generate_hash(extra_salt=0):
        tnow = int((time() * 100) % 100000000) + extra_salt
        return base58.b58encode_int(tnow)

