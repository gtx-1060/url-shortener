from hashids import Hashids
from app.config import HOST, PORT

hashids = Hashids()


def get_short_url_part(url_id: int):
    return hashids.encode(url_id)


def format_to_url(symbols: str) -> str:
    return "http://" + HOST + "/s/" + symbols + ":" + PORT