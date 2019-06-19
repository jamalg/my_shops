from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from back.config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
UnscopedSession = sessionmaker(bind=engine)
session = scoped_session(UnscopedSession, scopefunc=_app_ctx_stack.__ident_func__)
