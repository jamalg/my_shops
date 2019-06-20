from flask import Flask

from back import config, models, exceptions, auth, api, cli
from back.extensions import google


def create_app() -> Flask:
    app = Flask(__name__)

    config.init_app(app)
    auth.init_app(app)
    api.init_app(app)
    exceptions.init_app(app)
    models.init_app(app)
    cli.init_app(app)
    google.init_app(app)

    return app
