import logging
from typing import Dict, Any

from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema
from back.utils.sqlalchemy.helpers import session_manager

from back.models import db
from back.models.social import Like, DisLike
from back.schemas.user import UserSchema
from back.schemas.social import LikeSchema, DisLikeSchema
from back.exceptions import _SQLAlchemyError, _SchemaLoadError

logger = logging.getLogger(__name__)
DeclarativeBase = declarative_base()


def add_one(data: Dict, schema: Schema) -> Dict:
    resource, errors = schema().load(data)
    if errors:
        raise _SchemaLoadError(errors)

    with session_manager(db.UnscopedSession) as db_session:
        try:
            db_session.add(resource)
            db_session.commit()
            logger.info(
                "Added {} to db".format(resource.__class__.__name__),
                extra={resource.primary_key_name: resource.primary_key}
            )
            return schema().dump(resource).data
        except exc.SQLAlchemyError as e:
            raise _SQLAlchemyError(str(e))


def delete_one(model: DeclarativeBase, primary_key: Any) -> None:
    with session_manager(db.UnscopedSession) as db_session:
        try:
            resource = db_session.query(model).get(primary_key)
            db_session.delete(resource)
            db_session.commit()
            logger.info(
                "Deleted {} from db".format(resource.__class__.__name__),
                extra={resource.primary_key_name: resource.primary_key}
            )
        except exc.SQLAlchemyError as e:
            raise _SQLAlchemyError(str(e))


def add_user(user_data: Dict) -> int:
    return add_one(user_data, UserSchema)


def add_like(like_data: Dict) -> int:
    return add_one(like_data, LikeSchema)


def add_dislike(dislike_data: Dict) -> int:
    return add_one(dislike_data, DisLikeSchema)


def delete_like(like_id: int) -> None:
    return delete_one(Like, like_id)


def delete_dislike(dislike_id: int) -> None:
    return delete_one(DisLike, dislike_id)
