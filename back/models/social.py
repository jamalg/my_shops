from sqlalchemy import Column, Integer, String, ForeignKey

from back.models.base import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    place_id = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class DisLike(Base):
    __tablename__ = "dislikes"

    id = Column(Integer, primary_key=True)
    place_id = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
