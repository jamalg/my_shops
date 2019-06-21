from flask import Flask

from back.extensions.google.client import GoogleCloudApi
from back.extensions.google.exceptions import GoogleApiError

google_client = GoogleCloudApi()


def init_app(app: Flask) -> None:
    google_client.api_key = app.config["GOOGLE_CLOUD_API_KEY"]
    google_client.output = app.config["GOOGLE_CLOUD_DEFAULT_OUTPUT"]
    app.register_error_handler(GoogleApiError, GoogleApiError.error_handler)
