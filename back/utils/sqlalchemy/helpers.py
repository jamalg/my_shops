from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager


@contextmanager
def session_manager(session_factor: sessionmaker):
    session = session_factor()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
