import pytest

from back.models import helper
from back.models.user import User

from back.exceptions import _SchemaLoadError


def test_add_user(user_data, db_session):
    assert db_session.query(User).all() == []

    user_id = helper.add_user(user_data)["id"]

    assert db_session.query(User).get(user_id)


def test_add_user_bad_email(user_data, db_session):
    assert db_session.query(User).all() == []

    with pytest.raises(_SchemaLoadError):
        helper.add_user({**user_data, "email": "Not valid email"})

    assert db_session.query(User).all() == []
