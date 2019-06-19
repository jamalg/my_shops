from marshmallow import fields

from back.schemas.base import BaseSchema
from back.models.social import Like, DisLike


def non_empty_string(value: str) -> bool:
    return bool(value)


class SocialSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    place_id = fields.String(required=True, allow_none=False, validate=non_empty_string)
    user_id = fields.Integer(required=True, allow_none=False, validate=non_empty_string)


class LikeSchema(SocialSchema):
    __model__ = Like


class DisLikeSchema(SocialSchema):
    __model__ = DisLike
