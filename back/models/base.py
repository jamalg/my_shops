from sqlalchemy import Column, MetaData
from sqlalchemy.ext.declarative import declarative_base

from back.utils.sqlalchemy import types, functions

# Convention for naming constraints so that Alembic can track them
convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}
meta = MetaData(naming_convention=convention)


class Base:
    created_at = Column(types.UTCDateTime, server_default=functions.utcnow())
    updated_at = Column(types.UTCDateTime, server_default=functions.utcnow(), onupdate=functions.utcnow())

    @property
    def primary_key_name(self):
        return self.__class__.__table__.primary_key.columns.values()[0].name

    @property
    def primary_key(self):
        return getattr(self, self.primary_key_name)


Base = declarative_base(cls=Base, metadata=meta)
