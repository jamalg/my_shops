import json

import pytest
from marshmallow import fields

from back.models import helper
from back.api import me
from back.models.user import User
from back.models.social import Like
from back.exceptions import _SecurityError


@pytest.fixture()
def current_user(user_data, like_data, dislike_data, db_session):
    user_id = helper.add_user(user_data)["id"]
    helper.add_like({**like_data, "user_id": user_id})
    helper.add_dislike({**dislike_data, "user_id": user_id})

    user = db_session.query(User).get(user_id)

    old_current_user = me.current_user
    me.current_user = user
    yield user
    me.current_user = old_current_user


@pytest.fixture()
def other_user(user_data, like_data, dislike_data, db_session):
    user_id = helper.add_user({**user_data, "email": "new@mailbox.com"})["id"]
    helper.add_like({**like_data, "user_id": user_id})
    helper.add_dislike({**dislike_data, "user_id": user_id})

    user = db_session.query(User).get(user_id)

    yield user

    pass


def test_get_me(client, current_user):
    response = client.get("/api/me")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data["id"] == current_user.id
    assert data["first_name"] == current_user.first_name
    assert data["last_name"] == current_user.last_name
    assert data["email"] == current_user.email


def test_add_like(client, current_user, like_data, db_session):
    like_data.pop("user_id")
    response = client.post("/api/me/likes", json=like_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert data["place_id"] == like_data["place_id"]
    assert data["user_id"] == current_user.id

    assert db_session.query(Like).get(data["id"])


def test_add_like_bad_user_id(client, current_user, like_data, db_session):
    like_data["user_id"] = 345
    response = client.post("/api/me/likes", json=like_data)
    data = json.loads(response.data.decode())
    assert response.status_code == _SecurityError.CODE
    assert data["message"] == _SecurityError.PUBLIC_MESSAGE


def test_add_like_bad_data(client, current_user, like_data, db_session):
    # Empty payload
    response = client.post("/api/me/likes", json={})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["message"] == "Empty json payload"

    # Bad place_id
    like_data["user_id"] = current_user.id
    like_data["place_id"] = 345
    response = client.post("/api/me/likes", json=like_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert len(data["place_id"]) == 1 and data["place_id"][0] == fields.String.default_error_messages["invalid"]


def test_add_dislike(client, current_user, dislike_data, db_session):
    dislike_data.pop("user_id")
    response = client.post("/api/me/dislikes", json=dislike_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert data["place_id"] == dislike_data["place_id"]
    assert data["user_id"] == current_user.id

    assert db_session.query(Like).get(data["id"])


def test_add_dislike_bad_user_id(client, current_user, dislike_data, db_session):
    dislike_data["user_id"] = 345
    response = client.post("/api/me/dislikes", json=dislike_data)
    data = json.loads(response.data.decode())
    assert response.status_code == _SecurityError.CODE
    assert data["message"] == _SecurityError.PUBLIC_MESSAGE


def test_add_dislike_bad_data(client, current_user, dislike_data, db_session):
    # Empty payload
    response = client.post("/api/me/dislikes", json={})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["message"] == "Empty json payload"

    # Bad place_id
    dislike_data["user_id"] = current_user.id
    dislike_data["place_id"] = 345
    response = client.post("/api/me/dislikes", json=dislike_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert len(data["place_id"]) == 1 and data["place_id"][0] == fields.String.default_error_messages["invalid"]


def test_delete_like(client, current_user, db_session):
    response = client.delete("/api/me/likes/{}".format(current_user.likes[0].id))
    assert response.status_code == 200
    db_session.expunge(current_user.likes[0])
    assert current_user.likes[0].id
    assert db_session.query(Like).get(current_user.likes[0].id) is None


def test_delete_other_user_like(client, current_user, other_user, db_session):
    response = client.delete("/api/me/likes/{}".format(other_user.likes[0].id))
    data = json.loads(response.data.decode())
    assert response.status_code == _SecurityError.CODE
    assert data["message"] == _SecurityError.PUBLIC_MESSAGE
    db_session.expunge(other_user.likes[0])
    assert other_user.likes[0].id
    assert db_session.query(Like).get(other_user.likes[0].id)


def test_delete_none_existant_like(client, current_user):
    response = client.delete("/api/me/likes/354435")
    data = json.loads(response.data.decode())
    assert response.status_code == 404
    assert data["message"] == "Not found"
