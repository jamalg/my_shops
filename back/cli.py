from flask import Flask

from back.scripts.db import db_cli


def init_app(app: Flask) -> None:
    app.cli.add_command(db_cli)
