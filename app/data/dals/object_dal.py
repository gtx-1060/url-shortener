from sqlalchemy.orm import Session

from app.exceptions import ItemNotFoundException


class ObjectDAL:

    @staticmethod
    def chk_val(val):
        if val is None:
            raise ItemNotFoundException(type(val))
        return val

    def __init__(self, session: Session):
        self.session = session
