import json

from marshmallow import fields

from back.models.user import User
from back.models import helper


def test_post_user(client, user_data, db_session):
    assert db_session.query(User).all() == []

    response = client.post("/api/users", json=user_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 201

    assert db_session.query(User).get(data["id"])


def test_post_with_empty_json(client, user_data, db_session):
    assert db_session.query(User).all() == []

    response = client.post("/api/users", json={})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["message"] == "Empty json payload"

    assert db_session.query(User).all() == []


def test_post_with_bad_data(client, user_data, db_session):
    assert db_session.query(User).all() == []

    modified_data = {**user_data, "email": "Not valid"}
    response = client.post("/api/users", json=modified_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["email"][0] == fields.Email.default_error_messages["invalid"]

    assert db_session.query(User).all() == []


def test_post_user_with_existing_email(client, user_data, db_session):
    helper.add_user(user_data)

    response = client.post("/api/users", json=user_data)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "already used" in data["email"]
