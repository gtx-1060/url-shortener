import base64

from app.config import HOST, PORT


def get_short_url_part(obj_id: int):
    return base64.urlsafe_b64encode(str(100+obj_id).encode()).decode().replace('=', '0')


def format_to_url(symbols: str):
    return "http://" + HOST + "/s/" + symbols + ":" + PORT, symbols