from sqlalchemy.orm import Session


class ObjectDAL:

    def __init__(self, session: Session):
        self.session = session
