from sqlalchemy.orm import Session

from models import session as _orm_session


def get_db_session() -> Session:
    return _orm_session
