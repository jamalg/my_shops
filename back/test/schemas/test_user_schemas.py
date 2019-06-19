from marshmallow import fields

from back.schemas.user import UserSchema


def test_user_schema(user_data):
    user, errors = UserSchema().load(user_data)
    assert errors == {}
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.email == user_data["email"]
    assert user.password_hash != user_data["password"]


def test_required_values():
    _, errors = UserSchema().load({})
    assert len(errors["email"]) == 1 and "required" in errors["email"][0]
    assert len(errors["password"]) == 1 and "required" in errors["password"][0]


def test_email_validation(user_data):
    _, errors = UserSchema().load({**user_data, "email": "Not valid"})
    assert errors["email"][0] == fields.Email.default_error_messages["invalid"]
