import pytest

from back.models import helper
from back.models.social import Like, DisLike
from back.exceptions import _SchemaLoadError


def test_add_like(user_data, like_data, db_session):
    assert db_session.query(Like).all() == []

    user_id = helper.add_user(user_data)["id"]
    like_data["user_id"] = user_id
    like_id = helper.add_like(like_data)["id"]

    assert db_session.query(Like).get(like_id)


def test_add_like_missing_data(user_data, like_data, db_session):
    assert db_session.query(Like).all() == []

    user_id = helper.add_user(user_data)["id"]
    like_data["user_id"] = user_id

    # Missing user_id
    with pytest.raises(_SchemaLoadError):
        helper.add_like({"place_id": like_data["place_id"]})
    assert db_session.query(Like).all() == []

    # Missing place_id
    with pytest.raises(_SchemaLoadError):
        helper.add_like({"user_id": like_data["user_id"]})
    assert db_session.query(Like).all() == []


def test_delete_like(user_data, like_data, db_session):
    user_id = helper.add_user(user_data)["id"]
    like_data["user_id"] = user_id

    like_id = helper.add_like(like_data)["id"]
    assert db_session.query(Like).get(like_id)

    helper.delete_like(like_id)

    assert db_session.query(Like).get(like_id) is None


def test_add_dislike(user_data, dislike_data, db_session):
    assert db_session.query(DisLike).all() == []

    user_id = helper.add_user(user_data)["id"]
    dislike_data["user_id"] = user_id
    dislike_id = helper.add_dislike(dislike_data)["id"]

    assert db_session.query(DisLike).get(dislike_id)


def test_add_dislike_missing_data(user_data, dislike_data, db_session):
    assert db_session.query(DisLike).all() == []

    user_id = helper.add_user(user_data)["id"]
    dislike_data["user_id"] = user_id

    # Missing user_id
    with pytest.raises(_SchemaLoadError):
        helper.add_dislike({"place_id": dislike_data["place_id"]})
    assert db_session.query(DisLike).all() == []

    # Missing place_id
    with pytest.raises(_SchemaLoadError):
        helper.add_dislike({"user_id": dislike_data["user_id"]})
    assert db_session.query(DisLike).all() == []


def test_delete_dislike(user_data, dislike_data, db_session):
    user_id = helper.add_user(user_data)["id"]
    dislike_data["user_id"] = user_id

    dislike_id = helper.add_dislike(dislike_data)["id"]
    assert db_session.query(DisLike).get(dislike_id)

    helper.delete_dislike(dislike_id)

    assert db_session.query(DisLike).get(dislike_id) is None
