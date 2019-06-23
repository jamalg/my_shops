from flask import Flask

from back.scripts.db import db_cli
from back.scripts.redis import redis_cli


def init_app(app: Flask) -> None:
    app.cli.add_command(db_cli)
    app.cli.add_command(redis_cli)
