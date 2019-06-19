import logging
from typing import Dict

from marshmallow import Schema, post_load, fields

from back.auth import flask_bcrypt

OBFUSCATED_PASSWORD = "*" * 10
logger = logging.getLogger(__name__)


class BaseSchema(Schema):
    __model__ = None

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_object(self, data: Dict) -> object:
        if self.__model__ is None or self.partial:
            return data
        return self.__model__(**data)


class PasswordField(fields.Field):

    def __init__(self, *args, **kwargs) -> None:
        load_only = kwargs.pop("load_only", None)
        if load_only is False:
            logger.warning("Password fields badly set to load_only=False")
        super().__init__(*args, **kwargs, load_only=True)

    def _serialize(self, *args, **kwargs) -> str:
        logger.warning("Attempt to deserialize password field")
        return OBFUSCATED_PASSWORD

    def _deserialize(self, value: str, attr: str, data: dict) -> str:
        return flask_bcrypt.generate_password_hash(value).decode()
