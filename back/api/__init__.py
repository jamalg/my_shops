from flask import Flask

from back.api.auth import bp as auth_bp, login_manager
from back.api.me import bp as me_bp
from back.api.status import bp as status_bp
from back.api.user import bp as user_bp
from back.api.photo import bp as photo_bp
from back.api.place import bp as place_bp


def init_app(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(place_bp)
    app.register_blueprint(photo_bp)

    login_manager.init_app(app)
