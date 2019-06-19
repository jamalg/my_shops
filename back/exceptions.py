import logging
from typing import Optional

from flask import Flask, jsonify

logger = logging.getLogger(__name__)


class CustomError(Exception):
    CODE = 500
    PUBLIC_MESSAGE = "Internal Server Error"
    LOG_ERROR = True

    def __init__(self, message: str, data: Optional[dict] = None) -> None:
        self.message = message
        self.data = data
        if self.LOG_ERROR:
            logger.error(self, extra=self.data)

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)

    @staticmethod
    def error_handler(error):
        return jsonify({"message": error.PUBLIC_MESSAGE}), error.CODE


class _SQLAlchemyError(CustomError):
    CODE = 500
    PUBLIC_MESSAGE = "Internal Server Error"


class _SchemaLoadError(CustomError):
    CODE = 400
    PUBLIC_MESSAGE = "Bad data"


class _SecurityError(CustomError):
    CODE = 400
    PUBLIC_MESSAGE = "Bad data"


def init_app(app: Flask) -> None:
    app.register_error_handler(CustomError, CustomError.error_handler)
