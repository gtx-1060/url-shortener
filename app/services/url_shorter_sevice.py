from hashids import Hashids

hashids = Hashids()


def get_short_url_part(url_id: int):
    return hashids.encode(url_id)
