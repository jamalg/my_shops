from flask import Flask

from back.models import db
from back.models.user import User# noqa
from back.models.social import Like, DisLike  # noqa


def init_app(app: Flask) -> None:

    @app.teardown_request
    def remove_session(response_or_exc):
        db.session.remove()
        return response_or_exc
