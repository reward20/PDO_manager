from sqlalchemy.orm import (
    Session,
    sessionmaker,
)


__all__ = [
    "DbConnect",
]


class DbConnect(object):
    
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def __enter__(self):
        self.session = self._session_maker()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
      