import os

import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from alembic import command
from alembic.config import Config

from back.app import create_app
from back.models import db
from back.test import utils


DATA_PATH = "{}/test/data".format(os.path.abspath("."))
test_app = create_app()
test_app.app_context().push()


def read_json_from_data_folder(file_name):
    return utils.read_json("{}/{}.json".format(DATA_PATH, file_name))


@pytest.fixture()
def client():
    yield test_app.test_client()


@pytest.fixture(scope="function", autouse=True)
def db_session():
    connection = db.engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(bind=connection)

    # Monkey-patch the session
    db.UnscopedSession = TestSession
    db.session = scoped_session(TestSession)

    db_session = TestSession()
    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def create_db():
    alembic_config = Config("{}/alembic.ini".format(os.path.abspath(".")))
    with db.engine.connect() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    yield

    with db.engine.connect() as connection:
        alembic_config.attributes["connection"] = connection
        command.downgrade(alembic_config, "base")


@pytest.fixture()
def user_data():
    return read_json_from_data_folder("user_data")


@pytest.fixture()
def like_data():
    return read_json_from_data_folder("like_data")


@pytest.fixture()
def dislike_data():
    return read_json_from_data_folder("dislike_data")


@pytest.fixture()
def place_data():
    return read_json_from_data_folder("place_data")
