from flask import jsonify
from requests import Response


class GoogleApiError(Exception):

    def __init__(self, message, data=None):
        self.message = message
        self.data = data

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)

    @classmethod
    def from_http_response(cls, response: Response) -> Exception:
        if response.headers["content-type"].startswith("application/json"):
            return cls(message=response.reason, data=response.json())
        return cls(message=response.reason)

    @staticmethod
    def error_handler(error) -> Response:
        return jsonify({"message": error.message}), 400
