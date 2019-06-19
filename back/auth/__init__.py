from flask import Flask
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


def init_app(app: Flask) -> None:
    flask_bcrypt.init_app(app)
