from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from back.models.base import Base
from back.auth import flask_bcrypt


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    email = Column(String(512), nullable=False, unique=True, index=True)
    password_hash = Column(String(60), nullable=False)

    likes = relationship("Like")
    dislikes = relationship("DisLike")

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)
