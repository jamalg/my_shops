from marshmallow import fields

from back.schemas.base import BaseSchema, PasswordField
from back.models.user import User


class UserSchema(BaseSchema):
    __model__ = User

    id = fields.Integer(dump_only=True)
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email(required=True)
    password_hash = PasswordField(required=True, load_from="password", load_only=True)
